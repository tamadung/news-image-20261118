# news-image-20261118 — build log

Entry: a program that writes one image summing up the world news of
Wednesday 18 November 2026 to `/output/entry.png`. The image is a
newspaper-style front page (1024x1024, JPEG bytes, 244,890 bytes).

## The day's news (researched 18 Nov 2026, before building)

Sources: Jagran Josh + Education Times (18 Nov headline roundups), AppiSToS
world feed, WK Caeser / The Guardian, The Knowledge Library. The five
stories below were the most consequential and most widely covered, across
regions and fields:

1. **GULF ON EDGE (hero)** — Iran attacks a US military radar system in
   Bahrain with drones; Bahrain issues an all-clear after a threat warning;
   Kuwait reports drone interceptions; the Panama-flagged LPG tanker
   MT TARA GAS is attacked in the Strait of Hormuz (21 of 24 Indian crew
   evacuated to Khasab). The day's biggest story: a Gulf escalation.
2. **WAR — Crimea bridge hit again** — Ukraine damages the Crimean bridge
   in a major strike for the second consecutive day, as Russia pounds
   Kyiv's bridges.
3. **DIPLOMACY — Trump lands in Manila** — Trump arrives in Manila for
   Quad talks ahead of a China visit; Modi attends the East Asia Summit
   and ASEAN-India summit in Manila the same day.
4. **BUSINESS — Nvidia soars, $115.8bn** — Nvidia reports quarterly
   revenue of $115.84bn (double a year earlier, +103%); the board says it
   will not reinstate ousted CEO Jensen Huang.
5. **WEATHER — Cyclone Akvan** — Cyclone Akvan intensifies in the Bay of
   Bengal, expected to become a severe cyclonic storm by 19 November.

## Why this image

The judge's criteria, in its own order:
1. **Names the day** — the masthead says "WEDNESDAY · 18 NOVEMBER 2026"
   in gold on navy, and the footer repeats "18 NOVEMBER 2026 — FIVE
   STORIES, ONE DAY". No doubt which day this sums up, and it is 18
   November 2026, not the house images' 13 November.
2. **Breadth** — five stories across the Middle East, Europe, Asia-Pacific
   diplomacy, global tech/business, and weather.
3. **Reads** — each story is clear from its picture plus a short label:
   the hero scene (warship, radar dome, drone swarm, tanker) plus
   "GULF ON EDGE / Iran drones hit a US radar in Bahrain"; the four
   panels each carry a 2-line headline and a 1–2 line sub-caption.
4. **Faithful** — every headline is a reported fact (see sources above);
   no hype, no speculation shown as fact. The scenes are illustrations
   of reported events, not fake photographs of real people (no close-up
   faces; the Manila panel is a wide motorcade shot).
5. **Craft** — one clear front-page composition, white background, navy
   masthead, red field kickers. All text is rendered with PIL (DejaVu
   Sans) so it is crisp and legible — no AI-generated garbled text
   anywhere. Legible at 300 px: masthead 58 px, hero headline 50 px,
   panel headlines 24 px bold.

## How it was made

- Four scene photos generated (media pipeline, no text in them): Gulf
  dusk (warship + radar + drone swarm + tanker), burning Crimea-style
  bridge, Manila airport motorcade (Philippine + US flags), AI data
  centre with a chip. Each verified visually: no text, no artefacts.
- The Cyclone panel is a PIL-drawn weather graphic (spiral arms, eye,
  rain, sea, coastline) — a weather-map visual, not a photo.
- `compose.py` (build tool, not part of the entry) composites the five
  panels and all text with PIL into `entry.png` (JPEG, quality 88).
- `main.py` (Python 3.13 stdlib) only copies `entry.png` to the output
  directory unchanged — the simplest program the rules allow, written
  fresh in this session.

## Validation

- Output: JPEG, 1024x1024, 244,890 bytes (limit 1 MiB / 1024x1024). 
- Determinism: 2 runs byte-identical (sha256
  27e8f96d1688e37f8c9f1c66ec59aec8b3e46a872c60e989fd8854473f9c4ea6).
- Visual QC: front page read in full; all headlines fit their panels;
  no garbled text; date prominent twice.

## Weakest points

1. The drone swarm in the hero is dramatised (a large swarm) — the
   report says drones, not a count; an illustration, but a literal
   reader could call it exaggerated.
2. Panel headlines are 24 px — legible at full size, small at 300 px
   across; the masthead and hero headline carry the legibility.
3. The Cyclone panel is a drawn graphic, not a photograph — weaker
   than the four photo panels, though it reads clearly as a storm.
4. Five stories is a lot for one page; a 3-story page would be roomier,
   but breadth is the judge's #2 criterion.
5. The image is a single fixed picture: it cannot update if the day's
   news moves after it was composed (it was composed the morning of
   18 Nov WIB, from the overnight wire).
