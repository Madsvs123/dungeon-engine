"""The package root exports the headless engine surface."""

from __future__ import annotations

import dungeon_engine
from dungeon_engine import THRESHOLD, Actor, Event, EventQueue, GameState, Rng, run, step


def test_public_surface() -> None:
    assert dungeon_engine.__version__ == "0.1.0"
    assert THRESHOLD == 1000
    assert Rng(1).seed == 1
    assert Event("wait", 0, 1).kind == "wait"
    assert EventQueue().drain() == []
    assert GameState(seed=1).seed == 1
    assert Actor(id=1, name="a", speed=1).id == 1
    assert step([]) == []
    state = run(1, 0, actors=[])
    assert state.turn == 0
    assert state.state_hash()
