import numpy as np
import os
import pickle

from utils import utils
import parameters


class Backup:

    def __init__(self):
        pass

    def save(self):

        if not os.path.exists("data"):
            os.mkdir("data")

        with open("data/backup_{}.p".format(utils.timestamp()), "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, file_name):

        with open("data/{}.p".format(file_name), "rb") as f:

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

    def __init__(self, backups):
        super().__init__()

        self.backups = backups
        self.parameters = parameters.Parameters()
