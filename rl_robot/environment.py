import math
from pybrain.rl.environments.environment import Environment as PybrainEnvironment
import random
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

        self.reset()

    def isColliding(self):
        pass

    def getSensors(self):
        # TODO Update joint positions? Should probably print something if these
        # differ at all from the last action desired joint positions as if
        # they don't we can just query once at the start and trust those
        # TODO Convert proximity sensor data into distance and normal
        # TODO Make sure that data returned from this is the same as used for
        # calculating getReward at each step
        pass

    def performAction(self, action):
        # TODO Use the action object to affect change in the v-rep sim
        # pause communication
        # Increment joint positions by action
        # Send all new joint positions
        # unpause
        pass

    def reset(self):
        # get collision handles, joint handles, etc.
        self._scene_handles = self._load_scene_handles()

        # start streaming for all collision
        for collision in COLLISION_OBJECTS:
            collision_handle = self._scene_handles[collision]
            # TODO start streaming

        # TODO start streaming for all proximity sensors

        # generate random positions in environment for robot and goal - store all in env
        self._joint_positions = self._generate_joint_positions()

        print 'Generated the following {} positions for each of the robot\'s joints: {}'\
            .format(len(self._joint_positions), self._joint_positions)

        # apply joint positions
        self._apply_all_joint_positions(zip(JOINTS, self._joint_positions))

        return_code = vrep.simxLoadScene(self._client_id, self._scene_file, 0, vrep.simx_opmode_blocking)
        if return_code != vrep.simx_return_ok:
            raise SimulatorException('Could not load scene')

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
