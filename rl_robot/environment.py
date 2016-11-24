from pybrain.rl.environments.environment import Environment as PybrainEnvironment


class Environment(PybrainEnvironment):

    def __init__(self):
        # TODO Some sort of connection information for v-rep?
        self.reset()

    def getSensors(self):
        # TODO Collect values from v-rep and turn into some sort of state object
        # to be returned
        pass

    def performAction(self, action):
        # TODO Use the action object to affect change in the v-rep sim
        pass

    def reset(self):
        # TODO Re-generate random positions in environment for robot and goal
        pass
