"""Priority bands drain in order, FIFO inside a band."""

from __future__ import annotations

import pytest

from dungeon_engine.events import Event, EventQueue


def test_two_priorities_and_fifo_inside_a_band() -> None:
    queue = EventQueue()
    low_first = Event("hit", 0, 3)
    high_first = Event("wait", 0, 9)
    low_second = Event("hit", 0, 1)
    high_second = Event("wait", 0, 2)
    queue.push(low_first, priority=1)
    queue.push(high_first, priority=0)
    queue.push(low_second, priority=1)
    queue.push(high_second, priority=0)
    assert queue.drain() == [high_first, high_second, low_first, low_second]


def test_same_band_is_fifo_not_actor_id_order() -> None:
    queue = EventQueue()
    later_id = Event("hit", 1, 1)
    earlier_push = Event("hit", 1, 9)
    queue.push(earlier_push, 0)
    queue.push(later_id, 0)
    assert queue.drain() == [earlier_push, later_id]


def test_drain_returns_a_new_list_and_clears() -> None:
    queue = EventQueue()
    event = Event("wait", 0, 1)
    queue.push(event)
    drained = queue.drain()
    assert drained == [event]
    drained.append(Event("extra", 0, 2))
    assert len(queue) == 0
    assert queue.drain() == []


def test_push_requires_event_and_int_priority() -> None:
    queue = EventQueue()
    with pytest.raises(TypeError):
        queue.push("nope")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        queue.push(Event("wait", 0, 1), priority=True)  # type: ignore[arg-type]
