from pylab import plt, np
from scipy.signal import savgol_filter

import backup


sample_size = 10


def analyse_stability(file_name):

    pool_backup = backup.PoolBackup.load(file_name)

    parameters = pool_backup.parameters
    backups = pool_backup.backups

    n_backups = len(backups)

    if n_backups > sample_size:
        idx = np.random.choice(range(n_backups), size=sample_size, replace=False)

    else:
        idx = np.arange(n_backups)

    for i in idx:

        b = backups[i]

        plt.title(b.field_of_view)

        x = np.arange(parameters.t_max)
        y = np.absolute(b.positions[:, 0] - b.positions[:, 1]) / parameters.n_positions

        plt.scatter(x, y, marker='.')

        xx = np.linspace(x.min(), x.max(), len(y))

        window_size = len(y) - 2 if len(y) % 2 == 0 else len(y) - 1
        poly_order = 3

        y_hat = savgol_filter(y, window_size, poly_order)
        plt.plot(xx, y_hat, linewidth=2)

        plt.show()
