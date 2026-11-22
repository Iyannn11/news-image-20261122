#!/usr/bin/env python3
"""Render the News 22 broadsheet: 'Sunday 22 November 2026 — 35 Stories'.

Written fresh for Round 5. All story data is typed inline below.
Deterministic: no randomness, no timestamps in the image.
Usage: python3 render.py [output.png]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (26, 26, 26)
RED = (176, 30, 36)
GREY = (90, 86, 78)
LINE = (200, 192, 172)
CARD = (255, 255, 255)
MAP_BG = (226, 232, 236)
LAND = (232, 217, 184)
LAND_EDGE = (184, 168, 136)

FD = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

REGION_COLORS = {
    "EUROPE": (31, 78, 121),
    "ASIA": (122, 74, 0),
    "MIDDLE EAST": (122, 31, 31),
    "AFRICA": (31, 107, 74),
    "AMERICAS": (91, 45, 142),
    "OCEANIA": (14, 107, 122),
    "GLOBAL": (176, 30, 36),
}

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, spacing=3, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y

def text_h(fnt):
    return fnt.size

# ---------------------------------------------------------------- stories
# Six-fact strip: (tag, text)
FACTS = [
    ("RUSSIA", "550 munitions fired at Ukraine overnight"),
    ("COP31", "Objections close 03:00 GMT; vote 06:00 GMT"),
    ("F1", "Verstappen wins in Vegas; Red Bull 1–2"),
    ("CRICKET", "Head 123 off 83 seals Ashes win"),
    ("BITCOIN", "Falls below $60,000"),
    ("POPE", "Lunch with 1,300 poor people"),
]

# Big cards: (tag, place, headline, body, footer)
BIG = [
    ("GLOBAL", "ANTALYA", "COP31: OVERTIME",
     "New package proposed overnight; vote 06:00 GMT. The draft still "
     "omits fossil fuels.",
     "Climate talks · second overtime day"),
    ("AMERICAS", "LAS VEGAS", "VERSTAPPEN WINS VEGAS",
     "Verstappen wins the Las Vegas Grand Prix — Red Bull 1–2, "
     "Hadjar P2, Russell P3.",
     "Formula 1 · race 04:00 UTC"),
    ("EUROPE", "UKRAINE", "550 MUNITIONS OVERNIGHT",
     "Russia fires 496 drones and 53 missiles at Ukraine overnight — "
     "5 killed, 10 injured.",
     "Air force figures · Sunday"),
]

# Small cards: (tag, place, headline, body)
SMALL = [
    ("ASIA", "WELLINGTON", "INDIA 720/9 — RECORD IN NZ",
     "Highest Test total ever in NZ. Pant 128, Rahul 136; NZ 33/1 at tea."),
    ("ASIA", "CIKANDE", "INDONESIA FACTORY FIRE",
     "3 dead, 36 missing after a fire at a candy factory in Cikande, Serang."),
    ("MIDDLE EAST", "GAZA", "GAZA: STORM FLOODS TENTS",
     "5 killed, four of them children, as a sandbank collapses on tents."),
    ("GLOBAL", "", "BITCOIN BELOW $60,000",
     "Falls to $58,994 at 05:25 UTC after Friday's plunge to $55,130."),
    ("EUROPE", "VATICAN", "POPE LEO XIV'S SUNDAY",
     "Noon Angelus, then lunch with 1,300 poor people in the Paul VI Hall."),
    ("ASIA", "NEW DELHI", "NEPAL PM ARRIVES IN DELHI",
     "PM Balendra Shah arrives for a two-day state visit; Modi talks Monday."),
    ("ASIA", "BEIJING", "CHINA HITS BACK AT FCC BAN",
     "Beijing opposes the FCC vote barring three Chinese carriers from US numbers."),
    ("ASIA", "HONG KONG", "HONG KONG GOES TO THE POLLS",
     "856 candidates chase 723 seats; polls open 9am–6pm across 31 subsectors."),
    ("EUROPE", "GERMANY", "GERMANY: 23,000 TO STRIKE",
     "IG Metall calls a 24-hour Monday strike at Mercedes and Meyer Werft."),
    ("OCEANIA", "PERTH", "ASHES: HEAD 123 OFF 83",
     "Travis Head's 123 off 83 seals an eight-wicket win inside two days."),
]

# Also on Sunday, stories 14–35: (lead, text)
ALSO = [
    ("JURA", "Orange alert: 70–90mm rain to midnight"),
    ("UK–EU ROW", "Tories attack deal; in force 2028"),
    ("STARLINK FIRE", "Two arrested in Germany over Poland blaze"),
    ("MYANMAR", "M4.1 quake, 02:35 IST, depth 95km"),
    ("SHENZHOU XXIV", "Site ready; crewed flight due 25 Nov"),
    ("SUMATRA QUAKE", "M4.2 off West Sumatra; no tsunami threat"),
    ("MARCOS", "\u201cDetails being fixed\u201d on Trump\u2019s food demand"),
    ("DELHI AIR", "AQI 295, \u201cvery unhealthy\u201d; PM2.5 hazardous"),
    ("IRGC CLAIM", "Strikes claimed on two US Patriot radars"),
    ("EISENKOT", "Coalition talks with Likud open Sunday"),
    ("PORSCHE", "Icons of Porsche opens in Dubai"),
    ("AOUN", "Demands Israeli withdrawal on Independence Day"),
    ("TURKEY", "Israel blocking Gaza container homes, Ankara says"),
    ("S. AFRICA", "Yellow Level 2 storm + fire danger warning"),
    ("KHAYELITSHA", "Shooting: 4 dead, 6 injured"),
    ("BENIN", "Asks France for 35 more royal treasures"),
    ("SPACEX", "NROL-136 due 12:16 UTC from Vandenberg"),
    ("F1 ACADEMY", "Palmowski wins in Vegas; Campos take title"),
    ("WEMBANYAMA", "50 pts, 19 reb as Spurs beat Pelicans"),
    ("KNICKS", "Bridges buzzer-beater beats Blazers 97–96"),
    ("MLS", "Columbus beat Messi\u2019s Miami 3–0 in playoff"),
    ("MACARTHUR", "Beat Wellington 2–1, leaders\u2019 first defeat"),
]

REGIONS = [
    ("EUROPE", 6), ("ASIA", 10), ("MIDDLE EAST", 6), ("AFRICA", 3),
    ("AMERICAS", 6), ("OCEANIA", 2), ("GLOBAL", 2),
]

# Map dots: (lon, lat, region)
DOTS = [
    (30.7, 36.9, "GLOBAL"), (-115.1, 36.2, "AMERICAS"),
    (30.5, 50.4, "EUROPE"), (174.8, -41.3, "ASIA"),
    (106.2, -6.1, "ASIA"), (34.35, 31.4, "MIDDLE EAST"),
    (12.45, 41.9, "EUROPE"), (77.2, 28.6, "ASIA"),
    (116.4, 39.9, "ASIA"), (114.2, 22.3, "ASIA"),
    (13.4, 52.5, "EUROPE"), (115.85, -31.95, "OCEANIA"),
    (5.9, 46.7, "EUROPE"), (-0.1, 51.5, "EUROPE"),
    (19.4, 52.0, "EUROPE"), (96.0, 21.9, "ASIA"),
    (100.3, 40.9, "ASIA"), (100.5, -0.5, "ASIA"),
    (121.0, 14.6, "ASIA"), (50.6, 26.2, "MIDDLE EAST"),
    (34.8, 32.1, "MIDDLE EAST"), (55.3, 25.2, "MIDDLE EAST"),
    (35.5, 33.9, "MIDDLE EAST"), (32.9, 39.9, "MIDDLE EAST"),
    (28.0, -26.2, "AFRICA"), (18.7, -34.0, "AFRICA"),
    (2.6, 6.5, "AFRICA"), (-120.6, 34.7, "AMERICAS"),
    (-98.5, 29.4, "AMERICAS"), (-74.0, 40.7, "AMERICAS"),
    (-83.0, 40.0, "AMERICAS"), (151.2, -33.9, "OCEANIA"),
]

# Rough continent outlines in (lon, lat).
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-75, 72), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
     (-80, 25), (-85, 20), (-90, 15), (-95, 18), (-100, 20), (-110, 23),
     (-120, 30), (-125, 40), (-130, 50), (-140, 60), (-155, 58), (-165, 60)],
    [(-55, 60), (-45, 60), (-40, 70), (-50, 76), (-60, 74), (-58, 68)],
    [(-80, 10), (-75, 5), (-70, 0), (-60, -5), (-50, -5), (-40, -10),
     (-35, -15), (-40, -25), (-50, -30), (-60, -35), (-65, -40), (-70, -50),
     (-75, -45), (-75, -30), (-80, -15), (-82, -5)],
    [(-10, 36), (-5, 40), (-2, 44), (0, 48), (5, 50), (8, 55), (12, 58),
     (18, 60), (25, 62), (30, 60), (28, 55), (25, 50), (20, 45), (15, 40),
     (10, 38), (5, 36), (0, 38)],
    [(-10, 35), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 20),
     (45, 12), (50, 10), (48, 0), (42, -5), (40, -15), (35, -25), (30, -30),
     (25, -33), (20, -35), (15, -30), (12, -20), (10, -10), (8, 0), (5, 5),
     (-5, 5), (-10, 15), (-15, 25)],
    [(30, 60), (40, 65), (50, 68), (60, 70), (70, 72), (80, 73), (90, 75),
     (100, 76), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 65), (162, 60), (160, 55), (155, 50), (150, 45), (145, 40),
     (140, 35), (135, 33), (130, 32), (127, 35), (122, 38), (120, 32),
     (115, 25), (110, 20), (108, 12), (105, 8), (100, 8), (98, 15), (95, 20),
     (90, 22), (85, 20), (80, 15), (75, 10), (72, 20), (65, 25), (60, 25),
     (55, 27), (50, 30), (48, 30), (45, 32), (42, 36), (38, 36), (35, 36),
     (32, 40), (30, 45), (30, 55)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (150, -25),
     (146, -20), (142, -15), (140, -12), (135, -12), (132, -11), (130, -13),
     (126, -14), (122, -17), (118, -20)],
]

# ---------------------------------------------------------------- drawing
def draw_header(draw):
    draw.rectangle([0, 0, W, 28], fill=RED)
    draw.text((24, 6), "THE WORLD IN ONE DAY", font=SANS_B(15), fill=(255, 255, 255))
    right = "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    tw = draw.textlength(right, font=SANS_B(12))
    draw.text((W - 24 - tw, 8), right, font=SANS_B(12), fill=(255, 255, 255))

def draw_masthead(draw):
    title = "Sunday 22 November 2026"
    f = SERIF_B(60)
    tw = draw.textlength(title, font=f)
    draw.text(((W - tw) / 2, 34), title, font=f, fill=INK)
    deck = ("From a Las Vegas Grand Prix to a Pope\u2019s lunch with the poor "
            "\u2014 the whole world, in one day.")
    f2 = SERIF_I(17)
    tw2 = draw.textlength(deck, font=f2)
    draw.text(((W - tw2) / 2, 102), deck, font=f2, fill=GREY)

def draw_facts(draw):
    y0, y1 = 126, 170
    gap, n = 6, 6
    cw = (W - 48 - gap * (n - 1)) / n
    for i, (tag, text) in enumerate(FACTS):
        x0 = 24 + i * (cw + gap)
        draw.rectangle([x0, y0, x0 + cw, y1], outline=LINE, width=1)
        draw.rectangle([x0, y0, x0 + cw, y0 + 2], fill=REGION_COLORS.get(tag, RED))
        draw.text((x0 + 7, y0 + 6), tag, font=SANS_B(10), fill=REGION_COLORS.get(tag, RED))
        draw_wrapped(draw, x0 + 7, y0 + 20, text, SANS(11), cw - 14, spacing=1, max_lines=2)

def draw_big_cards(draw):
    y0, y1 = 176, 322
    gap = 8
    cw = (W - 48 - gap * 2) / 3
    for i, (tag, place, head, body, foot) in enumerate(BIG):
        x0 = 24 + i * (cw + gap)
        draw.rectangle([x0, y0, x0 + cw, y1], fill=CARD, outline=LINE, width=1)
        draw.rectangle([x0, y0, x0 + cw, y0 + 3], fill=REGION_COLORS[tag])
        label = tag + (" \u00b7 " + place if place else "")
        draw.text((x0 + 10, y0 + 10), label, font=SANS_B(12), fill=REGION_COLORS[tag])
        y = draw_wrapped(draw, x0 + 10, y0 + 30, head, SERIF_B(25), cw - 20, spacing=1, max_lines=2)
        y = draw_wrapped(draw, x0 + 10, y + 4, body, SANS(12), cw - 20, spacing=2, max_lines=2)
        draw.text((x0 + 10, y1 - 18), foot, font=SANS(11), fill=GREY)

def draw_small_cards(draw, rows_y):
    gap_x, gap_y = 6, 6
    cw = (W - 48 - gap_x * 4) / 5
    ch = 92
    for r, y0 in enumerate(rows_y):
        for c in range(5):
            idx = r * 5 + c
            tag, place, head, body = SMALL[idx]
            x0 = 24 + c * (cw + gap_x)
            draw.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD, outline=LINE, width=1)
            draw.rectangle([x0, y0, x0 + cw, y0 + 2], fill=REGION_COLORS[tag])
            label = tag + (" \u00b7 " + place if place else "")
            draw.text((x0 + 7, y0 + 6), label, font=SANS_B(10), fill=REGION_COLORS[tag])
            y = draw_wrapped(draw, x0 + 7, y0 + 20, head, SANS_B(14), cw - 14, spacing=1, max_lines=2)
            draw_wrapped(draw, x0 + 7, y + 2, body, SANS(11), cw - 14, spacing=1, max_lines=3)

def project(lon, lat, mx0, my0, mw, mh):
    x = mx0 + (lon + 180.0) / 360.0 * mw
    y = my0 + (90.0 - lat) / 180.0 * mh
    return (x, y)

def draw_map_row(draw):
    y0, y1 = 524, 690
    # --- map panel (left) ---
    mx0, mx1 = 24, 430
    draw.rectangle([mx0, y0, mx1, y1], fill=MAP_BG, outline=LINE, width=1)
    draw.text((mx0 + 10, y0 + 6), "WHERE IT HAPPENED", font=SANS_B(13), fill=INK)
    # true 2:1 equirectangular map, centred in the panel
    mw, mh = 276, 138
    px = mx0 + (mx1 - mx0 - mw) / 2
    py = y0 + 22
    for poly in CONTINENTS:
        pts = [project(lon, lat, px, py, mw, mh) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for lon, lat, region in DOTS:
        x, y = project(lon, lat, px, py, mw, mh)
        r = 3
        draw.ellipse([x - r, y - r, x + r, y + r],
                     fill=REGION_COLORS[region], outline=(255, 255, 255))
    # --- tally panel (right) ---
    tx0, tx1 = 442, 1000
    draw.rectangle([tx0, y0, tx1, y1], fill=CARD, outline=LINE, width=1)
    draw.text((tx0 + 12, y0 + 6), "STORIES BY REGION", font=SANS_B(13), fill=INK)
    col_w = (tx1 - tx0 - 24) / 2
    for i, (region, count) in enumerate(REGIONS):
        col = i % 2
        row = i // 2
        x = tx0 + 12 + col * col_w
        y = y0 + 32 + row * 30
        r = 5
        draw.ellipse([x, y + 2, x + 2 * r, y + 2 + 2 * r], fill=REGION_COLORS[region])
        draw.text((x + 16, y), region, font=SANS_B(13), fill=INK)
        cnt = "\u00b7 " + str(count)
        draw.text((x + 16 + draw.textlength(region, font=SANS_B(13)) + 6, y),
                  cnt, font=SANS_B(13), fill=GREY)

def draw_date_check(draw):
    y0, y1 = 696, 734
    draw.rectangle([24, y0, 1000, y1], fill=(255, 245, 245), outline=RED, width=2)
    label = "DATE CHECK"
    f = SANS_B(12)
    lw = draw.textlength(label, font=f)
    draw.rectangle([36, y0 - 9, 36 + lw + 12, y0 + 9], fill=RED)
    draw.text((42, y0 - 8), label, font=f, fill=(255, 255, 255))
    text = ("Every story above happened, or was first reported, on Sunday "
            "22 November 2026. Earlier stories were checked and rejected "
            "\u2014 see SOURCES.md.")
    draw.text((36, y0 + 14), text, font=SANS(12), fill=INK)

def draw_also(draw):
    y0 = 740
    draw.text((24, y0), "ALSO ON SUNDAY \u00b7 22 MORE STORIES", font=SANS_B(14), fill=INK)
    draw.line([24, y0 + 22, 1000, y0 + 22], fill=INK, width=1)
    col_w = (1000 - 24 - 30) / 2
    for i, (lead, text) in enumerate(ALSO):
        col = i // 11
        row = i % 11
        x = 24 + col * (col_w + 30)
        y = y0 + 30 + row * 18
        num = str(14 + i) + ". "
        draw.text((x, y), num, font=SANS_B(12), fill=INK)
        nx = x + draw.textlength(num, font=SANS_B(12))
        draw.text((nx, y), lead, font=SANS_B(12), fill=INK)
        lx = nx + draw.textlength(lead, font=SANS_B(12))
        draw.text((lx, y), " \u2014 " + text, font=SANS(12), fill=INK)

def draw_footer(draw):
    foot = ("THE WORLD IN ONE DAY \u00b7 SUNDAY 22 NOVEMBER 2026 \u00b7 "
            "35 STORIES \u00b7 7 REGIONS \u00b7 DRAWN 22 NOVEMBER 2026")
    f = SANS(11)
    tw = draw.textlength(foot, font=f)
    draw.text(((W - tw) / 2, 968), foot, font=f, fill=GREY)

def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_masthead(draw)
    draw_facts(draw)
    draw_big_cards(draw)
    draw_small_cards(draw, [328, 426])
    draw_map_row(draw)
    draw_date_check(draw)
    draw_also(draw)
    draw_footer(draw)
    return img

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build().save(out, "PNG")
    print("wrote", out)
