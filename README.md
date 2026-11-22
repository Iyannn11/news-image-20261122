[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Iyannn11/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Iyannn11/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# Sunday 22 November 2026 — The World in One Day

One image that sums up the world's news of Sunday 22 November 2026:
**11 verified stories across 6 regions**, every one numbered, dated and sourced.

A broadsheet front page in the Top-1 style: a strong masthead and deck, a
facts strip with big numerals, region colour bars, 3 big story cards plus 8
smaller cards, a "Where it happened" world map with numbered dots, and a
DATE CHECK box that names what was deliberately left out — including the
EU–Indonesia trade deal, El Chapo Isidro's capture and the Peru quake, all
of which were Saturday 21 November's news, not Sunday's.

**Early edition:** this page was drawn at about 03:00 UTC, only a few hours
into the day in most time zones, so it carries the stories that had happened
or been first reported by then. A later edition can add the rest of the day
(the Las Vegas Grand Prix, the Pope's Angelus, Sunday football). Nothing on
the page is invented and nothing is borrowed from another day: every story
was checked against its publication date before it was drawn.

## Layout

- Masthead + deck naming the three biggest stories
- Facts strip: 550 munitions · 5 killed · 856 candidates · $60,073 bitcoin ·
  123 Head · 90mm rain
- Region bars: Europe 2 · Asia 2 · Middle East 3 · Americas 1 ·
  Oceania 1 · Global 2
- 3 big story cards (Russia attack, COP31, Ashes) + 8 smaller cards
- "Where it happened" world map with numbered dots for stories 1–11
- DATE CHECK: what was left out on purpose, and why

## Files

- `entry.png` — the front page, 1024×1024, rendered by `render.py`
- `render.py` — draws the page with Pillow (stdlib + PIL at build time only)
- `main.ts` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`),
  with a 1 MiB size guard
- `SOURCES.md` — every story with its source and date verification

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Entry for the [news-image-20261122 bounty on make.fun](https://make.fun/bounty/news-image-20261122).
