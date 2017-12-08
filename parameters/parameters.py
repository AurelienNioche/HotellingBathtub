import json
import os
import shutil

# If you want the data to be saved (default is always on, but you could change that here)
save = True

__json_file__ = "parameters/parameters.json"

if not os.path.exists("parameters/parameters.json"):
    shutil.copy("templates/parameters.json", "parameters/parameters.json")

with open("parameters/parameters.json", "r") as f:

    __parameters__ = json.load(f)

    # Could use something as:
    # # for k, v in __parameters__.items():
    # #     vars()[k] = v
    # ... but it is more convenient to give explicitly all the params (allows using of auto-complete)

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
    zombies_customers = __parameters__["zombies_customers"]   # If true, customers will have no learning abilities
    mode = __parameters__["mode"]   # Could be "p_fixed" or "r_fixed
    discrete = __parameters__["discrete"]
    fields_of_view = __parameters__["fields_of_view"]
    fov_boundaries = __parameters__["fov_boundaries"]
    firm_class = __parameters__["firm_class"]


class Parameters:

    def __init__(self):

        for key, value in __parameters__.items():
            setattr(self, key, value)

    def dict(self):
        return {i: j for i, j in self.__dict__.items() if not i.startswith("__")}
