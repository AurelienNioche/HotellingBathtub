from pylab import plt, np
import os
import tqdm

import backup


def profit_firmA_against_profit_firmB(file_name, folder=None):

    if folder is None:
        folder = "data/figures"

    os.makedirs(folder, exist_ok=True)

    bkp = backup.RunBackup.load(file_name=file_name)
    parameters = bkp.parameters

    profit_max = parameters.n_positions * parameters.n_prices * parameters.unit_value

    x = np.arange(parameters.t_max)
    y = np.zeros((2, parameters.t_max))

    for f in range(2):
        for t in range(parameters.t_max):
            y[f, t] = np.mean(bkp.profits[:t+1, f] / profit_max)

        # y = np.array([np.mean(for_y[i][t]) for t in range(parameters.t_max)])
        # y_err = np.array([np.std(for_y[i][t]) for t in range(parameters.t_max)])

    fig = plt.Figure()

    plt.plot(x, y[0], label="Firm A")
    plt.plot(x, y[1], label="Firm B")
        # plt.fill_between(x, y - (y_err / 2), y + (y_err / 2), color="C{}".format(i), alpha=.25)

    plt.legend()
    plt.xlabel("t")
    plt.ylabel("Mean profit")

    plt.text(0.005, 0.005, file_name, transform=fig.transFigure, fontsize='x-small', color='0.5')

    plt.title("Evolution of profits over time ($r={}$)".format(bkp.field_of_view/2))

    plt.tight_layout()

    plt.savefig("{}/{}_mean_profit.pdf".format(folder, file_name))

    plt.show()
