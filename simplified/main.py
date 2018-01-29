import numpy as np
import multiprocessing as mlt
import tqdm

import os


try:
    import simplified.simplified_model as model
    import simplified.analysis as analysis
    import simplified.backup as backup

except ModuleNotFoundError:
    import simplified_model as model
    import analysis
    import backup


def get_pool_parameters(n_simulations=100, n_prices=100, n_positions=100, t_max=250, p_min=1, p_max=100):

    seeds = np.random.randint(2 ** 32, size=n_simulations)
    rs = np.random.random(size=n_simulations)
    init_move_firms = np.random.randint(n_prices*n_positions, size=n_simulations)

    parameters = [
        model.Parameters(
            n_positions=n_positions,
            n_prices=n_prices,
            t_max=t_max,
            r=rs[i],
            init_move_firm=init_move_firms[i],
            seed=seeds[i],
            p_min=p_min,
            p_max=p_max
        )
        for i in range(n_simulations)
    ]

    return parameters


def run(parameters):

    m = model.Model(parameters)
    positions, prices, profits = m.run()
    bkp = backup.RunBackup(parameters=parameters, positions=positions, prices=prices, profits=profits)
    return bkp


def main():

    pool = mlt.Pool()

    backups = []

    shared_parameters = model.SharedParameters(
        n_simulations=4,
        t_max=250,
        n_positions=100,
        n_prices=100,
        p_min=1,
        p_max=100
    )
    pool_parameters = get_pool_parameters(**shared_parameters.dict())

    for bkp in tqdm.tqdm(
            pool.imap_unordered(run, pool_parameters),
            total=len(pool_parameters)):
        backups.append(bkp)

    pool_backup = backup.PoolBackup(parameters=shared_parameters, backups=backups)

    file_name = pool_backup.save()

    print("Data have been saved using file name: '{}'.".format(file_name))

    analysis.pool.distance_over_fov(file_name=file_name, pool_backup=pool_backup,
                                    fig_folder=os.path.expanduser("~\Desktop"))


def single():

    parameters = model.Parameters()

    m = model.Model(parameters)
    positions, prices, profits = m.run()

    bkp = backup.RunBackup(parameters, positions, prices, profits)
    file_name = bkp.save()

    print("Data have been saved using file name: '{}'.".format(file_name))


if __name__ == "__main__":
    single()
