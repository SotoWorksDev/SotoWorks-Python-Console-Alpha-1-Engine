import sys
import pygame as pg

from engine import (
    input_manager,
    SceneManager,
    Scaler,
    ProfilerOverlay,
    enforce_input_contract
)

# --- Boot/Config ---
CONFIG_PATH = "config/settings.json"  # Or wherever your config lives
enforce_input_contract(CONFIG_PATH)

# --- Initialize Engine Systems ---
pg.init = ProfilerOverlay()
scaler = Scaler(CONFIG_PATH)
window = scaler.create_window()
scene_manager = SceneManager()

# --- Example Scene ---
class ExampleScene:
    def handle_event(self, event):
        # Handle scene-specific events (input, etc.)
        pass

    def update(self, dt):
        # Update game logic here
        pass

    def draw(self, surface):
        surface.fill((20, 24, 32))
        # Draw your game scene here

scene_manager.push(ExampleScene())

# --- Main Loop ---
RUNNING = True
while RUNNING:
    dt = clock.tick(60) / 1000.0  # Seconds per frame (max 60 FPS)
    profiler.tick(dt)

    # --- Event Handling ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            RUNNING = False
        input_manager.handle_event(event)
        scene_manager.handle_event(event)
        if event.type == pg.VIDEORESIZE:
            scaler.on_resize(event.w, event.h)

    # --- Update ---
    scene_manager.update(dt)
    input_manager.update()  # Reset transient input states if needed

    # --- Draw ---
    surface = scaler.begin()
    scene_manager.draw(surface)
    input_manager.draw_controls(surface)
    profiler.draw(surface)
    scaler.end()

pg.quit()
sys.exit()
