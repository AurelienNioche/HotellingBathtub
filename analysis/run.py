import backup
import analysis
from . import parameters


def run():

    pool_backup = backup.PoolBackup.load(file_name=parameters.file_name)
    analysis.analyse_profits(pool_backup=pool_backup, file_name=parameters.file_name)
    # analysis.analyse_pool(pool_backup=pool_backup, file_name=parameters.file_name)
