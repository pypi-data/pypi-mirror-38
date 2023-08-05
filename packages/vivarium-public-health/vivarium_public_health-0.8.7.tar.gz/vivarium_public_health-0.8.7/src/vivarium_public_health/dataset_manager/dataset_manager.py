"""A vivarium plugin for managing complex data."""
from pathlib import Path
from typing import Union, Sequence

import pandas as pd
from vivarium.config_tree import ConfigTree
from vivarium.framework.engine import Builder

from vivarium_public_health.dataset_manager import Artifact


_Filter = Union[str, int, Sequence[int], Sequence[str]]


class ArtifactManagerInterface:
    """The builder interface for accessing a data artifact."""
    def __init__(self, controller):
        self._controller = controller

    def load(self, entity_key: str, keep_age_group_edges: bool=True, **column_filters: _Filter) -> pd.DataFrame:
        """Loads data associated with a formatted entity key.

        The provided entity key must be of the form
        {entity_type}.{measure} or {entity_type}.{entity_name}.{measure}.

        Here entity_type denotes the kind of entity being described. Examples
        include cause, risk, population, and covariates.

        The entity_name is the name of the specific entity. For example,
        if we had entity_type as cause, we might have entity_name as
        diarrheal_diseases or ischemic_heart_disease.

        Finally, measure is the name of the quantity the data describes.
        Examples of measures are incidence, disability_weight, relative_risk,
        and cost.

        Parameters
        ----------
        entity_key :
            The key associated with the expected data.
        keep_age_group_edges :
            A flag that says whether the data should come back with the edges of
            the age bins in addition to the the age group midpoints.
        column_filters :
            Filters that subset the data by a categorical column and then remove the
            column from the raw data. They are supplied as keyword arguments to the
            load method in the form "column=value".

        Returns
        -------
            The data associated with the given key filtered down to the requested subset.
        """
        return self._controller.load(entity_key, keep_age_group_edges, **column_filters)


class ArtifactManager:
    """The controller plugin component for managing a data artifact."""

    configuration_defaults = {
        'input_data': {
            'artifact_path': None,
        }
    }

    def setup(self, builder: Builder):
        """Performs this component's simulation setup."""
        self.artifact = self._load_artifact(builder.configuration)

    def _load_artifact(self, configuration: ConfigTree) -> Artifact:
        """Looks up the path to the artifact hdf file, builds a default filter, and generates the data artifact.

        Parameters
        ----------
        configuration :
            Configuration block of the model specification containing the input data parameters.

        Returns
        -------
            An interface to the data artifact.
        """
        artifact_path = parse_artifact_path_config(configuration)
        draw = configuration.input_data.input_draw_number
        location = configuration.input_data.location
        base_filter_terms = [f'draw == {draw}', get_location_term(location)]
        return Artifact(artifact_path, base_filter_terms)

    def load(self, entity_key: str, keep_age_group_edges: bool=True, **column_filters: _Filter):
        """Loads data associated with the given entity key.

        Parameters
        ----------
        entity_key :
            The key associated with the expected data.
        keep_age_group_edges :
            A flag that says whether the data should come back with the edges of
            the age bins in addition to the the age group midpoints.
        column_filters :
            Filters that subset the data by a categorical column and then remove the
            column from the raw data. They are supplied as keyword arguments to the
            load method in the form "column=value".

        Returns
        -------
            The data associated with the given key, filtered down to the requested subset
            if the data is a dataframe.
        """
        data = self.artifact.load(entity_key)
        return filter_data(data, keep_age_group_edges, **column_filters) if isinstance(data, pd.DataFrame) else data


def filter_data(data: pd.DataFrame, keep_age_group_edges: bool, **column_filters: _Filter) -> pd.DataFrame:
    """Uses the provided column filters and age_group conditions to subset the raw data."""
    data = _subset_rows(data, **column_filters)
    data = _subset_columns(data, keep_age_group_edges, **column_filters)
    return data


def _subset_rows(data: pd.DataFrame, **column_filters: _Filter) -> pd.DataFrame:
    """Filters out unwanted rows from the data using the provided filters."""
    extra_filters = set(column_filters.keys()) - set(data.columns)
    if extra_filters:
        raise ValueError(f"Filtering by non-existent columns: {extra_filters}. "
                         f"Available columns: {data.columns}")

    for column, condition in column_filters.items():
        if column in data.columns:
            if not isinstance(condition, (list, tuple)):
                condition = [condition]
            mask = pd.Series(False, index=data.index)
            for c in condition:
                mask |= data[f"{column}"] == c
            row_indexer = data[mask].index
            data = data.loc[row_indexer, :]

    return data


def _subset_columns(data: pd.DataFrame, keep_age_group_edges: bool, **column_filters) -> pd.DataFrame:
    """Filters out unwanted columns and default columns from the data using provided filters."""
    columns_to_remove = set(list(column_filters.keys()) + ['draw', 'location'])
    if not keep_age_group_edges:
        columns_to_remove |= {"age_group_start", "age_group_end"}

    columns_to_remove = columns_to_remove.intersection(data.columns)
    return data.drop(columns=columns_to_remove)


def get_location_term(location: str) -> str:
    """Generates a location filter term from a location name."""
    template = "location == {quote_mark}{loc}{quote_mark} | location == {quote_mark}Global{quote_mark}"
    if "'" in location and '"' in location:  # Because who knows
        raise NotImplementedError(f"Unhandled location string {location}")
    elif "'" in location:
        quote_mark = '"'
    else:
        quote_mark = "'"

    return template.format(quote_mark=quote_mark, loc=location)


def parse_artifact_path_config(config: ConfigTree) -> str:
    """Gets the path to the data artifact from the simulation configuration.

    The path specified in the configuration may be absolute or it may be relative
    to the location of the configuration file.

    Parameters
    ----------
    config :
        The configuration block of the simulation model specification containing the artifact path.

    Returns
    -------
        The path to the data artifact.
    """
    path = Path(config.input_data.artifact_path)

    if not path.is_absolute():

        path_config = config.input_data.metadata('artifact_path')[-1]
        if path_config['source'] is None:
            raise ValueError("Insufficient information provided to find artifact.")
        path = Path(path_config['source']).parent.joinpath(path)

    if not path.exists():
        raise FileNotFoundError(f"Cannot find artifact at path {path}")

    return str(path)

