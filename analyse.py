import analysis


def main():
    file_name = "2017-12-22_16-48-42_994509"  # Max price 50, r=0.75, t_max=250
    # file_name = "2017-12-22_16-49-12_263358"  # Max price 50, r=0.25, t_max=250
    # file_name = "2017-12-22_16-49-20_509194"  # Max price 50, r=0.25, t_Max=250
    # file_name = "2017-12-22_16-49-00_253284"  # Max price 50, r=0.5

    # analysis.separate.pos_firmA_over_pos_firmB(file_name)
    analysis.separate.eeg_like(file_name)
    # analysis.separate.ascii_viewer(file_name)

    # file_name = "2017-12-20_16-47-16_824170"  # max price 50
    # analysis.pool.distance_over_fov(file_name)


if __name__ == '__main__':
    main()
