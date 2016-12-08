import pickle

from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments import Experiment
from pybrain.rl.learners import Q
from pybrain.rl.learners.valuebased import ActionValueNetwork
from pybrain.rl.explorers.continuous import NormalExplorer
from pybrain.structure.modules import Module
from pybrain.tools.shortcuts import buildNetwork

from constants import *
from environment import Environment
from task import Task

MAX_TRAINING_ITERATIONS = 10000


# TODO ideally this would be in a different file and I'd understand what
# it does better. Alas, deadlines.
class Controller(ActionValueNetwork):
    def __init__(self, dimState, numActions, name=None):
        Module.__init__(self, dimState, numActions, name)
        self.network = buildNetwork(dimState + numActions, dimState + numActions, numActions)
        self.numActions = numActions


def main():
    environment = Environment(LOCAL_HOST, PORT, PATH_TO_SCENE)
    task = Task(environment)

    controller = Controller(Environment.outdim, Environment.indim)
    learner = Q()
    learner.explorer = NormalExplorer(Environment.indim)

    agent = LearningAgent(controller, learner)

    experiment = Experiment(task, agent)

    for i in range(MAX_TRAINING_ITERATIONS):
        experiment.doInteractions()
        # agent.learn()
        # agent.reset()
        # environment.reset()

        # TODO check if iteration is mod something or other
            # TODO if true, write to pickle
            # TODO if not, check if the model params have converged if possible?

    # TODO ????
    return environment.teardown()


if __name__ == '__main__':
    main()
