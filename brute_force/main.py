import numpy as np
import multiprocessing as mlt
import tqdm

import pickle
import os

import brute_force.bf_model as model


def get_pool_parameters(shared_parameters):

    seeds = np.random.randint(2 ** 32, size=shared_parameters.n_simulations)
    rs = np.random.random(size=shared_parameters.n_simulations)
    init_move_firms = np.random.randint(
        shared_parameters.n_prices*shared_parameters.n_positions,
        size=shared_parameters.n_simulations)

    parameters = [
        model.Parameters(
            n_positions=shared_parameters.n_positions,
            n_prices=shared_parameters.n_prices,
            t_max=shared_parameters.t_max,
            horizon=shared_parameters.horizon,
            mode=shared_parameters.mode,
            unit_value=shared_parameters.unit_value,
            r=rs[i],
            init_move_firm=init_move_firms[i],
            seed=seeds[i]
        )
        for i in range(shared_parameters.n_simulations)
    ]

    return parameters


def run(parameters):

    m = model.Model(parameters)
    positions, prices, profits = m.run()
    bkp = model.RunBackup(parameters=parameters, positions=positions, prices=prices, profits=profits)
    return bkp


def run_profits_comparison(parameters):

    m = model.Model(parameters)
    diff = m.run()
    return parameters.r, diff


def main_profits_comparison():

    # from multiprocessing.pool import ThreadPool
    pool = mlt.Pool()

    shared_parameters = model.SharedParameters(
        mode=model.Mode.compare_profits,
        n_simulations=200,
        t_max=200,
        horizon=1,
        n_positions=10,
        n_prices=5
    )
    pool_parameters = get_pool_parameters(shared_parameters)

    results = np.zeros((shared_parameters.n_simulations, 2))

    for i, r in enumerate(tqdm.tqdm(
            pool.imap_unordered(run_profits_comparison, pool_parameters),
            total=len(pool_parameters))):
        results[i] = r

    save(results)


def save(results, path=os.path.expanduser("~/Desktop/results.p")):

    with open(path, "wb") as f:
        pickle.dump(results, f)


def distance_over_fov(file_name, pool_backup, fig_folder=None):
    from pylab import plt
    span_ratio = 0.33

    if fig_folder is None:
        fig_folder = "data/figures"

    os.makedirs(fig_folder, exist_ok=True)

    parameters = pool_backup.parameters
    backups = pool_backup.backups

    n_simulations = parameters.n_simulations

    n_positions = parameters.n_positions
    n_prices = parameters.n_prices
    unit_value = parameters.unit_value

    # Compute profit max
    profit_max = n_positions * n_prices * unit_value

    # Containers
    x = np.zeros(n_simulations)
    y = np.zeros(n_simulations)
    y_err = np.zeros(n_simulations)
    z = np.zeros(n_simulations)

    # How many time steps from the end of the simulation are included in analysis
    span = int(span_ratio * parameters.t_max)

    for i, b in enumerate(backups):

        try:
            # Save the parameter that affected the customers field of view
            x[i] = b.field_of_view / 2
        except AttributeError:
            x[i] = b.parameters.r

        # Compute the mean distance between the two firms
        data = np.absolute(
            b.positions[-span:, 0] -
            b.positions[-span:, 1]) / n_positions

        spacing = np.mean(data)
        spacing_std = np.std(data)

        y[i] = spacing
        y_err[i] = spacing_std

        # Get mean profits
        z[i] = np.mean(b.profits[-span:, :]) / profit_max

    # Plot this
    fig = plt.figure(figsize=(10, 6))
    ax = plt.subplot()

    ax.set_xlim(-0.01, 1.01)
    if max(y) < 0.5:
        ax.set_ylim(-0.01, 0.51)

    ax.set_xticks(np.arange(0, 1.1, 0.25))
    ax.set_yticks(np.arange(0, 0.51, 0.1))

    ax.set_xlabel("$r$")
    ax.set_ylabel("Mean distance")

    ax.set_title("Mean distance between firms over $r$")

    # add comment with file name
    plt.text(0.005, 0.005, file_name, transform=fig.transFigure, fontsize='x-small', color='0.5')

    # show random
    plt.text(0.005, 0.005, file_name, transform=fig.transFigure, fontsize='x-small', color='0.5')

    abc = ax.scatter(x, y, c=z, zorder=10, alpha=0.25)
    fig.colorbar(abc, label="Profits")

    plt.tight_layout()

    if file_name:
        plt.savefig("{}/{}.pdf".format(fig_folder, file_name))

    plt.show()


def main():

    pool = mlt.Pool()

    backups = []

    shared_parameters = model.SharedParameters(
        mode=model.Mode.h1_against_h1,
        n_simulations=200,
        t_max=250,
        horizon=1,
        n_positions=10,
        n_prices=5
    )

    pool_parameters = get_pool_parameters(shared_parameters)

    for bkp in tqdm.tqdm(
            pool.imap_unordered(run, pool_parameters),
            total=len(pool_parameters)):
        backups.append(bkp)

    pool_backup = model.PoolBackup(parameters=shared_parameters, backups=backups)

    file_name = pool_backup.save()

    print("Data have been saved using file name: '{}'.".format(file_name))

    distance_over_fov(file_name=file_name, pool_backup=pool_backup, fig_folder=os.path.expanduser("~\Desktop"))


if __name__ == "__main__":
    main_profits_comparison()
