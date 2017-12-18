from pylab import plt, np
import os
import tqdm
from scipy.signal import savgol_filter
import analysis.parameters as analysis


fig_folder = "data/figures"
os.makedirs(fig_folder, exist_ok=True)


def analyse_profits(pool_backup, file_name=""):

    parameters = pool_backup.parameters
    backups = pool_backup.backups

    profit_max = parameters.n_positions * parameters.n_prices * parameters.unit_value

    n_pools = 4

    # labels = [str(i) for i in range(n_pools)]

    labels = [
        "0 <= FoV < 0.25",
        "0.25 <= FoV < 0.50",
        "0.50 <= FoV < 0.75",
        "0.75 <= FoV <= 1"
    ]

    # f_cond = lambda x: 0 if x < 0.33 else 1 if 0.33 <= x <= 0.66 else 2

    f_cond = lambda x: 0 if x < 0.25 else 1 if x < 0.5 else 2 if x < 0.75 else 3

    x = range(parameters.t_max)
    for_y = [[[] for j in range(parameters.t_max)] for i in range(n_pools)]

    for i, b in tqdm.tqdm(enumerate(backups), total=len(backups)):

        cond = f_cond(b.field_of_view)

        for t in range(parameters.t_max):

            for_y[cond][t].append(np.mean(b.profits[t, :]) / profit_max)

    for i in range(n_pools):
        y = np.array([np.mean(for_y[i][t]) for t in range(parameters.t_max)])
        y_err = np.array([np.std(for_y[i][t]) for t in range(parameters.t_max)])
        plt.plot(x, y, label=labels[i])
        plt.fill_between(x, y-(y_err/2), y+(y_err/2), color="C{}".format(i), alpha=.25)

    plt.legend()
    plt.xlabel("t")
    plt.ylabel("Mean profit")

    if file_name:
        plt.title(file_name)

    plt.tight_layout()

    if file_name:
        plt.savefig("{}/{}_mean_profit_{}_cat.pdf".format(fig_folder, file_name, n_pools))

    # plt.show()
