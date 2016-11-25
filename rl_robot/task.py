from pybrain.rl.environments.task import Task as PybrainTask


class Task(PybrainTask):
    # TODO generate random positions in environment for robot and goal
    COLLISION_REWARD = -1000

    def getReward(self):
        if self.env.isColliding():
            return COLLISION_REWARD
        # TODO At each timestep just how close to goal end manipulator is
        # TODO check environment for collisions and cause serious negative reward
        pass
