import random

UNIT_POOL = {
    "Common":    {"cost": 1, "units": ["Knight", "Archer"]},
    "Rare":      {"cost": 3, "units": ["FireMage"]},
    "Epic":      {"cost": 5, "units": ["Priest"]},
    "Legendary": {"cost": 8, "units": []},
}

REFRESH_COST = 2

class Shop:
    def __init__(self):
        self.gold = 10
        self.stock = []
        self.refresh(free=True)

    def refresh(self, free=False):
        if not free:
            if self.gold < REFRESH_COST:
                print("Not enough gold to refresh!")
                return
            self.gold -= REFRESH_COST
        self.stock = []
        rarities = (["Common"] * 5) + (["Rare"] * 3) + (["Epic"] * 1)
        for _ in range(5):
            rarity = random.choice(rarities)
            unit_name = random.choice(UNIT_POOL[rarity]["units"]) if UNIT_POOL[rarity]["units"] else None
            if unit_name:
                self.stock.append({"name": unit_name, "rarity": rarity, "cost": UNIT_POOL[rarity]["cost"]})
        print(f"  Shop refreshed! Gold: {self.gold}")
        self.display()

    def display(self):
        print("  -- Shop --")
        for i, item in enumerate(self.stock):
            print(f"    [{i}] {item['name']} ({item['rarity']}) - {item['cost']} gold")

    def buy(self, index):
        if index >= len(self.stock):
            print("Invalid selection.")
            return None
        item = self.stock[index]
        if self.gold < item["cost"]:
            print("Not enough gold!")
            return None
        self.gold -= item["cost"]
        self.stock.pop(index)
        print(f"  Bought {item['name']}! Gold remaining: {self.gold}")
        return item["name"]

    def earn_gold(self, amount):
        self.gold += amount
        print(f"  +{amount} gold earned. Total: {self.gold}")
