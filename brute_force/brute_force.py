import numpy as np
from parameters import Parameters
import itertools


class BruteForce:

    def __init__(self):

        self.r = 0.5
        self.parameters = Parameters(n_positions=20, n_prices=10, t_max=10)

        self.strategies = np.array(
            list(itertools.product(range(self.parameters.n_positions), range(self.parameters.n_prices))),
            dtype=int
        )
        
        self.horizon = 2
        
        self.idx_strategies = np.arange(len(self.strategies))

        # Useful n
        self.n_strategies = len(self.strategies)
        self.n_path = self.n_strategies**self.horizon

        # Prepare useful arrays
        self.n_customers = self.compute_n_customers()
        self.firm_a_reply = self.compute_firm_a_replies()
        self.tree = self.get_tree()
        self.profits = self.compute_profits()

        self.anticipated_moves = np.zeros((self.n_path, self.horizon, 2), dtype=int)
        self.anticipated_profits = np.zeros((self.n_path, 2), dtype=int)

    def compute_n_customers(self):

        print("Compute n customers...",  end=" ", flush=True)

        z = np.zeros((self.parameters.n_positions, self.parameters.n_positions, 3), dtype=int)
        # Last parameter is idx0: n customers seeing only A,
        #                   idx1: n customers seeing only B,
        #                   idx2: customers seeing A and B,

        field_of_view = np.zeros((self.parameters.n_positions, 2))  # 2: min, max
        field_of_view[:] = [self.field_of_view(x) for x in range(self.parameters.n_positions)]

        for i, j in itertools.product(range(self.parameters.n_positions), repeat=2):

            for x in range(self.parameters.n_positions):

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

    def compute_firm_a_replies(self):

        print("Compute replies for firm A...", end=" ", flush=True)

        z = np.zeros(self.n_strategies, dtype=int)  # 2: position, price

        for i in range(self.n_strategies):
            z[i] = self.optimal_move(i)

        print("Done!")

        return z

    def field_of_view(self, x):

        r = int(self.r * self.parameters.n_positions)

        field_of_view = [
            max(x - r, 0),
            min(x + r, self.parameters.n_positions - 1)]

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

            exp_profits[i] = (price+1) * n_customers  # Price is in fact price index

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

            z[i, j, :] = n_customers * (prices + 1)  # Prices are idx of prices

        print("Done!")

        return z

    def get_tree(self):
        print("Building the tree...", end=" ", flush=True)
        z = np.array(list(itertools.product(range(self.n_strategies), repeat=self.horizon)), dtype=int)
        print("Done!")
        return z

    def firm_b_reply(self, a_move, b_precedent_move):

        self.anticipated_moves[:, 0, 0] = a_move

        print("Filling 'moves' array...", end=" ", flush=True)

        for t in range(self.horizon):

            for i in range(self.n_path):
                for s in self.tree[i]:
                    self.anticipated_moves[i, t, 1] = s

                    if (t + 1) < self.horizon:
                        self.anticipated_moves[i, t + 1, 0] = self.firm_a_reply[s]

        print("Done!")
        print("Filling 'profits' array...", end=" ", flush=True)

        for i in range(self.n_path):

            for t in range(self.horizon):

                if t == 0:
                    profits_firm_a_active = self.profits[
                        self.anticipated_moves[i, t, 0],
                        b_precedent_move
                    ]

                else:
                    profits_firm_a_active = self.profits[
                        self.anticipated_moves[i, t, 0],
                        self.anticipated_moves[i, t-1, 1]
                    ]

                profits_firm_b_active = self.profits[
                    self.anticipated_moves[i, t, 0],
                    self.anticipated_moves[i, t, 1]
                ]

                profits = profits_firm_a_active + profits_firm_b_active

                self.anticipated_profits[i, :] += profits

        print("Done!\n")
        # print("Results:\n")

        max_profits = max(self.anticipated_profits[:, 1])

        idx = np.flatnonzero(self.anticipated_profits[:, 1] == max_profits)

        best_i = np.random.choice(idx)

        # print("\nBest 'anticipated path' for B player give following payoffs:")
        # print("A player (Horizon 0): {}\nB player (Optimal): {}".format(
        #     self.anticipated_profits[best_i, 0], self.anticipated_profits[best_i, 1]))

        return self.anticipated_moves[best_i, 0, 1]

    def run(self):

        print("*" * 10 + "\n")
        print("'A' against 'B'")
        cumulative_profits = np.zeros(2, dtype=int)

        b_initial_move = np.random.randint(self.n_strategies)
        b_move = b_initial_move

        for t in range(self.parameters.t_max):

            print("Turn: {}\n".format(t))

            a_move = self.firm_a_reply[b_move]  # idx, t0, player
            profits_firm_a_active = self.profits[a_move, b_move]

            print("Firm A active")
            print("A: position = {}; price = {}; profits={}".format(
                self.strategies[a_move, 0], self.strategies[a_move, 1], profits_firm_a_active[0])
            )
            print("B: position = {}; price = {}; profits={}".format(
                self.strategies[b_move, 0], self.strategies[b_move, 1], profits_firm_a_active[1])
            )
            print("Repartition clients: {}"
                  .format(self.n_customers[self.strategies[a_move, 0], self.strategies[b_move, 0]]))
            print()

            b_move = self.firm_b_reply(a_move, b_precedent_move=b_move)
            profits_firm_b_active = self.profits[a_move, b_move]

            print("Firm B active")
            print("A: position = {}; price = {}; profits={}".format(
                self.strategies[a_move, 0], self.strategies[a_move, 1], profits_firm_b_active[0])
            )
            print("B: position = {}; price = {}; profits={}".format(
                self.strategies[b_move, 0], self.strategies[b_move, 1], profits_firm_b_active[1])
            )
            print("Repartition clients: {}".format(self.n_customers[self.strategies[a_move, 0], self.strategies[b_move, 0]]))
            print()

            pr = profits_firm_a_active + profits_firm_b_active
            cumulative_profits[:] = cumulative_profits[:] + pr

            print("Total profits for t: {} %% cumulative {} %%\n"
                  .format(pr, cumulative_profits))

            print("*" * 10 + "\n")

        print("*" * 10 + "\n")
        print("*" * 10 + "\n")
        print("*" * 10 + "\n")

        print("'A' against 'A'")
        b_move = b_initial_move
        print(b_move)
        cumulative_profits[:] = 0

        for t in range(self.parameters.t_max):

            print("Turn: {}".format(t))

            a_move = self.firm_a_reply[b_move]  # idx, t0, player
            profits_firm_a_active = self.profits[a_move, b_move]

            print("Firm A active")
            print("A: position = {}; price = {}; profits={}".format(
                self.strategies[a_move, 0], self.strategies[a_move, 1] + 1, profits_firm_a_active[0])
            )
            print("B: position = {}; price = {}; profits={}".format(
                self.strategies[b_move, 0], self.strategies[b_move, 1] + 1, profits_firm_a_active[1])
            )
            print("Clients: {}".format(self.n_customers[self.strategies[a_move, 0], self.strategies[b_move, 0]]))
            print()

            b_move = self.firm_a_reply[a_move]
            profits_firm_b_active = self.profits[a_move, b_move]

            print("Firm B active")
            print("A: position = {}; price = {}; profits={}".format(
                self.strategies[a_move, 0], self.strategies[a_move, 1] + 1, profits_firm_b_active[0])
            )
            print("B: position = {}; price = {}; profits={}".format(
                self.strategies[b_move, 0], self.strategies[b_move, 1] + 1, profits_firm_b_active[1])
            )
            print("Repartition clients: {}"
                  .format(self.n_customers[self.strategies[a_move, 0], self.strategies[b_move, 0]]))
            print()

            pr = profits_firm_a_active + profits_firm_b_active
            cumulative_profits[:] = cumulative_profits[:] + pr

            print("Total profits for t: {} %% cumulative {} %%\n"
                  .format(pr, cumulative_profits))

            print("*" * 10 + "\n")


def main():
    b = BruteForce()
    b.run()


if __name__ == "__main__":
    main()


