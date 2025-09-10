# src/profiles.py

import os, json

PROFILE_DIR = "profiles"

def list_profiles():
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
    return [f[:-5] for f in os.listdir(PROFILE_DIR) if f.endswith(".json")]

def save_profile(profile_name, data):
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
    with open(os.path.join(PROFILE_DIR, f"{profile_name}.json"), "w") as f:
        json.dump(data, f, indent=2)

def load_profile(profile_name):
    try:
        with open(os.path.join(PROFILE_DIR, f"{profile_name}.json"), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
