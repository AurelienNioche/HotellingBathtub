import numpy as np

from model import firm


class StupidFirm(firm.AbstractFirm):

    def __init__(self, parameters, **kwargs):
        super().__init__(parameters=parameters, **kwargs)

    def learn(self, profit):
        pass

    def select_strategy(self, opponents_positions, opponents_prices):

        self.x = np.random.randint(self.parameters.n_positions)
        self.price = np.random.randint(1, self.parameters.n_prices + 1)

        return self.x, self.price
