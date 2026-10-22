"""Actors who become ready together act in ascending id order."""

from __future__ import annotations

from dungeon_engine.scheduler import step


class Record:
    def __init__(self, actor_id: int, speed: int, energy: int = 0) -> None:
        self.id = actor_id
        self.speed = speed
        self.energy = energy


def test_tie_break_is_ascending_actor_id() -> None:
    higher = Record(9, speed=100, energy=900)
    lower = Record(2, speed=100, energy=900)
    assert step([higher, lower]) == [2, 9]
    assert higher.energy == 0
    assert lower.energy == 0
