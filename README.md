# Sunday 22 November 2026 — The World in One Day (35 Stories)

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Iyannn11/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Iyannn11/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

One image that sums up the world's news of **Sunday 22 November 2026** —
35 verified stories across 7 regions, in a Top-1-style broadsheet:
COP31 overtime in Antalya, Verstappen winning the Las Vegas Grand Prix,
and 550 munitions fired at Ukraine overnight, plus a 6-fact strip, a world
map of where it happened, and 22 more stories.

Built for the make.fun bounty
[Sum up 22 November's world news in one image](https://make.fun/bounty/news-image-20261122).

## How it works

`render.py` draws `entry.png` (1024×1024, deterministic — rendering twice
produces identical bytes) from the verified story data in `stories.json`.
`main.ts` (Node 22) copies `entry.png` to the output directory.

```sh
python3 render.py        # draws entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

## Files

- `render.py` — the broadsheet renderer (PIL, system fonts only)
- `stories.json` — all 35 verified stories + map locations + region counts
- `SOURCES.md` — every story's date/source, and the items rejected as not-22-Nov
- `entry.png` — the rendered image
- `main.ts` — entrypoint: copies `entry.png` to the output directory
