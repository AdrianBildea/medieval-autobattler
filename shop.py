import random

UNIT_POOL = {
    'Common':    {'cost': 1,  'units': ['Knight', 'Archer']},
    'Rare':      {'cost': 3,  'units': ['FireMage']},
    'Epic':      {'cost': 5,  'units': ['Priest']},
    'Legendary': {'cost': 8,  'units': []},
}

REFRESH_COST = 2

class Shop:
    def __init__(self, profile=None):
        self.profile = profile
        self.stock = []
        self.refresh(free=True)

    def refresh(self, free=False):
        if not free:
            if self.profile:
                if not self.profile.spend_gold(REFRESH_COST):
                    return
            else:
                print('  Refresh costs 2 gold.')
                return
        self.stock = []
        rarities = (['Common'] * 5) + (['Rare'] * 3) + (['Epic'] * 1)
        for _ in range(5):
            rarity = random.choice(rarities)
            unit_name = random.choice(UNIT_POOL[rarity]['units']) if UNIT_POOL[rarity]['units'] else None
            if unit_name:
                self.stock.append({'name': unit_name, 'rarity': rarity, 'cost': UNIT_POOL[rarity]['cost']})
        gold_disp = self.profile.gold if self.profile else '?'
        print(f'  Shop refreshed! Gold: {gold_disp}')
        self.display()

    def display(self):
        print('  -- Shop --')
        for i, item in enumerate(self.stock):
            print(f"    [{i}] {item['name']} ({item['rarity']}) - {item['cost']} gold")

    def buy(self, index, profile=None):
        profile = profile or self.profile
        if index >= len(self.stock):
            print('  Invalid selection.')
            return None
        item = self.stock[index]
        if profile:
            if not profile.spend_gold(item['cost']):
                return None
        self.stock.pop(index)
        print(f"  Bought {item['name']}! Gold remaining: {profile.gold if profile else '?'}")
        return item['name']

    def earn_gold(self, amount):
        if self.profile:
            self.profile.award_gold(amount)
        else:
            print(f'  +{amount} gold')
