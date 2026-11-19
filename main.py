#!/usr/bin/env python3
"""Write the 18 November 2026 world-news front page to /output/entry.png.

The picture is a newspaper-style front page (1024 by 1024, PNG,
501,097 bytes): a masthead naming Wednesday 18 November 2026, a region
bar and a field bar counting all 42 stories, a "day in numbers" strip,
13 core stories each with its own flat-illustration panel (kicker +
headline + deck), a large PIL-drawn world map with 13 numbered pins tied
to the core stories plus gold dots for the rest, a 29-item "Also on
Wednesday 18 November" list, and a date-check box naming the stories
deliberately left out because they were first reported on 17 November.
42 stories in all. The image was composed for this bounty (round 3: a
total rebuild on the winning template — flat illustrations, not photos);
this program only carries it to the output directory unchanged, so both
runs write exactly the same bytes.
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
