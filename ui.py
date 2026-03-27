import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def header(title):
    width = 44
    print('=' * width)
    print(f'  {title}')
    print('=' * width)

def hp_bar(current, maximum, length=20):
    if maximum <= 0:
        return '[' + '.' * length + ']'
    filled = int((current / maximum) * length)
    bar = '█' * filled + '░' * (length - filled)
    return f'[{bar}] {current}/{maximum}'

def show_main_menu():
    print()
    header('MEDIEVAL FANTASY AUTOBATTLER')
    print('  [1] Campaign')
    print('  [2] Endless Mode')
    print('  [3] Heroes')
    print('  [4] Shop')
    print('  [5] Inventory')
    print('  [6] Profile')
    print('  [7] Save & Quit')
    print()

def show_hero_screen(team):
    header('HEROES')
    if not team:
        print('  No heroes in your team.')
        return
    for i, unit in enumerate(team):
        alive = 'ALIVE' if unit.is_alive else 'FALLEN'
        print(f'  [{i}] {unit.name} [{unit.faction} {unit.unit_class} Lv{unit.level}] {alive}')
        print(f'       HP:  {hp_bar(unit.health, unit.max_health)}')
        print(f'       ATK: {unit.attack:>3}  DEF: {unit.defense:>3}  SPD: {unit.attack_speed:.1f}')
        print(f'       CRIT:{unit.crit_chance*100:.0f}%  AP: {unit.ability_power:>3}  Range: {unit.attack_range}')
        equip = getattr(unit, 'equipment', [])
        if equip:
            print(f'       Equipment: {", ".join(str(e) for e in equip)}')
        print()

def show_battle_screen(player_team, enemy_team, turn):
    header(f'BATTLE — Turn {turn}')
    print('  ENEMY TEAM:')
    for u in enemy_team:
        status = hp_bar(u.health, u.max_health, 15) if u.is_alive else '[DEFEATED]       '
        print(f'    {u.name:<18} {status}')
    print('  ' + '-' * 40)
    print('  PLAYER TEAM:')
    for u in player_team:
        status = hp_bar(u.health, u.max_health, 15) if u.is_alive else '[DEFEATED]       '
        print(f'    {u.name:<18} {status}')
    print()

def show_shop_screen(shop, profile):
    header(f'SHOP  (Gold: {profile.gold})')
    shop.display()
    print()
    print('  [r] Refresh shop (2 gold)')
    print('  [0-4] Buy unit')
    print('  [q] Back')
    print()

def show_profile_screen(profile):
    header('PLAYER PROFILE')
    profile.display()
    print()

def show_grid(grid):
    print()
    header('BATTLEFIELD GRID')
    grid.display([], [])
    print()

def prompt(message='  > '):
    return input(message).strip().lower()
