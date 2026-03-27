import random
from units import Knight, Archer, FireMage, Priest
from combat import Battle
from shop import Shop
from campaign import Campaign

def main():
    print("=== Medieval Fantasy Autobattler ===")
    print("MVP Prototype - Phase 1: Combat & Basic Units\n")

    player_team = [
        Knight("Sir Aldric", level=1),
        Archer("Lena", level=1),
        FireMage("Zafar", level=1),
        Priest("Brother Elm", level=1),
    ]

    enemy_team = [
        Knight("Dark Knight", level=1),
        Archer("Shadow Archer", level=1),
        FireMage("Hex Mage", level=1),
        Priest("Vile Priest", level=1),
    ]

    print("--- Player Team ---")
    for u in player_team:
        print(f"  {u}")

    print("\n--- Enemy Team ---")
    for u in enemy_team:
        print(f"  {u}")

    print("\n--- Battle Start ---")
    battle = Battle(player_team, enemy_team)
    result = battle.run()

    print(f"\n=== Battle Result: {result} ===")

    print("\n--- Campaign Demo ---")
    campaign = Campaign()
    campaign.run_level(1, player_team)

if __name__ == "__main__":
    main()
