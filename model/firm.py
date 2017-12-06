import numpy as np

import mlp
import utils
import parameters


class AbstractFirm(object):

    """Abstract class for firm"""

    def __init__(self, x, price):

        # Position and price
        self.x = x
        self.price = price

        # Max profit used for computing utility
        self.max_profit = parameters.n_positions * (parameters.n_prices + 1)

        self.profit = 0

    def sell_x_units(self, x):
        self.profit += self.price * x

    def reset_profit_counter(self):
        self.profit = 0

    def _u(self):

        # # According to Barreda, should be:
        # return self.profit ** self.r
        # But it is better if all values lies between 0 and 1 for applying RL
        return self.profit / self.max_profit

    def change_in_opponents_strategies(self, old_opponents_positions, old_opponents_prices):
        pass

    def select_strategy(self, opponents_positions, opponents_prices):
        pass


class NeuralNetworkFirm(AbstractFirm):

    """Abstract class"""

    alpha = parameters.alpha
    momentum = parameters.momentum
    temp = parameters.temp

    options = np.arange(parameters.n_positions * parameters.n_prices)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Size of input depend of the level of strategy
        self.network_input = np.zeros(self._get_network_input_size())

        # Output of network is expected profit; this will contain expected profit for each option
        self.network_outputs = np.zeros(self.options.size)

        self.network = self._create_network()

        # Create a mapping between int and 'strategy', a 'strategy' composed here by
        # a particular position and a particular price
        self.strategies = self._get_strategies()

        self.set_up()

    @classmethod
    def _get_strategies(cls):

        st = {}
        i = 0
        for pos in range(parameters.n_positions):
            for price in range(1, parameters.n_prices + 1):
                st[i] = {
                    "position": pos,
                    "price": price
                }
                i += 1

        return st

    def set_up(self):

        self.network.reset()

    def change_in_opponents_strategies(self, old_opponents_positions, old_opponents_prices):

        self._learn(
            opponents_positions=old_opponents_positions, opponents_prices=old_opponents_prices
        )

    def select_strategy(self, opponents_positions, opponents_prices):

        self._learn(
            opponents_positions=opponents_positions, opponents_prices=opponents_prices
        )

        self._get_network_outputs(
            opponents_positions=opponents_positions, opponents_prices=opponents_prices
        )

        p = utils.softmax(self.network_outputs, temp=self.temp)

        st = np.random.choice(self.options, p=p)
        self.x = self.strategies[st]["position"]
        self.price = self.strategies[st]["price"]

    def _get_network_outputs(self, opponents_positions, opponents_prices):

        for i in self.options:
            self._set_network_input(
                x=self.strategies[i]["position"], price=self.strategies[i]["price"],
                opponents_positions=opponents_positions, opponents_prices=opponents_prices
            )
            self.network_outputs[i] = self.network.propagate_forward(self.network_input)

    def _learn(self, opponents_positions, opponents_prices):

        self._set_network_input(x=self.x, price=self.price,
                                opponents_prices=opponents_prices, opponents_positions=opponents_positions)
        self.network.propagate_forward(self.network_input)
        self.network.propagate_backward(target=self._u(), lrate=self.alpha,
                                        momentum=self.momentum)

    def _create_network(self):

        return mlp.MLP(self.network_input.size, self.network_input.size, 1)

    @classmethod
    def _get_network_input_size(cls):

        return 0

    def _set_network_input(self, x, price, opponents_positions, opponents_prices):

        pass


class Firm(NeuralNetworkFirm):

    """Strategic firm using a neural network"""
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.set_up()

    @classmethod
    def _get_network_input_size(cls):
        return parameters.n_firms*parameters.n_positions + parameters.n_firms*parameters.n_prices

    def _set_network_input(self, x, price, opponents_positions, opponents_prices):

        b_position = np.zeros(parameters.n_positions, dtype=int)
        b_price = np.zeros(parameters.n_prices, dtype=int)

        network_input = []

        b_position[x] = 1
        b_price[price-1] = 1   # min price is 1 (not 0)

        network_input += list(b_position)
        network_input += list(b_price)

        for opp_pos, opp_price in zip(opponents_positions, opponents_prices):

            b_position[:] = 0
            b_price[:] = 0
            b_position[opp_pos] = 1
            b_price[opp_price-1] = 1  # min price is 1 (not 0)

            network_input += list(b_position)
            network_input += list(b_price)

        self.network_input[:] = network_input
