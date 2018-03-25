"""
This module provides representations of possibly random quantities, such as die
rolls and fixed values, with methods to get their average value.
"""


from fractions import Fraction


class SingleAmount:
    """
    The SingleAmount class represents a random quantity that takes picks
    uniformly from a range (i.e, a theoretical die). If the range only contains
    one value, it is just that value. The range includes the stop value.
    """
    def __init__(self, start, stop=None):
        """
        Create an amount object. If stop is None it will just have the
        value at start.
        """
        self.start = Fraction(start)
        self.stop = Fraction(stop if stop is not None else start)

    def get_average_value(self):
        return self.start + ((self.stop - self.start) / 2)

    def get_probability_above(value, re_rolling_at_or_below=0):
        pass

    def __add__(self, other):
        new_general_amount = GeneralAmount()
        new_general_amount.add_amount(self)
        new_general_amount.add_amount(other)
        return new_general_amount

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        new_general_amount = GeneralAmount()
        for _ in range(other):
            new_general_amount.add_amount(self)
        return new_general_amount

    def __rmul__(self, other):
        return self * other


class GeneralAmount(SingleAmount):
    """
    The GeneralAmount class represents a possibly random quantity. It
    can be a combination of SingleAmounts (i.e. 2D6). This is what is returned
    by operations on SingleAmounts.
    """
    def __init__(self):
        self._contained_amounts = []

    def add_amount(self, amount):
        self._contained_amounts.append(amount)

    def get_average_value(self):
        return sum(
            [amount.get_average_value() for amount in self._contained_amounts]
        )
