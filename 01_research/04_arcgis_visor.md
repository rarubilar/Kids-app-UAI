# What the CIT-UAI visor already has (and what it doesn't)

*Author: orchestrator. Snapshot taken 2026-09-28 with `tools/extract_arcgis.py` and
`tools/extract_osm.py`; the app dataset is built with `tools/build_app_data.py`.*

## 1. The visor

"OPORTUNIDADES NNA COMUNIDAD" is an ArcGIS Experience Builder app owned by
`CIT_UAI_PROYECTOS` (culture `es-cl`, public, about 3,140 views). It has one page, "Visor",
built on the web map **MAPA_EL_SAUCE** (item `624a05d73dc24fa6b3a4b7b32ce8bea2`) with a
satellite basemap, plus charts by category, implementing organization and age by
unidad vecinal, and a program search by category.

It's a **planner's tool**: it answers "what exists and where". The app we're designing is the
**kid's side of the same data**: it answers "what can I do near me today", and it sends back
what the visor can't know, which is what kids actually use, want and miss.

## 2. Layer inventory

| Layer (service) | Records | Geometry | What it's good for in the app |
|---|---:|---|---|
| Programas_Lo_Espejo_NNA_vista (public view) | 108 | point | **Core content**: activities and help entry points |
| Programas_Lo_Espejo_NNA (editable) | 269 | point | Municipal editing source; the view is a filtered subset |
| Resumen_Programas_Lo_Espejo | 149 | point | Earlier consolidated list with corrected names |
| RESUMEN_PROG_LE (table) | 85 | none | Category / organization summary |
| UV_LO_ESPEJO | 15 | polygon | Unidades vecinales: the unit for aggregating kid data |
| MZ_UV_LO_ESPEJO | 807 | polygon | **Censo 2024 by block**: kids 6-13 and 14-17, connectivity, households |
| MBHT_2017_Lo_Espejo | 765 | polygon | Human wellbeing matrix (Censo 2017 base): access, social, environment, safety |
| EL_SAUCE_Shape_contexto | 36 schools, 56 sport venues, 25 kindergartens, 9 health, 7 services, 3 police, 3 fire, 1 PDI | point | Places layer; schools for onboarding |
| Beneficiarios_programas | 1 (empty) | point | **Do not use**. See section 5 |

## 3. Programs: what's in them

108 confirmed programs, by category: sport and recreation 46, specific support and social
protection 20, health 14, education and scholarships 13, arts and culture 8, social and
community development 3, personal development 3, public space 1. The main owner is the
Municipality (68), followed by Fundación El Sauce (15) and national ministries.

After filtering for the app (`build_app_data.py`):

| Result | Count | Rule |
|---|---:|---|
| Activities shown to kids | **33 activities, 55 program records, 39 venues** | audience overlaps ages 8-17; free |
| Help entry points | 8 | OLN, Oficina de Juventud, CESFAM x4, CESAM, Ruka PESPI |
| Excluded: protection and health by referral | 27 | PPF, PIE, DAM, PDE, SENDA, etc. Kids reach them through adults. Listing them beside "futsal" would stigmatize |
| Excluded: adults, caregivers, organizations | 12 | e.g. pet sterilization, community funds |
| Excluded: age outside 8-17 | 6 | kindergartens, seniors |

The real offer is strong and varied: futsal (8 sites), Programa Barrio (Fútbol Más, 3
sites, 16:00-19:30), hockey, tennis, figure skating, parkour, bouldering and calisthenics
(Plaza Libre), **palín** (Mapuche sport), martial arts, ballet, cheerleading, school rock
band, batucada, robotics, and a pre-university course.

## 4. Supply vs. demand by unidad vecinal

Kids 8-17 estimated from Censo 2024 blocks (6-13 x 0.75 + 14-17, uniform-age assumption).
"Places" are **distinct venues** with at least one kid-facing workshop (the 55 program records
collapse into 39 venues, because several workshops share a gym or school). Parks from OSM;
courts from the CIT-UAI sport layer. The prototype's municipal view computes the same table live.

| UV | Kids 8-17 | Places with workshops | Of them, for ≤12 | Kids per place | Parks + playgrounds | Courts |
|---|---:|---:|---:|---:|---:|---:|
| 37B | 1,936 | 9 | 7 | 215 | 11 | 6 |
| 37C | 1,389 | 6 | 4 | 232 | 11 | 11 |
| 26 | 1,260 | 3 | 3 | 420 | 8 | 8 |
| **24** | **1,182** | **2** | **0** | **591** | 2 | 9 |
| **29** | **897** | **2** | 1 | **448** | 1 | 2 |
| **36** | **893** | **1** | 1 | **893** | 4 | 4 |
| 31 | 841 | 2 | 2 | 420 | 4 | 4 |
| 35 | 764 | 2 | 2 | 382 | 4 | 5 |
| 37A | 676 | 2 | 2 | 338 | 3 | 1 |
| 25 | 579 | 4 | 3 | 145 | 4 | 6 |
| 28 | 294 | 1 | 1 | 294 | 0 | 1 |
| 34 | 193 | 2 | 1 | 96 | 3 | 1 |
| 30 | 150 | 0 | 0 | - | 0 | 0 |
| 32 | 105 | 1 | 0 | 105 | 1 | 0 |
| 27 | 37 | 1 | 1 | 37 | 2 | 0 |
| **Total** | **≈11,200** | **38** (+1 just outside) | | **≈290** | 58 | 58 |

**Reading it.** UV 24 has the fourth-largest child population and nine courts, but only two
workshop venues and none for under-13s: the infrastructure exists, the programming doesn't.
UVs 36 and 29 are the other "offer deserts", and UVs 26 and 31 are stretched (≈420 kids per
venue). UV 24 and 29 are both populous and under-served, which makes them the natural pilot
(see `00_system/GUIDE.md` §B4).

Caveat: venues are the program addresses the municipality recorded; a program at a school
may serve kids from several UVs. The app will measure real catchment (which UV kids come
from) with coarse, consented check-ins, which the visor can't do today.

## 5. Data quality and governance issues found

1. **Public layer designed for minors' personal data.** `Beneficiarios_programas` is shared
   publicly and has fields for first and last names, age, birth date, gender, address,
   program, national ID number (RUT) and nationality. Today it holds one empty record, so
   nothing is exposed, but anything entered later would be public. Recommendation: make it
   private now, or delete it. Beneficiary lists must never live in a public feature service.
   `extract_arcgis.py` keeps only its schema.
2. **Officials' contact details** (name, email, phone) are in the public programs view.
   The app shows the unit (e.g. "Oficina de Deportes"), not the person.
3. **Schedule is filled in 9 of 108 programs, capacity in 7.** A kid can't decide without
   "when". Minimum fields to add: `dias`, `hora_inicio`, `hora_fin`, `edad_min`,
   `edad_max`, `cupos`, `inscripcion` (how to join), `costo`, `vigente_hasta`.
4. **Age is free text** ("desde los 7 hasta los 17 años", "Niños y niñas de 5 10años").
   The build script parses it, but structured `edad_min`/`edad_max` fields are needed.
5. **No events layer** (concerts, fairs, tournaments) and **no parks or bike-lane layers**.
   Parks, playgrounds, bike lanes, the municipal library and the Anfiteatro Violeta Parra
   come from OpenStreetMap. Only 7 bike-lane segments are mapped inside the comuna: either
   OSM is incomplete or the network is really that thin. The app can ask kids where they'd
   ride.
6. **Duplicate program records** by site (Zumba appears 10 times). The app groups them into
   one activity with several sites.

## 6. What the app gives back to this visor

| New layer, published back to CIT-UAI's ArcGIS | Grain | Answers |
|---|---|---|
| Check-ins per place per week | place, week, age band (k ≥ 10) | Which places kids actually use |
| Interest vs. offer | UV, activity type | Which activities are wanted where none exist |
| Place ratings and "what's missing" tags | place | Lighting, shade, bathrooms, safety perception |
| Catchment | origin UV → destination place | How far kids travel and from where |
| Program demand | program, month | Saves, "I'm going", sign-up intents |

See `02_platform/platform_architecture.md` for how this data is collected and protected.

## Sources

- CIT-UAI. (2026). *OPORTUNIDADES NNA COMUNIDAD* [ArcGIS Experience]. Retrieved September 28, 2026, from https://experience.arcgis.com/experience/27567a41504b4bb9a488e677e846fb4f
- Instituto Nacional de Estadísticas. (2025). *Censo de Población y Vivienda 2024: resultados por manzana* [Data set], via CIT-UAI layer MZ_UV_LO_ESPEJO.
- OpenStreetMap contributors. (2026). *OpenStreetMap* [Data set, ODbL]. Retrieved September 28, 2026, via Overpass API.
