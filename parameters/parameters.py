import json
import os
import shutil


class Parameters:

    def __init__(self):

        global __parameters__

        for key, value in __parameters__.items():
            setattr(self, key, value)

    def dict(self):
        return {i: j for i, j in self.__dict__.items() if not i.startswith("__")}


def load(json_file=None):

    global __json_file__, __parameters__, n_positions, n_prices, n_firms, alpha, momentum, temp, n_simulations, \
        t_max, zombies_customers, mode, discrete, fields_of_view, fov_boundaries, \
        firm_class, unit_value

    if json_file is None:

        if not os.path.exists(__json_file__):
            shutil.copy("templates/parameters.json", __json_file__)

        json_file = __json_file__

    with open(json_file, "r") as f:
        set_items(json.load(f))


def get():
    global __parameters__
    return list(__parameters__.items())


def set_items(dict_like):

    global __parameters__
    __parameters__ = dict_like
    for i in __parameters__:
        globals()[i] = dict_like[i]


# Default json_file to use as parameters
__json_file__ = "parameters/parameters.json"

# Containers for parameters
__parameters__ = None

# Parameters
n_positions = None        # By default, 21.
n_prices = None           # By default, 11
n_firms = None            # We will assume that it is 2. A change can induce not expected behaviors.
alpha = None              # Range is 0-1
momentum = None           # Range is 0-1
temp = None               # Range is 0-1
n_simulations = None
t_max = None
zombies_customers = None  # If true, customers will have no learning abilities
mode = None               # Could be "p_fixed" or "r_fixed
discrete = None
fields_of_view = None
fov_boundaries = None
firm_class = None
unit_value = None

# -------------------------- #

load()
