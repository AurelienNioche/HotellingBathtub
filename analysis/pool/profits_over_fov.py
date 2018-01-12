from pylab import plt, np
import os

import backup


def profits_over_fov(
        file_name, folder=None, separate_A_and_B=True, fitting_curve=True):

    if folder is None:
        folder = "data/figures"

    os.makedirs(folder, exist_ok=True)

    pool_backup = backup.PoolBackup.load(file_name=file_name)

    parameters = pool_backup.parameters
    backups = pool_backup.backups

    n_simulations = parameters.n_simulations

    # Containers
    x = np.zeros(n_simulations)
    y = np.zeros((2, n_simulations))

    for i, b in enumerate(backups):

        # Save the parameter that affected the customers field of view
        x[i] = b.field_of_view / 2

        # Get profits
        profit_max = parameters.n_positions * parameters.n_prices * parameters.unit_value
        for f in range(2):
            y[f, i] = np.mean(b.profits[:, f]) / profit_max

    # Plot this
    fig = plt.figure(figsize=(10, 6))
    ax = plt.subplot()

    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(-0.01, 0.51)

    ax.set_xticks(np.arange(0, 1.1, 0.25))
    ax.set_yticks(np.arange(0, 0.51, 0.1))

    add_title_and_labels(ax)
    add_comment_with_file_name(fig=fig, file_name=file_name)

    if separate_A_and_B is True:
        ax.scatter(x, y[0], zorder=10, alpha=0.25, label="Firm A")
        ax.scatter(x, y[1], zorder=10, alpha=0.25, label="Firm B")
        plt.legend()

    else:
        ax.scatter(x, np.mean(y, axis=0), zorder=10, alpha=0.25, color="black")

    if fitting_curve is True:
        add_fitting_curve(ax=ax, x=x, y=y[0])
        add_fitting_curve(ax=ax, x=x, y=y[1])

    plt.tight_layout()

    if file_name:
        plt.savefig("{}/{}_profits_over_fov.pdf".format(folder, file_name))

    plt.show()


def add_comment_with_file_name(fig, file_name):
    plt.text(0.005, 0.005, file_name, transform=fig.transFigure, fontsize='x-small', color='0.5')


def add_fitting_curve(ax, x, y):

    from scipy.optimize import least_squares

    def model(x, u):
        return x[0] * (u ** 2 + x[1] * u) / (u ** 2 + x[2] * u + x[3])

    def fun(x, u, y):
        return model(x, u) - y

    order = np.argsort(x)

    xdata = x[order]
    ydata = y[order]

    x0 = np.zeros(4)

    res = least_squares(fun, x0, bounds=(-1, 100), args=(xdata, ydata), verbose=1).x

    u_test = np.linspace(0, 1)
    ax.plot(u_test, model(res, u_test), '--', zorder=-10)


def add_title_and_labels(ax):

    ax.set_xlabel("$r$")
    ax.set_ylabel("Mean profits")

    ax.set_title("Profits over $r$")

