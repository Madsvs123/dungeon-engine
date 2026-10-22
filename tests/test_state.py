"""The state hash is canonical JSON, independent of actor input order."""

from __future__ import annotations

import hashlib
import json

import pytest

from dungeon_engine.state import Actor, GameState, canonical_payload


def _counters() -> dict[str, int]:
    return {"map": 0, "combat": 0, "loot": 0}


def _assert_json_safe(value: object) -> None:
    assert not isinstance(value, (set, frozenset))
    if isinstance(value, dict):
        for key, item in value.items():
            assert isinstance(key, str)
            _assert_json_safe(item)
    elif isinstance(value, list):
        for item in value:
            _assert_json_safe(item)
    else:
        assert isinstance(value, (str, int))


def test_hash_is_sha256_hex_of_canonical_json() -> None:
    state = GameState(seed=0)
    expected = (
        '{"actors":[],"event_log_count":0,'
        '"rng_counters":{"combat":0,"loot":0,"map":0},"seed":0,"turn":0}'
    )
    digest = hashlib.sha256(expected.encode("utf-8")).hexdigest()
    assert state.state_hash() == digest
    assert len(digest) == 64
    assert digest == digest.lower()


def test_actor_order_does_not_change_hash() -> None:
    first = Actor(id=1, name="a", speed=10, energy=1, hp=2)
    second = Actor(id=2, name="b", speed=20, energy=3, hp=4)
    left = GameState(seed=3, turn=1, actors=[first, second], rng_counters=_counters())
    right = GameState(seed=3, turn=1, actors=[second, first], rng_counters=_counters())
    assert left.state_hash() == right.state_hash()
    payload = canonical_payload(left)
    assert [actor["id"] for actor in payload["actors"]] == [1, 2]


def test_hp_changes_hash() -> None:
    healthy = GameState(
        seed=3,
        actors=[Actor(id=1, name="a", speed=10, energy=0, hp=5)],
        rng_counters=_counters(),
    )
    hurt = GameState(
        seed=3,
        actors=[Actor(id=1, name="a", speed=10, energy=0, hp=4)],
        rng_counters=_counters(),
    )
    assert healthy.state_hash() != hurt.state_hash()


def test_payload_has_no_sets_and_matches_literal_json() -> None:
    state = GameState(
        seed=7,
        turn=3,
        actors=[
            Actor(id=2, name="b", speed=5, energy=4, hp=3),
            Actor(id=1, name="a", speed=9, energy=8, hp=6),
        ],
        event_log_count=11,
        rng_counters={"map": 1, "combat": 2, "loot": 3},
    )
    payload = canonical_payload(state)
    _assert_json_safe(payload)
    expected = (
        '{"actors":['
        '{"energy":8,"hp":6,"id":1,"name":"a","speed":9},'
        '{"energy":4,"hp":3,"id":2,"name":"b","speed":5}'
        '],"event_log_count":11,"rng_counters":{"combat":2,"loot":3,"map":1},'
        '"seed":7,"turn":3}'
    )
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    assert encoded == expected
    assert state.state_hash() == hashlib.sha256(expected.encode("utf-8")).hexdigest()


def test_missing_counter_is_an_error() -> None:
    state = GameState(seed=1, rng_counters={"map": 0, "combat": 0})
    with pytest.raises(KeyError):
        state.state_hash()


def test_extra_counter_is_not_hashed() -> None:
    base = GameState(seed=1, rng_counters=_counters())
    extra_counters = _counters()
    extra_counters["noise"] = 5
    extra = GameState(seed=1, rng_counters=extra_counters)
    assert base.state_hash() == extra.state_hash()
