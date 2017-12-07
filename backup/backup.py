import numpy as np
import os
import pickle
import json

from utils import utils
import parameters


class Backup:

    pickle_folder = "data/pickle"
    os.makedirs(pickle_folder, exist_ok=True)

    def __init__(self):
        pass

    def save(self):

        file_name = "backup_{}".format(utils.timestamp())

        with open("{}/{}.p".format(self.pickle_folder, file_name), "wb") as f:
            pickle.dump(self, f)

        return file_name

    def load(self, file_name):

        with open("{}/{}.p".format(self.pickle_folder, file_name), "rb") as f:
            return pickle.load(f)


class RunBackup(Backup):

    def __init__(self, seed, field_of_view):
        super().__init__()

        self.seed = seed
        self.field_of_view = field_of_view

        self.positions = np.zeros((parameters.t_max, parameters.n_firms), dtype=int)
        self.prices = np.zeros((parameters.t_max, parameters.n_firms), dtype=int)
        self.profits = np.zeros((parameters.t_max, parameters.n_firms), dtype=int)

    def update(self, t, positions, prices, profits):

        self.positions[t] = positions
        self.prices[t] = prices
        self.profits[t] = profits


class PoolBackup(Backup):

    json_folder = "data/json"
    os.makedirs(json_folder, exist_ok=True)

    def __init__(self, backups):
        super().__init__()

        self.backups = backups
        self.parameters = parameters.Parameters()

    def save(self):

        # Save data in pickle
        file_name = super().save()

        # Save a summary of parameters in json
        with open("{}/{}.json".format(self.json_folder, file_name), "w") as f:

            param = {"name": file_name}
            param.update(self.parameters.dict())

            json.dump(param, f, indent=2)
