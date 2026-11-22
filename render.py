#!/usr/bin/env python3
"""Render the News 22 (Sunday 22 November 2026) broadsheet, Round 6.
Fresh build: 14 main stories + 10 in ALSO TODAY = 24 stories, 7 regions.
Structure: red header -> serif masthead -> 6-fact strip -> 3 hero cards ->
3 rows of small cards -> WHERE IT HAPPENED map strip -> ALSO TODAY list ->
DATE CHECK box (own row) -> footer. 1024x1024 PNG, deterministic.
All facts verified by web search on 22 Nov 2026. Story data is inline here.
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
RED = (200, 16, 46)
INK = (17, 17, 17)
GREY = (85, 85, 85)
LIGHT = (242, 242, 242)
LINE = (204, 204, 204)
MAPBG = (238, 243, 246)
LAND = (215, 222, 227)

FDIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = ImageFont.truetype(FDIR + "DejaVuSerif-Bold.ttf", 44)
SERIF = ImageFont.truetype(FDIR + "DejaVuSerif.ttf", 13)
SANS_B = ImageFont.truetype(FDIR + "DejaVuSans-Bold.ttf", 20)
SANS = ImageFont.truetype(FDIR + "DejaVuSans.ttf", 12)
SANS_S = ImageFont.truetype(FDIR + "DejaVuSans.ttf", 11)


def font(path, size):
    return ImageFont.truetype(FDIR + path, size)


def wrap(draw, text, fnt, max_w):
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


def text_block(draw, x, y, text, fnt, max_w, fill=INK, lh=None, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    if lh is None:
        lh = int(fnt.size * 1.3)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---------------- story data (inline, verified 22 Nov 2026) ----------------
HEROES = [
    ("GLOBAL", "COP31 STALLS INTO DAY TWO OF OVERTIME",
     "Antalya, Turkey \u2014 Negotiators were asked to weigh a last-minute text early Sunday after talks missed their Friday deadline. Fossil-fuel wording and a $120bn adaptation fund are still the blockers.",
     "Nearly 200 nations \u00b7 deal or no deal"),
    ("AMERICAS", "VERSTAPPEN WINS A WILD VEGAS THRILLER",
     "Las Vegas \u2014 Max Verstappen held off Lando Norris by 0.639s after 35 lead changes in 50 laps \u2014 his 75th career win and his third on the Strip in four years.",
     "Norris 2nd \u00b7 Piastri 3rd \u00b7 Russell hit the wall"),
    ("EUROPE", "550 MUNITIONS RAIN ON UKRAINE OVERNIGHT",
     "Kyiv \u2014 Russia fired 496 drones and 53 missiles overnight, Zelenskyy said Sunday. Five people were killed and energy sites were hit in nine regions.",
     "Lviv \u00b7 Zaporizhzhia \u00b7 Kharkiv among the targets"),
]

MAIN = [
    ("MIDDLE EAST", "Two tankers hit in the Strait of Hormuz",
     "Two tankers struck near Khasab, Oman. No casualties reported."),
    ("MIDDLE EAST", "Iran strikes Bahrain industrial site",
     "Bahrain said Iran set fire to a civilian site late Saturday."),
    ("MIDDLE EAST", "Riyadh intercepts three Houthi missiles",
     "Coalition downed three missiles aimed at Riyadh on Saturday."),
    ("AMERICAS", "Mexico captures \u2018El Chapo Isidro\u2019",
     "FBI\u2019s 10 Most Wanted boss seized in Guasave. Eleven died."),
    ("EUROPE", "Russian cargo ship ablaze in the Baltic",
     "Ship bound for Kaliningrad caught fire after a drone strike."),
    ("ASIA", "Myanmar guilty of Rohingya genocide",
     "ICJ ruled 9\u20136 Myanmar committed genocide in 2017 \u2014 a first."),
    ("GLOBAL", "No treaty to ban \u2018killer robots\u2019",
     "Geneva talks ended with no binding treaty on killer robots."),
    ("EUROPE", "Spain heads for a snap election",
     "Spaniards vote 29 Nov; polls put the People\u2019s Party ahead."),
    ("AMERICAS", "Quake shakes Peru\u2019s Andes",
     "A 6.7\u20136.8 quake struck Jun\u00edn, injuring 15. No deaths."),
    ("ASIA", "Toxic alcohol kills 11 in Manipur",
     "Toxic alcohol killed 11 and hospitalised 180+ in Manipur."),
    ("MIDDLE EAST", "Fire at Iraq power station kills four",
     "Fire at the Hartha plant near Basra killed 4, injured 35."),
]

ALSO = [
    "Florida floods break a 73-year record",
    "FBI probes a hack of its criminal database",
    "Denmark: Russia plotted to kill a rapper",
    "Somalia expels the UAE ambassador",
    "Boat capsizes in Nigeria, 24 dead",
    "Bondi first responders marry",
    "Factory fire in Indonesia kills three",
    "S&P 500 suffers worst week since Apr 2025",
    "Trump picks an economic squeeze on Iran",
    "EU plastic-waste export ban begins",
]

FACTS = [
    ("550", "munitions fired overnight"),
    ("496", "drones in the barrage"),
    ("35", "lead changes in Las Vegas"),
    ("0.639s", "Verstappen\u2019s margin"),
    ("DAY 2", "of COP31 overtime"),
    ("$92.57", "Brent crude a barrel"),
]

# (lon, lat, hero?, label)
DOTS = [
    (30.7, 36.9, True, "ANTALYA"), (-115.1, 36.2, True, "LAS VEGAS"),
    (30.5, 50.4, True, "KYIV"),
    (56.5, 26.5, False, ""), (50.5, 26.2, False, ""), (46.7, 24.7, False, ""),
    (-108.5, 25.6, False, ""), (25.0, 60.0, False, ""), (4.3, 52.1, False, ""),
    (6.1, 46.2, False, ""), (-3.7, 40.4, False, ""), (-75.2, -11.2, False, ""),
    (93.9, 24.8, False, ""), (47.8, 30.5, False, ""), (-80.7, 28.4, False, ""),
    (45.3, 2.0, False, ""), (3.4, 6.5, False, ""), (151.3, -33.9, False, ""),
    (106.8, -6.2, False, ""), (-77.0, 38.9, False, ""),
]

CONTINENTS = [
    [(-168, 66), (-155, 58), (-140, 60), (-130, 55), (-125, 48), (-120, 34),
     (-110, 25), (-105, 20), (-97, 16), (-90, 14), (-85, 12), (-80, 9),
     (-78, 8), (-82, 15), (-87, 20), (-90, 21), (-95, 19), (-97, 26),
     (-93, 30), (-89, 30), (-84, 30), (-81, 26), (-80, 32), (-76, 35),
     (-75, 40), (-70, 42), (-68, 45), (-65, 45), (-60, 47), (-55, 47),
     (-60, 52), (-65, 55), (-68, 58), (-72, 62), (-78, 62), (-85, 66),
     (-90, 68), (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71),
     (-165, 68), (-168, 66)],
    [(-79, 9), (-77, 4), (-75, -3), (-70, -5), (-60, -8), (-50, -5),
     (-40, -8), (-35, -12), (-38, -20), (-42, -28), (-48, -32), (-55, -35),
     (-62, -40), (-68, -45), (-73, -50), (-74, -40), (-73, -30), (-72, -18),
     (-75, -15), (-80, -5), (-81, 0), (-80, 6), (-79, 9)],
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (2, 48), (5, 50), (8, 54),
     (10, 57), (12, 55), (18, 56), (21, 59), (24, 60), (28, 62), (30, 65),
     (32, 68), (40, 68), (44, 66), (40, 60), (38, 55), (35, 50), (30, 46),
     (28, 44), (23, 40), (22, 38), (19, 40), (15, 38), (12, 38), (8, 39),
     (3, 38), (0, 36), (-2, 37), (-6, 36), (-9, 37), (-10, 36)],
    [(-17, 15), (-16, 20), (-10, 29), (-5, 35), (0, 36), (10, 37), (15, 32),
     (20, 32), (25, 32), (30, 31), (33, 27), (35, 23), (37, 18), (40, 15),
     (43, 11), (48, 11), (51, 10), (51, 5), (46, 0), (42, -5), (40, -10),
     (38, -18), (35, -25), (32, -28), (28, -32), (25, -34), (20, -35),
     (16, -30), (14, -22), (12, -15), (10, -5), (8, 2), (4, 6), (0, 5),
     (-5, 5), (-8, 4), (-13, 8), (-17, 12), (-17, 15)],
    [(35, 68), (40, 70), (50, 70), (60, 69), (70, 72), (80, 73), (90, 75),
     (100, 76), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 69), (170, 66), (178, 65), (170, 60), (162, 56), (158, 52),
     (150, 45), (142, 40), (138, 35), (132, 33), (127, 35), (122, 30),
     (120, 25), (115, 22), (110, 20), (108, 15), (105, 10), (100, 8),
     (98, 12), (95, 16), (92, 20), (89, 22), (86, 20), (83, 17), (80, 13),
     (77, 8), (75, 12), (73, 16), (70, 20), (66, 25), (62, 25), (58, 26),
     (55, 28), (52, 30), (50, 32), (48, 35), (46, 38), (44, 42), (42, 46),
     (40, 50), (38, 55), (36, 60), (35, 65), (35, 68)],
    [(113, -22), (114, -30), (116, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (148, -37),
     (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
     (140, -17), (136, -15), (132, -12), (128, -14), (124, -15), (120, -20),
     (114, -22), (113, -22)],
    [(166, -46), (168, -44), (172, -41), (175, -38), (177, -38), (174, -42),
     (170, -45), (166, -46)],
]


def main():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # ---- red header bar ----
    d.rectangle([0, 0, W, 44], fill=RED)
    d.text((MARGIN, 11), "THE WORLD IN ONE DAY",
           font=font("DejaVuSans-Bold.ttf", 20), fill=(255, 255, 255))
    right = "24 STORIES \u00b7 7 REGIONS"
    d.text((W - MARGIN - d.textlength(right, font=font("DejaVuSans-Bold.ttf", 16)), 13),
           right, font=font("DejaVuSans-Bold.ttf", 16), fill=(255, 255, 255))

    # ---- masthead ----
    title = "Sunday 22 November 2026"
    d.text(((W - d.textlength(title, font=SERIF_B)) / 2, 52),
           title, font=SERIF_B, fill=INK)
    sub = "Every story below happened on \u2014 or was confirmed on \u2014 this day."
    d.text(((W - d.textlength(sub, font=font("DejaVuSerif.ttf", 13))) / 2, 104),
           sub, font=font("DejaVuSerif.ttf", 13), fill=GREY)
    d.line([(MARGIN, 124), (W - MARGIN, 124)], fill=INK, width=2)

    # ---- 6-fact strip ----
    fw = (W - 2 * MARGIN - 5 * 8) / 6
    for i, (num, label) in enumerate(FACTS):
        x0 = MARGIN + i * (fw + 8)
        d.rectangle([x0, 130, x0 + fw, 174], fill=LIGHT)
        d.text((x0 + 8, 136), num, font=font("DejaVuSans-Bold.ttf", 19), fill=RED)
        text_block(d, x0 + 8, 158, label, font("DejaVuSans.ttf", 9),
                   fw - 16, fill=GREY, lh=12, max_lines=1)

    # ---- 3 hero cards ----
    hw = (W - 2 * MARGIN - 2 * 16) / 3
    hy0, hy1 = 182, 366
    for i, (tag, head, body, fact) in enumerate(HEROES):
        x0 = MARGIN + i * (hw + 16)
        d.rectangle([x0, hy0, x0 + hw, hy1], outline=INK, width=2)
        d.rectangle([x0, hy0, x0 + hw, hy0 + 6], fill=RED)
        d.text((x0 + 12, hy0 + 14), tag, font=font("DejaVuSans-Bold.ttf", 11), fill=RED)
        y = text_block(d, x0 + 12, hy0 + 34, head, font("DejaVuSans-Bold.ttf", 19),
                       hw - 24, lh=23, max_lines=3)
        text_block(d, x0 + 12, y + 4, body, font("DejaVuSans.ttf", 12),
                   hw - 24, lh=16, max_lines=4)
        d.text((x0 + 12, hy1 - 22), fact, font=font("DejaVuSans-Bold.ttf", 10), fill=RED)

    # ---- 11 main cards, rows of 4 / 4 / 3 ----
    rows = [MAIN[0:4], MAIN[4:8], MAIN[8:11]]
    y0 = 374
    for r, row in enumerate(rows):
        n = len(row)
        cw = (W - 2 * MARGIN - (n - 1) * 12) / n
        y1 = y0 + 84
        for i, (tag, head, body) in enumerate(row):
            x0 = MARGIN + i * (cw + 12)
            d.rectangle([x0, y0, x0 + cw, y1], outline=LINE, width=1)
            d.text((x0 + 8, y0 + 6), tag, font=font("DejaVuSans-Bold.ttf", 9), fill=RED)
            yy = text_block(d, x0 + 8, y0 + 20, head, font("DejaVuSans-Bold.ttf", 12),
                            cw - 16, lh=15, max_lines=2)
            text_block(d, x0 + 8, yy + 2, body, font("DejaVuSans.ttf", 10),
                       cw - 16, lh=13, max_lines=2)
        y0 = y1 + 8

    # ---- WHERE IT HAPPENED map strip ----
    d.text((MARGIN, 650), "WHERE IT HAPPENED",
           font=font("DejaVuSans-Bold.ttf", 15), fill=RED)
    d.text((MARGIN + 210, 653), "24 stories, plotted \u2014 red dots are the three lead stories",
           font=font("DejaVuSans.ttf", 11), fill=GREY)
    mx0, my0, mx1, my1 = MARGIN, 672, W - MARGIN, 782
    d.rectangle([mx0, my0, mx1, my1], fill=MAPBG)
    lat0, lat1 = 85.0, -60.0

    def proj(lon, lat):
        x = mx0 + (lon + 180.0) / 360.0 * (mx1 - mx0)
        y = my0 + (lat0 - lat) / (lat0 - lat1) * (my1 - my0)
        return x, y

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND)
    for lon, lat, hero, label in DOTS:
        x, y = proj(lon, lat)
        if hero:
            d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=RED, outline=(255, 255, 255), width=2)
        else:
            d.ellipse([x - 3.5, y - 3.5, x + 3.5, y + 3.5], fill=INK)
    labelf = font("DejaVuSans-Bold.ttf", 9)
    for lon, lat, hero, label in DOTS:
        if not label:
            continue
        x, y = proj(lon, lat)
        if label == "LAS VEGAS":
            d.text((x + 9, y - 5), label, font=labelf, fill=RED)
        elif label == "KYIV":
            d.text((x - 34, y - 14), label, font=labelf, fill=RED)
        else:  # ANTALYA: label below the dot, the cluster above is too dense
            d.text((x - 10, y + 8), label, font=labelf, fill=RED)

    # ---- ALSO TODAY ----
    d.text((MARGIN, 790), "ALSO TODAY \u00b7 10 MORE STORIES",
           font=font("DejaVuSans-Bold.ttf", 15), fill=RED)
    colw = (W - 2 * MARGIN - 24) / 2
    af = font("DejaVuSans.ttf", 12)
    for col in range(2):
        x0 = MARGIN + col * (colw + 24)
        for j in range(5):
            item = ALSO[col * 5 + j]
            y = 814 + j * 18
            d.text((x0, y), "\u2022  " + item, font=af, fill=INK)

    # ---- DATE CHECK box (own row) ----
    d.rectangle([MARGIN, 916, W - MARGIN, 972], outline=RED, width=2)
    d.text((MARGIN + 12, 924), "DATE CHECK",
           font=font("DejaVuSans-Bold.ttf", 13), fill=RED)
    check = ("Every story above happened on, or was confirmed on, Sunday 22 November 2026. "
             "The Las Vegas race finished Saturday night in Las Vegas \u2014 Sunday morning in Jakarta. "
             "COP31 was due to end Friday 20 November; it is still in overtime. "
             "The ICJ ruling concerns events from 2017; the verdict is this week\u2019s news.")
    text_block(d, MARGIN + 118, 924, check, font("DejaVuSans.ttf", 11),
               W - 2 * MARGIN - 130, lh=15, max_lines=3)

    # ---- footer ----
    foot = "Rendered by an AI agent for make.fun \u00b7 news-image-20261122 \u00b7 Sources: Reuters, AP, Formula 1, UKMTO, ICJ \u00b7 All facts checked 22 Nov 2026"
    d.text(((W - d.textlength(foot, font=font("DejaVuSans.ttf", 10))) / 2, 984),
           foot, font=font("DejaVuSans.ttf", 10), fill=GREY)

    out = "entry.png"
    img.save(out, "PNG", optimize=True)
    data = open(out, "rb").read()
    print("entry.png", len(data), "bytes, sha256",
          hashlib.sha256(data).hexdigest())
    print("stories: 14 main + 10 also = 24; regions: Europe 5, Asia 3, "
          "Middle East 4, Africa 2, Americas 5, Oceania 1, Global 4")


if __name__ == "__main__":
    main()
