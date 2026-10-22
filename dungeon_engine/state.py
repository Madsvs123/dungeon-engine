"""Canonical game state and its SHA-256 hash.

``state_hash`` is the hex digest of UTF-8 JSON produced by ``json.dumps``
with ``sort_keys=True``, ``separators=(",", ":")``, ``ensure_ascii=True``,
and ``allow_nan=False``. Actors are ordered by id before encoding. The object
contains ints, strings, lists, and dicts only. There are no sets.

Counter keys in the hash are exactly ``combat``, ``loot``, and ``map``.
Call ``state_hash`` on the ``GameState`` returned by a run. Callers do not
need to sort actors first; ``canonical_payload`` orders them by id.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

__all__ = ["Actor", "GameState", "canonical_payload"]

_COUNTER_KEYS = ("combat", "loot", "map")


@dataclass
class Actor:
    id: int
    name: str
    speed: int
    energy: int = 0
    hp: int = 1


def _default_counters() -> dict[str, int]:
    return {key: 0 for key in ("map", "combat", "loot")}


@dataclass
class GameState:
    seed: int
    turn: int = 0
    actors: list[Actor] = field(default_factory=list)
    event_log_count: int = 0
    rng_counters: dict[str, int] = field(default_factory=_default_counters)

    def state_hash(self) -> str:
        """SHA-256 hex of the canonical JSON for this state."""
        encoded = json.dumps(
            canonical_payload(self),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


def canonical_payload(state: GameState) -> dict[str, object]:
    """JSON-ready object. Actor order is id order, not input order."""
    actors = sorted(state.actors, key=lambda actor: actor.id)
    return {
        "actors": [
            {
                "energy": actor.energy,
                "hp": actor.hp,
                "id": actor.id,
                "name": actor.name,
                "speed": actor.speed,
            }
            for actor in actors
        ],
        "event_log_count": state.event_log_count,
        "rng_counters": {key: state.rng_counters[key] for key in _COUNTER_KEYS},
        "seed": state.seed,
        "turn": state.turn,
    }
