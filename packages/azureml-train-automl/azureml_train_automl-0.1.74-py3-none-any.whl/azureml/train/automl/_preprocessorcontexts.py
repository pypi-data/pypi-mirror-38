# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Holding the data context classes."""


class BaseDataContext(object):
    """
    Base data context class for input raw data and output transformed data.
    """
    def __init__(self, X, y=None,
                 X_valid=None,
                 y_valid=None,
                 sample_weight=None,
                 sample_weight_valid=None,
                 x_raw_column_names=None,
                 cv_splits_indices=None):
        """
        Constructor for the BaseDataContext class

        :param X: Input training data.
        :type X: numpy.ndarray or pandas.DataFrame
        :param y: Input training labels.
        :type y: numpy.ndarray or pandas.DataFrame
        :param X_valid: validation data.
        :type X_valid: numpy.ndarray or pandas.DataFrame
        :param y_valid: validation labels.
        :type y_valid: numpy.ndarray or pandas.DataFrame
        :param sample_weight: Sample weights for training data.
        :type sample_weight: numpy.ndarray or pandas.DataFrame
        :param sample_weight_valid: validation set sample weights.
        :type sample_weight_valid: numpy.ndarray or pandas.DataFrame
        :params x_raw_column_names: raw feature names of X data.
        :type x_raw_column_names: numpy.ndarray
        :param cv_splits_indices: Custom indices by which to split the data when running cross validation.
        :type cv_splits_indices: numpy.ndarray or pandas.DataFrame
        """
        self.X = X
        self.y = y
        self.X_valid = X_valid
        self.y_valid = y_valid
        self.sample_weight = sample_weight
        self.sample_weight_valid = sample_weight_valid
        self.x_raw_column_names = x_raw_column_names
        self.cv_splits_indices = cv_splits_indices


class RawDataContext(BaseDataContext):
    """
    Input raw data context
    """
    def __init__(self,
                 task_type,
                 X,  # DataFlow or DataFrame
                 y=None,  # DataFlow or DataFrame
                 X_valid=None,  # DataFlow
                 y_valid=None,  # DataFlow
                 sample_weight=None,
                 sample_weight_valid=None,
                 lag_length=None,
                 x_raw_column_names=None,
                 cv_splits_indices=None):
        """
        Constructor for the RawDataContext class

        :param X: Input training data.
        :type X: numpy.ndarray or pandas.DataFrame
        :param y: Input training labels.
        :type y: numpy.ndarray or pandas.DataFrame
        :param X_valid: validation data.
        :type X_valid: numpy.ndarray or pandas.DataFrame
        :param y_valid: validation labels.
        :type y_valid: numpy.ndarray or pandas.DataFrame
        :param sample_weight: Sample weights for training data.
        :type sample_weight: numpy.ndarray or pandas.DataFrame
        :param sample_weight_valid: validation set sample weights.
        :type sample_weight_valid: numpy.ndarray or pandas.DataFrame
        :params x_raw_column_names: raw feature names of X data.
        :type x_raw_column_names: numpy.ndarray
        :param cv_splits_indices: Custom indices by which to split the data when running cross validation.
        :type cv_splits_indices: numpy.ndarray or pandas.DataFrame
        :param task_type: constants.Tasks.CLASSIFICATION or constants.Tasks.REGRESSION
        :type task_typ: constants.Tasks
        """
        self.lag_length = lag_length
        self.task_type = task_type
        super().__init__(X=X, y=y,
                         X_valid=X_valid,
                         y_valid=y_valid,
                         sample_weight=sample_weight,
                         sample_weight_valid=sample_weight_valid,
                         x_raw_column_names=x_raw_column_names,
                         cv_splits_indices=cv_splits_indices)


class TransformedDataContext(BaseDataContext):
    def __init__(self,
                 X,  # DataFrame
                 y=None,  # DataFrame
                 X_valid=None,  # DataFrame
                 y_valid=None,  # DataFrame
                 sample_weight=None,
                 sample_weight_valid=None,
                 x_raw_column_names=None,
                 cv_splits_indices=None):
        """
        Constructor for the TransformerDataContext class

        :param X: Input training data.
        :type X: numpy.ndarray or pandas.DataFrame
        :param y: Input training labels.
        :type y: numpy.ndarray or pandas.DataFrame
        :param X_valid: validation data.
        :type X_valid: numpy.ndarray or pandas.DataFrame
        :param y_valid: validation labels.
        :type y_valid: numpy.ndarray or pandas.DataFrame
        :param sample_weight: Sample weights for training data.
        :type sample_weight: numpy.ndarray or pandas.DataFrame
        :param sample_weight_valid: validation set sample weights.
        :type sample_weight_valid: numpy.ndarray or pandas.DataFrame
        :params x_raw_column_names: raw feature names of X data.
        :type x_raw_column_names: numpy.ndarray
        :param cv_splits_indices: Custom indices by which to split the data when running cross validation.
        :type cv_splits_indices: numpy.ndarray or pandas.DataFrame
        """
        super().__init__(X=X, y=y,
                         X_valid=X_valid,
                         y_valid=y_valid,
                         sample_weight=sample_weight,
                         sample_weight_valid=sample_weight_valid,
                         x_raw_column_names=x_raw_column_names,
                         cv_splits_indices=cv_splits_indices)
        self.transformers = dict()

    def _set_transformer(self, x_transformer=None, lag_transformer=None):
        """
        Set the x_transformer and lag_transformer.

        :param x_transformer: transformer for x transformation.
        :param lag_transformer: lag transformer.
        """
        self.transformers['x_transformer'] = x_transformer
        self.transformers['lag_transformer'] = lag_transformer
