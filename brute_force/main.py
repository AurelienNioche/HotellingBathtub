import numpy as np
import multiprocessing as mlt
import tqdm

import brute_force.bf_model as model


def get_shared_parameters():

    return model.SharedParameters(
        mode="run_horizon_0_against_horizon_0",
        n_simulations=200,
        t_max=250,
        horizon=0,
        n_positions=100,
        n_prices=50
    )


def get_pool_parameters(shared_parameters):

    seeds = np.random.randint(2 ** 32, size=shared_parameters.n_simulations)
    rs = np.random.random(size=shared_parameters.n_simulations)
    init_b_strategies = np.random.randint(shared_parameters.n_prices*shared_parameters.n_positions,
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
            init_move_firm_b=init_b_strategies[i],
            seed=seeds[i]
        )
        for i in range(shared_parameters.n_simulations)
    ]

    return parameters


def run(parameters):

    m = model.Model(parameters)
    attr = getattr(m, parameters.mode)
    positions, prices, profits = attr()
    bkp = model.RunBackup(parameters=parameters, positions=positions, prices=prices, profits=profits)
    return bkp


def main():

    pool = mlt.Pool()

    backups = []

    shared_parameters = get_shared_parameters()
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
