import numpy as np

import parameters
import backup
from . import env

seeds = np.random.randint(2**32, size=parameters.n_simulations)


def run(i):

    # print("Run simulation {}...\n".format(i))

    # For reproduction and variability
    np.random.seed(seeds[i])

    # Get the parameter that will affect the field of view of customers
    if parameters.discrete is True:
        field_of_view = np.random.choice(parameters.fields_of_view)

    else:
        field_of_view = np.random.uniform(*parameters.fov_boundaries)

    # Backup
    b = backup.RunBackup(seed=seeds[i], field_of_view=field_of_view)

    # Environment object
    e = env.Environment(
        field_of_view=field_of_view,
        init_firm_positions=np.random.randint(parameters.n_positions, size=2),
        init_firm_prices=1 + np.random.randint(parameters.n_prices, size=2)
    )

    for t in range(parameters.t_max):

        # New time step
        e.time_step_first_part()

        # For future analysis
        b.update(
            t=t,
            positions=e.positions,
            prices=e.prices,
            profits=e.profits
        )

        # End turn
        e.time_step_second_part()

    # print("Simulation {} ends successfully.".format(i))

    return b

