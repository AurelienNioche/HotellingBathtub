# import parameters


class AbstractFirm(object):

    """
    Abstract class for firm
    """

    # Max profit used for computing utility

    def __init__(self, x, price, parameters, **kwargs):

        self.parameters = parameters
        self.max_profit = parameters.n_positions * parameters.n_prices * parameters.unit_value
        # Position and price
        self.x = x
        self.price = price

    def _u(self, profit):

        # # According to Barreda, should be:
        # return self.profit ** self.r
        # But it is better if all values lies between 0 and 1 for applying RL
        return profit / self.max_profit

    def learn(self, profit):
        raise NotImplementedError

    def select_strategy(self, opponents_positions, opponents_prices):
        raise NotImplementedError
