from environment import Environment

from constants import *
from utils import _generate_unique_filename

def main():
    # TODO create an environment object and start interfacing with it
    environment = Environment(LOCAL_HOST, PORT, PATH_TO_SCENE)
    return environment.teardown()

if __name__ == '__main__':
    main()
