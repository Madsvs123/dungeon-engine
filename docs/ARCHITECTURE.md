# Architecture

This slice is a headless turn loop. It does not generate maps, resolve combat, or draw a UI.

## Energy

`THRESHOLD` is 1000. One scheduler step adds each actor's `speed` to that actor's `energy`. While any actor has `energy >= 1000`, those actors form a wave. The wave is sorted by ascending `id`. Each actor in the wave subtracts 1000 and is appended to the action list. Leftover energy stays. If a leftover is still `>= 1000`, that actor is in the next wave of the same step. The step returns actor ids in action order, and an id can repeat.

A faster actor can therefore act twice before a slower one acts once. With speeds 300 and 100, both starting at 0:

- Step 4: the fast actor spends 1200 down to 200. The slow actor is at 400.
- Step 7: the fast actor spends 1100 down to 100. The slow actor is at 700 and has not acted.

Remainder: speed 150 from 0 reaches 1050 on step 7, spends 1000, and keeps 50.

Tie: two actors who reach 1000 on the same wave act in ascending id order, whatever order they were stored in.

## Event drain

`Event` is a frozen dataclass: `kind`, `turn`, `actor_id`, `payload`. `payload` is a tuple. `EventQueue.push` appends to a priority band. `drain` builds a new list by walking bands from the smallest priority number to the largest, FIFO inside each band, then clears the queue.

The runner pushes one `wait` event per action at priority 0. The event's turn is the state's turn index before that index increments. `drain` then runs, `event_log_count` grows by the drained length, and `turn` increments by one. Drained events are not stored on the state. Only the count is.

## Hash

`state_hash` is the lowercase SHA-256 hex digest of UTF-8 JSON from `json.dumps` with `sort_keys=True`, `separators=(",", ":")`, `ensure_ascii=True`, and `allow_nan=False`.

The object is:

- `seed` (int, master seed modulo 2**64)
- `turn` (int)
- `event_log_count` (int)
- `rng_counters` with exactly the keys `combat`, `loot`, and `map`
- `actors`, sorted by `id`, each with `energy`, `hp`, `id`, `name`, and `speed`

No set is serialized. Actor input order does not change the hash. A wait does not draw, so in this slice the counters stay zero. The seed is still inside the hash, and each substream advances only when something draws from it.
