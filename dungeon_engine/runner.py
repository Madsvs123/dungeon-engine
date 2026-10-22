"""Headless turn loop.

For each of ``turns`` iterations the runner:

1. Schedules the actors.
2. Pushes one ``wait`` event per action, stamped with the current turn index
   and that actor id. The payload is empty. Priority is 0.
3. Drains the queue and adds the drained length to ``event_log_count``.
4. Increments ``turn``.

A wait does not draw from the RNG. Counters stay at zero in this slice; the
seed is still stored on the state (masked to 64 bits) and is part of the hash.

``actors=None`` uses ``default_actors``. Any other list, including an empty
one, is copied and used as given. Actor ``energy`` is updated in place.
``run(seed, turns)`` is the CLI's loop. ``run(seed, turns, actors=[])`` is the
empty roster.
"""

from __future__ import annotations

from dungeon_engine.events import Event, EventQueue
from dungeon_engine.rng import Rng
from dungeon_engine.scheduler import step
from dungeon_engine.state import Actor, GameState

__all__ = ["default_actors", "run"]

WAIT_KIND = "wait"


def default_actors() -> list[Actor]:
    """Fixed party for the CLI. Ids and speeds do not change between runs."""
    return [
        Actor(id=1, name="wanderer", speed=100, energy=0, hp=10),
        Actor(id=2, name="guard", speed=60, energy=0, hp=14),
        Actor(id=3, name="scout", speed=150, energy=0, hp=8),
    ]


def run(seed: int, turns: int, actors: list[Actor] | None = None) -> GameState:
    """Run ``turns`` scheduler steps and return the resulting state."""
    if isinstance(turns, bool) or not isinstance(turns, int):
        raise TypeError("turns must be an int")
    if turns < 0:
        raise ValueError("turns must be >= 0")
    if actors is None:
        roster = default_actors()
    else:
        roster = list(actors)
    rng = Rng(seed)
    state = GameState(
        seed=rng.seed,
        turn=0,
        actors=roster,
        event_log_count=0,
        rng_counters=rng.counters(),
    )
    queue = EventQueue()
    for _ in range(turns):
        for actor_id in step(state.actors):
            queue.push(Event(kind=WAIT_KIND, turn=state.turn, actor_id=actor_id, payload=()))
        drained = queue.drain()
        state.event_log_count += len(drained)
        state.turn += 1
        state.rng_counters = rng.counters()
    return state
