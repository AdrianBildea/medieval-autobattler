import random
from units import Knight, Archer, FireMage, Priest

LEVELS = {
    1: {'enemies': lambda: [Knight('Goblin Knight')],                                                                        'reward_gold': 3},
    2: {'enemies': lambda: [Knight('Orc Grunt'), Archer('Bandit')],                                                          'reward_gold': 5},
    3: {'enemies': lambda: [Knight('Orc Warrior'), Archer('Dark Archer'), FireMage('Hex Mage')],                             'reward_gold': 7},
    4: {'enemies': lambda: [Knight('Black Knight'), Archer('Shadow Ranger'), FireMage('Warlock'), Priest('Dark Cleric')],    'reward_gold': 10},
}

UNIT_CLASSES = [Knight, Archer, FireMage, Priest]
ENEMY_PREFIXES = ['Shadow', 'Cursed', 'Dark', 'Vile', 'Fallen', 'Dread']

class Campaign:
    LEVELS = LEVELS

    def __init__(self):
        self.current_level = 1
        self.gold = 0

    def get_enemies(self, level_num):
        if level_num not in LEVELS:
            return []
        return LEVELS[level_num]['enemies']()

    def generate_wave(self, wave_num):
        count = min(2 + wave_num, 4)
        enemies = []
        for i in range(count):
            cls = random.choice(UNIT_CLASSES)
            prefix = random.choice(ENEMY_PREFIXES)
            unit = cls(f'{prefix} {cls.__name__}')
            lvl_boost = wave_num // 3
            for _ in range(lvl_boost):
                unit.upgrade()
            enemies.append(unit)
        return enemies

    def run_level(self, level_num, player_team):
        from combat import Battle
        if level_num not in LEVELS:
            print(f'  Level {level_num} not found.')
            return
        enemies = self.get_enemies(level_num)
        level = LEVELS[level_num]
        print(f'\n=== Campaign Level {level_num} ===')
        for u in player_team + enemies:
            u.health = u.max_health
        battle = Battle(player_team, enemies)
        result = battle.run()
        print(f'\n  Level {level_num} Result: {result}')
        if result == 'VICTORY':
            self.gold += level['reward_gold']
            print(f"  Reward: +{level['reward_gold']} gold | Total: {self.gold}")
        return result
