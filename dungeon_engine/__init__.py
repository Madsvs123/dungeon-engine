"""Deterministic turn engine for a future roguelike.

The package uses the Python standard library only and has no UI dependencies.

Public surface: ``Rng``, ``Event``, ``EventQueue``, ``step``, ``Actor``,
``GameState``, and ``run``. ``THRESHOLD`` is the energy required to act.
"""

from dungeon_engine.events import Event, EventQueue
from dungeon_engine.rng import Rng
from dungeon_engine.runner import run
from dungeon_engine.scheduler import THRESHOLD, step
from dungeon_engine.state import Actor, GameState

__version__ = "0.1.0"

__all__ = [
    "Actor",
    "Event",
    "EventQueue",
    "GameState",
    "Rng",
    "THRESHOLD",
    "run",
    "step",
]
