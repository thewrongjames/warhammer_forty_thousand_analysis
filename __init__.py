"""
This package provides tools for analysing particular eigth edition
warhammer forty thousand model loadouts.
"""
import operator
import amounts


D6 = amounts.SingleAmount(1, 6)
D3 = amounts.SingleAmount(1, 3)
TWO_D6 = 2 * D6


class Ability:
    """
    The ability class represents special rules of models, weapons or
    wargear, that modify how they behave.
    """
    MODIFICATIONS = [
        {'name': 'multiply', 'result': operator.mul},
        {'name': 'add', 'result': operator.add},
        {'name': 'set', 'result': lambda x, y: y},
    ]

    class InvalidModificationTypeError(Exception): pass
    class InvalidRerollsError(Exception): pass

    def __init__(
            self,
            affects_model,
            stat_line_changes,
            modification_type,
            reroll_hits_at_or_below=0,
            reroll_wounds_at_or_below=0
        ):
        """
        Create an ability object. affects_model determines whether it
        acts on a model or a weapon, stat_line_changes are the changes
        to be made to the stat line, and modification_type is how these
        changes affect the stat line they are modifying. For reroll
        all, the reroll value should just be set to six, as successes
        are not rerolled anyway.
        """
        if modification_type not in [
                modification['name'] for modification in Ability.MODIFICATIONS
        ]:
            raise InvalidModificationTypeError(
                'modification_type must be one of "multiply", "add" or "set"'
            )

        self.affects_model = affects_model
        self.stat_line_changes = stat_line_changes,
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

    def __init__(self, stat_line, points=0, abilities=[]):
        """
        Create a model object, with the stats in stat_line, and points
        cost in points. The required contents of the statline differs
        depending on the type of item, but it should be indexible.
        Abilities must be an array of ability, or ability like objects.
        """
        self.stat_line = stat_line
        self.points = points
        self.abilities = abilities


class Model(Item):
    """
    The model class represents the warhammer forty thousand rules'
    notion of a model.
    """

    class InvalidModelForEfficiencyError(Exception): pass

    BALLISTIC_SKILL_STAT_NAME = 'bs'
    WEAPON_SKILL_STAT_NAME = 'ws'
    STRENGTH_STAT_NAME = 's'

    def get_average_damage_output(self, target, weapon, wargear):
        abilities = self.abilities + wargear.abilities + weapon.abilities

        modified_self_stat_line = self.stat_line.copy()
        modified_weapon_stat_line = weapon.stat_line.copy()

        # Modifiers happen in the order multiply, add, and set, and are then
        # followed by modifiers due to the weapon, as per designers commentary.

        for current_abilities in (
                self.abilities + wargear.abilities,
                weapon.abilities
        ):
            for modifications in Ability.MODIFICATIONS:
                for ability in [
                    ability for ability in current_abilities
                    if ability.modification_type == modification_type
                ]:
                    stat_line = modified_self_stat_line if \
                        ability.affects_model else modified_weapon_stat_line
                    for key, modifier in ability.stat_line.items():
                        try:
                            stat_line[key] = modification.result(
                                stat_line[key],
                                ability.stat_line[key]
                            )
                        except KeyError:
                            raise Item.InvalidAbilityError(
                                'ability attempted to modify non-existant stat'
                            )

        modified_self = Model(modified_self_stat_line)
        modified_weapon = Weapon(modified_weapon_stat_line)

        if weapon.stat_line[WEAPON.IS_MELEE_STAT_NAME]:
            unmodified_hit_stat = self.stat_line[Model.WEAPON_SKILL_STAT_NAME]
            modified_hit_stat = modified_self.stat_line[
                Model.WEAPON_SKILL_STAT_NAME
            ]
        else:
            unmodified_hit_stat = self.stat_line[
                Model.BALLISTIC_SKILL_STAT_NAME
            ]
            modified_hit_stat = modified_self.stat_line[
                Model.BALLISTIC_SKILL_STAT_NAME
            ]

        reroll_hits_at_or_below = min(
            max(
                [ability.reroll_hits_at_or_below for ability in abilities]
            ),
            unmodified_hit_stat - 1
        )
        reroll_wounds_at_or_below = max(
            [ability.reroll_wounds_at_or_below for ability in abilities]
        )

        hit_chance = D_SIX.get_probability_at_least(
            hit_stat,
            reroll_hits_at_or_below
        )

    def get_average_damage_efficiency(self, target, weapon, wargear):
        try:
            return (
                self.get_damage_output(target, weapon, wargear) / self.points
            )
        except ZeroDivisionError:
            raise InvalidModelForEfficiencyError(
                'models with zero points cost cannot have an efficiency'
            )


class Weapon(Item):
    """
    The weapon class represents the warhammer forty thousand rules'
    notion of both melee and ranged weapons. In addition to other
    stats, the stat_line passed in should contain an is_melee key,
    containing a boolean representing whether or not it is a melee
    weapon. Weapons should not contain a strength characteristic, they
    should contain abilities that modify the users strength (including
    setting it to a desired value).
    """

    IS_MELEE_STAT_NAME = 'is_melee'
