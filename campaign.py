from units import Knight, Archer, FireMage, Priest
from combat import Battle

LEVELS = {
    1: {"enemies": [Knight("Goblin Knight")], "reward_gold": 3},
    2: {"enemies": [Knight("Orc Grunt"), Archer("Bandit")], "reward_gold": 5},
    3: {"enemies": [Knight("Orc Warrior"), Archer("Dark Archer"), FireMage("Hex Mage")], "reward_gold": 7},
    4: {"enemies": [Knight("Black Knight"), Archer("Shadow Ranger"), FireMage("Warlock"), Priest("Dark Cleric")], "reward_gold": 10},
}

class Campaign:
    def __init__(self):
        self.current_level = 1
        self.gold = 0

    def run_level(self, level_num, player_team):
        if level_num not in LEVELS:
            print(f"Level {level_num} not found.")
            return
        level = LEVELS[level_num]
        print(f"\n=== Campaign Level {level_num} ===")
        print("Enemies:")
        for e in level["enemies"]:
            print(f"  {e}")
        for u in player_team:
            u.health = u.max_health
        for u in level["enemies"]:
            u.health = u.max_health
        battle = Battle(player_team, level["enemies"])
        result = battle.run()
        print(f"\nLevel {level_num} Result: {result}")
        if result == "VICTORY":
            self.gold += level["reward_gold"]
            print(f"Reward: +{level['reward_gold']} gold | Total gold: {self.gold}")
        return result
