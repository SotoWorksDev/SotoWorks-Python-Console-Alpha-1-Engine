# version: 1.5 / 2025-09-08 / 21:21:46
"""
SotoWorks Python Console ALPHA 1 Engine (SWPC A1 / SWPC AI Engine) v1.5
Demo Main Script — Systems Upgrade + Pods Scaffolding
"""

import sys
import pathlib
import pygame as pg
from engine.boot.guard import enforce_input_contract
from engine.scene.manager import SceneManager
from engine.scenes.splash_scene import SplashScene
from engine.display.scaler import Scaler
from engine.debug.profiler import ProfilerOverlay

def main():
    enforce_input_contract("alpha_engine.toml")
    pg.init()
    pg.display.set_caption("SWPC AI Engine — Demo")

    scaler = Scaler("alpha_engine.toml")
    window = scaler.create_window()
    clock = pg.time.Clock()
    prof = ProfilerOverlay()

    sm = SceneManager()
    sm.push(SplashScene(next_scene_factory=lambda: None))

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.VIDEORESIZE:
                scaler.on_resize(e.w, e.h)
            if hasattr(e, 'pos'):
                lp = scaler.window_to_logical(e.pos)
                if lp is not None:
                    e = pg.event.Event(
                        e.type,
                        {**e.dict, 'pos': lp, 'button': getattr(e, 'button', 0)}
                    )
            sm.handle_event(e)

        sm.update(dt)
        surf = scaler.begin()
        sm.draw(surf)
        prof.tick(dt)
        prof.draw(surf)
        scaler.end()

    pg.quit()

if __name__ == "__main__":
    main()
