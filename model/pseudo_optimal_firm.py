import itertools as it
import parameters
import numpy as np

from . firm import AbstractFirm


class PseudoOptimalFirm(AbstractFirm):
    """Pseudo optimal player for a 2-players game"""

    options = np.array(list(it.product(range(parameters.n_positions), range(1, parameters.n_prices + 1))))

    def __init__(self, z, **kwargs):

        super().__init__(**kwargs)
        self.z = z

        self.exp_profits = np.zeros(len(self.options))

    def sell_x_units(self, x):
        self.profit += self.price * x

    def select_strategy(self, opponents_positions, opponents_prices):

        assert len(opponents_positions) == 1, \
            "This type of player is unable to play if there is more than one opponent"

        opp_pos = opponents_positions[0]
        opp_price = opponents_prices[0]

        for i, (pos, price) in enumerate(self.options):

            n_customers = self.z[pos, opp_pos, 0]

            to_share = self.z[pos, opp_pos, 2]

            if price < opp_price:
                n_customers += to_share

            elif price == opp_price:
                n_customers += round(to_share / 2)

            self.exp_profits[i] = price * n_customers

        idx = np.argwhere(self.exp_profits == np.amax(self.exp_profits))
        i = np.random.choice(idx)

        self.x, self.price = self.options[i]