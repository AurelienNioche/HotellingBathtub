from pylab import np, plt
import itertools as it

n_positions = 100
fov = 0.5

cond = "see_firm_1"  # see_firm_1, see_both
mode = "fixed_proportion"  # fixed_proportion, fixed_radius


def compute():
    pos = np.arange(0, n_positions)

    a = np.zeros((len(pos), len(pos)))

    b = np.zeros((len(pos), len(pos)), dtype=list)
    for x1, x2 in it.product(pos, repeat=2):
        b[x1, x2] = list()

    for c in pos:  # For each client

        print("Customer", c)

        if mode == "fixed_radius":
            field_of_view = get_field_of_view_with_fixed_radius(c)

        else:
            field_of_view = get_field_of_view(c)

        print("Field of view", field_of_view)

        for x1, x2 in it.product(pos, repeat=2):

            see_firm_1 = field_of_view[0] <= x1 <= field_of_view[1]
            see_firm_2 = field_of_view[0] <= x2 <= field_of_view[1]

            if cond == "see_both" and see_firm_1 and see_firm_2:
                a[x1, x2] += 1
                b[x1, x2].append(c)

            if cond == "see_firm_1" and see_firm_1 and not see_firm_2:
                a[x1, x2] += 1

            if cond == "see_firm_2" and not see_firm_1 and see_firm_2:
                a[x1, x2] += 1

    # for i in np.arange(n_positions - 1, -1, -1):
    #     print(i, [j for j in b[i]])
    return a


def get_field_of_view(x):

    n_seen = round(fov * n_positions)

    field_of_view = [x, x]

    n = n_seen - 1  # Customer already sees its own position

    left = np.random.choice([True, False])

    for i in range(n):

        if left:  # Extent on the left

            if field_of_view[0] - 1 >= 0:
                field_of_view[0] -= 1

            else:
                field_of_view[1] += 1

        else:  # Extent on the right

            if field_of_view[1] + 1 < n_positions:
                field_of_view[1] += 1

            else:
                field_of_view[0] -= 1

        left = np.invert(left)  # Begin by the other side at the next iteration

    return field_of_view


def get_field_of_view_with_fixed_radius(x):

    r = int((fov * n_positions) / 2)

    field_of_view = (
        max(x - r, 0),
        min(x + r, n_positions - 1))

    return field_of_view


def main():
    r = compute()
    fig = plt.Figure(figsize=(8, 6))
    ax = plt.subplot(1, 1, 1, aspect=1/21)
    im = ax.imshow(r, origin="lower", extent=[0, 1, 0, 1], cmap=plt.cm.gray_r)
    plt.colorbar(im)
    plt.title(cond.replace("_", " ").capitalize() +
              ", p={}, mode='{}'".format(fov, mode.replace("_", " ")))

    ax.set_xlabel("x2")
    ax.set_ylabel("x1")
    plt.savefig("../data/figures/a_priori_x_vs_x_{}_{}_{}.pdf".format(cond, fov*100, mode))
    plt.show()


if __name__ == "__main__":
    main()
