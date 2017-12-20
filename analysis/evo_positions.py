from pylab import np, plt

import backup


def evo_positions(file_name):

    bkp = backup.RunBackup.load(file_name=file_name)

    pos = bkp.positions[-1000:]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.scatter(pos[:, 0], pos[:, 1], color="black", alpha=0.01)
    plt.xlim(-1, bkp.parameters.n_positions)
    plt.ylim(-1, bkp.parameters.n_positions)
    plt.xticks(range(0, bkp.parameters.n_positions, round(bkp.parameters.n_positions/5)))
    plt.yticks(range(0, bkp.parameters.n_positions, round(bkp.parameters.n_positions/5)))
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title(file_name)
    ax.set_aspect(1)
    plt.tight_layout()
    plt.show()
