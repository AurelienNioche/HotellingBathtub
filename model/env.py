import numpy as np
import itertools as it

import parameters
from model import customer, firm


class Environment(object):
    """Hotelling, 1929"""

    def __init__(self, field_of_view, init_firm_positions, init_firm_prices):

        self.firms = []
        self.customers = []

        self.active_player = 0

        self.z = None  # Will be used in case of bot customers

        # Set the environment
        self.set_up(field_of_view, init_firm_positions, init_firm_prices)

    def set_up(self, parameter_field_of_view, init_firm_positions, init_firm_prices):

        self._spawn_firms(init_firm_positions, init_firm_prices)
        self._spawn_customers(parameter_field_of_view)

        if parameters.n_firms == 2 and parameters.zombies_customers:
            self.compute_z()

    def _spawn_firms(self, init_firm_positions, init_firm_prices):

        for position, price in zip(init_firm_positions, init_firm_prices):

            f = firm.Firm(x=position, price=price)
            self.firms.append(f)

    def _spawn_customers(self, field_of_view):

        for i in range(parameters.n_positions):

            c = customer.Customer(x=i, field_of_view=field_of_view)
            self.customers.append(c)

    def compute_z(self):

        self.z = np.zeros((parameters.n_positions, parameters.n_positions, 3))
        # Last parameter is idx0: n customers seeing only A,
        #                   idx1: n customers seeing only B,
        #                   idx2: customers seeing A and B,

        for i, j in it.product(range(parameters.n_positions), repeat=2):

            for c in self.customers:

                field_of_view = c.get_field_of_view()

                see_firm_0 = field_of_view[0] <= i <= field_of_view[1]
                see_firm_1 = field_of_view[0] <= j <= field_of_view[1]

                if see_firm_0 and see_firm_1:
                    self.z[i, j, 2] += 1

                elif see_firm_0:
                    self.z[i, j, 0] += 1

                elif see_firm_1:
                    self.z[i, j, 1] += 1

    def _reset_profits(self):

        for f in self.firms:
            f.reset_profit_counter()

    def get_profits(self):

        return [f.profit for f in self.firms]

    def get_positions(self):

        return [f.x for f in self.firms]

    def get_prices(self):

        return [f.price for f in self.firms]

    def time_step_first_part(self):

        prices = np.zeros(parameters.n_firms, dtype=int)
        positions = np.zeros(parameters.n_firms, dtype=int)

        prices[:] = self.get_prices()
        positions[:] = self.get_positions()

        n_customers = np.zeros(parameters.n_firms)

        if parameters.n_firms == 2 and parameters.zombies_customers:

            n_customers[:] = self.z[positions[0], positions[1], :2]

            to_share = self.z[positions[0], positions[1], 2]
            if to_share > 0:
                r = np.random.randint(to_share + 1)
                n_customers[0] += r
                n_customers[1] += to_share - r

            for i in range(2):
                self.firms[i].sell_x_units(n_customers[i])

        else:

            firms_idx = np.arange(parameters.n_firms)
            for c in self.customers:
                field_of_view = c.get_field_of_view()

                cond0 = positions >= field_of_view[0]
                cond1 = positions <= field_of_view[1]

                firms_idx_c = firms_idx[cond0 * cond1]

                choice = c.get_firm_choice(
                    firms_idx=firms_idx_c, prices=prices[firms_idx_c])

                if choice != -1:
                    self.firms[choice].sell_x_units(1)

    def time_step_second_part(self):

        positions = np.array([self.firms[i].x for i in range(parameters.n_firms)])
        prices = np.array([self.firms[i].price for i in range(parameters.n_firms)])

        idx = np.arange(parameters.n_firms)

        bool_opponents_active = idx[:] != self.active_player

        self.firms[self.active_player].select_strategy(
            opponents_positions=positions[bool_opponents_active],
            opponents_prices=prices[bool_opponents_active]
        )

        for i in idx[bool_opponents_active]:
            bool_opponents_i = idx[:] != i

            self.firms[i].change_in_opponents_strategies(
                old_opponents_positions=positions[bool_opponents_i],
                old_opponents_prices=prices[bool_opponents_i]
            )

        self._reset_profits()

        self.active_player = (self.active_player + 1) % parameters.n_firms
