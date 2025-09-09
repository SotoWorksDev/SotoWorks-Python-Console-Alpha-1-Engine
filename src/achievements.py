# src/achievements.py
ACHIEVEMENTS = [
    {"id": "first_stealth", "desc": "First Stealth Takedown", "unlocked": False},
    {"id": "no_damage_l1", "desc": "No Damage: Level 1", "unlocked": False},
    # Add more...
]

def unlock_achievement(ach_id):
    for ach in ACHIEVEMENTS:
        if ach["id"] == ach_id:
            ach["unlocked"] = True
            print(f"Achievement unlocked: {ach['desc']}")
