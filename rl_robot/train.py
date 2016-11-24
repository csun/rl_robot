from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments import Experiment
from pybrain.rl.learners import Q
from pybrain.rl.learners.valuebased import ActionValueNetwork

from environment import Environment
from task import Task


def main():
    # TODO Connect environment to v-rep server
    environment = Environment(...)
    task = Task(environment)
    # TODO figure out how to initialize this
    cotroller = ActionValueNetwork(...)
    agent = LearningAgent(controller, Q())

    experiment = Experiment(task, agent)

    # TODO Define better end condition for training loop
    while True:
        # TODO figure out how many steps of interaction to do
        experiment.doInteractions(...)
        agent.learn()
        agent.reset()
        environment.reset()
        # TODO use pickle to save model evey N iterations


if __name__ == '__main__':
    main()
