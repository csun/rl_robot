import time

MODEL_FILE_PATTERN = 'reinforcement_learning_robot_model_{}.pkl'

def _generate_unique_filename():
    return MODEL_FILE_PATTERN.format(int(time.time() * 100))
