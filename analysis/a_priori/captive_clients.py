import tqdm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import os

# Computation
# -----------------------------------------------------------------------------


def compute_clients(x1, x2):
    """ Compute the number of unique and shared. """

    U1 = np.where(V[:, x1] == 1)[0]
    U2 = np.where(V[:, x2] == 1)[0]
    S = np.intersect1d(U1, U2)
    U1 = np.setdiff1d(U1, S)
    U2 = np.setdiff1d(U2, S)
    return len(U1), len(U2), len(S)


# ----------------------------------- #

folder = "../../doc/draft/fig/a_priori"  # "figures"
os.makedirs(folder, exist_ok=True)

# ----------------------------------------- #

plt.rc("ytick", labelsize="small")
plt.rc("xtick", labelsize="small")

# Parameters
# -----------------------------------------------------------------------------
seed       = 123
np.random.seed(seed)
n_position = 100 # Number of discrete position over [0,1]
n_client   = 100 # Number of clients
n_firm     = 2  # Number of firms


# Uniform position
P = np.linspace(0, 1, n_client, endpoint=True)
P = (np.round(P*(n_position-1))).astype(int)

relative_radius = [0.25, 0.5, 0.75]

for rr in relative_radius:

    # Same constant radius for each client
    r = n_position * rr
    R = int(np.round(r))*np.ones(n_client,dtype=int)

    # Build the local view for each client
    V = np.zeros((n_client, n_position))
    for i in range(n_client):
        lower_bound = max(0, P[i]-R[i])
        upper_bound = min(P[i]+R[i], n_position)
        V[i, lower_bound:upper_bound] = 1

    C1 = np.zeros((n_position, n_position))
    C2 = np.zeros((n_position, n_position))
    S  = np.zeros((n_position, n_position))
    G  = np.zeros((n_position, n_position))

    for x1 in tqdm.trange(n_position):
        for x2 in range(n_position):
            u1, u2, s = compute_clients(x1, x2)
            C1[x1, x2] = u1
            C2[x1, x2] = u2
            S[x1, x2] = s
            G[x1, x2] = n_client - u1 - u2 - s

    # Visualization
    # -----------------------------------------------------------------------------
    # fig = plt.figure(figsize=(7, 7))

    # Captive clients (A)
    ax = plt.subplot()
    ax.set_aspect(1)

    cmap = plt.get_cmap("viridis")

    bounds = np.arange(0, 51, 2)
    norm = colors.BoundaryNorm(bounds, cmap.N)

    im = ax.imshow(C1, vmin=0, vmax=n_client/2, origin='lower', extent=[0, 100, 0, 100], norm=norm)
    cb = plt.colorbar(im, norm=norm, ticks=(0, 25, 50))

    n_levels = int(C1.max()*16/(n_client/2))
    ct = ax.contourf(C1, n_levels, origin='lower', vmax=n_client / 2)

    ax.axvline(50, color="white", linewidth=0.5, linestyle="--", zorder=10)
    ax.axhline(50, color="white", linewidth=0.5, linestyle="--", zorder=10)
    ax.set_xlabel("Position A", labelpad=10)
    ax.set_ylabel("Position B", labelpad=10)

    ax.set_title("A captive clients ($r={:.2f}$)".format(rr))

    plt.savefig("{}/captive_clients_r_{}.pdf".format(folder, int(rr*100)))
    plt.show()
