#!/usr/bin/env python3
"""compose-v3.py — build the news-image-20261118 round-3 front page (1024x1024).

Winner-template rebuild (same template as 17 Nov v3 + the #1's data bars):
cream paper, big serif date masthead, 13 core stories each with its own
flat-illustration panel (generated flat art, no AI text), a large world map
with numbered pins 1-13 tied to the core stories plus gold dots for the
also-on stories, and a numbered ALSO ON list for the rest. Plus the #1's
extras: a region bar (counts per region), a field bar (counts per field),
a THE DAY IN NUMBERS strip, and a DATE CHECK box (stories deliberately
left out because they were first reported on 17 Nov).
All text is drawn with PIL (DejaVu Serif for headlines, DejaVu Sans for
body) — no AI-generated text anywhere. Deterministic: same inputs, same
bytes. 42 stories in all.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = Path(__file__).resolve().parent
ILLU = BASE / "v3-illu"

PAPER = (247, 241, 222)
INK = (24, 30, 42)
RED = (200, 16, 46)
GOLD = (176, 141, 60)
GREY = (96, 94, 86)
PANEL = (255, 255, 255)
BORDER = (198, 192, 176)
MAP_BG = (255, 255, 255)
MAP_LAND = (232, 222, 196)
MAP_EDGE = (178, 168, 140)

REGIONS = {
    "EUROPE": (13, 71, 161),
    "MIDDLE EAST": (200, 16, 46),
    "ASIA": (27, 94, 32),
    "AFRICA": (106, 27, 154),
    "AMERICAS": (176, 106, 0),
    "OCEANIA": (0, 131, 143),
    "WORLD": (69, 90, 100),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)  # noqa: E731
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
F_SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731


def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap_lines(d, text, f, max_w, max_lines):
    """Greedy wrap to max_lines; add an ellipsis only if words are cut off."""
    words = text.split()
    lines = []
    idx = 0
    while idx < len(words) and len(lines) < max_lines:
        cur = words[idx]
        idx += 1
        while idx < len(words):
            cand = cur + " " + words[idx]
            if text_w(d, cand, f) <= max_w:
                cur = cand
                idx += 1
            else:
                break
        lines.append(cur)
    if idx < len(words):  # some words did not fit: mark the last line
        last = lines[-1]
        while last and text_w(d, last + "\u2026", f) > max_w:
            last = last[:-1].rstrip()
        lines[-1] = last + "\u2026"
    return lines


def crop_to(im, tw, th, ybias=0.5):
    """Center-crop im to aspect tw/th (vertical bias ybias), then resize."""
    sw, sh = im.size
    ta, sa = tw / th, sw / sh
    if sa > ta:  # source wider: crop width, keep full height
        nw = int(sh * ta)
        x0 = (sw - nw) // 2
        box = (x0, 0, x0 + nw, sh)
    else:  # source narrower: crop height with vertical bias
        nh = int(sw / ta)
        y0 = int((sh - nh) * ybias)
        box = (0, y0, sw, y0 + nh)
    return im.crop(box).resize((tw, th), Image.LANCZOS)


# ---------------------------------------------------------------- stories
# (num, file, region, kicker, headline, deck, lon, lat, ybias)
CORE = [
    (1, "01-gulf-intercept", "MIDDLE EAST", "MIDDLE EAST \u00b7 IRAN WAR",
     "Kuwait and Bahrain intercept drones",
     "Iran says it aimed at US forces at Kuwait's Ali Al Salem base.",
     50.5, 26.2, 0.5),
    (2, "02-manila-quad", "ASIA", "ASIA \u00b7 DIPLOMACY",
     "Trump lands in Manila",
     "Quad talks in Manila; Trump meets Marcos on APEC eve.",
     121, 15, 0.5),
    (3, "03-crimea-bridge", "EUROPE", "EUROPE \u00b7 WAR",
     "Crimea Bridge hit again",
     "Second-day strike; road span collapses into the Kerch Strait.",
     34, 45, 0.62),
    (4, "04-nvidia-record", "AMERICAS", "AMERICAS \u00b7 TECH",
     "Nvidia posts record $115.8bn",
     "First results since Huang's exit; guides Q4 to $130bn.",
     -122, 37, 0.5),
    (5, "05-cyclone-akvan", "ASIA", "ASIA \u00b7 WEATHER",
     "Cyclone Akvan nears India's coast",
     "Landfall in Andhra Pradesh is forecast for Friday.",
     80, 16, 0.5),
    (6, "06-apec-shenzhen", "ASIA", "ASIA \u00b7 DIPLOMACY",
     "Xi greets Trump as APEC opens in Shenzhen",
     "A first three-way meeting with Putin is set for Thursday.",
     114, 22, 0.5),
    (7, "07-cop31-split", "WORLD", "WORLD \u00b7 CLIMATE",
     "COP31 splits over a fossil-fuel phase-out",
     "Antalya talks argue over the draft as Friday's deadline nears.",
     30, 37, 0.5),
    (8, "08-bangladesh", "ASIA", "ASIA \u00b7 LABOUR",
     "Bangladesh protests shut 55 factories",
     "Wage march blocks a highway; police report about 300 arrests.",
     90, 24, 0.5),
    (9, "09-gtavi-midnight", "WORLD", "WORLD \u00b7 GAMES",
     "GTA VI goes on sale at midnight",
     "The launch rolls out by time zone, New Zealand first.",
     174, -41, 0.5),
    (10, "10-voyager-space", "WORLD", "WORLD \u00b7 SPACE",
     "Voyager 1 is one light-day from Earth",
     "The first human-made object that far, 49 years on.",
     -80, 28, 0.5),
    (11, "11-ebola", "AFRICA", "AFRICA \u00b7 HEALTH",
     "Ebola surge in Congo",
     "11,000 cases, 5,400 dead; WHO reviews emergency status.",
     25, -2, 0.5),
    (12, "12-haiti-raid", "AMERICAS", "AMERICAS \u00b7 HAITI",
     "Salvadoran troops raid a gang boss's home",
     "Bukele's forces demolish Jeff's mansion; 'gift to Haiti'.",
     -72, 19, 0.5),
    (13, "13-australia-sanctions", "OCEANIA", "OCEANIA \u00b7 DIPLOMACY",
     "Australia sanctions Daniella Weiss",
     "With the UK, it targets West Bank settler violence.",
     149, -35, 0.5),
]

# (num, region, headline, summary, lon, lat) — ALSO ON, 2 lines each.
ALSO = [
    (14, "OCEANIA", "Quake hits Papua New Guinea", "Magnitude 6.0 strikes", 147, -6),
    (15, "EUROPE", "Quake in Romania", "5.3-magnitude tremor", 25, 46),
    (16, "OCEANIA", "Cyclone Xavier", "Category 5 hits Cook Islands", -160, -21),
    (17, "ASIA", "World Court rules on Myanmar", "Genocide verdict due", 96, 20),
    (18, "MIDDLE EAST", "Gaza cold kills in tents", "Freezing nights; aid blocked", 34, 31),
    (19, "AMERICAS", "US details $12bn Venezuela oil", "Maduro revenue report", -66, 7),
    (20, "EUROPE", "France protests: 4th weekend", "Cost-of-living marches", 2, 49),
    (21, "MIDDLE EAST", "Eisenkot to form government", "Bypasses Netanyahu", 35, 32),
    (22, "AMERICAS", "Cyber-attack hits supermarkets", "Freezers down in 7 states", -98, 39),
    (23, "EUROPE", "Norway holds threat level 3", "Threat level stays at 3/5", 11, 60),
    (24, "EUROPE", "Latvia confirms new cabinet", "Kulbergs wins vote", 24, 57),
    (25, "AMERICAS", "Guatemala prosecutor shot", "Investigator wounded", -90, 15),
    (26, "EUROPE", "UN: 372 killed in Ukraine", "October toll, monitors say", 32, 50),
    (27, "AFRICA", "Sudan: 2,230 civilians dead", "Drones killed 1,630", 30, 13),
    (28, "WORLD", "Grossi seeks UN top job", "IAEA chief bids for post", 9, 46),
    (29, "ASIA", "Dhoni retires from IPL", "Cricket icon ends career", 77, 28),
    (30, "WORLD", "Markets slide worldwide", "S&P -1%, DAX -2%, gold -2%", -74, 41),
    (31, "AMERICAS", "US computer outages reach NSA", "Federal systems hit", -77, 39),
    (32, "WORLD", "Solar flare M1.1 recorded", "Sun fires mid-strength flare", 0, 0),
    (33, "EUROPE", "UK climate targets at risk", "Weaker EV rules blamed", 0, 51),
    (34, "MIDDLE EAST", "WFP: one hot meal every two days", "Gaza rations food", 34, 31),
    (35, "MIDDLE EAST", "Yemen: Saudi-led forces strike", "60 Houthi targets hit", 45, 15),
    (36, "MIDDLE EAST", "West Bank: UK and Australia sanction", "settler leaders", 35, 32),
    (37, "MIDDLE EAST", "Lebanon: World Bank says rebuilding", "is lagging", 36, 34),
    (38, "ASIA", "Kashmir: Indian forces kill a militant", "commander", 75, 34),
    (39, "ASIA", "Philippines: Trump meets Imelda Marcos", "in Manila", 121, 15),
    (40, "ASIA", "South Korea: Lee seeks China's help", "for peace", 127, 38),
    (41, "ASIA", "Malaysia: minutes show AG opposed", "Najib's house arrest", 102, 3),
    (42, "AFRICA", "Ethiopia\u2013Eritrea tensions", "troops mass on border", 39, 15),
]

# Region counts (all 42 stories) for the region bar.
REGION_COUNTS = [
    ("EUROPE", 7), ("MIDDLE EAST", 7), ("ASIA", 10), ("AFRICA", 3),
    ("AMERICAS", 6), ("OCEANIA", 3), ("WORLD", 6),
]
# Field counts (all 42 stories) for the field bar.
FIELD_COUNTS = [
    ("War & security", 13), ("Politics & diplomacy", 9),
    ("Economy & labour", 3), ("Society & culture", 3),
    ("Disasters & weather", 4), ("Tech", 3), ("Climate & space", 4),
    ("Justice", 3),
]

ILLU_FILES = {}
for _s in CORE:
    _p = sorted((ILLU).glob(f"media-generation-{_s[1]}-*.webp"))
    assert _p, f"illustration missing for {_s[1]}"
    ILLU_FILES[_s[1]] = _p[0]

# ------------------------------------------------------------- world map
CONTINENTS = {
    "North America": [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69),
                      (-85, 66), (-80, 73), (-65, 60), (-55, 52), (-60, 47),
                      (-70, 44), (-75, 35), (-80, 32), (-81, 26), (-84, 30),
                      (-90, 21), (-97, 26), (-105, 20), (-105, 23), (-110, 24),
                      (-114, 29), (-117, 33), (-122, 37), (-124, 40), (-124, 48),
                      (-130, 55), (-140, 60), (-155, 58), (-165, 60), (-168, 66)],
    "South America": [(-79, 9), (-72, 12), (-62, 10), (-52, 5), (-50, 0),
                      (-44, -3), (-35, -8), (-40, -20), (-48, -28), (-57, -38),
                      (-65, -41), (-68, -50), (-70, -54), (-73, -50), (-73, -37),
                      (-70, -30), (-70, -18), (-77, -12), (-81, -6), (-80, 1),
                      (-79, 9)],
    "Africa": [(-17, 15), (-17, 21), (-10, 31), (-5, 35), (10, 37), (20, 32),
               (30, 31), (35, 28), (39, 21), (43, 12), (51, 11), (48, 0),
               (40, -10), (40, -20), (35, -28), (28, -33), (20, -35), (15, -27),
               (12, -18), (13, -10), (9, 4), (-8, 5), (-13, 8), (-17, 15)],
    "Europe": [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (5, 53),
               (8, 57), (10, 59), (5, 60), (12, 56), (18, 56), (21, 55),
               (24, 59), (28, 60), (30, 62), (30, 70), (40, 68), (45, 68),
               (50, 69), (55, 68), (60, 69), (68, 73), (75, 73), (80, 73),
               (70, 72), (60, 70), (55, 68), (50, 60), (45, 55), (40, 50),
               (40, 47), (35, 45), (30, 46), (28, 44), (23, 40), (20, 40),
               (15, 38), (10, 38), (5, 38), (0, 38), (-5, 36), (-10, 36)],
    "Asia": [(30, 70), (40, 68), (50, 69), (60, 69), (68, 73), (75, 73),
             (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72),
             (140, 72), (150, 70), (160, 70), (170, 67), (178, 65), (170, 60),
             (162, 56), (158, 52), (150, 59), (142, 55), (140, 45), (135, 43),
             (130, 42), (127, 40), (126, 38), (122, 39), (120, 32), (122, 28),
             (118, 25), (110, 20), (108, 12), (105, 9), (100, 7), (98, 10),
             (95, 16), (92, 21), (88, 22), (85, 19), (80, 15), (77, 8),
             (73, 16), (70, 20), (66, 25), (60, 25), (56, 27), (52, 28),
             (50, 30), (48, 30), (44, 29), (40, 30), (36, 36), (30, 36),
             (28, 41), (30, 46), (30, 55), (30, 60), (30, 70)],
    "Oceania": [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
                (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
                (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
                (142, -11), (137, -12), (135, -15), (132, -11), (130, -13),
                (126, -14), (122, -17), (118, -20), (113, -22)],
}

CONTINENT_LABELS = [
    ("NORTH AMERICA", -115, 55), ("SOUTH AMERICA", -60, -15),
    ("AFRICA", 8, 15), ("EUROPE", -15, 60), ("ASIA", 125, 62),
    ("OCEANIA", 134, -25),
]


def project(lon, lat, x0, y0, w, h):
    return (x0 + (lon + 170) / 360 * w, y0 + (1 - (lat + 58) / 148) * h)


def collide(px, py, placed, min_d):
    for qx, qy in placed:
        if (px - qx) ** 2 + (py - qy) ** 2 < min_d ** 2:
            return True
    return False


def place_pin(px, py, placed, min_d, max_r=60):
    """Spiral search for a free spot near (px, py)."""
    if not collide(px, py, placed, min_d):
        return px, py
    for r in range(6, max_r, 4):
        for k in range(16):
            a = k / 16 * 2 * math.pi
            qx, qy = px + r * math.cos(a), py + r * math.sin(a)
            if not collide(qx, qy, placed, min_d):
                return qx, qy
    return px, py


# ---------------------------------------------------------------- panels
def draw_badge(d, cx, cy, num, r=10):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=(255, 255, 255), width=1)
    f = F_SANS_B(11 if num < 10 else 10)
    tw = d.textlength(str(num), font=f)
    d.text((cx - tw / 2, cy - 8 if num < 10 else cy - 7), str(num), font=f, fill=(255, 255, 255))


def draw_panel_large(d, img, x, y, w, h, s):
    """Wide panel (top row): illustration on top, text below."""
    num, key, region, kicker, headline, deck, lon, lat, yb = s
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=BORDER)
    im = Image.open(ILLU_FILES[key]).convert("RGB")
    img.paste(crop_to(im, w - 2, 96, yb), (x + 1, y + 1))
    draw_badge(d, x + 13, y + 13, num)
    tx = x + 8
    d.text((tx, y + 102), kicker, font=F_SANS_B(10), fill=REGIONS[region])
    hl = wrap_lines(d, headline, F_SERIF_B(16), w - 16, 2)
    yy = y + 118
    for ln in hl:
        d.text((tx, yy), ln, font=F_SERIF_B(16), fill=INK)
        yy += 19
    dk = wrap_lines(d, deck, F_SANS(11), w - 16, 2)
    yy += 1
    for ln in dk:
        d.text((tx, yy), ln, font=F_SANS(11), fill=(58, 58, 58))
        yy += 13


def draw_panel_small(d, img, x, y, w, h, s):
    """Single-width panel: illustration on top, text below."""
    num, key, region, kicker, headline, deck, lon, lat, yb = s
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=BORDER)
    im = Image.open(ILLU_FILES[key]).convert("RGB")
    img.paste(crop_to(im, w - 2, 72, yb), (x + 1, y + 1))
    draw_badge(d, x + 12, y + 12, num)
    tx = x + 6
    d.text((tx, y + 78), kicker, font=F_SANS_B(9), fill=REGIONS[region])
    hl = wrap_lines(d, headline, F_SERIF_B(13), w - 12, 2)
    yy = y + 92
    for ln in hl:
        d.text((tx, yy), ln, font=F_SERIF_B(13), fill=INK)
        yy += 16
    dk = wrap_lines(d, deck, F_SANS(10), w - 12, 2)
    for ln in dk:
        d.text((tx, yy), ln, font=F_SANS(10), fill=(58, 58, 58))
        yy += 11


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top line ---
    d.text((16, 4), "THE WORLD'S NEWS IN ONE PICTURE", font=F_SANS_B(11), fill=INK)
    t = "42 STORIES \u00b7 7 REGIONS \u00b7 8 FIELDS \u00b7 13 ILLUSTRATED \u00b7 ALL FROM WEDNESDAY"
    d.text((1008, 4), t, font=F_SANS_B(11), fill=RED, anchor="ra")

    # --- masthead: big serif date ---
    d.text((512, 18), "Wednesday 18 November 2026", font=F_SERIF_B(44),
           fill=INK, anchor="ma")
    d.line([(16, 72), (1008, 72)], fill=RED, width=2)
    d.line([(16, 76), (1008, 76)], fill=INK, width=1)

    # --- region bar (counts per region, proportional widths) ---
    ry0, ry1 = 80, 96
    total = sum(c for _n, c in REGION_COUNTS)
    x = 16
    for name, count in REGION_COUNTS:
        seg_w = int(992 * count / total)
        d.rectangle([x, ry0, x + seg_w, ry1], fill=REGIONS[name])
        label = f"{name} {count}"
        f = F_SANS_B(10)
        tw = d.textlength(label, font=f)
        if tw + 8 <= seg_w:
            d.text((x + (seg_w - tw) / 2, ry0 + 3), label, font=f,
                   fill=(255, 255, 255))
        x += seg_w

    # --- field bar (black, counts per field) ---
    fy0, fy1 = 98, 114
    d.rectangle([16, fy0, 1008, fy1], fill=(24, 30, 42))
    fields = "  \u00b7  ".join(f"{n} {c}" for n, c in FIELD_COUNTS)
    t = "BY FIELD:  " + fields
    f = F_SANS_B(10)
    tw = d.textlength(t, font=f)
    d.text(((1024 - tw) / 2, fy0 + 3), t, font=f, fill=(255, 255, 255))

    # --- the day in numbers ---
    ny = 118
    nums = ("THE DAY IN NUMBERS:  55 factories shut in Bangladesh  \u00b7  "
            "$115.8bn Nvidia's record quarter  \u00b7  1 light-day: Voyager 1's "
            "distance  \u00b7  1,441 drones over Ukraine  \u00b7  11,000 Ebola cases")
    f = F_SANS_B(10)
    tw = d.textlength(nums, font=f)
    d.text(((1024 - tw) / 2, ny), nums, font=f, fill=INK)

    # --- story grid: row 1 = 3 large, rows 2-3 = 5 small each ---
    # row 1: y 136-318 (182 tall: 96 illustration + kicker + 2-line
    # headline + 2-line deck), 3 x 330 wide
    row1_y, row1_h = 136, 182
    cols1 = [16, 347, 678]
    for i in range(3):
        draw_panel_large(d, img, cols1[i], row1_y, 330, row1_h, CORE[i])
    # rows 2-3: y 322-468, 472-618 (146 tall), 5 x 196 wide
    cols5 = [16, 215, 414, 613, 812]
    pw5 = 196
    for i in range(5):
        draw_panel_small(d, img, cols5[i], 322, pw5, 146, CORE[3 + i])
    for i in range(5):
        draw_panel_small(d, img, cols5[i], 472, pw5, 146, CORE[8 + i])

    # --- bottom band: map (left) + ALSO ON (right) ---
    # Map box
    mx0, my0, mx1, my1 = 16, 622, 424, 1008
    d.rectangle([mx0, my0, mx1, my1], fill=MAP_BG, outline=BORDER)
    d.text((mx0 + 10, my0 + 7), "WHERE IT HAPPENED", font=F_SANS_B(12), fill=INK)
    d.text((mx1 - 10, my0 + 8), "13 numbered stories",
           font=F_SANS(10), fill=GREY, anchor="ra")
    map_x0, map_y0, map_w, map_h = mx0 + 8, my0 + 28, mx1 - mx0 - 16, 300
    for name, pts in CONTINENTS.items():
        xy = [project(lon, lat, map_x0, map_y0, map_w, map_h) for lon, lat in pts]
        d.polygon(xy, fill=MAP_LAND, outline=MAP_EDGE)
    for label, lon, lat in CONTINENT_LABELS:
        lx, ly = project(lon, lat, map_x0, map_y0, map_w, map_h)
        f = F_SANS_B(8)
        d.text((lx - d.textlength(label, font=f) / 2, ly - 4), label,
               font=f, fill=(120, 114, 96))
    # pins: numbered 1-13 first, then gold dots for ALSO ON
    placed = []
    for s in CORE:
        num, _k, _r, _ki, _h, _de, lon, lat, _y = s
        px, py = project(lon, lat, map_x0, map_y0, map_w, map_h)
        px, py = place_pin(px, py, placed, 21)
        placed.append((px, py))
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = F_SANS_B(9)
        tw = d.textlength(str(num), font=f)
        d.text((px - tw / 2, py - 6), str(num), font=f, fill=(255, 255, 255))
    for _n, _r, _h, _s, lon, lat in ALSO:
        px, py = project(lon, lat, map_x0, map_y0, map_w, map_h)
        px, py = place_pin(px, py, placed, 12)
        placed.append((px, py))
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GOLD,
                  outline=(255, 255, 255), width=1)
    # legend + sources
    ly = my1 - 34
    lx = mx0 + 10
    for name in ["EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "AMERICAS", "OCEANIA", "WORLD"]:
        d.rectangle([lx, ly + 2, lx + 8, ly + 10], fill=REGIONS[name])
        lx += 11
        f = F_SANS_B(8)
        d.text((lx, ly), name, font=f, fill=GREY)
        lx += int(d.textlength(name, font=f)) + 8
    d.text((mx0 + 10, my1 - 18),
           "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 Al Jazeera \u00b7 Bloomberg \u2014 18 Nov 2026. All drawings original.",
           font=F_SANS(9), fill=GREY)

    # ALSO ON — 3 columns, 2-line wrapped items
    ax0, ax1 = 432, 1008
    d.text((ax0, 628), "ALSO ON WEDNESDAY 18 NOVEMBER", font=F_SANS_B(14), fill=RED)
    d.line([(ax0, 646), (ax1, 646)], fill=RED, width=1)
    col_x = [432, 624, 816]
    col_w = [184, 184, 192]
    col_items = [ALSO[0:10], ALSO[10:20], ALSO[20:29]]
    for ci in range(3):
        yy = 654
        for num, region, headline, summary, _lon, _lat in col_items[ci]:
            # Number in bold 9px; text wrapped with the BOLD font for
            # measurement so the bold headline on line 1 can never overflow
            # into the next column (bold is the widest rendering).
            f_num = F_SANS_B(9)
            d.text((col_x[ci], yy), f"{num}.", font=f_num, fill=REGIONS[region])
            num_w = d.textlength(f"{num}.", font=f_num) + 4
            avail = col_w[ci] - num_w
            text = headline + " \u2014 " + summary
            lines = wrap_lines(d, text, F_SANS_B(9), avail, 2)
            x = col_x[ci] + num_w
            f_head = F_SANS_B(9)
            f_body = F_SANS(9)
            for li, ln in enumerate(lines):
                if li == 0 and ln.startswith(headline):
                    d.text((x, yy), headline, font=f_head, fill=INK)
                    hw = d.textlength(headline, font=f_head)
                    rest = ln[len(headline):]
                    if rest:
                        d.text((x + hw, yy), rest, font=f_body, fill=(58, 58, 58))
                else:
                    d.text((x, yy), ln, font=f_body, fill=(58, 58, 58))
                yy += 12
            yy += 1  # gap between items

    # DATE CHECK box (bottom of ALSO ON area)
    dx0, dy0, dx1, dy1 = 432, 924, 1008, 1008
    d.rectangle([dx0, dy0, dx1, dy1], outline=RED, width=1)
    d.text((dx0 + 8, dy0 + 6), "DATE CHECK", font=F_SANS_B(10), fill=RED)
    check = ("Left out on purpose because they were first reported on 17 Nov, "
             "not today: the An-12 crash in Siberia (19 killed), the US losing "
             "measles-free status, Peltola's Alaska Senate win, and Mongolia's "
             "president resigning.")
    lines = wrap_lines(d, check, F_SANS(10), dx1 - dx0 - 16, 4)
    yy = dy0 + 22
    for ln in lines:
        d.text((dx0 + 8, yy), ln, font=F_SANS(10), fill=(58, 58, 58))
        yy += 13

    return img


def main():
    img = build()
    out = BASE / "entry-v3.png"
    img.save(out, format="PNG", optimize=True)
    size = out.stat().st_size
    print(f"entry-v3.png: {img.size}, {size} bytes")
    if size > 1_048_576:
        out_jpg = BASE / "entry-v3.jpg"
        img.save(out_jpg, format="JPEG", quality=90)
        print(f"PNG too big; JPEG fallback: {out_jpg.stat().st_size} bytes")


if __name__ == "__main__":
    main()
