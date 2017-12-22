import os
from pylab import plt

import backup

fig_folder = "data/figures"
os.makedirs(fig_folder, exist_ok=True)


def pos_firmA_over_pos_firmB(file_name):

    bkp = backup.RunBackup.load(file_name=file_name)

    pos = bkp.positions[-1000:]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.scatter(pos[:, 0], pos[:, 1], color="black", alpha=0.05)
    plt.xlim(-1, bkp.parameters.n_positions)
    plt.ylim(-1, bkp.parameters.n_positions)
    plt.xticks(range(0, bkp.parameters.n_positions+1, round(bkp.parameters.n_positions/5)))
    plt.yticks(range(0, bkp.parameters.n_positions+1, round(bkp.parameters.n_positions/5)))
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("{}\nfield of view: {}".format(file_name,  bkp.field_of_view))
    ax.set_aspect(1)
    plt.tight_layout()
    plt.savefig("data/figures/{}_evo_positions.pdf".format(file_name))
    plt.show()
