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
        time.sleep(2)
        self.getSensors()

    def isColliding(self):
        for collision in self._read_all_collisions():
            # check if a collision occurs
            return
        return False

    def getSensors(self):
        # TODO Update joint positions? Should probably print something if these
        # differ at all from the last action desired joint positions as if
        # they don't we can just query once at the start and trust those
        # TODO Convert proximity sensor data into distance and normal
        # TODO Make sure that data returned from this is the same as used for
        # calculating getReward at each step
        streamed_sensor_data = []
        for i in range(5):
            for sensor in PROXIMITY_SENSORS:
                sensor_handle = self._scene_handles[sensor]
                code, state, point, handle, normal = vrep.simxReadProximitySensor(self._client_id, sensor_handle, vrep.simx_opmode_buffer)
                print code
                if code != vrep.simx_return_ok:
                    time.sleep(0.1)
                    code, state, point, handle, normal = vrep.simxReadProximitySensor(self._client_id, sensor_handle, vrep.simx_opmode_buffer)
                    print 'Retried code {}'.format(code)
                    # raise Exception('Fatal: streaming data not available for sensor {}'.format(sensor))
                # create list of tuples of distance and normal for each sensor
                # TODO use point to calculate distance
                streamed_sensor_data.append((point, normal))

        # update only if relevant; also, print; in either case, return the current state of the world
        if self._sensor_data != streamed_sensor_data:
            self._sensor_data = streamed_sensor_data
            print 'Updated sensors {}'.format(self._sensor_data)

        return self._sensor_data


    def performAction(self, deltas):
        # just pass in a list of joint angle changes that matches the order in state (see: self._joint_positions)
        if len(deltas) != len(JOINTS):
            raise SimulatorException('Given deltas object length [{}] does not match num joints [{}]').format(len(deltas), len(JOINTS))

        # pause communication

        # Increment joint positions by action and apply to the robot
        self._joint_positions = [jp + djp for jp, djp in zip(self._joint_positions, deltas)]
        self._apply_all_joint_positions(self._joint_positions)

        # unpause

    def reset(self):
        # first load up the original scene
        scene_did_load = vrep.simxLoadScene(self._client_id, self._scene_file, 0, vrep.simx_opmode_blocking)
        if scene_did_load != vrep.simx_return_ok:
            raise SimulatorException('Could not load scene')

        # get collision handles, joint handles, etc.
        self._scene_handles = self._load_scene_handles()

        self._sensor_data = None

        # start streaming for all collision
        for collision in COLLISION_OBJECTS:
            collision_handle = self._scene_handles[collision]
            # TODO start streaming

        # TODO start streaming for all proximity sensors
        for sensor in PROXIMITY_SENSORS:
            sensor_handle = self._scene_handles[sensor]
            code, state, point, handle, normal = vrep.simxReadProximitySensor(self._client_id, sensor_handle, vrep.simx_opmode_streaming)


        # generate random positions in environment for robot and goal - store all in env
        self._joint_positions = self._generate_joint_positions()

        print 'Generated the following {} initial positions for each of the robot\'s joints:\n{}'\
            .format(len(self._joint_positions), self._joint_positions)

        # apply joint positions
        self._apply_all_joint_positions(zip(JOINTS, self._joint_positions))

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

    def _generate_joint_positions(self):
        return [2 * math.pi * random.random() for _ in JOINTS]

    def _apply_all_joint_positions(self, positions_to_apply):
        for joint, position in positions_to_apply:
            object_handle = self._scene_handles[joint]
            code = vrep.simxSetJointPosition(self._client_id, object_handle, position, vrep.simx_opmode_blocking)

            if code != vrep.simx_return_ok:
                raise SimulatorException('[Code {}] Failed to move joint {} with handle {} to position {}.')\
                    .format(code, joint, object_handle, position)

    # both these functions assume that streaming has been started and will fail if not
    def _read_all_sensors(self):
        pass


    def _read_all_collisions(self):
        pass
