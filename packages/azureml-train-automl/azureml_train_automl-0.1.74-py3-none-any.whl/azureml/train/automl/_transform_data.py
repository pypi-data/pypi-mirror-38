# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Holding the preprocess functions."""
import pandas as pd
import scipy
from azureml.train.automl._preprocessorcontexts import (RawDataContext,
                                                        TransformedDataContext)
from automl.client.core.common.preprocess import (DataTransformer,
                                                  LaggingTransformer)
from automl.client.core.common.exceptions import (DataException,
                                                  ServiceException)


def _transform_data(raw_data_context, preprocess=False, logger=None):
    """
    Transform input data from RawDataContext to TransformedDataContext.

    :param raw_data_context: The raw input data.
    :type raw_data_context: RawDataContext
    :param preprocess: The switch controls the preprocess.
    :type preprocess: bool
    :param logger: The logger
    :type logger: logger
    """
    if logger:
        logger.info("Pre-processing user data")

    transformed_data_context = TransformedDataContext(X=raw_data_context.X,
                                                      y=raw_data_context.y,
                                                      X_valid=raw_data_context.X_valid,
                                                      y_valid=raw_data_context.y_valid,
                                                      sample_weight=raw_data_context.sample_weight,
                                                      sample_weight_valid=raw_data_context.sample_weight_valid,
                                                      x_raw_column_names=raw_data_context.x_raw_column_names,
                                                      cv_splits_indices=raw_data_context.cv_splits_indices)

    x_is_sparse = scipy.sparse.issparse(transformed_data_context.X)
    if preprocess is False or preprocess == "False" or x_is_sparse:
        transformed_data_context._set_transformer(x_transformer=None, lag_transformer=None)
        return transformed_data_context

    transformer, lag_transformer = None, None
    try:
        transformed_data_context.X = _add_raw_column_names_to_X(raw_data_context.x_raw_column_names,
                                                                transformed_data_context.X)
        transformer, transformed_data_context.X = _get_transformer_x(transformed_data_context.X,
                                                                     transformed_data_context.y,
                                                                     raw_data_context.task_type,
                                                                     logger)
    except ValueError:
        raise Exception(
            "Cannot preprocess training data. Run after processing manually.")

    if transformed_data_context.X_valid is not None:
        try:
            transformed_data_context.X_valid = _add_raw_column_names_to_X(raw_data_context.x_raw_column_names,
                                                                          transformed_data_context.X_valid)
            transformed_data_context.X_valid = transformer.transform(transformed_data_context.X_valid)
        except ValueError:
            raise Exception(
                "Cannot preprocess validation data. Run after processing manually.")

    # todo can probably be moved to a helper
    if raw_data_context.lag_length is not None and raw_data_context.lag_length > 0:
        lag_transformer = LaggingTransformer(raw_data_context.lag_length)
        transformed_data_context.X = lag_transformer.fit_transform(transformed_data_context.X)
        if transformed_data_context.X_valid is not None:
            transformed_data_context.X_valid = lag_transformer.fit_transform(transformed_data_context.X_valid)
        if logger:
            logger.info(
                "lagging transformer is enabled with length {}.".format(raw_data_context.lag_length))

    transformed_data_context._set_transformer(transformer, lag_transformer)

    if isinstance(transformed_data_context.X, pd.DataFrame):
        # X should be a numpy array
        transformed_data_context.X = transformed_data_context.X.values

    return transformed_data_context


def _get_transformer_x(x, y, task_type, logger=None):
    """
    Given data, compute transformations and transformed data

    :param x: input data
    :param y: labels
    :param task_type: one of the tasks defined in constants.Tasks
    :param logger: logger object for logging data from pre-processing
    :return: transformer, transformed_x
    """

    dt = DataTransformer(task_type)
    x_transform = dt.fit_transform_with_logger(x, y, logger)

    return dt, x_transform


def _add_raw_column_names_to_X(x_raw_column_names, X):
    """
    Add raw column names to X

    :param x_raw_column_names: List of raw column names
    :param X: dataframe / array
    :raise ValueError if number of raw column names is not same as the number of columns in X
    :return: Dataframe with column names
    """
    # Combine the raw feature names with X
    if x_raw_column_names is not None:
        if x_raw_column_names.shape[0] != X.shape[1]:
            raise DataException("Number of raw column names " + x_raw_column_names.shape[0] +
                                "and number of columns in input data " + X.shape[1] + " do not match")

        X_with_raw_columns = pd.DataFrame(
            data=X, columns=x_raw_column_names.tolist())

        return X_with_raw_columns

    return X
