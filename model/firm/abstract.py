import parameters


class AbstractFirm(object):

    """Abstract class for firm"""

    # Max profit used for computing utility
    max_profit = parameters.n_positions * parameters.n_prices

    def __init__(self, x, price, **kwargs):

        # Position and price
        self.x = x
        self.price = price

    def _u(self, profit):

        # # According to Barreda, should be:
        # return self.profit ** self.r
        # But it is better if all values lies between 0 and 1 for applying RL
        return profit / self.max_profit

    def learn(self, profit):
        pass

    def select_strategy(self, opponents_positions, opponents_prices):
        pass
