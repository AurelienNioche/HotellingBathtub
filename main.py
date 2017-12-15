import multiprocessing as mlt
import tqdm
import os
import numpy as np

import parameters
import model
import backup
import analysis


def main(parameters_file=None):
    """Produce data"""

    param = parameters.load(parameters_file)

    print('Parameters are: ', param.dict())

    pool = mlt.Pool()

    backups = []

    seeds = np.random.randint(2**32, size=param.n_simulations)

    for bkp in tqdm.tqdm(
            pool.imap_unordered(model.run, zip(seeds, (param, ) * param.n_simulations)),
            total=param.n_simulations):
        backups.append(bkp)

    pool_backup = backup.PoolBackup(backups=backups)

    file_name = pool_backup.save()
    analysis.analyse_pool(pool_backup, file_name=file_name)


if __name__ == "__main__":

    if os.path.exists("tasks") and os.listdir("tasks"):

        parameters_files = [os.path.join("tasks", f)
                            for f in os.listdir("tasks") if os.path.isfile(os.path.join("tasks", f))]
        for i in parameters_files:
            main(i)  # Use every parameters file contained in tasks folder

    else:
        main()  # Use default parameters file located in parameters.json
