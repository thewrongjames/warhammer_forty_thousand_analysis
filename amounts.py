"""
This module provides representations of possibly random quantities,
such as die rolls and fixed values, with methods to get their
average value.
"""


from fractions import Fraction


class SingleAmount:
    """
    The SingleAmount class represents a random quantity that takes
    picks uniformly from a range (i.e, a theoretical die). If the range
    only contains one value, it is just that value. The range includes
    the stop value.
    """
    class InvalidStopError(Exception): pass
    class PointNotInAmountRange(Exception): pass

    def __init__(self, start, stop=None):
        """
        Create an amount object. If stop is None it will just have the
        value at start.
        """
        if stop is not None and stop < start:
            raise InvalidStopError(
                'if stop is set, it must not be smaller that start'
            )

        self.start = Fraction(start)
        self.stop = Fraction(stop if stop is not None else start)

    def get_average_value(self):
        return self.start + ((self.stop - self.start) / 2)

    def get_probability_at_least(self, value_to_be_at_least, rerolling_from=0):
        """
        Get the probability that a 'roll' will be above at least
        value_to_be_at_least, allowing for 'rerolls'. This currently
        only implements rerolling fails, and assumes that rerolls will
        need to get the same value as the initial roll. Values at or
        below rerolling_from are 'rerolled'. Non integer-like values
        may yeild strange results. If rerolling_from is greater than or
        equal to value_to_be_at_least, it will be set to one less than
        value_to_be_at_least.
        """
        if not self.start <= value_to_be_at_least <= self.stop:
            raise SingleAmount.PointNotInAmountRange(
                'both value_to_be_at_least must be at least the start value'\
                ' of the amount, and at most the stop value'
            )
        if not self.start <= rerolling_from + 1:
            raise SingleAmount.PointNotInAmountRange(
                'rerolling_from + 1 must be at least the start of the amount'
            )
        if rerolling_from >= value_to_be_at_least:
            rerolling_from = value_to_be_at_least - 1
        # rerolling_from + 1 is used as we want zero to be a valid value, and
        # it needs to be (at least) 1 smaller than value_to_be_at_least,
        # assuming we are only rerolling fails.

        amount_spread = self.stop - self.start + 1 # +1 as range includes stop.
        fraction_above = (self.stop - value_to_be_at_least + 1) / amount_spread
        # ^ +1 as if it is the value itself it still counts.
        fraction_to_reroll = (rerolling_from + 1 - self.start) / amount_spread
        # ^ +1 as we also reroll the values themselves.

        # probability_above_value = fraction_above + fraction_above *
        #     fraction_to_reroll
        # probability_above_value = fraction_above(1 + fraction_to_reroll)
        return fraction_above * (1 + fraction_to_reroll)

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

    def __abs__(self):
        return self.get_average_value()


class GeneralAmount(SingleAmount):
    """
    The GeneralAmount class represents a possibly random quantity. It
    can be a combination of SingleAmounts (i.e. 2D6). This is what is
    returned by operations on SingleAmounts.
    """
    def __init__(self):
        self._contained_amounts = []

    def add_amount(self, amount):
        self._contained_amounts.append(amount)

    def get_average_value(self):
        return sum(
            [amount.get_average_value() for amount in self._contained_amounts]
        )
