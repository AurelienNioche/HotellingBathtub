from pylab import np, plt
import os

folder = "../../doc/draft/fig/a_priori"  # "figures"
os.makedirs(folder, exist_ok=True)

n_positions = 100
mode = "fixed_radius"  # fixed_proportion, fixed_radius


def compute():

    fov = np.arange(0, 1, 1/n_positions)
    pos = np.arange(0, n_positions)

    a = np.zeros((len(fov), len(pos)))

    for f_i, f in enumerate(fov):

        for c in pos:  # For each client

            if mode == "fixed_radius":
                field_of_view = get_field_of_view_with_fixed_radius(c, f)

            else:
                field_of_view = get_field_of_view(c, f)

            for x in pos:  # For each position of the firm
                a[f_i, x] += int(field_of_view[0] <= x <= field_of_view[1])

    return a


def get_field_of_view(x, rel_field_of_view):

    n_seen = int(rel_field_of_view * n_positions)

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


def get_field_of_view_with_fixed_radius(x, rel_field_of_view):

    r = int((rel_field_of_view * n_positions) / 2)

    field_of_view = (
        max(x - r, 0),
        min(x + r, n_positions - 1))

    return field_of_view


def main():

    r = compute()
    fig = plt.Figure(figsize=(8, 6))
    ax = plt.subplot(1, 1, 1, aspect=1/21)
    im = ax.imshow(r, origin="upper", extent=[0, 1, 1, 0], cmap=plt.cm.gray_r)
    plt.colorbar(im)

    ax.set_ylabel("Proportion of beach seen")
    ax.set_xlabel("Position")

    plt.savefig("{}/a_priori_x_vs_r_{}.pdf".format(folder, mode))
    plt.show()


if __name__ == "__main__":

    main()
