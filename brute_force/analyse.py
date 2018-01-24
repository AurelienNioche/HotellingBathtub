import numpy as np
import pickle
import os
from pylab import plt

from scipy.optimize import least_squares


def model(x, u):
    return x[0] * (u ** 2 + x[1] * u) / (u ** 2 + x[2] * u + x[3])


def fun(x, u, y):
    return model(x, u) - y


def add_fitting_curve(ax, x, y):

    order = np.argsort(x)

    xdata = x[order]
    ydata = y[order]

    x0 = np.zeros(4)

    res = least_squares(fun, x0, bounds=(-2, 200), args=(xdata, ydata), verbose=1).x

    u_test = np.linspace(0, 1)
    ax.plot(u_test, model(res, u_test), '--', zorder=-10, color="black")


def plot(results, path=os.path.expanduser("~/Desktop/results.pdf")):

    x = results[:, 0]
    y = results[:, 1]

    fig = plt.figure(figsize=(10, 6))
    ax = plt.subplot()

    ax.scatter(x, y, color='black', alpha=0.25)
    ax.set_xlabel("$r$")
    ax.set_ylabel("Diff of profits between $h_0$ and $h_1$")
    ax.set_title("Does strategic depth impact profits?")

    add_fitting_curve(ax, x, y)

    plt.tight_layout()

    plt.savefig(path)
    plt.show()


def load(path=os.path.expanduser("~/Desktop/results.p")):

    with open(path, "rb") as f:
        return pickle.load(f)


def main():

    results = load()
    plot(results)


if __name__ == "__main__":
    main()
