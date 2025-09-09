# src/save_system.py
import json

SAVE_FILE = "savegame.json"

def save_game(stats, unlocks):
    with open(SAVE_FILE, "w") as f:
        json.dump({"stats": stats, "unlocks": unlocks}, f)

def load_game():
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data["stats"], data["unlocks"]
    except (FileNotFoundError, KeyError):
        return None, None
