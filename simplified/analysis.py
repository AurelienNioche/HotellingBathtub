import os

try:
    import simplified.analysis as analysis
    import simplified.backup as backup

except ModuleNotFoundError:
    import analysis
    import backup


def main():

    file_name = "2018-01-29_18-07-20_781493"
    folder_name = os.path.dirname(os.path.realpath(__file__)) + "/data/pickle/"

    pool_backup = backup.PoolBackup.load(file_name=file_name, folder_name=folder_name)

    analysis.pool.distance_over_fov(file_name=file_name, pool_backup=pool_backup,
                                    fig_folder=os.path.expanduser("~\Desktop"))


def single():

    file_name = "2018-01-29_18-26-36_382249"
    folder_name = os.path.dirname(os.path.realpath(__file__)) + "/data/pickle/"

    run_backup = backup.RunBackup.load(file_name=file_name, folder_name=folder_name)

    analysis.separate.eeg_like(file_name=file_name, backup=run_backup,
                               fig_folder=os.path.expanduser("~\Desktop"))

    analysis.separate.pos_firmA_over_pos_firmB(file_name=file_name, backup=run_backup,
                                               fig_folder=os.path.expanduser("~\Desktop"))


if __name__ == "__main__":

    single()
