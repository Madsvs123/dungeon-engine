"""Frozen events and a priority-band queue.

``Event`` is a frozen dataclass. ``payload`` is a tuple so the record stays
immutable. ``EventQueue`` keeps one FIFO list per priority band. ``drain``
walks bands from the smallest priority number to the largest, preserves push
order inside a band, returns a new list, and clears the queue.

Example::

    queue = EventQueue()
    queue.push(Event("wait", 0, 1), priority=1)
    queue.push(Event("hit", 0, 2), priority=0)
    queue.drain()  # hit first, then wait; the queue is empty afterwards
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

__all__ = ["Event", "EventQueue"]


@dataclass(frozen=True, slots=True)
class Event:
    kind: str
    turn: int
    actor_id: int
    payload: tuple[Any, ...] = ()


class EventQueue:
    """Priority bands with FIFO order inside each band."""

    def __init__(self) -> None:
        self._bands: dict[int, list[Event]] = {}

    def push(self, event: Event, priority: int = 0) -> None:
        if not isinstance(event, Event):
            raise TypeError("event must be an Event")
        if isinstance(priority, bool) or not isinstance(priority, int):
            raise TypeError("priority must be an int")
        band = self._bands.get(priority)
        if band is None:
            band = []
            self._bands[priority] = band
        band.append(event)

    def drain(self) -> list[Event]:
        """Return a new list of every queued event, then clear the queue."""
        ordered: list[Event] = []
        for priority in sorted(self._bands):
            ordered.extend(self._bands[priority])
        self._bands.clear()
        return ordered

    def __len__(self) -> int:
        return sum(len(band) for band in self._bands.values())
