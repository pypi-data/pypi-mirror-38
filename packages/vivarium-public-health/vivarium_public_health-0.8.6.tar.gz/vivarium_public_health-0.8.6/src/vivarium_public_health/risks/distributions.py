from typing import Dict, Callable, Tuple, Union

import numpy as np
import pandas as pd
from scipy import stats, optimize, special

from vivarium.framework.values import list_combiner, joint_value_post_processor
from vivarium_public_health.util import pivot_age_sex_year_binned
from .data_transformation import should_rebin, rebin_exposure_data


class NonConvergenceError(Exception):
    """ Raised when the optimization fails to converge """
    def __init__(self, message: str, dist: str) -> None:
        super().__init__(message)
        self.dist = dist


class MissingDataError(Exception):
    pass


def _get_optimization_result(exposure: pd.DataFrame, func: Callable,
                             initial_func: Callable) -> Tuple:
    """Finds the shape parameters of distributions which generates mean/sd close to actual mean/sd.

    Parameters
    ---------
    exposure :
        Table where each row has a `mean` and `standard_deviation` for a single distribution.
    func:
        The optimization objective function.  Takes arguments `initial guess`, `mean`, and `standard_deviation`.
    initial_func:
        Function to produce initial guess from a `mean` and `standard_deviation`.

    Returns
    --------
        A tuple of the optimization results.
    """

    mean, sd = exposure['mean'].values, exposure['standard_deviation'].values
    results = []
    with np.errstate(all='warn'):
        for i in range(len(mean)):
            initial_guess = initial_func(mean[i], sd[i])
            result = optimize.minimize(func, initial_guess, (mean[i], sd[i],), method='Nelder-Mead',
                                       options={'maxiter': 10000})
            results.append(result)
    return tuple(results)


class BaseDistribution:
    """Generic vectorized wrapper around scipy distributions."""

    distribution = None

    def __init__(self, exposure: pd.DataFrame):
        self._range = self._get_min_max(exposure)
        self._parameter_data = self._get_params(exposure)
        self._ranges_data = {'x_min': pd.DataFrame(self._range['x_min'], index=exposure.index),
                             'x_max': pd.DataFrame(self._range['x_max'], index=exposure.index)}

    def setup(self, builder):
        self.parameters = {name: builder.lookup.build_table(data.reset_index()) for name, data in
                           self._parameter_data.items()}
        self.ranges_data = {name: builder.lookup.build_table(data.reset_index()) for name, data in
                            self._ranges_data.items()}

    @staticmethod
    def _get_min_max(exposure: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Gets the upper and lower bounds of the distribution support."""
        exposure_mean, exposure_sd = exposure['mean'], exposure['standard_deviation']
        alpha = 1 + exposure_sd ** 2 / exposure_mean ** 2
        scale = exposure_mean / np.sqrt(alpha)
        s = np.sqrt(np.log(alpha))
        x_min = stats.lognorm(s=s, scale=scale).ppf(.001)
        x_max = stats.lognorm(s=s, scale=scale).ppf(.999)
        return {'x_min': x_min, 'x_max': x_max}

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        raise NotImplementedError()

    def process(self, data: Union[np.ndarray, pd.Series], process_type: str,
                ranges: Dict[str, np.ndarray]) -> Union[np.ndarray, pd.Series]:
        """Function called before and after distribution looks to handle pre- and post-processing.

        This function should look like an if sieve on the `process_type` and fall back with a call to
        this method if no processing needs to be done.

        Parameters
        ----------
        data :
            The data to be processed.
        process_type :
            One of `pdf_preprocess`, `pdf_postprocess`, `ppf_preprocess`, `ppf_post_process`.
        ranges :
            Upper and lower bounds of the distribution support.

        Returns
        -------
            The processed data.
        """
        return data

    def pdf(self, x: pd.Series, interpolation: bool=True) -> Union[np.ndarray, pd.Series]:
        if not interpolation:
            params = self._parameter_data
            ranges = self._range
        else:
            params = {name: p(x.index) for name, p in self.parameters.items()}
            ranges = {name: p(x.index) for name, p in self.ranges_data.items()}

        x = self.process(x, "pdf_preprocess", ranges)
        pdf = self.distribution(**params).pdf(x)
        return self.process(pdf, "pdf_postprocess", ranges)

    def ppf(self, x: pd.Series, interpolation: bool=True) -> Union[np.ndarray, pd.Series]:
        if not interpolation:
            params = self._parameter_data
            ranges = self._range
        else:
            params = {name: p(x.index) for name, p in self.parameters.items()}
            ranges = {name: p(x.index) for name, p in self.ranges_data.items()}

        x = self.process(x, "ppf_preprocess", ranges)
        ppf = self.distribution(**params).ppf(x)
        return self.process(ppf, "ppf_postprocess", ranges)


class Beta(BaseDistribution):

    distribution = stats.beta

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        exposure_mean, exposure_sd = exposure['mean'], exposure['standard_deviation']
        scale = self._range['x_max'] - self._range['x_min']
        a = 1 / scale * (exposure_mean - self._range['x_min'])
        b = (1 / scale * exposure_sd) ** 2
        shape_1 = a ** 2 / b * (1 - a) - a
        shape_2 = a / b * (1 - a) ** 2 + (a - 1)
        params = {'scale': pd.DataFrame(scale, index=exposure.index),
                  'a': pd.DataFrame(shape_1, index=exposure.index),
                  'b': pd.DataFrame(shape_2, index=exposure.index)}
        return params

    def process(self, data: Union[np.ndarray, pd.Series], process_type: str,
                ranges: Dict[str, np.ndarray]) -> np.array:
        if process_type == 'pdf_preprocess':
            value = data - ranges['x_min']
        elif process_type == 'ppf_postprocess':
            value = data + ranges['x_max'] - ranges['x_min']
        else:
            value = super().process(data, process_type, ranges)
        return np.array(value)


class Exponential(BaseDistribution):

    distribution = stats.expon

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        return {'scale': pd.DataFrame(exposure['mean'], index=exposure.index)}


class Gamma(BaseDistribution):

    distribution = stats.gamma

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        mean, sd = exposure['mean'], exposure['standard_deviation']
        a = (mean / sd) ** 2
        scale = sd ** 2 / mean
        return {'a': pd.DataFrame(a, index=exposure.index), 'scale': pd.DataFrame(scale, index=exposure.index)}


class Gumbel(BaseDistribution):

    distribution = stats.gumbel_r

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        mean, sd = exposure['mean'], exposure['standard_deviation']
        loc = mean - (np.euler_gamma * np.sqrt(6) / np.pi * sd)
        scale = np.sqrt(6) / np.pi * sd
        return {'loc': pd.DataFrame(loc, index=exposure.index),
                'scale': pd.DataFrame(scale, index=exposure.index)}


class InverseGamma(BaseDistribution):

    distribution = stats.invgamma

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        def f(guess, mean, sd):
            alpha, beta = np.abs(guess)
            mean_guess = beta / (alpha - 1)
            var_guess = beta ** 2 / ((alpha - 1) ** 2 * (alpha - 2))
            return (mean - mean_guess) ** 2 + (sd ** 2 - var_guess) ** 2

        opt_results = _get_optimization_result(exposure, f, lambda m, s: np.array((m, m * s)))
        data_size = len(exposure)

        if not np.all([opt_results[k].success for k in range(data_size)]):
            raise NonConvergenceError('InverseGamma did not converge!!', 'invgamma')

        shape = np.abs([opt_results[k].x[0] for k in range(data_size)])
        scale = np.abs([opt_results[k].x[1] for k in range(data_size)])
        return {'a': pd.DataFrame(shape, index=exposure.index), 'scale': pd.DataFrame(scale, index=exposure.index)}


class InverseWeibull(BaseDistribution):

    distribution = stats.invweibull

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        # moments from  Stat Papers (2011) 52: 591. https://doi.org/10.1007/s00362-009-0271-3
        # it is much faster than using stats.invweibull.mean/var
        def f(guess, mean, sd):
            shape, scale = np.abs(guess)
            mean_guess = scale * special.gamma(1 - 1 / shape)
            var_guess = scale ** 2 * special.gamma(1 - 2 / shape) - mean_guess ** 2
            return (mean - mean_guess) ** 2 + (sd ** 2 - var_guess) ** 2

        opt_results = _get_optimization_result(exposure, f, lambda m, s: np.array((max(2.2, s / m), m)))
        data_size = len(exposure)

        if not np.all([opt_results[k].success for k in range(data_size)]):
            raise NonConvergenceError('InverseWeibull did not converge!!', 'invweibull')

        shape = np.abs([opt_results[k].x[0] for k in range(data_size)])
        scale = np.abs([opt_results[k].x[1] for k in range(data_size)])
        return {'c': pd.DataFrame(shape, index=exposure.index), 'scale': pd.DataFrame(scale, index=exposure.index)}


class LogLogistic(BaseDistribution):

    distribution = stats.burr12

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        def f(guess, mean, sd):
            shape, scale = np.abs(guess)
            b = np.pi / shape
            mean_guess = scale * b / np.sin(b)
            var_guess = scale ** 2 * 2 * b / np.sin(2 * b) - mean_guess ** 2
            return (mean - mean_guess) ** 2 + (sd ** 2 - var_guess) ** 2

        opt_results = _get_optimization_result(exposure, f, lambda m, s: np.array((max(2, m), m)))
        data_size = len(exposure)

        if not np.all([opt_results[k].success for k in range(data_size)]):
            raise NonConvergenceError('LogLogistic did not converge!!', 'llogis')

        shape = np.abs([opt_results[k].x[0] for k in range(data_size)])
        scale = np.abs([opt_results[k].x[1] for k in range(data_size)])
        return {'c': pd.DataFrame(shape, index=exposure.index),
                'd': pd.DataFrame([1]*len(exposure), index=exposure.index),
                'scale': pd.DataFrame(scale, index=exposure.index)}


class LogNormal(BaseDistribution):

    distribution = stats.lognorm

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        mean, sd = exposure['mean'], exposure['standard_deviation']
        alpha = 1 + sd ** 2 / mean ** 2
        s = np.sqrt(np.log(alpha))
        scale = mean / np.sqrt(alpha)
        return {'s': pd.DataFrame(s, index=exposure.index),
                'scale': pd.DataFrame(scale, index=exposure.index)}


class MirroredGumbel(BaseDistribution):

    distribution = stats.gumbel_r

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        loc = self._range['x_max'] - exposure['mean'] - (
                    np.euler_gamma * np.sqrt(6) / np.pi * exposure['standard_deviation'])
        scale = np.sqrt(6) / np.pi * exposure['standard_deviation']
        return {'loc': pd.DataFrame(loc, index=exposure.index),
                'scale': pd.DataFrame(scale, index=exposure.index)}

    def process(self, data: Union[np.ndarray, pd.Series], process_type: str,
                ranges: Dict[str, np.ndarray]) -> np.ndarray:
        if process_type == 'pdf_preprocess':
            value = ranges['x_max'] - data
        elif process_type == 'ppf_preprocess':
            value = 1 - data
        elif process_type == 'ppf_postprocess':
            value = ranges['x_max'] - data
        else:
            value = super().process(data, process_type, ranges)
        return np.array(value)


class MirroredGamma(BaseDistribution):

    distribution = stats.gamma

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        mean, sd = exposure['mean'], exposure['standard_deviation']
        a = ((self._range['x_max'] - mean) / sd) ** 2
        scale = sd ** 2 / (self._range['x_max'] - mean)
        return {'a': pd.DataFrame(a, index=exposure.index), 'scale': pd.DataFrame(scale, index=exposure.index)}

    def process(self, data: Union[np.ndarray, pd.Series], process_type: str,
                ranges: Dict[str, np.ndarray]) -> np.ndarray:
        if process_type == 'pdf_preprocess':
            value = ranges['x_max'] - data
        elif process_type == 'ppf_preprocess':
            value = 1 - data
        elif process_type == 'ppf_postprocess':
            value = ranges['x_max'] - data
        else:
            value = super().process(data, process_type, ranges)
        return np.array(value)


class Normal(BaseDistribution):

    distribution = stats.norm

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        return {'loc': pd.DataFrame(exposure['mean'], index=exposure.index),
                'scale': pd.DataFrame(exposure['standard_deviation'], index=exposure.index)}


class Weibull(BaseDistribution):

    distribution = stats.weibull_min

    def _get_params(self, exposure: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        def f(guess, mean, sd):
            shape, scale = np.abs(guess)
            mean_guess = scale * special.gamma(1 + 1 / shape)
            var_guess = scale ** 2 * special.gamma(1 + 2 / shape) - mean_guess ** 2
            return (mean - mean_guess) ** 2 + (sd ** 2 - var_guess) ** 2

        opt_results = _get_optimization_result(exposure, f, lambda m, s: np.array((m, m / s)))
        data_size = len(exposure)

        if not np.all([opt_results[k].success is True for k in range(data_size)]):
            raise NonConvergenceError('Weibull did not converge!!', 'weibull')

        shape = np.abs([opt_results[k].x[0] for k in range(data_size)])
        scale = np.abs([opt_results[k].x[1] for k in range(data_size)])
        return {'c': pd.DataFrame(shape, index=exposure.index), 'scale': pd.DataFrame(scale, index=exposure.index)}


class EnsembleDistribution:
    """Represents an arbitrary distribution as a weighted sum of several concrete distribution types."""

    def __init__(self, exposure, weights, distribution_map):
        self.weights, self._distributions = self.get_valid_distributions(exposure, weights, distribution_map)

    @staticmethod
    def get_valid_distributions(exposure: pd.DataFrame, weights: pd.Series,
                                distribution_map: Dict) -> Tuple[np.ndarray, Dict]:
        """Produces a distribution that filters out non convergence errors and rescales weights appropriately.

        Parameters
        ----------
        exposure :
            Table where each row has a `mean` and `standard_deviation` for a single distribution.
        weights :
            A list of normalized distribution weights indexed by distribution type.
        distribution_map :
            Mapping between distribution name and distribution class.

        Returns
        -------
            Rescaled weights and the subset of the distribution map corresponding to convergent distributions.
        """
        dist = dict()
        for key in distribution_map:
            try:
                dist[key] = distribution_map[key](exposure)
            except NonConvergenceError as e:
                if weights[e.dist] > 0.05:
                    weights = weights.drop(e.dist)
                else:
                    raise NonConvergenceError(f'Divergent {key} distribution has weights: {100*weights[key]}%', key)

        return weights/np.sum(weights), dist

    def setup(self, builder):
        builder.components.add_components(self._distributions.values())

    def pdf(self, x: pd.Series, interpolation: bool=True) -> Union[np.ndarray, pd.Series]:
        return np.sum([self.weights[name] * dist.pdf(x, interpolation)
                       for name, dist in self._distributions.items()], axis=0)

    def ppf(self, x: pd.Series, interpolation: bool=True) -> Union[np.ndarray, pd.Series]:
        if not x.empty:
            exposures = []
            for name, dist in self._distributions.items():
                exposures.append(self.weights[name] * dist.ppf(x, interpolation))
            return np.sum(exposures, axis=0)
        else:
            return np.array([])


class PolytomousDistribution:
    def __init__(self, exposure_data: pd.DataFrame, risk: str):
        self.exposure_data = exposure_data
        self._risk = risk
        self.categories = sorted([column for column in self.exposure_data if 'cat' in column],
                                 key=lambda column: int(column[3:]))

    def setup(self, builder):
        self.exposure = builder.value.register_value_producer(f'{self._risk}.exposure_parameters',
                                                              source=builder.lookup.build_table(self.exposure_data))

    def ppf(self, x):
        exposure = self.exposure(x.index)
        sorted_exposures = exposure[self.categories]
        if not np.allclose(1, np.sum(sorted_exposures, axis=1)):
            raise MissingDataError('All exposure data returned as 0.')
        exposure_sum = sorted_exposures.cumsum(axis='columns')
        category_index = (exposure_sum.T < x).T.sum('columns')
        return pd.Series(np.array(self.categories)[category_index], name=self._risk + '_exposure', index=x.index)


class DichotomousDistribution:
    def __init__(self, exposure_data: pd.DataFrame, risk: str):
        self.exposure_data = exposure_data.drop('cat2', axis=1)
        self._risk = risk

    def setup(self, builder):
        self._base_exposure = builder.lookup.build_table(self.exposure_data)
        self.exposure_proportion = builder.value.register_value_producer(f'{self._risk}.exposure_parameters',
                                                                         source=self.exposure)
        self.joint_paf = builder.value.register_value_producer(f'{self._risk}.paf',
                                                               source=lambda index: [pd.Series(0, index=index)],
                                                               preferred_combiner=list_combiner,
                                                               preferred_post_processor=joint_value_post_processor)

    def exposure(self, index):
        base_exposure = self._base_exposure(index).values
        joint_paf = self.joint_paf(index).values
        return base_exposure * (1-joint_paf)

    def ppf(self, x):
        exposed = x < self.exposure_proportion(x.index)

        return pd.Series(exposed.replace({True: 'cat1', False: 'cat2'}), name=self._risk + '_exposure', index=x.index)


class RebinPolytomousDistribution(DichotomousDistribution):
    pass


def get_distribution(risk: str, risk_type: str, builder):

    distribution_type = builder.data.load(f"{risk_type}.{risk}.distribution")
    exposure_data = builder.data.load(f"{risk_type}.{risk}.exposure")

    if distribution_type == "dichotomous":
        exposure_data = pivot_age_sex_year_binned(exposure_data, 'parameter', 'value')
        distribution = DichotomousDistribution(exposure_data, risk)

    elif distribution_type == 'polytomous':
        SPECIAL = ['unsafe_water_source', 'low_birth_weight_and_short_gestation']
        rebin = should_rebin(risk, builder.configuration)

        if rebin and risk in SPECIAL:
            raise NotImplementedError(f'{risk} cannot be rebinned at this point')

        if rebin:
            exposure_data = rebin_exposure_data(exposure_data)
            exposure_data = pivot_age_sex_year_binned(exposure_data, 'parameter', 'value')
            distribution = RebinPolytomousDistribution(exposure_data, risk)
        else:
            exposure_data = pivot_age_sex_year_binned(exposure_data, 'parameter', 'value')
            distribution = PolytomousDistribution(exposure_data, risk)

    elif distribution_type in ['normal', 'lognormal', 'ensemble']:
        exposure_sd = builder.data.load(f"{risk_type}.{risk}.exposure_standard_deviation")
        exposure_data = exposure_data.rename(index=str, columns={"value": "mean"})
        exposure_sd = exposure_sd.rename(index=str, columns={"value": "standard_deviation"})

        exposure = exposure_data.merge(exposure_sd).set_index(['year', 'year_start', 'year_end',
                                                               'age', 'age_group_start', 'age_group_end', 'sex'])

        if distribution_type == 'normal':
            distribution = Normal(exposure)

        elif distribution_type == 'lognormal':
            distribution = LogNormal(exposure)
        else:
            weights = builder.data.load(f'risk_factor.{risk}.ensemble_weights')
            distribution_map = {'betasr': Beta,
                                'exp': Exponential,
                                'gamma': Gamma,
                                'gumbel': Gumbel,
                                'invgamma': InverseGamma,
                                'invweibull': InverseWeibull,
                                'llogis': LogLogistic,
                                'lnorm': LogNormal,
                                'mgamma': MirroredGamma,
                                'mgumbel': MirroredGumbel,
                                'norm': Normal,
                                'weibull': Weibull}

            if risk == 'high_ldl_cholesterol':
                weights = weights.drop('invgamma', axis=1)

            if 'invweibull' in weights.columns and np.all(weights['invweibull'] < 0.05):
                weights = weights.drop('invweibull', axis=1)

            weights_cols = list(set(distribution_map.keys()) & set(weights.columns))
            weights = weights[weights_cols]

            # weight is all same across the demo groups
            e_weights = weights.iloc[0]
            dist = {d: distribution_map[d] for d in weights_cols}

            distribution = EnsembleDistribution(exposure, e_weights/np.sum(e_weights), dist)
    else:
        raise NotImplementedError(f"Unhandled distribution type {distribution}")

    return distribution
