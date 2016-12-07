import sys
import math
import random
import time

import numpy as np
import vrep
from pybrain.rl.environments.environment import Environment as PybrainEnvironment

from sim_constants import *


class ConnectionException(Exception):
    pass


class SimulatorException(Exception):
    pass


class Environment(PybrainEnvironment):
    
    # All joint positions
    # All proximity sensor distances
    # Distance to goal vector
    outdim = len(JOINTS) + len(PROXIMITY_SENSORS) + 3
    indim = len(JOINTS)

    def __init__(self, address, port, scene_file):
        self._scene_file = scene_file
        self._client_id = vrep.simxStart(address, port, True, True, 5000, 5)

        if self._client_id == -1:
            raise ConnectionException('Could not connect')

        # set joint angles and start streaming
        self.reset()
        self.getSensors()

    def isColliding(self):
        return self._is_colliding

    def distanceFromGoal(self):
        return np.linalg.norm(np.array(self._distance_vector_to_goal))

    def getSensors(self):
        # If we haven't moved since the last sensor reading, our old sensor readings are still correct.
        if self._current_sensor_step == self._current_action_step:
            return self._sensor_data_vector

        self._check_for_collisions()
        self._get_goal_distance_data()
        self._get_proximity_sensor_distances()
        self._generate_sensor_data_vector()

        self._current_sensor_step = self._current_action_step

        return self._sensor_data_vector

    def performAction(self, deltas):
        # just pass in a list of joint angle changes that matches the order in state (see: self._joint_positions)
        if len(deltas) != len(JOINTS):
            raise SimulatorException('Given deltas object length [{}] does not match num joints [{}]').format(len(deltas), len(JOINTS))

        # Increment joint positions by action and apply to the robot
        # TODO figure out how to specify how many deltas Learner can provide to env and max / min delta value
        # TODO figure out how to set joint limits as well
        self._joint_positions = [(jp[0], jp[1] + djp) for jp, djp in zip(self._joint_positions, deltas)]
        self._apply_all_joint_positions()
        self._current_action_step += 1
        time.sleep(0.1)

    def reset(self):
        # first load up the original scene
        scene_did_load = vrep.simxLoadScene(self._client_id, self._scene_file, 0, vrep.simx_opmode_blocking)
        if scene_did_load != vrep.simx_return_ok:
            raise SimulatorException('Could not load scene')

        self._goal_point = np.array([0, 0, 0])
        self._current_action_step = 0
        self._current_sensor_step = None
        # Tuple of joint handle and current position
        self._joint_positions = [(None, 0)] * len(JOINTS)
        self._distance_vector_to_goal = np.array([0, 0, 0])
        self._proximity_sensor_distances = [sys.maxint] * len(PROXIMITY_SENSORS)
        self._is_colliding = False
        self._sensor_data_vector = [0] * Environment.outdim

        # get collision handles, joint handles, etc.
        self._scene_handles = self._load_scene_handles()

        self._generate_goal_position()

        vrep.simxStartSimulation(self._client_id, vrep.simx_opmode_blocking)
        time.sleep(0.1)

        self._start_streaming()

        # sleep after streaming starts for data to roll in
        time.sleep(1)

        # We want to get sensors once so that things like _distance_from_goal are properly initialized
        self.getSensors()

    # shut down environment gracefully to avoid problems with vrep
    def teardown(self):
        print 'Stopping data streaming for all collisions.'
        for collision in COLLISION_OBJECTS:
            collision_handle = self._scene_handles[collision]
            code = vrep.simxReadCollision(self._client_id, collision_handle, vrep.simx_opmode_discontinue)[0]
            if code != vrep.simx_return_ok:
                raise Exception('Failed to stop streaming from a collision object.')

        print 'Stopping data streaming for all proximity sensors.'
        for sensor in PROXIMITY_SENSORS:
            sensor_handle = self._scene_handles[sensor]
            code = vrep.simxReadProximitySensor(self._client_id, sensor_handle, vrep.simx_opmode_discontinue)[0]
            if code != vrep.simx_return_ok:
                raise Exception('Failed to stop streaming from a sensor.')

        # pray that graceful shutdown actually happened
        print 'Stopping simulation.'

        vrep.simxStopSimulation(self._client_id, vrep.simx_opmode_blocking)
        time.sleep(0.1)

        return True

    # Scene Configuration Helper Functions ----------------------------------------------------------------
    def _load_scene_handles(self):
        def handle_failure(name):
            raise SimulatorException('Failed to get handle for {}'.format(name))

        # load all objects
        print 'Loading all objects...'
        object_handles = {}
        for obj_name in LINKS + JOINTS + PROXIMITY_SENSORS + [TIP_OBJECT]:
            code, handle = vrep.simxGetObjectHandle(self._client_id, obj_name, vrep.simx_opmode_blocking)
            if code == vrep.simx_return_ok:
                object_handles[obj_name] = handle
            else:
                handle_failure(obj_name)
        # load collisions -- use the same map as for objects
        print 'Loading all collisions...'
        for coll_name in COLLISION_OBJECTS:
            code, handle = vrep.simxGetCollisionHandle(self._client_id, coll_name, vrep.simx_opmode_blocking)
            if code == vrep.simx_return_ok:
                object_handles[coll_name] = handle
            else:
                handle_failure(coll_name)

        for index, joint in enumerate(JOINTS):
            self._joint_positions[index] = (object_handles[joint], 0)

        return object_handles

    def _start_streaming(self):
        print 'Beginning to stream all collisions.'
        for collision in COLLISION_OBJECTS:
            collision_handle = self._scene_handles[collision]
            code = vrep.simxReadCollision(self._client_id, collision_handle, vrep.simx_opmode_streaming)[0]
            if code != vrep.simx_return_novalue_flag:
                raise SimulatorException('Failed to start streaming for collision object {}'.format(collision))

        print 'Beginning to stream data for all proximity sensors.'
        for sensor in PROXIMITY_SENSORS:
            sensor_handle = self._scene_handles[sensor]
            code = vrep.simxReadProximitySensor(self._client_id, sensor_handle, vrep.simx_opmode_streaming)[0]
            if code != vrep.simx_return_novalue_flag:
                raise SimulatorException('Failed to start streaming for proximity sensor {}'.format(sensor))

        print 'Beginning to stream data for robot tip.'
        code = vrep.simxGetObjectPosition(self._client_id, self._scene_handles[TIP_OBJECT], -1, vrep.simx_opmode_streaming)[0]
        if code != vrep.simx_return_novalue_flag:
            raise SimulatorException('Failed to start streaming for robot tip')

    def _generate_goal_position(self):
        goal_area = random.choice(POTENTIAL_GOAL_AREAS)
        lower_bound = goal_area[0]
        ranges = goal_area[1]

        for i in range(3):
            self._goal_point[i] = lower_bound[i] + (random.random() * ranges[i])

    def _get_goal_distance_data(self):
        code, tip_position = vrep.simxGetObjectPosition(self._client_id, self._scene_handles[TIP_OBJECT], -1, vrep.simx_opmode_buffer)

        if code != vrep.simx_return_ok:
            raise SimulatorException('Failed to get tip position.')

        self._distance_vector_to_goal = np.subtract(tip_position, self._goal_point)
        self._distance_from_goal = np.linalg.norm(self._distance_vector_to_goal)

    def _get_proximity_sensor_distances(self):
        self._normals = []
        self._proximity_sensor_distances = []

        for sensor in PROXIMITY_SENSORS:
            sensor_handle = self._scene_handles[sensor]
            code, state, point, handle, normal = vrep.simxReadProximitySensor(self._client_id, sensor_handle, vrep.simx_opmode_buffer)
            if code == vrep.simx_return_ok:
                self._normals.append(normal)

                if state: # not detecting anything
                    self._proximity_sensor_distances.append(np.linalg.norm(np.array(point)))
                else:
                    self._proximity_sensor_distances.append(sys.maxint)
            else:
                raise SimulatorException('Failed to stream from sensor [{}].'.format(sensor))

        if len(self._normals) != len(PROXIMITY_SENSORS) or len(self._proximity_sensor_distances) != len(PROXIMITY_SENSORS):
            raise SimulatorException('Improper parity of data vector.')

        print 'Finished loading all normals and distances...'

    def _generate_sensor_data_vector(self):
        data_vector_index = 0

        def add_all(arr):
            for element in arr:
                self._sensor_data_vector[data_vector_index] = element
                data_vector_index += 1

        for _, position in self._joint_positions:
            self._sensor_data_vector[data_vector_index] = position
            data_vector_index += 1
        add_all(self._proximity_sensor_distances)
        add_all(self._distance_vector_to_goal)

    def _apply_all_joint_positions(self):
        print 'Moving robot to new configuration: {}'.format(map(lambda x: x[1], positions_to_apply))
        vrep.simxPauseCommunication(self._client_id, True)

        for joint_handle, position in self._joint_positions:
            code = vrep.simxSetJointPosition(self._client_id, joint_handle, position, vrep.simx_opmode_blocking)

            if code != vrep.simx_return_ok:
                raise SimulatorException('[Code {}] Failed to move joint {} with handle {} to position {}.')\
                    .format(code, joint, object_handle, position)

        vrep.simxPauseCommunication(self._client_id, True)

    def _check_for_collisions(self):
        self._is_colliding = False

        for collision_object_name in COLLISION_OBJECTS:
            collision_handle = self._scene_handles[collision_object_name]
            code, state = vrep.simxReadCollision(self._client_id, collision_handle, vrep.simx_opmode_buffer)

            if code == vrep.simx_return_ok and state:
                print 'COLLISION DETECTED WITH {}'.format(collision_object_name)
                self._is_colliding = True
                return
