from __init__ import Model, Weapon, Ability, D6, D3


toughnesses_one_to_ten = [Model({'T': t}) for t in range(1, 11)]
space_marine_veteran_stat_line = {'WS': 4, 'S': 4, 'A': 2}


chainsword = Weapon(
    {'D': 1, 'AP': 0, 'is_melee': True},
    abilities=[Ability(stat_line_changes={'A': 1})],
    name='chainsword',
    points=0
)
lightning_claw = Weapon(
    {'D': 1, 'AP': -2, 'is_melee': True},
    abilities=[Ability(reroll_wounds_at_or_below=6)],
    name='lightning_claw',
    points=8
)
power_axe = Weapon(
    {'D': 1, 'AP': -2, 'is_melee': True},
    abilities=[Ability(stat_line_changes={'S': 1})],
    name='power_axe',
    points=5
)
power_fist = Weapon(
    {'D': D3, 'AP': -3, 'is_melee': True},
    abilities=[
        Ability(
            stat_line_changes={'S': 2},
            modification_type=Ability.MULTIPLY_MODIFICATION_NAME
        ),
        Ability(
            stat_line_changes={'WS': -1},
            modification_type=Ability.ADD_MODIFICATION_NAME
        )
    ],
    name='power_fist',
    points=12
)
power_maul_or_power_lance = Weapon(
    {'D': 1, 'AP': -1, 'is_melee': True},
    abilities=[
        Ability(
            stat_line_changes={'S': 2}
        )
    ],
    name='power_maul_or_power_lance',
    points=4
)
power_sword = Weapon(
    {'D': 1, 'AP': -3, 'is_melee': True},
    name='power_sword',
    points=4
)
thunder_hammer = Weapon(
    {'D': 3, 'AP': -3, 'is_melee': True},
    abilities=[
        Ability(
            stat_line_changes={'S': 2},
            modification_type=Ability.MULTIPLY_MODIFICATION_NAME
        ),
        Ability(
            stat_line_changes={'WS': -1},
            modification_type=Ability.ADD_MODIFICATION_NAME
        )
    ],
    name='thunder_hammer',
    points=16
)
two_chainswords = Weapon(
    {'D': 1, 'AP': 0, 'is_melee': True},
    abilities=[Ability(stat_line_changes={'A': 2})],
    name='two_chainswords',
    points=0
)
two_lightning_claws = Weapon(
    {'D': 1, 'AP': -2, 'is_melee': True},
    abilities=[
        Ability(stat_line_changes={'A': 1}, reroll_wounds_at_or_below=6)
    ],
    name='two_lightning_claws',
    points=12
)


weapons = [
    chainsword, lightning_claw, power_axe, power_fist,
    power_maul_or_power_lance, power_sword, thunder_hammer, two_chainswords,
    two_lightning_claws
]


model = Model(space_marine_veteran_stat_line, points=18)
for one_less_than_toughness, target in enumerate(toughnesses_one_to_ten):
    toughness = one_less_than_toughness + 1
    print(toughness)
    results = [
        (weapon.name, model.get_average_damage_efficiency(target, weapon))
        for weapon in weapons
    ]
    results.sort(key=lambda name_and_output: name_and_output[1], reverse=True)
    for result in results:
        print(f'{result[0]}: {float(result[1])}')
    print()
