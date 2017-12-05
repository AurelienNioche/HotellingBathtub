import numpy as np


import parameters


class Backup:

    def __init__(self, seed, parameter_field_of_view):

        self.seed = seed
        self.parameter_field_of_view = parameter_field_of_view

        self.positions = np.zeros((parameters.t_max, parameters.n_firms), dtype=int)
        self.prices = np.zeros((parameters.t_max, parameters.n_firms), dtype=int)
        self.profits = np.zeros((parameters.t_max, parameters.n_firms), dtype=int)

    def update(self, t, positions, prices, profits):

        self.positions[t] = positions
        self.prices[t] = prices
        self.profits[t] = profits
