from units import Knight, Archer, FireMage, Priest, ALL_UNIT_CLASSES, apply_faction_synergies
from combat import Battle
from shop import Shop
from campaign import Campaign
from grid import Grid
from inventory import Inventory
from progression import PlayerProfile
from ui import (show_main_menu, show_hero_screen, show_battle_screen,
                show_shop_screen, show_profile_screen, prompt, header, hp_bar)


class Game:
    def __init__(self):
        self.profile = PlayerProfile()
        self.team = []  # Player starts with NO units — must build via shop
        self.shop = Shop(self.profile)
        self.inventory = Inventory()
        self.campaign = Campaign()
        self.grid = Grid()

    def run(self):
        print('\n=== MEDIEVAL FANTASY AUTOBATTLER ===')
        choice = prompt('  Load save? [y/n]: ')
        if choice == 'y':
            self.profile.load()

        print('\n  Tip: Go to [4] Shop to recruit your first heroes!')

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

    # ── CAMPAIGN ──────────────────────────────────────────────────────────────

    def do_campaign(self):
        header('CAMPAIGN')
        if not self.team:
            print('  You have no heroes! Go to the Shop first.')
            prompt('  Press enter...')
            return
        max_level = max(self.campaign.LEVELS.keys())
        next_level = self.profile.campaign_progress + 1
        if next_level > max_level:
            print('  You have completed all campaign levels!')
            prompt('  Press enter...')
            return
        print(f'  Starting Campaign Level {next_level}...')
        print('  Your team:')
        for u in self.team:
            print(f'    {u}')
        prompt('  Press enter to begin battle...')
        self._run_battle(self.team, self.campaign.get_enemies(next_level), is_campaign=True, level_num=next_level)

    # ── ENDLESS ───────────────────────────────────────────────────────────────

    def do_endless(self):
        header('ENDLESS MODE')
        if not self.team:
            print('  You have no heroes! Go to the Shop first.')
            prompt('  Press enter...')
            return
        wave = 1
        while True:
            print(f'\n  Wave {wave}')
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

    # ── BATTLE ENGINE ─────────────────────────────────────────────────────────

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

    # ── HEROES ────────────────────────────────────────────────────────────────

    def do_heroes(self):
        while True:
            show_hero_screen(self.team)
            if not self.team:
                prompt('  Press enter to continue...')
                return
            print('  [s] Sell a hero (+1 gold)  |  [q] Back')
            cmd = prompt()
            if cmd == 'q':
                break
            elif cmd == 's':
                show_hero_screen(self.team)
                idx_cmd = prompt('  Enter hero index to sell: ')
                if idx_cmd.isdigit():
                    idx = int(idx_cmd)
                    if 0 <= idx < len(self.team):
                        sold = self.team.pop(idx)
                        self.profile.award_gold(1)
                        print(f'  Sold {sold.name} for 1 gold.')

    # ── SHOP ──────────────────────────────────────────────────────────────────

    def do_shop(self):
        while True:
            show_shop_screen(self.shop, self.profile)
            print(f'  Team: {len(self.team)}/{self.profile.max_team_size} slots used')
            cmd = prompt()
            if cmd == 'q':
                break
            elif cmd == 'r':
                self.shop.refresh()
            elif cmd.isdigit():
                idx = int(cmd)
                if len(self.team) >= self.profile.max_team_size:
                    print(f'  Team is full! ({self.profile.max_team_size} slots). Sell a hero first.')
                    continue
                unit_name = self.shop.buy(idx, self.profile)
                if unit_name:
                    unit = self._create_unit(unit_name)
                    if unit:
                        self.team.append(unit)
                        print(f'  {unit.name} [{unit.faction} {unit.unit_class}] added to your team!')
                        # Check for 3-copy upgrade merge
                        self.shop.check_upgrades(self.team)

    # ── INVENTORY ─────────────────────────────────────────────────────────────

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
            if 0 <= h_idx < len(self.team):
                self.inventory.equip(idx, self.team[h_idx])

    # ── HELPERS ───────────────────────────────────────────────────────────────

    def _create_unit(self, name):
        """Instantiate any of the 12 unit types by name."""
        cls = ALL_UNIT_CLASSES.get(name)
        if not cls:
            print(f'  Unknown unit: {name}')
            return None
        unit_num = sum(1 for u in self.team if type(u).__name__ == name) + 1
        return cls(f'{name} #{unit_num}')
