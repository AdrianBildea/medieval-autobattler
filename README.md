# Medieval Fantasy Autobattler

A fully playable Python prototype for a mobile medieval fantasy autobattler game, built from the GDD.

> **Run it:** `python main.py`

---

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | Entry point |
| `game.py` | Full game loop — menus, modes, flow |
| `units.py` | All 12 unit classes, stats, abilities, faction synergies |
| `combat.py` | Auto-battle engine, AI behavior, turn system |
| `grid.py` | 4×4 battlefield, auto-placement, grid-aware targeting |
| `shop.py` | Shop system, unit pool, upgrade merging (3-copy mechanic) |
| `inventory.py` | 8 item types with rarities, equip system, random drops |
| `progression.py` | XP, leveling, gold, team size unlocks, save/load (JSON) |
| `campaign.py` | 4 campaign levels + endless wave generator |
| `ui.py` | Terminal UI: HP bars, menus, hero/shop/profile screens |

---

## How to Play

```bash
git clone https://github.com/AdrianBildea/medieval-autobattler
cd medieval-autobattler
python main.py
```

**Main Menu options:**
- `[1]` Campaign — fight 4 story levels with scaling enemies
- `[2]` Endless Mode — infinite waves, difficulty scales every 3 waves
- `[3]` Heroes — view your team stats and equipment
- `[4]` Shop — buy units with gold, refresh for 2 gold
- `[5]` Inventory — equip dropped items to heroes
- `[6]` Profile — view XP, level, W/L record
- `[7]` Save & Quit — saves progress to `save_data.json`

---

## Units (12 Total)

| Unit | Faction | Class | Special Ability |
|------|---------|-------|-----------------|
| Knight | Human | Tank | Shield Slam (stun) |
| Paladin | Human | Tank | Holy Shield (self-heal + DEF buff) |
| FireMage | Human | Mage | Fireball (AoE, 3 targets) |
| Priest | Human | Support | Heal (lowest HP ally) |
| Archer | Elf | DPS | Power Shot (2x damage) |
| Rogue | Elf | DPS | Backstab (2.5x crit) |
| IceMage | Elf | Mage | Blizzard (AoE + slow) |
| Bard | Elf | Support | Inspiring Song (heal all allies) |
| OrcWarrior | Orc | DPS | Rampage (multi-hit) |
| OrcShaman | Orc | Support | War Cry (boost ally ATK) |
| LichMage | Undead | Mage | Death Bolt (drain HP) |
| SkeletonWarrior | Undead | Tank | Bone Crush (reduce DEF) + Revive |

---

## Faction Synergies

| Faction | 2 Units | 4 Units |
|---------|---------|----------|
| Human | +10% Health | +25% Health |
| Elf | +15% Attack Speed | +30% Attack Speed |
| Orc | +20% Damage | +40% Damage |
| Undead | Lifesteal | Lifesteal + 35% Revive chance |

---

## Unit Upgrading

Collect 3 copies of the same unit → automatic merge into Level 2.  
Collect 3 Level 2 copies → Level 3.  
Stats scale: **+40% HP, +30% ATK, +30% DEF** per level.

---

## Equipment

Items drop after victories and can be equipped to any hero:

| Item | Rarity | Bonus |
|------|--------|-------|
| Sword | Common | +10 ATK |
| Great Sword | Rare | +30 ATK |
| Armor | Common | +20 HP |
| Plate Mail | Epic | +100 HP |
| Ring | Rare | +15 AP |
| Amulet | Common | +8 DEF |
| Boots | Rare | +0.3 ATK Speed |
| Crown | Legendary | +0.45 Crit Chance |

---

## Progression

| Player Level | Team Size |
|-------------|----------|
| 1–2 | 3 units |
| 3–4 | 4 units |
| 5–6 | 5 units |
| 7–8 | 6 units |
| 9–10 | 7 units |

XP earned: +50 (Victory), +25 (Draw), +15 (Defeat)

---

## Development Phases

| Phase | Status | Content |
|-------|--------|---------|
| 1 | ✅ Done | Combat engine, AI, basic units |
| 2 | ✅ Done | Grid system, positioning, inventory |
| 3 | ✅ Done | Shop system, gold economy, upgrade merging |
| 4 | ✅ Done | Terminal UI, HP bars, all screens |
| 5 | ✅ Done | XP progression, leveling, save/load |

---

## Planned (Post-MVP)

- Guilds & Raids
- PvP Arena (async)
- Seasons & rank resets
- Unity/Godot port with full graphical UI

---

## Tech Stack

- **Prototype:** Python 3.10+
- **Engine (planned):** Unity or Godot
- **Language (planned):** C# or GDScript
- **Platform (planned):** Android & iOS
- **Art (planned):** Kenney assets / Itch.io assets
