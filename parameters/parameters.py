import json
import os
import shutil


class Parameters:

    def __init__(
            self, n_positions=21, n_prices=11,
            n_firms=2, alpha=0.1, momentum=0.0, temp=0.02,
            n_simulations=10, t_max=3000, unit_value=1,
            zombies_customers=True,
            fov_mode='r_fixed', running_mode='default',
            fov_if_unique=0.5,
            fov_if_discrete=(0.25, 0.5),
            fov_boundaries=(0, 1),
            firm_class=("Firm", "Firm"), name=""):

        self.n_positions = n_positions  # By default, 21.
        self.n_prices = n_prices  # By default, 11
        self.n_firms = n_firms  # We will assume that it is 2. A change can induce not expected behaviors.
        self.alpha = alpha  # Range is 0-1
        self.momentum = momentum  # Range is 0-1
        self.temp = temp  # Range is 0-1
        self.n_simulations = n_simulations
        self.t_max = t_max
        self.zombies_customers = zombies_customers  # If true, customers will have no learning abilities
        self.fov_mode = fov_mode  # Could be "p_fixed" or "r_fixed
        self.running_mode = running_mode  # Can be 'default' or 'unique' or 'discrete'
        self.fov_if_unique = fov_if_unique  # Will be used if 'running_mode' is set to 'unique'
        self.fov_if_discrete = fov_if_discrete  # Will be used if 'running_mode' equal to discrete
        self.fov_boundaries = fov_boundaries  # Will be used when fov is randomly drawn
        self.firm_class = firm_class  # Could be "PseudoOptimalFirm", "Firm", "Stupid"
        self.unit_value = unit_value  # Default is one
        self.name = name

    def dict(self):
        return {i: j for i, j in self.__dict__.items() if not i.startswith("__")}


def load(json_file=None):

    if json_file is None:

        json_file = "parameters/parameters.json"

        if not os.path.exists(json_file):
            shutil.copy("templates/parameters.json", json_file)

    with open(json_file, "r") as f:
        return Parameters(**json.load(f))
