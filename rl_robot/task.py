from pybrain.rl.environments.task import Task as PybrainTask
from sim_constants import ACTOR_LIMITS


class Task(PybrainTask):
    COLLISION_REWARD = -10000
    GOAL_REWARD = 10
    GOAL_RADIUS = 0.05
    DELTA_DISTANCE_REWARD_CONSTANT = 1

    def __init__(self, environment):
        super(Task, self).__init__(environment)
        self.actor_limits = ACTOR_LIMITS

        self._last_distance_from_goal = 9999.99

    def getReward(self):
        if self.env.isColliding():
            return Task.COLLISION_REWARD

        total_reward = 0
        distance_from_goal = self.env.distanceFromGoal()

        total_reward += ((self._last_distance_from_goal - distance_from_goal)
                * Task.DELTA_DISTANCE_REWARD_CONSTANT)
        if distance_from_goal <= Task.GOAL_RADIUS:
            total_reward += GOAL_REWARD
