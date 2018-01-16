import numpy as np
import multiprocessing as mlt

from .. import parameters
from .. import backup
from . import brute_force


def main():

    param =

    print('Parameters are: ', param.dict())

    pool = mlt.Pool()

    backups = []

    seeds = np.random.randint(2 ** 32, size=param.n_simulations)

    for bkp in tqdm.tqdm(
            pool.imap_unordered(model.run, zip(seeds, (param,) * param.n_simulations)),
            total=param.n_simulations):
        backups.append(bkp)

    pool_backup = backup.PoolBackup(parameters=param, backups=backups)

    file_name = pool_backup.save()

    print("Data have been saved using file name: '{}'.".format(file_name))

    try:
        analysis.pool.distance_over_fov(file_name=file_name)
    except _tkinter.TclError:
        print("Figures can not be produced if there is no graphic server.")


if __name__ == "__main__":
    main()