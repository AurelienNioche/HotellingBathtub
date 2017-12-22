import numpy as np
import matplotlib.pyplot as plt

import backup


def eeg_like(file_name):

    bkp = backup.RunBackup.load(file_name=file_name)

    pst = bkp.positions
    prc = bkp.prices

    t_max = 250 # bkp.parameters.t_max

    t = np.arange(t_max)

    position_A = pst[1:251, 0]
    position_B = pst[1:251, 1]
    price_A = prc[1:251, 0]
    price_B = prc[1:251, 0]

    color_A = "orange"
    color_B = "blue"

    position_min = 0
    position_max = bkp.parameters.n_positions - 1

    price_min = 1
    price_max = bkp.parameters.n_prices * bkp.parameters.unit_value

    fig = plt.Figure()

    # Position firm A

    ax = plt.subplot(4, 1, 1)
    ax.plot(t, position_A, color=color_A, alpha=1, linewidth=1.1)
    # ax.plot(t, position_B, color="black", alpha=0.5, linewidth=1)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([position_min, position_max])
    ax.set_ylabel('Position A', labelpad=10)

    # Add title
    plt.title("radius={}".format(bkp.field_of_view/2))

    # Position firm B

    ax = plt.subplot(4, 1, 2)
    ax.plot(t, position_B, color=color_B, alpha=1, linewidth=1.1)
    # ax.plot(t, position_A, color="black", alpha=0.5, linewidth=1)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([position_min, position_max])
    ax.set_ylabel('Position B', labelpad=10)

    # Price firm A

    ax = plt.subplot(4, 1, 3)
    ax.plot(t, price_A, color=color_A, alpha=1, linewidth=1.1, clip_on=False)
    # ax.plot(t, price_B, color="black", alpha=0.5, linewidth=1)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([price_min, price_max])
    ax.set_ylabel('Price A', labelpad=10)  #rotation=0)
    ax.set_ylim([price_min, price_max])

    # Price firm B

    ax = plt.subplot(4, 1, 4)
    ax.plot(t, price_B, color=color_B, alpha=1, linewidth=1.1, clip_on=False)
    # ax.plot(t, price_A, color="black", alpha=0.5, linewidth=1)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([price_min, price_max])
    ax.set_ylabel('Price B', labelpad=10) # , rotation=0)
    ax.set_ylim([price_min, price_max])

    ax.set_xlabel("Time", labelpad=10)

    plt.text(0.005, 0.005, file_name, transform=fig.transFigure, fontsize='x-small', color='0.5')
    plt.show()
