import analysis
import backup


if __name__ == "__main__":

    pool_backup = backup.PoolBackup.load("backup_2017-12-06_15-23-57_769814")
    analysis.analyse_pool(pool_backup=pool_backup)