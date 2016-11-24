from pybrain.rl.environments.task import Task as PybrainTask


class Task(PybrainTask):
    # TODO May not actually need to override anything. Seems like the base
    # implementation of Task handles a lot of stuff as long as the returns
    # from Environment are in expected format.
    pass
