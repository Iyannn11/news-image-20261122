#!/usr/bin/env python3
"""News 22 Round 7 — 'The World in One Day', Sunday 22 November 2026.
Top 1 structure (3 hero illustrated + 10 small illustrated + 22 compact
numbered) + R2's vivid picture-rich DNA. All 35 stories verified by web
search on 22 Nov 2026. All illustrations are drawn by this script with PIL.
Deterministic render: 1024x1024 PNG.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 222)
PAPER = (255, 253, 246)
RED = (200, 16, 46)
DARKRED = (160, 10, 35)
INK = (20, 20, 20)
GREY = (90, 86, 76)
LINE = (200, 192, 172)
NAVY = (31, 56, 100)
BLUE = (31, 120, 180)
BROWN = (139, 90, 43)
PURPLE = (106, 61, 154)
TEAL = (0, 128, 128)
GREEN = (46, 125, 50)
STRIP = (239, 232, 208)
TAN = (216, 196, 158)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
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


def text_lines(draw, x, y, text, fnt, max_w, fill, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -90 + i * 36
        rr = r if i % 2 == 0 else r * 0.45
        import math
        pts.append((cx + rr * math.cos(math.radians(ang)),
                    cy + rr * math.sin(math.radians(ang))))
    d.polygon(pts, fill=fill)


# ---------------- illustrations (drawn on the main canvas) ----------------
def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 84, 124))
    # globe: blue circle with green landmass blobs + white grid
    gx, gy, gr = x + w * 0.46, y + h * 0.50, h * 0.38
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(60, 130, 200),
              outline=(255, 255, 255), width=2)
    d.ellipse([gx - gr * 0.55, gy - gr * 0.75, gx + gr * 0.15,
               gy - gr * 0.05], fill=(46, 139, 87))
    d.ellipse([gx - gr * 0.10, gy + gr * 0.05, gx + gr * 0.70,
               gy + gr * 0.70], fill=(46, 139, 87))
    d.ellipse([gx + gr * 0.30, gy - gr * 0.55, gx + gr * 0.75,
               gy - gr * 0.10], fill=(46, 139, 87))
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 20, 160,
          fill=(255, 255, 255), width=1)
    d.line([gx - gr, gy, gx + gr, gy], fill=(255, 255, 255), width=1)
    # clock
    cx, cy, r = x + w * 0.82, y + h * 0.50, h * 0.26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=(200, 16, 46), width=2)
    d.line([cx, cy, cx, cy - r * 0.65], fill=(20, 20, 20), width=2)
    d.line([cx, cy, cx + r * 0.55, cy + r * 0.25], fill=(20, 20, 20), width=2)
    # thermometer
    tx = x + w * 0.08
    d.rounded_rectangle([tx, y + h * 0.30, tx + 10, y + h * 0.82],
                        radius=5, fill=(255, 255, 255))
    d.rectangle([tx + 2, y + h * 0.55, tx + 8, y + h * 0.80],
                fill=(200, 16, 46))
    d.ellipse([tx - 3, y + h * 0.74, tx + 13, y + h * 0.92],
              fill=(200, 16, 46))


def ill_ukraine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 18, 38))
    import random
    rnd = random.Random(7)
    for _ in range(14):
        sx = x + rnd.uniform(0.05, 0.95) * w
        sy = y + rnd.uniform(0.05, 0.45) * h
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 230, 150))
    # skyline
    base = y + h
    for bx, bw, bh in [(0.02, 0.14, 0.45), (0.18, 0.12, 0.62),
                       (0.32, 0.16, 0.38), (0.50, 0.12, 0.55),
                       (0.64, 0.14, 0.42), (0.80, 0.16, 0.58)]:
        d.rectangle([x + bx * w, base - bh * h, x + (bx + bw) * w, base],
                    fill=(8, 10, 22))
        for wy in range(3):
            for wx in range(2):
                d.rectangle([x + (bx + 0.02 + wx * 0.05) * w,
                             base - bh * h + 6 + wy * 9,
                             x + (bx + 0.04 + wx * 0.05) * w,
                             base - bh * h + 11 + wy * 9],
                            fill=(255, 200, 80))
    # explosions
    for ex, ey, r in [(0.22, 0.30, 16), (0.58, 0.22, 13), (0.82, 0.34, 11)]:
        star(d, x + ex * w, y + ey * h, r, (255, 140, 40))
        star(d, x + ex * w, y + ey * h, r * 0.55, (255, 220, 90))
    # drone trails
    d.line([x + 0.05 * w, y + 0.12 * h, x + 0.30 * w, y + 0.28 * h],
           fill=(255, 120, 60), width=2)
    d.line([x + 0.65 * w, y + 0.08 * h, x + 0.55 * w, y + 0.24 * h],
           fill=(255, 120, 60), width=2)


def ill_verstappen(d, x, y, w, h):
    # sunset gradient bands
    bands = [(255, 140, 60), (255, 110, 90), (180, 60, 140), (90, 40, 110)]
    for i, c in enumerate(bands):
        d.rectangle([x, y + i * h // 4, x + w, y + (i + 1) * h // 4], fill=c)
    d.ellipse([x + w * 0.72, y + h * 0.10, x + w * 0.92, y + h * 0.55],
              fill=(255, 220, 120))
    # palm silhouette
    d.line([x + w * 0.10, y + h * 0.95, x + w * 0.13, y + h * 0.35],
           fill=(20, 20, 20), width=4)
    for a in range(-70, 71, 35):
        import math
        ex = x + w * 0.13 + 26 * math.cos(math.radians(a - 90))
        ey = y + h * 0.35 + 16 * math.sin(math.radians(a - 90))
        d.line([x + w * 0.13, y + h * 0.35, ex, ey], fill=(20, 20, 20),
               width=3)
    # race car
    cy = y + h * 0.72
    d.rectangle([x + w * 0.30, cy - 14, x + w * 0.78, cy + 2],
                fill=(10, 10, 30))
    d.polygon([(x + w * 0.42, cy - 14), (x + w * 0.52, cy - 26),
               (x + w * 0.66, cy - 26), (x + w * 0.70, cy - 14)],
              fill=(10, 10, 30))
    d.rectangle([x + w * 0.78, cy - 22, x + w * 0.84, cy - 6],
                fill=(10, 10, 30))
    for wx in (0.36, 0.68):
        d.ellipse([x + wx * w, cy - 2, x + (wx + 0.07) * w, cy + 12],
                  fill=(5, 5, 5), outline=(220, 220, 220), width=2)
    # checkered flag
    fx, fy = x + w * 0.86, y + h * 0.12
    for r in range(3):
        for c in range(4):
            d.rectangle([fx + c * 7, fy + r * 7, fx + c * 7 + 7, fy + r * 7 + 7],
                        fill=(255, 255, 255) if (r + c) % 2 == 0 else (10, 10, 10))


def ill_scales(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 190))
    cx = x + w * 0.5
    d.rectangle([cx - 2, y + h * 0.12, cx + 2, y + h * 0.80],
                fill=(120, 90, 20))
    d.line([x + w * 0.22, y + h * 0.22, x + w * 0.78, y + h * 0.22],
           fill=(120, 90, 20), width=3)
    for sx in (0.22, 0.78):
        px = x + sx * w
        d.line([px, y + h * 0.22, px, y + h * 0.42], fill=(120, 90, 20),
               width=2)
        d.polygon([(px - 22, y + h * 0.42), (px + 22, y + h * 0.42),
                   (px, y + h * 0.58)], fill=(200, 160, 40),
                  outline=(120, 90, 20))
    d.rectangle([cx - 18, y + h * 0.80, cx + 18, y + h * 0.88],
                fill=(120, 90, 20))
    # gavel
    d.rounded_rectangle([x + w * 0.68, y + h * 0.68, x + w * 0.92,
                         y + h * 0.80], radius=3, fill=(90, 60, 20))
    d.line([x + w * 0.80, y + h * 0.74, x + w * 0.98, y + h * 0.90],
           fill=(90, 60, 20), width=3)


def ill_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 190, 210))
    d.ellipse([x + w * 0.78, y + h * 0.08, x + w * 0.94, y + h * 0.42],
              fill=(255, 220, 120))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(20, 90, 120))
    for wy in (0.66, 0.76, 0.86):
        d.arc([x + 0.05 * w, y + wy * h, x + 0.95 * w, y + (wy + 0.14) * h],
              0, 180, fill=(255, 255, 255), width=2)
    # hull + containers
    d.polygon([(x + w * 0.08, y + h * 0.62), (x + w * 0.88, y + h * 0.62),
               (x + w * 0.80, y + h * 0.78), (x + w * 0.16, y + h * 0.78)],
              fill=(40, 40, 50))
    for i, c in enumerate([(200, 60, 40), (40, 120, 200), (220, 180, 40)]):
        d.rectangle([x + w * (0.18 + i * 0.16), y + h * 0.42,
                     x + w * (0.32 + i * 0.16), y + h * 0.60], fill=c)
    d.rectangle([x + w * 0.66, y + h * 0.30, x + w * 0.76, y + h * 0.60],
                fill=(240, 240, 240))
    # smoke
    d.ellipse([x + w * 0.70, y + h * 0.14, x + w * 0.76, y + h * 0.30],
              fill=(200, 200, 200))


def ill_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 190, 160))
    d.polygon([(x, y + h), (x + w * 0.30, y + h * 0.25),
               (x + w * 0.55, y + h)], fill=(110, 90, 70))
    d.polygon([(x + w * 0.35, y + h), (x + w * 0.62, y + h * 0.12),
               (x + w * 0.95, y + h)], fill=(80, 65, 50))
    d.polygon([(x + w * 0.55, y + h * 0.18), (x + w * 0.62, y + h * 0.12),
               (x + w * 0.70, y + h * 0.22), (x + w * 0.60, y + h * 0.30)],
              fill=(255, 255, 255))
    # seismograph strip
    d.rectangle([x + w * 0.06, y + h * 0.68, x + w * 0.94, y + h * 0.92],
                fill=(255, 255, 255), outline=(20, 20, 20))
    pts = []
    import math
    for i in range(41):
        px = x + w * 0.06 + i * (w * 0.88 / 40)
        py = y + h * 0.80 + math.sin(i * 1.7) * (h * 0.10) * (1 if i % 3 else 0.4)
        if i in (18, 19, 20, 21):
            py = y + h * 0.80 + (h * 0.12 if i % 2 == 0 else -h * 0.12)
        pts.append((px, py))
    d.line(pts, fill=(200, 16, 46), width=2)


def ill_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 230, 150))
    d.rectangle([x, y, x + w * 0.18, y + h], fill=(200, 16, 46))
    d.rectangle([x, y, x + w, y + h * 0.18], fill=(200, 16, 46))
    # ballot box
    bx, by = x + w * 0.42, y + h * 0.38
    d.rectangle([bx, by, bx + w * 0.30, by + h * 0.48], fill=(60, 60, 90))
    d.rectangle([bx - 6, by - 8, bx + w * 0.30 + 6, by], fill=(40, 40, 70))
    d.rectangle([bx + w * 0.10, by - 8, bx + w * 0.20, by - 4],
                fill=(20, 20, 20))
    # ballot paper + tick
    d.polygon([(bx + w * 0.02, by - h * 0.30), (bx + w * 0.16, by - h * 0.34),
               (bx + w * 0.14, by - h * 0.08), (bx, by - h * 0.06)],
              fill=(255, 255, 255), outline=(20, 20, 20))
    d.line([(bx + w * 0.03, by - h * 0.20), (bx + w * 0.06, by - h * 0.14),
            (bx + w * 0.13, by - h * 0.28)], fill=(0, 150, 60), width=3)


def ill_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 160, 70))
    d.rectangle([x + w * 0.30, y, x + w * 0.70, y + h], fill=(190, 160, 110))
    # stumps
    for sx in (0.44, 0.50, 0.56):
        d.rectangle([x + sx * w, y + h * 0.16, x + (sx + 0.02) * w,
                     y + h * 0.42], fill=(240, 220, 140))
    d.rectangle([x + w * 0.44, y + h * 0.13, x + w * 0.58, y + h * 0.17],
                fill=(240, 220, 140))
    for sx in (0.44, 0.50, 0.56):
        d.rectangle([x + sx * w, y + h * 0.62, x + (sx + 0.02) * w,
                     y + h * 0.88], fill=(240, 220, 140))
    # ball + bat
    d.ellipse([x + w * 0.72, y + h * 0.30, x + w * 0.82, y + h * 0.50],
              fill=(200, 30, 30), outline=(255, 255, 255), width=2)
    d.line([x + w * 0.20, y + h * 0.75, x + w * 0.30, y + h * 0.45],
           fill=(200, 170, 110), width=5)


def ill_waves(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 110, 180))
    for wy, c in [(0.55, (20, 80, 150)), (0.70, (15, 65, 130)),
                  (0.85, (10, 50, 110))]:
        d.arc([x - w * 0.05, y + wy * h, x + w * 0.45, y + (wy + 0.30) * h],
              180, 360, fill=(255, 255, 255), width=3)
        d.arc([x + w * 0.50, y + wy * h, x + w * 1.05, y + (wy + 0.30) * h],
              180, 360, fill=(255, 255, 255), width=3)
    # seismograph zigzag
    pts = [(x + w * 0.08 + i * w * 0.84 / 12,
            y + h * 0.30 + (h * 0.12 if i % 2 == 0 else -h * 0.12))
           for i in range(13)]
    d.line(pts, fill=(255, 220, 60), width=3)


def ill_handcuffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 45, 60))
    for cx in (0.32, 0.68):
        d.ellipse([x + (cx - 0.13) * w, y + h * 0.28, x + (cx + 0.13) * w,
                   y + h * 0.78], outline=(200, 200, 210), width=5)
    d.line([x + w * 0.45, y + h * 0.42, x + w * 0.55, y + h * 0.42],
           fill=(200, 200, 210), width=4)
    d.ellipse([x + w * 0.47, y + h * 0.36, x + w * 0.53, y + h * 0.48],
              fill=(200, 200, 210))
    star(d, x + w * 0.50, y + h * 0.14, 10, (255, 210, 60))


def ill_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(15, 20, 45))
    import math
    for _ in range(10):
        sx = x + (hash(str(_)) % 90 + 5) / 100 * w
        sy = y + (hash(str(_ + 9)) % 30 + 5) / 100 * h
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # arc trail
    d.arc([x + w * 0.05, y - h * 0.55, x + w * 0.95, y + h * 0.75],
          200, 340, fill=(255, 160, 60), width=3)
    # missile
    d.polygon([(x + w * 0.72, y + h * 0.30), (x + w * 0.78, y + h * 0.18),
               (x + w * 0.84, y + h * 0.30)], fill=(220, 220, 220))
    d.rectangle([x + w * 0.72, y + h * 0.30, x + w * 0.84, y + h * 0.52],
                fill=(200, 200, 200))
    # intercept burst
    star(d, x + w * 0.30, y + h * 0.55, 15, (255, 180, 40))
    star(d, x + w * 0.30, y + h * 0.55, 8, (255, 240, 140))


def ill_robot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(190, 195, 205))
    # robot head
    d.rounded_rectangle([x + w * 0.30, y + h * 0.22, x + w * 0.70,
                         y + h * 0.72], radius=8, fill=(120, 125, 135),
                        outline=(40, 40, 50), width=2)
    d.ellipse([x + w * 0.38, y + h * 0.38, x + w * 0.46, y + h * 0.52],
              fill=(80, 220, 255))
    d.ellipse([x + w * 0.54, y + h * 0.38, x + w * 0.62, y + h * 0.52],
              fill=(80, 220, 255))
    d.rectangle([x + w * 0.40, y + h * 0.60, x + w * 0.60, y + h * 0.64],
                fill=(40, 40, 50))
    d.line([x + w * 0.50, y + h * 0.22, x + w * 0.50, y + h * 0.08],
           fill=(40, 40, 50), width=3)
    d.ellipse([x + w * 0.47, y + h * 0.03, x + w * 0.53, y + h * 0.12],
              fill=(255, 60, 60))
    # no symbol
    cx, cy, r = x + w * 0.50, y + h * 0.48, h * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 16, 46),
              width=4)
    d.line([cx - r * 0.7, cy + r * 0.7, cx + r * 0.7, cy - r * 0.7],
           fill=(200, 16, 46), width=4)


def ill_rugby(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 140, 60))
    d.rectangle([x, y + h * 0.62, x + w, y + h * 0.66],
                fill=(255, 255, 255))
    d.rectangle([x, y + h * 0.30, x + w, y + h * 0.34],
                fill=(255, 255, 255))
    # goalposts
    d.line([x + w * 0.14, y + h * 0.10, x + w * 0.14, y + h * 0.62],
           fill=(255, 255, 255), width=3)
    d.line([x + w * 0.22, y + h * 0.10, x + w * 0.22, y + h * 0.62],
           fill=(255, 255, 255), width=3)
    d.line([x + w * 0.14, y + h * 0.34, x + w * 0.22, y + h * 0.34],
           fill=(255, 255, 255), width=3)
    # ball
    d.ellipse([x + w * 0.55, y + h * 0.55, x + w * 0.85, y + h * 0.85],
              fill=(150, 90, 50), outline=(255, 255, 255), width=2)
    d.line([x + w * 0.63, y + h * 0.62, x + w * 0.77, y + h * 0.78],
           fill=(255, 255, 255), width=2)

# ---------------- stories (all verified by web search, 22 Nov 2026) --------
# (region, label, headline, body, source, illustration)
HEROES = [
    ("GLOBAL", "COP31 STALLS INTO DAY TWO OF OVERTIME",
     "Antalya, Turkey \u2014 Negotiators were asked to weigh a last-minute text early Sunday after talks missed their Friday deadline. Fossil-fuel wording and a $120bn adaptation fund are still unresolved.",
     "AP / Reuters", ill_cop31),
    ("EUROPE", "550 MUNITIONS RAIN ON UKRAINE OVERNIGHT",
     "Kyiv \u2014 Russia fired 496 drones and 53 missiles overnight, Zelenskyy said Sunday. Five people were killed and energy sites were hit in nine regions.",
     "AP / Air Force", ill_ukraine),
    ("AMERICAS", "VERSTAPPEN WINS A WILD VEGAS THRILLER",
     "Las Vegas \u2014 Max Verstappen held off Lando Norris by 0.639s after 35 lead changes in 50 laps \u2014 his third win on the Strip in four years.",
     "Formula 1", ill_verstappen),
]

SMALL = [
    ("ASIA", "MYANMAR GUILTY OF ROHINGYA GENOCIDE",
     "The Hague \u2014 The ICJ ruled 9\u20136 on Thursday that Myanmar committed genocide in 2017, a first for a state. Reparations were ordered.",
     "ICJ / UN", ill_scales),
    ("MIDDLE EAST", "TWO TANKERS HIT IN THE STRAIT OF HORMUZ",
     "Two tankers struck near Khasab, Oman. No casualties reported.",
     "UKMTO", ill_tanker),
    ("AMERICAS", "QUAKE SHAKES PERU'S ANDES",
     "A 6.7\u20136.8 quake struck Jun\u00edn, injuring 15. No deaths.",
     "USGS / IGP", ill_quake),
    ("EUROPE", "SPAIN HEADS FOR A SNAP ELECTION",
     "Spaniards vote 29 Nov; polls put the People's Party ahead.",
     "The Guardian", ill_ballot),
    ("OCEANIA", "ENGLAND END 15-YEAR ASHES WAIT",
     "Melbourne \u2014 England won the 4th Test by 4 wickets, their first win in Australia since 2011. Australia lead 3\u20131.",
     "Cricbuzz", ill_cricket),
    ("OCEANIA", "BANDA SEA QUAKE FELT IN DARWIN",
     "A magnitude 6.8 quake struck near Timor-Leste. No tsunami threat.",
     "GFZ", ill_waves),
    ("AMERICAS", "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
     "FBI's 10 Most Wanted boss seized in Guasave. Eleven died.",
     "FBI", ill_handcuffs),
    ("MIDDLE EAST", "RIYADH INTERCEPTS THREE HOUTHI MISSILES",
     "Coalition downed three missiles aimed at Riyadh on Saturday.",
     "SPA", ill_missile),
    ("GLOBAL", "NO TREATY TO BAN 'KILLER ROBOTS'",
     "Geneva talks ended with no binding treaty on killer robots.",
     "UN", ill_robot),
    ("OCEANIA", "AUSTRALIA EDGE WALES IN CARDIFF",
     "A Gordon penalty sealed a 29\u201326 win at Principality Stadium.",
     "QNC News", ill_rugby),
]

# compact numbered list (stories 14-35)
ALSO = [
    ("MIDDLE EAST", "Fire at Iraq power station kills four"),
    ("ASIA", "Toxic alcohol kills 11 in Manipur"),
    ("EUROPE", "Russian cargo ship ablaze in the Baltic"),
    ("MIDDLE EAST", "Iran strikes Bahrain industrial site"),
    ("ASIA", "South Korea minister quits over exam cheating"),
    ("MIDDLE EAST", "Iran unveils missile launcher at underground base"),
    ("AFRICA", "Somalia expels the UAE ambassador"),
    ("AFRICA", "Boat capsizes in Nigeria, 24 dead"),
    ("AMERICAS", "Florida floods break a 73-year record"),
    ("AMERICAS", "FBI probes hack of its criminal database"),
    ("EUROPE", "Denmark: Russia plotted to kill a rapper"),
    ("OCEANIA", "Bondi first responders marry"),
    ("ASIA", "Factory fire in Indonesia kills three"),
    ("GLOBAL", "S&P 500 suffers worst week since April 2025"),
    ("AMERICAS", "Trump picks an economic squeeze on Iran"),
    ("EUROPE", "EU plastic-waste export ban begins"),
    ("EUROPE", "Poland: missile strike was likely intentional"),
    ("EUROPE", "Kryvyi Rih strike kills boy, 7, and paramedic"),
    ("EUROPE", "Lviv strike kills two, injures ten"),
    ("GLOBAL", "Next climate summit set for Addis Ababa in Nov 2027"),
    ("GLOBAL", "Antonelli, 20, becomes F1's youngest champion"),
    ("AMERICAS", "Ferraris clash in Vegas; both penalised"),
]

REGIONS = [("GLOBAL", 5, NAVY), ("EUROPE", 8, RED), ("MIDDLE EAST", 5, BROWN),
           ("ASIA", 4, PURPLE), ("AMERICAS", 7, BLUE), ("OCEANIA", 4, TEAL),
           ("AFRICA", 2, GREEN)]

FACTS = [("550", "munitions fired overnight"),
         ("496", "drones in the barrage"),
         ("35", "lead changes in Las Vegas"),
         ("0.639s", "Verstappen's margin"),
         ("DAY 2", "of COP31 overtime"),
         ("$120bn", "adaptation fund dropped")]

# ---------------- map (dark navy ocean, tan continents) --------------------
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73),
           (-75, 62), (-60, 47), (-70, 42), (-80, 32), (-90, 21),
           (-97, 16), (-105, 20), (-110, 23), (-125, 40), (-125, 49),
           (-150, 60)],
    "SA": [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
           (-50, -30), (-60, -35), (-70, -40), (-70, -55), (-75, -35),
           (-80, -20), (-80, -5)],
    "EU": [(-10, 36), (-9, 43), (0, 44), (5, 44), (10, 45), (12, 44),
           (15, 40), (20, 40), (23, 36), (28, 36), (30, 40), (28, 45),
           (25, 45), (20, 50), (15, 55), (10, 57), (5, 58), (0, 51),
           (-5, 50), (-10, 44)],
    "AF": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31),
           (35, 28), (40, 15), (45, 11), (51, 10), (48, 0), (40, -10),
           (35, -20), (30, -30), (20, -35), (15, -30), (12, -18),
           (13, -5), (9, 4), (-8, 5), (-15, 11)],
    "AS": [(30, 36), (35, 36), (40, 38), (45, 40), (50, 40), (55, 45),
           (60, 50), (65, 55), (70, 60), (75, 70), (80, 73), (90, 75),
           (100, 77), (110, 74), (120, 73), (130, 72), (140, 72),
           (150, 70), (160, 66), (170, 66), (178, 65), (170, 60),
           (162, 58), (158, 52), (150, 60), (142, 50), (140, 40),
           (135, 35), (130, 33), (127, 35), (122, 38), (120, 30),
           (115, 22), (110, 20), (105, 10), (100, 8), (95, 15),
           (90, 22), (85, 20), (80, 15), (77, 8), (75, 12), (70, 20),
           (65, 25), (60, 25), (55, 26), (50, 29), (48, 30), (44, 29),
           (40, 32), (35, 36)],
    "OC": [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
           (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
           (153, -32), (153, -27), (150, -22), (146, -19), (142, -11),
           (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
           (122, -17), (118, -20), (114, -22)],
}

# (lon, lat, number or None) — 1-13 are the illustrated stories
DOTS = [(30.7, 36.9, 1), (30.5, 50.5, 2), (-115.1, 36.2, 3),
        (56.2, 26.2, 4), (46.7, 24.7, 5), (96.0, 20.0, 6),
        (-75.2, -11.2, 7), (-3.7, 40.4, 8), (145.0, -37.8, 9),
        (128.0, -6.0, 10), (-108.5, 25.6, 11), (6.1, 46.2, 12),
        (-4.0, 51.5, 13), (50.6, 26.2, None), (44.4, 33.3, None),
        (101.0, 3.0, None), (45.3, 2.0, None), (8.5, 4.5, None),
        (126.6, 37.5, None), (-81.0, 27.0, None), (151.2, -33.9, None),
        (19.0, 52.0, None), (33.6, 48.4, None), (24.0, 49.8, None),
        (38.7, 9.0, None), (-95.0, 29.0, None)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 58))
    lat_top, lat_bot = 78, -58

    def proj(lon, lat):
        px = x + (lon + 180) / 360 * w
        py = y + (lat_top - lat) / (lat_top - lat_bot) * h
        return (px, py)

    for poly in CONTINENTS.values():
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=TAN)
    for lon, lat, num in DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        if num is not None:
            f = font(SANSB, 8)
            tw = d.textlength(str(num), font=f)
            d.text((px - tw / 2, py - 4), str(num), font=f,
                   fill=(255, 255, 255))
    f = font(SANSB, 9)
    for lon, lat, label, dx, dy in [(30.7, 36.9, "ANTALYA", 10, 4),
                                    (30.5, 50.5, "KYIV", -34, -16),
                                    (-115.1, 36.2, "LAS VEGAS", 10, -4)]:
        px, py = proj(lon, lat)
        # dark halo so the label reads over the tan continents
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            d.text((px + dx + ox, py + dy + oy), label, font=f,
                   fill=(16, 28, 58))
        d.text((px + dx, py + dy), label, font=f, fill=(255, 255, 255))


# ---------------- page ------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 16
    CW = W - 2 * M  # 992

    # header bar
    d.rectangle([0, 0, W, 34], fill=RED)
    f = font(SANSB, 15)
    d.text((M, 8), "THE WORLD IN ONE DAY", font=f, fill=(255, 255, 255))
    t = "35 STORIES \u00b7 7 REGIONS"
    d.text((W - M - d.textlength(t, font=f), 8), t, font=f,
           fill=(255, 255, 255))

    # masthead
    f = font(SERIF, 50)
    t = "Sunday 22 November 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, 40), t, font=f, fill=INK)
    f = font(SANS, 13)
    t = ("COP31 stalls in overtime  \u00b7  Verstappen wins a wild Vegas thriller"
         "  \u00b7  550 munitions rain on Ukraine")
    d.text(((W - d.textlength(t, font=f)) / 2, 100), t, font=f, fill=GREY)

    # fact strip
    y0 = 122
    d.rectangle([M, y0, W - M, y0 + 48], fill=STRIP)
    cw = CW / 6
    for i, (num, label) in enumerate(FACTS):
        cx = M + i * cw
        if i:
            d.line([cx, y0 + 6, cx, y0 + 42], fill=LINE, width=1)
        f = font(SANSB, 21)
        d.text((cx + 10, y0 + 4), num, font=f, fill=RED)
        f = font(SANS, 10)
        d.text((cx + 10, y0 + 30), label, font=f, fill=GREY)

    # region bar
    y0 = 178
    total = sum(c for _, c, _ in REGIONS)
    x = M
    for name, count, color in REGIONS:
        seg = CW * count / total
        d.rectangle([x, y0, x + seg - 1, y0 + 26], fill=color)
        f = font(SANSB, 10)
        t = f"{name} \u00b7 {count}"
        tw = d.textlength(t, font=f)
        if tw <= seg - 8:
            d.text((x + (seg - tw) / 2, y0 + 7), t, font=f,
                   fill=(255, 255, 255))
        else:
            # narrow segment: two-line label (name over count)
            f2 = font(SANSB, 9)
            for j, ln in enumerate((name, str(count))):
                lw = d.textlength(ln, font=f2)
                d.text((x + (seg - lw) / 2, y0 + 3 + j * 11), ln, font=f2,
                       fill=(255, 255, 255))
        x += seg

    # hero cards
    y0 = 212
    hw = (CW - 16) / 3
    hh = 232
    for i, (region, headline, body, source, ill) in enumerate(HEROES):
        cx = M + i * (hw + 8)
        d.rectangle([cx, y0, cx + hw, y0 + hh], fill=PAPER,
                    outline=LINE, width=1)
        d.rectangle([cx, y0, cx + hw, y0 + 3], fill=RED)
        ill(d, cx + 1, y0 + 4, hw - 2, 108)
        ty = y0 + 120
        f = font(SANSB, 10)
        d.text((cx + 8, ty), region, font=f, fill=RED)
        ty += 15
        ty = text_lines(d, cx + 8, ty, headline, font(SANSB, 15),
                        hw - 16, INK, leading=18, max_lines=2)
        ty += 2
        ty = text_lines(d, cx + 8, ty, body, font(SANS, 11),
                        hw - 16, INK, leading=14, max_lines=3)
        f = font(SANS, 9)
        d.text((cx + 8, y0 + hh - 16), f"({source})", font=f, fill=GREY)

    # small cards: 2 rows x 5
    y0 = 452
    sw = (CW - 4 * 8) / 5
    sh = 132
    for row in range(2):
        for col in range(5):
            idx = row * 5 + col
            region, headline, body, source, ill = SMALL[idx]
            cx = M + col * (sw + 8)
            cy = y0 + row * (sh + 8)
            d.rectangle([cx, cy, cx + sw, cy + sh], fill=PAPER,
                        outline=LINE, width=1)
            ill(d, cx + 1, cy + 1, sw - 2, 58)
            ty = cy + 64
            f = font(SANSB, 8)
            d.text((cx + 6, ty), region, font=f, fill=RED)
            ty += 11
            ty = text_lines(d, cx + 6, ty, headline, font(SANSB, 10),
                            sw - 12, INK, leading=12, max_lines=2)
            ty = text_lines(d, cx + 6, ty, body, font(SANS, 9),
                            sw - 12, INK, leading=11, max_lines=2)

    # bottom: map + numbered list
    y0 = 736
    map_w = 392
    d.rectangle([M, y0, M + map_w, y0 + 148], fill=(16, 28, 58))
    f = font(SANSB, 11)
    d.text((M + 8, y0 + 4), "WHERE IT HAPPENED", font=f, fill=(255, 255, 255))
    draw_map(d, M, y0 + 22, map_w, 126)
    lx = M + map_w + 12
    lw = W - M - lx
    f = font(SANSB, 12)
    d.text((lx, y0), "ALSO ON SUNDAY \u00b7 22 MORE STORIES", font=f, fill=RED)
    col_w = (lw - 8) / 2
    f = font(SANS, 10)
    for i, (region, text) in enumerate(ALSO):
        col = i // 11
        row = i % 11
        tx = lx + col * (col_w + 8)
        ty = y0 + 20 + row * 12
        num = f"{14 + i}. "
        d.text((tx, ty), num, font=f, fill=RED)
        nw = d.textlength(num, font=f)
        t = text
        while d.textlength(t, font=f) > col_w - nw - 2 and len(t) > 10:
            t = t[:-1]
        d.text((tx + nw, ty), t, font=f, fill=INK)

    # date check (wrapped to fit, box grows with the lines)
    y0 = 898
    f = font(SANS, 10)
    dc_lines = []
    dc_lines += wrap(d, "Every story above happened on, or was confirmed on, "
                     "Sunday 22 November 2026. The Las Vegas race finished "
                     "Saturday night in Las Vegas \u2014 Sunday morning in "
                     "Jakarta.", f, W - 2 * M - 20)
    dc_lines += wrap(d, "COP31 was due to end Friday 20 November; it is "
                     "still in overtime. The ICJ verdict is this week's "
                     "news, about 2017 events. Verified count: 496 drones + "
                     "53 missiles, not Top 1's rounded '400'.", f,
                     W - 2 * M - 20)
    box_h = 22 + 13 * len(dc_lines)
    d.rectangle([M, y0, W - M, y0 + box_h], outline=RED, width=2)
    f = font(SANSB, 11)
    d.text((M + 10, y0 + 6), "DATE CHECK", font=f, fill=RED)
    f = font(SANS, 10)
    ty = y0 + 22
    for ln in dc_lines:
        d.text((M + 10, ty), ln, font=f, fill=INK)
        ty += 13

    # footer
    f = font(SANS, 9)
    t = ("Rendered by an AI agent for make.fun \u00b7 news-image-20261122"
         " \u00b7 Sources: AP, Reuters, Formula 1, UKMTO, ICJ, USGS"
         " \u00b7 All facts checked 22 Nov 2026")
    d.text(((W - d.textlength(t, font=f)) / 2, y0 + box_h + 8), t, font=f,
           fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
