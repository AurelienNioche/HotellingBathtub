import numpy as np
import itertools
import math


class Parameters:

    def __init__(
            self, n_positions=2, n_prices=1,
            t_max=1, r=0.5, horizon=2, unit_value=1, seed=0, name="", init_move_firm_b=0):

        self.init_move_firm_b = init_move_firm_b
        self.n_positions = n_positions
        self.n_prices = n_prices
        self.t_max = t_max
        self.unit_value = unit_value
        self.r = r
        self.horizon = horizon
        self.seed = seed
        self.name = name

    def dict(self):
        return {i: j for i, j in self.__dict__.items() if not i.startswith("__")}


class BruteForce:

    def __init__(self, param):

        np.random.seed(param.seed)
        
        self.n_positions = param.n_positions
        self.n_prices = param.n_prices
        self.t_max = param.t_max
        self.r = param.r
        self.unit_value = param.unit_value
        self.horizon = param.horizon

        self.init_move_firm_b = param.init_move_firm_b
        
        self.strategies = np.array(
            list(itertools.product(range(self.n_positions), range(self.n_prices))),
            dtype=int
        )

        # Useful n
        self.n_strategies = len(self.strategies)
        self.n_moves_anticipated_for_itself = 1 + self.horizon // 2
        self.n_path = self.n_strategies**self.n_moves_anticipated_for_itself

        self.idx_strategies = np.arange(self.n_strategies)

        # Prepare useful arrays
        self.n_customers = self.compute_n_customers()
        self.horizon_0_reply = self.compute_horizon_0_replies()
        self.tree = self.get_tree()
        self.profits = self.compute_profits()

        y_size = 1 + int(math.ceil(self.horizon / 2))
        self.anticipated_moves = np.zeros((self.n_path, y_size, 2), dtype=int)
        self.anticipated_profits = np.zeros(self.n_path, dtype=int)

    def compute_n_customers(self):

        print("Compute n customers...",  end=" ", flush=True)

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

        print("Done!")

        return z

    def compute_horizon_0_replies(self):

        print("Compute replies for firm with a horizon...", end=" ", flush=True)

        z = np.zeros(self.n_strategies, dtype=int)  # 2: position, price

        for i in range(self.n_strategies):
            z[i] = self.optimal_move(i)

        print("Done!")

        return z

    def field_of_view(self, x):

        r = int(self.r * self.n_positions)

        field_of_view = [
            max(x - r, 0),
            min(x + r, self.n_positions - 1)
        ]

        return field_of_view

    def optimal_move(self, idx_strategy):

        opp_pos, opp_price = self.strategies[idx_strategy]
        
        exp_profits = np.zeros(self.n_strategies)

        for i, (pos, price) in enumerate(self.strategies):

            n_customers = self.n_customers[pos, opp_pos, 0]

            to_share = self.n_customers[pos, opp_pos, 2]

            if price < opp_price:
                n_customers += to_share

            elif price == opp_price:
                n_customers += round(to_share / 2)

            exp_profits[i] = (price+1) * self.unit_value * n_customers  # Price is in fact price index

        max_profits = max(exp_profits)

        idx = np.flatnonzero(exp_profits == max_profits)

        i = np.random.choice(idx)

        return i

    def compute_profits(self):

        print("Computing profits...", end=" ", flush=True)

        z = np.zeros((self.n_strategies, self.n_strategies, 2), dtype=int)

        n_customers = np.zeros(2, dtype=int)

        for i, j in itertools.product(range(self.n_strategies), repeat=2):

            positions = np.array([self.strategies[i, 0], self.strategies[j, 0]])
            prices = np.array([self.strategies[i, 1], self.strategies[j, 1]])

            n_customers[:] = self.n_customers[positions[0], positions[1], :2]

            to_share = self.n_customers[positions[0], positions[1], 2]

            if to_share > 0:

                if prices[0] == prices[1]:
                    # r = np.random.randint(to_share + 1)
                    # n_customers[:] += r, to_share - r
                    n0 = round(to_share / 2)
                    n = np.array([n0, to_share - n0])
                    np.random.shuffle(n)
                    n_customers[:] = n
                else:
                    n_customers[int(prices[1] < prices[0])] += to_share

            z[i, j, :] = n_customers * (prices + 1) * self.unit_value  # Prices are idx of prices

        print("Done!")

        return z

    def get_tree(self):
        
        print("Building the tree...", end=" ", flush=True)
        z = np.array(list(
            itertools.product(range(self.n_strategies), repeat=self.n_moves_anticipated_for_itself)), dtype=int)
        print("Done!")

        print("Tree:")
        for i in range(z.shape[0]):
            print(z[i])
        return z

    def compute_anticipated_moves(self, opponent_move, verbose=False):

        self.anticipated_moves[:, 0, 0] = opponent_move

        if verbose:
            print("Filling 'moves' array...", end=" ", flush=True)

        for t in range(self.n_moves_anticipated_for_itself):
            self.anticipated_moves[:, t, 1] = self.tree[:, t]
            try:
                self.anticipated_moves[:, t + 1, 0] = self.horizon_0_reply[self.tree[:, t]]
            except IndexError:
                pass

        # self.anticipated_moves[:, -1, 1] = self.tree[:, -1]

        if verbose:
            print("Done!")
            self.print_anticipated_moves()

    def compute_anticipated_profits(self, verbose):

        if verbose:
            print("Filling 'profits' array...", end=" ", flush=True)

        for i in range(self.n_path):

            n_moves, t = 0, 0

            while True:

                # Role is active
                profits = self.profits[
                    self.anticipated_moves[i, t, 0],
                    self.anticipated_moves[i, t, 1]
                ]

                self.anticipated_profits[i] += profits[1]

                n_moves += 1

                if n_moves >= self.horizon:
                    break

                # Role is passive
                profits = self.profits[
                    self.anticipated_moves[i, t + 1, 0],
                    self.anticipated_moves[i, t, 1]
                ]

                self.anticipated_profits[i] += profits[1]

                n_moves += 1
                t += 1

                if n_moves >= self.horizon:
                    break

        if verbose:
            print("Done!\n")
        # print("Results:\n")

    def horizon_x_reply(self, opponent_move, verbose=False):

        self.compute_anticipated_moves(opponent_move, verbose)
        self.compute_anticipated_profits(verbose)

        max_profits = max(self.anticipated_profits)

        # noinspection PyTypeChecker
        idx = np.flatnonzero(self.anticipated_profits[:] == max_profits)

        best_i = np.random.choice(idx)

        # print("\nBest 'anticipated path' for B player give following payoffs:")
        # print("A player (Horizon 0): {}\nB player (Optimal): {}".format(
        #     self.anticipated_profits[best_i, 0], self.anticipated_profits[best_i, 1]))

        return self.anticipated_moves[best_i, 0, 1]

    def print_moves(self, active, a_move, b_move, profits):

        print("Firm {} active".format(active))
        print("A: position = {}; price = {}; profits={}".format(
            self.strategies[a_move, 0], self.strategies[a_move, 1] + 1, profits[0])
        )
        print("B: position = {}; price = {}; profits={}".format(
            self.strategies[b_move, 0], self.strategies[b_move, 1] + 1, profits[1])
        )
        print(
            "Repartition clients: {}".format(self.n_customers[self.strategies[a_move, 0], self.strategies[b_move, 0]]))
        print()

    def print_anticipated_moves(self):

        print("\nAnticipated moves are:")

        for i in range(self.anticipated_moves.shape[0]):
            print("#{}".format(i), end=" ")
            print([(self.anticipated_moves[i, t, 0], self.anticipated_moves[i, t, 1]) for t in
                   range(self.anticipated_moves.shape[1])], end=" ")
            print("## [(opponent, itself) at t, (opponent, itself) at t+1, ...")
        print("\n")

    def run_horizon_0_against_horizon_x(self, verbose=False):

        if verbose:
            print("*" * 10 + "\n")
            print("'Horizon 0' against 'Horizon {}'".format(self.horizon))
            print("*" * 10 + "\n")
            print("N strategies", self.n_strategies)
            print("N path", self.n_path)
            print("N moves anticipated for itself", self.n_moves_anticipated_for_itself)
            print("*" * 10 + "\n")

        # For recording
        positions = np.zeros((self.t_max, 2))
        prices = np.zeros((self.t_max, 2))
        profits = np.zeros((self.t_max, 2))

        b_move = self.init_move_firm_b
        a_active = True

        for t in range(self.t_max):

            # A is active
            if a_active:
                a_move = self.horizon_0_reply[b_move]  # idx, t0, player

            else:
                b_move = self.horizon_x_reply(a_move, verbose)

            profits[t, :] = self.profits[a_move, b_move]
            positions[t, :] = self.strategies[a_move, 0], self.strategies[b_move, 0]
            prices[t, :] = self.strategies[a_move, 1], self.strategies[b_move, 1]

            if verbose:
                self.print_moves(active=["B", "A"][a_active], a_move=a_move, b_move=b_move, profits=profits[t, :])

            a_active = not a_active

        return positions, prices, profits


def main():

    param = Parameters(n_positions=20, n_prices=10, t_max=10, r=0.5, horizon=2, init_move_firm_b=0)

    b = BruteForce(param)
    b.run_horizon_0_against_horizon_x(verbose=True)


if __name__ == "__main__":
    main()


