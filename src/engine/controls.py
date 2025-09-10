# ─────────────────────────────────────────────────────────────────────────────
# SotoWorks Standard Header
# Project: Space Mack — ISO Strike (SWPC Alpha)
# File: controls.py
# Version: 1.0
# Author: Mario Soto Studios — SotoWorks Games
# License: Internal use per SotoWorks Master Guide
# Notes: Pygame input manager. 1x left stick, L/R triggers, face buttons, 8-way D-Pad (diagonals).
#        Tap/hold detection, remappable JSON, keyboard fallback, mobile-friendly deadzones.
# ─────────────────────────────────────────────────────────────────────────────

from __future__ import annotations
import pygame, json, os, time
from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional

# ---------- ACTIONS (engine-facing) ----------
A_MOVE            = "move"              # (x,y) analog
A_JUMP            = "jump"
A_CROUCH_COVER    = "crouch_cover"      # hold
A_PARRY           = "parry"             # tap (L in duels)
A_DODGE           = "dodge"             # tap with dir
A_SHOOT           = "shoot"
A_MELEE           = "melee"
A_INTERACT        = "interact"          # use/hack/pickup
A_GRENADE         = "grenade"
A_ROCKET          = "rocket"            # heavy weapon / flamethrower alt
A_WEAPON_PREV     = "weapon_prev"
A_WEAPON_NEXT     = "weapon_next"
A_OBJ_TOGGLE      = "objective_toggle"
A_MINIMAP_TOGGLE  = "minimap_toggle"
A_USE_CONSUMABLE  = "use_consumable"
A_DROP_DECOY      = "drop_decoy"
A_EQUIP_HEAVY     = "equip_heavy"
A_EQUIP_GADGET    = "equip_gadget"
A_STEALTH_TOGGLE  = "stealth_toggle"
A_ALT_FIRE_SWAP   = "alt_fire_swap"
A_INVENTORY       = "inventory"
A_PAUSE           = "pause"

DEFAULT_BINDINGS = {
    # Face buttons
    A_SHOOT:          {"kbd":[pygame.K_k], "joy_buttons":[0]},  # A
    A_MELEE:          {"kbd":[pygame.K_j], "joy_buttons":[1]},  # B
    A_INTERACT:       {"kbd":[pygame.K_i], "joy_buttons":[2]},  # X
    A_JUMP:           {"kbd":[pygame.K_l], "joy_buttons":[3]},  # Y
    # System
    A_INVENTORY:      {"kbd":[pygame.K_TAB], "joy_buttons":[7]},  # START
    A_PAUSE:          {"kbd":[pygame.K_ESCAPE], "joy_buttons":[6]},# SELECT/Back
    # Triggers / shoulders
    A_CROUCH_COVER:   {"kbd":[pygame.K_LCTRL], "joy_buttons":[4]}, # L (hold)
    A_PARRY:          {"kbd":[pygame.K_q], "joy_buttons":[4]},     # L tap (duels)
    A_ROCKET:         {"kbd":[pygame.K_e], "joy_buttons":[5]},     # R tap
    A_DODGE:          {"kbd":[pygame.K_SPACE], "joy_buttons":[5]}, # R + dir
    A_GRENADE:        {"kbd":[pygame.K_u], "joy_buttons":[2], "hold":True}, # X hold
    # D-Pad cardinals
    A_OBJ_TOGGLE:     {"hat":"up"},
    A_USE_CONSUMABLE: {"hat":"down"},
    A_WEAPON_PREV:    {"hat":"left"},
    A_WEAPON_NEXT:    {"hat":"right"},
    # D-Pad diagonals
    A_EQUIP_GADGET:   {"hat":"up_right"},
    A_EQUIP_HEAVY:    {"hat":"down_right"},
    A_STEALTH_TOGGLE: {"hat":"down_left"},
    A_ALT_FIRE_SWAP:  {"hat":"up_left"},
    # Optional minimap toggle (alias to objective)
    A_MINIMAP_TOGGLE: {"kbd":[pygame.K_m]},
}

# Keyboard movement (fallback)
K_MOVE = {
    "up":    [pygame.K_w, pygame.K_UP],
    "down":  [pygame.K_s, pygame.K_DOWN],
    "left":  [pygame.K_a, pygame.K_LEFT],
    "right": [pygame.K_d, pygame.K_RIGHT],
}

# ---------- INTERNAL HELPERS ----------
def _now() -> float:
    return time.perf_counter()

@dataclass
class ButtonState:
    pressed: bool = False
    changed: bool = False
    t_down: float = 0.0
    t_up: float = 0.0

    def set(self, is_down: bool):
        if is_down != self.pressed:
            self.pressed = is_down
            self.changed = True
            if is_down: self.t_down = _now()
            else:       self.t_up   = _now()
        else:
            self.changed = False

    def was_pressed(self) -> bool:
        return self.changed and self.pressed

    def was_released(self) -> bool:
        return self.changed and (not self.pressed)

    def held_for(self) -> float:
        return _now() - self.t_down if self.pressed else 0.0

@dataclass
class InputConfig:
    deadzone: float = 0.22           # left stick deadzone
    dodge_tap_window: float = 0.25   # seconds
    hold_threshold: float = 0.35     # seconds to treat as "hold"

@dataclass
class ControlEvent:
    action: str
    value: Optional[Tuple[float,float]] = None
    kind: str = "press"  # "press","release","axis","hold","tap"

@dataclass
class InputManager:
    bindings: Dict[str, dict] = field(default_factory=lambda: DEFAULT_BINDINGS.copy())
    cfg: InputConfig = field(default_factory=InputConfig)

    def __post_init__(self):
        pygame.joystick.init()
        self.joys = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for j in self.joys:
            j.init()

        self.btn: Dict[str, ButtonState] = {a: ButtonState() for a in self.bindings}
        self.events: list[ControlEvent] = []
        self._axis_move = (0.0, 0.0)
        self._last_r_tap_t = 0.0
        self._last_l_tap_t = 0.0

    # ---------- CONFIG ----------
    def save_bindings(self, path: str):
        with open(path, "w") as f: json.dump(self.bindings, f, indent=2)

    def load_bindings(self, path: str):
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            self.bindings.update(data)

    # ---------- UPDATE ----------
    def update(self):
        self.events.clear()
        pygame.event.pump()

        # --- Read joystick states ---
        hat = (0,0)
        if self.joys:
            j = self.joys[0]
            # Left stick on axes 0 (x) and 1 (y)
            ax = j.get_axis(0) if j.get_numaxes() > 0 else 0.0
            ay = j.get_axis(1) if j.get_numaxes() > 1 else 0.0
            # Deadzone
            ax = 0.0 if abs(ax) < self.cfg.deadzone else ax
            ay = 0.0 if abs(ay) < self.cfg.deadzone else ay
            self._axis_move = (ax, ay)

            # D-Pad hat (supports diagonals)
            if j.get_numhats() > 0:
                hat = j.get_hat(0)  # (x,y) with diagonals

            # Triggers as buttons (typical Android pads map LB=4 RB=5; adapt if needed)
            lb = bool(j.get_button(4))
            rb = bool(j.get_button(5))
        else:
            # Keyboard fallback: WASD for move
            keys = pygame.key.get_pressed()
            ax = float(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - float(keys[pygame.K_a] or keys[pygame.K_LEFT])
            ay = float(keys[pygame.K_s] or keys[pygame.K_DOWN])  - float(keys[pygame.K_w] or keys[pygame.K_UP])
            self._axis_move = (ax, ay)
            lb = keys[pygame.K_LCTRL]
            rb = keys[pygame.K_e] or keys[pygame.K_SPACE]

        # --- Move action (analog) ---
        if self._axis_move != (0.0, 0.0):
            self.events.append(ControlEvent(A_MOVE, self._axis_move, "axis"))

        # --- Map hat (8-way + holds) ---
        self._apply_hat(hat)

        # --- Map face/trigger buttons + tap/hold semantics ---
        self._apply_button(A_SHOOT)
        self._apply_button(A_MELEE)
        self._apply_button(A_INTERACT, hold_name=A_GRENADE)  # X hold = grenade
        self._apply_button(A_JUMP)
        self._apply_button(A_INVENTORY)
        self._apply_button(A_PAUSE)

        # L Trigger: crouch hold + parry tap
        self._apply_trigger_combo(left_trigger=lb, right_trigger=rb)

        # Weapon prev/next/list already handled via hat cardinals + diagonals

    # ---------- INTERNAL MAPPERS ----------
    def _apply_hat(self, hv: Tuple[int,int]):
        hx, hy = hv
        # cardinals
        self._emit_hat("up",     hy ==  1, A_OBJ_TOGGLE)
        self._emit_hat("down",   hy == -1, A_USE_CONSUMABLE)
        self._emit_hat("left",   hx == -1, A_WEAPON_PREV)
        self._emit_hat("right",  hx ==  1, A_WEAPON_NEXT)
        # diagonals
        self._emit_hat("up_right",   (hx,hy)==(1,1),   A_EQUIP_GADGET)
        self._emit_hat("down_right", (hx,hy)==(1,-1),  A_EQUIP_HEAVY)
        self._emit_hat("down_left",  (hx,hy)==(-1,-1), A_STEALTH_TOGGLE)
        self._emit_hat("up_left",    (hx,hy)==(-1,1),  A_ALT_FIRE_SWAP)

    def _emit_hat(self, name: str, is_on: bool, action: str):
        st = self.btn[action]
        st.set(is_on)
        if st.was_pressed():  self.events.append(ControlEvent(action, kind="press"))
        if st.was_released(): self.events.append(ControlEvent(action, kind="release"))

    def _apply_button(self, action: str, hold_name: Optional[str]=None):
        keys = pygame.key.get_pressed()
        is_down = False

        spec = self.bindings.get(action, {})
        for k in spec.get("kbd", []):
            if keys[k]: is_down = True
        if self.joys:
            j = self.joys[0]
            for b in spec.get("joy_buttons", []):
                if j.get_button(b): is_down = True

        st = self.btn[action]
        st.set(is_down)

        # tap
        if st.was_pressed():
            self.events.append(ControlEvent(action, kind="press"))

        # hold conversion
        if hold_name and st.pressed and st.held_for() >= self.cfg.hold_threshold:
            self.events.append(ControlEvent(hold_name, kind="hold"))

        if st.was_released():
            self.events.append(ControlEvent(action, kind="release"))

    def _apply_trigger_combo(self, left_trigger: bool, right_trigger: bool):
        # L: crouch/cover hold, or parry tap if quick
        stL = self.btn.setdefault("_L", ButtonState())
        prev = stL.pressed
        stL.set(left_trigger)

        if stL.was_pressed():
            self._last_l_tap_t = _now()

        if stL.pressed:
            # after hold threshold -> crouch/cover
            if stL.held_for() >= self.cfg.hold_threshold:
                self._emit_hold(A_CROUCH_COVER)
        elif prev and stL.was_released():
            # quick tap within window -> parry
            if (_now() - self._last_l_tap_t) <= self.cfg.dodge_tap_window:
                self.events.append(ControlEvent(A_PARRY, kind="tap"))

        # R: rocket tap OR dodge with direction (LS + quick tap)
        stR = self.btn.setdefault("_R", ButtonState())
        stR.set(right_trigger)
        if stR.was_pressed():
            self._last_r_tap_t = _now()

            # if moving significantly, treat as dodge
            ax, ay = self._axis_move
            if (ax*ax + ay*ay) >= 0.25:
                self.events.append(ControlEvent(A_DODGE, value=(ax,ay), kind="tap"))
            else:
                self.events.append(ControlEvent(A_ROCKET, kind="tap"))

    def _emit_hold(self, action: str):
        # de-dupe continuous spam: only emit once per update cycle as 'hold'
        self.events.append(ControlEvent(action, kind="hold"))

    # ---------- PUBLIC API ----------
    def poll(self) -> list[ControlEvent]:
        """Call update() each frame, then poll() to consume events."""
        out = self.events[:]
        self.events.clear()
        return out

    def move_vector(self) -> Tuple[float,float]:
        return self._axis_move

# ---------- Minimal demo ----------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 450))
    clock = pygame.time.Clock()
    im = InputManager()
    print("Controls demo running. Press ESC or SELECT to quit.")

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

        im.update()
        for ce in im.poll():
            if ce.action in (A_PAUSE,) and ce.kind == "press":
                running = False
            # Print a compact log line
            if ce.action == A_MOVE and ce.kind == "axis":
                pass  # noisy; skip
            else:
                print(f"{ce.kind:6s} -> {ce.action}", ("", ce.value)[ce.value is not None])

        screen.fill((8,12,18))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
