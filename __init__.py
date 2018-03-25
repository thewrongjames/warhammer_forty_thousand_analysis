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

    modification_types = (SET, ADD, MULTIPLY)
    reroll_types = (REROLL_HITS, REROLL_WOUNDS)

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
        Create an ability object. affects_model determines whether it acts on a
        model or a weapon, stat_line_changes are the changes to be made to the
        stat line, and modification_type is how these changes affect the stat
        line they are modifying.
        """
        if modification_type not in Ability.modification_types:
            raise InvalidModificationTypeError(
                'modification_type must be one of Ability.SET, Ability.ADD, or'\
                ' Ability.MULTIPLY'
            )

        self.affects_model = affects_model
        self.stat_line_changes = stat_line_changes,
        self.modification_type = modification_type
        self.reroll_hits_at_or_below = reroll_hits_at_or_below
        self.reroll_wounds_at_or_below = reroll_wounds_at_or_below


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

    class InvalidModelForEfficiencyError(Exception): pass

    BALLISTIC_SKILL_STAT_NAME = 'bs'
    WEAPON_SKILL_STAT_NAME = 'ws'

    def get_average_damage_output(self, target, weapon, wargear):
        abilities = self.abilities + wargear.abilities + weapon.abilities
        reroll_hits_at_or_below = max(
            [ability.reroll_hits_at_or_below for ability in abilities]
        )
        reroll_wounds_at_or_below = max(
            [ability.reroll_wounds_at_or_below for ability in abilities]
        )

        modified_self = Model(self.stat_line, 0, [])
        modified_weapon = Weapon(weapon.stat_line, 0, [])

        if weapon.stat_line[WEAPON.IS_MELEE_STAT_NAME]:
            hit_stat = self.stat_line[Model.WEAPON_SKILL_STAT_NAME]
        else:
            hit_stat = self.stat_line[Model.BALLISTIC_SKILL_STAT_NAME]

        # TODO:
        # Incorporate rerolls before modifiers here.
        hit_chance = D_SIX.get_probability_at_least(hit_stat)

        # Assumes add / subtract, multiply, set, order of operations for
        # modifiers

    def get_average_damage_efficiency(self, target, weapon, wargear):
        try:
            return self.get_damage_output(target, weapon, wargear) / self.points
        except ZeroDivisionError:
            raise InvalidModelForEfficiencyError(
                'models with zero points cost cannot have an efficiency'
            )


class Weapon(Item):
    """
    The weapon class represents the warhammer forty thousand rules' notion of
    both melee and ranged weapons. In addition to other stats, the stat_line
    passed in should contain an is_melee key, containing a boolean representing
    whether or not it is a melee weapon. Weapons should not contain a strength
    characteristic, they should contain abilities that modify the users strength
    (including setting it to a desired value).
    """

    IS_MELEE_STAT_NAME = 'is_melee'
