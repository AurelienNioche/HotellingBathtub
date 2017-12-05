import numpy as np


def softmax(x, temp):
    """Compute softmax values
    for each sets of scores in x."""

    e_x = np.exp(x / temp)

    return e_x / e_x.sum()


def normalize(x, min_, max_):
    x_scaled = (x - min_) / (max_ - min_)
    return x_scaled
