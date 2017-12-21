import analysis


def main():

    file_name = "2017-12-21_17-00-14_669489"

    analysis.evo_positions(file_name)
    analysis.ascii_viewer(file_name)
    # analysis.analyse_pool("2017-12-20_16-47-16_824170")


if __name__ == '__main__':
    main()