import numpy as np

import backup


def ascii_viewer(file_name):

    bkp = backup.RunBackup.load(file_name=file_name)

    pos = bkp.positions
    prc = bkp.prices

    for t in range(bkp.parameters.t_max):
        frags = []

        for i in range(bkp.parameters.n_positions):

            a_part = "A:{}".format("{}".format(prc[t, 0]).zfill(2))
            b_part = "B:{}".format("{}".format(prc[t, 1]).zfill(2))
            neutral_part = "-" * len(a_part)

            f = "|"

            pres = np.where(pos[t, :] == i)[0]

            if not len(pres):
                f += neutral_part * 2

            elif len(pres) == 2:
                f += a_part + b_part

            else:
                if pres[0] == 0:
                    f += a_part + neutral_part
                else:
                    f += neutral_part + b_part

            f += "|"
            frags.append(f)

        print("{}".format(t).zfill(4), "".join(frags))