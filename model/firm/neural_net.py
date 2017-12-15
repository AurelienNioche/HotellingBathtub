import numpy as np

import mlp
import utils
# import parameters


from model.firm import AbstractFirm


class Firm(AbstractFirm):

    """Firm with learning"""

    def __init__(self, init_opp_positions, init_opp_prices, parameters, **kwargs):
        super().__init__(**kwargs)

        self.alpha = parameters.alpha
        self.momentum = parameters.momentum
        self.temp = parameters.temp

        self.parameters = parameters

        self.options = np.arange(parameters.n_positions * parameters.n_prices)

        # Size of input depend of the level of strategy
        self.network_input = np.zeros(self._get_network_input_size())

        # Output of network is expected profit; this will contain expected profit for each option
        self.network_outputs = np.zeros(self.options.size)

        self.network = self._create_network()

        # Create a mapping between int and 'strategy', a 'strategy' composed here by
        # a particular position and a particular price
        self.strategies = self._get_strategies()

        self.opp_positions = np.array(init_opp_positions, dtype=int)
        self.opp_prices = np.array(init_opp_prices, dtype=int)

        self._set_up()

    def _get_strategies(self):

        st = {}
        i = 0
        for pos in range(self.parameters.n_positions):
            for price in range(1, self.parameters.n_prices + 1):
                st[i] = {
                    "position": pos,
                    "price": price
                }
                i += 1

        return st

    def _set_up(self):

        self.network.reset()

    def learn(self, profit):

        self._set_network_input(x=self.x, price=self.price)
        self.network.propagate_forward(self.network_input)
        self.network.propagate_backward(target=self._u(profit=profit), lrate=self.alpha,
                                        momentum=self.momentum)

    def select_strategy(self, opponents_positions, opponents_prices):

        self.opp_positions[:] = opponents_positions
        self.opp_prices[:] = opponents_prices

        self._get_network_outputs()

        p = utils.softmax(self.network_outputs, temp=self.temp)

        st = np.random.choice(self.options, p=p)

        self.x = self.strategies[st]["position"]
        self.price = self.strategies[st]["price"]

        return self.x, self.price

    def _get_network_outputs(self):

        for i in self.options:
            self._set_network_input(x=self.strategies[i]["position"], price=self.strategies[i]["price"],
                                    set_opponents_part=i == 0)
            self.network_outputs[i] = self.network.propagate_forward(self.network_input)

    def _create_network(self):

        return mlp.MLP(self.network_input.size, self.network_input.size, 1)

    def _get_network_input_size(self):
        return self.parameters.n_firms*self.parameters.n_positions +self.parameters.n_firms*self.parameters.n_prices

    def _set_network_input(self, x, price, set_opponents_part=True):

        n_po = self.parameters.n_positions
        n_pr = self.parameters.n_prices

        b_position = np.zeros(n_po, dtype=int)
        b_price = np.zeros(n_pr, dtype=int)

        b_position[x] = 1
        b_price[price-1] = 1   # min price is 1 (not 0)

        begin = 0
        end = begin + n_po
        self.network_input[begin:end] = b_position

        begin = end
        end = begin + n_pr
        self.network_input[begin:end] = b_price

        if set_opponents_part:
            for opp_pos, opp_price in zip(self.opp_positions, self.opp_prices):

                b_position[:] = 0
                b_price[:] = 0
                b_position[opp_pos] = 1
                b_price[opp_price-1] = 1  # min price is 1 (not 0)

                begin = end
                end = begin + n_po
                self.network_input[begin:end] = b_position

                begin = end
                end = begin + n_pr
                self.network_input[begin:end] = b_price
