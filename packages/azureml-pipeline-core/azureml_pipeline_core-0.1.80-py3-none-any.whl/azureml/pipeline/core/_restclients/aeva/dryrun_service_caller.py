# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""dryrun_service_calller.py, module for interacting with the AzureML service."""

import uuid
import datetime
from .service_caller_base import AE3PServiceCallerBase
from azureml.pipeline.core._restclients.aeva.models import ModuleEntity, Module, EntityInterface, DataLocation
from azureml.pipeline.core._restclients.aeva.models import PipelineCreationInfo, PipelineEntity, DataReference
from azureml.pipeline.core._restclients.aeva.models import NodePortInterface, ExperimentEntity, ExperimentStatus
from azureml.pipeline.core._restclients.aeva.models import NodeInputPort, NodeOutputPort, DataSourceEntity, NodeOutput
from azureml.pipeline.core._restclients.aeva.models import DataTypeEntity, AzureBlobReference, TaskStatus, Parameter


class DryRunServiceCaller(AE3PServiceCallerBase):
    """DryRunServiceCaller."""
    def __init__(self):
        """Initializes DryRunServiceCaller."""
        self._module_entities = {}
        self._module_hash_to_id = {}
        self._datasource_hash_to_id = {}
        self._experiment_entities = {}
        self._graph_entities = {}
        self._graph_interfaces = {}
        self._datasource_entities = {}
        self._pipeline_entities = {}
        self._datatype_entities = {}
        self._experiment_entities_from_pipelines = {}
        self._submitted_pipeline_infos = {}
        self._service_endpoint = "mock servicecaller"

    def create_datasource_async(self, creation_info):
        """CreateDataSourceAsync.

        :param creation_info: The datasource creation info
        :type creation_info: ~swaggerfixed.models.DataSourceCreationInfo
        :return: DatasetEntity
        :rtype: ~swaggerfixed.models.DatasetEntity
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock create_datasource_async')
        id = str(uuid.uuid4())
        azure_data_reference = AzureBlobReference(relative_path=creation_info.path_on_data_store,
                                                  aml_data_store_name=creation_info.data_store_name)

        data_reference = DataReference(type='1', azure_blob_reference=azure_data_reference)

        entity = DataSourceEntity(id=id, name=creation_info.name,
                                  data_type_id=creation_info.data_type_id,
                                  description=creation_info.description,
                                  data_location=DataLocation(storage_id='mock_storage_id',
                                                             data_reference=data_reference))
        self._datasource_entities[id] = entity
        if creation_info.identifier_hash is not None:
            self._datasource_hash_to_id[creation_info.identifier_hash] = id

        return entity

    def update_datasource_async(self, id, updated):
        """UpdateDataSourceAsync.

        :param id: The datasource id
        :type id: str
        :param updated: The updated datasource
        :type updated: ~swaggerfixed.models.DataSourceEntity
        :return: None
        :rtype: None
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock update_datasource_async')
        pass

    def get_datasource_async(self, id):
        """GetDataSourceAsync.

        :param id: The datasource id
        :type id: str
        :return: DatasetEntity
        :rtype: ~swaggerfixed.models.DatasetEntity
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock get_datasource_async')
        return self._datasource_entities[id]

    def get_module_async(self, id):
        """GetModuleAsync.

        :param id: The module id
        :type id: str
        :return: Module
        :rtype: ~swaggerfixed.models.Module
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock get_module_async')
        module_entity = self._module_entities[id]

        parameters = []
        metadata_parameters = []
        input_ports = []
        output_ports = []

        for param in module_entity.structured_interface.parameters:
            parameter = Parameter(name=param.name, documentation=param.description, default_value=param.default_value,
                                  is_optional=param.is_optional, type=param.parameter_type)
            parameters.append(parameter)

        for metadata_param in module_entity.structured_interface.metadata_parameters:
            metadata_parameter = Parameter(name=metadata_param.name, documentation=metadata_param.description,
                                           default_value=metadata_param.default_value,
                                           is_optional=metadata_param.is_optional, type=metadata_param.parameter_type)
            metadata_parameters.append(metadata_parameter)

        for input in module_entity.structured_interface.inputs:
            input_port = NodeInputPort(name=input.name, documentation=input.description,
                                       data_types_ids=input.data_type_ids_list, is_optional=input.is_optional)
            input_ports.append(input_port)

        for output in module_entity.structured_interface.outputs:
            output_port = NodeOutputPort(name=output.name, documentation=output.description,
                                         data_type_id=output.data_type_id,
                                         pass_through_input_name=output.pass_through_data_type_input_name)
            output_ports.append(output_port)

        node_interface = NodePortInterface(inputs=input_ports, outputs=output_ports)
        interface = EntityInterface(parameters=parameters, ports=node_interface,
                                    metadata_parameters=metadata_parameters)
        module = Module(data=module_entity, interface=interface)
        return module

    def create_module_async(self, creation_info):
        """CreateModuleAsync.

        :param creation_info: The module creation info
        :type creation_info: ~swaggerfixed.models.ModuleCreationInfo
        :return: ModuleEntity
        :rtype: ~swaggerfixed.models.ModuleEntity
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock create_module_async')
        id = str(uuid.uuid4())
        entity = ModuleEntity(id=id, name=creation_info.name, created_date=datetime.datetime.now(),
                              is_deterministic=creation_info.is_deterministic, module_execution_type='escloud',
                              structured_interface=creation_info.structured_interface,
                              last_modified_date=datetime.datetime.now(),
                              data_location=DataLocation(storage_id='mock_storage_id'))
        self._module_entities[id] = entity
        if creation_info.identifier_hash is not None:
            self._module_hash_to_id[creation_info.identifier_hash] = id

        return entity

    def update_module_async(self, id, updated):
        """UpdateModuleAsync.

        :param id: The module id
        :type id: str
        :param updated: The updated module
        :type updated: ~swaggerfixed.models.ModuleEntity
        :return: None
        :rtype: None
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock update_module_async')
        pass

    def create_unsubmitted_experiment_async(self, creation_info_with_graph, experiment_name):
        """CreateUnsubmittedExperimentWithGraphAsync.

        :param creation_info_with_graph: The experiment creation info
        :type creation_info_with_graph:
         ~swaggerfixed.models.ExperimentCreationInfoWithGraph
        :param experiment_name: The experiment name
        :type experiment_name: str
        :return: ExperimentEntity
        :rtype: ~swaggerfixed.models.ExperimentEntity
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock create_unsubmitted_experiment_async')
        id = str(uuid.uuid4())
        graph_id = str(uuid.uuid4())
        creation_info_with_graph.graph.id = graph_id
        entity = ExperimentEntity(id=id, description=creation_info_with_graph.creation_info.description,
                                  graph_id=graph_id)
        self._experiment_entities[id] = entity
        self._graph_entities[creation_info_with_graph.graph.id] = creation_info_with_graph.graph
        self._graph_entities[creation_info_with_graph.graph.id].run_history_experiment_name = experiment_name
        self._graph_interfaces[creation_info_with_graph.graph.id] = creation_info_with_graph.graph_interface
        return entity

    def submit_saved_experiment_async(self, experiment_id):
        """SubmitSavedExperimentAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :return: None
        :rtype: None
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock submit_saved_experiment_async')
        pass

    def get_experiment_async(self, experiment_id):
        """GetExperimentAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :return: ExperimentEntity
        :rtype: ~swaggerfixed.models.ExperimentEntity
        :raises:
         :class:`ErrorResponseException`
        """
        entity = self._experiment_entities[experiment_id]
        if entity.status is None:
            entity.status = ExperimentStatus(status_code='0')  # None -> NotStarted
        elif entity.status.status_code is '0':
            entity.status.status_code = '1'  # NotStarted -> Running
        elif entity.status.status_code is '1':
            entity.status.status_code = '3'  # Running -> Finished

        return entity

    def cancel_experiment_async(self, experiment_id):
        """CencelExperimentAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :return: None
        :rtype: None
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock cancel_experiment_async')
        pass

    def get_graph_async(self, graph_id):
        """GetGraphAsync

        :param graph_id: The graph id
        :type graph_id: str
        :return: GraphEntity
        :rtype: ~swaggerfixed.models.GraphEntity
        :raises:
         :class:`ErrorResponseException`
        """
        return self._graph_entities[graph_id]

    def get_graph_interface_async(self, graph_id):
        """GetGraphInterfaceAsync

        :param graph_id: The graph id
        :type graph_id: str
        :return: GraphEntity
        :rtype: ~swaggerfixed.models.EntityInterface
        :raises:
         :class:`ErrorResponseException`
        """
        return self._graph_interfaces[graph_id]
        pass

    def get_node_status_code_async(self, experiment_id, node_id):
        """GetNodeStatusCodeAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :param node_id: The node id
        :type node_id: str
        :return: node status code
        :rtype: StatusCode
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock get_node_status_code_async')
        return '4'  # Finished

    def get_node_status_async(self, experiment_id, node_id):
        """GetNodeStatusAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :param node_id: The node id
        :type node_id: str
        :return: node status
        :rtype: TaskStatus
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock get_node_status_async')
        return TaskStatus(status_code='4', run_id='MockRunId_{0}_{1}'.format(experiment_id, node_id))

    def get_all_nodes_in_level_status_async(self, experiment_id):
        """GetAllNodesInLevelStatusAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :return: dict
        :rtype: dict[str: TaskStatus]
        """
        print('mock get_all_nodes_in_level_status_async')
        graph = self.get_experiment_async(experiment_id).graph_id
        statuses = {}
        for node in graph.module_nodes:
            statuses[node.node_id] = TaskStatus(status_code='4',
                                                run_id='MockRunId_{0}_{1}'.format(experiment_id, node.node_id))
        return statuses

    def get_node_outputs_async(self, experiment_id, node_id):
        """GetNodeOutputsAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :param node_id: The node id
        :type node_id: str
        :return: node outputs dictionary
        :rtype: dict
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock get_node_outputs_async')
        experiment = self._experiment_entities[experiment_id]
        graph = self._graph_entities[experiment.graph_id]
        module_id = None
        for module_node in graph.module_nodes:
            if module_node.id == node_id:
                module_id = module_node.module_id
                break

        structured_outputs = self._module_entities[module_id].structured_interface.outputs
        outputs = {}
        for structured_output in structured_outputs:
            azure_data_reference = AzureBlobReference(relative_path="path",
                                                      aml_data_store_name="data_store")

            data_reference = DataReference(type='1', azure_blob_reference=azure_data_reference)

            data_location = DataLocation(data_reference=data_reference)

            outputs[structured_output.name] = NodeOutput(data_type_id=structured_output.data_type_id,
                                                         logical_size_in_bytes=0,
                                                         physical_size_in_bytes=0,
                                                         hash=str(uuid.uuid4()),
                                                         data_location=data_location)

        return outputs

    def get_node_job_log_async(self, experiment_id, node_id):
        """GetNodeJobLogAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :param node_id: The node id
        :type node_id: str
        :return: node job log
        :rtype: str
        :raises:
         :class:`ErrorResponseException`
        """
        return 'mock job log'

    def get_node_stdout_log_async(self, experiment_id, node_id):
        """GetNodeStdOutAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :param node_id: The node id
        :type node_id: str
        :return: node stdout
        :rtype: str
        :raises:
         :class:`ErrorResponseException`
        """
        return 'mock stdout'

    def get_node_stderr_log_async(self, experiment_id, node_id):
        """GetNodeStdErrAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :param node_id: The node id
        :type node_id: str
        :return: node stderr
        :rtype: str
        :raises:
         :class:`ErrorResponseException`
        """
        return 'mock stderr'

    def create_pipeline_async(self, pipeline_creation_info):
        """CreatePipelineAsync.

        :param pipeline_creation_info: The pipeline creation info
        :type pipeline_creation_info: ~swagger.models.PipelineCreationInfo
        :return: PipelineEntity
        :rtype: ~swaggerfixed.models.PipelineEntity
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock create_pipeline_async')
        graph_id = str(uuid.uuid4())
        self._graph_entities[graph_id] = pipeline_creation_info.graph
        self._graph_interfaces[graph_id] = pipeline_creation_info.graph_interface
        id = str(uuid.uuid4())
        entity = PipelineEntity(id=id, name=pipeline_creation_info.name,
                                description=pipeline_creation_info.description, version=pipeline_creation_info.version,
                                graph_id=graph_id, entity_status='0',
                                url='https://placeholder/'+id)
        self._pipeline_entities[id] = entity
        return entity

    def get_pipeline_async(self, pipeline_id):
        """GetPipelineAsync.

        :param pipeline_id: The pipeline id
        :type pipeline_id: str
        :return: PipelineEntity
        :rtype: ~swaggerfixed.models.PipelineEntity
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock get_pipeline_async')
        return self._pipeline_entities[pipeline_id]

    def submit_experiment_from_pipeline_async(self, pipeline_id, pipeline_submission_info):
        """SubmitExperimentFromPipelineAsync.

        :param pipeline_id: The pipeline id
        :type pipeline_id: str
        :param pipeline_submission_info: pipeline submission information
        :type pipeline_submission_info: ~swagger.models.PipelineSubmissionInfo
        :return: ExperimentEntity
        :rtype: ~swaggerfixed.models.ExperimentEntity
        :raises:
         :class:`ErrorResponseException`
        """
        print('mock submit_experiment_from_pipeline_async')
        if self._pipeline_entities[pipeline_id] is None:
            raise Exception('pipeline_id not found')

        id = str(uuid.uuid4())
        entity = ExperimentEntity(id=id, run_history_experiment_name=pipeline_submission_info.experiment_name,
                                  pipeline_id=pipeline_id)
        self._experiment_entities[id] = entity
        self._submitted_pipeline_infos[id] = pipeline_submission_info
        if pipeline_id in self._experiment_entities_from_pipelines:
            self._experiment_entities_from_pipelines[pipeline_id].append(entity)
        else:
            self._experiment_entities_from_pipelines[pipeline_id] = [entity]
        return entity

    def try_get_module_by_hash_async(self, identifier_hash):
        """GetModuleByHashAsync.

        :param identifier_hash: The module identifierHash
        :type identifier_hash: str
        :return: Module that was found, or None if not found
        :rtype: ~swagger.models.Module
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        if identifier_hash in self._module_hash_to_id:
            return self.get_module_async(self._module_hash_to_id[identifier_hash])
        else:
            return None

    def try_get_datasource_by_hash_async(self, identifier_hash):
        """GetDataSourceByHashAsync.

        :param identifier_hash: The datasource identifierHash
        :type identifier_hash: str
        :return: DataSourceEntity that was found, or None if not found
        :rtype: ~swagger.models.DataSourceEntity or
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        if identifier_hash in self._datasource_hash_to_id:
            return self.get_datasource_async(self._datasource_hash_to_id[identifier_hash])
        else:
            return None

    def get_all_datatypes_async(self):
        """GetAllDataTypesAsync.

        :return: list
        :rtype: list[~swagger.models.DataTypeEntity]
        :raises:
         :class:`ErrorResponseException`
        """
        return self._datatype_entities.values()

    def create_datatype_async(self, creation_info):
        """CreateNewDataTypeAsync.

        :param creation_info: The DataTypeEntity creation info
        :type creation_info: ~swagger.models.DataTypeCreationInfo
        :return: DataTypeEntity
        :rtype: ~swagger.models.DataTypeEntity
        :raises:
         :class:`ErrorResponseException`
        """
        if creation_info.id in self._datatype_entities:
            raise ValueError('Datatype already exists')
        entity = DataTypeEntity(name=creation_info.name, description=creation_info.description,
                                is_directory=creation_info.is_directory,
                                parent_data_type_ids=creation_info.parent_data_type_ids, id=creation_info.id)
        self._datatype_entities[creation_info.id] = entity
        return entity

    def update_datatype_async(self, id, updated):
        """UpdateDataTypeAsync.

        :param id: The DataTypeEntity id
        :type id: str
        :param updated: The DataTypeEntity to update
        :type updated: ~swagger.models.DataTypeEntity
        :return: DataTypeEntity
        :rtype: ~swagger.models.DataTypeEntity
        :raises:
         :class:`ErrorResponseException`
        """
        self._datatype_entities[id] = updated
        return updated

    def get_experiments_by_pipeline_id_async(self, pipeline_id):
        """GetExperimentsByPipelineIdAsync.

        :param pipeline_id: The published pipeline id
        :type pipeline_id: str
        :return: list
        :rtype: list[~swagger.models.ExperimentEntity]
        :raises:
         :class:`ErrorResponseException`
        """
        return self._experiment_entities_from_pipelines[pipeline_id]

    def get_all_published_pipelines(self, active_only=True):
        """GetPublishedPipelinesAsync.

        :param active_only: Indicate whether to load active only
        :type active_only: bool
        :return: list
        :rtype: list[~swagger.models.PipelineEntity]
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        return list(self._pipeline_entities.values())

    def update_published_pipeline_status_async(self, pipeline_id, new_status):
        """UpdateStatusAsync.

        :param pipeline_id: The published pipeline id
        :type pipeline_id: str
        :param new_status: New status for the pipeline ('Active', 'Deprecated', or 'Disabled')
        :type new_status: str
        :return: None
        :rtype: None
        :raises:
         :class:`ErrorResponseException`
        """
        enum_status = self.entity_status_to_enum(new_status)
        self._pipeline_entities[pipeline_id].entity_status = enum_status
