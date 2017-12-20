import hyperopt as hpt   # Warning! TypeError: 'generator' object is not subscriptable -> pip install networkx==1.11
import numpy as np
import os

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
        "t_max": 3000,
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
        "unit_value": 1,
        "unique": True,
        "unique_fov": True
    }

    param = parameters.Parameters(**param)

    # To return: mean of this list
    profits = []

    # Environment object
    for field in [0.3, 0.4, 0.5, 0.6, 0.7]:

        e = env.Environment(
            parameters=param,
            field_of_view=field,
            init_firm_positions=[10, 10],
            init_firm_prices=[5, 5]
        )

        for t in range(param.t_max):

            print("\rTrial {} => cond:{}, time step: {}".format(trials, field, t), end='')

            # New time step
            e.time_step_first_part()

            # End turn
            e.time_step_second_part()

            if t > 0.33*param.t_max:
                profits.append(np.mean(e.profits))

    trials += 1

    return -np.mean(profits)


def main():

    space = {
        'alpha': hpt.hp.uniform('alpha', 0.09, 0.3),
        'temp': hpt.hp.uniform('temp', 0.015, 0.025)
    }

    result = hpt.fmin(
        fn=run,
        space=space,
        algo=hpt.tpe.suggest,
        max_evals=1000
    )

    os.makedirs("optimization", exist_ok=True)

    with open("optimization/optimization_results.txt", 'a') as f:
        line = '\nOptimized parameters are: {}'.format(result)
        f.write(line)
        f.close()
        print(line)


if __name__ == '__main__':
    main()
