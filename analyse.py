import analysis


def main():

    # file_name = "2017-12-22_13-23-58_025412"
    file_name = "2017-12-22_13-26-07_335384"

    # analysis.separate.pos_firmA_over_pos_firmB(file_name)
    # analysis.separate.ascii_viewer(file_name)
    analysis.separate.eeg_like(file_name)
    # analysis.analyse_pool("2017-12-20_16-47-16_824170")


if __name__ == '__main__':
    main()