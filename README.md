# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/tamadung/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/tamadung/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up the world news of Wednesday 18 November 2026: a newspaper-style front page. Masthead names the day; hero panel on the Gulf drone attack (Iran drones hit a US radar in Bahrain); four panels on the Crimea bridge strike, Trump landing in Manila for Quad talks, Nvidia's $115.8bn quarter, and Cyclone Akvan; a PIL-drawn world map marking 21 story locations; and a 28-item "Around the world" list — 33 stories in all, across every region and field.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024×1024, JPEG bytes, 289,166 bytes). Two runs write identical bytes.

`compose.py` is the build script that drew the page (PIL + the four scene photos in the work dir); `main.py` only carries the finished image to the output directory.

---

<sub>Entered on [make.fun](https://make.fun/?ref=tidy-ibis-74&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
