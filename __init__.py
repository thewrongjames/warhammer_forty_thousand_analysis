"""
This package provides tools for analysing particular eigth edition warhammer
forty thousand model loadouts.
"""


class SingleAmount:
    """
    The SingleAmount class represents a random quantity that takes picks
    uniformly from a range (i.e, a theoretical die). If the range only contains
    one value, it is just that value. The range includes the stop value.
    """
    def __init__(self, start, stop=none):
        """
        Create an amount object. If stop is none it will just have the
        value at start.
        """
        self.start = start
        self.stop = stop if stop is not none else start

    def get_average_value(self):
        return self.start + ((self.stop - self.start) / 2)

    def __add__(self, other):
        new_general_amount = GeneralAmount()
        new_general_amount.add_amount(self)
        new_general_amount.add_amount(other)
        return new_general_amount

    def __mul__(self, other):
        new_general_amount = GeneralAmount()
        for _ in range(other):
            new_general_amount.add_amount(self)
        return new_general_amount


class GeneralAmount(SingleAmount):
    """
    The GeneralAmount class represents a possibly random quantity. It
    can be a combination of SingleAmounts (i.e. 2D6).
    """
    def __init__(self):
        self._contained_amounts = []

    def add_amount(self, amount):
        self._contained_amounts.append(amounts)

    def get_average_value(self):
        return sum(
            self._contained_amounts,
            lambda amount: amount.get_average_value()
        )


class Ability:
    """
    The ability class represents special rules of models, weapons or wargear,
    that modify how they behave.
    """
    SET = object()
    ADD = object()
    MULTIPLY = object()
    modification_types = (SET, ADD, MULTIPLY)
    class InvalidModificationTypeError(Exception): pass

    def __init__(
            self,
            affects_model,
            stat_line_changes,
            modification_type
        ):
        """
        Create an ability object. affects_model determines whether it acts of a
        model of a weapon, stat_line_changes are the changes to be made to the
        stat line, and modification_type is how these changes affect the stat
        line they are modifying.
        """
        if modification_type not in Ability.modification_types:
            raise InvalidModificationTypeError(
                'modification_type must be one of Ability.SET, Ability.ADD, or'\
                'Ability.MULTIPLY'
            )
        self.affects_model = affects_model
        self.stat_line_chanes = stat_line_changes,
        self.modification_type = modification_type


class Item:
    """
    The Item class represents anything in warhammer forty thousand with a
    points cost and a statline (i.e. weapons and models).
    """
    def __init__(self, stat_line, points, abilities):
        """
        Create a model object, with the stats in stat_line, and points cost in
        points. The required contents of the statline differs depending on the
        type of item, but it should be indexible. Abilities must be an array of
        ability, or ability like objects.
        """
        self.stat_line = stat_line
        self.points = points
        self.abilities = abilities


class Model(Item):
    """
    The model class represents the warhammer forty thousand rules' notion of a
    model.
    """

    def get_damage_output(target, weapon, wargear):
        pass

    def get_damage_efficiency(target, weapon, wargear):
        pass


class Weapon(Item):
    """
    The weapon class represents the warhammer forty thousand rules' notion of
    both melee and ranged weapons.
    """
