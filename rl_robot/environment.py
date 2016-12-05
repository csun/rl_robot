import math
from pybrain.rl.environments.environment import Environment as PybrainEnvironment
import random
import time
import vrep

from joint_constants import *


class ConnectionException(Exception):
    pass


class SimulatorException(Exception):
    pass


class Environment(PybrainEnvironment):

    def __init__(self, address, port, scene_file):
        self._scene_file = scene_file
        self._client_id = vrep.simxStart(address, port, True, True, 5000, 5)

        if self._client_id == -1:
            raise ConnectionException('Could not connect')

        # set joint angles and start streaming
        self.reset()

    def isColliding(self):
        for object_name, has_collision in self._read_all_collisions():
            if has_collision:
                print 'COLLISION! with object named [{}].'.format(object_name)
                return True
        return False

    def distanceFromGoal(self):
        # TODO
        pass

    def getSensors(self):
        # If we haven't moved since the last sensor reading, our old sensor readings are still correct.
        if self._current_sensor_step == self._current_action_step:
            return self._sensor_data_vector

        self._get_goal_distance_data()
        self._get_proximity_sensor_distances()
        self._generate_sensor_data_vector()

        return self._sensor_data_vector

    def performAction(self, deltas):
        # just pass in a list of joint angle changes that matches the order in state (see: self._joint_positions)
        if len(deltas) != len(JOINTS):
            raise SimulatorException('Given deltas object length [{}] does not match num joints [{}]').format(len(deltas), len(JOINTS))

        # Increment joint positions by action and apply to the robot
        # TODO figure out how to specify how many deltas Learner can provide to env and max / min delta value
        # TODO figure out how to set joint limits as well
        self._joint_positions = [jp + djp for jp, djp in zip(self._joint_positions, deltas)]
        self._apply_all_joint_positions(self._joint_positions)

    def reset(self):
        vrep.simxStopSimulation(self._client_id, vrep.simx_opmode_blocking)
        time.sleep(0.1)

        # first load up the original scene
        scene_did_load = vrep.simxLoadScene(self._client_id, self._scene_file, 0, vrep.simx_opmode_blocking)
        if scene_did_load != vrep.simx_return_ok:
            raise SimulatorException('Could not load scene')

        # get collision handles, joint handles, etc.
        self._scene_handles = self._load_scene_handles()

        self._current_action_step = 0
        self._current_sensor_step = None
        self._joint_positions = # TODO
        self._end_effector_position = # TODO
        self._goal_position = # TODO
        self._proximity_sensor_distances = # TODO
        self._sensor_data_vector = None

        vrep.simxStartSimulation(self._client_id, vrep.simx_opmode_blocking)

        # TODO move to helper
        print 'Beginning to stream all collisions.'
        # start streaming for all collision
        for collision in COLLISION_OBJECTS:
            collision_handle = self._scene_handles[collision]
            # TODO make a helper for these calls that sends streaming only if never opened?
            code, state = vrep.simxReadCollision(self._client_id, collision_handle, vrep.simx_opmode_streaming)

        print 'Beginning to stream data for all proximity sensors.'
        for sensor in PROXIMITY_SENSORS:
            sensor_handle = self._scene_handles[sensor]
            code, state, point, handle, normal = vrep.simxReadProximitySensor(self._client_id, sensor_handle, vrep.simx_opmode_streaming)

    # Scene Configuration Helper Functions ----------------------------------------------------------------
    def _load_scene_handles(self):
        failed_handles = []

        # load all objects
        object_handles = {}
        for obj_name in LINKS + JOINTS + PROXIMITY_SENSORS:
            code, handle = vrep.simxGetObjectHandle(self._client_id, obj_name, vrep.simx_opmode_blocking)

            if code == vrep.simx_return_ok:
                object_handles[obj_name] = handle
            else:
                failed_handles.append(obj_name)

        # load collisions -- use the same map as for objects
        for coll_name in COLLISION_OBJECTS:
            code, handle = vrep.simxGetCollisionHandle(self._client_id, coll_name, vrep.simx_opmode_blocking)

            if code == vrep.simx_return_ok:
                object_handles[coll_name] = handle
            else:
                failed_handles.append(coll_name)

        if len(failed_handles) > 0:
            print 'Failed to obtain handles for the following objects: {}'.format(failed_handles)

        return object_handles

    def _get_goal_distance_data(self):
        # TODO
        pass

    def _get_proximity_sensor_distances(self):
        # TODO
        pass

    def _generate_sensor_data_vector(self):
        # TODO
        pass

    def _apply_all_joint_positions(self, positions_to_apply):
        print 'Moving robot to new configuration: {}'.format(map(lambda x: x[1], positions_to_apply))
        # TODO pause communications
        for joint, position in positions_to_apply:
            object_handle = self._scene_handles[joint]
            code = vrep.simxSetJointPosition(self._client_id, object_handle, position, vrep.simx_opmode_blocking)

            if code != vrep.simx_return_ok:
                raise SimulatorException('[Code {}] Failed to move joint {} with handle {} to position {}.')\
                    .format(code, joint, object_handle, position)
        # TODO unpause communications

    # both these functions assume that streaming has been started and will fail if not
    def _read_all_sensors(self):
        streamed_sensor_data = []
        for sensor in PROXIMITY_SENSORS:
            sensor_handle = self._scene_handles[sensor]
            code, state, point, handle, normal = vrep.simxReadProximitySensor(self._client_id, sensor_handle, vrep.simx_opmode_buffer)
            # create list of tuples of distance and normal for each sensor
            distance = self._distance_from_sensor_to_point(sensor, point)
            streamed_sensor_data.append((distance, normal))
        return streamed_sensor_data


    def _read_all_collisions(self):
        collisions = []
        for collision_object_name in COLLISION_OBJECTS:
            collision_handle = self._scene_handles[collision_object_name]
            code, state = vrep.simxReadCollision(self._client_id, collision_handle, vrep.simx_opmode_buffer)
        collisions.append((collision_object_name, state))

    # Helper function -------------------------------------------------------------------------------------
    def _distance_to_point(sensor_name, point):
        return 1
