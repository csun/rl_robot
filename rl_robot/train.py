import pickle
import signal
import sys
import time

from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments import EpisodicExperiment
from pybrain.rl.agents.linearfa import LinearFA_Agent
from pybrain.rl.learners.valuebased.nfq import NFQ
from pybrain.rl.learners.valuebased.linearfa import Q_LinFA
from pybrain.rl.learners.valuebased import ActionValueNetwork
from pybrain.rl.explorers.continuous import NormalExplorer
from pybrain.structure.modules import Module
from pybrain.tools.shortcuts import buildNetwork
from pybrain.rl.agents import OptimizationAgent
from pybrain.optimization import PGPE

from constants import *
from environment import Environment
from task import Task


TRAINING_ITERATIONS = 10


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

    # controller = Controller(Environment.outdim, Environment.indim)
    # controller = ActionValueNetwork(Environment.outdim, Environment.indim)
    # learner = Q_LinFA(Environment.indim, Environment.outdim)
    # learner = NFQ()
    # learner.explorer = NormalExplorer(Environment.indim)

    # agent = LearningAgent(controller, learner)
    # agent = LinearFA_Agent(learner)
    net = buildNetwork(Environment.outdim, Environment.indim)
    agent = OptimizationAgent(net, PGPE())

    experiment = EpisodicExperiment(task, agent)

    def signal_handler(signal, frame):
        print 'Exiting gracefully'
        environment.teardown()
        # TODO also pickle here
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        time.sleep(1)
        print 'NEW ITERATION'
        experiment.doEpisodes(Task.EPISODE_MAX_STEPS)
        # experiment.doInteractions(TRAINING_ITERATIONS)
        # agent.learn()
        # agent.reset()
        # environment.reset()

        # TODO check if iteration is mod something or other
            # TODO if true, write to pickle
            # TODO if not, check if the model params have converged if possible?


if __name__ == '__main__':
    main()
