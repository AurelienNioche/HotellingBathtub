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

        __parameters__ = json.load(f)

        # This will not me manipulated very often
        n_positions = __parameters__["n_positions"]  # By default, 21.
        n_prices = __parameters__["n_prices"]  # By default, 11
        n_firms = __parameters__["n_firms"]  # We will assume that it is 2. A change can induce not expected behaviors.

        alpha = __parameters__["alpha"]  # Range is 0-1
        momentum = __parameters__["momentum"]  # Range is 0-1
        temp = __parameters__["temp"]  # Range is 0-1

        # This will influence the computation time, but also the robustness of the results
        n_simulations = __parameters__["n_simulations"]
        t_max = __parameters__["t_max"]

        # These variables should affect results in an interesting manner
        zombies_customers = __parameters__["zombies_customers"]  # If true, customers will have no learning abilities
        mode = __parameters__["mode"]  # Could be "p_fixed" or "r_fixed
        discrete = __parameters__["discrete"]
        fields_of_view = __parameters__["fields_of_view"]
        fov_boundaries = __parameters__["fov_boundaries"]
        firm_class = __parameters__["firm_class"]
        unit_value = __parameters__["unit_value"]


def get():
    global __parameters__
    return list(__parameters__.items())


# Default json_file to use as parameters
__json_file__ = "parameters/parameters.json"

# Containers for parameters
__parameters__ = None

# Parameters
n_positions = None
n_prices = None
n_firms = None
alpha = None
momentum = None
temp = None
n_simulations = None
t_max = None
zombies_customers = None
mode = None
discrete = None
fields_of_view = None
fov_boundaries = None
firm_class = None
unit_value = None

# -------------------------- #

load()



