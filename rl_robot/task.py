from pybrain.rl.environments.task import Task as PybrainTask


class Task(PybrainTask):
    COLLISION_REWARD = -1000
    REWARD_CONSTANT = 10.0

    def __init__(self, environment):
        self.env = environment

    def getReward(self):
        if self.env.isColliding():
            return COLLISION_REWARD
        return REWARD_CONSTANT / self.env._distance_from_goal
