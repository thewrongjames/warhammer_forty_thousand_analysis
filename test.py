from __init__ import Model, Weapon, D6, D3

model = Model({'WS': 4, 'S': 4, 'T': 4, 'A': D3})
weapon = Weapon({'D': D3 + 2 * D6, 'is_melee': True})

print(float(model.get_average_damage_output(model, weapon)))
