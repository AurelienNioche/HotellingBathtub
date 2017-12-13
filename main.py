import multiprocessing as mlt
import tqdm

import parameters

import model
import backup
import analysis


def main():
    """Produce data"""

    print('Parameters are: ', parameters.get())

    pool = mlt.Pool()

    backups = []

    for i in tqdm.tqdm(
            pool.imap_unordered(model.run, range(parameters.n_simulations), total=parameters.n_simulations)):
        backups.append(i)

    pool_backup = backup.PoolBackup(backups=backups)

    if parameters.save is True:
        file_name = pool_backup.save()
        analysis.analyse_pool(pool_backup, file_name=file_name)

    else:
        analysis.analyse_pool(pool_backup)


if __name__ == "__main__":

    main()
