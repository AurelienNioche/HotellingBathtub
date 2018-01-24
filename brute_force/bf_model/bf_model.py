import numpy as np
import itertools
import math

import backup


class Mode:

    compare_profits = 0
    h0_against_h0 = 1
    h0_against_h1 = 2
    h1_against_h1 = 3


class Parameters:

    def __init__(
            self, n_positions=2, n_prices=1,
            t_max=1, r=0.5, horizon=2, unit_value=1, seed=0, name="",
            init_move_firm=0, mode=Mode.h0_against_h1
    ):
        self.init_move_firm = init_move_firm
        self.n_positions = n_positions
        self.n_prices = n_prices
        self.t_max = t_max
        self.unit_value = unit_value
        self.r = r
        self.horizon = horizon
        self.seed = seed
        self.name = name
        self.mode = mode

    def dict(self):
        return {i: j for i, j in self.__dict__.items() if not i.startswith("__")}


class SharedParameters:

    def __init__(self, n_simulations=300, n_positions=20, n_prices=10, horizon=2, t_max=100, unit_value=1,
                 mode=Mode.h0_against_h1):

        self.n_simulations = n_simulations

        self.n_positions = n_positions
        self.n_prices = n_prices

        self.horizon = horizon
        self.t_max = t_max

        self.unit_value = unit_value

        self.mode = mode

    def dict(self):
        return {i: j for i, j in self.__dict__.items() if not i.startswith("__")}


class RunBackup(backup.Backup):

    def __init__(self, parameters, positions, prices, profits):
        super().__init__(parameters)

        self.positions = positions
        self.prices = prices
        self.profits = profits


class PoolBackup(backup.PoolBackup):
    pass


class Model:

    def __init__(self, param):

        np.random.seed(param.seed)

        self.n_positions = param.n_positions
        self.n_prices = param.n_prices
        self.t_max = param.t_max
        self.r = param.r
        self.unit_value = param.unit_value
        self.horizon = param.horizon

        self.mode = param.mode

        self.init_move_firm = param.init_move_firm

        self.strategies = np.array(
            list(itertools.product(range(self.n_positions), range(self.n_prices))),
            dtype=int
        )

        # Useful n
        self.n_strategies = len(self.strategies)
        self.n_moves_anticipated_for_itself = 1 + self.horizon // 2
        self.n_path = self.n_strategies ** self.n_moves_anticipated_for_itself

        self.idx_strategies = np.arange(self.n_strategies)

        # Prepare useful arrays
        self.n_customers = self.compute_n_customers()
        self.profits = self.compute_profits()
        self.horizon_0_reply = self.compute_horizon_0_replies()

        self.tree = self.get_tree()

        y_size = 1 + int(math.ceil(self.horizon / 2))
        self.anticipated_moves = np.ones((self.n_path, y_size, 2), dtype=int) * -1
        self.anticipated_profits = np.ones(self.n_path, dtype=int) * -1

    def compute_n_customers(self):

        z = np.zeros((self.n_positions, self.n_positions, 3), dtype=int)
        # Last parameter is idx0: n customers seeing only A,
        #                   idx1: n customers seeing only B,
        #                   idx2: customers seeing A and B,

        field_of_view = np.zeros((self.n_positions, 2))  # 2: min, max
        field_of_view[:] = [self.field_of_view(x) for x in range(self.n_positions)]

        for i, j in itertools.product(range(self.n_positions), repeat=2):

            for x in range(self.n_positions):

                see_firm_0 = field_of_view[x, 0] <= i <= field_of_view[x, 1]
                see_firm_1 = field_of_view[x, 0] <= j <= field_of_view[x, 1]

                if see_firm_0 and see_firm_1:
                    z[i, j, 2] += 1

                elif see_firm_0:
                    z[i, j, 0] += 1

                elif see_firm_1:
                    z[i, j, 1] += 1

        return z

    def field_of_view(self, x):

        r = int(self.r * self.n_positions)

        field_of_view = [
            max(x - r, 0),
            min(x + r, self.n_positions - 1)
        ]

        return field_of_view

    def compute_profits(self):

        z = np.zeros((self.n_strategies, self.n_strategies, 2), dtype=int)

        n_customers = np.zeros(2, dtype=int)

        for i, j in itertools.product(range(self.n_strategies), repeat=2):

            positions = np.array([self.strategies[i, 0], self.strategies[j, 0]])
            prices = np.array([self.strategies[i, 1], self.strategies[j, 1]])

            n_customers[:] = self.n_customers[positions[0], positions[1], :2]

            to_share = self.n_customers[positions[0], positions[1], 2]

            if to_share > 0:

                if prices[0] == prices[1]:
                    n_customers[:] += to_share

                else:
                    n_customers[int(prices[1] < prices[0])] += to_share * 2

            z[i, j, :] = n_customers * (prices + 1) * self.unit_value  # Prices are idx of prices

        return z

    def optimal_move(self, opp_strategy):

        exp_profits = np.zeros(self.n_strategies)

        exp_profits[:] = self.profits[:, opp_strategy, 0]

        max_profits = max(exp_profits)

        idx = np.flatnonzero(exp_profits == max_profits)

        i = np.random.choice(idx)

        return i

    def compute_horizon_0_replies(self):

        z = np.zeros(self.n_strategies, dtype=int)  # 2: position, price

        for i in range(self.n_strategies):
            z[i] = self.optimal_move(i)

        return z

    def get_tree(self):

        z = np.array(list(
            itertools.product(range(self.n_strategies), repeat=self.n_moves_anticipated_for_itself)), dtype=int)

        return z

    def compute_anticipated_moves(self, opponent_move):

        self.anticipated_moves[:, 0, 0] = opponent_move

        for t in range(self.n_moves_anticipated_for_itself):
            self.anticipated_moves[:, t, 1] = self.tree[:, t]
            try:
                self.anticipated_moves[:, t + 1, 0] = self.horizon_0_reply[self.tree[:, t]]
            except IndexError:
                pass

    def compute_anticipated_profits(self):

        self.anticipated_profits[:] = 0

        for i in range(self.n_path):

            n_moves, t = 0, 0

            while True:

                # Role is active
                self.anticipated_profits[i] += self.profits[
                    self.anticipated_moves[i, t, 0],
                    self.anticipated_moves[i, t, 1],
                    1
                ]

                n_moves += 1

                if n_moves > self.horizon:
                    break

                # Role is passive
                self.anticipated_profits[i] += self.profits[
                    self.anticipated_moves[i, t + 1, 0],  #
                    self.anticipated_moves[i, t, 1],
                    1
                ]

                n_moves += 1
                t += 1

                if n_moves > self.horizon:
                    break

    def horizon_x_reply(self, opponent_move):

        self.compute_anticipated_moves(opponent_move)
        self.compute_anticipated_profits()

        max_profits = max(self.anticipated_profits)

        # noinspection PyTypeChecker
        idx = np.flatnonzero(self.anticipated_profits[:] == max_profits)

        best_i = np.random.choice(idx)

        return self.anticipated_moves[best_i, 0, 1]  # t=0, player=1

    def run(self):

        if self.mode == Mode.h0_against_h1:
            return self.play(a_uses_horizon=False, b_uses_horizon=True)

        elif self.mode == Mode.h0_against_h0:
            return self.play(a_uses_horizon=False, b_uses_horizon=False)

        elif self.mode == Mode.h1_against_h1:
            return self.play(a_uses_horizon=True, b_uses_horizon=True)

        else:

            return self.play(b_uses_horizon=True) - self.play(b_uses_horizon=False)

    def play(self, a_uses_horizon=False, b_uses_horizon=True):

        if self.mode != Mode.compare_profits:

            # For recording
            positions = np.zeros((self.t_max, 2))
            prices = np.zeros((self.t_max, 2))
            profits = np.zeros((self.t_max, 2))

        else:
            positions, prices, profits = None, None, None

        a_active = True

        if a_active:
            a_move = np.nan
            b_move = self.init_move_firm

        else:
            a_move = self.init_move_firm
            b_move = np.nan

        prf = 0

        for t in range(self.t_max):

            # A is active
            if a_active:
                if a_uses_horizon:
                    a_move = self.horizon_x_reply(b_move)
                else:
                    a_move = self.horizon_0_reply[b_move]

            else:
                if b_uses_horizon:
                    b_move = self.horizon_x_reply(a_move)
                else:
                    b_move = self.horizon_0_reply[a_move]

            prf += self.profits[a_move, b_move, 1]

            if self.mode != Mode.compare_profits:

                profits[t, :] = self.profits[a_move, b_move]
                positions[t, :] = self.strategies[a_move, 0], self.strategies[b_move, 0]
                prices[t, :] = self.strategies[a_move, 1], self.strategies[b_move, 1]

            a_active = not a_active

        if self.mode != Mode.compare_profits:
            return positions, prices, profits / 2
            # Divide by 2 because of the trick for repartition of clients in case of equal price

        else:
            return prf


def main():

    param = Parameters(n_positions=40, n_prices=10, t_max=100, r=0.5, horizon=1, init_move_firm=51,
                       mode=Mode.h0_against_h0)

    m = Model(param)
    positions, prices, profits = m.run()
    print("Done!")


if __name__ == "__main__":
    main()
