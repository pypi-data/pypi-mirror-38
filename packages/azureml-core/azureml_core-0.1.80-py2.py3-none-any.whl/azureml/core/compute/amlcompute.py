# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Manages AmlCompute Targets in Azure ML"""

import copy
import sys
import time
from azureml._compute._constants import MLC_COMPUTE_RESOURCE_ID_FMT
from azureml._compute._constants import MLC_ENDPOINT_FMT
from azureml._compute._util import amlcompute_payload_template
from azureml.core.compute import ComputeTarget
from azureml.core.compute.compute import ComputeTargetProvisioningConfiguration
from azureml.exceptions import ComputeTargetException
from dateutil.parser import parse


class AmlCompute(ComputeTarget):
    """
    Class for managing AmlCompute target objects.
    """
    _compute_type = 'BatchAI'

    def _initialize(self, workspace, obj_dict):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        """
        name = obj_dict['id']
        compute_resource_id = MLC_COMPUTE_RESOURCE_ID_FMT.format(workspace.subscription_id, workspace.resource_group,
                                                                 workspace.name, name)
        mlc_endpoint = MLC_ENDPOINT_FMT.format(workspace.subscription_id, workspace.resource_group, workspace.name,
                                               name)
        location = obj_dict['location']
        compute_type = obj_dict['properties']['computeType']
        tags = obj_dict['tags']
        description = obj_dict['properties']['description']
        created_on = None
        modified_on = None
        cluster_resource_id = obj_dict['properties']['resourceId']
        cluster_location = obj_dict['properties']['computeLocation'] \
            if 'computeLocation' in obj_dict['properties'] else None
        provisioning_state = obj_dict['properties']['provisioningState']
        provisioning_errors = obj_dict['properties']['provisioningErrors']
        is_attached = obj_dict['properties']['isAttachedCompute']
        vm_size = obj_dict['properties']['properties']['vmSize'] \
            if obj_dict['properties']['properties'] else None
        vm_priority = obj_dict['properties']['properties']['vmPriority'] \
            if obj_dict['properties']['properties'] else None
        scale_settings = obj_dict['properties']['properties']['scaleSettings'] \
            if obj_dict['properties']['properties'] else None
        scale_settings = RequestedScaleSettings.deserialize(scale_settings) if scale_settings else None
        status = AmlComputeStatus.deserialize(obj_dict['properties']['status']['detailedStatus']) \
            if 'status' in obj_dict['properties'] and 'detailedStatus' in obj_dict['properties']['status'] else None
        super(AmlCompute, self)._initialize(compute_resource_id, name, location, compute_type, tags, description,
                                            created_on, modified_on, provisioning_state, provisioning_errors,
                                            cluster_resource_id, cluster_location, workspace, mlc_endpoint, None,
                                            workspace._auth, is_attached)
        self.vm_size = vm_size
        self.vm_priority = vm_priority
        self.scale_settings = scale_settings
        self.status = status

    @staticmethod
    def _create(workspace, name, provisioning_configuration):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :param provisioning_configuration:
        :type provisioning_configuration: AmlComputeProvisioningConfiguration
        :return:
        :rtype: AmlCompute
        """
        compute_create_payload = AmlCompute._build_create_payload(provisioning_configuration, workspace.location)
        return ComputeTarget._create_compute_target(workspace, name, compute_create_payload, AmlCompute)

    @staticmethod
    def provisioning_configuration(vm_size='', vm_priority="dedicated", autoscale_enabled=True, min_nodes=0,
                                   max_nodes=None, tags=None, description=None):
        """
        Create a configuration object for provisioning an AmlCompute target

        :param vm_size: Size of agent VMs. More details can be found here: https://aka.ms/azureml-vm-details.
            Note that not all sizes are available in all regions, as
            detailed in the previous link.
        :type vm_size: str
        :param vm_priority: dedicated or lowpriority VMs. If not specified, will default to dedicated.
        :type vm_priority: str
        :param autoscale_enabled: Whether or not to enable autoscaling on the cluster.
            If not specified, will default to True.
        :type autoscale_enabled: bool
        :param min_nodes: Minimum number of nodes to use on the cluster. If not specified, will default to 0.
        :type min_nodes: int
        :param max_nodes: Maximum number of nodes to use on the cluster
        :type max_nodes: int
        :param tags: A dictionary of key value tags to provide to the compute object
        :type tags: dict[str, str]
        :param description: A description to provide to the compute object
        :type description: str
        :return: A configuration object to be used when creating a Compute object
        :rtype: AmlComputeProvisioningConfiguration
        :raises: ComputeTargetException
        """
        config = AmlComputeProvisioningConfiguration(vm_size, vm_priority, autoscale_enabled, min_nodes,
                                                     max_nodes, tags, description)
        return config

    @staticmethod
    def _build_create_payload(config, location):
        """
        Construct the payload needed to create an AmlCompute cluster

        :param config:
        :type config: azureml.core.compute.AmlComputeProvisioningConfiguration
        :param location:
        :type location: str
        :return:
        :rtype: dict
        """
        json_payload = copy.deepcopy(amlcompute_payload_template)
        del(json_payload['properties']['resourceId'])
        del(json_payload['properties']['computeLocation'])
        json_payload['location'] = location
        if not config.vm_size and not config.vm_priority and config.scale_settings.autoscale_enabled is None:
            del(json_payload['properties']['properties'])
        else:
            if not config.vm_size:
                del(json_payload['properties']['properties']['vmSize'])
            else:
                json_payload['properties']['properties']['vmSize'] = config.vm_size
            if not config.vm_priority:
                del(json_payload['properties']['properties']['vmPriority'])
            else:
                json_payload['properties']['properties']['vmPriority'] = config.vm_priority
            if config.scale_settings.autoscale_enabled is None:
                del(json_payload['properties']['properties']['scaleSettings'])
            else:
                json_payload['properties']['properties']['scaleSettings'] = config.scale_settings.serialize()
        if config.tags:
            json_payload['tags'] = config.tags
        else:
            del(json_payload['tags'])
        if config.description:
            json_payload['properties']['description'] = config.description
        else:
            del(json_payload['properties']['description'])
        return json_payload

    def wait_for_completion(self, show_output=False, min_node_count=None, timeout_in_minutes=20):
        """
        Wait for the AmlCompute cluster to finish provisioning. This can be configured to wait for a minimum number of
        nodes, and to timeout after a set period of time.

        :param show_output: Boolean to provide more verbose output
        :type show_output: bool
        :param min_node_count: Minimum number of nodes to wait for before considering provisioning to be complete. This
            doesn't have to equal the minimum number of nodes that the compute was provisioned with, however it should
            not be greater than that.
        :type min_node_count: int
        :param timeout_in_minutes: The duration in minutes to wait before considering provisioning to have failed.
        :type timeout_in_minutes: int
        :raises: ComputeTargetException
        """
        min_nodes_reached, timeout_reached, terminal_state_reached, status_errors_present = \
            self._wait_for_nodes(min_node_count, timeout_in_minutes, show_output)
        print('AmlCompute wait for completion finished')
        if min_nodes_reached:
            print('Minimum number of nodes requested have been provisioned')
        elif timeout_reached:
            print('Wait timeout has been reached')
        elif terminal_state_reached:
            if self.status:
                state = self.status.provisioning_state.capitalize()
            else:
                state = self.provisioning_state.capitalize()
            print('Terminal state of "{}" has been reached'.format(state))
            if state == 'Failed':
                print('Provisioning errors: {}'.format(self.provisioning_errors))
        elif status_errors_present:
            if self.status:
                errors = self.status.errors
            else:
                errors = self.provisioning_errors
            print('There were errors reported from AmlCompute:\n{}'.format(errors))

    def _wait_for_nodes(self, min_node_count, timeout_in_minutes, show_output):
        """

        :param min_node_count:
        :type min_node_count: int
        :param timeout_in_minutes:
        :type timeout_in_minutes: int
        :param show_output:
        :type show_output: bool
        :return:
        :rtype:
        """
        self.refresh_state()
        start_time = time.time()

        if self.status:
            current_state = self.status.provisioning_state
        else:
            current_state = self.provisioning_state
        if show_output and current_state:
            sys.stdout.write('{}'.format(current_state))
            sys.stdout.flush()

        min_nodes_reached = self._min_node_count_reached(min_node_count)
        timeout_reached = self._polling_timeout_reached(start_time, timeout_in_minutes)
        terminal_state_reached = self._terminal_state_reached()
        status_errors_present = self._status_errors_present()

        while not min_nodes_reached and not timeout_reached and not terminal_state_reached \
                and not status_errors_present:
            time.sleep(5)
            self.refresh_state()

            if self.status:
                state = self.status.provisioning_state
            else:
                state = None

            if show_output and state:
                if state != current_state and state != 'succeeded':
                    if current_state is None:
                        sys.stdout.write('{}'.format(state))
                    else:
                        sys.stdout.write('\n{}'.format(state))
                    current_state = state
                elif state:
                    sys.stdout.write('.')
                sys.stdout.flush()

            min_nodes_reached = self._min_node_count_reached(min_node_count)
            timeout_reached = self._polling_timeout_reached(start_time, timeout_in_minutes)
            terminal_state_reached = self._terminal_state_reached()
            status_errors_present = self._status_errors_present()

        if show_output:
            sys.stdout.write('\n')
            sys.stdout.flush()

        return min_nodes_reached, timeout_reached, terminal_state_reached, status_errors_present

    def _min_node_count_reached(self, min_node_count):
        """

        :param min_node_count:
        :type min_node_count: int
        :return:
        :rtype: bool
        """
        if not min_node_count:
            if self.status and self.status.scale_settings:
                if self.status.scale_settings.manual:
                    min_node_count = self.status.scale_settings.manual.target_node_count
                elif self.status.scale_settings.auto_scale:
                    min_node_count = self.status.scale_settings.auto_scale.min_node_count
        if min_node_count is not None and self.status and self.status.current_node_count >= min_node_count:
            return True
        return False

    def _polling_timeout_reached(self, start_time, timeout_in_minutes):
        """

        :param start_time:
        :type start_time: datetime.datetime
        :param timeout_in_minutes:
        :type timeout_in_minutes: int
        :return:
        :rtype: bool
        """
        cur_time = time.time()
        if cur_time - start_time > timeout_in_minutes * 60:
            return True
        return False

    def _terminal_state_reached(self):
        """

        :param state:
        :type state: str
        :return:
        :rtype: bool
        """
        if self.status:
            state = self.status.provisioning_state.capitalize()
        else:
            state = self.provisioning_state.capitalize()
        if state == 'Failed' or state == 'Canceled':
            return True
        return False

    def _status_errors_present(self):
        """

        :return:
        :rtype:
        """
        if (self.status and self.status.errors) or self.provisioning_errors:
            return True
        return False

    def refresh_state(self):
        """
        Perform an in-place update of the properties of the object based on the current state of the
        corresponding cloud object. Primarily useful for manual polling of compute state.
        """
        cluster = AmlCompute(self.workspace, self.name)
        self.modified_on = cluster.modified_on
        self.provisioning_state = cluster.provisioning_state
        self.provisioning_errors = cluster.provisioning_errors
        self.cluster_resource_id = cluster.cluster_resource_id
        self.cluster_location = cluster.cluster_location
        self.vm_size = cluster.vm_size
        self.vm_priority = cluster.vm_priority
        self.scale_settings = cluster.scale_settings
        self.status = cluster.status

    def get_status(self):
        """
        Retrieves the current detailed status for the AmlCompute cluster.

        :return: A detailed status object for the cluster
        :rtype: AmlComputeStatus
        """
        self.refresh_state()
        return self.status

    def delete(self):
        """
        Removes the AmlCompute object from its associated workspace.

        .. remarks::
            If this object was created through Azure ML,
            the corresponding cloud based objects will also be deleted. If this object was created externally and only
            attached to the workspace, it will raise exception and nothing will be changed.

        :raises: ComputeTargetException
        """
        self._delete_or_detach('delete')

    def detach(self):
        """
        Detach is not supported for AmlCompute object. Try to use delete instead.

        :raises: ComputeTargetException
        """
        raise ComputeTargetException('Detach is not supported for AmlCompute object. Try to use delete instead.')

    def serialize(self):
        """
        Convert this AmlCompute object into a json serialized dictionary.

        :return: The json representation of this AmlCompute object
        :rtype: dict
        """
        scale_settings = self.scale_settings.serialize() if self.scale_settings else None
        amlcompute_properties = {'vmSize': self.vm_size, 'vmPriority': self.vm_priority,
                                 'scaleSettings': scale_settings}
        amlcompute_status = self.status.serialize() if self.status else None
        cluster_properties = {'computeType': 'BatchAI', 'computeLocation': self.cluster_location,
                              'description': self.description, 'resourceId': self.cluster_resource_id,
                              'provisioningErrors': self.provisioning_errors,
                              'provisioningState': self.provisioning_state, 'properties': amlcompute_properties,
                              'status': amlcompute_status}
        return {'id': self.id, 'name': self.name, 'tags': self.tags, 'location': self.location,
                'properties': cluster_properties}

    @staticmethod
    def deserialize(workspace, object_dict):
        """
        Convert a json object into a AmlCompute object. Will fail if the provided workspace is not the workspace
        the Compute is associated with.

        :param workspace: The workspace object the AmlCompute object is associated with
        :type workspace: azureml.core.workspace.Workspace
        :param object_dict: A json object to convert to a AmlCompute object
        :type object_dict: dict
        :return: The AmlCompute representation of the provided json object
        :rtype: AmlCompute
        :raises: ComputeTargetException
        """
        AmlCompute._validate_get_payload(object_dict)
        target = AmlCompute(None, None)
        target._initialize(workspace, object_dict)
        return target

    @staticmethod
    def _validate_get_payload(payload):
        if 'properties' not in payload or 'computeType' not in payload['properties']:
            raise ComputeTargetException('Invalid cluster payload:\n'
                                         '{}'.format(payload))
        if payload['properties']['computeType'] != AmlCompute._compute_type:
            raise ComputeTargetException('Invalid cluster payload, not "{}":\n'
                                         '{}'.format(AmlCompute._compute_type, payload))
        for arm_key in ['location', 'id', 'tags']:
            if arm_key not in payload:
                raise ComputeTargetException('Invalid cluster payload, missing ["{}"]:\n'
                                             '{}'.format(arm_key, payload))
        for key in ['properties', 'provisioningErrors', 'description', 'provisioningState', 'resourceId']:
            if key not in payload['properties']:
                raise ComputeTargetException('Invalid cluster payload, missing ["properties"]["{}"]:\n'
                                             '{}'.format(key, payload))
        if payload['properties']['properties']:
            for amlcompute_key in ['vmPriority', 'vmSize', 'scaleSettings']:
                if amlcompute_key not in payload['properties']['properties']:
                    raise ComputeTargetException('Invalid cluster payload, missing '
                                                 '["properties"]["properties"]["{}"]:\n'
                                                 '{}'.format(amlcompute_key, payload))


class AmlComputeProvisioningConfiguration(ComputeTargetProvisioningConfiguration):
    """
    Provisioning configuration object for AmlCompute targets. This objects is used to
    define the configuration parameters for provisioning AmlCompute objects.

    :param vm_size: Size of agent VMs. More details can be found here: https://aka.ms/azureml-vm-details.
        Note that not all sizes are available in all regions, as
        detailed in the previous link.
    :type vm_size: str
    :param vm_priority: dedicated or lowpriority VMs. If not specified, will default to dedicated.
    :type vm_priority: str
    :param autoscale_enabled: Whether or not to enable autoscaling on the cluster.
        If not specified, will default to True.
    :type autoscale_enabled: bool
    :param autoscale_min_nodes: Minimum number of nodes to use on the cluster.
        If not specified, will default to 0.
    :type autoscale_min_nodes: int
    :param autoscale_max_nodes: Maximum number of nodes to use on the cluster
    :type autoscale_max_nodes: int
    :param location: Location to provision cluster in. If not specified, will default to workspace location.
    :type location: str
    :param tags: A dictionary of key value tags to provide to the compute object
    :type tags: dict[str, str]
    :param description: A description to provide to the compute object
    :type description: str
    """
    def __init__(self, vm_size='', vm_priority="dedicated", autoscale_enabled=True, autoscale_min_nodes=0,
                 autoscale_max_nodes=None, tags=None, description=None):
        """
        Create a configuration object for provisioning a AmlCompute target

        :param vm_size: Size of agent VMs. More details can be found here: https://aka.ms/azureml-vm-details.
            Note that not all sizes are available in all regions, as
            detailed in the previous link.
        :type vm_size: str
        :param vm_priority: dedicated or lowpriority VMs. If not specified, will default to dedicated.
        :type vm_priority: str
        :param autoscale_enabled: Whether or not to enable autoscaling on the cluster.
            If not specified, will default to True.
        :type autoscale_enabled: bool
        :param autoscale_min_nodes: Minimum number of nodes to use on the cluster.
        :type autoscale_min_nodes: int
        :param autoscale_max_nodes: Maximum number of nodes to use on the cluster
        :type autoscale_max_nodes: int
        :param location: Location to provision cluster in. If not specified, will default to workspace location.
        :type location: str
        :param tags: A dictionary of key value tags to provide to the compute object
        :type tags: dict[str, str]
        :param description: A description to provide to the compute object
        :type description: str
        :return: A configuration object to be used when creating a Compute object
        :rtype: AmlComputeProvisioningConfiguration
        :raises: ComputeTargetException
        """
        super(AmlComputeProvisioningConfiguration, self).__init__(AmlCompute, None)
        self.vm_size = vm_size
        self.vm_priority = vm_priority
        self.scale_settings = RequestedScaleSettings(autoscale_enabled, autoscale_min_nodes, autoscale_max_nodes)
        self.validate_configuration()
        self.tags = tags
        self.description = description

    def validate_configuration(self):
        """
        Checks that the specified configuration values are valid. Will raise a ComputeTargetException if validation
        fails.

        :raises: ComputeTargetException
        """
        if self.scale_settings.autoscale_enabled is None:
            if self.scale_settings.minimum_node_count is not None:
                raise ComputeTargetException('Invalid provisioning configuration, value provided for min node count'
                                             'but autoscale flag not set.')
            if self.scale_settings.maximum_node_count is not None:
                raise ComputeTargetException('Invalid provisioning configuration, value provided for max node count'
                                             'but autoscale flag not set.')
        elif self.scale_settings.autoscale_enabled:
            if self.scale_settings.minimum_node_count is None or self.scale_settings.maximum_node_count is None:
                raise ComputeTargetException('Invalid provisioning configuration, min and max node counts must both '
                                             'be provided to enable autoscaling.')
        elif self.scale_settings.autoscale_enabled is False:
            if self.scale_settings.maximum_node_count is None or self.scale_settings.maximum_node_count is None or \
                    self.scale_settings.minimum_node_count != self.scale_settings.maximum_node_count:
                raise ComputeTargetException('Invalid provisioning configuration, min and max node counts must be '
                                             'provided and equal when autoscale is False.')


class RequestedScaleSettings(object):
    """
    Requested scale settings object for a AmlCompute object
    """
    def __init__(self, autoscale_enabled, minimum_node_count, maximum_node_count):
        """
        Initialize the RequestedScaleSettings object

        :param autoscale_enabled: Whether or not to enable autoscaling on the cluster. If enabled, must provide min
            and max nodes as well. If explicitly set to False, min and max nodes must be equal and are used to provide
            manual setting for number of nodes.
        :type autoscale_enabled: bool
        :param minimum_node_count: Minimum number of nodes to use on the cluster.
        :type minimum_node_count: int
        :param maximum_node_count: Maximum number of nodes to use on the cluster
        :type maximum_node_count: int
        """
        self.autoscale_enabled = autoscale_enabled
        self.minimum_node_count = minimum_node_count
        self.maximum_node_count = maximum_node_count

    def serialize(self):
        """
        Convert this RequestedScaleSettings object into a json serialized dictionary.

        :return: The json representation of this RequestedScaleSettings object
        :rtype: dict
        """
        return {'autoScaleEnabled': self.autoscale_enabled, 'minNodeCount': self.minimum_node_count,
                'maxNodeCount': self.maximum_node_count}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a RequestedScaleSettings object.

        :param object_dict: A json object to convert to a RequestedScaleSettings object
        :type object_dict: dict
        :return: The RequestedScaleSettings representation of the provided json object
        :rtype: RequestedScaleSettings
        :raises: ComputeTargetException
        """
        if not object_dict:
            return None
        for key in ['autoScaleEnabled', 'minNodeCount', 'maxNodeCount']:
            if key not in object_dict:
                raise ComputeTargetException('Invalid scale settings payload, missing "{}":\n'
                                             '{}'.format(key, object_dict))
        return RequestedScaleSettings(object_dict['autoScaleEnabled'], object_dict['minNodeCount'],
                                      object_dict['maxNodeCount'])


class AmlComputeStatus(object):
    """
    Detailed status for a AmlCompute object

    .. remarks::
        Initialize a AmlComputeStatus object

    :param allocation_state: String description of the current allocation state
    :type allocation_state: str
    :param allocation_state_transition_time: Time of the most recent allocation state change
    :type allocation_state_transition_time: datetime.datetime
    :param creation_time: Cluster creation time
    :type creation_time: datetime.datetime
    :param current_node_count: The current number of nodes used by the cluster
    :type current_node_count: int
    :param errors: A list of error details, if any
    :type errors: list[dict]
    :param node_state_counts: An object containing counts of the various current node states in the cluster
    :type node_state_counts: AmlComputeNodeStateCounts
    :param provisioning_state: Current provisioning state of the cluster
    :type provisioning_state: str
    :param provisioning_state_transition_time: Time of the most recent provisioning state change
    :type provisioning_state_transition_time: datetime.datetime
    :param scale_settings: An object containing the specified scale settings for the cluster
    :type scale_settings: ScaleSettings
    :param vm_priority: dedicated or lowpriority VMs.
    :type vm_priority: str
    :param vm_size: Size of agent VMs. More details can be found here: https://aka.ms/azureml-vm-details.
        Note that not all sizes are available in all regions, as
        detailed in the previous link.
    :type vm_size: str
    """
    def __init__(self, allocation_state, allocation_state_transition_time, creation_time, current_node_count,
                 errors, node_state_counts, provisioning_state, provisioning_state_transition_time, scale_settings,
                 vm_priority, vm_size):
        """
        Initialize a AmlComputeStatus object

        :param allocation_state: String description of the current allocation state
        :type allocation_state: str
        :param allocation_state_transition_time: Time of the most recent allocation state change
        :type allocation_state_transition_time: datetime.datetime
        :param creation_time: Cluster creation time
        :type creation_time: datetime.datetime
        :param current_node_count: The current number of nodes used by the cluster
        :type current_node_count: int
        :param errors: A list of error details, if any
        :type errors: list[dict]
        :param node_state_counts: An object containing counts of the various current node states in the cluster
        :type node_state_counts: AmlComputeNodeStateCounts
        :param provisioning_state: Current provisioning state of the cluster
        :type provisioning_state: str
        :param provisioning_state_transition_time: Time of the most recent provisioning state change
        :type provisioning_state_transition_time: datetime.datetime
        :param scale_settings: An object containing the specified scale settings for the cluster
        :type scale_settings: ScaleSettings
        :param vm_priority: dedicated or lowpriority VMs.
        :type vm_priority: str
        :param vm_size: Size of agent VMs. More details can be found here: https://aka.ms/azureml-vm-details.
            Note that not all sizes are available in all regions, as
            detailed in the previous link.
        :type vm_size: str
        """
        self.allocation_state = allocation_state
        self.allocation_state_transition_time = allocation_state_transition_time
        self.creation_time = creation_time
        self.current_node_count = current_node_count
        self.errors = errors
        self.node_state_counts = node_state_counts
        self.provisioning_state = provisioning_state
        self.provisioning_state_transition_time = provisioning_state_transition_time
        self.scale_settings = scale_settings
        self.vm_priority = vm_priority
        self.vm_size = vm_size

    def serialize(self):
        """
        Convert this AmlComputeStatus object into a json serialized dictionary.

        :return: The json representation of this AmlComputeStatus object
        :rtype: dict
        """
        allocation_state_transition_time = self.allocation_state_transition_time.isoformat() \
            if self.allocation_state_transition_time else None
        creation_time = self.creation_time.isoformat() if self.creation_time else None
        node_state_counts = self.node_state_counts.serialize() if self.node_state_counts else None
        provisioning_state_transition_time = self.provisioning_state_transition_time.isoformat() \
            if self.provisioning_state_transition_time else None
        scale_settings = self.scale_settings.serialize() if self.scale_settings else None
        return {'allocationState': self.allocation_state,
                'allocationStateTransitionTime': allocation_state_transition_time, 'creationTime': creation_time,
                'currentNodeCount': self.current_node_count, 'errors': self.errors,
                'nodeStateCounts': node_state_counts, 'provisioningState': self.provisioning_state,
                'provisioningStateTransitionTime': provisioning_state_transition_time, 'scaleSettings': scale_settings,
                'vmPriority': self.vm_priority, 'vmSize': self.vm_size}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a AmlComputeStatus object.

        :param object_dict: A json object to convert to a AmlComputeStatus object
        :type object_dict: dict
        :return: The AmlComputeStatus representation of the provided json object
        :rtype: AmlComputeStatus
        :raises: ComputeTargetException
        """
        allocation_state = object_dict['properties.allocationState'] \
            if 'properties.allocationState' in object_dict else None
        allocation_state_transition_time = parse(object_dict['properties.allocationStateTransitionTime']) \
            if 'properties.allocationStateTransitionTime' in object_dict else None
        creation_time = parse(object_dict['properties.creationTime']) \
            if 'properties.creationTime' in object_dict else None
        current_node_count = object_dict['properties.currentNodeCount'] \
            if 'properties.currentNodeCount' in object_dict else None
        errors = object_dict['properties.errors'] \
            if 'properties.errors' in object_dict else None
        node_state_counts = AmlComputeNodeStateCounts.deserialize(object_dict['properties.nodeStateCounts']) \
            if 'properties.nodeStateCounts' in object_dict else None
        provisioning_state = object_dict['properties.provisioningState'] \
            if 'properties.provisioningState' in object_dict else None
        provisioning_state_transition_time = parse(object_dict['properties.provisioningStateTransitionTime']) \
            if 'properties.provisioningStateTransitionTime' in object_dict else None
        scale_settings = ScaleSettings.deserialize(object_dict['properties.scaleSettings']) \
            if 'properties.scaleSettings' in object_dict else None
        vm_priority = object_dict['properties.vmPriority'] if 'properties.vmPriority' in object_dict else None
        vm_size = object_dict['properties.vmSize'] if 'properties.vmSize' in object_dict else None

        return AmlComputeStatus(allocation_state, allocation_state_transition_time, creation_time, current_node_count,
                                errors, node_state_counts, provisioning_state, provisioning_state_transition_time,
                                scale_settings, vm_priority, vm_size)


class AmlComputeNodeStateCounts(object):
    """
    Detailed node counts for a AmlCompute object
    """
    def __init__(self, idle_node_count, leaving_node_count, preparing_node_count, running_node_count,
                 unusable_node_count):
        """
        Initialize a AmlComputeNodeStateCounts object

        :param idle_node_count: Current number of idle nodes
        :type idle_node_count: int
        :param leaving_node_count: Current number of nodes that are being deprovisioned
        :type leaving_node_count: int
        :param preparing_node_count: Current number of nodes that are being provisioned
        :type preparing_node_count: int
        :param running_node_count: Current number of in use nodes
        :type running_node_count: int
        :param unusable_node_count: Current number of unusable nodes
        :type unusable_node_count: int
        """
        self.idle_node_count = idle_node_count
        self.leaving_node_count = leaving_node_count
        self.preparing_node_count = preparing_node_count
        self.running_node_count = running_node_count
        self.unusable_node_count = unusable_node_count

    def serialize(self):
        """
        Convert this AmlComputeNodeStateCounts object into a json serialized dictionary.

        :return: The json representation of this AmlComputeNodeStateCounts object
        :rtype: dict
        """
        return {'idleNodeCount': self.idle_node_count, 'leavingNodeCount': self.leaving_node_count,
                'preparingNodeCount': self.preparing_node_count, 'runningNodeCount': self.running_node_count,
                'unusableNodeCount': self.unusable_node_count}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a AmlComputeNodeStateCounts object.

        :param object_dict: A json object to convert to a AmlComputeNodeStateCounts object
        :type object_dict: dict
        :return: The AmlComputeNodeStateCounts representation of the provided json object
        :rtype: AmlComputeNodeStateCounts
        :raises: ComputeTargetException
        """
        idle_node_count = object_dict['idleNodeCount'] if 'idleNodeCount' in object_dict else None
        leaving_node_count = object_dict['leavingNodeCount'] if 'leavingNodeCount' in object_dict else None
        preparing_node_count = object_dict['preparingNodeCount'] if 'preparingNodeCount' in object_dict else None
        running_node_count = object_dict['runningNodeCount'] if 'runningNodeCount' in object_dict else None
        unusable_node_count = object_dict['unusableNodeCount'] if 'unusableNodeCount' in object_dict else None

        return AmlComputeNodeStateCounts(idle_node_count, leaving_node_count, preparing_node_count, running_node_count,
                                         unusable_node_count)


class ScaleSettings(object):
    """
    Specific scale settings for a AmlCompute object
    """
    def __init__(self, manual_scale_settings, auto_scale_settings):
        """
        Initialize a ScaleSettings object

        :param manual_scale_settings: An object defining the current manual scale settings for the cluster
        :type manual_scale_settings: ManualScaleSettings | None
        :param auto_scale_settings: An object defining the current automatic scale settings for the cluster
        :type auto_scale_settings: AutoScaleSettings | None
        """
        self.manual = manual_scale_settings
        self.auto_scale = auto_scale_settings

    def serialize(self):
        """
        Convert this ScaleSettings object into a json serialized dictionary.

        :return: The json representation of this ScaleSettings object
        :rtype: dict
        """
        manual = self.manual.serialize() if self.manual else None
        auto_scale = self.auto_scale.serialize() if self.auto_scale else None
        return {'manual': manual, 'autoScale': auto_scale}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a ScaleSettings object.

        :param object_dict: A json object to convert to a ScaleSettings object
        :type object_dict: dict
        :return: The ScaleSettings representation of the provided json object
        :rtype: ScaleSettings
        :raises: ComputeTargetException
        """
        manual = ManualScaleSettings.deserialize(object_dict['manual']) \
            if 'manual' in object_dict and object_dict['manual'] else None
        auto_scale = AutoScaleSettings.deserialize(object_dict['autoScale']) \
            if 'autoScale' in object_dict and object_dict['autoScale'] else None

        return ScaleSettings(manual, auto_scale)


class ManualScaleSettings(object):
    """
    Details for manual scale settings for a AmlCompute object
    """
    def __init__(self, target_node_count, node_deallocation_option):
        """
        Initialize a ManualScaleSettings object

        :param target_node_count: The number of desired nodes for the cluster
        :type target_node_count: int
        :param node_deallocation_option: Option when nodes are deallocated
        :type node_deallocation_option: str
        """
        self.target_node_count = target_node_count
        self.node_deallocation_option = node_deallocation_option

    def serialize(self):
        """
        Convert this ManualScaleSettings object into a json serialized dictionary.

        :return: The json representation of this ManualScaleSettings object
        :rtype: dict
        """
        return {'targetNodeCount': self.target_node_count, 'nodeDeallocationOption': self.node_deallocation_option}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a ManualScaleSettings object.

        :param object_dict: A json object to convert to a ManualScaleSettings object
        :type object_dict: dict
        :return: The ManualScaleSettings representation of the provided json object
        :rtype: ManualScaleSettings
        :raises: ComputeTargetException
        """
        target_node_count = object_dict['targetNodeCount'] if 'targetNodeCount' in object_dict else None
        node_deallocation_option = object_dict['nodeDeallocationOption'] \
            if 'nodeDeallocationOption' in object_dict else None

        return ManualScaleSettings(target_node_count, node_deallocation_option)


class AutoScaleSettings(object):
    """
    Details for automatic scale settings for a AmlCompute object
    """
    def __init__(self, max_node_count, min_node_count, initial_node_count):
        """
        Initialize an AutoScaleSettings object

        :param max_node_count: The maximum number of nodes for the cluster
        :type max_node_count: int
        :param min_node_count: The minimum number of nodes for the cluster
        :type min_node_count: int
        :param initial_node_count: The number of nodes for the cluster to start with
        :type initial_node_count: int
        """
        self.max_node_count = max_node_count
        self.min_node_count = min_node_count
        self.initial_node_count = initial_node_count

    def serialize(self):
        """
        Convert this AutoScaleSettings object into a json serialized dictionary.

        :return: The json representation of this AutoScaleSettings object
        :rtype: dict
        """
        return {'maximumNodeCount': self.max_node_count, 'minimumNodeCount': self.min_node_count,
                'initialNodeCount': self.initial_node_count}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a AutoScaleSettings object.

        :param object_dict: A json object to convert to a AutoScaleSettings object
        :type object_dict: dict
        :return: The AutoScaleSettings representation of the provided json object
        :rtype: AutoScaleSettings
        :raises: ComputeTargetException
        """
        max_node_count = object_dict['maximumNodeCount'] if 'maximumNodeCount' in object_dict else None
        min_node_count = object_dict['minimumNodeCount'] if 'minimumNodeCount' in object_dict else None
        initial_node_count = object_dict['initialNodeCount'] if 'initialNodeCount' in object_dict else None

        return AutoScaleSettings(max_node_count, min_node_count, initial_node_count)
