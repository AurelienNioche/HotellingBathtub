from pylab import plt, np
import os


def distance_over_fov(file_name, pool_backup, fig_folder=None):

    span_ratio = 0.33

    if fig_folder is None:
        fig_folder = "data/figures"

    os.makedirs(fig_folder, exist_ok=True)

    parameters = pool_backup.parameters
    backups = pool_backup.backups

    n_simulations = parameters.n_simulations

    n_positions = parameters.n_positions
    p_max = parameters.p_max

    # Compute profit max
    profit_max = n_positions * p_max

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

    ax.set_xlabel("$r$")
    ax.set_ylabel("Mean distance")

    ax.set_title("Mean distance between firms over $r$")

    # add comment with file name
    plt.text(0.005, 0.005, file_name, transform=fig.transFigure, fontsize='x-small', color='0.5')

    # show random
    plt.text(0.005, 0.005, file_name, transform=fig.transFigure, fontsize='x-small', color='0.5')

    abc = ax.scatter(x, y, c=z, zorder=10, alpha=0.25)
    fig.colorbar(abc, label="Profits")

    plt.tight_layout()

    if file_name:
        plt.savefig("{}/{}.pdf".format(fig_folder, file_name))

    plt.show()
