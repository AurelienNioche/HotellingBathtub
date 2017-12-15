import json
import os
import shutil


class Parameters:

    def __init__(
            self, n_positions, n_prices, n_firms, alpha, momentum, temp, n_simulations, t_max,
            zombies_customers, mode, discrete, fields_of_view, fov_boundaries, firm_class, unit_value):
        self.n_positions = n_positions  # By default, 21.
        self.n_prices = n_prices  # By default, 11
        self.n_firms = n_firms  # We will assume that it is 2. A change can induce not expected behaviors.
        self.alpha = alpha  # Range is 0-1
        self.momentum = momentum  # Range is 0-1
        self.temp = temp  # Range is 0-1
        self.n_simulations = n_simulations
        self.t_max = t_max
        self.zombies_customers = zombies_customers  # If true, customers will have no learning abilities
        self.mode = mode  # Could be "p_fixed" or "r_fixed
        self.discrete = discrete
        self.fields_of_view = fields_of_view
        self.fov_boundaries = fov_boundaries
        self.firm_class = firm_class
        self.unit_value = unit_value

    def dict(self):
        return {i: j for i, j in self.__dict__.items() if not i.startswith("__")}


def load(json_file=None):

    if json_file is None:

        json_file = "parameters/parameters.json"

        if not os.path.exists(json_file):
            shutil.copy("templates/parameters.json", json_file)

    with open(json_file, "r") as f:
        return Parameters(**json.load(f))
