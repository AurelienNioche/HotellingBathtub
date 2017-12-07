import analysis
import backup


if __name__ == "__main__":

    file_name = "backup_2017-12-06_22-43-57_070773"
    pool_backup = backup.PoolBackup.load(file_name=file_name)
    analysis.analyse_pool(pool_backup=pool_backup, file_name=file_name)
    # analysis.analyse_stability(pool_backup)
