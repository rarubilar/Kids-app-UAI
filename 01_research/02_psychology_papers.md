# Psychology of Attention & Engagement in Kids (8-17): 5 Core Papers

**For:** Kids App Lo Espejo (Municipality of Lo Espejo + CIT-UAI)
**Prepared by:** child-psych-researcher agent
**Date:** 2026-09-28

## How to read this

We need to get 8-17 year-olds (mostly low-income, Android-first) to open this app *and then
go outside* — to a class, a park, a concert, a bike lane — without exploiting the same
attention-capture tricks that make commercial apps addictive. This document picks 5 core,
peer-reviewed papers, one per angle we need covered: (1) motivation theory, (2) gamification
effects, (3) location-based/exergame physical activity, (4) adolescent brain/peer development,
and (5) ethical design limits (screen time + dark patterns). Five short supporting papers are
added where the core paper needed a second data point (e.g., a second Pokémon GO study, or the
theoretical model behind the developmental paper).

**Verification method:** every paper below was checked by resolving its DOI through the
CrossRef API (`https://api.crossref.org/works/<doi>`) and/or `https://doi.org/<doi>`, and
cross-checked against the publisher/ERIC/PubMed record for year, volume, issue, and page range
where CrossRef metadata was incomplete. All 10 papers (5 core + 5 supporting) resolved
successfully and matched the expected title/authors/journal. None were dropped.

Each core paper section below gives: the APA 7 reference with DOI, why it was chosen for this
app, its method and sample, its key findings with actual numbers, its limitations, and what we
concretely do with it in the product. A comparison table follows, then the design-principle
handoff for the product/design team.

---

## P1 — Motivation: Self-Determination Theory in games

**Reference (verified: yes, via CrossRef + doi.org → Springer, matches title/authors/journal):**
Ryan, R. M., Rigby, C. S., & Przybylski, A. (2006). The motivational pull of video games: A
self-determination theory approach. *Motivation and Emotion, 30*(4), 344–360.
https://doi.org/10.1007/s11031-006-9051-8

**Why chosen:** This is the founding empirical application of Self-Determination Theory (SDT)
to games, and the theoretical ancestor of almost every credible "ethical engagement" framework
used since (including the gamification meta-analysis below). It gives us a non-manipulative
account of *why* people voluntarily return to an activity: because it satisfies the needs for
autonomy, competence, and relatedness — not because it exploits a bias.

**Method & sample:** Four studies. Studies 1-3 were short controlled play sessions (single game,
then comparisons across 2 and 4 games) measuring players' in-game perceived autonomy and
competence against enjoyment, preference between games, and pre-to-post changes in well-being.
Study 4 surveyed an online community of massively-multiplayer-game (MMO) players using autonomy,
competence and relatedness scales (internal consistency α = .63–.71) against enjoyment and
intention to keep playing. (The paper's full-text sample sizes per sub-study were not accessible
behind the publisher paywall from secondary sources; this is noted as a limitation below.)

**Key findings with numbers:** In Studies 1-3, perceived autonomy and competence were
significant positive predictors of enjoyment and of which game players preferred, and were
associated with pre-to-post improvements in well-being; competence perceptions were tied to how
intuitive the controls felt and how immersed/present players felt. In Study 4, autonomy,
competence, and relatedness **each independently and significantly predicted both enjoyment and
intention to keep playing**, even after statistically controlling for the other two needs — i.e.
no single need substitutes for the other two.

**Limitations:** Studies 1-3 use lab/short-session game tasks that may not transfer directly to
a municipal-services app; Study 4 is correlational, self-report, and drawn from self-selected
adult gamers already active in an MMO community (not children/adolescents, not our low-income
Android population); the paper predates smartphones entirely (2006).

**What we do with this in the app:**
- Give kids real choice in *how* they reach a goal (which class, which park, which order) —
  autonomy, not a single forced path.
- Always show a clear, achievable next step and visible progress toward something real ("1 more
  session to finish this class") — competence.
- Add light, opt-in social features (e.g., seeing a friend is going) rather than mandatory ones —
  relatedness without pressure.
- Do not rely on points/rewards alone; anchor engagement in these three needs, which is what
  sustains *voluntary* return visits.

---

## P2 — Gamification effects on learning/behavior (meta-analysis)

**Reference (verified: yes, via CrossRef; print year/issue confirmed against ERIC EJ1245270 and
Google Scholar record, which list 2020, Vol. 32(1), pp. 77–112 for the same DOI CrossRef
initially timestamped as an online-first 2019 record):**
Sailer, M., & Homner, L. (2020). The gamification of learning: A meta-analysis. *Educational
Psychology Review, 32*(1), 77–112. https://doi.org/10.1007/s10648-019-09498-w

**Why chosen:** This is the most rigorous, recent meta-analysis quantifying whether gamification
actually changes cognitive, motivational, and behavioral outcomes, rather than relying on a
single study. It lets us set realistic expectations and pick which game elements are worth
building (and which — leaderboards/points alone — are not).

**Method & sample:** Random-effects meta-analysis of controlled/quasi-experimental gamification
studies, pooling effect sizes (Hedges' g) separately for three outcome domains.

**Key findings with numbers:** Gamification produced significant, small-to-moderate positive
effects: **cognitive learning outcomes g = 0.49** (95% CI [0.30, 0.69], k = 19 studies, N = 1,686);
**motivational outcomes g = 0.36** (95% CI [0.18, 0.54], k = 16, N = 2,246); **behavioral
outcomes g = 0.25** (95% CI [0.04, 0.46], k = 9, N = 951). Effects were driven by which game
elements were used: elements that add meaningful choice, narrative, and social interaction
outperformed "points/badges/leaderboards-only" implementations, which showed weaker or
inconsistent effects.

**Limitations:** Effect sizes are modest, and the behavioral-outcome confidence interval nearly
touches zero (0.04), meaning some included studies found almost no behavior change. Most primary
studies are short (single session/course), so durability beyond weeks is unclear. Most of the
underlying studies were conducted with higher-education or adult learners, not specifically an
8-17 population, so effect sizes should be treated as an upper-bound estimate for our context.

**What we do with this in the app:**
- Prefer game mechanics with real meaning (a storyline tied to the neighborhood, genuine
  challenges tied to actual outings) over generic points/badges/leaderboards, which this
  meta-analysis shows are the weakest lever.
- Set modest internal expectations: gamification alone is a small-to-moderate nudge (g ≈
  0.25–0.49), not a silver bullet — pair it with real incentives from the municipality (actual
  event access, recognition, community programs).
- Measure behavioral outcomes (attendance) separately from motivational ones (app opens); the
  meta-analysis shows these do not move by the same amount.

---

## P3 — Location-based mobile games and physical activity

**Reference (verified: yes, via CrossRef, matches JMIR record):**
Althoff, T., White, R. W., & Horvitz, E. (2016). Influence of Pokémon Go on physical activity:
Study and implications. *Journal of Medical Internet Research, 18*(12), e315.
https://doi.org/10.2196/jmir.6759

**Why chosen:** This is the largest natural experiment showing that a location-based mobile app
can causally increase real-world physical movement — precisely our theory of change (open the
app → go to a real place). It is the direct evidence base for a "go there to unlock it"
mechanic.

**Method & sample:** Observational study using de-identified wearable step-count data (Microsoft
Band) and search-engine engagement logs, covering **more than 32,000 U.S. Pokémon GO players**,
comparing each player's daily steps before vs. after adopting the app, plus a nationwide
search-log analysis of engagement/attrition patterns.

**Key findings with numbers:** Players increased their average daily step count by **1,437 steps
per day (a 25% increase)** relative to their own pre-adoption baseline in the weeks after
installing the game — the largest population-scale physical-activity effect ever measured for a
single app at the time of publication.

**Limitations:** The sample is self-selected U.S. wearable-device owners (Microsoft Band users),
who skew toward adults with disposable income and pre-existing interest in fitness tracking —
not representative of our low-income, Android-only, 8-17 population; the study cannot fully rule
out that people who were already becoming more active were also more likely to adopt the game
(reverse causation); no children/adolescent-specific breakdown is reported.

**What we do with this in the app:**
- Build the core loop so that "completing" something in-app (a badge, a quest step) requires
  physically visiting a real place — a park, a court, a mural, a class location — mirroring
  Pokémon GO's spatial mechanic.
- Track real-world visits/check-ins as the primary success metric, not just app opens or time
  spent in-app (our users are unlikely to own wearables, so this must be self-reported/GPS
  check-in based, not step-counter based).
- Expect a strong initial spike in engagement and plan for it to fade (see S3 below) rather than
  assuming a single location mechanic sustains interest indefinitely.

---

## P4 — Adolescent reward sensitivity and peer presence

**Reference (verified: yes, via CrossRef + confirmed page range F1–F10 and March 2011 issue
date against ERIC EJ941761 and Wiley Online Library abstract page, since CrossRef alone did not
return the page range):**
Chein, J., Albert, D., O'Brien, L., Uckert, K., & Steinberg, L. (2011). Peers increase
adolescent risk taking by enhancing activity in the brain's reward circuitry. *Developmental
Science, 14*(2), F1–F10. https://doi.org/10.1111/j.1467-7687.2010.01035.x

**Why chosen:** This is the key evidence that 13-17 year-olds are neurologically more
reward-sensitive to being observed by peers than either younger children or adults — directly
explaining why our 13-17 experience needs different (and more carefully guarded) social features
than our 8-12 experience.

**Method & sample:** fMRI experiment with three age groups (early adolescents, young adults, and
adults; total sample of roughly 40 participants across the three groups) performing a simulated
driving-risk task ("Stoplight"), each completing one block alone and one block while believing
two same-age peers were watching from an adjacent room.

**Key findings with numbers:** Adolescents took significantly more risks (more running of
yellow lights, more crashes) when peers were watching versus alone; adults' risk-taking was
unaffected by peer presence, with young adults intermediate. Neuroimaging showed adolescents
(but not adults) had significantly greater activation in reward-related brain regions (ventral
striatum, orbitofrontal cortex) specifically during peer-observed trials, and this
reward-circuit activation statistically predicted the increase in risky choices.

**Limitations:** Very small sample (~40 total across three age groups); a simulated lab driving
game is far removed from real app/social-media use; "peers" were unfamiliar same-age confederates
in an adjacent room, not close friends or an online audience, so generalizing to in-app "friends"
or "likes" features is inferential, not directly tested; no data on 8-12 year-olds specifically
(youngest group was already adolescent) and no reported socioeconomic breakdown.

**What we do with this in the app:**
- For 13-17: light, opt-in visibility of a few known peers ("2 friends are going to this
  workshop") can ethically leverage this heightened peer-reward sensitivity — but only ever to
  point toward a real, positive, real-world activity, never toward risk or competition.
- For 8-12: minimize peer-observation/comparison mechanics; favor caregiver-visible, individual
  mastery framing instead, since the developmental peer-reward sensitivity this paper documents
  is specifically an adolescent (not middle-childhood) phenomenon.
- Never build features that combine peer-visibility with risk or extremity ("who went furthest/
  latest/did the wildest thing") — this is precisely the mechanism this paper shows amplifies
  risky choices in teens.
- Keep any peer-visibility feature small and known (a few friends), not a broad public audience,
  matching the study's two-peer paradigm rather than a mass-leaderboard design.

---

## P5 — Manipulative design ("dark patterns") in children's apps

**Reference (verified: yes, via CrossRef, matches JAMA Network Open record):**
Radesky, J., Hiniker, A., McLaren, C., Akgun, E., Schaller, A., Weeks, H. M., Campbell, S., &
Gearhardt, A. N. (2022). Prevalence and characteristics of manipulative design in mobile
applications used by children. *JAMA Network Open, 5*(6), e2217641.
https://doi.org/10.1001/jamanetworkopen.2022.17641

**Why chosen:** This is the direct "must-not-do" evidence base — the only one of the five papers
that empirically catalogs which manipulative attention-capture techniques are actually deployed
against children in real apps today, letting us build an explicit internal ban-list.

**Method & sample:** Cross-sectional study of apps used by **160 children aged 3-5** in the
U.S.; parents (recruited as a convenience sample of legal guardians who owned a smartphone/
tablet) identified their child's most-used app, and researchers coded the resulting apps for
manipulative/deceptive design features: parasocial pressure from characters, fabricated time
pressure, navigation/exit obstruction, social pressure, and advertising/purchase pressure.

**Key findings with numbers:** **80% of the apps examined ("four in five") contained at least
one manipulative design feature**; only 20% had none. Manipulative design was significantly more
prevalent in apps used by children from lower-parent-education, lower-income households — a
socioeconomic-equity finding directly relevant to our own low-income target population. Common
tactics included ads disguised as gameplay, characters emotionally pressuring continued play or
against closing the app, and forced-choice purchase prompts.

**Limitations:** The sample is preschool-age (3-5), younger than our 8-17 target range, so
tactics and effects on older children/teens are extrapolated rather than directly measured; the
design is descriptive/cross-sectional (it documents prevalence, not the size of the behavioral or
purchasing effect); it is a U.S. convenience sample of parents willing to complete online
research, not Chile-specific.

**What we do with this in the app:**
- Maintain a hard internal ban-list, audited against this paper's taxonomy before every release:
  no fake countdown timers, no characters/notifications that guilt-trip a child for leaving or
  not returning, no ads disguised as content, no purchase-pressure flows.
- Because manipulative design in the U.S. data was *more* common precisely among lower-income
  households — our own demographic — treat "clean, non-manipulative by design" as a core equity
  commitment, not just a nice-to-have.
- Any "come back soon" prompt must be honest and skippable (no fabricated scarcity like "only 2
  spots left!" unless literally true).

---

## Supporting references (short)

**S1.** Przybylski, A. K., & Weinstein, N. (2017). A large-scale test of the Goldilocks
hypothesis: Quantifying the relations between digital-screen use and the mental well-being of
adolescents. *Psychological Science, 28*(2), 204–215. https://doi.org/10.1177/0956797616678438
(**verified: yes**). Nationally representative sample of English 15-year-olds (N = 120,115) found
a curvilinear ("Goldilocks") relationship: moderate digital-screen use was associated with equal
or better well-being than none, while heavy use predicted lower well-being. *Use:* success should
be measured as real-world attendance, not time-in-app; don't design for maximum session length.

**S2.** Orben, A., & Przybylski, A. K. (2019). The association between adolescent well-being and
digital technology use. *Nature Human Behaviour, 3*(2), 173–182.
https://doi.org/10.1038/s41562-018-0506-1 (**verified: yes**). Specification-curve analysis
across three datasets (combined N = 355,358) found digital technology use explains at most 0.4%
of variance in adolescent well-being — comparable to trivial effects like eating potatoes. *Use:*
screen time itself is not the ethical risk; manipulative design (P5) is. Avoid shame-based
screen-time messaging.

**S3.** Howe, K. B., Suharlim, C., Ueda, P., Howe, D., Kawachi, I., & Rimm, E. B. (2016). Gotta
catch 'em all! Pokémon GO and physical activity among young adults: Difference in differences
study. *BMJ, 355*, i6270. https://doi.org/10.1136/bmj.i6270 (**verified: yes**). In 1,182 U.S.
adults (18-35) with iPhone step-tracking, daily steps rose by 955 (~24%) in week 1 post-install
but decayed back to baseline by week 6. *Use:* confirms the ~4-6 week novelty-decay pattern also
implied by P3; plan a content refresh cadence on that timescale.

**S4.** Steinberg, L. (2008). A social neuroscience perspective on adolescent risk-taking.
*Developmental Review, 28*(1), 78–106. https://doi.org/10.1016/j.dr.2007.08.002 (**verified:
yes**). Theoretical dual-systems model: reward/sensation-seeking rises from preadolescence, peaks
in mid-adolescence (~13-16), then declines, while self-control develops linearly and continues
maturing into the 20s. *Use:* justifies splitting engagement design at roughly the 8-12 / 13-17
boundary used throughout this document.

**S5.** Somerville, L. H., Jones, R. M., & Casey, B. J. (2010). A time of change: Behavioral and
neural correlates of adolescent sensitivity to appetitive and aversive environmental cues. *Brain
and Cognition, 72*(1), 124–133. https://doi.org/10.1016/j.bandc.2009.07.003 (**verified: yes**).
Review/synthesis showing adolescence is a distinct period of heightened sensitivity to incentive
and social-evaluative cues relative to both childhood and adulthood. *Use:* supports warmer,
belonging-oriented framing for 13-17, and curiosity/mastery framing (not social-evaluative) for
8-12.

---

## Comparison table

| # | Paper (short) | Angle | Age focus | Method / Sample | Key number | Core design takeaway |
|---|---|---|---|---|---|---|
| P1 | Ryan, Rigby & Przybylski (2006) | Motivation (SDT) | General (adult gamers) | 4 studies; lab sessions + MMO community survey | Autonomy, competence, relatedness each *independently* predict enjoyment & return play | Design for real choice + visible progress + light social ties |
| P2 | Sailer & Homner (2020) | Gamification meta-analysis | General (mostly older learners) | Meta-analysis, k = 9–19 studies per outcome, N up to 2,246 | g = 0.49 cognitive / 0.36 motivational / 0.25 behavioral | Meaningful mechanics > points/badges/leaderboards; expect modest effects |
| P3 | Althoff, White & Horvitz (2016) | Location-based PA | General (US adults) | Wearable + search-log data, n > 32,000 | +1,437 steps/day (+25%) post-adoption | "Go there to unlock it" loop; measure real visits |
| P4 | Chein et al. (2011) | Adolescent reward sensitivity & peers | 13-17 vs. adults | fMRI, ~40 participants, 3 age groups | Adolescents show ↑ reward-circuit activity only when peers watch | Peer-visibility OK for teens if pointed at real activities; avoid for 8-12 |
| P5 | Radesky et al. (2022) | Ethical design / dark patterns | 3-5 (extrapolated upward) | Cross-sectional coding of apps used by 160 children | 80% of apps had ≥1 manipulative design feature | Hard ban-list on manipulative patterns; extra duty given low-income link |
| S1 | Przybylski & Weinstein (2017) | Wellbeing / screen time | 15-year-olds | N = 120,115, national survey | Curvilinear ("Goldilocks") screen time–wellbeing relation | Optimize for real-world outcomes, not session length |
| S2 | Orben & Przybylski (2019) | Wellbeing / screen time | Adolescents (3 datasets) | N = 355,358, specification curve analysis | Tech use explains ≤0.4% of wellbeing variance | Don't shame screen time; design ethics, not usage limits, is the lever |
| S3 | Howe et al. (2016) | Location-based PA | Young adults 18-35 | N = 1,182, diff-in-diff | +955 steps/day (~24%), decays to baseline by week 6 | Refresh content every 4-6 weeks to counter decay |
| S4 | Steinberg (2008) | Adolescent development (theory) | 8-12 vs. 13-17 vs. adult | Theoretical/dual-systems synthesis | Reward-seeking peaks ~13-16; self-control matures linearly into 20s | Justifies the 8-12 / 13-17 design split |
| S5 | Somerville, Jones & Casey (2010) | Adolescent development | 8-12 vs. 13-17 | Review/neuro synthesis | Adolescence = distinct peak in incentive/social-cue sensitivity | Belonging framing for teens; mastery framing for 8-12 |

---

## Handoff: design principles

1. **[P1]** Give kids real choice in how they reach a goal (which class, park, or order to do
   things) — never a single forced path.
2. **[P1]** Always surface a clear, achievable next step and visible progress toward something
   real ("1 more session to finish this class"), not abstract points.
3. **[P1]** Make social/relatedness features opt-in and light-touch (e.g., "a friend is going"),
   never mandatory or comparison-based.
4. **[P2]** Prefer game mechanics with real meaning — narrative, real-world challenges, genuine
   choice — over generic points/badges/leaderboards, which the evidence shows are the weakest
   lever.
5. **[P2]** Set realistic internal expectations: gamification alone produces small-to-moderate
   effects (g ≈ 0.25–0.49); pair it with real municipal incentives (actual events, recognition).
6. **[P3]** Build the core loop so completing something in-app requires physically visiting a
   real place (park, court, mural, class venue).
7. **[P3/S3]** Plan a content/quest refresh cadence roughly every 4-6 weeks to counter the
   novelty decay documented in both Pokémon GO studies.
8. **[P4]** For the 13-17 experience, small known-peer visibility ("2 friends are going") can
   ethically leverage teens' heightened peer-reward sensitivity — but only ever pointed at real,
   positive, real-world activities.
9. **[P4/S4/S5]** Split the UX by age band: 8-12 = mastery/curiosity framing, individual
   progress, caregiver-visible; 13-17 = peer-visibility, belonging/identity framing, more
   autonomy — matching the documented mid-adolescent peak in reward/social sensitivity.
10. **[P5]** Maintain a hard internal ban-list of manipulative patterns (fake timers, guilt-trip
    characters, disguised ads, forced purchase flows), audited against Radesky et al.'s taxonomy
    before every release.
11. **[S1]** Measure success as real-world attendance/visits, not total in-app time or session
    count; never optimize for longer sessions as a goal in itself.
12. **[S2]** Do not use shame- or fear-based "too much screen time" messaging — overall device
    use has a near-zero relationship to wellbeing; the actual ethical risk is manipulative
    design, not device use per se.

### Must NOT do

- Must **not** use fake countdown timers or fabricated scarcity ("only 2 spots left!") unless
  literally true. **[P5]**
- Must **not** use characters, mascots, or notifications that guilt-trip or emotionally pressure
  a child into not closing or leaving the app. **[P5]**
- Must **not** disguise ads as content/gameplay or use manipulative purchase/upgrade flows, even
  in service of "engagement." **[P5]**
- Must **not** build public leaderboards or broad social comparison, especially around risky or
  extreme behavior ("who went furthest/latest") — this directly misuses the documented
  adolescent peer-reward mechanism. **[P4]**
- Must **not** apply 13-17 peer-visibility mechanics to the 8-12 experience; the underlying
  peer-reward sensitivity this relies on is an adolescent-specific finding, not yet present in
  middle childhood. **[P4, S4, S5]**
- Must **not** optimize core product metrics around in-app time-spent or session count; optimize
  for real-world visits/attendance instead. **[P3, S1]**
- Must **not** use shame- or fear-based screen-time messaging toward kids or caregivers — the
  evidence does not support it and it undermines trust. **[S1, S2]**
