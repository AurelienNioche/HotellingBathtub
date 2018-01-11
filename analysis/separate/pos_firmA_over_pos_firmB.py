import os
from pylab import plt

import backup


def pos_firmA_over_pos_firmB(file_name, folder=None):

    if folder is None:
        folder = "data/figures"

    os.makedirs(folder, exist_ok=True)

    bkp = backup.RunBackup.load(file_name=file_name)

    pos = bkp.positions[-1000:]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.scatter(pos[:, 0], pos[:, 1], color="black", alpha=0.05)
    ax.axvline(0.5, color="white", linewidth=0.5, linestyle="--")
    ax.axhline(0.5, color="white", linewidth=0.5, linestyle="--")

    plt.xlim(-1, bkp.parameters.n_positions)
    plt.ylim(-1, bkp.parameters.n_positions)
    plt.xticks(range(0, bkp.parameters.n_positions+1, round(bkp.parameters.n_positions/5)))
    plt.yticks(range(0, bkp.parameters.n_positions+1, round(bkp.parameters.n_positions/5)))

    plt.xlabel("Position A")
    plt.ylabel("Position B")

    plt.text(0.005, 0.005, file_name, transform=fig.transFigure, fontsize='x-small', color='0.5')

    plt.title("$r={:.2f}$".format(bkp.field_of_view/2))
    ax.set_aspect(1)
    plt.tight_layout()
    plt.savefig("{}/{}_evo_positions.pdf".format(folder, file_name))
    plt.show()
