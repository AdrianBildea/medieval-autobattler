from units import Knight, Archer, FireMage, Priest, apply_faction_synergies
from combat import Battle
from shop import Shop
from campaign import Campaign
from grid import Grid
from inventory import Inventory, Item
from progression import PlayerProfile
from ui import (show_main_menu, show_hero_screen, show_battle_screen,
                show_shop_screen, show_profile_screen, show_grid, prompt, header, hp_bar)

def build_starter_team():
    return [
        Knight('Sir Aldric'),
        Archer('Lena'),
        FireMage('Zafar'),
    ]

class Game:
    def __init__(self):
        self.profile = PlayerProfile()
        self.team = build_starter_team()
        self.shop = Shop(self.profile)
        self.inventory = Inventory()
        self.campaign = Campaign()
        self.grid = Grid()

    def run(self):
        print('\n=== MEDIEVAL FANTASY AUTOBATTLER ===')
        choice = prompt('  Load save? [y/n]: ')
        if choice == 'y':
            self.profile.load()

        while True:
            show_main_menu()
            cmd = prompt()
            if cmd == '1':
                self.do_campaign()
            elif cmd == '2':
                self.do_endless()
            elif cmd == '3':
                self.do_heroes()
            elif cmd == '4':
                self.do_shop()
            elif cmd == '5':
                self.do_inventory()
            elif cmd == '6':
                show_profile_screen(self.profile)
                prompt('  Press enter to continue...')
            elif cmd == '7':
                self.profile.save()
                print('  Goodbye!')
                break
            else:
                print('  Invalid option.')

    def do_campaign(self):
        header('CAMPAIGN')
        max_level = max(self.campaign.LEVELS.keys())
        next_level = self.profile.campaign_progress + 1
        if next_level > max_level:
            print('  You have completed all campaign levels!')
            prompt('  Press enter...')
            return
        print(f'  Starting Campaign Level {next_level}...')
        prompt('  Press enter to begin battle...')
        self._run_battle(self.team, self.campaign.get_enemies(next_level), is_campaign=True, level_num=next_level)

    def do_endless(self):
        header('ENDLESS MODE')
        wave = 1
        while True:
            print(f'  Wave {wave}')
            enemies = self.campaign.generate_wave(wave)
            prompt(f'  Press enter to fight wave {wave}...')
            result = self._run_battle(self.team, enemies, is_campaign=False)
            if result == 'DEFEAT':
                print(f'  Endless Mode ended at Wave {wave}!')
                break
            wave += 1
            for u in self.team:
                u.health = u.max_health
        prompt('  Press enter...')

    def _run_battle(self, player_team, enemy_team, is_campaign=False, level_num=None):
        self.grid = Grid()
        self.grid.auto_place_team(player_team, is_player=True)
        self.grid.auto_place_team(enemy_team, is_player=False)
        print('\n  Grid Positions:')
        self.grid.display(player_team, enemy_team)
        for u in player_team:
            u.health = u.max_health
        battle = Battle(player_team, enemy_team, self.grid)
        result = battle.run()
        print(f'\n  === Result: {result} ===')
        self.profile.record_battle(result)
        if result == 'VICTORY':
            drop = self.inventory.random_drop()
            print(f'  Item drop: {drop}')
            if is_campaign and level_num:
                reward = self.campaign.LEVELS[level_num]['reward_gold']
                self.profile.award_gold(reward)
                self.profile.campaign_progress = level_num
        prompt('  Press enter to continue...')
        return result

    def do_heroes(self):
        show_hero_screen(self.team)
        prompt('  Press enter to continue...')

    def do_shop(self):
        while True:
            show_shop_screen(self.shop, self.profile)
            cmd = prompt()
            if cmd == 'q':
                break
            elif cmd == 'r':
                self.shop.refresh()
            elif cmd.isdigit():
                unit_name = self.shop.buy(int(cmd), self.profile)
                if unit_name and len(self.team) < self.profile.max_team_size:
                    unit = self._create_unit(unit_name)
                    if unit:
                        self.team.append(unit)
                        print(f'  {unit_name} added to your team!')
                elif unit_name:
                    print(f'  Team is full! Max size: {self.profile.max_team_size}')

    def do_inventory(self):
        self.inventory.display()
        if not self.inventory.items:
            prompt('  Press enter...')
            return
        cmd = prompt('  Equip item? Enter item index or [q]: ')
        if cmd == 'q' or not cmd.isdigit():
            return
        idx = int(cmd)
        show_hero_screen(self.team)
        hero_cmd = prompt('  Equip to which hero? Enter hero index: ')
        if hero_cmd.isdigit():
            h_idx = int(hero_cmd)
            if h_idx < len(self.team):
                self.inventory.equip(idx, self.team[h_idx])

    def _create_unit(self, name):
        mapping = {
            'Knight': Knight, 'Archer': Archer,
            'FireMage': FireMage, 'Priest': Priest,
        }
        cls = mapping.get(name)
        return cls(f'{name} #{len(self.team)+1}') if cls else None
