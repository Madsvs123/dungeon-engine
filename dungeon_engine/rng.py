"""SplitMix64 substreams for map, combat, and loot.

Arithmetic is modulo 2**64. This module does not use ``random``.

SplitMix64 step (Steele, Lea, Flood):

- ``state = (state + 0x9E3779B97F4A7C15) mod 2**64``
- ``z = state``
- ``z = (z xor (z >> 30)) * 0xBF58476D1CE4E5B9 mod 2**64``
- ``z = (z xor (z >> 27)) * 0x94D049BB133111EB mod 2**64``
- ``output = z xor (z >> 31)``

Domain separation: the master seed is not a stream and does not advance when
a substream is drawn. Each named substream gets its own state, derived once:

- ``state = master_seed mod 2**64``
- for each byte ``b`` in the UTF-8 stream name, add ``b + 1`` (mod 2**64),
  then replace ``state`` with the internal state of one SplitMix64 step
  (the step's output is discarded)
- that internal state is the substream's initial state

``Rng.draw(name)`` runs one SplitMix64 step on that substream only and adds
one to that substream's counter. ``Rng.counters`` returns a new dict.

Example::

    rng = Rng(42)
    first_map = rng.draw("map")
    first_combat = rng.draw("combat")  # the second map draw is still pending
"""

from __future__ import annotations

__all__ = ["STREAMS", "Rng"]

_MASK = (1 << 64) - 1
_GOLDEN = 0x9E3779B97F4A7C15
_MIX_1 = 0xBF58476D1CE4E5B9
_MIX_2 = 0x94D049BB133111EB

STREAMS = ("map", "combat", "loot")


def _splitmix64_step(state: int) -> tuple[int, int]:
    """Return ``(next_state, output)`` for one SplitMix64 step."""
    state = (state + _GOLDEN) & _MASK
    z = state
    z = ((z ^ (z >> 30)) * _MIX_1) & _MASK
    z = ((z ^ (z >> 27)) * _MIX_2) & _MASK
    output = (z ^ (z >> 31)) & _MASK
    return state, output


def _derive_state(master_seed: int, name: str) -> int:
    state = master_seed & _MASK
    for byte in name.encode("utf-8"):
        state = (state + byte + 1) & _MASK
        state, _output = _splitmix64_step(state)
    return state


class _Substream:
    def __init__(self, state: int) -> None:
        self.state = state & _MASK
        self.draws = 0

    def next_u64(self) -> int:
        self.state, value = _splitmix64_step(self.state)
        self.draws += 1
        return value


class Rng:
    """Master seed plus independent map, combat, and loot substreams."""

    def __init__(self, seed: int) -> None:
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise TypeError("seed must be an int")
        self.seed = seed & _MASK
        self._streams = {
            name: _Substream(_derive_state(self.seed, name)) for name in STREAMS
        }

    def draw(self, stream: str) -> int:
        """Next unsigned 64-bit value from ``stream``. Other streams stay put."""
        try:
            substream = self._streams[stream]
        except KeyError:
            known = ", ".join(STREAMS)
            raise KeyError(f"unknown stream {stream!r}; expected one of {known}") from None
        return substream.next_u64()

    def counters(self) -> dict[str, int]:
        """Draw counts for each stream. A new dict on every call."""
        return {name: substream.draws for name, substream in self._streams.items()}
