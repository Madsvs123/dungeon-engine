"""The debug flag prints seed, turn, and actor count."""

from __future__ import annotations

import pytest

from dungeon_engine.cli import build_parser, main


def test_debug_prints_seed_turn_and_actor_count(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["--seed", "42", "--turns", "500", "--debug"])
    assert code == 0
    assert capsys.readouterr().out == "seed=42 turn=500 actors=3\n"


def test_debug_line_comes_before_the_hash(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["--seed", "42", "--turns", "1", "--debug", "--hash-out"])
    assert code == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "seed=42 turn=1 actors=3"
    assert len(lines) == 2
    assert len(lines[1]) == 64
    int(lines[1], 16)


def test_debug_defaults_off() -> None:
    args = build_parser().parse_args(["--seed", "1", "--turns", "1"])
    assert args.debug is False
    assert args.hash_out is False
