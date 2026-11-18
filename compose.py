#!/usr/bin/env python3
"""Composite the news-image-20261118 resubmit front page (1024x1024).

Denser than the first entry: the same 5 big stories (Gulf hero + 4 panels)
plus a world map marking story locations and a 28-item "Around the world"
list, for 33 stories in all -- the winner pattern (30+ stories + map).

Layout (1024x1024):
  masthead 0-84 (navy, title + date)
  hero     92-280 (Gulf, full width, headline overlay)
  4 panels 288-460 (photo + kicker + headline + sub)
  header   470-499 (AROUND THE WORLD - 28 MORE STORIES)
  map      500-756 (left, 480 wide, PIL-drawn world map + dots)
  list col 500-750 (right of map, 10 items)
  list 2col 766-991 (bottom, 9 + 9 items)
  footer   1004 (date line)
All text is rendered with PIL (DejaVu) -- no AI-generated text anywhere.
Deterministic: fixed coordinates, no randomness. Output is JPEG bytes
(saved as entry.png -- the gate reads magic bytes, JPEG is allowed).
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
WORK = "/home/hatch/workspace/makefun/news-image-20261118-work/scenes"
OUT = "/home/hatch/workspace/makefun/news-image-20261118-work/entry.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (13, 43, 69)
GOLD = (245, 179, 1)
RED = (198, 32, 32)
DARK = (20, 20, 20)
GRAY = (68, 68, 68)
LIGHT = (217, 217, 217)
WHITE = (255, 255, 255)
OCEAN = (232, 240, 247)
LAND = (203, 216, 227)
LAND_EDGE = (148, 168, 184)


def font(path, size):
    return ImageFont.truetype(path, size)


def crop_fill(im, tw, th):
    """Center-crop to target aspect, then resize (LANCZOS)."""
    sw, sh = im.size
    ta, sa = tw / th, sw / sh
    if sa > ta:
        nw = int(sh * ta)
        x0 = (sw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, sh))
    else:
        nh = int(sw / ta)
        y0 = (sh - nh) // 2
        im = im.crop((0, y0, sw, y0 + nh))
    return im.resize((tw, th), Image.LANCZOS)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to max width; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_cyclone(tw, th):
    """Stylised weather-map cyclone panel (no photo needed)."""
    img = Image.new("RGB", (tw, th), (24, 52, 74))
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(th):
        t = y / th
        r = int(24 + (58 - 24) * t)
        g = int(52 + (96 - 52) * t)
        b = int(74 + (128 - 74) * t)
        d.line([(0, y), (tw, y)], fill=(r, g, b))
    d.rectangle([0, th - 52, tw, th], fill=(14, 38, 60))
    for i, yy in enumerate(range(th - 46, th - 6, 12)):
        d.arc([6 + i * 3, yy, tw - 6 - i * 3, yy + 18], 0, 180,
              fill=(120, 170, 210, 160), width=2)
    cx, cy = tw // 2, th // 2 - 18
    for k in range(5):
        r = 18 + k * 17
        start = 20 + k * 55
        ox, oy = cx + k * 7, cy + k * 5
        d.arc([ox - r, oy - r, ox + r, oy + r], start, start + 300,
              fill=(255, 255, 255, 235 - k * 28), width=7)
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(16, 34, 52))
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=(255, 255, 255, 220), width=2)
    for i in range(34):
        x = (i * 53) % (tw + 20) - 10
        y = (i * 37) % (th - 70) + 8
        d.line([(x, y), (x - 7, y + 16)], fill=(190, 215, 235, 150), width=2)
    d.polygon([(0, th), (0, th - 34), (52, th - 52), (96, th - 30), (120, th - 44),
               (150, th - 26), (150, th)], fill=(38, 66, 48))
    return img.filter(ImageFilter.GaussianBlur(0.4))


# ---- world map: simplified continent outlines in (lon, lat) ----
NORTH_AMERICA = [
    (-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 58),
    (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24),
    (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9),
    (-80, 8), (-79, 9), (-82, 13), (-85, 16), (-87, 13), (-88, 18),
    (-90, 21), (-91, 19), (-96, 19), (-97, 26), (-93, 30), (-89, 30),
    (-84, 30), (-81, 25), (-80, 32), (-76, 35), (-75, 39), (-74, 40),
    (-70, 42), (-68, 44), (-65, 44), (-60, 47), (-55, 47), (-60, 52),
    (-65, 58), (-68, 58), (-75, 62), (-78, 62), (-85, 66), (-92, 66),
    (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68),
]
GREENLAND = [
    (-45, 60), (-40, 62), (-35, 65), (-30, 68), (-25, 70), (-20, 72),
    (-22, 75), (-30, 78), (-40, 80), (-50, 78), (-55, 75), (-58, 72),
    (-55, 68), (-50, 64),
]
SOUTH_AMERICA = [
    (-80, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
    (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
    (-66, -55), (-68, -50), (-65, -45), (-62, -40), (-57, -38), (-52, -33),
    (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3),
    (-44, -2), (-50, 0), (-52, 5), (-55, 6), (-60, 8), (-62, 9),
    (-68, 11), (-72, 12), (-75, 11), (-77, 8),
]
AFRICA = [
    (-17, 15), (-16, 20), (-15, 27), (-10, 31), (-5, 35), (0, 36),
    (10, 37), (11, 34), (15, 32), (20, 32), (25, 31), (30, 31), (32, 31),
    (34, 28), (35, 23), (37, 18), (39, 15), (43, 12), (48, 11), (51, 12),
    (46, 5), (42, 0), (40, -5), (40, -10), (38, -15), (35, -20), (32, -26),
    (28, -33), (26, -34), (20, -35), (17, -32), (15, -27), (13, -18),
    (12, -10), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 12),
]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (44, -25), (43, -21)]
EUROPE = [
    (-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49),
    (0, 50), (2, 51), (5, 53), (8, 55), (8, 57), (10, 59), (5, 60),
    (5, 62), (10, 64), (12, 66), (18, 69), (25, 71), (30, 70), (32, 68),
    (35, 66), (40, 64), (44, 62), (48, 60), (50, 59), (46, 56), (44, 52),
    (40, 50), (38, 47), (35, 45), (30, 45), (28, 44), (23, 40), (22, 37),
    (26, 38), (30, 36), (28, 37), (23, 36), (19, 40), (15, 44), (12, 44),
    (8, 44), (3, 42), (0, 40), (-2, 37), (-6, 36), (-9, 37),
]
BRITAIN = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-2, 50)]
ASIA = [
    (30, 36), (33, 36), (36, 36), (36, 33), (40, 32), (44, 30), (48, 30),
    (50, 29), (54, 27), (57, 26), (58, 25), (61, 25), (66, 25), (70, 22),
    (72, 20), (76, 18), (77, 15), (80, 13), (80, 10), (77, 8), (80, 7),
    (82, 10), (85, 15), (88, 22), (91, 22), (93, 18), (95, 16), (98, 14),
    (100, 12), (103, 10), (105, 9), (107, 11), (109, 13), (106, 20),
    (108, 18), (110, 20), (114, 22), (118, 25), (120, 28), (122, 30),
    (120, 35), (122, 38), (124, 40), (127, 40), (130, 42), (132, 43),
    (135, 44), (138, 46), (140, 48), (142, 50), (142, 53), (140, 55),
    (137, 58), (135, 60), (132, 62), (135, 65), (140, 68), (145, 70),
    (150, 70), (155, 68), (158, 65), (160, 62), (162, 60), (163, 64),
    (170, 66), (178, 65), (178, 68), (173, 64), (170, 60), (162, 58),
    (158, 53), (155, 50), (150, 48), (145, 45), (140, 40), (135, 38),
    (130, 35), (127, 34), (126, 38), (124, 40), (122, 38), (120, 35),
    (118, 30), (115, 25), (110, 20), (108, 18), (105, 15), (102, 12),
    (100, 10), (97, 12), (95, 15), (92, 18), (90, 22), (86, 20), (83, 17),
    (80, 14), (77, 10), (74, 12), (72, 18), (70, 22), (66, 25), (62, 25),
    (58, 26), (54, 28), (50, 30), (46, 30), (42, 32), (38, 34), (35, 36),
    (32, 36),
]
JAPAN = [
    (130, 31), (132, 33), (134, 34), (137, 35), (139, 36), (140, 38),
    (141, 40), (142, 42), (144, 44), (143, 43), (141, 40), (140, 37),
    (138, 35), (136, 34), (133, 33), (131, 32),
]
SE_ASIA_ISLANDS = [
    (95, 5), (98, 7), (100, 5), (102, 2), (104, 0), (106, -2), (108, -4),
    (110, -6), (112, -7), (114, -8), (116, -9), (118, -10), (120, -10),
    (122, -9), (124, -8), (126, -6), (128, -4), (130, -2), (131, 0),
    (128, 2), (126, 4), (124, 6), (122, 8), (120, 10), (118, 12),
    (116, 14), (114, 16), (112, 18), (110, 20), (108, 21), (106, 20),
    (104, 18), (102, 16), (100, 14), (98, 12), (96, 10), (95, 7),
]
AUSTRALIA = [
    (113, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
    (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
    (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
    (140, -17), (136, -15), (135, -12), (132, -12), (130, -13), (126, -14),
    (122, -17), (118, -20),
]
NEW_ZEALAND = [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (175, -40), (172, -42), (169, -44)]

CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, MADAGASCAR,
              EUROPE, BRITAIN, ASIA, JAPAN, SE_ASIA_ISLANDS, AUSTRALIA, NEW_ZEALAND]

# (lon, lat, label, anchor, dx, dy) -- anchor: PIL anchor for the label
DOTS = [
    (50.5, 26.2, "GULF", "lm", 8, -2),
    (34.0, 45.0, "CRIMEA", "lm", 8, 4),
    (121.0, 14.6, "MANILA", "lm", 8, 6),
    (114.1, 22.5, "SHENZHEN", "mb", 0, -10),
    (-150.0, 64.0, "ALASKA", "lm", 8, -2),
    (23.0, -3.0, "CONGO", "lm", 8, -2),
    (34.5, 31.5, "GAZA", "rm", -8, 0),
    (87.0, 55.3, None, None, 0, 0),        # Siberia plane crash
    (147.0, -6.3, None, None, 0, 0),       # Papua New Guinea quake
    (-160.0, -21.0, None, None, 0, 0),     # Cyclone Xavier, Cook Islands
    (2.3, 48.9, None, None, 0, 0),         # France protests
    (-0.1, 51.5, None, None, 0, 0),        # London / UK climate
    (30.0, 13.0, None, None, 0, 0),        # Sudan
    (-90.5, 15.0, None, None, 0, 0),       # Guatemala
    (24.0, 56.9, None, None, 0, 0),        # Latvia
    (10.7, 59.9, None, None, 0, 0),        # Norway
    (151.0, -33.9, None, None, 0, 0),      # Australia sanctions
    (80.0, 16.0, None, None, 0, 0),        # India: Cyclone Akvan, Dhoni
    (-66.0, 6.5, None, None, 0, 0),        # Venezuela
    (-77.0, 38.9, None, None, 0, 0),       # Washington: measles, outages
    (174.0, -41.0, None, None, 0, 0),      # New Zealand: GTA VI first
]


def draw_world_map(tw, th):
    """Simple equirectangular world map (lat 85..-55) with story dots."""
    img = Image.new("RGB", (tw, th), OCEAN)
    d = ImageDraw.Draw(img)

    def proj(lon, lat):
        x = (lon + 180.0) / 360.0 * tw
        y = (85.0 - lat) / 140.0 * th
        return (x, y)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    f_cap = font(BOLD, 13)
    d.text((10, 8), "WHERE IT HAPPENED", font=f_cap, fill=(90, 110, 128))
    f_lab = font(BOLD, 12)
    for lon, lat, label, anchor, dx, dy in DOTS:
        x, y = proj(lon, lat)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=RED, outline=WHITE, width=1)
        if label:
            # white halo for legibility, then navy text
            for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                d.text((x + dx + ox, y + dy + oy), label, font=f_lab,
                       fill=WHITE, anchor=anchor)
            d.text((x + dx, y + dy), label, font=f_lab, fill=NAVY, anchor=anchor)
    return img


# ---- the 28 short stories: (headline, detail) ----
MORE_STORIES = [
    ("APEC opens in Shenzhen", "Xi hosts Putin; summit Thursday"),
    ("Democrats take Alaska", "Peltola wins; party reaches 56"),
    ("Ebola surge in Congo", "11,000 cases, 5,400 dead"),
    ("US loses measles-free status", "5,400 cases end 26-year run"),
    ("Russian plane crash", "Military jet down; 19 killed"),
    ("Quake hits Papua New Guinea", "Magnitude 6.0 strikes"),
    ("Quake in Romania", "5.3-magnitude tremor"),
    ("Cyclone Xavier", "Category 5 hits Cook Islands"),
    ("World Court rules on Myanmar", "Genocide verdict due"),
    ("Gaza cold kills in tents", "Freezing nights; aid blocked"),
    ("US details $12bn Venezuela oil", "Maduro revenue report"),
    ("France protests: 4th weekend", "Cost-of-living marches"),
    ("Eisenkot to form government", "Bypasses Netanyahu"),
    ("Cyber-attack hits supermarkets", "Freezers down in 7 states"),
    ("Australia sanctions West Bank", "3 people, 4 entities"),
    ("Norway holds threat level 3", "Threat level stays at 3/5"),
    ("Latvia confirms new cabinet", "Kulbergs wins vote"),
    ("Guatemala prosecutor shot", "Investigator wounded"),
    ("UN: 372 killed in Ukraine", "October toll, monitors say"),
    ("Sudan: 2,230 civilians dead", "Drones killed 1,630"),
    ("Grossi seeks UN top job", "IAEA chief bids for post"),
    ("GTA VI out at midnight", "Global launch Thursday"),
    ("Dhoni retires from IPL", "Cricket icon ends career"),
    ("Markets slide worldwide", "S&P -1%, DAX -2%, gold -2%"),
    ("US computer outages reach NSA", "Federal systems hit"),
    ("Solar flare M1.1 recorded", "Sun fires mid-strength flare"),
    ("UK climate targets at risk", "Weaker EV rules blamed"),
    ("WFP: one hot meal every two days", "Gaza rations food"),
]


def fit_line(draw, head, detail, max_w):
    """Build one dense-list line; trim the detail until it fits."""
    f_head = font(BOLD, 15)
    f_det = font(REG, 14)
    bullet = "\u2022  "
    w_bullet = draw.textlength(bullet, font=f_head)
    w_head = draw.textlength(head, font=f_head)
    sep = " \u2014 "
    w_sep = draw.textlength(sep, font=f_det)
    det = detail
    while det and w_bullet + w_head + w_sep + draw.textlength(det, font=f_det) > max_w:
        det = det[:-1]
    if det != detail:
        det = det.rstrip(" ,;:") + "\u2026"
    return bullet, head, sep, det


def draw_list_item(draw, x, y, head, detail, max_w):
    """Draw one dense-list line at (x, y); returns nothing."""
    f_head = font(BOLD, 15)
    f_det = font(REG, 14)
    bullet, head, sep, det = fit_line(draw, head, detail, max_w)
    cx = x
    draw.text((cx, y), bullet, font=f_head, fill=RED)
    cx += draw.textlength(bullet, font=f_head)
    draw.text((cx, y), head, font=f_head, fill=NAVY)
    cx += draw.textlength(head, font=f_head)
    draw.text((cx, y), sep, font=f_det, fill=GRAY)
    cx += draw.textlength(sep, font=f_det)
    draw.text((cx, y), det, font=f_det, fill=GRAY)


def main():
    page = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(page)

    # ---- masthead ----
    d.rectangle([0, 0, W, 84], fill=NAVY)
    f_title = font(BOLD, 46)
    f_date = font(BOLD, 24)
    t = "THE WORLD TODAY"
    d.text(((W - d.textlength(t, font=f_title)) / 2, 10), t, font=f_title, fill=WHITE)
    t = "WEDNESDAY \u00b7 18 NOVEMBER 2026"
    d.text(((W - d.textlength(t, font=f_date)) / 2, 56), t, font=f_date, fill=GOLD)
    d.rectangle([0, 84, W, 88], fill=GOLD)

    # ---- hero: Gulf ----
    gulf = Image.open(os.path.join(WORK, "media-generation-gulf-hero-0-e6e22ac0-99be-43c4-a1ca-3f944e11cc98.png")).convert("RGB")
    hero = crop_fill(gulf, 992, 188)
    page.paste(hero, (16, 92))
    grad = Image.new("RGBA", (992, 110), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for y in range(110):
        a = int(200 * (y / 110) ** 1.6)
        gd.line([(0, y), (992, y)], fill=(0, 0, 0, a))
    page.paste(grad, (16, 92 + 188 - 110), grad)
    hd = ImageDraw.Draw(page)
    f_hero = font(BOLD, 40)
    f_hero_sub = font(REG, 22)
    hd.text((32, 92 + 188 - 92), "GULF ON EDGE", font=f_hero, fill=WHITE)
    hd.text((32, 92 + 188 - 42), "Iran drones hit a US radar in Bahrain", font=f_hero_sub, fill=(235, 235, 235))

    # ---- 4 panels ----
    panels = [
        ("media-generation-ukraine-bridge-0-929fa7aa-96d2-4c30-a8ca-a86ca934069a.png",
         "WAR", "CRIMEA BRIDGE HIT AGAIN", "Second-day strike"),
        ("media-generation-manila-arrival-0-76ad6820-3d19-4961-a35c-b41f4364b649.png",
         "DIPLOMACY", "TRUMP LANDS IN MANILA", "Quad talks in Manila"),
        ("media-generation-nvidia-chip-0-515b6624-d983-4b96-bf3a-0ed4ee204739.png",
         "BUSINESS", "NVIDIA SOARS $115.8BN", "Record sales; Huang barred"),
        (None, "WEATHER", "CYCLONE AKVAN", "Severe storm nears Bengal"),
    ]
    px = [16, 267, 518, 769]
    pw = 239
    py = 288
    f_kick = font(BOLD, 14)
    f_head = font(BOLD, 20)
    f_sub = font(REG, 15)
    for i, (fname, kick, head, sub) in enumerate(panels):
        x = px[i]
        d.rectangle([x, py, x + pw, py + 172], outline=LIGHT, width=1)
        if fname:
            im = Image.open(os.path.join(WORK, fname)).convert("RGB")
            page.paste(crop_fill(im, pw, 88), (x, py))
        else:
            page.paste(draw_cyclone(pw, 88), (x, py))
        d.text((x + 10, py + 94), kick, font=f_kick, fill=RED)
        lines = wrap(d, head, f_head, pw - 20)[:2]
        yy = py + 112
        for line in lines:
            d.text((x + 10, yy), line, font=f_head, fill=NAVY)
            yy += 23
        d.text((x + 10, py + 150), sub, font=f_sub, fill=GRAY)

    # ---- section header ----
    d.line([(16, 470), (W - 16, 470)], fill=LIGHT, width=1)
    f_sec = font(BOLD, 19)
    d.text((16, 476), "AROUND THE WORLD \u2014 28 MORE STORIES", font=f_sec, fill=NAVY)
    f_sec_r = font(BOLD, 16)
    t = "33 STORIES IN ALL"
    d.text((W - 16 - d.textlength(t, font=f_sec_r), 478), t, font=f_sec_r, fill=RED)

    # ---- world map (left) ----
    page.paste(draw_world_map(480, 256), (16, 500))
    d.rectangle([16, 500, 496, 756], outline=LIGHT, width=1)

    # ---- dense list, column 1 (right of map) ----
    col1 = MORE_STORIES[0:10]
    for i, (head, detail) in enumerate(col1):
        draw_list_item(d, 508, 500 + i * 25, head, detail, 500)

    # ---- dense list, bottom two columns ----
    colA = MORE_STORIES[10:19]
    colB = MORE_STORIES[19:28]
    for i, (head, detail) in enumerate(colA):
        draw_list_item(d, 16, 766 + i * 25, head, detail, 490)
    for i, (head, detail) in enumerate(colB):
        draw_list_item(d, 518, 766 + i * 25, head, detail, 490)

    # ---- footer ----
    f_foot = font(BOLD, 16)
    t = "18 NOVEMBER 2026 \u2014 33 STORIES, ONE DAY"
    d.text(((W - d.textlength(t, font=f_foot)) / 2, 1004), t, font=f_foot, fill=GRAY)

    page.save(OUT, format="JPEG", quality=88, optimize=True, progressive=False)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
