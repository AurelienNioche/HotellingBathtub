import analysis


def main():

    fig_folder = "doc/draft/fig/results"

    # Individual results
    file_names = (
        "2017-12-22_16-48-42_994509",  # Max price 50, r=0.75, t_max=250
        "2017-12-22_16-49-12_263358",  # Max price 50, r=0.25, t_max=250
        "2017-12-22_16-49-20_509194",  # Max price 50, r=0.25, t_max=250
        "2017-12-22_16-49-00_253284",  # Max price 50, r=0.5, t_max=250
    )

    for file_name in file_names:
        analysis.separate.pos_firmA_over_pos_firmB(file_name, folder=fig_folder)
        analysis.separate.eeg_like(file_name, folder=fig_folder)
        # analysis.separate.ascii_viewer(file_name)

    # Results for pool
    file_name = "2017-12-22_16-14-02_224254"
    # file_name = "2017-12-20_16-47-16_824170"  # max price 50
    analysis.pool.distance_over_fov(file_name, folder=fig_folder)
    analysis.pool.profits_over_fov(file_name=file_name, folder=fig_folder, separate_A_and_B=False)
    analysis.pool.profits_over_distance(file_name=file_name, folder=fig_folder, separate_A_and_B=False)


def optimal_against_random():

    import os
    fig_folder = os.path.expanduser("~/Desktop/")
    #
    # file_name = "2018-01-11_11-57-28_313189"
    # analysis.separate.profit_firmA_against_profit_firmB(file_name=file_name, folder=fig_folder)
    # analysis.separate.pos_firmA_over_pos_firmB(file_name, folder=fig_folder)
    # analysis.separate.eeg_like(file_name, folder=fig_folder)

    file_name = "2018-01-11_13-43-31_963302"
#    analysis.pool.distance_over_fov(file_name=file_name, folder=fig_folder)
    analysis.pool.profits_over_fov(file_name=file_name, folder=fig_folder)


if __name__ == '__main__':

    main()
