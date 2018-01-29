import os
from pylab import plt


def pos_firmA_over_pos_firmB(file_name, backup, fig_folder=None):

    if fig_folder is None:
        fig_folder = "data/figures"

    os.makedirs(fig_folder, exist_ok=True)

    n_positions = backup.parameters.n_positions

    pos = backup.positions[-1000:]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.scatter(pos[:, 0], pos[:, 1], color="black", alpha=0.05)
    ax.axvline(0.5, color="white", linewidth=0.5, linestyle="--")
    ax.axhline(0.5, color="white", linewidth=0.5, linestyle="--")

    plt.xlim(-1, n_positions)
    plt.ylim(-1, n_positions)
    plt.xticks(range(0, n_positions+1, round(n_positions/5)))
    plt.yticks(range(0, n_positions+1, round(n_positions/5)))

    plt.xlabel("Position A")
    plt.ylabel("Position B")

    plt.text(0.005, 0.005, file_name, transform=fig.transFigure, fontsize='x-small', color='0.5')

    plt.title("$r={:.2f}$".format(backup.parameters.r))
    ax.set_aspect(1)
    plt.tight_layout()
    plt.savefig("{}/{}_evo_positions.pdf".format(fig_folder, file_name))
    plt.show()
