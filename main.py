#!/usr/bin/env python3
"""Write the 18 November 2026 world-news front page to /output/entry.png.

The picture is a newspaper-style front page (1024 by 1024, JPEG bytes in a
file named entry.png): a masthead naming Wednesday 18 November 2026, a hero
panel on the Gulf drone attack, four panels -- the Crimea bridge hit, Trump
landing in Manila, Nvidia's record sales, and Cyclone Akvan -- plus a
PIL-drawn world map marking 21 story locations and a 28-item "Around the
world" list, for 33 stories in all. The image was composed for this bounty
(resubmit: denser than the first entry's five stories); this program only
carries it to the output directory unchanged, so both runs write exactly
the same bytes. The output file keeps the name entry.png even though its
bytes are a JPEG -- the gate tells the format from the first bytes, and the
rules allow JPEG in entry.png.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(SRC, dst)
    print(f"wrote {dst} ({dst.stat().st_size} bytes)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
