import numpy as np
import matplotlib.pyplot as plt
import os

folder = "../../doc/draft/fig/a_priori"  # "figures"
os.makedirs(folder, exist_ok=True)


plt.rc("ytick", labelsize="small")
plt.rc("xtick", labelsize="small")

# Parameters
# -----------------------------------------------------------------------------
seed       = 123
np.random.seed(seed)
n_position = 100  # Number of discrete position over [0,1]
n_client   = 100  # Number of clients
n_firm     = 2    # Number of firms

# Uniform position
P = np.linspace(0, 1, n_client, endpoint=True)
P = (np.round(P*(n_position-1))).astype(int)


def get_targetable_clients(rel_r):

    # Same constant radius for each client
    r = n_position * rel_r
    R = int(np.round(r)) * np.ones(n_client, dtype=int)

    # Build the local view for each client
    V = np.zeros((n_client, n_position))
    for i in range(n_client):
        lower_bound = max(0, P[i]-R[i])
        upper_bound = min(P[i]+R[i], n_position)
        V[i, lower_bound:upper_bound] = 1

    return V.sum(axis=0)


# Client visibility
ax = plt.subplot()
X = np.linspace(0, 1, n_position)


for rr in [0.25, 0.50, 0.75]:
    Y = get_targetable_clients(rr)
    ax.plot(X, Y, label="$r={:.2f}$".format(rr), clip_on=True)

plt.legend()

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


for tick in ax.get_xticklabels():
    tick.set_fontsize("small")
for tick in ax.get_yticklabels():
    tick.set_fontsize("small")
ax.set_xticks([0,0.5, 1])
ax.set_yticks([25, 50, 75, 100])
ax.set_ylim([22, 100.25])
ax.set_ylabel("Targetable clients")
ax.set_xlabel("Position")

plt.savefig("{}/clients_visibility.pdf".format(folder))
plt.show()
