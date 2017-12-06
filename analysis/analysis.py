import numpy as np


def analyse_pool(pool_backup):

    analysis_span = 0.1

    parameters = pool_backup.parameters
    backups = pool_backup.backups

    n_simulations = parameters.n_simulations

    # Containers
    x = np.zeros(n_simulations)
    y = np.zeros(n_simulations)
    y_err = np.zeros(n_simulations)
    z = np.zeros(n_simulations)

    # How many time steps from the end of the simulation are included in analysis
    span = int(analysis_span * parameters.t_max)

    for i, b in enumerate(backups):

        # Save the parameter that affected the customers field of view
        x[i] = b.field_of_view

        # Compute the mean distance between the two firms
        data = np.absolute(
                b.positions[-span:, 0] -
                b.positions[-span:, 1]) / parameters.n_positions

        spacing = np.mean(data)
        spacing_std = np.std(data)

        y[i] = spacing
        y_err[i] = spacing_std

        # Get mean profits
        profit_max = parameters.n_positions * parameters.n_prices
        z[i] = np.mean(b.profits[-span:, :]) / profit_max

    # Plot this
    from pylab import plt

    plt.figure(figsize=(10, 6))

    plt.scatter(x, y, c=z, zorder=10)
    plt.colorbar(label="Profits")

    # Add boxplot if only extreme values have been tested
    if not parameters.discrete:
        plt.errorbar(x, y, yerr=y_err, fmt='.', alpha=0.5)

    else:
        to_plot = tuple([[] for i in range(len(parameters.fields_of_view))])

        for i, b in enumerate(backups):
            cond = parameters.fields_of_view.index(b.field_of_view)
            to_plot[cond].append(y[i])

        bp = plt.boxplot(to_plot, positions=parameters.fields_of_view)
        for e in ['boxes', 'caps', 'whiskers']:
            for b in bp[e]:
                b.set_alpha(0.5)

    plt.title(parameters.mode.replace("_", " ").capitalize())
    plt.xlabel("Field of view")
    plt.ylabel("Mean distance")

    plt.tight_layout()
    plt.show()
