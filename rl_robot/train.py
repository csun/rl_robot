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
    controller = ActionValueNetwork(3, 3)
    agent = LearningAgent(controller, Q())

    experiment = Experiment(task, agent)

    # TODO Define better end condition for training loop
    for i in range(MAX_TRAINING_ITERATIONS):
        # TODO figure out how many steps of interaction to do
        # experiment.doInteractions(...)
        # agent.learn()
        # agent.reset()
        # environment.reset()
        # TODO use pickle to save model evey N iterations
        pass

    # TODO ????
    environment.teardown()


if __name__ == '__main__':
    main()
