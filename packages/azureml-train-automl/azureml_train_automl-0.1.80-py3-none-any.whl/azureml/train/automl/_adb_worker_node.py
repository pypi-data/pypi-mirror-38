# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import importlib
import json
import logging
import os
import threading
from datetime import datetime

import numpy as np
import pytz
from azureml._restclient import JasmineClient
from azureml.core import Run
from azureml.core.authentication import AzureMlTokenAuthentication
from azureml.core.experiment import Experiment
from azureml.core.workspace import Workspace
from azureml.train.automl import extract_user_data, fit_pipeline

from automl.client.core.common import metrics, pipeline_spec
from azureml.train.automl import utilities
from . import _constants_azureml, _dataprep_utilities, automl, constants
from ._automl_settings import _AutoMLSettings
from .automl import set_problem_info
from .run import AutoMLRun


class _AdbWorkerNode(object):
    """
    This code runs the experiments/iterations on the driver node.
    """

    def __init__(self,
                 parent_run_id,
                 subscription_id,
                 resource_group,
                 experiment,
                 workspace_name,
                 automl_settings,
                 aml_token,
                 service_url,
                 get_data_content,
                 dataprep_json=None
                 ):
        """
        Constructor for the _AdbWorkerNode class

        :param parent_run_id: Parent run id.
        :type parent_run_id: string
        :param subscription_id: Subscription Id.
        :type subscription_id: string
        :param resource_group: Resource group.
        :type resource_group: string
        :param experiment: Experiment object.
        :type experiment: Experiment
        :param workspace_name: Workspace name.
        :type workspace_name: string
        :param automl_settings: AutoML settings.
        :type automl_settings: _AutoMLSettings
        :param aml_token: aml token.
        :type aml_token: string
        :param service_url: service url.
        :type service_url: string
        :param get_data_content: get_data.py script contents.
        :type get_data_content: string
        :param dataprep_json: dataprep json.
        :type dataprep_json: string
        """
        self._parent_run_id = parent_run_id
        self._subscription_id = subscription_id
        self._resource_group = resource_group
        self._experiment = experiment
        self._workspace_name = workspace_name
        self._automl_settings = automl_settings
        self._dataprep_json = dataprep_json
        if self._dataprep_json:
            self._dataprep_json = self._dataprep_json.replace(
                '\\"', '"').replace('\\\\', '\\')
        self._entry_point = 'get_data.py'
        self._input_data = None
        self.fp = fit_pipeline
        self.logger = logging.getLogger('__name__')
        os.environ["AZUREML_ARM_SUBSCRIPTION"] = subscription_id
        os.environ["AZUREML_ARM_RESOURCEGROUP"] = resource_group
        os.environ["AZUREML_ARM_WORKSPACE_NAME"] = workspace_name
        os.environ["AZUREML_ARM_PROJECT_NAME"] = self._experiment.name
        os.environ["AZUREML_RUN_TOKEN"] = aml_token
        os.environ["AZUREML_SERVICE_ENDPOINT"] = service_url
        if get_data_content:
            with open(self._entry_point, 'w') as f:
                f.write(get_data_content)

    def get_data(self):
        data_dictionary = {}
        if (self._input_data is None):
            if self._dataprep_json:
                data_dictionary = _dataprep_utilities.load_dataflows_from_json(
                    self._dataprep_json)

            input = input_data(data_dictionary)
            self._input_data = input_data(utilities._format_training_data(
                user_script=self._entry_point,
                X=input.X,
                y=input.y,
                X_valid=input.X_valid,
                y_valid=input.y_valid,
                sample_weight=input.sample_weight,
                sample_weight_valid=input.sample_weight_valid,
                cv_splits_indices=input.cv_splits_indices
            ))

        return self._input_data

    def fit_iteration(self, pipeline_dto):
        run_id = pipeline_dto.childrun_id
        pipeline_id = pipeline_dto.pipeline_id

        os.environ["AZUREML_RUN_ID"] = run_id
        print("Received pipeline: {0} for run id '{1}'".format(
            pipeline_dto.pipeline_spec, run_id))
        try:
            data = self.get_data()
            child_run = Run(self._experiment,
                            run_id)
            child_run.start()
            print("{0}: Starting childrun...".format(run_id))

            if (run_id.endswith("setup")):
                set_problem_info(X=data.X,
                                 y=data.y,
                                 task_type=self._automl_settings.task_type,
                                 current_run=child_run,
                                 preprocess=self._automl_settings.preprocess
                                 )

            else:
                result = fit_pipeline(
                    child_run_metrics=child_run,
                    pipeline_script=pipeline_dto.pipeline_spec,
                    automl_settings=self._automl_settings,
                    run_id=run_id,
                    X=data.X,
                    y=data.y,
                    sample_weight=data.sample_weight,
                    X_valid=data.X_valid,
                    y_valid=data.y_valid,
                    sample_weight_valid=data.sample_weight_valid,
                    cv_splits_indices=data.cv_splits_indices,
                    experiment=self._experiment,
                    pipeline_id=pipeline_id,
                    remote=True)

                print("result : ", result)
                if len(result['errors']) > 0:
                    err_type = next(iter(result['errors']))
                    inner_ex = result['errors'][err_type]['exception']
                    raise RuntimeError(inner_ex) from inner_ex

                score = result[self._automl_settings.primary_metric]
                duration = result['fit_time']
                print("Score : ", score)
                print("Duration : ", duration)

            child_run.complete()
            print("{0}: Childrun completed successfully.".format(run_id))

        except Exception as e:
            print(e)
            if child_run:
                child_run.fail()


class input_data(object):
    def __init__(self, data_dictionary):
        if (data_dictionary is None):
            data_dictionary = {}
        self.X = data_dictionary.get('X', None)
        self.y = data_dictionary.get('y', None)
        self.X_valid = data_dictionary.get('X_valid', None)
        self.y_valid = data_dictionary.get('y_valid', None)
        self.sample_weight = data_dictionary.get('sample_weight', None)
        self.sample_weight_valid = data_dictionary.get(
            'sample_weight_valid', None)
        self.cv_splits_indices = data_dictionary.get('cv_splits_indices', None)
