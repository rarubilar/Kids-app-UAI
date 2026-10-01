# Kids App Lo Espejo → **Reflejo**

The map of Lo Espejo for kids and teens aged 8-17: find something to do nearby, go, check in
at the real place, and tell the city what's missing. The municipality and CIT-UAI see how kids
use the city, in anonymous totals, and use it to improve programs and public space.

**Open the prototype:** double-click `04_prototype/index.html` (needs internet for fonts and
map tiles; everything else is local). On a desktop you get a presenter panel with demo
controls; on a phone it runs full screen.

---

## What's in this folder

| Folder | What | Start with |
|---|---|---|
| `00_system/` | How the agent system works, and a guide to the whole project | `GUIDE.md`, `ORCHESTRATION.md` |
| `.claude/agents/` | The 7 specialist agents (Claude Code subagents) | one file per role |
| `01_research/` | Demographics, 5 psychology papers, app benchmark, CIT-UAI visor analysis | each file ends in a **Handoff** section |
| `02_platform/` | Backend, data pipeline, privacy law, sizing, costs, roadmap | `platform_architecture.md` |
| `03_design/` | UX strategy and design system (tokens, type, motion, copy) | `design_system.md` |
| `04_prototype/` | The HTML prototype, its real data and screenshots of every iteration | `index.html` |
| `05_loop/` | The optimization loop: rubric, and the log of every iteration | `LOOP.md`, `iteration_log.md` |
| `data/raw/` | Snapshot of the CIT-UAI ArcGIS layers and OpenStreetMap | `_summary.json` |
| `tools/` | Scripts to refresh data, rebuild the app dataset, and screenshot the prototype | see below |

## The loop, in numbers

| Iteration | Scored by | Score /100 |
|---|---|---:|
| 1 | builder | 67 |
| 2 | builder | 78 (inflated) |
| 3 | independent critic | 62 |
| 4 | builder, measured | 76 |
| 5 | independent critic | **78**, stop rule met |

Plus a post-review patch for the critic's last five defects. Every screen state is audited for
touch targets (48×48), text size, WCAG contrast and layout leaks: all zero at the end.
Details: `05_loop/iteration_log.md`.

## Key findings

- **≈11,200 kids aged 8-17** live in Lo Espejo (Censo 2024 blocks), 59% of them under 14, so
  guardian consent (Ley 21.719, in force 1 Dec 2026) is the default path, not an edge case.
- **Phones, not computers:** 91% of households have internet but only 43% have a computer.
- **The offer is real but invisible:** 33 free workshops for this age at 39 venues (futsal,
  hockey, tennis, figure skating, parkour, bouldering, palín, rock band, batucada, robotics,
  ballet...). Only 9 of 108 programs publish a schedule.
- **Offer deserts:** UV 24 has 1,182 kids and no workshop for under-13s; UV 36 has 893 kids per
  venue. Recommended pilot: UV 24 + 29, with 37B as comparison.
- **Governance risk found:** a public ArcGIS layer is designed to hold minors' names, RUT and
  birth dates (empty today). Make it private before it's used.
- **Closest analogue:** Helsinki's Harrastuspassi (Finnish model for leisure). No Chilean
  comuna has a map-based youth app.
- **Infrastructure is cheap** (≈US$400-1,500/year); the real cost is people for content,
  moderation and community work.

## What a production team should do next (final critic + guide)

1. Signed, rotating QR signs at the pilot venues; one rating per kid per place; test with ~30 kids.
2. A data protection impact assessment under Ley 21.719 and real guardian verification.
3. Programs publish structured schedules (47 of 55 sites have no days today).
4. Accessibility and performance checks in CI, on a cheap Android, in both themes.
5. A named municipal owner and response time for "Responder a los niños".

More in `00_system/GUIDE.md` §5.

## Refreshing the data

```bash
python tools/extract_arcgis.py    # CIT-UAI visor layers  -> data/raw/
python tools/extract_osm.py       # parks, playgrounds, bike lanes (OSM) -> data/raw/
python tools/build_app_data.py    # -> 04_prototype/data/app_data.js
bash tools/shoot.sh <N>           # screenshots of every screen -> 04_prototype/screenshots/iter-N/
```

## Sources and honesty notes

Real: programs, places, schools, unidades vecinales and census counts. Simulated and labeled
"demo" in the UI: events, usage numbers in the municipal view, friends, and "what's missing"
percentages. Legal analysis should be reviewed by the municipality's legal team before launch.
Help-screen lines were checked on 2026-09-28: 147 Fono Niños (Carabineros, free, 24 h;
ChileAtiende) and *4141 (MINSAL, free, 24 h); re-check them before launch.
