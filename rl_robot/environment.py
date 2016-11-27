import vrep
from pybrain.rl.environments.environment import Environment as PybrainEnvironment


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
        # TODO store joint positions to start
        # TODO get collision handles, joint handles, etc.
        # TODO start streaming for all collision
        # TODO start streaming for all proximity sensors

        return_code = vrep.simxLoadScene(self._client_id, scene_file)
        if return_code != vrep.simx_return_ok:
            raise SimulatorException('Could not load scene')

