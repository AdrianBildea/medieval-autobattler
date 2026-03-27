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
        self.grid_pos = None
        self.equipment = []

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
            print(f"  *** {self.name} upgraded to Level {self.level}! ***")
            return True
        return False

    def __repr__(self):
        return (f"{self.name} [{self.faction} {self.unit_class} Lv{self.level}] "
                f"HP:{self.health}/{self.max_health} ATK:{self.attack} DEF:{self.defense}")


# HUMAN UNITS

class Knight(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Human", unit_class="Tank",
                         health=200, attack=20, defense=15,
                         attack_speed=0.8, crit_chance=0.1,
                         ability_power=10, attack_range=1, level=level)

    def use_ability(self, targets):
        if targets:
            target = targets[0] if isinstance(targets, list) else targets
            target.stun_turns = 1
            dealt = target.take_damage(self.attack)
            print(f"    {self.name} uses Shield Slam on {target.name}! Stun + {dealt} dmg")


class Paladin(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Human", unit_class="Tank",
                         health=220, attack=18, defense=18,
                         attack_speed=0.7, crit_chance=0.08,
                         ability_power=20, attack_range=1, level=level)

    def use_ability(self, targets):
        self.heal(int(self.ability_power * 0.8))
        self.defense += 5
        print(f"    {self.name} uses Holy Shield! +5 DEF and heals {int(self.ability_power * 0.8)} HP")


# ELF UNITS

class Archer(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Elf", unit_class="DPS",
                         health=110, attack=30, defense=5,
                         attack_speed=1.2, crit_chance=0.25,
                         ability_power=15, attack_range=3, level=level)

    def use_ability(self, targets):
        if targets:
            target = min(targets, key=lambda u: u.health)
            dealt = target.take_damage(int(self.attack * 2))
            print(f"    {self.name} uses Power Shot on {target.name} for {dealt} dmg")


class Rogue(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Elf", unit_class="DPS",
                         health=100, attack=40, defense=4,
                         attack_speed=1.4, crit_chance=0.35,
                         ability_power=20, attack_range=1, level=level)

    def use_ability(self, targets):
        if targets:
            target = min(targets, key=lambda u: u.health)
            dealt = target.take_damage(int(self.attack * 2.5))
            print(f"    {self.name} Backstab hits {target.name} for {dealt} dmg!")


class IceMage(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Elf", unit_class="Mage",
                         health=85, attack=28, defense=3,
                         attack_speed=0.65, crit_chance=0.12,
                         ability_power=38, attack_range=3, level=level)

    def use_ability(self, targets):
        hit = targets[:3] if isinstance(targets, list) else [targets]
        for t in hit:
            dealt = t.take_damage(int(self.ability_power * 1.0))
            t.stun_turns = 1
            print(f"    {self.name} Blizzard hits {t.name} for {dealt} dmg + Slow")


class Bard(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Elf", unit_class="Support",
                         health=95, attack=12, defense=4,
                         attack_speed=0.65, crit_chance=0.07,
                         ability_power=30, attack_range=2, level=level)

    def use_ability(self, allies):
        if allies:
            heal_each = int(self.ability_power * 0.6)
            for ally in allies:
                if ally.is_alive:
                    ally.heal(heal_each)
            print(f"    {self.name} Inspiring Song heals all allies for {heal_each} HP")


# ORC UNITS

class OrcWarrior(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Orc", unit_class="DPS",
                         health=160, attack=38, defense=8,
                         attack_speed=1.0, crit_chance=0.2,
                         ability_power=20, attack_range=1, level=level)

    def use_ability(self, targets):
        hit = targets[:2] if isinstance(targets, list) else [targets]
        for t in hit:
            dealt = t.take_damage(int(self.attack * 1.5))
            print(f"    {self.name} Rampage hits {t.name} for {dealt} dmg")


class OrcShaman(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Orc", unit_class="Support",
                         health=130, attack=15, defense=6,
                         attack_speed=0.7, crit_chance=0.08,
                         ability_power=30, attack_range=2, level=level)

    def use_ability(self, allies):
        if allies:
            target = min(allies, key=lambda u: u.attack)
            target.attack = int(target.attack * 1.2)
            print(f"    {self.name} War Cry! {target.name} ATK boosted to {target.attack}")


# UNDEAD UNITS

class LichMage(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Undead", unit_class="Mage",
                         health=95, attack=30, defense=4,
                         attack_speed=0.8, crit_chance=0.18,
                         ability_power=50, attack_range=3, level=level)
        self.lifesteal = True

    def use_ability(self, targets):
        hit = targets[:3] if isinstance(targets, list) else [targets]
        total_drain = 0
        for t in hit:
            dealt = t.take_damage(int(self.ability_power * 0.9))
            total_drain += int(dealt * 0.4)
            print(f"    {self.name} Death Bolt hits {t.name} for {dealt} dmg")
        self.heal(total_drain)
        print(f"    {self.name} drains {total_drain} HP")


class SkeletonWarrior(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Undead", unit_class="Tank",
                         health=170, attack=22, defense=10,
                         attack_speed=0.9, crit_chance=0.12,
                         ability_power=12, attack_range=1, level=level)
        self.revive_chance = 0.25

    def use_ability(self, targets):
        if targets:
            target = targets[0] if isinstance(targets, list) else targets
            target.defense = max(0, target.defense - 3)
            dealt = target.take_damage(self.attack)
            print(f"    {self.name} Bone Crush on {target.name}: {dealt} dmg, -3 DEF")


# Human Mage
class FireMage(Unit):
    def __init__(self, name, level=1):
        super().__init__(name, faction="Human", unit_class="Mage",
                         health=90, attack=35, defense=3,
                         attack_speed=0.7, crit_chance=0.15,
                         ability_power=40, attack_range=3, level=level)

    def use_ability(self, targets):
        hit = targets[:3] if isinstance(targets, list) else [targets]
        for t in hit:
            dealt = t.take_damage(int(self.ability_power * 1.2))
            print(f"    {self.name} Fireball hits {t.name} for {dealt} dmg")


# Human Support
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


ALL_UNIT_CLASSES = {
    "Knight": Knight, "Paladin": Paladin,
    "Archer": Archer, "Rogue": Rogue,
    "FireMage": FireMage, "IceMage": IceMage,
    "OrcWarrior": OrcWarrior, "OrcShaman": OrcShaman,
    "LichMage": LichMage, "SkeletonWarrior": SkeletonWarrior,
    "Priest": Priest, "Bard": Bard,
}


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
