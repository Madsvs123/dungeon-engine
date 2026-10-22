"""Speed decides how often an actor acts in one step sequence."""

from __future__ import annotations

from dungeon_engine.scheduler import THRESHOLD, step


class Record:
    def __init__(self, actor_id: int, speed: int, energy: int = 0) -> None:
        self.id = actor_id
        self.speed = speed
        self.energy = energy


def test_threshold_is_1000() -> None:
    assert THRESHOLD == 1000


def test_empty_roster() -> None:
    assert step([]) == []


def test_exact_threshold_spends_1000() -> None:
    actor = Record(7, speed=1000, energy=0)
    assert step([actor]) == [7]
    assert actor.energy == 0


def test_speed_is_added_before_the_check() -> None:
    actor = Record(1, speed=100, energy=900)
    assert step([actor]) == [1]
    assert actor.energy == 0


def test_faster_actor_acts_twice_before_slower_one() -> None:
    # Id 9 is faster. Id 1 would win a tie, and still has not acted after
    # the fast actor's second action.
    fast = Record(9, speed=300)
    slow = Record(1, speed=100)
    actions: list[int] = []
    for _ in range(7):
        actions.extend(step([slow, fast]))
    assert actions == [9, 9]
    assert fast.energy == 100
    assert slow.energy == 700
    assert slow.energy < THRESHOLD
