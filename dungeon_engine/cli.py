"""Command-line interface.

``--seed`` and ``--turns`` are required. ``--hash-out`` prints the SHA-256
state hash as one hex line on stdout. ``--debug`` prints
``seed=<seed> turn=<turn> actors=<count>`` and, when both flags are set,
prints that line before the hash.
"""

from __future__ import annotations

import argparse

from dungeon_engine.runner import run

__all__ = ["build_parser", "main"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dungeon_engine",
        description="Run the deterministic turn engine.",
    )
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--turns", type=int, required=True)
    parser.add_argument(
        "--hash-out",
        action="store_true",
        help="Print the SHA-256 state hash.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print seed, turn, and actor count.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    state = run(args.seed, args.turns)
    if args.debug:
        print(f"seed={state.seed} turn={state.turn} actors={len(state.actors)}")
    if args.hash_out:
        print(state.state_hash())
    return 0
