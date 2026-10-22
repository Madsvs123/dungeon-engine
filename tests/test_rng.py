"""Substream independence and the documented SplitMix64 mixer."""

from __future__ import annotations

import pytest

from dungeon_engine.rng import STREAMS, Rng


def test_stream_names() -> None:
    assert STREAMS == ("map", "combat", "loot")
    assert set(Rng(1).counters()) == {"map", "combat", "loot"}


def test_same_seed_same_draws() -> None:
    left = Rng(99)
    right = Rng(99)
    for name in STREAMS:
        assert [left.draw(name) for _ in range(5)] == [right.draw(name) for _ in range(5)]


def test_draw_advances_only_that_substream() -> None:
    untouched = Rng(42)
    drawn = Rng(42)
    drawn.draw("map")
    drawn.draw("map")
    assert drawn.draw("combat") == untouched.draw("combat")
    assert drawn.draw("loot") == untouched.draw("loot")
    assert drawn.counters() == {"map": 2, "combat": 1, "loot": 1}
    assert untouched.counters() == {"map": 0, "combat": 1, "loot": 1}


def test_counters_are_a_copy() -> None:
    rng = Rng(1)
    rng.draw("loot")
    snapshot = rng.counters()
    snapshot["loot"] = 0
    assert rng.counters()["loot"] == 1


def test_different_seeds_diverge() -> None:
    assert [Rng(1).draw("map") for _ in range(4)] != [Rng(2).draw("map") for _ in range(4)]


def test_seed_is_masked_to_64_bits() -> None:
    assert Rng(0).draw("map") == Rng(1 << 64).draw("map")
    assert Rng(5).seed == 5
    assert Rng((1 << 64) + 5).seed == 5


def test_draws_are_u64() -> None:
    rng = Rng(123456789)
    for name in STREAMS:
        for _ in range(20):
            value = rng.draw(name)
            assert isinstance(value, int)
            assert 0 <= value < (1 << 64)


def test_unknown_stream() -> None:
    with pytest.raises(KeyError, match="unknown stream"):
        Rng(1).draw("magic")


def test_bool_seed_rejected() -> None:
    with pytest.raises(TypeError):
        Rng(True)  # type: ignore[arg-type]


def test_known_splitmix_vector() -> None:
    # Locked output of the documented mixer. Change only with the algorithm.
    assert Rng(42).draw("map") == 0x0CCDFA7E677CF22A
    assert Rng(42).draw("combat") == 0x531C3DABFEF561BA
    assert Rng(42).draw("loot") == 0x8FEB2BD4F73814AB
