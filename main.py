import multiprocessing as mlt
import shutil


try:
    import parameters

except ModuleNotFoundError:
    shutil.copy("templates/parameters.py", "parameters/parameters.py")
    import parameters

import model
import backup
import analysis


def main():

    pool = mlt.Pool()

    backups = pool.map(model.run, range(parameters.n_simulations))

    pool_backup = backup.PoolBackup(backups=backups)

    if parameters.save is True:
        pool_backup.save()

    analysis.analyse_pool(pool_backup)


if __name__ == "__main__":

    main()
