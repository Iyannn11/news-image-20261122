#!/usr/bin/env python3
"""Render the News 22 Nov 2026 broadsheet (1024x1024 PNG).

Top-1-style broadsheet, early edition: 11 verified stories, 6 regions.
Every story happened or was first reported on Sunday 22 November 2026.
Deterministic: same input -> same bytes (no timestamps, no randomness).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)
INK = (26, 26, 26)
RED = (185, 28, 28)
RED_DK = (153, 27, 27)
GREY = (90, 84, 74)
RULE = (60, 56, 48)
CARD_BG = (255, 252, 244)

FD = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    p = os.path.join(FD, name)
    if not os.path.exists(p):
        p = os.path.join(FD, "DejaVuSans.ttf")
    return ImageFont.truetype(p, size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_w(s, f):
    return d.textlength(s, font=f)

def wrap(s, f, maxw):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(t, f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(x, y, s, f, maxw, fill=INK, leading=None, align="left"):
    lh = leading or int(f.size * 1.28)
    yy = y
    for ln in wrap(s, f, maxw):
        if align == "center":
            d.text((x + (maxw - text_w(ln, f)) / 2, yy), ln, font=f, fill=fill)
        else:
            d.text((x, yy), ln, font=f, fill=fill)
        yy += lh
    return yy

def hline(y, x0=14, x1=1010, w=2, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)

def banner(x, y, w, text, size=19):
    """Red banner bar with white bold caps text."""
    h = size + 12
    d.rectangle([x, y, x + w, y + h], fill=RED)
    f = F_SANS_B(size)
    tw = text_w(text, f)
    d.text((x + (w - tw) / 2, y + 5), text, font=f, fill=(255, 255, 255))
    return h

def card(x, y, w, h, illo=None):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=(180, 172, 152), width=1)
    if illo:
        illo(x + 1, y + 1, w - 2)

def card_text(x, y, w, num, loc, headline, body, source, bottom, hl_size=20, body_size=12):
    """num/location line, headline, body, source — all in flow, never overlapping."""
    f_loc = F_SANS_B(11)
    d.text((x + 8, y), f"{num}  {loc}", font=f_loc, fill=RED)
    f_hl = F_SERIF_B(hl_size)
    yy = draw_wrapped(x + 8, y + 15, headline, f_hl, w - 16, leading=hl_size + 3)
    f_body = F_SERIF(body_size)
    yy = draw_wrapped(x + 8, yy + 3, body, f_body, w - 16, leading=body_size + 4)
    f_src = F_SANS(10)
    d.text((x + 8, yy + 3), source, font=f_src, fill=GREY)
    return yy

# ---------------------------------------------------------------- header
d.text((14, 8), "THE WORLD IN ONE DAY", font=F_SANS_B(15), fill=RED)
right = "11 STORIES \u00b7 6 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
d.text((1010 - text_w(right, F_SANS_B(11)), 11), right, font=F_SANS_B(11), fill=INK)
hline(30, w=2)

# ---------------------------------------------------------------- masthead
mast = "Sunday 22 November 2026"
f_mast = F_SERIF_B(62)
d.text(((W - text_w(mast, f_mast)) / 2, 36), mast, font=f_mast, fill=INK)
deck = "Russia\u2019s biggest night attack of the war \u00b7 COP31 still without a deal \u00b7 Australia wrap up the Ashes in two days"
f_deck = F_SERIF(17)
d.text(((W - text_w(deck, f_deck)) / 2, 108), deck, font=f_deck, fill=INK)
hline(132, w=1)
hline(135, w=2)

# ---------------------------------------------------------------- facts strip (6 facts, y 142-182)
facts = [
    ("550", "munitions in Russia\u2019s overnight attack on Ukraine"),
    ("5", "killed, 10 injured \u2014 a family of four died in Lviv"),
    ("856", "candidates for 723 Hong Kong election seats"),
    ("$60,073", "bitcoin holds above $60,000 after Friday\u2019s plunge"),
    ("123", "Travis Head\u2019s runs as Australia win the Ashes opener"),
    ("90mm", "rain forecast in France\u2019s Jura on Sunday"),
]
fw = (1010 - 14) / 6
for i, (num, cap) in enumerate(facts):
    x0 = 14 + i * fw
    d.text((x0 + 4, 142), num, font=F_SANS_B(24), fill=RED)
    draw_wrapped(x0 + 4, 170, cap, F_SANS(10), fw - 12, fill=GREY, leading=12)
    if i:
        d.line([(x0, 142), (x0, 196)], fill=(200, 192, 172), width=1)
hline(200, w=1)

# ---------------------------------------------------------------- region bars (y 204-222)
regions = [
    ("EUROPE 2", 2, (29, 78, 216)),
    ("ASIA 2", 2, (185, 28, 28)),
    ("MIDDLE EAST 3", 3, (146, 64, 14)),
    ("AMERICAS 1", 1, (109, 40, 217)),
    ("OCEANIA 1", 1, (15, 118, 110)),
    ("GLOBAL 2", 2, (51, 65, 85)),
]
total = sum(r[1] for r in regions)
bx = 14
for name, n, col in regions:
    seg = (1010 - 14) * n / total
    d.rectangle([bx, 204, bx + seg, 222], fill=col)
    f_rb = F_SANS_B(10)
    tw = text_w(name, f_rb)
    d.text((bx + (seg - tw) / 2, 207), name, font=f_rb, fill=(255, 255, 255))
    bx += seg
import math

# ---------------------------------------------------------------- illustrations
def illo_russia(x, y, w):
    h = 90
    d.rectangle([x, y, x + w, y + h], fill=(13, 20, 48))
    for sx, sy in [(0.08, 0.15), (0.2, 0.08), (0.35, 0.2), (0.5, 0.1), (0.65, 0.18), (0.8, 0.08), (0.92, 0.22)]:
        d.ellipse([x + sx * w - 1.5, y + sy * h - 1.5, x + sx * w + 1.5, y + sy * h + 1.5], fill=(255, 255, 255))
    for (x0f, y0f, x1f) in [(0.0, 0.55, 0.14), (0.14, 0.42, 0.28), (0.28, 0.6, 0.42), (0.42, 0.35, 0.56), (0.56, 0.58, 0.7), (0.7, 0.45, 0.84), (0.84, 0.62, 1.0)]:
        d.rectangle([x + x0f * w, y + y0f * h, x + x1f * w, y + 0.78 * h], fill=(8, 12, 30))
        for wx in range(3):
            for wy in range(2):
                d.rectangle([x + (x0f + 0.02 + wx * 0.04) * w, y + (y0f + 0.05 + wy * 0.12) * h,
                             x + (x0f + 0.035 + wx * 0.04) * w, y + (y0f + 0.1 + wy * 0.12) * h], fill=(255, 200, 80))
    d.rectangle([x, y + 0.78 * h, x + w, y + h], fill=(5, 8, 20))
    for (dx, dy) in [(0.3, 0.25), (0.62, 0.18), (0.8, 0.32)]:
        d.ellipse([x + dx * w - 3, y + dy * h - 3, x + dx * w + 3, y + dy * h + 3], fill=(200, 200, 200))
        d.line([(x + dx * w, y + dy * h), (x + (dx + 0.12) * w, y + (dy - 0.08) * h)], fill=(200, 200, 200), width=1)
    for (ex, ey, r) in [(0.48, 0.42, 14), (0.88, 0.5, 10)]:
        cx, cy = x + ex * w, y + ey * h
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))], fill=(255, 140, 0), width=3)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 220, 100))

def illo_cop31(x, y, w):
    h = 90
    d.rectangle([x, y, x + w, y + h], fill=(220, 235, 215))
    cx, cy, r = x + 0.28 * w, y + 0.52 * h, 32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(66, 135, 245))
    d.ellipse([cx - 18, cy - 14, cx - 2, cy + 2], fill=(46, 160, 67))
    d.ellipse([cx + 2, cy + 6, cx + 20, cy + 20], fill=(46, 160, 67))
    d.ellipse([cx - 6, cy - 26, cx + 10, cy - 12], fill=(46, 160, 67))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 60, 120), width=2)
    kx, ky, kr = x + 0.74 * w, y + 0.5 * h, 27
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255), outline=(40, 40, 40), width=2)
    d.line([(kx, ky), (kx, ky - 17)], fill=(40, 40, 40), width=3)
    d.line([(kx, ky), (kx + 12, ky + 6)], fill=(40, 40, 40), width=3)
    d.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=RED)
    d.text((x + 0.52 * w, y + 0.82 * h), "DAY 14 \u00b7 NO DEAL", font=F_SANS_B(11), fill=RED_DK)

def illo_ashes(x, y, w):
    h = 90
    d.rectangle([x, y, x + w, y + h], fill=(34, 139, 34))
    d.rectangle([x, y + 0.42 * h, x + w, y + 0.78 * h], fill=(176, 141, 87))
    d.line([(x, y + 0.42 * h), (x + w, y + 0.42 * h)], fill=(255, 255, 255), width=2)
    d.line([(x, y + 0.78 * h), (x + w, y + 0.78 * h)], fill=(255, 255, 255), width=2)
    # stumps with bails, centred right
    sx = x + 0.68 * w
    for i in range(3):
        d.rectangle([sx + i * 7, y + 0.32 * h, sx + i * 7 + 5, y + 0.62 * h], fill=(245, 222, 179), outline=(150, 120, 70))
    d.rectangle([sx, y + 0.29 * h, sx + 19, y + 0.33 * h], fill=(245, 222, 179))
    # bat leaning on the stumps
    bx, by = x + 0.58 * w, y + 0.62 * h
    d.polygon([(bx, by), (bx + 10, by - 34), (bx + 20, by - 30), (bx + 10, by + 2)], fill=(205, 170, 120), outline=(120, 85, 50))
    # ball with motion arc
    d.arc([x + 0.2 * w, y + 0.35 * h, x + 0.45 * w, y + 0.75 * h], start=200, end=340, fill=(255, 255, 255), width=2)
    d.ellipse([x + 0.42 * w - 8, y + 0.62 * h - 8, x + 0.42 * w + 8, y + 0.62 * h + 8], fill=(185, 28, 28), outline=(255, 255, 255), width=1)

def illo_quake(x, y, w):
    h = 56
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 190))
    d.polygon([(x, y + h), (x + 0.3 * w, y + 0.15 * h), (x + 0.55 * w, y + h)], fill=(120, 90, 60))
    d.polygon([(x + 0.4 * w, y + h), (x + 0.7 * w, y + 0.3 * h), (x + w, y + h)], fill=(90, 70, 50))
    pts = [(x + i * w / 10, y + h * (0.5 + (0.28 if i % 2 else -0.28))) for i in range(11)]
    d.line(pts, fill=RED, width=3)
    hx, hy = x + 0.72 * w, y + 0.62 * h
    d.rectangle([hx, hy, hx + 26, hy + 16], fill=(255, 255, 255), outline=(60, 60, 60))
    d.polygon([(hx - 3, hy), (hx + 13, hy - 10), (hx + 29, hy)], fill=RED)

def illo_hk(x, y, w):
    h = 56
    d.rectangle([x, y, x + w, y + h], fill=(210, 225, 240))
    bx, by = x + 0.32 * w, y + 0.42 * h
    d.rectangle([bx, by, bx + 0.36 * w, by + 0.42 * h], fill=(30, 50, 90))
    d.rectangle([bx + 0.08 * w, by + 0.05 * h, bx + 0.28 * w, by + 0.1 * h], fill=(247, 241, 227))
    px, py = x + 0.36 * w, y + 0.22 * h
    d.rectangle([px, py, px + 0.28 * w, py + 0.3 * h], fill=(255, 255, 255), outline=(120, 120, 120))
    d.line([(px + 6, py + 18), (px + 16, py + 28), (px + 34, py + 8)], fill=RED, width=4)
    d.text((x + 0.72 * w, y + 0.6 * h), "723", font=F_SANS_B(16), fill=(30, 50, 90))

def illo_bahrain(x, y, w):
    h = 56
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 52))
    for sx, sy in [(0.1, 0.15), (0.3, 0.1), (0.55, 0.12), (0.85, 0.18)]:
        d.ellipse([x + sx * w - 1, y + sy * h - 1, x + sx * w + 1, y + sy * h + 1], fill=(255, 255, 255))
    # radar dish
    dx, dy = x + 0.3 * w, y + 0.55 * h
    d.arc([dx - 22, dy - 22, dx + 22, dy + 22], start=200, end=340, fill=(180, 200, 255), width=4)
    d.line([(dx, dy), (dx + 18, dy - 18)], fill=(180, 200, 255), width=3)
    d.line([(dx, dy), (dx, dy + 14)], fill=(180, 200, 255), width=3)
    # missile trail + flame
    d.line([(x + 0.62 * w, y + 0.2 * h), (x + 0.9 * w, y + 0.45 * h)], fill=(255, 200, 80), width=2)
    d.ellipse([x + 0.9 * w - 6, y + 0.45 * h - 6, x + 0.9 * w + 6, y + 0.45 * h + 6], fill=(255, 140, 0))
    d.rectangle([x + 0.05 * w, y + 0.82 * h, x + w, y + h], fill=(8, 12, 30))

def illo_israel(x, y, w):
    h = 56
    d.rectangle([x, y, x + w, y + h], fill=(235, 230, 215))
    bx, by = x + 0.25 * w, y + 0.25 * h
    d.polygon([(bx, by), (bx + 0.5 * w, by), (bx + 0.25 * w, by - 14)], fill=(90, 100, 120))
    d.rectangle([bx, by, bx + 0.5 * w, by + 0.45 * h], fill=(180, 185, 195))
    for i in range(4):
        cx = bx + 0.06 * w + i * 0.12 * w
        d.rectangle([cx, by + 0.05 * h, cx + 8, by + 0.42 * h], fill=(245, 245, 245))
    d.rectangle([bx - 6, by + 0.45 * h, bx + 0.5 * w + 6, by + 0.52 * h], fill=(90, 100, 120))
    # small flag
    fx, fy = x + 0.82 * w, y + 0.15 * h
    d.line([(fx, fy), (fx, fy + 26)], fill=(60, 60, 60), width=2)
    d.rectangle([fx, fy, fx + 26, fy + 16], fill=(255, 255, 255), outline=(40, 90, 200))
    d.line([(fx, fy + 3), (fx + 26, fy + 3)], fill=(40, 90, 200), width=2)
    d.line([(fx, fy + 13), (fx + 26, fy + 13)], fill=(40, 90, 200), width=2)

def illo_bitcoin(x, y, w):
    h = 56
    d.rectangle([x, y, x + w, y + h], fill=(247, 147, 26))
    cx, cy, r = x + 0.26 * w, y + 0.5 * h, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    d.text((cx - 9, cy - 17), "B", font=F_SANS_B(32), fill=(247, 147, 26))
    d.line([(cx - 4, cy - 20), (cx - 4, cy + 20)], fill=(247, 147, 26), width=2)
    d.line([(cx + 4, cy - 20), (cx + 4, cy + 20)], fill=(247, 147, 26), width=2)
    pts = [(x + 0.5 * w, y + 0.25 * h), (x + 0.62 * w, y + 0.45 * h), (x + 0.74 * w, y + 0.35 * h),
           (x + 0.86 * w, y + 0.55 * h), (x + 0.97 * w, y + 0.5 * h)]
    d.line(pts, fill=(255, 255, 255), width=3)
    d.text((x + 0.52 * w, y + 0.62 * h), "$60,073", font=F_SANS_B(15), fill=(255, 255, 255))

def illo_spacex(x, y, w):
    h = 56
    d.rectangle([x, y, x + w, y + h], fill=(10, 18, 46))
    for sx, sy in [(0.08, 0.2), (0.2, 0.1), (0.4, 0.18), (0.62, 0.1), (0.85, 0.22), (0.93, 0.1)]:
        d.ellipse([x + sx * w - 1, y + sy * h - 1, x + sx * w + 1, y + sy * h + 1], fill=(255, 255, 255))
    rx = x + 0.45 * w
    d.rectangle([rx, y + 0.12 * h, rx + 14, y + 0.62 * h], fill=(240, 240, 240))
    d.polygon([(rx, y + 0.12 * h), (rx + 7, y + 0.02 * h), (rx + 14, y + 0.12 * h)], fill=RED)
    d.polygon([(rx - 6, y + 0.62 * h), (rx, y + 0.5 * h), (rx, y + 0.62 * h)], fill=(200, 200, 200))
    d.polygon([(rx + 14, y + 0.62 * h), (rx + 14, y + 0.5 * h), (rx + 20, y + 0.62 * h)], fill=(200, 200, 200))
    d.polygon([(rx + 3, y + 0.62 * h), (rx + 7, y + 0.85 * h), (rx + 11, y + 0.62 * h)], fill=(255, 160, 0))
    d.rectangle([x, y + 0.86 * h, x + w, y + h], fill=(40, 40, 60))
    d.line([(x + 0.7 * w, y + 0.86 * h), (x + 0.7 * w, y + 0.3 * h)], fill=(120, 120, 140), width=3)

def illo_jura(x, y, w):
    h = 56
    d.rectangle([x, y, x + w, y + h], fill=(170, 190, 210))
    d.polygon([(x, y + h), (x + 0.35 * w, y + 0.45 * h), (x + 0.7 * w, y + h)], fill=(60, 110, 70))
    d.polygon([(x + 0.5 * w, y + h), (x + 0.8 * w, y + 0.55 * h), (x + w, y + h)], fill=(45, 90, 60))
    cx, cy = x + 0.5 * w, y + 0.3 * h
    for ox, oy, r in [(-26, 4, 16), (0, -6, 20), (26, 4, 16)]:
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r], fill=(70, 80, 95))
    for i in range(6):
        rx = x + (0.15 + i * 0.13) * w
        d.line([(rx, y + 0.55 * h), (rx - 4, y + 0.72 * h)], fill=(40, 90, 180), width=2)

def illo_porsche(x, y, w):
    h = 56
    for i, col in enumerate([(255, 170, 60), (255, 140, 50), (240, 110, 60), (200, 80, 70)]):
        d.rectangle([x, y + i * h / 4, x + w, y + (i + 1) * h / 4], fill=col)
    d.ellipse([x + 0.68 * w, y + 0.08 * h, x + 0.68 * w + 26, y + 0.08 * h + 26], fill=(255, 230, 150))
    # car silhouette: low sleek body + cabin with windows
    cx, cy = x + 0.1 * w, y + 0.6 * h
    d.polygon([(cx, cy), (cx + 16, cy - 10), (cx + 66, cy - 10), (cx + 82, cy), (cx + 82, cy + 7), (cx, cy + 7)], fill=(25, 25, 35))
    d.polygon([(cx + 20, cy - 9), (cx + 28, cy - 19), (cx + 54, cy - 19), (cx + 60, cy - 9)], fill=(25, 25, 35))
    d.polygon([(cx + 30, cy - 17), (cx + 36, cy - 17), (cx + 36, cy - 10), (cx + 30, cy - 10)], fill=(150, 200, 235))
    d.polygon([(cx + 40, cy - 17), (cx + 50, cy - 17), (cx + 50, cy - 10), (cx + 40, cy - 10)], fill=(150, 200, 235))
    for wx in (0.3, 0.72):
        wxp = x + wx * w
        d.ellipse([wxp - 8, cy + 1, wxp + 8, cy + 17], fill=(10, 10, 10), outline=(200, 200, 200))
        d.ellipse([wxp - 3, cy + 6, wxp + 3, cy + 12], fill=(180, 180, 180))
    d.rectangle([x, y + 0.86 * h, x + w, y + h], fill=(60, 45, 40))
    # palm
    px, py = x + 0.88 * w, y + h
    d.line([(px, py), (px + 4, y + 0.3 * h)], fill=(90, 60, 30), width=3)
    for ang in (-50, -20, 10, 40):
        a = math.radians(ang - 90)
        d.line([(px + 4, y + 0.3 * h), (px + 4 + 16 * math.cos(a), y + 0.3 * h + 16 * math.sin(a))], fill=(30, 120, 50), width=3)

# ---------------------------------------------------------------- big cards (y 228-470)
BIG_Y, BIG_H = 228, 242
big = [
    (14, "RUSSIA: 550 MUNITIONS", illo_russia, "1", "LVIV \u00b7 WAR",
     "Biggest overnight attack of the war",
     "496 drones and 53 missiles; five killed, ten hurt. A family of four died in Lviv.",
     "(Ukraine air force; Zelenskyy)"),
    (351, "COP31: NO DEAL YET", illo_cop31, "2", "ANTALYA \u00b7 CLIMATE",
     "Climate summit runs into overtime",
     "Talks deadlocked past their deadline; no deal as Sunday began. A third text is promised.",
     "(AP; UN)"),
    (688, "ASHES: HEAD 123", illo_ashes, "3", "PERTH \u00b7 CRICKET",
     "Australia win the Ashes in two days",
     "Head smashed 123 off 83; Starc took 7 for 58 as England fell by eight wickets.",
     "(Sportskeeda; Cricbuzz)"),
]
for (x, bann, illo, num, loc, hl, body, src) in big:
    card(x, BIG_Y, 322, BIG_H, illo=None)
    bh = banner(x + 1, BIG_Y + 1, 320, bann, size=19)
    illo(x + 1, BIG_Y + 1 + bh, 320)
    card_text(x, BIG_Y + 1 + bh + 90 + 6, 322, num, loc, hl, body, src, BIG_Y + BIG_H, hl_size=20, body_size=12)

# ---------------------------------------------------------------- medium cards (2 rows of 4)
MED_H = 190
med_rows = [
    (478, [
        (14, "MYANMAR: QUAKE 4.1", illo_quake, "4", "MYANMAR \u00b7 EARTHQUAKE",
         "Magnitude 4.1 quake shakes Myanmar",
         "Struck at 02:35 IST, 95 km deep. No damage reported.",
         "(NCS; ANI)"),
        (266, "HONG KONG: VOTE", illo_hk, "5", "HONG KONG \u00b7 ELECTION",
         "Hong Kong votes for 723 seats",
         "856 candidates contest 31 subsectors; polls 9am\u20136pm.",
         "(China Daily Asia)"),
        (518, "BAHRAIN: IRGC CLAIM", illo_bahrain, "6", "BAHRAIN \u00b7 WAR",
         "IRGC claims US radar strikes",
         "Guards say they hit Patriot radars at al-Riffa and Awali. Unconfirmed.",
         "(Al Jazeera)"),
        (770, "ISRAEL: COALITION TALKS", illo_israel, "7", "JERUSALEM \u00b7 POLITICS",
         "Eisenkot opens talks with Likud",
         "First meeting on Sunday; Likud wants Netanyahu as sole PM.",
         "(Times of Israel)"),
    ]),
    (676, [
        (14, "BITCOIN: $60,073", illo_bitcoin, "8", "WORLD \u00b7 MARKETS",
         "Bitcoin holds above $60,000",
         "Near $60,073 early Sunday after Friday\u2019s plunge to $55,130.",
         "(Finnhub; CoinDesk)"),
        (266, "SPACEX: LAUNCH DUE", illo_spacex, "9", "VANDENBERG \u00b7 SPACE",
         "Spy-satellite launch due at noon",
         "Falcon 9 to lift NROL-136 at 12:16 UTC; booster to land back.",
         "(SpaceX; NRO)"),
        (518, "JURA: ORANGE ALERT", illo_jura, "10", "JURA \u00b7 WEATHER",
         "France warns of floods in the Jura",
         "Orange alert for Sunday: 70\u201390mm of rain, up to 100mm.",
         "(M\u00e9t\u00e9o-France; Le Progr\u00e8s)"),
        (770, "PORSCHE: DUBAI", illo_porsche, "11", "DUBAI \u00b7 CULTURE",
         "Icons of Porsche opens in Dubai",
         "Sheikh Mansoor tours the opening day of the classic-car festival.",
         "(WAM; ANI)"),
    ]),
]
for (ry, cards) in med_rows:
    for (x, bann, illo, num, loc, hl, body, src) in cards:
        card(x, ry, 240, MED_H, illo=None)
        bh = banner(x + 1, ry + 1, 238, bann, size=14)
        illo(x + 1, ry + 1 + bh, 238)
        card_text(x, ry + 1 + bh + 56 + 5, 240, num, loc, hl, body, src, ry + MED_H, hl_size=16, body_size=11)

# ---------------------------------------------------------------- map + date check (y 874-990)
MAP_Y, MAP_H = 874, 116
d.text((14, MAP_Y), "WHERE IT HAPPENED", font=F_SANS_B(13), fill=INK)
d.rectangle([14, MAP_Y + 18, 640, MAP_Y + MAP_H], fill=(18, 48, 110), outline=(180, 172, 152), width=1)
CONTINENTS = {
    "na": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-95, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-150, 60), (-168, 66)],
    "sa": [(-80, 10), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -52), (-73, -40), (-72, -20), (-80, -5), (-80, 10)],
    "eu": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (25, 65), (20, 70), (15, 70), (5, 60), (0, 55), (-5, 50), (-10, 43), (-10, 36)],
    "af": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15), (48, 11), (51, 10), (44, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -30), (12, -18), (8, -2), (9, 4), (-8, 5), (-17, 15)],
    "as": [(30, 36), (35, 42), (40, 46), (45, 48), (50, 50), (55, 55), (60, 60), (65, 68), (70, 72), (75, 73), (85, 75), (95, 77), (105, 77), (115, 73), (125, 72), (135, 72), (150, 70), (160, 66), (170, 66), (178, 65), (170, 60), (160, 55), (150, 50), (140, 45), (135, 40), (130, 35), (127, 33), (122, 30), (120, 25), (115, 20), (110, 15), (105, 10), (100, 8), (95, 10), (90, 15), (88, 22), (85, 20), (80, 15), (77, 8), (75, 15), (70, 20), (65, 25), (60, 25), (55, 26), (50, 28), (48, 30), (44, 32), (40, 36), (35, 36), (30, 36)],
    "au": [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)],
    "gl": [(-55, 60), (-45, 60), (-40, 64), (-30, 68), (-20, 70), (-25, 76), (-40, 80), (-55, 76), (-60, 70), (-55, 60)],
    "uk": [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-3, 50), (-5, 50)],
    "jp": [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41), (143, 42), (141, 45), (140, 40), (139, 37), (137, 36), (133, 35), (130, 31)],
    "nz": [(167, -45), (170, -43), (173, -41), (175, -38), (178, -37), (176, -40), (174, -42), (171, -44), (168, -46), (167, -45)],
}
MAP_X0, MAP_X1 = 14, 640
MAP_TOP, MAP_BOT = MAP_Y + 18, MAP_Y + MAP_H
def proj(lon, lat):
    px = MAP_X0 + (lon + 180) / 360 * (MAP_X1 - MAP_X0)
    py = MAP_TOP + (75 - lat) / 135 * (MAP_BOT - MAP_TOP)
    return (px, py)
for poly in CONTINENTS.values():
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=(232, 214, 170))
DOTS = [
    (1, 24.0, 49.8, (0, 0)), (2, 30.7, 36.9, (0, 0)), (3, 115.9, -31.9, (0, 0)),
    (4, 94.6, 24.4, (0, 0)), (5, 114.2, 22.3, (0, 0)), (6, 50.6, 26.2, (0, 0)),
    (7, 35.2, 31.8, (16, -12)), (8, 0.0, 51.5, (-16, -10)), (9, -120.6, 34.7, (0, 0)),
    (10, 5.9, 46.7, (0, 0)), (11, 55.3, 25.2, (18, 2)),
]
for (n, lon, lat, (ox, oy)) in DOTS:
    tx, ty = proj(lon, lat)
    cx, cy = tx + ox, ty + oy
    if ox or oy:
        d.line([(tx, ty), (cx, cy)], fill=(255, 255, 255), width=1)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=(255, 255, 255), width=1)
    s = str(n)
    d.text((cx - text_w(s, F_SANS_B(9)) / 2, cy - 6.5), s, font=F_SANS_B(9), fill=(255, 255, 255))

# date check box
d.rectangle([650, MAP_Y, 1010, MAP_Y + MAP_H], fill=(255, 245, 240), outline=RED, width=2)
d.text((660, MAP_Y + 5), "DATE CHECK", font=F_SANS_B(13), fill=RED)
dc = ("Left out \u2014 Saturday 21 Nov news: EU\u2013Indonesia trade deal; El Chapo Isidro\u2019s capture; "
      "Peru quake 6.7; Gaza aid-vehicle strike; Zelenskyy\u2019s peace-plan remarks. Older: Wall Street "
      "correction (Fri 20 Nov); Texas execution (Thu 19 Nov); Iran strikes on Kuwait & Bahrain (Wed 19 Nov). "
      "Not yet played when drawn: Las Vegas GP (04:00 UTC); Pope\u2019s Angelus (11:00 UTC); Liverpool v Man Utd.")
draw_wrapped(660, MAP_Y + 23, dc, F_SANS(9), 340, fill=INK, leading=12)

# ---------------------------------------------------------------- footer
hline(996, w=1)
d.text((14, 1000), "Every story here happened, or was first reported, on Sunday 22 November 2026. Officials\u2019 counts and claims are attributed.",
       font=F_SANS(10), fill=GREY)
d.text((14, 1012), "Sources named beside each story \u00b7 original drawings \u00b7 EARLY EDITION \u2014 drawn at about 03:00 UTC, before the day\u2019s later events; a later edition adds them.",
       font=F_SANS(10), fill=GREY)

# ---------------------------------------------------------------- save
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print(out, os.path.getsize(out))
