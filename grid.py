class Grid:
    """4x4 battlefield. Rows 0-1 = enemy zone, Rows 2-3 = player zone."""
    ROWS = 4
    COLS = 4

    def __init__(self):
        self.cells = {}  # (row, col) -> Unit

    def place(self, unit, row, col):
        if not self._valid(row, col):
            print(f"  Invalid position ({row},{col})")
            return False
        if (row, col) in self.cells:
            print(f"  Cell ({row},{col}) already occupied by {self.cells[(row,col)].name}")
            return False
        self.cells[(row, col)] = unit
        unit.grid_pos = (row, col)
        return True

    def remove(self, unit):
        pos = getattr(unit, 'grid_pos', None)
        if pos and pos in self.cells:
            del self.cells[pos]
        unit.grid_pos = None

    def move(self, unit, new_row, new_col):
        self.remove(unit)
        return self.place(unit, new_row, new_col)

    def _valid(self, row, col):
        return 0 <= row < self.ROWS and 0 <= col < self.COLS

    def get_unit(self, row, col):
        return self.cells.get((row, col))

    def nearest_enemy(self, unit, enemy_team):
        pos = getattr(unit, 'grid_pos', None)
        if not pos:
            return None
        alive_enemies = [e for e in enemy_team if e.is_alive]
        if not alive_enemies:
            return None
        def dist(e):
            ep = getattr(e, 'grid_pos', None)
            if not ep:
                return 999
            return abs(pos[0] - ep[0]) + abs(pos[1] - ep[1])
        return min(alive_enemies, key=dist)

    def auto_place_team(self, team, is_player=True):
        tanks = [u for u in team if u.unit_class == 'Tank']
        others = [u for u in team if u.unit_class != 'Tank']
        if is_player:
            frontline_row, backline_row = 3, 2
        else:
            frontline_row, backline_row = 0, 1
        col = 0
        for unit in tanks:
            if col < self.COLS:
                self.place(unit, frontline_row, col)
                col += 1
        col = 0
        for unit in others:
            if col < self.COLS:
                self.place(unit, backline_row, col)
                col += 1

    def display(self, player_team, enemy_team):
        print("\n  +----+----+----+----+")
        for row in range(self.ROWS):
            row_str = "  |"
            for col in range(self.COLS):
                unit = self.cells.get((row, col))
                if unit and unit.is_alive:
                    abbr = unit.name[:3].upper()
                else:
                    abbr = "  ."
                row_str += f"{abbr:^4}|"
            label = " <- ENEMY" if row < 2 else " <- PLAYER"
            print(row_str + label)
        print("  +----+----+----+----+")
