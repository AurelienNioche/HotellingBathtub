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
        n_positions=40,
        n_prices=10
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


def main():

    pool = mlt.Pool()

    backups = []

    shared_parameters = model.SharedParameters(
        mode=model.Mode.h0_against_h0,
        n_simulations=50,
        t_max=100,
        horizon=1,
        n_positions=100,
        n_prices=50
    )

    pool_parameters = get_pool_parameters(shared_parameters)

    for bkp in tqdm.tqdm(
            pool.imap_unordered(run, pool_parameters),
            total=len(pool_parameters)):
        backups.append(bkp)

    pool_backup = model.PoolBackup(parameters=shared_parameters, backups=backups)

    file_name = pool_backup.save()

    print("Data have been saved using file name: '{}'.".format(file_name))


if __name__ == "__main__":
    main()
