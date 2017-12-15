import numpy as np
import itertools as it
# import parameters

from model import customer, firm


class Environment(object):
    """Hotelling, 1929"""

    def __init__(self, field_of_view, init_firm_positions, init_firm_prices, parameters):

        self.parameters = parameters

        self.two_players = parameters.n_firms == 2

        self.idx = np.arange(parameters.n_firms)

        self.firms = []
        self.customers = []

        self.positions = np.zeros(parameters.n_firms, dtype=int)
        self.prices = np.zeros(parameters.n_firms, dtype=int)
        self.profits = np.zeros(parameters.n_firms)

        self.active_player = 0

        self.z = None  # Will be used in case of bot customers

        # Set the environment
        self.set_up(field_of_view, init_firm_positions, init_firm_prices)

    def set_up(self, parameter_field_of_view, init_firm_positions, init_firm_prices):

        self.positions[:] = init_firm_positions
        self.prices[:] = init_firm_prices

        self._spawn_firms()
        self._spawn_customers(parameter_field_of_view)

        if self.two_players and self.parameters.zombies_customers:
            self.compute_z()

    def _spawn_firms(self):

        for i, position, price in zip(self.idx, self.positions, self.prices):

            opponents = self.idx != i

            f = getattr(firm, self.parameters.firm_class[i])(
                x=position, price=price,
                init_opp_positions=self.positions[opponents], init_opp_prices=self.prices[opponents],
                z=self.z,
                parameters=self.parameters
            )
            self.firms.append(f)

    def _spawn_customers(self, field_of_view):

        for i in range(self.parameters.n_positions):

            c = customer.Customer(x=i, field_of_view=field_of_view, parameters=self.parameters)
            self.customers.append(c)

    def compute_z(self):

        assert len(self.customers), "Customers have to be spawn before computing z."

        self.z = np.zeros((self.parameters.n_positions, self.parameters.n_positions, 3), dtype=int)
        # Last parameter is idx0: n customers seeing only A,
        #                   idx1: n customers seeing only B,
        #                   idx2: customers seeing A and B,

        for i, j in it.product(range(self.parameters.n_positions), repeat=2):

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

    def time_step_first_part(self):

        # Make active firm play

        opponents_passive = self.idx != self.active_player

        self.positions[self.active_player], self.prices[self.active_player] = \
            self.firms[self.active_player].select_strategy(
                opponents_positions=self.positions[opponents_passive],
                opponents_prices=self.prices[opponents_passive]
            )

    def time_step_second_part(self):

        # Compute profits
        self.profits[:] = 0

        n_customers = np.zeros(self.parameters.n_firms, dtype=int)

        if self.two_players and self.parameters.zombies_customers:

            n_customers[:] = self.z[self.positions[0], self.positions[1], :2]

            to_share = self.z[self.positions[0], self.positions[1], 2]

            if to_share > 0:

                if self.prices[0] == self.prices[1]:
                    r = np.random.randint(to_share + 1)
                    n_customers[:] += r, to_share - r

                else:
                    n_customers[int(self.prices[1] < self.prices[0])] += to_share

            self.profits += n_customers * self.prices * self.parameters.unit_value

        else:

            firms_idx = np.arange(self.parameters.n_firms)

            for c in self.customers:
                field_of_view = c.get_field_of_view()

                cond0 = self.positions >= field_of_view[0]
                cond1 = self.positions <= field_of_view[1]

                firms_idx_c = firms_idx[cond0 * cond1]

                choice = c.get_firm_choice(
                    firms_idx=firms_idx_c, prices=self.prices[firms_idx_c])

                if choice != -1:
                    self.profits[choice] += self.prices[choice] * self.parameters.unit_value

        # Make firms learn
        for i in self.idx:

            self.firms[i].learn(self.profits[i])

        # Change active player
        self.active_player = (self.active_player + 1) % self.parameters.n_firms
