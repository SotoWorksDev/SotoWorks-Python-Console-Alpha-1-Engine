import pygame, math, time, json, os

def _dist(x1, y1, x2, y2): return math.hypot(x2 - x1, y2 - y1)
def _now(): return time.perf_counter()

class VirtualPad:
    def __init__(self, cfg, screen_w, screen_h, assets=None):
        self.cfg = cfg["vpad"]
        self.w, self.h = screen_w, screen_h
        self.assets = assets or {}
        self.opacity_idle = int(self.cfg.get("opacity_idle", 0.65) * 255)
        self.opacity_active = int(self.cfg.get("opacity_active", 0.9) * 255)

        # Stick
        st = self.cfg["stick"]
        self.st_c = (self.w * st["cx"], self.h * st["cy"])
        self.r_out = self.w * st["r_outer"]
        self.r_in = self.w * st["r_inner"]

        # Buttons
        self.btn_defs = {}
        for name, v in self.cfg["buttons"].items():
            if "r" in v:
                # Circle: (center_x, center_y, radius)
                self.btn_defs[name] = ("circle", (self.w * v["cx"], self.h * v["cy"], self.w * v["r"]))
            else:
                # Rect: (left, top, width, height)
                self.btn_defs[name] = (
                    "rect",
                    (
                        self.w * v["cx"] - self.w * v["w"] / 2,
                        self.h * v["cy"] - self.h * v["h"] / 2,
                        self.w * v["w"],
                        self.h * v["h"],
                    ),
                )

        # State
        self.stick_touch = None
        self.stick_vec = (0.0, 0.0)
        self.btn_touches = {}  # tid: (btn, down_time)
        self.btn_states = {k: False for k in self.btn_defs}
        self.btn_hold_times = {}
        self._events = []

    def on_touch(self, touches):
        now = _now()
        self._events.clear()
        # --- Stick logic ---
        stick_owner = self.stick_touch
        # Release stick if owner's finger not present
        if stick_owner is not None and not any(t[0] == stick_owner and t[3] for t in touches):
            self.stick_touch, self.stick_vec = None, (0.0, 0.0)

        # Assign stick owner if available
        for tid, x, y, dn in touches:
            if not dn: continue
            if self.stick_touch is None and _dist(x, y, *self.st_c) <= self.r_out:
                self.stick_touch = tid
            if tid == self.stick_touch:
                dx, dy = x - self.st_c[0], y - self.st_c[1]
                mag = max(1e-6, math.hypot(dx, dy))
                mag_n = min(1.0, mag / self.r_out)
                self.stick_vec = (dx / mag * mag_n, dy / mag * mag_n)
                self._events.append(("move", {"vec": self.stick_vec}))

        # --- Button logic ---
        current_btns = set()
        for tid, x, y, dn in touches:
            if not dn: continue
            for name, (kind, data) in self.btn_defs.items():
                hit = False
                if kind == "circle":
                    cx, cy, r = data
                    hit = _dist(x, y, cx, cy) <= r
                else:
                    rx, ry, rw, rh = data
                    hit = rx <= x <= rx + rw and ry <= y <= ry + rh
                if hit:
                    current_btns.add((tid, name))
                    if (tid, name) not in self.btn_touches:
                        self.btn_touches[(tid, name)] = now
                        self.btn_states[name] = True  # pressed
                        # Immediate tap event for most buttons except LT/RT
                        spec = self.cfg["buttons"][name]
                        if name == "RT":
                            v = self.stick_vec
                            if abs(v[0]) + abs(v[1]) > 0.25:
                                self._events.append(("dodge", {}))
                            else:
                                self._events.append(("rocket", {}))
                        elif name == "LT":
                            # Wait for tap/hold on release
                            pass
                        else:
                            act = spec.get("action")
                            if act: self._events.append((act, {}))

        # Tap/hold detection for triggers (LT)
        for (tid, name), down_time in list(self.btn_touches.items()):
            if (tid, name) not in current_btns:
                spec = self.cfg["buttons"][name]
                duration = now - down_time
                if name == "LT":
                    if duration > 0.32:
                        self._events.append(("crouch_cover", {}))
                    else:
                        self._events.append(("parry", {}))
                # Remove from state
                del self.btn_touches[(tid, name)]
                self.btn_states[name] = False

    def get_events(self):
        out = self._events.copy()
        self._events.clear()
        return out

    def get_stick_vec(self): return self.stick_vec

    def is_btn_down(self, name): return self.btn_states.get(name, False)

    def draw(self, surf, is_active=False):
        opacity = self.opacity_active if is_active else self.opacity_idle
        # Stick
        stick_outer = self.assets.get("stick_outer")
        stick_inner = self.assets.get("stick_inner")
        if stick_outer:
            s = stick_outer.copy(); s.set_alpha(opacity)
            rect = s.get_rect(center=self.st_c)
            surf.blit(s, rect)
        else:
            pygame.draw.circle(surf, (80,120,180,opacity), self.st_c, int(self.r_out), 4)
        if stick_inner:
            s = stick_inner.copy(); s.set_alpha(opacity)
            p = (int(self.st_c[0]+self.stick_vec[0]*self.r_out), int(self.st_c[1]+self.stick_vec[1]*self.r_out))
            rect = s.get_rect(center=p)
            surf.blit(s, rect)
        else:
            p = (int(self.st_c[0]+self.stick_vec[0]*self.r_out), int(self.st_c[1]+self.stick_vec[1]*self.r_out))
            pygame.draw.circle(surf, (128,220,255,opacity), p, int(self.r_in))
        # Buttons
        for name, (kind, data) in self.btn_defs.items():
            img = self.assets.get(f"btn_{name.lower()}")
            if img:
                s = img.copy(); s.set_alpha(opacity)
                if kind == "circle":
                    rect = s.get_rect(center=(data[0], data[1]))
                else:
                    rect = s.get_rect(center=(data[0] + data[2]/2, data[1] + data[3]/2))
                surf.blit(s, rect)
            else:
                color = (190, 80, 80, opacity) if self.is_btn_down(name) else (80, 80, 190, opacity)
                if kind == "circle":
                    pygame.draw.circle(surf, color, (int(data[0]), int(data[1])), int(data[2]))
                else:
                    pygame.draw.rect(surf, color, pygame.Rect(*data), border_radius=10)

# ---------- Sample integration -----------

def load_vpad_config(path_or_dict, screen_w, screen_h, asset_loader):
    if isinstance(path_or_dict, str):
        with open(path_or_dict) as f:
            cfg = json.load(f)
    else:
        cfg = path_or_dict
    assets = {}
    # Example: asset_loader
