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

        # TODO get collision handles, joint handles, etc.

        self.reset()

    def isColliding(self):
        # TODO
        pass

    def getSensors(self):
        # TODO Collect values from v-rep and turn into some sort of state object
        # to be returned
        pass

    def performAction(self, action):
        # TODO Use the action object to affect change in the v-rep sim
        # TODO store joint positions to start
        # pause communication
        # Increment joint positions by action
        # Send all new joint positions
        # unpause
        pass

    def reset(self):
        return_code = vrep.simxLoadScene(self._client_id, scene_file)
        if return_code != vrep.simx_return_ok:
            raise SimulatorException('Could not load scene')

