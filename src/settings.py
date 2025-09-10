# src/settings.py

SETTINGS = {
    "music_volume": 0.7,
    "sfx_volume": 0.7,
    "colorblind": False,
    "controls": {"up": "w", "down": "s", "left": "a", "right": "d"}
}

def save_settings(path="settings.json"):
    import json
    with open(path, "w") as f:
        json.dump(SETTINGS, f)

def load_settings(path="settings.json"):
    import os, json
    if os.path.exists(path):
        with open(path, "r") as f:
            SETTINGS.update(json.load(f))
