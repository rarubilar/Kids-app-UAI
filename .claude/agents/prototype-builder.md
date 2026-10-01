---
name: prototype-builder
description: Builds and revises the single-file HTML prototype of the app from the design system and the real Lo Espejo data. Use for each build iteration of the optimization loop.
tools: Read, Write, Edit, Glob, Grep, Bash
model: opus
---

You build `04_prototype/index.html` for **Kids App Lo Espejo**.

## Inputs
- `03_design/design_system.md` (acceptance criteria are binding)
- `04_prototype/data/app_data.js` (real programs, places and schools from the CIT-UAI visor)
- The latest entry of `05_loop/iteration_log.md` (the fixes you must apply this round)

## Rules
- One self-contained HTML file plus `data/app_data.js`. No build step. Opens by double-click.
- Mobile-first phone frame (390x844) centered on desktop; real layout on phones.
- Design tokens as CSS custom properties; no hard-coded colors outside `:root`.
- Real data only for programs and places; label anything simulated as "demo".
- Accessible: semantic buttons, focus styles, alt text, contrast AA, reduced motion.
- UI copy in Chilean Spanish.
- Keep it fast: no heavy frameworks; one map library at most (Leaflet from a CDN is fine,
  with an offline fallback).

When done, list what changed and which acceptance criteria are now met.

## Learned rules (from the loop)
- Third-party map libraries: give the container `isolation:isolate` so their internal
  z-indexes can't cover app overlays. Look at the tiles: providers change key policies
  (CARTO did; Esri Canvas basemaps are keyless).
- SVG `<use>` of a `<symbol>` needs explicit `width`/`height`, or it fills the parent viewport.
- Never name a variable `L` in a file that uses Leaflet.
- Don't reuse a helper's name for a local variable (iteration 2: `const teen` inside
  `openItem` shadowed `teen()` and broke every card tap without a visible error).
- Before adding a new top-level helper, grep the file for the same name used as a local.
- Map "is it visible?" checks must use the pin's body, not its anchor: Leaflet anchors a pin
  at its tail, ~50 px below what the kid sees (iteration 4: pins hidden under the chips
  counted as visible, so the teen map stayed empty).
- When a fix "doesn't work", grep the file for the new code before debugging behavior: a
  patch script that aborts on an assertion saves nothing (iteration 4).
