import pickle
import signal
import sys
import os
from glob import glob
import time

from pybrain.optimization import PGPE
from pybrain.rl.agents import OptimizationAgent
from pybrain.rl.experiments import EpisodicExperiment
from pybrain.tools.shortcuts import buildNetwork

from constants import *
from environment import Environment
from task import Task


AUTOSAVE_INTERVAL = 10


def main():
    if len(sys.argv) != 2:
        print 'Please provide a path to a model data directory.'
        print ('The script will load the newest model data from the directory,'
               'then continue to improve that model')
        sys.exit(0)

    model_directory = sys.argv[1]
    existing_models = sorted(glob(os.path.join(model_directory, '*.rlmdl')))

    if existing_models:
        newest_model_name = existing_models[-1]
        iteration_count = int(newest_model_name[-12:-6]) + 1
        print 'Loading model {}'.format(newest_model_name)

        newest_model = open(newest_model_name, 'r')
        agent = pickle.load(newest_model)
    else:
        net = buildNetwork(Environment.outdim,
                           Environment.outdim + Environment.indim,
                           Environment.indim)
        agent = OptimizationAgent(net, PGPE())
        iteration_count = 1

    environment = Environment(LOCAL_HOST, PORT, PATH_TO_SCENE)
    task = Task(environment)


    experiment = EpisodicExperiment(task, agent)


    def signal_handler(signal, frame):
        print 'Exiting gracefully'
        environment.teardown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)


    while True:
        time.sleep(1)

        print '>>>>> Running iteration {}'.format(iteration_count)
        # NOTE this weird stuff is hacky, but we need it to plug in our autosave
        # stuff properly. Took a long time to figure this out.
        experiment.optimizer.maxEvaluations = experiment.optimizer.numEvaluations + experiment.optimizer.batchSize

        try:
            experiment.doEpisodes()
        except Exception as e:
            print 'ERROR RUNNING SIMULATION: \n{}'.format(e)
            environment.teardown()
        else:
            if iteration_count % AUTOSAVE_INTERVAL == 0:
                filename = str(iteration_count).zfill(6) + '.rlmdl'
                filename = os.path.join(model_directory, filename)
                f = open(filename, 'w+')
                print 'Saving model to {}'.format(filename)

                pickle.dump(agent, f)

            iteration_count += 1

        print 'Iteration finished <<<<<'


if __name__ == '__main__':
    main()
