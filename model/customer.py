import numpy as np


import parameters


class Customer:

    def __init__(self, x, field_of_view):

        self.x = x
        self.rel_field_of_view = field_of_view

        self.abs_field_of_view = self._what_is_seen()

    def get_field_of_view(self):
        return self.abs_field_of_view

    @classmethod
    def get_firm_choice(cls, firms_idx, prices):
        """choice function"""

        consume = len(prices) > 0

        if consume:
            price = min(prices)  # Choose minimum price
            firm_choice = np.random.choice(firms_idx[prices == price])

        else:
            firm_choice = -1

        return firm_choice

    def _get_field_of_view_with_fixed_p(self):

        n_seen = int(self.rel_field_of_view * parameters.n_positions)

        field_of_view = [self.x, self.x]

        n = n_seen - 1  # Customer already sees its own position

        left = np.random.choice([True, False])

        for i in range(n):

            if left:  # Extent on the left

                if field_of_view[0] - 1 >= 0:
                    field_of_view[0] -= 1

                else:
                    field_of_view[1] += 1

            else:  # Extent on the right

                if field_of_view[1] + 1 < parameters.n_positions:
                    field_of_view[1] += 1

                else:
                    field_of_view[0] -= 1

            left = np.invert(left)  # Begin by the other side at the next iteration

        return field_of_view

    def _get_field_of_view_with_fixed_r(self):

        r = int((self.rel_field_of_view * parameters.n_positions) / 2)

        field_of_view = (
            max(self.x - r, 0),
            min(self.x + r, parameters.n_positions-1))

        return field_of_view

    def _what_is_seen(self):

        if parameters.mode == "p_fixed":
            field_of_view = self._get_field_of_view_with_fixed_p()

        elif parameters.mode == "r_fixed":
            field_of_view = self._get_field_of_view_with_fixed_r()

        else:
            raise ValueError("'mode' in parameters contains a misspelling.")

        return field_of_view
