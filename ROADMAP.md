# Roadmap

Steps 1 and 2 are the deterministic turn engine in this repository. The steps below are future work. They are not implemented.

3. Add an entity-component store so actors, items, and tiles are data the turn loop can update without a UI.
4. Define a headless command buffer. The only player input is a list of intents applied at the start of a turn.
5. Introduce a strict tile grid with integer coordinates and blocking flags.
6. Generate one dungeon floor with BSP room splits, drawing only on the map substream.
7. Connect rooms with corridors and reject a floor that is not fully walkable from the stairs.
8. Stack multiple floors and place up and down stairs between them.
9. Compute field of view on the grid from an actor's tile.
10. Track occupancy so two actors cannot share a tile, and closed doors block sight and movement.
11. Resolve melee on the combat substream: a hit check, damage, and a combat event.
12. Apply hit points, armor, and death. Remove a dead actor from the scheduler.
13. Add a hard permadeath toggle. When it is on, death ends the run and records a final hash.
14. Add skills with an energy cost and a cooldown, emitted as events when they are used.
15. Let enemies choose an intent with a deterministic policy. Rolls stay on the combat substream.
16. Represent items and inventories as components, including pickup and drop.
17. Roll loot on the loot substream when a container or a defeated actor is resolved.
18. Equip items into slots and fold their modifiers into attack and speed.
19. Save a run as the canonical state JSON plus the master seed.
20. Replay a run from the seed and the recorded intent list, and require the same final hash.
21. Apply status effects that tick on the actor's action and expire by turn.
22. Add doors, keys, and one interact intent that opens or unlocks.
23. Add hazard tiles that enqueue a damage event when an actor enters them.
24. Give actors a faction, and treat a hostile faction as a legal melee target.
25. Pathfind hostile AI on the grid. Equal-cost ties break by lower x, then lower y.
26. Keep a text transcript of drained events for headless debugging. The engine package still has no UI.
27. Add a separate TUI package that imports the engine and renders the grid. The engine package stays free of UI dependencies.
28. Add a standard run length as configuration for a campaign start. `--turns` stays available on the CLI.
29. Load monster and item tables from plain data files. The tables contain no accounts and no personal data.
30. Add one integration scenario: a seeded floor, a fight, a save, and a replay that matches the hash.
