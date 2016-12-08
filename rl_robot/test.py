from environment import Environment

from constants import *
from utils import _generate_unique_filename
import time

def main():
    # TODO create an environment object and start interfacing with it
    environment = Environment(LOCAL_HOST, PORT, PATH_TO_SCENE)
    environment.performAction([1] * 7)
    print environment.getSensors()
    return environment.teardown()

if __name__ == '__main__':
    main()
