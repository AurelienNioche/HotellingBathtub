import multiprocessing as mlt
import tqdm
import os
import numpy as np

import parameters
import model
import backup
import analysis
import avakas

import sys


def main(parameters_file=None):
    """Produce data"""

    param = parameters.load(parameters_file)

    if param.running_mode == 'unique':
        seed = np.random.randint(2 ** 32)
        bkp = model.run((seed, param))
        file_path = bkp.save()
        print("Data have been saved using file name: '{}'.".format(file_path))

        analysis.evo_positions(file_path)

    else:
        print('Parameters are: ', param.dict())

        pool = mlt.Pool()

        backups = []

        seeds = np.random.randint(2**32, size=param.n_simulations)

        for bkp in tqdm.tqdm(
                pool.imap_unordered(model.run, zip(seeds, (param, ) * param.n_simulations)),
                total=param.n_simulations):
            backups.append(bkp)

        pool_backup = backup.PoolBackup(parameters=param, backups=backups)

        file_name = pool_backup.save()

        print("Data have been saved using file name: '{}'.".format(file_name))

        analysis.analyse_pool(file_name=file_name)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        i = sys.argv[1]
        parameters_file = avakas.get

    if os.path.exists("tasks") and os.listdir("tasks"):

        print("I will use the parameters files in the 'tasks' directory.")

        parameters_files = [os.path.join("tasks", f)
                            for f in os.listdir("tasks") if os.path.isfile(os.path.join("tasks", f))]
        for i in parameters_files:
            main(i)  # Use every parameters file contained in tasks folder

    else:
        main()  # Use default parameters file located in parameters.json
