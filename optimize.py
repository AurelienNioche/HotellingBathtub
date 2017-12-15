import hyperopt as hpt
import numpy as np

import parameters
from model import env


# global count variable
trials = 0


def run(kwargs):

    global trials

    #  Parameters definition
    param = {
        "n_positions": 21,
        "n_prices": 11,
        "n_firms": 2,
        "alpha": kwargs["alpha"],
        "momentum": 0,
        "temp": kwargs["temp"],
        "n_simulations": 1,
        "t_max": 50,
        "zombies_customers": False,
        "mode": "p_fixed",
        "discrete": True,
        "fields_of_view": [
            0.3,
            0.7
        ],
        "fov_boundaries": [
            0,
            1
          ],
        "firm_class": ["Firm", "Firm"],
        "unit_value": 1
    }

    param = parameters.Parameters(**param)

    # To return: mean of this list
    profits = []

    # Environment object
    for field in [0.3, 0.7]:

        e = env.Environment(
            parameters=param,
            field_of_view=field,
            init_firm_positions=[10, 10],
            init_firm_prices=[5, 5]
        )

        for t in range(param.t_max):

            print("\rTrial nb {} =>  time step {}".format(trials, t), end='')

            # New time step
            e.time_step_first_part()

            # End turn
            e.time_step_second_part()

            profits.append(np.mean(e.profits))

    trials += 1

    return -np.mean(profits)


def main():

    space = {
        'alpha': hpt.hp.uniform('alpha', 0.05, 0.3),
        'temp': hpt.hp.uniform('temp', 0.01, 0.03)
    }

    result = hpt.fmin(
        fn=run,
        space=space,
        algo=hpt.tpe.suggest,
        max_evals=10
    )

    print('\nOptimized parameters are: ', result)


if __name__ == '__main__':
    main()
