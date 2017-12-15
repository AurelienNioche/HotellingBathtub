import numpy as np

import parameters
import model


def main():
    """Produce data"""
    param = parameters.load()

    print('Parameters are: ', param.dict())

    seed = np.random.randint(2**32)
    model.run((seed, param))


if __name__ == "__main__":

    main()
