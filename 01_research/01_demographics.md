# Demographics research — Kids App Lo Espejo

**Question:** Who are the 8–17 year olds of Lo Espejo, where are they, and what does that mean for the app?
**Prepared by:** demographics-analyst · **Date:** 2026-09-28

---

## 0. Data provenance — verifying the orchestrator's baseline

### 0.1 `manzanas_uv.geojson` is Censo 2024, not Censo 2017

Three independent checks confirm this:

1. **Population match.** Summing `n_per` across the 807 blocks gives **85,958**. INE's *official* Censo 2024 count for Lo Espejo, republished by the Biblioteca del Congreso Nacional (BCN, 2025), is **87,295**. The block sum is 98.5% of the official total (gap of 1,337 people, 1.5%) — consistent with INE's standard statistical-secrecy masking of very small blocks plus ~138 zero-population blocks (industrial/park parcels) in the file. Compare this to Censo 2017's official comunal count of **98,804** (BCN, 2025) — 15% higher than the block sum, i.e., the wrong census entirely.
2. **The Afrodescendant field.** The dataset carries `n_afrodesc` with real, non-trivial values (comuna total 679, 0.79% of population). Chile's census **never had a direct Afrodescendant self-identification question before 2024**: in Censo 2017 only a generic "Otro" write-in under the Indigenous-peoples question let 9,919 people nationwide (0.06%) self-describe as Afrodescendant (Iraguen, n.d.; Observatorio Ciudadano, n.d.). A dedicated Afrodescendant question was added nationwide only for Censo 2024, implementing Ley 21.151 (2019); nationally 174,190 people (0.94%) identified as Afrodescendant (INE, 2025b). A comuna in the Metropolitan Region (not Arica, where a 2017 pilot ran) reporting a real `n_afrodesc` count is only possible if this is 2024 data.
3. **Age-band cross-check.** Our block sums (0–5: 5,196; 6–13: 8,767; 14: ~1,155 of the 4,622 in the 14–17 band) imply an "0–14" total of ≈15,118, versus INE's official Censo 2024 "0–14" figure of 15,405 (BCN, 2025) — a 1.9% gap, in the same direction and magnitude as the total-population gap above. Censo 2017's 0–14 band would be much larger (Lo Espejo's population fell 11.6% between censuses; see §1).

The `n_serv_tel`/`n_serv_com`/`n_serv_tab`/`n_internet` fields (household telephone/computer/tablet/internet) do **not** by themselves prove the census year — Censo 2017's public 21-question summary does not appear to include a household-ICT block (BioBioChile, 2017; t13, 2017), but I could not obtain Censo 2017's ICT questionnaire directly, so I flag this as suggestive, not decisive, evidence. The population and Afrodescendant checks above are decisive.

**Conclusion: `manzanas_uv.geojson` = Censo 2024 (INE), block level, 807 manzanas across the 15 official unidades vecinales (UV) of Lo Espejo.** Field meanings, confirmed against INE's Censo 2024 documentation and cross-checked against household totals in the data itself: `n_serv_tel` = households with telephone (fixed or mobile), `n_serv_com` = households with a computer, `n_serv_tab` = households with a tablet, `n_serv_int`/`n_internet` = households with internet access. (Inferred as household-level, not person-level: in the sample block used to verify, `n_hog`=184 households and `n_serv_tel`=176, `n_internet`=170 — values close to but below the household count, as expected for household equipment/services penetration rather than a person count.)

### 0.2 Does 85,958 (or 87,295) cover the whole comuna?

Yes, with the caveat above. INE's Censo 2024 comunal total for Lo Espejo is **87,295** (BCN, 2025), 100% urban (Lo Espejo has no rural population). The 15 unidades vecinales in `unidades_vecinales.geojson` are the municipality's full official territorial division, and the 807 blocks in `manzanas_uv.geojson` are the full block inventory for those 15 UVs. The 1.5% shortfall versus the INE comunal total is very likely INE's small-block statistical-disclosure masking (common in Chilean block-level Censo releases) rather than missing territory.

**A striking finding while verifying this: Lo Espejo's population fell 11.6% between Censo 2017 (98,804) and Censo 2024 (87,295), while Chile's population grew 5.2% nationally over the same period (17,574,003 → 18,480,432)** (BCN, 2025; INE, 2025a; t13, 2017). I found no Lo Espejo-specific study confirming the cause; a plausible but unverified hypothesis is the demolition/regeneration of aging social-housing blocks under MINVU's national "Regeneración de Conjuntos Habitacionales" program, which Lo Espejo has been part of, combined with out-migration — **this is a genuine gap**, not a sourced fact, and matters because INE's own 2020-vintage population *projection* for 2024 (100,694, cited in some secondary reports) overshot the real Censo 2024 count by 15%, showing pre-census planning figures for this comuna were unreliable.

### 0.3 What is the MBHT (`mbht_2017.geojson`)?

The **Matriz de Bienestar Humano Territorial (MBHT)** is a territorial-wellbeing index built by the **Centro de Inteligencia Territorial of Universidad Adolfo Ibáñez (CIT-UAI)** — the same team behind this project's visor data — and hosted/distributed through Chile's Subsecretaría de Desarrollo Regional y Administrativo (SUBDERE) at plataformabht.subdere.gov.cl and matrizbht.cl (Asimov Consultores, n.d.; CIT-UAI, n.d.-a; SUBDERE/MBHT, n.d.). It aggregates roughly 18 base indicators, built primarily from **Censo 2017** data plus MINEDUC, MINAGRI, satellite imagery and OpenStreetMap, into four dimensions present in our file as `dim_acc` (accessibility), `dim_soc` (socioeconomic), `dim_amb` (environmental/community assets) and `dim_seg` (security), which are combined via multicriteria aggregation into a single **BHT index from 0 (worst) to 1 (best)** at the census-block level, with a categorical tier (`tob`: tramo de bienestar — Bajo/Medio/Alto) (SUBDERE/MBHT, n.d.).

For Lo Espejo's 765 MBHT blocks: mean BHT = **0.54** (min 0.30, max 0.69); dimension means: accessibility 0.62, socioeconomic 0.56, environmental 0.66, security 0.74. **Not one of the 765 blocks is classified "Alto" (high wellbeing): 528 blocks (69%) are "Bajo" (low) and 237 (31%) are "Medio" (medium)** — a whole-comuna ceiling that is itself a finding: by CIT-UAI's own territorial-wellbeing metric, no part of Lo Espejo reaches the top tier. `persons` sums to 98,650, matching Censo 2017's 98,804 within 0.16% (same masking pattern as §0.1), confirming the 2017 vintage. `e4a18` = 19,821 is the **2017** population aged 4–18 (15 single ages), a different age band and a different, larger-population year than our 2024-based 8–17 estimate — see §1.3 for a cross-check using both datasets together.

Note: CIT-UAI separately runs a specific "Mapa de Oportunidades de Bienestar para la Niñez" for Lo Espejo, developed with the municipality and Fundación El Sauce (CIT-UAI, n.d.-b) — this is very likely the umbrella project this visor snapshot belongs to, though I could not confirm the manzanas_uv/MBHT layers are literally served from that specific child-wellbeing map versus CIT-UAI's general territorial-intelligence platform.

---

## 1. Key numbers

| # | Figure | Value | Source (year) |
|---|---|---|---|
| 1 | Lo Espejo total population (Censo 2024, official) | **87,295** | INE via BCN, 2025 |
| 2 | Lo Espejo total population (Censo 2017, official) | 98,804 (−11.6% by 2024) | BCN, 2025 |
| 3 | Chile national population (Censo 2024 / 2017) | 18,480,432 / 17,574,003 (+5.2%) | INE, 2025a; t13, 2017 |
| 4 | Block-level population sum, `manzanas_uv.geojson` (807 blocks, Censo 2024) | 85,958 (98.5% of official) | This dataset; INE via BCN, 2025 |
| 5 | **Estimated resident cohort aged 8–17** (uniform-within-band assumption; arithmetic in §1.1) | **≈ 11,197** (13.0% of comunal population) | Derived from Censo 2024 block data |
| 6 | Households (block sum) / with internet | 26,908 / 24,585 (91.4%) | Censo 2024 block data |
| 7 | CASEN multidimensional poverty (5 dimensions), 2022 vs 2017 | 28.8% vs 37.5% | Ministerio de Desarrollo Social y Familia via BCN, 2025 |
| 8 | Homicide rate 2023, highest in the Metropolitan Region | **16.7 per 100,000** (national ≈6.3–6.6) | Subsecretaría de Prevención del Delito via La Tercera, 2024; INE/CEAD, 2025 |

Supporting numbers used throughout: CASEN income poverty 6.8% (2022) vs 6.7% (2017); foreign-born population 6,818 (7.8%, Censo 2024, official) vs 6,202 immigrants in the block sum (7.2%, same masking gap as population); RSH deprivation indicators for Lo Espejo — 8.2% of RSH-registered persons lack basic services, 11.9% live in overcrowded housing (March 2025) (BCN, 2025); MBHT mean 0.54, no "Alto" blocks (§0.3); MINEDUC 2024 enrollment 11,556 across Lo Espejo's schools (§3); Chile-wide smartphone-with-internet access starting at age 8.9 on average (UNICEF/CEPPE-UC/CIAE, 2023); national household internet access 96.5% (SUBTEL, 2025); Android ≈78% of the Chilean mobile OS market (indicative, see §5.2).

### 1.1 Arithmetic for the 8–17 cohort estimate

Censo 2024 age bands in the block data are 0–5, **6–13**, **14–17**, 18–24 (not single years), so an 8–17 cohort must be estimated:

- 6–13 band (8 single ages) totals 8,767. Assuming a uniform per-age distribution, ages 8–13 (6 of those 8 ages) ≈ 8,767 × 6/8 = **6,575**.
- 14–17 band totals 4,622 in full (it is already exactly the 14–17 range needed).
- **Estimated 8–17 cohort = 6,575 + 4,622 = 11,197** (matches the orchestrator's baseline exactly; recomputed independently in Python from the raw GeoJSON, see §1.2 for the by-UV breakdown).

This is 13.0% of the comunal population (11,197/85,958), noticeably above the comuna's already-young 0–14 share (17.6% of 0-14, per official stats) once you back out ages 0–7.

### 1.2 Spatial distribution — which UVs concentrate kids

Recomputed directly from `manzanas_uv.geojson` (807 blocks, grouped by `uv_carto`):

| UV | Population | Est. 8–17 | Households | % of comuna's kids |
|---|---|---|---|---|
| 37B | 12,958 | 1,936 | 3,972 | 17.3% |
| 37C | 10,303 | 1,389 | 3,292 | 12.4% |
| 26 | 9,449 | 1,260 | 3,006 | 11.3% |
| 24 | 8,584 | 1,182 | 2,659 | 10.6% |
| 29 | 7,123 | 897 | 2,183 | 8.0% |
| 36 | 6,853 | 893 | 2,027 | 8.0% |
| 31 | 6,513 | 841 | 1,958 | 7.5% |
| 35 | 6,669 | 765 | 2,074 | 6.8% |
| 37A | 5,639 | 676 | 1,836 | 6.0% |
| 25 | 5,510 | 579 | 1,831 | 5.2% |
| 28 | 2,181 | 294 | 669 | 2.6% |
| 34 | 1,829 | 193 | 602 | 1.7% |
| 30 | 1,100 | 150 | 366 | 1.3% |
| 32 | 935 | 105 | 333 | 0.9% |
| 27 | 312 | 37 | 100 | 0.3% |

**The top 10 UVs (37B, 37C, 26, 24, 29, 36, 31, 35, 37A, 25) hold 93% of the estimated 8–17 population** (10,418 of 11,197); the five smallest UVs (28, 34, 30, 32, 27) together hold only 7%. This is the single most important spatial fact for rollout sequencing: a pilot covering the top 5 UVs (37B, 37C, 26, 24, 29) alone would already reach 6,664 kids — 59% of the comuna's target cohort — with far less geographic and operational scope than a comuna-wide launch.

### 1.3 Cross-checking the estimate against the MBHT (Censo 2017) dataset

As an independent sanity check, I used the *other* dataset (`mbht_2017.geojson`, Censo 2017, `e4a18` = population aged 4–18 = 19,821 across 15 single ages) and scaled it forward:

1. Average population per single age, 2017: 19,821 / 15 ages = 1,321.
2. Ages 8–17 span 10 of those single ages: 1,321 × 10 = 13,214 (2017 estimate for the 8–17 band, under a uniform-per-age assumption).
3. Scale for the comuna's known population decline (87,295/98,804 = 0.8835): 13,214 × 0.8835 ≈ **11,676**.

This lands within 4.3% of the Censo-2024-based estimate of 11,197 (§1.1) — two independent datasets, two different census years, and two different estimation paths converge on roughly **11,200–11,700 kids aged 8–17 currently living in Lo Espejo**. I treat 11,197 as the primary planning number because it is directly derived from the newer, relevant census, but the convergence is reassuring given both estimates rely on a uniform-within-band assumption that is unverified at the individual-age level.

---

## 2. Age structure, 2017 → 2024

| Age band | Censo 2024 | Share |
|---|---|---|
| 0–14 | 15,405 | 17.6% |
| 15–29 | 18,379 | 21.1% |
| 30–44 | 17,970 | 20.6% |
| 45–64 | 21,940 | 25.1% |
| 65+ | 13,601 | 15.6% |

(BCN, 2025, reporting official INE Censo 2024 comunal results.) Lo Espejo's 65+ share (15.6%) is already above the *national* Censo 2024 figure (14.0%; INE, 2025a), meaning Lo Espejo is aging faster than the country while simultaneously losing population overall (§0.2) — a comuna that is both shrinking and greying, which should temper any assumption that the 8–17 cohort will grow over the app's lifetime; if anything, absent new housing, it may shrink further. I could not obtain INE's finer 5-year age bands (e.g., 5–9, 10–14, 15–19) for Lo Espejo specifically — the REDATAM/dashboard tools require interactive querying that I could not complete — so §1.1's block-level 6–13/14–17 bands remain the best available breakdown; **this is a gap** worth closing with a direct REDATAM pull before finalizing product sizing.

---

## 3. Schools

Two sources, not fully reconciled:

- **CIT-UAI visor snapshot** (`ctx_colegios.geojson`, vintage year 2024 per its `AGNO` field): **36 operating schools** (`ESTADO_EST`=1 for all), of which **15 are municipal/local-public** (`COD_DEPE`=2) and **21 are particular subvencionado** (`COD_DEPE`=3, subsidized-private). No fully private-fee or corporación-delegada schools appear. This matches an independent finding that Lo Espejo has "15 escuelas municipales" (Municipalidad de Lo Espejo, n.d.-a).
- **MINEDUC enrollment, 2024** (via BCN, 2025): **11,556 students** total: early childhood education 1,494; primary 6,911; special education 670; secondary humanistic-scientific 1,578; secondary technical-professional 334 (these five categories sum to 10,987, ~569 short of the reported 11,556 total — likely an adult-education or other category not broken out by BCN; **unresolved gap**).
- **Basic + media enrollment** (the closest MINEDUC proxy to "kids studying in Lo Espejo," ages roughly 6–18): 6,911 + 1,578 + 334 = **8,823 students**. This is meaningfully smaller than our 11,197 *resident* 8–17 estimate — plausible in dense urban Santiago, where children cross comuna lines to attend school in either direction, but I found **no data on net commuting flows** for Lo Espejo specifically. Do not treat MINEDUC school enrollment and comunal child population as interchangeable when sizing the app.
- **SIMCE**: 10 of Lo Espejo's 15 municipal schools improved their scores in the 2023 round, alongside a national uptick in Math and Language scores after a decade of stagnation (Municipalidad de Lo Espejo, n.d.-b; MINEDUC, n.d.). I did not pull school-by-school SIMCE scores; this is a qualitative, directionally positive signal, not sized data.

---

## 4. Vulnerability

- **CASEN income poverty**: 6.8% (2022) vs 6.7% (2017) — essentially flat, and lower than I expected for this comuna's reputation; treat with caution because comunal CASEN figures are **Small Area Estimates (SAE)**, produced via the Fay-Herriot method combining CASEN survey data with administrative records, and carry wider confidence intervals for small comunas than the national CASEN figure (Ministerio de Desarrollo Social y Familia, 2022; CEPAL, n.d.).
- **CASEN multidimensional poverty** (5 dimensions: education, health, work/social security, housing/environment, social cohesion): **28.8% (2022), down sharply from 37.5% (2017)** (Ministerio de Desarrollo Social y Familia, 2022, via BCN, 2025). The large gap between income poverty (6.8%) and multidimensional poverty (28.8%) means most vulnerability in Lo Espejo is **non-monetary** — housing quality, environment, education access — which lines up with the MBHT finding that no block reaches "Alto" wellbeing (§0.3) even though outright income poverty is comparatively contained.
- **Registro Social de Hogares (RSH)**, Lo Espejo, March 2025: 8.2% of RSH-registered residents lack basic services; 11.9% live in overcrowded housing (BCN, 2025). Nationally, over 17 million people (≈9 million households) are registered in the RSH, distributed across seven vulnerability tramos (0–40%, 41–50%, …, 91–100%); households in the 40–70% tramos are considered highest-priority for most subsidies (El Mostrador, 2024; BioBioChile, 2025). I found **no comuna-specific RSH tramo distribution** for Lo Espejo (a gap — the municipality's own SECPLAN/Desarrollo Comunitario office would hold this).
- **Safety**: Lo Espejo had the Metropolitan Region's **highest homicide rate in 2023, 16.7 per 100,000** — ahead of San Ramón (16.6) and Cerrillos (14.4) — per the Subsecretaría de Prevención del Delito's *Informe Nacional de Víctimas de Homicidios Consumados*, reported by La Tercera (2024). Nationally, ENUSC 2024 recorded household victimization by violent crime at 8.5% (up from 8.2% in 2023) and a record 57% perceiving they will be victimized in the next 12 months, though perceived insecurity drops sharply from country level (87.7%) to neighborhood level (50.8%) (INE, 2025c; Radio U. de Chile, 2025). I found no Lo Espejo-specific ENUSC breakdown — comuna-level ENUSC exists but I could not retrieve it in this pass (**gap**). Given Lo Espejo's outlier homicide rate, this matters directly for a product that encourages kids to move around public space.

---

## 5. Digital access

### 5.1 Household connectivity in Lo Espejo (Censo 2024 block data, own computation)

Of 26,908 households (block sum): **91.4% have internet** (24,585), **96.8% have telephone** (26,049), **43.4% have a computer** (11,677), only **18.7% have a tablet** (5,024). Internet access is close to, but below, the *national* SUBTEL figure of 96.5% of households (2024) (SUBTEL, 2025) — plausible for a lower-income comuna. Computer and tablet ownership are markedly lower than internet/telephone access, which matters directly for design: a large share of connected households are likely **mobile/smartphone-only**, not desktop- or tablet-equipped.

### 5.2 Chilean children's device and internet use (national)

- **Kids Online Chile 2022** (CEPPE-UC and CIAE-U. de Chile, with MINEDUC's innovation center and UNICEF; 3,011 children aged 9–17 surveyed across 131 schools): the average age of first mobile phone dropped from 11 (2016) to **8.9 years (2022)**; **58% of children get their first internet-enabled phone before age 10** (UNICEF Chile, 2023; PUC, 2023). This directly supports designing for smartphone ownership starting well within the app's 8-year-old floor.
- **SUBTEL's XI Encuesta de Acceso y Usos de Internet (2024)**: smartphones reach 98.9% penetration across all socioeconomic groups, but laptop/computer access is starkly unequal — only 41.4% in the lowest socioeconomic group vs 86.1% in the highest (SUBTEL, 2025). Households with school/university-age children have the highest connection rates of any household type (66.5% with both fixed and mobile) (SUBTEL, 2025). National household internet access reached a record 96.5% in 2024 (Infraestructura Pública, 2024; SUBTEL, 2025).
- **Android vs iOS**: market-research aggregators put Android at roughly **78% of Chile's mobile OS market**, with Apple/Samsung/Xiaomi as the leading vendors (MarkNtel Advisors, n.d.; Expert Market Research, n.d.). I flag this as **indicative, not authoritative** — these figures come from commercial market-research summaries, not a StatCounter or SUBTEL primary read that I was able to verify directly. Given Lo Espejo's lower-income profile (§4), the true Android share locally is plausibly even higher than the national 78%. **Recommendation for the platform architect: build Android-first (or a lightweight installable PWA), and do not assume tablet or desktop access.**

---

## 6. Mobility and safety

- **Bike infrastructure**: Lo Espejo is included in the Gran Santiago and "Zona Sur" cycle-route master plans (alongside San Ramón, El Bosque, La Pintana, La Granja and La Cisterna), with roughly 15 km of cycle routes projected and only about 3 km existing today (CIDEU-referenced planning search; regional master-plan coverage) — I could not find a primary planning document with these exact figures, so treat the 15 km/3 km split as **approximate, secondary-sourced**, not confirmed against MINVU/GORE RM's own plan documents. The regional "Plan Maestro de Ciclovías del Gran Santiago" targets 820 km of new cycle routes across 34 comunas by 2035 (The Clinic, 2024) — Lo Espejo's specific allocation within that plan needs direct confirmation from GORE RM or SECTRA (**gap**).
- **Safety**: see §4 — Lo Espejo's 2023 homicide rate (16.7/100,000) was the highest of any Metropolitan Region comuna, well above the national rate (≈6.3–6.6/100,000 after Censo-2024 rebasing) (La Tercera, 2024; Atisba/CEAD, 2025). This is a first-order constraint on any feature that encourages unsupervised movement through public space (e.g., wayfinding to a park or class at night) and argues strongly for parent-visible location/time context, well-lit and monitored venue prioritization, and coordination with the municipality's existing "Programa de Alarmas Comunitarias y Pulsadores Individuales" and Dirección de Seguridad Pública y Humana (both present in the `programas_nna` catalogue).
- **Transit**: I did not find Lo Espejo-specific data on Metro/bus access for children in this pass (**gap**) — the comuna is served by Line 4A of the Santiago Metro (general knowledge, not independently re-verified against a current source in this research pass) but school-commute mode share was not located.

---

## 7. The municipal program catalogue itself is a demand-side gap

Inspecting `programas_nna.geojson` (108 programs) and `programas_nna_edicion.geojson` (269 program-edition records) directly: **0 of 269 records report a `PARTICIP` (participant) count, and only 7 report `CUPOS` (slots), summing to just 182 slots total** — against an estimated 11,197 kids aged 8–17. In other words, **the municipality's own program catalogue has no usable baseline of how many kids currently use any given program**, which is exactly the kind of anonymous usage signal this app is meant to start generating. This is worth stating plainly to the platform architect and designer: there is no existing "current demand" anchor to calibrate adoption assumptions against — the scenarios in §8 are built from first principles, not from observed municipal-program usage.

---

## 8. Expected users

Base cohort: **11,197** kids aged 8–17 resident in Lo Espejo (§1.1), concentrated 93% in 10 of the 15 UVs (§1.2).

**No Chilean benchmark for municipal, child-facing app adoption or engagement was found in this research pass** (§7 confirms the municipality's own programs don't track this either). The scenarios below are therefore explicitly **planning assumptions**, laid out transparently so the team can substitute real numbers once instrumented:

| Scenario | Registered (% of cohort) | Registered users | Assumed MAU/Registered | MAU (monthly active) | Assumed DAU/MAU (stickiness) | DAU (daily active) |
|---|---|---|---|---|---|---|
| Low | 20% | ~2,239 | 45% | ~1,010 | 15% | ~150 |
| Mid | 40% | ~4,479 | 50% | ~2,240 | 18% | ~400 |
| High | 60% | ~6,718 | 55% | ~3,695 | 20% | ~740 |

Rationale for the MAU/DAU ratios: a municipal utility/discovery app (classes, parks, events) is inherently *episodic* rather than habit-forming — usage should spike around class enrollment windows, school holidays and event calendars rather than being driven daily, so I assumed DAU/MAU stickiness (15–20%) below what social or gaming apps typically report, and let both ratios rise slightly with the adoption scenario on the assumption that higher penetration correlates with stronger word-of-mouth/habitual use among sports/arts-class families. **These ratios are not sourced and should be replaced with real analytics within the first 2–3 months of pilot.**

Two structural factors should shape which scenario is realistic at launch, both found in this research:

1. **Rollout geography**: a pilot limited to the top 5 UVs (37B, 37C, 26, 24, 29) already reaches 6,664 kids (59% of the comuna cohort) — the Low/Mid scenarios above are plausible even at that reduced geographic scope, because most of the cohort lives there anyway.
2. **Consent friction under Ley 21.719**: Chile's new data-protection law takes full effect **1 December 2026** — about two months after today. It requires **verifiable parental/guardian consent for all personal-data processing of children under 14**, and specifically for sensitive data of 14–15 year-olds; only 16–17 year-olds fall under general adult rules (Lawwwing, n.d.; RecordingLaw, n.d.). Roughly **59% of the target cohort (≈6,575 of 11,197) is under 14** by our band estimate (§1.1), meaning the majority of potential users cannot legally self-register with full data processing without a parent completing a verifiable consent step. This should be treated as a hard constraint on the adoption curve, not just a legal footnote — it will very likely push real adoption toward the Low end of the table above unless the registration flow is explicitly designed around parent-mediated onboarding for the under-14 majority.

---

## Handoff: design implications

1. **Design for parent-mediated onboarding as the default, not the exception.** ~59% of the 8–17 cohort is under 14, and Ley 21.719 (in force 1 December 2026) requires verifiable parental consent for all data processing of under-14s, plus consent for sensitive data of 14–15s. A parent/guardian account or companion flow is a legal requirement for the majority of users, not a nice-to-have.
2. **Build Android-first, mobile-only, low-bandwidth-tolerant.** Household computer ownership is only 43% and tablet ownership just 19% in Lo Espejo (own computation from Censo 2024 blocks), versus 91% internet and 97% telephone access — most connected households are smartphone-only. Android holds an estimated ~78% of the Chilean market and is plausibly higher in a lower-income comuna; do not assume desktop or tablet access anywhere in the flow.
3. **Sequence the rollout by UV, not comuna-wide.** 93% of the estimated 11,197 kids aged 8–17 live in 10 of Lo Espejo's 15 UVs, and 59% live in just the top 5 (37B, 37C, 26, 24, 29). A phased pilot in those UVs reaches most of the audience with a fraction of the operational footprint.
4. **Treat the app itself as the first source of usage data — there is none today.** The municipality's own 269-record program catalogue has zero participant counts and only 182 total program slots recorded against ~11,197 kids. There is no baseline to validate adoption assumptions against; instrument everything from day one and revisit the §8 scenarios within the first quarter.
5. **Lead with safety-aware, not just discovery-oriented, UX for public-space features.** Lo Espejo had the Metropolitan Region's highest homicide rate in 2023 (16.7/100,000, more than double the national rate). Any feature that routes a child through public space (park finder, bike-lane navigation, event check-in) should default to well-lit/monitored venues, expose time-of-day context, and consider a parent-visible "where my kid is going" layer, ideally tied into the municipality's existing Alarmas Comunitarias / Seguridad Pública y Humana programs.
6. **Don't conflate "lives in Lo Espejo" with "studies in Lo Espejo."** MINEDUC's basic+media enrollment for schools located in Lo Espejo (8,823 students) is meaningfully smaller than the resident 8–17 cohort (11,197); a real, unquantified share of local kids study elsewhere and vice versa. School-based sign-up channels (the 15 municipal + 21 subsidized-private schools) will not reach the whole target population on their own — plan a non-school channel too (e.g., CESFAM, community centers, the OLN).
7. **Lean on non-income vulnerability, not just poverty rate, to prioritize investment.** Multidimensional poverty (28.8%) is over four times income poverty (6.8%) in Lo Espejo, and the MBHT shows zero census blocks reaching "high" territorial wellbeing. The gaps are in housing, environment, education and access — not primarily household income — which should steer which programs/venues the app foregrounds (proximity and quality of free/public options) over anything paywalled.
8. **Route the Oficina Local de la Niñez (OLN) into the product, not just the data.** The OLN already runs a Children's Consultative Council (CCNNA) for ages 10–17 and case-management/territorial-management functions covering all under-18s in the comuna — a natural governance and co-design partner, and a channel for reaching at-risk kids the app's organic adoption curve may miss.
9. **Validate three specific gaps before finalizing sizing/consent flows**: (a) pull INE's Censo 2024 REDATAM 5-year age bands for Lo Espejo directly (this report used only the 6–13/14–17 block bands); (b) get a comuna-level ENUSC or CEAD breakdown to replace the national safety figures used here; (c) confirm the population-decline hypothesis (housing regeneration vs. migration) with the municipality's SECPLAN, since it affects whether the 8–17 cohort is expected to grow, hold steady, or keep shrinking.
10. **Use the top-UV ranking as the map's default zoom/sort order**, not just for rollout planning — 37B, 37C, 26 and 24 alone account for over half the target cohort, and are the areas where program density, safety design, and marketing spend will have the most leverage.

---

## References (APA 7)

Asimov Consultores. (n.d.). *Matriz de Bienestar Humano Territorial* [Project page]. https://www.asimov.cl/proyectos/matriz-de-bienestar-humano-territorial

Atisba. (2025). *Homicidios en Santiago 2024, con datos CEAD*. https://atisba.cl/monitor/homicidios-en-santiago-2024-con-datos-cead/

Biblioteca del Congreso Nacional de Chile (BCN). (2025). *Reportes estadísticos comunales: Lo Espejo (2025)*. https://www.bcn.cl/siit/reportescomunales/reporpdf.html?anno=2025&idcom=13116

Biblioteca del Congreso Nacional de Chile (BCN). (2024). *Reportes estadísticos comunales: Lo Espejo (2024)*. https://www.bcn.cl/siit/reportescomunales/reporpdf.html?anno=2024&idcom=13116

BioBioChile. (2017, April 17). *Todos deben contestar: esto te preguntarán en el Censo 2017*. https://www.biobiochile.cl/noticias/nacional/chile/2017/04/17/todos-deben-contestar-esto-te-preguntaran-en-el-censo-2017.shtml

BioBioChile. (2025, August 12). *Registro Social de Hogares: qué significa estar en el 40%, 70% o 100% y de qué depende cada tramo*. https://www.biobiochile.cl/noticias/servicios/toma-nota/2025/08/12/registro-social-de-hogares-que-significa-estar-en-el-40-70-o-100-y-de-que-depende-cada-tramo.shtml

Centro de Inteligencia Territorial UAI (CIT-UAI). (n.d.-a). *Somos*. https://cit.uai.cl/somos/

Centro de Inteligencia Territorial UAI (CIT-UAI). (n.d.-b). *CIT-UAI articula el Mapa de Oportunidades de Bienestar para la niñez para fortalecer a las infancias en Lo Espejo*. https://cit.uai.cl/cit-uai-articula-el-mapa-de-oportunidades-de-bienestar-para-la-ninez-para-fortalecer-a-las-infancias-en-lo-espejo/

Comisión Económica para América Latina y el Caribe (CEPAL). (n.d.). *Estimación de la pobreza en Chile a nivel de comuna* [Presentation]. https://www.cepal.org/sites/default/files/presentations/seminario-sae-uruguay-mdsf-chile-jenny-encina.pdf

El Mostrador. (2024, August 20). *Registro Social de Hogares: revisa los tramos en los que te puedes ubicar*. https://www.elmostrador.cl/datos-utiles/2024/08/20/registro-social-de-hogares-revisa-los-tramos-en-los-que-te-puedes-ubicar/

Expert Market Research. (n.d.). *Chile smartphones market share & size*. https://www.expertmarketresearch.com/reports/chile-smartphones-market

Iraguen, M. (n.d.). *Medición de pueblos indígenas y afrodescendientes en el Censo de Población y Vivienda 2017* [Presentation]. CEPAL. https://www.cepal.org/sites/default/files/presentations/03_magdalena_iraguen_ine_chile.pdf

Infraestructura Pública. (2024). *Acceso a internet en Chile alcanza nuevo récord y llega al 96,5% de los hogares*. https://www.infraestructurapublica.cl/acceso-a-internet-en-chile-alcanza-nuevo-record-y-llega-al-965-de-los-hogares/

Instituto Nacional de Estadísticas (INE). (2025a, March 27). *Primeros resultados del Censo 2024: 18.480.432 personas fueron censadas en Chile, manteniéndose la tendencia de envejecimiento de la población*. https://www.ine.gob.cl/sala-de-prensa/prensa/general/noticia/2025/03/27/primeros-resultados-del-censo-2024-18.480.432-personas-fueron-censadas-en-chile-manteni%C3%A9ndose-la-tendencia-de-envejecimiento-de-la-poblaci%C3%B3n

Instituto Nacional de Estadísticas (INE). (2025b, September 2). *INE y CEPAL realizan conversatorio sobre visibilidad y reconocimiento afrodescendiente en Chile y resultados del Censo 2024*. https://www.ine.gob.cl/sala-de-prensa/prensa/general/noticia/2025/09/02/ine-y-cepal-realizan-conversatorio-sobre-visibilidad-y-reconocimiento-afrodescendiente-en-chile-y-resultados-del-censo-2024

Instituto Nacional de Estadísticas (INE). (2025c, July 7). *Subsecretaría de Prevención del Delito e INE presentan los resultados de la Encuesta Nacional Urbana de Seguridad Ciudadana (ENUSC) 2024*. https://www.ine.gob.cl/sala-de-prensa/prensa/general/noticia/2025/07/07/subsecretar%C3%ADa-de-prevenci%C3%B3n-del-delito-e-ine-presentan-los-resultados-de-la-encuesta-nacional-urbana-de-seguridad-ciudadana-(enusc)-2024

Instituto Nacional de Estadísticas (INE). (n.d.). *Censo 2024 — Resultados*. https://censo2024.ine.gob.cl/resultados/

La Tercera. (2024, May 6). *El mapa de frecuencia de homicidios en la RM: Santiago, Puente Alto y San Bernardo encabezan el listado*. https://www.latercera.com/nacional/noticia/el-mapa-de-homicidios-en-la-rm-santiago-puente-alto-y-san-bernardo-encabezan-el-listado/6FK4R7KIRBHDHATK4LRBPC4FCQ/

Lawwwing. (n.d.). *La nueva era de la protección de datos en Chile: qué cambia con la Ley 21.719*. https://lawwwing.com/la-nueva-era-de-la-proteccion-de-datos-en-chile-que-cambia-con-la-ley-21-719/

MarkNtel Advisors. (n.d.). *Chile smartphone market overview & insights 2032*. https://www.marknteladvisors.com/research-library/chile-smartphone-market.html

Ministerio de Desarrollo Social y Familia. (2022). *Estimaciones de pobreza comunal 2022 (metodología SAE)*. https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/pobreza-comunal/2022/Resultados_Estimaciones_SAE_2022.pdf

Ministerio de Educación de Chile (MINEDUC). (n.d.). *Resultados educativos 2023: Simce*. https://www.mineduc.cl/resultados-educativos-2023-simce/

Municipalidad de Lo Espejo. (n.d.-a). *Oficina Local de la Niñez (OLN)*. https://www.loespejo.cl/oficina-local-de-la-ninez-oln/

Municipalidad de Lo Espejo. (n.d.-b). *10 de 15 escuelas municipales de Lo Espejo aumentaron sus puntajes Simce*. https://www.loespejo.cl/10-de-15-escuelas-municipales-de-lo-espejo-aumentaron-sus-puntajes-simce/

Observatorio Ciudadano. (n.d.). *El Censo y la exclusión de los afrodescendientes*. https://observatorio.cl/censo-la-exclusion-los-afrodescendientes/

Pontificia Universidad Católica de Chile (PUC). (2023). *Revelan principales resultados del estudio "Kids Online" en Chile*. https://www.uc.cl/noticias/revelan-principales-resultados-del-estudio-kids-online-en-chile/

Radio Universidad de Chile. (2025, July 7). *ENUSC 2024: victimización en hogares sube y percepción de inseguridad alcanza récord histórico*. https://radio.uchile.cl/2025/07/07/enusc-2024-victimizacion-en-hogares-sube-y-percepcion-de-inseguridad-alcanza-record-historico/

RecordingLaw. (n.d.). *Leyes de privacidad de datos de Chile: la reforma de la Ley 21.719, la nueva agencia y la entrada en vigencia en diciembre de 2026*. https://www.recordinglaw.com/es/world-laws/world-data-privacy-laws/chile-data-privacy-laws/

Subsecretaría de Desarrollo Regional y Administrativo (SUBDERE) / Matriz de Bienestar Humano Territorial. (n.d.). *MBHT — notas metodológicas*. https://plataformabht.subdere.gov.cl/assets/files/notas-metodologicas.pdf

Subsecretaría de Telecomunicaciones (SUBTEL). (2025). *XI Encuesta de Acceso y Usos de Internet — Informe final*. https://www.subtel.gob.cl/wp-content/uploads/2025/02/Informe-Final-Subtel-Acceso-y-Uso-Internet-2024.pdf

t13. (2017, December 22). *Censo 2017: INE cifra población chilena en 17.574.003*. https://www.t13.cl/noticia/nacional/censo-2017-ine-cifra-poblacion-chilena-17.574.003

UNICEF Chile. (2023). *Se adelanta a los 8,9 años el acceso al celular con internet y crece su uso para tareas escolares y aprender cosas que les gustan*. https://www.unicef.org/chile/comunicados-prensa/se-adelanta-los-89-a%C3%B1os-el-acceso-al-celular-con-internet-y-crece-su-uso-para

UNICEF Chile. (2023). *Kids Online Chile 2022*. https://www.unicef.org/chile/informes/kids-online-chile-2022

---

*Data files used directly (read-only, this session): `data/raw/manzanas_uv.geojson`, `data/raw/manzanas_uv.schema.json`, `data/raw/mbht_2017.geojson`, `data/raw/mbht_2017.schema.json`, `data/raw/ctx_colegios.geojson`, `data/raw/ctx_colegios.schema.json`, `data/raw/unidades_vecinales.geojson`, `data/raw/programas_nna.geojson`, `data/raw/programas_nna_edicion.geojson`, `data/raw/resumen_prog_le.geojson`, `data/raw/_summary.json`. All aggregate figures in §0–§1 and §7 were recomputed independently from these files with Python during this research pass, not copied from the orchestrator's baseline.*
