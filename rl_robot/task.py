from pybrain.rl.environments.episodic import EpisodicTask
from sim_constants import ACTOR_LIMITS


class Task(EpisodicTask):
    EPISODE_MAX_STEPS = 300
    COLLISION_REWARD = -10000
    GOAL_REWARD = 10
    GOAL_RADIUS = 0.05
    DELTA_DISTANCE_REWARD_CONSTANT = 1

    def __init__(self, environment):
        super(Task, self).__init__(environment)
        self.actor_limits = ACTOR_LIMITS

    def reset(self):
        self.env.teardown()

        super(Task, self).reset()
        self._should_finish = False
        self._last_distance_from_goal = 9999.99

    def isFinished(self):
        return self._should_finish or (self.samples >= Task.EPISODE_MAX_STEPS)

    def getReward(self):
        if self.env.isColliding():
            self._should_finish = True
            return Task.COLLISION_REWARD

        total_reward = 0
        distance_from_goal = self.env.distanceFromGoal()

        total_reward += ((self._last_distance_from_goal - distance_from_goal)
                * Task.DELTA_DISTANCE_REWARD_CONSTANT)
        if distance_from_goal <= Task.GOAL_RADIUS:
            total_reward += Task.GOAL_REWARD * (Task.EPISODE_MAX_STEPS - self.samples)
            self._should_finish = True

        return total_reward
