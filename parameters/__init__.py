from . parameters import *


def items():

    return dict([(i, j) for i, j in parameters.__dict__.items() if not i.startswith("__")])


class Parameters:

    def __init__(self):

        for key, value in items().items():
            setattr(self, key, value)
