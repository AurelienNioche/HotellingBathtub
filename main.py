import multiprocessing as mlt
import tqdm
import os

import parameters
import model
import backup
import analysis


def main(parameters_file=None):
    """Produce data"""

    parameters.load(parameters_file)

    print('Parameters are: ', parameters.get())

    pool = mlt.Pool()

    backups = []

    for bkp in tqdm.tqdm(
            pool.imap_unordered(model.run, range(parameters.n_simulations)), total=parameters.n_simulations):
        backups.append(bkp)

    pool_backup = backup.PoolBackup(backups=backups)

    file_name = pool_backup.save()
    analysis.analyse_pool(pool_backup, file_name=file_name)


if __name__ == "__main__":

    parameters_files = None

    if os.path.exists("tasks"):
        parameters_files = [os.path.join("tasks", f)
                            for f in os.listdir("tasks") if os.path.isfile(os.path.join("tasks", f))]
    if parameters_files:
        for i in parameters_files:
            main(i)  # Use every parameters file contained in tasks folder

    else:
        main()  # Use default parameters file located in parameters.json
