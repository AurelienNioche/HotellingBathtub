from pylab import plt, np
import os
from scipy.signal import savgol_filter

import backup


fig_folder = "data/figures"
os.makedirs(fig_folder, exist_ok=True)


def analyse_pool(file_name, bw=False):

    pool_backup = backup.PoolBackup.load(file_name=file_name)

    parameters = pool_backup.parameters
    backups = pool_backup.backups

    n_simulations = parameters.n_simulations

    # Containers
    x = np.zeros(n_simulations)
    y = np.zeros(n_simulations)
    y_err = np.zeros(n_simulations)
    z = np.zeros(n_simulations)

    # How many time steps from the end of the simulation are included in analysis
    span = int(0.33 * parameters.t_max)

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
        profit_max = parameters.n_positions * parameters.n_prices * parameters.unit_value
        z[i] = np.mean(b.profits[-span:, :]) / profit_max

    if bw:
        plot_bw(x, y, file_name)

    else:
        plot_color(x, y, z, y_err, parameters, backups, file_name)


def plot_bw(x, y, file_name):

    # Plot this
    plt.figure(figsize=(10, 6))

    plt.scatter(x, y, facecolor="black", edgecolor='none', s=25, alpha=0.15)

    plt.xlabel("Field of view")
    plt.ylabel("Mean distance")

    if file_name:
        plt.title(file_name)

    plt.tight_layout()

    if file_name:
        plt.savefig("{}/{}_gray.pdf".format(fig_folder, file_name))

    plt.show()


def plot_color(x, y, z, y_err, parameters, backups, file_name, show_error_bars=False):

    # Plot this
    plt.figure(figsize=(10, 5))

    plt.scatter(x, y, c=z, zorder=10, alpha=0.25)
    plt.colorbar(label="Profits")

    fit = False

    if fit:
        window_size = len(y) - 2 if len(y) % 2 != 0 else len(y) - 1
        poly_order = 3
        order = np.argsort(x)
        y_hat = savgol_filter(y[order], window_size, poly_order)
        plt.plot(x[order], y_hat, linewidth=2, zorder=20)

    # Add boxplot if only extreme values have been tested
    if not parameters.running_mode == "discrete":
        if show_error_bars:
            plt.errorbar(x, y, yerr=y_err, fmt='.', alpha=0.1)

    else:
        to_plot = tuple([[] for i in range(len(parameters.fov_if_discrete))])

        for i, b in enumerate(backups):
            cond = parameters.fov_if_discrete.index(b.field_of_view)
            to_plot[cond].append(y[i])

        bp = plt.boxplot(to_plot, positions=parameters.fov_if_discrete)
        for e in ['boxes', 'caps', 'whiskers']:
            for b in bp[e]:
                b.set_alpha(0.5)

    plt.xlabel("Field of view")
    plt.ylabel("Mean distance")

    if file_name:
        plt.title(file_name)

    plt.tight_layout()

    if file_name:
        plt.savefig("{}/{}.pdf".format(fig_folder, file_name))

    plt.show()
