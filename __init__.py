"""
This package provides tools for analysing particular eigth edition warhammer
forty thousand model loadouts.
"""
import amounts


D_SIX = amounts.SingleAmount(1, 6)
D_THREE = amounts.SingleAmount(1, 3)
TWO_D_SIX = 2 * D_SIX


class Ability:
    """
    The ability class represents special rules of models, weapons or wargear,
    that modify how they behave.
    """
    MULTIPLY = object()
    ADD = object()
    SET = object()
    RE_ROLL_HITS = object()
    RE_ROLL_WOUNDS = object()

    modification_types = (SET, ADD, MULTIPLY)
    re_roll_types = (RE_ROLL_HITS, RE_ROLL_WOUNDS)

    class InvalidModificationTypeError(Exception): pass
    class InvalidRerollsError(Exception): pass

    def __init__(
            self,
            affects_model,
            stat_line_changes,
            modification_type,
            re_rolls=[]
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
                ' Ability.MULTIPLY'
            )
        try:
            if False in [
                    re_roll in Ability.re_roll_types for re_roll in re_rolls
            ]:
                raise InvalidRerollsError(
                    'one or more of the values in re_rolls was not valid; each'\
                    ' re_roll must be one of Ability.RE_ROLL_HITS or '\
                    'Ability.RE_ROLL_WOUNDS'
                )
        except TypeError:
            raise InvalidRerollsError('re_rolls must be iterable')

        self.affects_model = affects_model
        self.stat_line_chanes = stat_line_changes,
        self.modification_type = modification_type
        self.re_rolls = re_rolls


class Item:
    """
    The Item class represents anything in warhammer forty thousand with a
    points cost and a statline (i.e. weapons, models, and other wargear).
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

    BALLISTIC_SKILL_STAT_NAME = 'bs'
    WEAPON_SKILL_STAT_NAME = 'ws'

    def get_average_damage_output(self, target, weapon, wargear):
        pass

    def get_average_damage_efficiency(self, target, weapon, wargear):
        return self.get_damage_output(target, weapon, wargear) / self.points


class Weapon(Item):
    """
    The weapon class represents the warhammer forty thousand rules' notion of
    both melee and ranged weapons. In addition to other stats, the stat_line
    passed in should contain an is_melee key, containing a boolean representing
    whether or not it is a melee weapon.
    """

    IS_MELEE_STAT_NAME = 'is_melee'
