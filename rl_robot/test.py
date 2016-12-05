from environment import Environment
import os

LOCAL_HOST = '127.0.0.1'
PATH_TO_SCENE = os.path.join(os.getcwd(), '../scene.ttt')
PORT = 19997

def main():
    print PATH_TO_SCENE
    # TODO create an environment object and start interfacing with it
    environment = Environment(LOCAL_HOST, PORT, PATH_TO_SCENE)

if __name__ == '__main__':
    main()
