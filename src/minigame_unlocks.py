# src/minigame_unlocks.py

from .master_unlock_grid import MASTER_UNLOCK_GRID

def unlock_feature(unlock_name):
    print(f"Unlocked: {unlock_name}")

def check_minigame_unlocks(stats, minigame_results):
    # Example: ISO Strike Shooter
    if minigame_results.get('ISO Strike Shooter', {}).get('perfect_runs', 0) >= 2:
        unlock_feature('Manny Drone (Playable)')
    # Casino Table
    if minigame_results.get('Casino Table', {}).get('max_payout', False):
        unlock_feature('Casino High-Roller')
        unlock_feature('Golden Chip')
    # Lockpicking/Hacking
    if minigame_results.get('Lockpicking', {}).get('fast_hacks', 0) >= 3:
        unlock_feature('Silent Boots')
    # Phantom Duel QTE
    if minigame_results.get('Phantom Duel QTE', {}).get('perfect_parry', False):
        unlock_feature("Phantom’s Blade (skin)")
    # Dog Distraction
    if minigame_results.get('Dog Distraction', {}).get('cleared', False):
        unlock_feature('Guard Dog (AI companion)')
    # Cipher Node Puzzle
    if minigame_results.get('Cipher Node Puzzle', {}).get('shortcut_unlocked', False):
        unlock_feature('Xyra (Playable)')
