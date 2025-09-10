# src/codex.py

CODEX_ENTRIES = [
    {"id": "lore1", "title": "The Syndicate", "body": "A shadowy group...", "unlocked": False},
    {"id": "lore2", "title": "Night City", "body": "A city of secrets...", "unlocked": False}
]

def unlock_entry(entry_id):
    for entry in CODEX_ENTRIES:
        if entry["id"] == entry_id:
            entry["unlocked"] = True
