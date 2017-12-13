import parameters

import model


def main():
    """Produce data"""

    print('Parameters are: ', parameters.get())

    model.run(0)


if __name__ == "__main__":

    main()
