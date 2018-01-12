import numpy as np
from parameters import Parameters
import itertools
from tqdm import tqdm


class BruteForce:

    def __init__(self):

        self.r = 0.25
        self.parameters = Parameters(n_positions=100, n_prices=10, t_max=2)

        self.strategies = np.array(
            list(itertools.product(range(self.parameters.n_positions), range(self.parameters.n_prices))),
            dtype=int
        )
        
        self.idx_strategies = np.arange(len(self.strategies))

        self.n_strategies = len(self.strategies)

        self.n_customers = self.compute_n_customers()
        self.strategies_A = self.compute_strategies_A()
        self.tree = self.get_tree()
        self.profits = self.compute_profits()

    def compute_n_customers(self):

        print("Compute n customers...",  end=" ", flush=True)

        z = np.zeros((self.parameters.n_positions, self.parameters.n_positions, 3), dtype=int)
        # Last parameter is idx0: n customers seeing only A,
        #                   idx1: n customers seeing only B,
        #                   idx2: customers seeing A and B,

        field_of_views = [self.field_of_view(x) for x in range(self.parameters.n_positions)]

        for i, j in itertools.product(range(self.parameters.n_positions), repeat=2):

            for x in range(self.parameters.n_positions):

                field_of_view = field_of_views[x]

                see_firm_0 = field_of_view[0] <= i <= field_of_view[1]
                see_firm_1 = field_of_view[0] <= j <= field_of_view[1]

                if see_firm_0 and see_firm_1:
                    z[i, j, 2] += 1

                elif see_firm_0:
                    z[i, j, 0] += 1

                elif see_firm_1:
                    z[i, j, 1] += 1

        print("Done!")

        return z

    def compute_strategies_A(self):

        print("Compute strategies for A...", end=" ", flush=True)

        z = np.zeros(self.n_strategies, dtype=int)  # 2: position, price

        for i in tqdm(range(self.n_strategies)):
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

            positions = self.strategies[i, 0], self.strategies[j, 0]
            prices = self.strategies[i, 1], self.strategies[j, 1]

            n_customers[:] = self.n_customers[positions[0], positions[1], :2]

            to_share = self.n_customers[positions[0], positions[1], 2]

            if to_share > 0:

                if prices[0] == prices[1]:
                    r = np.random.randint(to_share + 1)
                    n_customers[:] += r, to_share - r

                else:
                    n_customers[int(prices[1] < prices[0])] += to_share

            z[i, j, :] = n_customers * prices

        print("Done!")

        return z

    def get_tree(self):
        print("Building the tree...", end=" ", flush=True)
        z = np.array(list(itertools.product(range(self.n_strategies), repeat=self.parameters.t_max)), dtype=int)
        print("Done!")
        return z

    def run(self):

        init_strategy_B = np.random.randint(self.n_strategies)

        moves = np.zeros((self.n_strategies ** self.parameters.t_max, self.parameters.t_max, 2),
                         dtype=int)

        moves[:, 0, 0] = self.optimal_move(init_strategy_B)  # :, player A, t0

        print("Filling 'moves' array...", end=" ")

        n = self.n_strategies**self.parameters.t_max

        for t in tqdm(range(self.parameters.t_max)):

            for i in range(n):
                for s in self.tree[i]:
                    moves[i, t, 1] = s

                    if (t+1) < self.parameters.t_max:
                        moves[i, t+1, 0] = self.strategies_A[s]

        print("Done!")
        print("Filling 'profits' array...", end=" ")

        cum_profits = np.zeros((self.n_strategies**self.parameters.t_max, 2), dtype=int)

        for i in range(self.n_strategies**self.parameters.t_max):

            for t in range(self.parameters.t_max):

                profits = self.profits[
                    moves[i, t, 0],
                    moves[i, t, 1]
                ]
                cum_profits[i, :] += profits[:]

        print("Done!\n")
        print("*" * 10 + "\n")
        print("Results:\n")

        print("Cumulative profits are:")
        print(cum_profits)

        best_i = np.argmax(cum_profits[:, 1])

        print("\nBest 'path' for B player give following payoffs:")
        print("A player (Horizon 0): {}\nB player (Optimal): {}".format(cum_profits[best_i, 0], cum_profits[best_i, 1]))


def main():
    b = BruteForce()
    b.run()


if __name__ == "__main__":
    main()


