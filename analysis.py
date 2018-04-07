from copy import copy
from __init__ import Model, Weapon, Ability, D6, D3


targets = {}
for wounds in range(1, 7):
    for toughness in range(1, 11):
        for save in range(2, 7):
            targets[(wounds, toughness, save)] = (
                Model({'W': wounds, 'T': toughness, 'Sv': save})
            )
space_marine_veteran_stat_line = {'BS': 3, 'WS': 3, 'S': 4, 'A': 2, 'Sv': 3}
space_marine_stat_line = {'BS': 3, 'WS': 3, 'S': 4, 'A': 1, 'Sv': 3}
inceptor_stat_line = {'BS': 3, 'WS': 3, 'S': 4, 'A': 2, 'Sv': 3}
dreadnaught_stat_line = {'BS': 3, 'WS': 3, 'S': 6, 'A': 4, 'Sv': 3}
ironclad_dreadnaught_stat_line = {'BS': 3, 'WS': 3, 'S': 6, 'A': 4, 'Sv': 3}
venerable_dreadnaught_stat_line = {'BS': 2, 'WS': 2, 'S': 6, 'A': 4, 'Sv': 3}


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
boltgun_in_rapid_fire_range = Weapon(
    {'D': 1, 'AP': 0, 'is_melee': False},
    name='boltgun_in_rapid_fire_range',
    abilities=[
        Ability(
            stat_line_changes={'A': 2, 'S': 4},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ]
)
frag_grenade = Weapon(
    {'D': 1, 'AP': 0, 'is_melee': False},
    name='frag_grenade',
    abilities=[
        Ability(
            stat_line_changes={'A': D6, 'S': 3},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ]
)
krak_grenade = Weapon(
    {'D': D3, 'AP': -1, 'is_melee': False},
    name='krak_grenade',
    abilities=[
        Ability(
            stat_line_changes={'A': 1, 'S': 6},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ]
)
heavy_bolter = Weapon(
    {'D': 1, 'AP': -1, 'is_melee': False},
    name='heavy_bolter',
    abilities=[
        Ability(
            stat_line_changes={'A': 1, 'S': 5},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=10
)
lascannon = Weapon(
    {'D': D6, 'AP': -3, 'is_melee': False},
    name='lascannon',
    abilities=[
        Ability(
            stat_line_changes={'A': 1, 'S': 9},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=25
)
lascannon_rerolling_ones_and_twos_one_quarter_of_the_time = Weapon(
    {'D': 3.5 + ((4.1666666 - 3.5) / 4), 'AP': -3, 'is_melee': False},
    name='lascannon_rerolling_ones_and_twos_one_quarter_of_the_time',
    abilities=[
        Ability(
            stat_line_changes={'A': 1, 'S': 9},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=25
)
missile_launcher_krak_missile = Weapon(
    {'D': D6, 'AP': -2, 'is_melee': False},
    name='missile_launcher_krak_missile',
    abilities=[
        Ability(
            stat_line_changes={'A': 1, 'S': 8},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=25
)
missile_launcher_frag_missile = Weapon(
    {'D': 1, 'AP': 0, 'is_melee': False},
    name='missile_launcher_frag_missile',
    abilities=[
        Ability(
            stat_line_changes={'A': D6, 'S': 4},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=25
)
multimelta = Weapon(
    {'D': D6, 'AP': -4, 'is_melee': False},
    name='multimelta',
    abilities=[
        Ability(
            stat_line_changes={'A': 1, 'S': 8},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=27
)
plasma_cannon_not_overcharged = Weapon(
    {'D': 1, 'AP': -3, 'is_melee': False},
    name='plasma_cannon_not_overcharged',
    abilities=[
        Ability(
            stat_line_changes={'A': D3, 'S': 7},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=21
)
plasma_cannon_overcharged = Weapon(
    {'D': 2, 'AP': -3, 'is_melee': False},
    name='plasma_cannon_overcharged',
    abilities=[
        Ability(
            stat_line_changes={'A': D3, 'S': 8},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=21 + ((2/6) * (13 + 21))
)
plasma_cannon_overcharged_with_captain = copy(plasma_cannon_overcharged)
plasma_cannon_overcharged_with_captain.points = 21 + ((2/36) * (13 + 21))
assault_bolter = Weapon(
    {'D': 1, 'AP': -1, 'is_melee': False},
    name='assault_bolter',
    abilities=[
        Ability(
            stat_line_changes={'A': 3, 'S': 5},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=10
)
plasma_exterminator_not_overcharged = Weapon(
    {'D': 1, 'AP': -3, 'is_melee': False},
    name='plasma_exterminator_not_overcharged',
    abilities=[
        Ability(
            stat_line_changes={'A': D3, 'S': 7},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=17
)
plasma_exterminator_overcharged = Weapon(
    {'D': 2, 'AP': -3, 'is_melee': False},
    name='plasma_exterminator_overcharged',
    abilities=[
        Ability(
            stat_line_changes={'A': D3, 'S': 8},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=17 + ((2/6) * (25 + 17))
)
assault_cannon = Weapon(
    {'D': 1, 'AP': -1, 'is_melee': False},
    name='assault_cannon',
    abilities=[
        Ability(
            stat_line_changes={'A': 6, 'S': 8},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=22
)
heavy_plasma_cannon_not_overcharged = Weapon(
    {'D': 1, 'AP': -3, 'is_melee': False},
    name='plasma_cannon_not_overcharged',
    abilities=[
        Ability(
            stat_line_changes={'A': D3, 'S': 7},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=30
)
heavy_plasma_cannon_overcharged = Weapon(
    {'D': 2, 'AP': -3, 'is_melee': False},
    name='plasma_cannon_overcharged',
    abilities=[
        Ability(
            stat_line_changes={'A': D3, 'S': 8},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=30 + ((1/6)*(1/8)*90)
)
twin_lascannon = Weapon(
    {'D': D6, 'AP': -3, 'is_melee': False},
    name='lascannon',
    abilities=[
        Ability(
            stat_line_changes={'A': 2, 'S': 9},
            modification_type=Ability.SET_MODIFICATION_NAME
        )
    ],
    points=50
)


vanguard_veteran_weapon_combinations = [
    [chainsword],
    [lightning_claw],
    [power_axe],
    [power_fist],
    [power_maul_or_power_lance],
    [power_sword],
    [thunder_hammer],
    [two_chainswords],
    [two_lightning_claws]
]
space_marine_veteran = Model(
    space_marine_veteran_stat_line,
    points=18,
    name='space_marine_veteran'
)
devastator_weapon_combinations = [
    [heavy_bolter],
    [lascannon],
    [missile_launcher_krak_missile],
    [missile_launcher_frag_missile],
    #[multimelta],
    [plasma_cannon_not_overcharged],
    [plasma_cannon_overcharged],
    #[lascannon_rerolling_ones_and_twos_one_quarter_of_the_time]
]
heavy_weapon_devastator = Model(
    space_marine_stat_line,
    points=13 + ((1/4)*13*2),
    name='heavy_weapon_devastator'
)
devastator_with_captain_weapon_combinations = copy(
    devastator_weapon_combinations
)
devastator_with_captain_weapon_combinations.remove(
    [plasma_cannon_overcharged]
)
devastator_with_captain_weapon_combinations.append(
    [plasma_cannon_overcharged_with_captain]
)
heavy_weapon_devastator_with_captain = Model(
    space_marine_stat_line,
    points=13 + ((1/4)*13*2) + ((1/8)*77),
    name='heavy_weapon_devastator_with_captain',
    abilities=[Ability(reroll_hits_at_or_below=1)]
)
inceptor_weapon_combinations = [
    [assault_bolter],
    [plasma_exterminator_not_overcharged],
    [plasma_exterminator_overcharged]
]
inceptor = Model(
    inceptor_stat_line,
    points=25,
    name='inceptor'
)
dreadnaught_heavy_weapons = [
    assault_cannon,
    heavy_plasma_cannon_not_overcharged,
    heavy_plasma_cannon_overcharged,
    multimelta,
    twin_lascannon
]
ranged_dreadnaught_weapon_combinations = [
    [first_weapon, missile_launcher]
    for first_weapon in dreadnaught_heavy_weapons
    for missile_launcher in (
        missile_launcher_frag_missile,
        missile_launcher_krak_missile
    )
]
dreadnaught = Model(
    dreadnaught_stat_line,
    points=70,
    name='dreadnaught'
)
venerable_dreadnaught = Model(
    venerable_dreadnaught_stat_line,
    points=90,
    name='venerable_dreadnaught'
)


options = [
    (space_marine_veteran, vanguard_veteran_weapon_combinations),
    (heavy_weapon_devastator, devastator_weapon_combinations),
    (inceptor, inceptor_weapon_combinations),
    (
        heavy_weapon_devastator_with_captain,
        devastator_with_captain_weapon_combinations
    ),
    (dreadnaught, ranged_dreadnaught_weapon_combinations),
    (venerable_dreadnaught, ranged_dreadnaught_weapon_combinations),
]


results = []
for wounds, toughness, save in sorted(targets.keys()):
    target = targets[(wounds, toughness, save)]
    for model, weapon_combinations in options:
        for weapon_combination in weapon_combinations:
            result = float(
                model.get_average_damage_efficiency(target, weapon_combination)
            )
            weapon_names = [weapon.name for weapon in weapon_combination]
            name = f'{model.name} with {", ".join(weapon_names)}'
            results.append((wounds, toughness, save, name, result))


output = ''
already_done_wounds_toughness_saves = []
results.sort(key=lambda result: (result[0], result[1], -result[2], -result[4]))
for wounds, toughness, save, weapon_name, result in results:
    if already_done_wounds_toughness_saves.count((wounds, toughness, save)) \
            < 1:
        output += (
            f'W: {wounds}, T: {toughness}, Sv: {save} - {weapon_name} '
            f'{result}\n'
        )
    already_done_wounds_toughness_saves.append((wounds, toughness, save))

with open('best.txt', 'w') as output_file:
    output_file.write(output)
