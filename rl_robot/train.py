import pickle

from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments import Experiment
from pybrain.rl.learners import Q
from pybrain.rl.learners.valuebased import ActionValueNetwork

from constants import *
from environment import Environment
from task import Task

MAX_TRAINING_ITERATIONS = 10000

def main():
    environment = Environment(LOCAL_HOST, PORT, PATH_TO_SCENE)
    task = Task(environment)

    # TODO figure out what to put for the params passed to ActionValueNetwork
    controller = ActionValueNetwork(Environment.indim, Environment.outdim)
    agent = LearningAgent(controller, Q())

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
