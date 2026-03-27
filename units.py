import random

FACTION_SYNERGIES = {
    "Human":  {2: ("health_pct", 0.10), 4: ("health_pct", 0.25)},
    "Elf":    {2: ("attack_speed_pct", 0.15), 4: ("attack_speed_pct", 0.30)},
    "Orc":    {2: ("damage_pct", 0.20), 4: ("damage_pct", 0.40)},
    "Undead": {2: ("lifesteal", True), 4: ("lifesteal_revive", True)},
}

class Unit:
    def __init__(self, name, faction, unit_class, health, attack, defense,
                 attack_speed, crit_chance, ability_power, attack_range, level=1):
        self.name = name
        self.faction = faction
        self.unit_class = unit_class
        self.base_health = health
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.attack_speed = attack_speed
        self.crit_chance = crit_chance
        self.ability_power = ability_power
        self.attack_range = attack_range
        self.level = level
        self.stun_turns = 0
        self.lifesteal = False
        self.revive_chance = 0.0
        self.copies = 1

    @property
    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        mitigated = max(1, amount - self.defense)
        self.health = max(0, self.health - mitigated)
        return mitigated

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def use_ability(self, targets):
        pass

    def attack_target(self, target):
        if self.stun_turns > 0:
            self.stun_turns -= 1
            print(f"    {self.name} is stunned!")
            return 0
        dmg = self.attack
        if random.random() < self.crit_chance:
            dmg = int(dmg * 1.5)
            print(f"    CRIT! ", end="")
        dealt = target.take_damage(dmg)
        if self.lifesteal:
            self.heal(int(dealt * 0.3))
        print(f"    {self.name} attacks {target.name} for {dealt} dmg (HP: {target.health}/{target.max_health})")
        return dealt

    def try_revive(self):
        if random.random() < self.revive_chance:
            self.health = int(self.max_health * 0.3)
            print(f"    {self.name} revives with {self.health} HP!")
            return True
        return False

    def upgrade(self):
        self.copies += 1
        if self.copies >= 3:
            self.copies = 0
            self.level += 1
            self.max_health = int(self.max_health * 1.4)
            self.health = self.max_health
            self.attack = int(self.attack * 1.3)
            self.defense = int(self.defense * 1.3)
            print(f"  {self.name} upgraded to Level {self.level}!")
            return True
        return False

    def __repr__(self):
        return (f"{self.name} [{self.faction} {self.unit_class} Lv{self.level}] "
                f"HP:{self.health}/{self.max_health} ATK:{self.attack} DEF:{self.defense}")


class Knight(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Human", unit_class="Tank",
                         health=200, attack=20, defense=15,
                         attack_speed=0.8, crit_chance=0.1,
                         ability_power=10, attack_range=1, level=level)

    def use_ability(self, targets):
        if targets:
            target = targets[0]
            target.stun_turns = 1
            dmg = self.attack
            dealt = target.take_damage(dmg)
            print(f"    {self.name} uses Shield Slam on {target.name}! Stun + {dealt} dmg")


class Archer(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Elf", unit_class="DPS",
                         health=110, attack=30, defense=5,
                         attack_speed=1.2, crit_chance=0.25,
                         ability_power=15, attack_range=3, level=level)

    def use_ability(self, targets):
        if targets:
            target = min(targets, key=lambda u: u.health)
            dmg = int(self.attack * 2)
            dealt = target.take_damage(dmg)
            print(f"    {self.name} uses Power Shot on {target.name} for {dealt} dmg")


class FireMage(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Human", unit_class="Mage",
                         health=90, attack=35, defense=3,
                         attack_speed=0.7, crit_chance=0.15,
                         ability_power=40, attack_range=3, level=level)

    def use_ability(self, targets):
        hit_targets = targets[:3]
        for t in hit_targets:
            dmg = int(self.ability_power * 1.2)
            dealt = t.take_damage(dmg)
            print(f"    {self.name} Fireball hits {t.name} for {dealt} dmg")


class Priest(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Human", unit_class="Support",
                         health=100, attack=10, defense=5,
                         attack_speed=0.6, crit_chance=0.05,
                         ability_power=35, attack_range=2, level=level)

    def use_ability(self, allies):
        if allies:
            target = min(allies, key=lambda u: u.health)
            heal_amount = int(self.ability_power * 1.5)
            target.heal(heal_amount)
            print(f"    {self.name} heals {target.name} for {heal_amount} HP (HP: {target.health}/{target.max_health})")


def apply_faction_synergies(team):
    from collections import Counter
    counts = Counter(u.faction for u in team)
    for faction, count in counts.items():
        if faction not in FACTION_SYNERGIES:
            continue
        synergy = FACTION_SYNERGIES[faction]
        bonus_type, bonus_val = None, None
        if count >= 4 and 4 in synergy:
            bonus_type, bonus_val = synergy[4]
        elif count >= 2 and 2 in synergy:
            bonus_type, bonus_val = synergy[2]
        if bonus_type:
            print(f"  Faction Synergy: {count}x {faction} -> {bonus_type} {bonus_val}")
            for u in team:
                if u.faction == faction:
                    if bonus_type == "health_pct":
                        u.max_health = int(u.max_health * (1 + bonus_val))
                        u.health = u.max_health
                    elif bonus_type == "damage_pct":
                        u.attack = int(u.attack * (1 + bonus_val))
                    elif bonus_type == "attack_speed_pct":
                        u.attack_speed *= (1 + bonus_val)
                    elif bonus_type == "lifesteal":
                        u.lifesteal = True
                    elif bonus_type == "lifesteal_revive":
                        u.lifesteal = True
                        u.revive_chance = 0.35
