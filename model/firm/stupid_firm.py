import numpy as np

from model import firm
import parameters


class StupidFirm(firm.AbstractFirm):

    def __init__(self):
        super().__init__()

    def learn(self, profit):
        pass

    def select_strategy(self, opponents_positions, opponents_prices):

        self.x = np.random.randint(parameters.n_positions)
        self.price = np.random.randint(1, parameters.n_prices + 1)

        return self.x, self.price
