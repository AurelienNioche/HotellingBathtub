from pylab import plt, np
import os
from scipy.signal import savgol_filter

import backup

span_ratio = 0.33


def distance_over_fov(file_name, show_random=True, bw=False, show_error_bars=False, show_fitting_curve=False,
                      fig_folder=None, data_folder=None):

    if fig_folder is None:
        fig_folder = "data/figures"

    os.makedirs(fig_folder, exist_ok=True)

    pool_backup = backup.PoolBackup.load(folder_name=data_folder, file_name=file_name)

    parameters = pool_backup.parameters
    backups = pool_backup.backups

    n_simulations = parameters.n_simulations

    n_positions = parameters.n_positions
    n_prices = parameters.n_prices
    unit_value = parameters.unit_value

    # Compute profit max
    profit_max = n_positions * n_prices * unit_value

    # Containers
    x = np.zeros(n_simulations)
    y = np.zeros(n_simulations)
    y_err = np.zeros(n_simulations)
    z = np.zeros(n_simulations)

    # How many time steps from the end of the simulation are included in analysis
    span = int(span_ratio * parameters.t_max)

    for i, b in enumerate(backups):

        try:
            # Save the parameter that affected the customers field of view
            x[i] = b.field_of_view / 2
        except AttributeError:
            x[i] = b.parameters.r

        # Compute the mean distance between the two firms
        data = np.absolute(
                b.positions[-span:, 0] -
                b.positions[-span:, 1]) / n_positions

        spacing = np.mean(data)
        spacing_std = np.std(data)

        y[i] = spacing
        y_err[i] = spacing_std

        # Get mean profits
        z[i] = np.mean(b.profits[-span:, :]) / profit_max

    # Plot this
    fig = plt.figure(figsize=(10, 6))
    ax = plt.subplot()

    ax.set_xlim(-0.01, 1.01)
    if max(y) < 0.5:
        ax.set_ylim(-0.01, 0.51)

    ax.set_xticks(np.arange(0, 1.1, 0.25))
    ax.set_yticks(np.arange(0, 0.51, 0.1))

    add_title_and_labels(ax)
    add_comment_with_file_name(fig=fig, file_name=file_name)

    if show_random:
        ax.axhline(0.33, color='0.5', linewidth=0.5, linestyle="--", zorder=-10)

    if show_error_bars:
        ax.errorbar(x, y, yerr=y_err, fmt='.', alpha=0.1)

    if show_fitting_curve:
        add_fitting_curve(ax=ax, x=x, y=y)

    if hasattr(parameters, 'running_mode') and parameters.running_mode == "discrete":
        boxplot(pool_backup=pool_backup, ax=ax, y=y)

    if bw:
        plot_bw(ax=ax, x=x, y=y, file_name=file_name, fig_folder=fig_folder)

    else:
        plot_color(fig=fig, ax=ax, x=x, y=y, z=z, file_name=file_name, fig_folder=fig_folder)


def boxplot(pool_backup, ax, y):

    parameters = pool_backup.parameters
    backups = pool_backup.backups

    to_plot = tuple([[] for i in range(len(parameters.fov_if_discrete))])

    for i, b in enumerate(backups):

        cond = parameters.fov_if_discrete.index(b.field_of_view)
        to_plot[cond].append(y[i])

    bp = ax.boxplot(to_plot, positions=parameters.fov_if_discrete)
    for e in ['boxes', 'caps', 'whiskers']:
        for b in bp[e]:
            b.set_alpha(0.5)


def plot_bw(ax, x, y, file_name, fig_folder):

    ax.scatter(x, y, facecolor="black", edgecolor='none', s=25, alpha=0.15)

    plt.tight_layout()

    if file_name:
        plt.savefig("{}/{}_gray.pdf".format(fig_folder, file_name))

    plt.show()


def plot_color(fig, ax, x, y, z, file_name, fig_folder):

    abc = ax.scatter(x, y, c=z, zorder=10, alpha=0.25)
    fig.colorbar(abc, label="Profits")

    plt.tight_layout()

    if file_name:
        plt.savefig("{}/{}.pdf".format(fig_folder, file_name))

    plt.show()


def add_comment_with_file_name(fig, file_name):
    plt.text(0.005, 0.005, file_name, transform=fig.transFigure, fontsize='x-small', color='0.5')


def add_fitting_curve(ax, x, y):

    window_size = len(y) - 2 if len(y) % 2 != 0 else len(y) - 1
    poly_order = 3
    order = np.argsort(x)
    y_hat = savgol_filter(y[order], window_size, poly_order)
    ax.plot(x[order], y_hat, linewidth=2, zorder=20)


def add_title_and_labels(ax):

    ax.set_xlabel("$r$")
    ax.set_ylabel("Mean distance")

    ax.set_title("Mean distance between firms over $r$")

