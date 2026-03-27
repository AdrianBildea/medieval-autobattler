import random

UNIT_POOL = {
    "Common":    {"cost": 1,  "units": ["Knight", "Archer", "OrcWarrior", "SkeletonWarrior"]},
    "Rare":      {"cost": 3,  "units": ["FireMage", "IceMage", "Rogue", "Paladin"]},
    "Epic":      {"cost": 5,  "units": ["Priest", "Bard", "OrcShaman", "LichMage"]},
    "Legendary": {"cost": 8,  "units": []},
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
                print("  Refresh costs 2 gold.")
                return
        self.stock = []
        rarities = (["Common"] * 5) + (["Rare"] * 3) + (["Epic"] * 1)
        for _ in range(5):
            rarity = random.choice(rarities)
            units = UNIT_POOL[rarity]["units"]
            if units:
                unit_name = random.choice(units)
                self.stock.append({"name": unit_name, "rarity": rarity, "cost": UNIT_POOL[rarity]["cost"]})
        gold_disp = self.profile.gold if self.profile else "?"
        print(f"  Shop refreshed! Gold: {gold_disp}")
        self.display()

    def display(self):
        print("  -- Shop --")
        for i, item in enumerate(self.stock):
            print(f"    [{i}] {item['name']} ({item['rarity']}) - {item['cost']} gold")

    def buy(self, index, profile=None):
        profile = profile or self.profile
        if index >= len(self.stock):
            print("  Invalid selection.")
            return None
        item = self.stock[index]
        if profile and not profile.spend_gold(item["cost"]):
            return None
        self.stock.pop(index)
        print(f"  Bought {item['name']}! Gold remaining: {profile.gold if profile else '?'}")
        return item["name"]

    def check_upgrades(self, team):
        """Check if any 3 identical units can be merged into a level-up."""
        name_map = {}
        for unit in team:
            key = f"{type(unit).__name__}_lv{unit.level}"
            name_map.setdefault(key, []).append(unit)
        for key, units in name_map.items():
            if len(units) >= 3:
                base = units[0]
                base.upgrade()
                team.remove(units[1])
                team.remove(units[2])
                print(f"  3x {type(base).__name__} merged into Level {base.level}!")
                return True
        return False

    def earn_gold(self, amount):
        if self.profile:
            self.profile.award_gold(amount)
        else:
            print(f"  +{amount} gold")
