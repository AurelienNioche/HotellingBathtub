import numpy as np
import multiprocessing as mlt

import parameters
from model import backup, env

seeds = np.random.randint(2**32, size=parameters.n_simulations)


def run(i):

    print("Run simulation {}...".format(i))

    # For reproduction and variability
    np.random.seed(seeds[i])

    # Get the parameter that will affect the field of view of customers
    if parameters.extremes_only:
        parameter_field_of_view = 0.2 if i % 2 == 0 else 0.8
    else:
        parameter_field_of_view = np.random.random()

    # Backup
    b = backup.Backup(seed=seeds[i], parameter_field_of_view=parameter_field_of_view)

    # Environment object
    e = env.Environment(
        parameter_field_of_view=parameter_field_of_view,
        init_firm_positions=np.random.randint(parameters.n_positions, size=2),
        init_firm_prices=np.random.randint(1, parameters.n_prices + 1, size=2)
    )

    for t in range(parameters.t_max):

        # New time step
        e.time_step_first_part()

        # For future analysis
        b.update(
            t=t,
            positions=e.get_positions(),
            prices=e.get_prices(),
            profits=e.get_profits()
        )

        # End turn
        e.time_step_second_part()

    print("Simulation {} ends successfully.".format(i))
    print()

    return b


def analyse(backups):

    # Containers
    p = np.zeros(parameters.n_simulations)
    m = np.zeros(parameters.n_simulations)

    # How many time steps from the end of the simulation are included in analysis
    span = int(parameters.analysis_span_prop * parameters.t_max)

    for i, b in enumerate(backups):

        # Compute the mean distance between the two firms
        spacing = np.mean(
            np.absolute(
                b.positions[-span][0] -
                b.positions[-span][1])
        )
        m[i] = spacing

        # Save the parameter that affected the customers field of view
        p[i] = b.parameter_field_of_view

    # Plot this
    from pylab import plt

    plt.scatter(p, m, s=10)

    # Add boxplot if only extreme values have been tested
    if parameters.extremes_only:
        bp = plt.boxplot((m[0::2], m[1::2]), positions=np.unique(p))
        for e in ['boxes', 'caps', 'whiskers']:
            for b in bp[e]:
                b.set_alpha(0.5)

    plt.title(parameters.mode.replace("_", " ").capitalize())
    plt.xlabel("Field of view")
    plt.ylabel("Mean distance")

    plt.show()


def main():

    pool = mlt.Pool()

    backups = pool.map(run, range(parameters.n_simulations))
    analyse(backups)


if __name__ == "__main__":

    main()
