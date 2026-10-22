"""A run with no actors still has one canonical hash."""

from __future__ import annotations

import hashlib

from dungeon_engine.runner import run


def test_empty_actor_hash_matches_canonical_json() -> None:
    state = run(42, 15, actors=[])
    expected = (
        '{"actors":[],"event_log_count":0,'
        '"rng_counters":{"combat":0,"loot":0,"map":0},"seed":42,"turn":15}'
    )
    digest = hashlib.sha256(expected.encode("utf-8")).hexdigest()
    assert state.seed == 42
    assert state.turn == 15
    assert state.actors == []
    assert state.event_log_count == 0
    assert state.rng_counters == {"map": 0, "combat": 0, "loot": 0}
    assert state.state_hash() == digest
    assert run(42, 15, actors=[]).state_hash() == digest
