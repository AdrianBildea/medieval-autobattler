import random

MAX_TURNS = 60

class Battle:
    def __init__(self, player_team, enemy_team):
        from units import apply_faction_synergies
        self.player_team = [u for u in player_team]
        self.enemy_team = [u for u in enemy_team]
        print("\nApplying faction synergies...")
        apply_faction_synergies(self.player_team)
        apply_faction_synergies(self.enemy_team)

    @property
    def player_alive(self):
        return [u for u in self.player_team if u.is_alive]

    @property
    def enemy_alive(self):
        return [u for u in self.enemy_team if u.is_alive]

    def unit_act(self, unit, allies, enemies):
        if not unit.is_alive:
            return
        if unit.unit_class == "Support":
            living_allies = [u for u in allies if u.is_alive and u != unit]
            if living_allies:
                unit.use_ability(living_allies)
            return
        if unit.unit_class == "Mage":
            living_enemies = [u for u in enemies if u.is_alive]
            if living_enemies and random.random() < 0.4:
                unit.use_ability(living_enemies)
                return
        living_enemies = [u for u in enemies if u.is_alive]
        if not living_enemies:
            return
        target = min(living_enemies, key=lambda e: e.health)
        unit.attack_target(target)
        if not target.is_alive and hasattr(target, "try_revive"):
            target.try_revive()
        if random.random() < 0.25:
            unit.use_ability(living_enemies)

    def run(self):
        for turn in range(1, MAX_TURNS + 1):
            print(f"\n-- Turn {turn} --")
            all_units = self.player_alive + self.enemy_alive
            random.shuffle(all_units)
            for unit in all_units:
                if unit in self.player_team:
                    self.unit_act(unit, self.player_team, self.enemy_team)
                else:
                    self.unit_act(unit, self.enemy_team, self.player_team)
            if not self.player_alive:
                return "DEFEAT"
            if not self.enemy_alive:
                return "VICTORY"
        return "DRAW"
