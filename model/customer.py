import numpy as np


import parameters


class Customer:

    def __init__(self, x, parameter_field_of_view):

        self.x = x
        self.parameter_field_of_view = parameter_field_of_view

        # self.firm_choice = None
        # self.utility = None
        self.field_of_view = self._what_is_seen()

    def get_field_of_view(self):
        return self.field_of_view

    @classmethod
    def get_firm_choice(cls, firms_idx, prices):
        """choice function"""

        consume = len(prices) > 0

        if consume:
            price = min(prices)  # Choose minimum price
            firm_choice = np.random.choice(firms_idx[prices == price])

        else:
            # price = 0
            firm_choice = -1

        # exploration_cost = self.t_cost * self.extra_view
        # self.utility = int(consume) * self.u_consumption - (exploration_cost + price)

        return firm_choice

    def _get_field_of_view_with_fixed_p(self):

        n_seen = int(self.parameter_field_of_view * parameters.n_positions)

        left = np.random.choice((True, False))
        field_of_view = [self.x, self.x]
        for i in range(n_seen - 1):  # Customer already sees its own position
            if left:
                if field_of_view[0] - 1 > 0:
                    field_of_view[0] -= 1
                else:
                    field_of_view[1] += 1
            else:
                if field_of_view[1] + 1 < parameters.n_positions:
                    field_of_view[1] += 1
                else:
                    field_of_view[0] -= 1

        return field_of_view

    def _get_field_of_view_with_fixed_r(self):

        r = int((self.parameter_field_of_view * parameters.n_positions / 2))

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

