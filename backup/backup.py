import numpy as np
import os
import pickle
import json

from utils import utils


class Backup:

    pickle_folder = "data/pickle"
    os.makedirs(pickle_folder, exist_ok=True)

    json_folder = "data/json"
    os.makedirs(json_folder, exist_ok=True)

    def __init__(self, parameters):

        self.parameters = parameters

    def save(self):

        file_name = "{}".format(utils.timestamp())

        # Save a summary of parameters in json
        with open("{}/{}.json".format(self.json_folder, file_name), "w") as f:

            param = self.parameters.dict()
            param.update({"name": file_name})

            json.dump(param, f, indent=2)

        with open("{}/{}.p".format(self.pickle_folder, file_name), "wb") as f:
            pickle.dump(self, f)

        return file_name

    @classmethod
    def load(cls, file_name, folder_name):

        if folder_name is None:
            folder_name = cls.pickle_folder

        with open("{}/{}.p".format(folder_name, file_name), "rb") as f:
            return pickle.load(f)


class RunBackup(Backup):

    def __init__(self, parameters, seed, field_of_view):
        super().__init__(parameters)

        self.seed = seed
        self.field_of_view = field_of_view

        self.positions = np.zeros((parameters.t_max, parameters.n_firms), dtype=int)
        self.prices = np.zeros((parameters.t_max, parameters.n_firms), dtype=int)
        self.profits = np.zeros((parameters.t_max, parameters.n_firms))

    def update(self, t, positions, prices, profits):

        self.positions[t] = positions
        self.prices[t] = prices
        self.profits[t] = profits


class PoolBackup(Backup):

    def __init__(self, parameters, backups):
        super().__init__(parameters)

        self.backups = backups

