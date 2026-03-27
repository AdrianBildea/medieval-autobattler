import random

ITEM_TEMPLATES = {
    'Sword':       {'stat': 'attack',        'value': 10,   'rarity': 'Common'},
    'Great Sword': {'stat': 'attack',        'value': 20,   'rarity': 'Rare'},
    'Armor':       {'stat': 'max_health',    'value': 20,   'rarity': 'Common'},
    'Plate Mail':  {'stat': 'max_health',    'value': 50,   'rarity': 'Epic'},
    'Ring':        {'stat': 'ability_power', 'value': 10,   'rarity': 'Rare'},
    'Amulet':      {'stat': 'defense',       'value': 8,    'rarity': 'Common'},
    'Boots':       {'stat': 'attack_speed',  'value': 0.2,  'rarity': 'Rare'},
    'Crown':       {'stat': 'crit_chance',   'value': 0.15, 'rarity': 'Legendary'},
}

RARITY_MULTIPLIER = {'Common': 1.0, 'Rare': 1.5, 'Epic': 2.0, 'Legendary': 3.0}

class Item:
    def __init__(self, name):
        template = ITEM_TEMPLATES[name]
        self.name = name
        self.stat = template['stat']
        self.rarity = template['rarity']
        self.value = round(template['value'] * RARITY_MULTIPLIER[self.rarity], 2)

    def apply(self, unit):
        old = getattr(unit, self.stat, 0)
        setattr(unit, self.stat, old + self.value)
        if self.stat == 'max_health':
            unit.health = min(unit.health + int(self.value), unit.max_health)
        print(f"    {unit.name} equipped {self.name} (+{self.value} {self.stat})")

    def remove(self, unit):
        old = getattr(unit, self.stat, 0)
        setattr(unit, self.stat, max(0, old - self.value))

    def __repr__(self):
        return f"{self.name} [{self.rarity}] +{self.value} {self.stat}"


class Inventory:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)
        print(f"  Item added to inventory: {item}")

    def equip(self, item_index, unit):
        if item_index >= len(self.items):
            print('Invalid item index.')
            return
        item = self.items.pop(item_index)
        if not hasattr(unit, 'equipment'):
            unit.equipment = []
        unit.equipment.append(item)
        item.apply(unit)

    def display(self):
        if not self.items:
            print('  Inventory is empty.')
            return
        print('  -- Inventory --')
        for i, item in enumerate(self.items):
            print(f'    [{i}] {item}')

    def random_drop(self):
        name = random.choice(list(ITEM_TEMPLATES.keys()))
        item = Item(name)
        self.add(item)
        return item
