# input_manager.py
# Sotoworks Alpha 1 Engine — Mobile-First Input Manager

import pygame as pg

class InputManager:
    """
    Handles input for mobile and desktop:
    - Touch, swipe, pinch gestures
    - On-screen virtual controls (joystick, dpad, diamond action buttons, start)
    - Gamepad/keyboard fallback
    - Dynamically switchable control schemes
    """
    SCHEME_JOYSTICK = 'joystick'
    SCHEME_DPAD = 'dpad'
    SCHEME_TOUCH = 'touch'
    SCHEME_GAMEPAD = 'gamepad'

    ACTIONS = ['move_up', 'move_down', 'move_left', 'move_right', 'start', 'action_w', 'action_a', 'action_s', 'action_d']

    def __init__(self):
        self.control_scheme = self.SCHEME_JOYSTICK
        self.schemes = [self.SCHEME_JOYSTICK, self.SCHEME_DPAD, self.SCHEME_TOUCH, self.SCHEME_GAMEPAD]
        self.active_actions = set()
        self.touches = {}         # finger_id: (x, y)
        self.gestures = {}        # e.g. 'swipe': direction, 'pinch': scale
        self.virtual_buttons = self._setup_virtual_buttons()
        self._init_pygame_touch()
        self._just_switched = False

    def _init_pygame_touch(self):
        # Enable touch events if supported by platform
        try:
            pg.event.set_allowed([pg.FINGERDOWN, pg.FINGERUP, pg.FINGERMOTION, pg.MULTIGESTURE])
        except Exception:
            pass

    def _setup_virtual_buttons(self):
        """
        Define zones for virtual controls based on scheme.
        Returns a dict: {action: pygame.Rect}
        """
        buttons = {}
        screen_w, screen_h = pg.display.get_surface().get_size()
        center_x, center_y = screen_w // 2, screen_h // 2

        def diamond(cx, cy, size):
            # Diamond layout for W,A,S,D (up, left, down, right)
            offset = size // 1.5
            return {
                'action_w': pg.Rect(cx, cy - offset, size, size),
                'action_a': pg.Rect(cx - offset, cy, size, size),
                'action_s': pg.Rect(cx, cy + offset, size, size),
                'action_d': pg.Rect(cx + offset, cy, size, size),
            }

        size = int(screen_h * 0.08)
        start_btn_rect = pg.Rect(center_x - size*2, center_y, size*1.5, size*1.2)
        if self.control_scheme == self.SCHEME_JOYSTICK:
            # Place joystick on left, diamond on right
            buttons['joystick'] = pg.Rect(size, screen_h - size*3, size*2, size*2)
            buttons['start'] = start_btn_rect
            buttons.update(diamond(screen_w - size*3, screen_h - size*3, size))
        elif self.control_scheme == self.SCHEME_DPAD:
            # Dpad on left, diamond on right
            buttons['dpad'] = pg.Rect(size, screen_h - size*3, size*2, size*2)
            buttons['start'] = start_btn_rect
            buttons.update(diamond(screen_w - size*3, screen_h - size*3, size))
        elif self.control_scheme == self.SCHEME_TOUCH:
            # Only diamond and start
            buttons['start'] = start_btn_rect
            buttons.update(diamond(center_x + size*2, center_y, size))
        # Gamepad/keyboard do not need virtual buttons
        return buttons

    def switch_scheme(self, scheme):
        if scheme not in self.schemes:
            return
        self.control_scheme = scheme
        self.virtual_buttons = self._setup_virtual_buttons()
        self._just_switched = True

    def handle_event(self, event):
        if event.type == pg.FINGERDOWN:
            self.touches[event.finger_id] = (event.x, event.y)
            self._process_touch(event.x, event.y, down=True)
        elif event.type == pg.FINGERUP:
            if event.finger_id in self.touches:
                self._process_touch(*self.touches[event.finger_id], down=False)
                del self.touches[event.finger_id]
        elif event.type == pg.FINGERMOTION:
            self.touches[event.finger_id] = (event.x, event.y)
        elif event.type == pg.MULTIGESTURE:
            self._process_gesture(event)
        elif event.type == pg.KEYDOWN or event.type == pg.KEYUP:
            self._process_keyboard(event)
        elif event.type == pg.JOYBUTTONDOWN or event.type == pg.JOYBUTTONUP:
            self._process_gamepad(event)
        elif event.type == pg.VIDEORESIZE:
            self.virtual_buttons = self._setup_virtual_buttons()

    def _process_touch(self, x, y, down):
        """Check if touch is within any virtual button zone."""
        sx, sy = pg.display.get_surface().get_size()
        px, py = int(x * sx), int(y * sy)
        for action, rect in self.virtual_buttons.items():
            if rect.collidepoint(px, py):
                if down:
                    self.active_actions.add(action)
                else:
                    self.active_actions.discard(action)

    def _process_gesture(self, event):
        # Placeholder: map gestures to actions
        # Example: if event.pinched, set self.gestures['pinch'] = event
        pass

    def _process_keyboard(self, event):
        keymap = {
            pg.K_w: 'action_w',
            pg.K_a: 'action_a',
            pg.K_s: 'action_s',
            pg.K_d: 'action_d',
            pg.K_RETURN: 'start',
            pg.K_UP: 'move_up',
            pg.K_LEFT: 'move_left',
            pg.K_DOWN: 'move_down',
            pg.K_RIGHT: 'move_right',
            # Add more if needed
        }
        if event.key in keymap:
            if event.type == pg.KEYDOWN:
                self.active_actions.add(keymap[event.key])
            elif event.type == pg.KEYUP:
                self.active_actions.discard(keymap[event.key])

    def _process_gamepad(self, event):
        # Map gamepad buttons to actions
        pass  # Implement based on your mappings

    def update(self):
        """Call at the end of each frame to reset transient gesture states."""
        if self._just_switched:
            self.active_actions.clear()
            self._just_switched = False
        # Optionally clear gesture states here

    def is_action_active(self, action):
        return action in self.active_actions

    def draw_controls(self, surface):
        """Draw the current virtual controls overlay."""
        color = (220, 220, 255, 120)
        for action, rect in self.virtual_buttons.items():
            pg.draw.rect(surface, color, rect, border_radius=12)
            # Draw button label
            font = pg.font.SysFont(None, int(rect.height * 0.7))
            label = ""
            if action == 'start':
                label = "START"
            elif action.startswith('action_'):
                label = action[-1].upper()
            elif action in ('joystick', 'dpad'):
                label = action.upper()
            if label:
                txt = font.render(label, True, (40, 40, 90))
                surface.blit(txt, txt.get_rect(center=rect.center))

    def get_virtual_buttons(self):
        """For testing or debugging: returns a copy of the button rects."""
        return self.virtual_buttons.copy()

# Singleton instance
input_manager = InputManager()
