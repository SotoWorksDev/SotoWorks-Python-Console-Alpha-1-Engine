# engine/__init__.py
"""
Sotoworks Alpha 1 Engine Core Package

Exposes:
- input_manager: Singleton for input management.
- SceneManager: Core scene manager class.
- Scaler: Display scaler utility.
- ProfilerOverlay: Debugging profiler overlay.
- enforce_input_contract: Boot/guard utility.
"""

from .input_manager import input_manager
from .scene.manager import SceneManager
from .display.scaler import Scaler
from .debug.profiler import ProfilerOverlay
from .boot.guard import enforce_input_contract

# Now you can do, for example:
# from engine import input_manager, SceneManager, Scaler, ProfilerOverlay, enforce_input_contract
