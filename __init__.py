"""
This package provides tools for analysing particular eigth edition
warhammer forty thousand model loadouts.
"""
from fractions import Fraction

import amounts


D6 = amounts.SingleAmount(1, 6)
D3 = amounts.SingleAmount(1, 3)
ABILITY_ADD_MODIFICATION_NAME = 'add'


class Ability:
    """
    The ability class represents special rules of models, weapons or
    wargear, that modify how they behave.
    """
    MULTIPLY_MODIFICATION_NAME = 'multiply'
    ADD_MODIFICATION_NAME = ABILITY_ADD_MODIFICATION_NAME
    SET_MODIFICATION_NAME = 'set'
    MODIFICATIONS = [
        {'name': MULTIPLY_MODIFICATION_NAME, 'result': lambda x, y: x * y},
        {'name': ADD_MODIFICATION_NAME, 'result': lambda x, y: x + y},
        {'name': SET_MODIFICATION_NAME, 'result': lambda x, y: y},
    ]

    class InvalidModificationTypeError(Exception): pass
    class InvalidRerollsError(Exception): pass

    def __init__(
            self,
            affects_model=True,
            stat_line_changes={},
            modification_type=ABILITY_ADD_MODIFICATION_NAME,
            reroll_hits_at_or_below=0,
            reroll_wounds_at_or_below=0
        ):
        """
        Create an ability object. affects_model determines whether it
        acts on a model or a weapon, stat_line_changes are the changes
        to be made to the stat line, and modification_type is how these
        changes affect the stat line they are modifying. For reroll
        all, the reroll value should just be set to six, as successes
        are not rerolled anyway. The stat line changes default to
        adding.
        """
        if modification_type not in [
                modification['name'] for modification in Ability.MODIFICATIONS
        ]:
            raise InvalidModificationTypeError(
                'modification_type must be one of "multiply", "add" or "set"'
            )

        self.affects_model = affects_model
        self.stat_line_changes = stat_line_changes
        self.modification_type = modification_type
        self.reroll_hits_at_or_below = reroll_hits_at_or_below
        self.reroll_wounds_at_or_below = reroll_wounds_at_or_below


class Item:
    """
    The Item class represents anything in warhammer forty thousand with
    a points cost and a statline (i.e. weapons, models, and other
    wargear).
    """
    class InvalidAbilityError(Exception): pass

    def __init__(self, stat_line, points=0, wargear=[], abilities=[], name=''):
        """
        Create a model object, with the stats in stat_line, and points
        cost in points. The required contents of the statline differs
        depending on the type of item, but it should be indexible.
        Abilities must be an array of ability, or ability like objects.
        """
        self.stat_line = stat_line
        self.points = points
        self.abilities = abilities
        self.wargear = wargear
        self.name = name


class Model(Item):
    """
    The model class represents the warhammer forty thousand rules'
    notion of a model.
    """

    class InvalidModelForEfficiencyError(Exception): pass
    class ZeroToughnessError(Exception): pass

    BALLISTIC_SKILL_STAT_NAME = 'BS'
    WEAPON_SKILL_STAT_NAME = 'WS'
    STRENGTH_STAT_NAME = 'S'
    TOUGHNESS_STAT_NAME = 'T'
    ATTACKS_STAT_NAME = 'A'
    TO_WOUND_ROLL_MODIFIER_STAT_NAME = 'to_wound_roll_modifier'

    def get_wargear_abilities(self):
        wargear_abilities = []
        [wargear_abilities.extend(item.abilities) for item in self.wargear]
        return wargear_abilities

    def get_modified_stat_lines(self, weapon=None):
        """
        Get a tulpe of the stat line of the model and of it's weapon
        (if given) after all the abilities of the wargear and the
        weapon have been applied to them.
        """

        # See, I could do it with list comprehensions if I wanted.
        # wargear_abilities = [
        #     ability for abilities in [item.abilities for item in self.wargear]
        #     for ability in abilities
        # ]
        wargear_abilities = self.get_wargear_abilities()
        weapon_abilities = weapon.abilities if weapon else []

        modified_self_stat_line = self.stat_line.copy()
        modified_self_stat_line[Model.TO_WOUND_ROLL_MODIFIER_STAT_NAME] = 0
        if weapon is None:
            modified_weapon_stat_line = {}
        else:
            modified_weapon_stat_line = weapon.stat_line.copy()

        # Modifiers happen in the order multiply, add, and set, and are
        # then followed by modifiers due to the weapon, as per the
        # designers commentary.

        for current_abilities in (
                self.abilities + wargear_abilities,
                weapon_abilities
        ):
            for modification in Ability.MODIFICATIONS:
                for ability in [
                    ability for ability in current_abilities
                    if ability.modification_type == modification['name']
                ]:
                    if weapon is None and not ability.affects_model:
                        continue
                    stat_line = modified_self_stat_line if \
                        ability.affects_model else modified_weapon_stat_line

                    for key, modifier in ability.stat_line_changes.items():
                        try:
                            stat_line[key] = modification['result'](
                                stat_line[key],
                                ability.stat_line_changes[key]
                            )
                        except KeyError:
                            raise Item.InvalidAbilityError(
                                'ability attempted to modify non-existant stat'
                            )

        return modified_self_stat_line, modified_weapon_stat_line

    @staticmethod
    def get_to_wound_roll(strength, toughness):
        if toughness == 0:
            return 2

        to_wound_ratio = Fraction(strength, toughness)
        if to_wound_ratio >= 2:
            wound_at_or_below = 2
        elif to_wound_ratio <= Fraction(1, 2):
            wound_at_or_below = 6
        elif to_wound_ratio > 1:
            wound_at_or_below = 3
        elif to_wound_ratio < 1:
            wound_at_or_below = 5
        elif to_wound_ratio == 1:
            wound_at_or_below = 4

        return wound_at_or_below

    def get_average_damage_output(self, target, weapon):
        """
        Calculate the average damage output of a particular model with it's
        given wargear, with a particular weapon.
        """

        modified_self_stat_line, modified_weapon_stat_line = \
            self.get_modified_stat_lines(weapon)
        modified_target_stat_line, _ = target.get_modified_stat_lines()

        if weapon.stat_line[Weapon.IS_MELEE_STAT_NAME]:
            unmodified_hit_stat = self.stat_line[Model.WEAPON_SKILL_STAT_NAME]
            modified_hit_stat = modified_self_stat_line[
                Model.WEAPON_SKILL_STAT_NAME
            ]
        else:
            unmodified_hit_stat = self.stat_line[
                Model.BALLISTIC_SKILL_STAT_NAME
            ]
            modified_hit_stat = modified_self_stat_line[
                Model.BALLISTIC_SKILL_STAT_NAME
            ]

        # This assumes only re-rolling successes, and then ensures that the
        # re-rolls happen after modifiers, by only re-rolling what would be
        # below the original hit stat. If the needed to hit roll is improved
        # by modifications, that is okay to, as the get_probability_at_least
        # Amount method will only 'reroll' values below the
        # value_to_be_at_least that it is given. Also, max will error if
        # the iterable it is given is empty, so, if that is the case, we
        # we default to zero.

        all_abilities = (
            self.abilities
            + self.get_wargear_abilities()
            + weapon.abilities
        )

        reroll_hits_at_or_below = min(
            max(
                [ability.reroll_hits_at_or_below for ability in all_abilities]
            ),
            unmodified_hit_stat - 1
        ) if all_abilities else 0

        hit_chance = D6.get_probability_at_least(
            modified_hit_stat,
            reroll_hits_at_or_below
        )

        unmodified_wound_at_or_below = Model.get_to_wound_roll(
            modified_self_stat_line[Model.STRENGTH_STAT_NAME],
            modified_target_stat_line[Model.TOUGHNESS_STAT_NAME]
        )
        # We subtract the to wound roll modifier, as it modifies the roll, the
        # opposite of modifying the required value.
        modified_wound_at_or_below = (
            unmodified_wound_at_or_below - modified_self_stat_line[
                Model.TO_WOUND_ROLL_MODIFIER_STAT_NAME
            ]
        )

        reroll_wounds_at_or_below = min(
            max(
                [
                    ability.reroll_wounds_at_or_below
                    for ability in all_abilities
                ]
            ),
            unmodified_wound_at_or_below - 1
        ) if all_abilities else 0

        wound_chance = D6.get_probability_at_least(
            modified_wound_at_or_below,
            reroll_wounds_at_or_below
        )

        # abs shouldn't change the value of positive integers, but will get the
        # average value if they are amounts.
        attacks = abs(modified_self_stat_line[Model.ATTACKS_STAT_NAME])
        damage = abs(modified_weapon_stat_line[Weapon.DAMAGE_STAT_NAME])

        # TODO:
        # Implement saves.

        return attacks * hit_chance * wound_chance * damage

    def get_average_damage_efficiency(self, target, weapon):
        points_cost = self.points + weapon.points + sum(
            [item.points for item in self.wargear]
        )
        try:
            return (
                self.get_average_damage_output(target, weapon) / points_cost
            )
        except ZeroDivisionError:
            raise InvalidModelForEfficiencyError(
                'zero points cost cannot have an efficiency'
            )


class Weapon(Item):
    """
    The weapon class represents the warhammer forty thousand rules'
    notion of both melee and ranged weapons. In addition to other
    stats, the stat_line passed in should contain an is_melee key,
    containing a boolean representing whether or not it is a melee
    weapon. Weapons should not contain a strength or attacks
    characteristic, they should contain abilities that modify the users
    strength or attacks (including setting it to a desired value).
    """

    IS_MELEE_STAT_NAME = 'is_melee'
    DAMAGE_STAT_NAME = 'D'
