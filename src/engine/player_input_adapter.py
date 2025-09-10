# src/engine/player_input_adapter.py

class PlayerInputAdapter:
    """
    Unifies input events from InputManager (controls.py) and VirtualPad (vpad.py),
    and yields canonical action names (e.g. 'shoot', 'jump', etc.) for your player/game logic.
    """

    def __init__(self, input_manager, virtual_pad=None):
        self.input_manager = input_manager
        self.virtual_pad = virtual_pad

    def poll_actions(self):
        """Yield tuples of (action, data) for both physical and virtual controls."""
        # 1. Physical controls (gamepad/keyboard)
        for ce in self.input_manager.poll():
            # ce has .action, .value (for move), .kind
            if ce.action == "move" and ce.kind == "axis":
                yield ("move", {"vec": ce.value})
            elif ce.action == "jump" and ce.kind == "press":
                yield ("jump", {})
            elif ce.action == "shoot" and ce.kind == "press":
                yield ("shoot", {})
            elif ce.action == "melee" and ce.kind == "press":
                yield ("melee", {})
            elif ce.action == "interact" and ce.kind == "press":
                yield ("interact
