"""Energy scheduler.

``THRESHOLD`` is 1000. One call to ``step`` is one scheduler step:

1. Add each actor's ``speed`` to that actor's ``energy``.
2. While any actor has ``energy >= 1000``, form a wave of those actors.
3. Sort the wave by ascending ``id``. Each actor in the wave subtracts 1000
   and is appended to the action list. Leftover energy stays.
4. An actor whose leftover is still ``>= 1000`` joins the next wave of this
   same step, so one step can contain more than one action from one actor.

The returned list is action order. An id can appear more than once. Ties in
a wave break by ascending actor id. Actor objects are mutated in place.

Example: speeds 300 and 100, both starting at energy 0. After seven steps the
fast actor has acted twice and still holds a remainder of 100. The slow actor
is at 700 and has not acted.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

__all__ = ["THRESHOLD", "step"]

THRESHOLD = 1000


class EnergyActor(Protocol):
    id: int
    speed: int
    energy: int


def step(actors: Iterable[EnergyActor]) -> list[int]:
    """Advance energy and return actor ids in the order they act."""
    roster = list(actors)
    for actor in roster:
        actor.energy += actor.speed
    acted: list[int] = []
    while True:
        ready = [actor for actor in roster if actor.energy >= THRESHOLD]
        if not ready:
            return acted
        ready.sort(key=lambda actor: actor.id)
        for actor in ready:
            actor.energy -= THRESHOLD
            acted.append(actor.id)
