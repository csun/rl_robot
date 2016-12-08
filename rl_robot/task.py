from pybrain.rl.environments.episodic import EpisodicTask
from sim_constants import ACTOR_LIMITS


class Task(EpisodicTask):
    EPISODE_MAX_STEPS = 300
    COLLISION_MAX_REWARD = -5
    COLLISION_MIN_REWARD = -10
    GOAL_BASE_REWARD = 20
    GOAL_REWARD_PER_STEP = 0.2
    GOAL_RADIUS = 0.05
    DELTA_DISTANCE_REWARD_BASE = 1.0
    DELTA_DISTANCE_REWARD_CAP = 2.0
    CONSECUTIVE_DIRECTIONAL_MULTIPLIER = 1.004

    def __init__(self, environment):
        super(Task, self).__init__(environment)
        self.actor_limits = ACTOR_LIMITS

    def reset(self):
        self.env.teardown()
        print '!!Total reward from last run {}!!'.format(self.cumreward)

        super(Task, self).reset()
        self._should_finish = False
        self._last_distance_from_goal = None
        self._delta_distance_reward_multiplier = Task.DELTA_DISTANCE_REWARD_BASE

    def isFinished(self):
        return self._should_finish or (self.samples >= Task.EPISODE_MAX_STEPS)

    def getReward(self):
        distance_from_goal = self.env.distanceFromGoal()

        if self._last_distance_from_goal == None:
            self._last_distance_from_goal = distance_from_goal

        if self.env.isColliding():
            self._should_finish = True
            reward = distance_from_goal * Task.COLLISION_MAX_REWARD
            return min(Task.COLLISION_MAX_REWARD, max(Task.COLLISION_MIN_REWARD, reward))
        elif distance_from_goal <= Task.GOAL_RADIUS:
            print 'REACHED GOAL'
            self._should_finish = True
            return Task.GOAL_BASE_REWARD + (Task.GOAL_REWARD_PER_STEP * (Task.EPISODE_MAX_STEPS - self.samples))
        elif (self._last_distance_from_goal < 0) == (distance_from_goal < 0):
            self._delta_distance_reward_multiplier *= Task.CONSECUTIVE_DIRECTIONAL_MULTIPLIER
            self._delta_distance_reward_multiplier = max(self._delta_distance_reward_multiplier, Task.DELTA_DISTANCE_REWARD_CAP)
        else:
            self._delta_distance_reward_multiplier = Task.DELTA_DISTANCE_REWARD_BASE

        reward = (self._last_distance_from_goal - distance_from_goal) * self._delta_distance_reward_multiplier
        self._last_distance_from_goal = distance_from_goal
        return reward
