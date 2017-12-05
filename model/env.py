import numpy as np

import parameters
from model import customer, firm


class Environment(object):
    """Hotelling, 1929"""

    def __init__(self, parameter_field_of_view, init_firm_positions, init_firm_prices):

        self.firms = []
        self.customers = []

        self.active_player = 0

        # Set the environment
        self.set_up(parameter_field_of_view, init_firm_positions, init_firm_prices)

    def set_up(self, parameter_field_of_view, init_firm_positions, init_firm_prices):

        self._spawn_firms(init_firm_positions, init_firm_prices)
        self._spawn_customers(parameter_field_of_view)

    def _spawn_firms(self, init_firm_positions, init_firm_prices):

        for position, price in zip(init_firm_positions, init_firm_prices):

            f = firm.Firm(x=position, price=price)
            self.firms.append(f)

    def _spawn_customers(self, parameter_field_of_view):

        for i in range(parameters.n_positions):

            c = customer.Customer(x=i, parameter_field_of_view=parameter_field_of_view)
            self.customers.append(c)

    def _reset_profits(self):

        for f in self.firms:
            f.reset_profit_counter()

    def get_profits(self):

        return [f.profit for f in self.firms]

    def get_positions(self):

        return [f.x for f in self.firms]

    def get_prices(self):

        return [f.price for f in self.firms]

    # def get_customer_firm_choices(self):
    #
    #     return [c.firm_choice for c in self.customers]
    #
    # def get_customer_extra_view_choices(self):
    #
    #     return [c.extra_view for c in self.customers]
    #
    # def get_customer_utility(self):
    #
    #     return [c.utility for c in self.customers]

    def time_step_first_part(self):

        prices = np.zeros(parameters.n_firms, dtype=int)
        positions = np.zeros(parameters.n_firms, dtype=int)

        prices[:] = self.get_prices()
        positions[:] = self.get_positions()

        firms_idx = np.arange(parameters.n_firms)

        for c in self.customers:
            field_of_view = c.get_field_of_view()

            cond0 = positions >= field_of_view[0]
            cond1 = positions <= field_of_view[1]

            firms_idx_c = firms_idx[cond0 * cond1]

            choice = c.get_firm_choice(
                firms_idx=firms_idx_c, prices=prices[firms_idx_c])

            if choice != -1:
                self.firms[choice].sell_one_unit()

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
