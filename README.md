[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Iyannn11/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Iyannn11/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Day — Sunday 22 November 2026

**50 verified stories · 7 regions · every one dated Sunday 22 November 2026.**

A single-image broadsheet summing up the world news of Sunday 22 November 2026: COP31 in overtime in Antalya, Russia's overnight attack on Ukraine, Verstappen winning the Las Vegas Grand Prix, India piling up a record Test total in New Zealand, a factory fire in Indonesia, floods in Gaza, and 44 more stories from every region — plus a world map showing where each one happened.

Built for the [make.fun bounty — Sum up 22 November's world news in one image](https://make.fun/bounty/news-image-20261122).

## How it was made

- `stories.json` — the 50 verified stories (headline, region, map location) with sources in `SOURCES.md`.
- `render.py` — draws `entry.png` (1024×1024, deterministic) from `stories.json` with PIL.
- `main.ts` — copies `entry.png` to `/output/entry.png`.

## Reproduce

```sh
python3 render.py        # writes entry.png (deterministic — same sha256 every run)
npx tsx main.ts          # writes /output/entry.png
```

## Date check

Every story was checked against its source: it happened, or was first reported, on Sunday 22 November 2026. Stories dated 21 November or earlier were rejected — the full rejection list is in `SOURCES.md`.
