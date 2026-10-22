"""Entry point for ``python -m dungeon_engine``."""

from __future__ import annotations

import sys

from dungeon_engine.cli import main

if __name__ == "__main__":
    sys.exit(main())
