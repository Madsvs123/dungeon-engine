# dungeon-engine

`dungeon-engine` is a deterministic turn engine for a future roguelike. Steps 1 and 2 are in this repository: seeded substreams, an energy scheduler, a priority event queue, a canonical state hash, and a headless command-line runner. Later systems are listed in `ROADMAP.md` and are not implemented.

## Who it is for

This project is for the author, who is the sole owner. There are no player accounts, and the engine stores no personal data.

## Language

Python 3, standard library only. The `dungeon_engine` package has zero UI dependencies. The CLI uses `argparse`. Randomness is an explicit SplitMix64 generator in `dungeon_engine/rng.py`, not `random.Random`.

## Run

From this directory:

```
py -3 -m dungeon_engine --seed 42 --turns 500 --hash-out
```

The process prints one SHA-256 hex digest of the final state.

With `--debug`, the process prints one line, `seed=<seed> turn=<turn> actors=<count>`. If `--hash-out` is also set, that line comes first and the hash follows.

```
py -3 -m dungeon_engine --seed 42 --turns 500 --debug
```

The CLI runs a fixed party of three actors (`wanderer`, `guard`, `scout`). `dungeon_engine.runner.run` accepts an explicit actor list, including an empty one.

## Test

Install pytest, then run the suite from this directory:

```
py -3 -m pip install pytest
py -3 -m pytest
```

## Design defaults

- **Run length.** You pass `--turns`. A standard campaign length is future work.
- **Permadeath.** Not in this slice. When combat exists, the default will be a hard permadeath toggle.
- **Space.** Future maps are a strict grid.
- **Determinism.** The same seed and the same inputs always produce the same `state_hash`.

Energy, event drain, and the hash are specified in `docs/ARCHITECTURE.md`.

## License

MIT License. Copyright 2026 Madsvs123. See `LICENSE`.
