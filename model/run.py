import numpy as np
import tqdm

import backup
from . import env


def run(args):

    seed, parameters = args

    # print("Run simulation {}...\n".format(i))

    # For reproduction and variability
    np.random.seed(seed)

    it = range(parameters.t_max)

    # Get the parameter that will affect the field of view of customers
    if parameters.running_mode == 'unique':
        field_of_view = parameters.fov_if_unique
        it = tqdm.tqdm(it)

    elif parameters.running_mode == 'discrete':
        field_of_view = np.random.choice(parameters.fov_if_discrete)

    else:
        field_of_view = np.random.uniform(*parameters.fov_boundaries)

    # Backup
    b = backup.RunBackup(seed=seed, field_of_view=field_of_view, parameters=parameters)

    # Environment object
    e = env.Environment(
        parameters=parameters,
        field_of_view=field_of_view,
        init_firm_positions=np.random.randint(parameters.n_positions, size=2),
        init_firm_prices=1 + np.random.randint(parameters.n_prices, size=2)
    )

    for t in it:

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

    return b
