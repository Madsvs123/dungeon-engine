"""Same seed and the same inputs reproduce the state hash."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from dungeon_engine.cli import main
from dungeon_engine.events import Event, EventQueue
from dungeon_engine.runner import run
from dungeon_engine.state import Actor

ROOT = Path(__file__).resolve().parents[1]


def test_same_seed_and_empty_inputs_match() -> None:
    left = run(42, 30, actors=[])
    right = run(42, 30, actors=[])
    assert left.state_hash() == right.state_hash()
    assert left.turn == 30
    assert left.event_log_count == 0
    assert left.actors == []


def test_different_seed_changes_hash() -> None:
    assert run(42, 30, actors=[]).state_hash() != run(43, 30, actors=[]).state_hash()


def test_default_party_is_deterministic() -> None:
    assert run(42, 40).state_hash() == run(42, 40).state_hash()
    assert len(run(1, 0).actors) == 3


def test_seed_stored_mod_2_64() -> None:
    state = run((1 << 64) + 5, 0, actors=[])
    assert state.seed == 5


def test_negative_turns_rejected() -> None:
    with pytest.raises(ValueError):
        run(1, -1, actors=[])


def test_each_action_appends_one_wait_to_the_log() -> None:
    actors = [Actor(id=1, name="solo", speed=1000, energy=0, hp=3)]
    state = run(5, 4, actors=actors)
    assert state.event_log_count == 4
    assert state.turn == 4
    assert actors[0].energy == 0


def test_log_counts_every_actor_action() -> None:
    actors = [
        Actor(id=2, name="b", speed=1000, energy=0, hp=1),
        Actor(id=1, name="a", speed=1000, energy=0, hp=1),
    ]
    state = run(5, 1, actors=actors)
    assert state.event_log_count == 2


def test_acting_actor_emits_wait(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[Event] = []
    real_push = EventQueue.push

    def spy(self: EventQueue, event: Event, priority: int = 0) -> None:
        seen.append(event)
        real_push(self, event, priority)

    monkeypatch.setattr(EventQueue, "push", spy)
    actors = [
        Actor(id=8, name="late", speed=1000, energy=0, hp=1),
        Actor(id=3, name="early", speed=1000, energy=0, hp=1),
    ]
    run(1, 1, actors=actors)
    assert seen == [
        Event(kind="wait", turn=0, actor_id=3, payload=()),
        Event(kind="wait", turn=0, actor_id=8, payload=()),
    ]


def test_cli_prints_one_hash(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["--seed", "42", "--turns", "20", "--hash-out"])
    assert code == 0
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert lines == [run(42, 20).state_hash()]
    assert len(lines[0]) == 64


def test_module_cli_prints_one_hash() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "dungeon_engine", "--seed", "42", "--turns", "500", "--hash-out"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    lines = proc.stdout.splitlines()
    assert lines == [run(42, 500).state_hash()]
