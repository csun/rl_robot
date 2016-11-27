from environment import Environment
import os

LOCAL_HOST = '127.0.0.1'
PATH_TO_SCENE = os.path.join(os.getcwd(), '../scene.ttt')

def main():
    # TODO create an environment object and start interfacing with it
    environment = Environment(LOCAL_HOST, 19997, PATH_TO_SCENE)


if __name__ == '__main__':
    main()
