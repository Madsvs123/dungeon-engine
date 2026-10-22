"""Acting spends 1000 and keeps the leftover energy."""

from __future__ import annotations

from dungeon_engine.scheduler import step


class Record:
    def __init__(self, actor_id: int, speed: int, energy: int = 0) -> None:
        self.id = actor_id
        self.speed = speed
        self.energy = energy


def test_remainder_is_preserved() -> None:
    actor = Record(1, speed=150, energy=0)
    actions: list[int] = []
    for _ in range(7):
        actions.extend(step([actor]))
    assert actions == [1]
    assert actor.energy == 50
