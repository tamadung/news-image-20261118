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

## Resubmit: denser front page (18 Nov 2026, ~16:20 WIB)

First entry scored **97.41%, rank #927** (12/0/0); #10 = 98.77%, gap 1.35
points. The weakness was breadth: five stories only, while the winning
pattern is 30+ stories plus a map. This resubmit keeps the same five big
stories and adds a PIL-drawn world map (21 location dots, 7 labelled) and a
28-item "Around the world" list, for **33 stories in all**.

### The 28 added stories (all real, 18 Nov 2026)

Sources: Horizon (18 Nov world + markets roundup), OneTurn (48 stories,
18 Nov), Daily Baku (18 Nov wire), The Paris Eye (18 Nov breaking),
AppiSToS (18 Nov world feed), The Brief, Raj Global Studies (50 news,
18 Nov). Each item below is one line on the page (bold lead-in + detail):

APEC opens in Shenzhen (Xi hosts Putin; Trump-Xi-Putin summit Thursday);
Democrats take Alaska (Peltola wins Senate seat; party reaches 56); Ebola
surge in Congo (11,000 cases, 5,400 dead); US loses measles-free status
(5,400 cases end 26-year run); Russian plane crash in Siberia (19 killed);
quake in Papua New Guinea (6.0); quake in Romania (5.3); Cyclone Xavier
(Category 5, Northern Cook Islands); World Court rules on Myanmar
(genocide verdict due); Gaza cold kills in tents; US details $12bn
Venezuela oil cash; France protests, 4th weekend; Eisenkot to form
government in Israel (bypassing Netanyahu); cyber-attack hits
supermarkets in seven European states; Australia sanctions West Bank
settlers; Norway holds terror threat at level 3; Latvia confirms new
cabinet; Guatemala prosecutor shot; UN: 372 killed in Ukraine in October;
Sudan: 2,230 civilians dead; Grossi seeks UN top job; GTA VI out at
midnight (global launch Thursday); Dhoni retires from IPL; markets slide
worldwide (S&P -1%, DAX -2%, gold -2%); US computer outages reach the NSA;
solar flare M1.1 recorded; UK climate targets at risk; WFP: one hot meal
every two days in Gaza.

### Layout changes (1024x1024, JPEG 289,166 bytes)

- Masthead and hero kept (Gulf photo, same scene file); hero shortened to
  188 px so the page gains room below.
- Four panels kept (same three photos + PIL cyclone graphic), shrunk to
  172 px each with one-line subs.
- New: world map (480x256, PIL-drawn simplified continents, equirect
  projection lat 85..-55, 21 red dots, 7 labels with white halo). Two dots
  dropped to avoid label collisions (Israel dot sat on the Gaza dot;
  Romania dot sat on the Crimea label). Gaza label moved left of its dot
  after it overlapped the Gulf label in the first render.
- New: 28-item list in three columns (10 beside the map, 9 + 9 below).
  Lead-ins are Title Case bold (15 px) + regular detail (14 px): all-caps
  at 16 px measured 390-587 px per line and truncated details to "...";
  Title Case at 15/14 px fits all 28 lines untruncated (worst 472 px in a
  490 px column, verified programmatically).
- All text still PIL-rendered (DejaVu); no AI-generated text anywhere.

### Validation

- Output: JPEG, 1024x1024, 289,166 bytes (limit 1 MiB).
- Determinism: `main.py` only copies `entry.png`; two runs byte-identical
  (sha256 ae4f66b670732888c7bc018397da9651271b57408c8090d1e59e58fe72320aa3).
- Visual QC: full page read; masthead, hero, panels, header, map labels
  (Alaska, Crimea, Gaza, Gulf, Shenzhen, Manila, Congo) and all 28 list
  lines legible, no overlap, no truncation, no garbled text.
- `compose.py` (the build script) is now included in the repo alongside
  the image, so the page can be rebuilt from its sources.

## Weakest points (carried over from the first entry)

1. The drone swarm in the hero is dramatised (a large swarm) — the
   report says drones, not a count; an illustration, but a literal
   reader could call it exaggerated.
2. Panel headlines are 20 px (was 24 px) — legible at full size, small
   at 300 px across; the masthead and hero headline carry the legibility.
3. The Cyclone panel is a drawn graphic, not a photograph — weaker
   than the four photo panels, though it reads clearly as a storm.
4. The dense-list type is 15/14 px — legible at full size, small at
   300 px across; the breadth gain (criterion 2) is the trade-off, and
   it matches the winning pattern of 30+ stories.
5. The image is a single fixed picture: it cannot update if the day's
   news moves after it was composed (it was composed the morning of
   18 Nov WIB, from the overnight wire).
