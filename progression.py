import json
import os

LEVEL_THRESHOLDS = {
    1: 0, 2: 100, 3: 250, 4: 500, 5: 900,
    6: 1400, 7: 2000, 8: 2800, 9: 3800, 10: 5000
}

TEAM_SIZE_BY_LEVEL = {
    1: 3, 2: 3, 3: 4, 4: 4, 5: 5,
    6: 5, 7: 6, 8: 6, 9: 7, 10: 7
}

SAVE_FILE = 'save_data.json'

class PlayerProfile:
    def __init__(self, name='Player'):
        self.name = name
        self.level = 1
        self.xp = 0
        self.gold = 10
        self.wins = 0
        self.losses = 0
        self.campaign_progress = 0

    @property
    def max_team_size(self):
        return TEAM_SIZE_BY_LEVEL.get(self.level, 7)

    @property
    def xp_to_next(self):
        next_lvl = self.level + 1
        if next_lvl not in LEVEL_THRESHOLDS:
            return None
        return LEVEL_THRESHOLDS[next_lvl] - self.xp

    def award_xp(self, amount):
        self.xp += amount
        print(f'  +{amount} XP (Total: {self.xp})')
        self._check_levelup()

    def award_gold(self, amount):
        self.gold += amount
        print(f'  +{amount} gold (Total: {self.gold})')

    def spend_gold(self, amount):
        if self.gold < amount:
            print(f'  Not enough gold! Have {self.gold}, need {amount}')
            return False
        self.gold -= amount
        return True

    def record_battle(self, result):
        if result == 'VICTORY':
            self.wins += 1
            self.award_xp(50)
            self.award_gold(5)
        elif result == 'DEFEAT':
            self.losses += 1
            self.award_xp(15)
            self.award_gold(2)
        else:
            self.award_xp(25)
            self.award_gold(3)

    def _check_levelup(self):
        while self.level < 10:
            next_lvl = self.level + 1
            if next_lvl in LEVEL_THRESHOLDS and self.xp >= LEVEL_THRESHOLDS[next_lvl]:
                self.level += 1
                new_size = TEAM_SIZE_BY_LEVEL[self.level]
                print(f'  *** LEVEL UP! Now Level {self.level} — Team size: {new_size} ***')
            else:
                break

    def display(self):
        xp_next = self.xp_to_next
        xp_str = f'{xp_next} to next level' if xp_next else 'MAX LEVEL'
        print(f'  Player: {self.name} | Level {self.level} | XP: {self.xp} ({xp_str})')
        print(f'  Gold: {self.gold} | W/L: {self.wins}/{self.losses} | Team Size: {self.max_team_size}')
        print(f'  Campaign Progress: Level {self.campaign_progress}')

    def save(self):
        data = {
            'name': self.name, 'level': self.level, 'xp': self.xp,
            'gold': self.gold, 'wins': self.wins, 'losses': self.losses,
            'campaign_progress': self.campaign_progress
        }
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f'  Game saved to {SAVE_FILE}')

    def load(self):
        if not os.path.exists(SAVE_FILE):
            print('  No save file found. Starting fresh.')
            return
        with open(SAVE_FILE) as f:
            data = json.load(f)
        self.name = data.get('name', 'Player')
        self.level = data.get('level', 1)
        self.xp = data.get('xp', 0)
        self.gold = data.get('gold', 10)
        self.wins = data.get('wins', 0)
        self.losses = data.get('losses', 0)
        self.campaign_progress = data.get('campaign_progress', 0)
        print(f'  Save loaded for {self.name} (Level {self.level})')
