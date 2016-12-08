import pickle
import signal
import sys

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


TRAINING_ITERATIONS = 360


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

    def signal_handler(signal, frame):
        print 'Exiting gracefully'
        environment.teardown()
        # TODO also pickle here
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        experiment.doInteractions(TRAINING_ITERATIONS)
        agent.learn()
        agent.reset()
        environment.reset()

        # TODO check if iteration is mod something or other
            # TODO if true, write to pickle
            # TODO if not, check if the model params have converged if possible?

    # TODO ????
    return environment.teardown()


if __name__ == '__main__':
    main()
