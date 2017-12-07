import multiprocessing as mlt

import parameters

import model
import backup
import analysis


def main():

    pool = mlt.Pool()

    backups = pool.map(model.run, range(parameters.n_simulations))

    pool_backup = backup.PoolBackup(backups=backups)

    if parameters.save is True:
        file_name = pool_backup.save()
        analysis.analyse_pool(pool_backup, file_name=file_name)

    else:
        analysis.analyse_pool(pool_backup)


if __name__ == "__main__":

    main()
