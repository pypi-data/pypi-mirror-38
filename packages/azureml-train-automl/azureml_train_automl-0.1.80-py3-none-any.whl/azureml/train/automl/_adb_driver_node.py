# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import importlib
import json
import logging
import os
import threading
from datetime import datetime
import time

import numpy as np
import pytz
from azureml._restclient import JasmineClient
from azureml.core import Run
from azureml.core.authentication import AzureMlTokenAuthentication
from azureml.core.experiment import Experiment
from azureml.core.workspace import Workspace
from azureml.train.automl import extract_user_data, fit_pipeline

from automl.client.core.common import metrics, pipeline_spec, utilities

from . import _constants_azureml, _dataprep_utilities, automl, constants
from ._automl_settings import _AutoMLSettings
from ._adb_worker_node import _AdbWorkerNode
from .automl import set_problem_info
from .run import AutoMLRun


class _AdbDriverNode(threading.Thread):
    """
    This code initiates the experiments to be run on worker nodes by calling\
    adb map and collect.
    """

    MAX_RETRY_COUNT = 5
    SLEEP_TIME = 10

    def __init__(self, name, input_data, spark_context, partition_count):
        """
        Constructor for the _AdbDriverNode class

        :param name: Name of the experiment run.
        :param type: string
        :param input_data: Input context data for the worker node run.
        :param type: Array of tuple [(worker_id, context_dictionary),(worker_id, context_dictionary)]
        :param name: Spark context.
        :param type: spark context.
        :param name: Partition count.
        :param type: int
        """
        super(_AdbDriverNode, self).__init__()
        self.name = name
        self.input_data = input_data
        self.spark_context = spark_context
        self.partition_count = partition_count

    def run(self):
        automlRDD = self.spark_context.parallelize(
            self.input_data, self.partition_count)
        automlRDD.map(_adb_workernode_run).collect()


def _adb_workernode_run(input_params):
    """
    This method is responsible for reading run configuraiton values and call jasmine to get next
    pipeline and call fit iteration.
    """
    worker_id = input_params[0]
    run_context = input_params[1]
    subscription_id = run_context['subscription_id']
    resource_group = run_context['resource_group']
    workspace_name = run_context['workspace_name']
    location = run_context['location']
    aml_token = run_context['aml_token']
    experiment_name = run_context['experiment_name']
    parent_run_id = run_context['parent_run_id']
    dataprep_json = run_context.get('dataprep_json', None)
    service_url = run_context['service_url']
    get_data_content = run_context.get("get_data_content", None)
    auth = AzureMlTokenAuthentication(aml_token)
    # Disabling service check, as this is in remote context and we don't have an arm token
    # to check arm if the workspace exists or not.
    workspace = Workspace(subscription_id, resource_group, workspace_name,
                          auth=auth, _location=location, _disable_service_check=True)
    experiment = Experiment(workspace, experiment_name)
    automl_settings = _AutoMLSettings(
        experiment, **json.loads(run_context['automl_settings_str']))
    jasmine_client = JasmineClient.create(
        workspace, experiment.name, host=service_url)

    worker_node_estimator = _AdbWorkerNode(parent_run_id,
                                           subscription_id,
                                           resource_group,
                                           experiment,
                                           workspace_name,
                                           automl_settings,
                                           aml_token,
                                           service_url,
                                           get_data_content,
                                           dataprep_json=dataprep_json
                                           )
    print("{0}: Starting experiment run on driver node...".format(parent_run_id))
    retry_count = 0
    while (True):
        try:
            pipeline_dto = jasmine_client.get_next_pipeline(parent_run_id, worker_id)
            if pipeline_dto.is_experiment_over:
                print("Experiment already finished.")
                break
            if pipeline_dto.pipeline_spec == "":
                if pipeline_dto.retry_after > 0:
                    print("Waiting for pipelines wait for {0} seconds".format(pipeline_dto.retry_after))
                    time.sleep(pipeline_dto.retry_after)
                continue
            worker_node_estimator.fit_iteration(pipeline_dto)
            retry_count = 0
        except Exception as e:
            print(e)
            retry_count += 1
            if retry_count <= _AdbDriverNode.MAX_RETRY_COUNT:
                print("retry count:{0}, sleeping for {1} sec".format(retry_count, _AdbDriverNode.SLEEP_TIME))
                time.sleep(_AdbDriverNode.SLEEP_TIME)
            else:
                break

    print("{0}: Finished experiment run on driver node.".format(parent_run_id))
