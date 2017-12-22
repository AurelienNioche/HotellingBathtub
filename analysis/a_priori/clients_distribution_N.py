import tqdm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

plt.rc("ytick", labelsize="small")
plt.rc("xtick", labelsize="small")

# Parameters
# -----------------------------------------------------------------------------
seed       = 123
np.random.seed(seed)
n_position = 32 # Number of discrete position over [0,1]
n_client   = 32 # Number of clients
n_firm     = 2  # Number of firms

# Uniform position
P = np.linspace(0, 1, n_client, endpoint=True)
P = (np.round(P*(n_position-1))).astype(int)
# Same constant radius for each client
r = n_position/4
R = int(np.round(r))*np.ones(n_client,dtype=int)


# Computation
# -----------------------------------------------------------------------------

def compute_clients(x1, x2):
    """ Compute the number of unique and shared. """

    U1 = np.where(V[:,x1] == 1)[0]
    U2 = np.where(V[:,x2] == 1)[0]
    S = np.intersect1d(U1, U2)
    U1 = np.setdiff1d(U1, S)
    U2 = np.setdiff1d(U2, S)
    return len(U1), len(U2), len(S)

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
        C1[x1,x2] = u1
        C2[x1,x2] = u2
        S[x1,x2] = s
        G[x1,x2] = n_client - u1 - u2 - s



# Visualization
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(7,8))


# Captive clients (A)
ax = plt.subplot2grid((5, 2), (0, 0), rowspan=2, colspan=1)
ct = ax.contourf(C1, 16, extent=[0,1,0,1], origin='lower')
plt.colorbar(ct)
ax.set_xlim(0,1), ax.set_xticks([0,1])
ax.set_ylim(0,1), ax.set_yticks([0,1])
ax.axvline(0.5, color="white", linewidth=0.5, linestyle="--")
ax.axhline(0.5, color="white", linewidth=0.5, linestyle="--")
ax.set_xlabel("Firm B position", labelpad=-10)
ax.set_ylabel("Firm A position", labelpad=-10)
ax.set_title("A captive clients")
text = ax.text(0.05, 0.95, "A", fontsize=16,  weight="bold",
               color="white", ha="left", va="top", transform=ax.transAxes)
text.set_path_effects([path_effects.Stroke(linewidth=1, foreground='black'),
                       path_effects.Normal()])

# Captive clients (B)
ax = plt.subplot2grid((5, 2), (0, 1), rowspan=2, colspan=1)
ct = ax.contourf(C2, 16, extent=[0,1,0,1], origin='lower')
plt.colorbar(ct)
ax.set_xlim(0,1), ax.set_xticks([0,1])
ax.set_ylim(0,1), ax.set_yticks([0,1])
ax.axvline(0.5, color="white", linewidth=0.5, linestyle="--")
ax.axhline(0.5, color="white", linewidth=0.5, linestyle="--")
ax.set_xlabel("Firm B position", labelpad=-10)
ax.set_ylabel("Firm A position", labelpad=-10)
ax.set_title("B captive clients")
text = ax.text(0.05, 0.95, "B", fontsize=16,  weight="bold",
               color="white", ha="left", va="top", transform=ax.transAxes)
text.set_path_effects([path_effects.Stroke(linewidth=1, foreground='black'),
                       path_effects.Normal()])

# Volatile clients
ax = plt.subplot2grid((5, 2), (2, 0), rowspan=2, colspan=1)
ct = ax.contourf(S, 16, extent=[0,1,0,1], origin='lower')
plt.colorbar(ct)
ax.set_xlim(0,1), ax.set_xticks([0,1])
ax.set_ylim(0,1), ax.set_yticks([0,1])
ax.axvline(0.5, color="white", linewidth=0.5, linestyle="--")
ax.axhline(0.5, color="white", linewidth=0.5, linestyle="--")
ax.set_xlabel("Firm B position", labelpad=-10)
ax.set_ylabel("Firm A position", labelpad=-10)
ax.set_title("Volatile clients")
text = ax.text(0.05, 0.95, "C", fontsize=16,  weight="bold",
               color="white", ha="left", va="top", transform=ax.transAxes)
text.set_path_effects([path_effects.Stroke(linewidth=1, foreground='black'),
                       path_effects.Normal()])

# Ghost clients
ax = plt.subplot2grid((5, 2), (2, 1), rowspan=2, colspan=1)
ct = ax.contourf(G, 16, extent=[0,1,0,1], origin='lower')
plt.colorbar(ct)
ax.set_xlim(0,1), ax.set_xticks([0,1])
ax.set_ylim(0,1), ax.set_yticks([0,1])
ax.axvline(0.5, color="white", linewidth=0.5, linestyle="--")
ax.axhline(0.5, color="white", linewidth=0.5, linestyle="--")

ax.set_xlabel("Firm B position", labelpad=-10)
ax.set_ylabel("Firm A position", labelpad=-10)
ax.set_title("Ghost clients")
text = ax.text(0.05, 0.95, "D", fontsize=16,  weight="bold",
               color="white", ha="left", va="top", transform=ax.transAxes)
text.set_path_effects([path_effects.Stroke(linewidth=1, foreground='black'),
                       path_effects.Normal()])

# Client visibility
ax = plt.subplot2grid((5, 2), (4, 0), rowspan=1, colspan=2)
X = np.linspace(0, 1, n_position)
Y = V.sum(axis=0)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.plot(X, Y, color="0.0", linewidth=.5)
for tick in ax.get_xticklabels():
    tick.set_fontsize("small")
for tick in ax.get_yticklabels():
    tick.set_fontsize("small")
ax.set_xticks([0,1])
ax.set_xlabel("Client visibility", labelpad=-10)
text = ax.text(0.0125, 0.95, "E", fontsize=16,  weight="bold",
               color="black", ha="left", va="top", transform=ax.transAxes)

plt.tight_layout()
plt.savefig("figures/hoteling-distribution.pdf")
plt.show()
