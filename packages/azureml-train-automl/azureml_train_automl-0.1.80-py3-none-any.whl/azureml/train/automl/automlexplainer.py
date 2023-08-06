# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The AutoML Model Explainer."""

from .ensemble import Ensemble
from .utilities import _convert_explanation


def explain_model(fitted_model, X_train, X_test, features=None, **kwargs):
    """
    Explain the model with provided X_train and X_test data
    :param fitted_model: fitted AutoML model to explain.
    :type fitted_model: sklearn.pipeline
    :Param X_train: A matrix of feature vector examples for initializing the explainer.
    :type X_train: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
    :Param X_test: A matrix of feature vector examples on which to explain the model's output.
    :type X_test: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
    :param features: A list of feature names.
    :type features: list[str]
    :return: The model's explanation
    :return: tuple(shap_values, expected_values, overall_summary, overall_imp,
        per_class_summary and per_class_imp)
        where
        - shap_values = For regression model, this returns a matrix of feature importance values.
        For classification model, the dimension of this matrix is (# examples x # features).
        - expected_values = The expected value of the model applied to the set of initialization examples.
        - overall_summary = The model level feature importance values sorted in descending order.
        - overall_imp = The feature names sorted in the same order as in overall_summary or the indexes
        that would sort overall_summary.
        - per_class_summary = The class level feature importance values sorted in descending order when
        classification model is evaluated. Only available for the classification case.
        - per_class_imp = The feature names sorted in the same order as in per_class_summary or the indexes
        that would sort per_class_summary. Only available for the classification case.
        :rtype: (Union[list, list[list]], list, list, list, list, list)
    """

    try:
        from azureml.explain.model._internal import TabularExplainer

        # Transform the dataset for datatransformer and laggingtransformer only
        # Ensembling pipeline may group the miro pipelines into one step
        for name, transformer in fitted_model.steps[:-1]:
            if (transformer is not None) and (name == "datatransformer" or name == "laggingtransformer"):
                X_train = transformer.transform(X_train)
                X_test = transformer.transform(X_test)
                if name == "datatransformer":
                    features = transformer.get_engineered_feature_names()

        # To explain the pipeline which should exclude datatransformer and laggingtransformer
        fitted_model = Ensemble._transform_single_fitted_pipeline(fitted_model)

        # Create the TabularExplainer to explain the model
        explainer = TabularExplainer()

        # Explain the model and save the explanation information to artifact
        explanation = explainer.explain_model(fitted_model, X_train, X_test, features, **kwargs)

        return _convert_explanation(explanation)
    except ImportError as import_error:
        raise import_error


def retrieve_model_explanation(child_run):
    """
    Retrieve the model explanation from the Runhistory
    :param child_run: the run object corresponding to best pipeline
    :type child_run: azureml.core.run.Run
    :return: tuple(shap_values, expected_values, overall_summary, overall_imp,
    per_class_summary and per_class_imp)
    where
    - shap_values = For regression model, this returns a matrix of feature importance values.
    For classification model, the dimension of this matrix is (# examples x # features).
    - expected_values = The expected value of the model applied to the set of initialization examples.
    - overall_summary = The model level feature importance values sorted in descending order.
    - overall_imp = The feature names sorted in the same order as in overall_summary or the indexes
    that would sort overall_summary.
    - per_class_summary = The class level feature importance values sorted in descending order when
    classification model is evaluated. Only available for the classification case.
    - per_class_imp = The feature names sorted in the same order as in per_class_summary or the indexes
    that would sort per_class_summary. Only available for the classification case.
    :rtype: (Union[list, list[list]], list, list, list, list, list)
    """
    try:
        from azureml.explain.model._internal.results import get_model_explanation, get_model_summary

        # Get the (shap values,expected values) first
        explanation = get_model_explanation(child_run)
        # Get explanation summary information
        explanation = explanation + get_model_summary(child_run)
        return _convert_explanation(explanation)
    except ImportError as import_error:
        raise import_error
