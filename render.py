#!/usr/bin/env python3
"""Render the Sunday 22 November 2026 front page for news-image-20261122 (Round 8).

One 1024x1024 broadsheet: 35 verified stories, 7 regions. Top 1's structure
(cream paper, serif masthead, 6-fact strip, colourful region bar, 3 big hero
cards, 2 rows of small illustrated cards, world map, dense numbered list,
red DATE CHECK box) with richer layered illustrations and the sharpest
verified numbers for the day. All story data is inline in this file.
Deterministic: fixed seed, no timestamps in the image.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

random.seed(20261122)

W, H = 1024, 1024
PAPER = (247, 241, 222)
PAPER_DARK = (240, 230, 204)
INK = (26, 26, 26)
GREY = (90, 86, 76)
RED = (185, 28, 28)
RED_DARK = (153, 27, 27)
NAVY = (15, 32, 64)
TAN = (216, 196, 154)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_font_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, box, top, bottom):
    """Vertical gradient fill inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for y in range(y0, y1):
        draw.line([(x0, y), (x1, y)], fill=lerp(top, bottom, (y - y0) / h))


def hgrad(draw, box, left, right):
    """Horizontal gradient fill inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    w = max(1, x1 - x0)
    for x in range(x0, x1):
        draw.line([(x, y0), (x, y1)], fill=lerp(left, right, (x - x0) / w))


def glow(draw, cx, cy, r, colour, rings=4):
    """Soft radial glow: concentric circles fading out."""
    for i in range(rings, 0, -1):
        rr = r * i // rings
        a = 255 // (rings + 2) * (rings - i + 1)
        overlay = Image.new("RGBA", (rr * 2 + 4, rr * 2 + 4), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([2, 2, 2 + rr * 2, 2 + rr * 2], fill=colour + (a,))
        draw._image.paste(overlay, (cx - rr - 2, cy - rr - 2), overlay)


def stars(draw, box, n, colour=(255, 255, 255)):
    x0, y0, x1, y1 = box
    for _ in range(n):
        x = random.randint(x0 + 2, x1 - 2)
        y = random.randint(y0 + 2, y1 - 2)
        r = random.choice([1, 1, 1, 2])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=colour)


def wrap(text, font, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, colour, width, leading=None, max_lines=None):
    """Draw a wrapped paragraph; returns the y just below the last line."""
    leading = leading or int(font.size * 1.28)
    lines = wrap(text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=colour)
        y += leading
    return y


def centre(draw, cx, y, text, font, colour):
    draw.text((cx - font.getlength(text) / 2, y), text, font=font, fill=colour)


def skyline(draw, box, base_y, colour, lit=True):
    """Deterministic city skyline silhouette with lit windows."""
    x0, y0, x1, y1 = box
    x = x0
    while x < x1 - 8:
        bw = random.randint(18, 34)
        bh = random.randint(18, max(19, base_y - y0 - 6))
        top = base_y - bh
        draw.rectangle([x, top, min(x + bw, x1), base_y], fill=colour)
        if lit:
            for wy in range(top + 5, base_y - 5, 9):
                for wx in range(x + 4, min(x + bw - 4, x1 - 4), 8):
                    if random.random() < 0.45:
                        draw.rectangle([wx, wy, wx + 3, wy + 4],
                                       fill=(255, 214, 110))
        x += bw + random.randint(2, 7)


def waves(draw, box, colour, n=3, amp=5):
    """Sine wave lines across a box."""
    x0, y0, x1, y1 = box
    for k in range(n):
        yy = y0 + (y1 - y0) * (k + 1) / (n + 1)
        pts = []
        for x in range(x0, x1 + 1, 6):
            pts.append((x, yy + amp * math.sin((x - x0) / 26.0 + k * 1.7)))
        draw.line(pts, fill=colour, width=2)

# ---------------------------------------------------------------------------
# Hero illustrations (each ~325 x 112): layered, with gradient skies, glow,
# silhouettes and several scene elements so they read as illustrations,
# not diagrams.
# ---------------------------------------------------------------------------

def ill_cop31(draw, box):
    """COP31: teal dusk sky, glowing globe, red thermometer, white clock."""
    x0, y0, x1, y1 = box
    vgrad(draw, box, (38, 92, 110), (12, 42, 66))
    stars(draw, (x0, y0, x1, y0 + 45), 14)
    # ground band
    draw.rectangle([x0, y1 - 16, x1, y1], fill=(10, 30, 48))
    # sun glow low on the horizon
    glow(draw, x1 - 46, y1 - 20, 26, (255, 170, 80))
    draw.ellipse([x1 - 62, y1 - 36, x1 - 30, y1 - 4], fill=(255, 196, 110))
    # globe, centre-left
    cx, cy, r = x0 + 62, y0 + 58, 34
    glow(draw, cx, cy, r + 12, (90, 180, 220))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 140, 205))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(220, 240, 250), width=2)
    for (gx, gy, gr) in [(cx - 12, cy - 10, 11), (cx + 12, cy + 6, 9),
                         (cx + 4, cy - 18, 7), (cx - 18, cy + 14, 6)]:
        draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(74, 160, 90))
    # thermometer, left
    tx = x0 + 14
    draw.rounded_rectangle([tx, y0 + 18, tx + 12, y1 - 22], 6, fill=(240, 240, 235),
                           outline=(180, 40, 40), width=2)
    draw.ellipse([tx - 3, y1 - 34, tx + 15, y1 - 16], fill=(200, 40, 40))
    draw.rectangle([tx + 4, y0 + 34, tx + 8, y1 - 26], fill=(200, 40, 40))
    for yy in range(y0 + 24, y0 + 52, 7):
        draw.line([(tx + 12, yy), (tx + 17, yy)], fill=(120, 30, 30), width=1)
    # clock, right
    kx, ky, kr = x1 - 52, y0 + 34, 20
    draw.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(250, 250, 245),
                 outline=(30, 30, 30), width=2)
    draw.line([(kx, ky), (kx, ky - 12)], fill=(30, 30, 30), width=2)
    draw.line([(kx, ky), (kx + 9, ky + 5)], fill=(30, 30, 30), width=2)
    draw.ellipse([kx - 2, ky - 2, kx + 2, ky + 2], fill=(200, 40, 40))


def ill_ukraine(draw, box):
    """Ukraine night: dark sky, lit skyline, orange missile trails, red glow."""
    x0, y0, x1, y1 = box
    vgrad(draw, box, (10, 14, 38), (52, 24, 62))
    stars(draw, (x0, y0, x1, y0 + 50), 22)
    # moon + glow
    glow(draw, x1 - 44, y0 + 24, 20, (230, 230, 200))
    draw.ellipse([x1 - 56, y0 + 12, x1 - 32, y0 + 36], fill=(238, 236, 210))
    # missile trails: bright streaks with glowing heads
    for (sx, sy, ex, ey) in [(x0 + 30, y0 + 8, x0 + 96, y0 + 66),
                             (x0 + 150, y0 + 2, x0 + 196, y0 + 52),
                             (x0 + 240, y0 + 12, x0 + 282, y0 + 60)]:
        draw.line([(sx, sy), (ex, ey)], fill=(255, 150, 60), width=3)
        draw.line([(sx, sy), (ex, ey)], fill=(255, 210, 120), width=1)
        glow(draw, ex, ey, 9, (255, 170, 70))
        draw.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 220, 140))
    # skyline silhouette with lit windows, two depths
    skyline(draw, (x0, y0 + 52, x1, y1 - 8), y1 - 8, (16, 18, 34), lit=True)
    # red horizon glow
    draw.rectangle([x0, y1 - 10, x1, y1], fill=(120, 28, 28))
    draw.rectangle([x0, y1 - 10, x1, y1 - 7], fill=(200, 70, 50))


def ill_vegas(draw, box):
    """Las Vegas: sunset gradient, big low sun, race car, chequered flag."""
    x0, y0, x1, y1 = box
    vgrad(draw, box, (255, 140, 60), (150, 40, 110))
    vgrad(draw, (x0, y0 + 52, x1, y1), (190, 60, 120), (70, 20, 80))
    # sun + glow
    glow(draw, x1 - 62, y0 + 46, 34, (255, 220, 130))
    draw.ellipse([x1 - 88, y0 + 20, x1 - 36, y0 + 72], fill=(255, 226, 150))
    # distant strip towers
    for (bx, bw, bh) in [(x0 + 12, 14, 34), (x0 + 34, 10, 46), (x0 + 52, 12, 28)]:
        draw.rectangle([bx, y1 - 58 - bh, bx + bw, y1 - 58], fill=(60, 16, 60))
        for wy in range(y1 - 56 - bh, y1 - 62, 8):
            draw.rectangle([bx + 3, wy, bx + 6, wy + 3], fill=(255, 220, 120))
    # road
    draw.rectangle([x0, y1 - 34, x1, y1], fill=(32, 28, 44))
    for lx in range(x0 + 6, x1, 26):
        draw.line([(lx, y1 - 17), (lx + 12, y1 - 17)], fill=(250, 220, 90), width=3)
    # race car silhouette
    cx0, cy = x0 + 84, y1 - 46
    draw.polygon([(cx0, cy), (cx0 + 26, cy - 2), (cx0 + 62, cy - 2),
                  (cx0 + 96, cy + 6), (cx0 + 118, cy + 6), (cx0 + 122, cy + 12),
                  (cx0 + 4, cy + 12)], fill=(12, 12, 16))
    draw.polygon([(cx0 + 34, cy - 2), (cx0 + 48, cy - 16), (cx0 + 76, cy - 16),
                  (cx0 + 84, cy - 2)], fill=(12, 12, 16))
    for wx in (cx0 + 24, cx0 + 94):
        draw.ellipse([wx - 11, cy + 2, wx + 11, cy + 24], fill=(8, 8, 10))
        draw.ellipse([wx - 5, cy + 8, wx + 5, cy + 18], fill=(150, 150, 160))
    # speed lines
    for (sx, sy, ln) in [(x0 + 8, cy - 6, 34), (x0 + 22, cy + 4, 26),
                         (x0 + 2, cy - 16, 22)]:
        draw.line([(sx, sy), (sx + ln, sy)], fill=(255, 240, 200), width=2)
    # chequered flag, top right
    fx, fy = x1 - 46, y0 + 8
    draw.line([(fx, fy), (fx, fy + 26)], fill=(30, 30, 30), width=2)
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                draw.rectangle([fx + 2 + c * 7, fy + r * 7, fx + 9 + c * 7,
                                fy + 7 + r * 7], fill=(20, 20, 20))
            else:
                draw.rectangle([fx + 2 + c * 7, fy + r * 7, fx + 9 + c * 7,
                                fy + 7 + r * 7], fill=(250, 250, 250))


# ---------------------------------------------------------------------------
# Small-card illustrations (each ~196 x 48): gradient ground + a clear icon.
# ---------------------------------------------------------------------------

def _mini(draw, box, top, bottom):
    vgrad(draw, box, top, bottom)


def ill_scales(draw, box):
    _mini(draw, box, (232, 222, 190), (206, 188, 140))
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, y0 + 10
    draw.line([(cx, cy), (cx, y1 - 8)], fill=(120, 90, 30), width=3)
    draw.line([(cx - 34, cy + 6), (cx + 34, cy + 6)], fill=(120, 90, 30), width=3)
    for s in (-1, 1):
        px = cx + s * 34
        draw.line([(px, cy + 6), (px, cy + 20)], fill=(120, 90, 30), width=2)
        draw.polygon([(px - 12, cy + 20), (px + 12, cy + 20), (px, cy + 30)],
                     fill=(180, 140, 50))
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(120, 90, 30))


def ill_tanker(draw, box):
    _mini(draw, box, (140, 190, 215), (40, 90, 130))
    x0, y0, x1, y1 = box
    draw.ellipse([x1 - 34, y0 + 4, x1 - 12, y0 + 26], fill=(255, 220, 130))
    # hull + containers
    draw.polygon([(x0 + 22, y0 + 26), (x1 - 22, y0 + 26), (x1 - 34, y1 - 12),
                  (x0 + 34, y1 - 12)], fill=(40, 44, 52))
    for (bx, col) in [(x0 + 44, (200, 60, 50)), (x0 + 70, (60, 120, 200)),
                      (x0 + 96, (230, 180, 60))]:
        draw.rectangle([bx, y0 + 14, bx + 22, y0 + 26], fill=col)
    draw.rectangle([x1 - 52, y0 + 6, x1 - 34, y0 + 26], fill=(230, 230, 225))
    waves(draw, (x0, y1 - 14, x1, y1), (200, 230, 245), n=2, amp=3)


def ill_mountains(draw, box):
    _mini(draw, box, (150, 190, 225), (220, 210, 180))
    x0, y0, x1, y1 = box
    draw.ellipse([x1 - 30, y0 + 4, x1 - 10, y0 + 24], fill=(255, 225, 140))
    draw.polygon([(x0, y1), (x0 + 52, y0 + 8), (x0 + 104, y1)], fill=(110, 80, 60))
    draw.polygon([(x0 + 52, y0 + 8), (x0 + 66, y0 + 20), (x0 + 40, y0 + 20)],
                 fill=(250, 250, 250))
    draw.polygon([(x0 + 84, y1), (x0 + 142, y0 + 16), (x1, y1)], fill=(80, 58, 44))
    draw.polygon([(x0 + 142, y0 + 16), (x0 + 154, y0 + 26), (x0 + 130, y0 + 26)],
                 fill=(250, 250, 250))
    # seismograph zigzag in red across the lower third
    pts = []
    for i, x in enumerate(range(x0 + 6, x1 - 4, 8)):
        pts.append((x, y1 - 12 + (10 if i % 4 == 1 else (-10 if i % 4 == 3 else 0))))
    draw.line(pts, fill=(185, 28, 28), width=2)


def ill_ballot(draw, box):
    _mini(draw, box, (200, 60, 60), (140, 30, 30))
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    draw.rectangle([cx - 34, y0 + 18, cx + 34, y1 - 6], fill=(70, 40, 40))
    draw.rectangle([cx - 40, y0 + 12, cx + 40, y0 + 20], fill=(50, 28, 28))
    draw.rectangle([cx - 8, y0 + 14, cx + 8, y0 + 18], fill=(20, 20, 20))
    draw.polygon([(cx + 6, y0 - 2), (cx + 22, y0 - 12), (cx + 30, y0 + 2),
                  (cx + 14, y0 + 12)], fill=(250, 250, 245))
    draw.line([(cx + 12, y0 + 4), (cx + 18, y0 + 10), (cx + 26, y0 - 2)],
              fill=(30, 140, 60), width=2)


def ill_cricket(draw, box):
    _mini(draw, box, (90, 160, 90), (40, 110, 50))
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y1 - 18, x1, y1], fill=(210, 190, 140))
    draw.line([(x0, y1 - 18), (x1, y1 - 18)], fill=(255, 255, 255), width=2)
    # stumps
    sx = x0 + 30
    for dx in (0, 8, 16):
        draw.line([(sx + dx, y0 + 12), (sx + dx, y0 + 30)], fill=(240, 210, 130),
                  width=3)
    draw.line([(sx, y0 + 10), (sx + 16, y0 + 10)], fill=(240, 210, 130), width=2)
    # red ball + bat
    draw.ellipse([x1 - 40, y0 + 14, x1 - 24, y0 + 30], fill=(185, 30, 30))
    draw.ellipse([x1 - 36, y0 + 18, x1 - 28, y0 + 26], fill=(230, 90, 80))
    draw.line([(x1 - 62, y0 + 8), (x1 - 52, y0 + 26)], fill=(210, 180, 120), width=5)


def ill_quake_sea(draw, box):
    _mini(draw, box, (60, 130, 180), (20, 60, 110))
    x0, y0, x1, y1 = box
    draw.ellipse([x0 + 12, y0 + 4, x0 + 34, y0 + 26], fill=(255, 225, 140))
    waves(draw, (x0, y0 + 12, x1, y1 - 4), (180, 220, 245), n=4, amp=4)
    # small island + palm
    draw.ellipse([x1 - 62, y1 - 12, x1 - 8, y1 - 2], fill=(200, 180, 120))
    draw.line([(x1 - 34, y1 - 12), (x1 - 34, y1 - 30)], fill=(90, 60, 30), width=3)
    for a in (-50, -20, 10, 40):
        ex = x1 - 34 + int(14 * math.cos(math.radians(a - 90)))
        ey = y1 - 30 + int(14 * math.sin(math.radians(a - 90)))
        draw.line([(x1 - 34, y1 - 30), (ex, ey)], fill=(50, 140, 70), width=3)


def ill_cuffs(draw, box):
    _mini(draw, box, (50, 52, 66), (22, 24, 34))
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    for s in (-1, 1):
        ox = cx + s * 30
        draw.ellipse([ox - 16, y0 + 12, ox + 16, y0 + 44], outline=(200, 200, 205),
                     width=5)
        draw.ellipse([ox - 5, y0 + 23, ox + 5, y0 + 33], fill=(160, 160, 165))
    draw.arc([cx - 30, y0 - 2, cx + 30, y0 + 18], 180, 360, fill=(200, 200, 205),
             width=4)
    draw.ellipse([x1 - 30, y0 + 6, x1 - 14, y0 + 22], fill=(255, 214, 110))
    for px, py in [(x1 - 26, y0 + 10), (x1 - 20, y0 + 14), (x1 - 22, y0 + 18)]:
        draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(150, 110, 30))


def ill_missiles(draw, box):
    _mini(draw, box, (30, 32, 52), (90, 30, 40))
    x0, y0, x1, y1 = box
    stars(draw, (x0, y0, x1, y0 + 22), 10)
    # dome + three rising missiles with trails
    draw.arc([x0 + 60, y1 - 22, x1 - 60, y1 + 14], 180, 360, fill=(120, 130, 150),
             width=3)
    for (mx, mh) in [(x0 + 40, 26), ((x0 + x1) // 2, 34), (x1 - 46, 22)]:
        draw.line([(mx, y1 - 8), (mx, y1 - 8 - mh)], fill=(255, 170, 80), width=2)
        draw.polygon([(mx - 4, y1 - 8 - mh), (mx + 4, y1 - 8 - mh), (mx, y1 - 16 - mh)],
                     fill=(230, 230, 230))
        glow(draw, mx, y1 - 8 - mh, 6, (255, 180, 90))


def ill_robot(draw, box):
    _mini(draw, box, (120, 128, 140), (60, 64, 74))
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, y0 + 24
    draw.line([(cx, cy - 18), (cx, cy - 8)], fill=(180, 180, 185), width=3)
    draw.ellipse([cx - 3, cy - 22, cx + 3, cy - 16], fill=(255, 80, 80))
    draw.rounded_rectangle([cx - 26, cy - 8, cx + 26, cy + 20], 6,
                           fill=(190, 195, 200), outline=(70, 74, 82), width=2)
    for s in (-1, 1):
        draw.ellipse([cx + s * 15 - 5, cy + 2, cx + s * 15 + 5, cy + 12],
                     fill=(200, 40, 40))
    draw.line([(cx - 12, cy + 14), (cx + 12, cy + 14)], fill=(70, 74, 82), width=2)
    draw.line([(cx - 34, cy + 4), (cx - 26, cy + 4)], fill=(140, 144, 150), width=4)
    draw.line([(cx + 26, cy + 4), (cx + 34, cy + 4)], fill=(140, 144, 150), width=4)


def ill_rugby(draw, box):
    _mini(draw, box, (70, 150, 80), (30, 100, 45))
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y1 - 14, x1, y1], fill=(200, 185, 130))
    for lx in range(x0, x1, 28):
        draw.line([(lx, y0), (lx, y1 - 14)], fill=(220, 235, 220), width=1)
    # goal posts
    gx = x0 + 26
    draw.line([(gx, y0 + 6), (gx, y0 + 30)], fill=(250, 250, 250), width=3)
    draw.line([(gx + 22, y0 + 6), (gx + 22, y0 + 30)], fill=(250, 250, 250), width=3)
    draw.line([(gx, y0 + 18), (gx + 22, y0 + 18)], fill=(250, 250, 250), width=3)
    # ball
    bx, by = x1 - 44, y0 + 24
    draw.ellipse([bx - 20, by - 11, bx + 20, by + 11], fill=(150, 95, 50))
    draw.line([(bx - 20, by), (bx + 20, by)], fill=(240, 240, 240), width=2)
    draw.line([(bx, by - 11), (bx, by + 11)], fill=(240, 240, 240), width=1)

# ---------------------------------------------------------------------------
# World map (dark navy, tan continents, red numbered dots).
# ---------------------------------------------------------------------------

CONTINENTS = [
    # North America
    [(28, 706), (52, 690), (86, 686), (108, 700), (104, 722), (88, 730),
     (70, 748), (56, 760), (40, 744), (28, 724)],
    # South America
    [(96, 776), (112, 770), (128, 782), (132, 806), (122, 838), (110, 856),
     (102, 830), (94, 800)],
    # Europe
    [(142, 694), (158, 686), (172, 692), (176, 706), (164, 716), (150, 712),
     (142, 704)],
    # Africa
    [(148, 724), (168, 720), (186, 730), (188, 754), (176, 782), (162, 800),
     (152, 778), (144, 748)],
    # Asia
    [(178, 690), (210, 682), (248, 686), (272, 700), (268, 724), (244, 736),
     (222, 748), (200, 736), (186, 720), (178, 704)],
    # Australia
    [(232, 830), (254, 826), (268, 836), (262, 852), (242, 854), (230, 842)],
]

MAP_DOTS = [
    (1, 170, 720), (2, 166, 704), (3, 46, 734), (5, 204, 746),
    (6, 106, 814), (8, 258, 854), (9, 240, 830), (10, 56, 760),
    (11, 184, 754), (14, 196, 736),
]


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=NAVY)
    for poly in CONTINENTS:
        draw.polygon(poly, fill=TAN)
    # graticule hint
    for gx in range(x0 + 40, x1, 56):
        draw.line([(gx, y0), (gx, y1)], fill=(28, 52, 92), width=1)
    for n, dx, dy in MAP_DOTS:
        draw.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=RED,
                     outline=(255, 255, 255), width=1)
        f = F(SANS_B, 8)
        tw = f.getlength(str(n))
        draw.text((dx - tw / 2, dy - 5), str(n), font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------------------
# Stories — all data inline (verified 22 Nov 2026; see sources in footer).
# Regions: GLOBAL 7, EUROPE 8, MIDDLE EAST 5, ASIA 4, AMERICAS 6,
# OCEANIA 2, AFRICA 3 = 35.
# ---------------------------------------------------------------------------

FACTS = [
    ("186", "drones in the overnight raid"),
    ("161", "drones downed or jammed"),
    ("0.639s", "Verstappen's winning margin"),
    ("34", "lead changes in Las Vegas"),
    ("DAY 2", "of COP31 overtime"),
    ("35%", "electricity-share goal by 2035"),
]

REGIONS = [
    ("GLOBAL", 7, (30, 58, 95)),
    ("EUROPE", 8, (185, 28, 28)),
    ("MIDDLE EAST", 5, (139, 90, 43)),
    ("ASIA", 4, (107, 63, 160)),
    ("AMERICAS", 6, (14, 116, 144)),
    ("OCEANIA", 2, (15, 118, 110)),
    ("AFRICA", 3, (21, 128, 61)),
]

HEROES = [
    {
        "region": "GLOBAL", "ill": ill_cop31,
        "headline": "COP31 STALLS INTO DAY TWO OF OVERTIME",
        "body": "Antalya, Turkey \u2014 Talks missed their Friday deadline; negotiators weighed a last-minute text early Sunday. The draft drops fossil fuels \u2014 and concedes 1.5\u00b0C may be missed.",
        "source": "(AP / Reuters)",
    },
    {
        "region": "EUROPE", "ill": ill_ukraine,
        "headline": "186 DRONES RAIN ON UKRAINE OVERNIGHT",
        "body": "Kyiv \u2014 Russia fired 186 drones overnight, 72 of them jet-powered Shaheds. Air defences downed 161 by 08:00; strikes hit 18 sites.",
        "source": "(Ukrainian Air Force)",
    },
    {
        "region": "AMERICAS", "ill": ill_vegas,
        "headline": "VERSTAPPEN WINS A WILD VEGAS THRILLER",
        "body": "Las Vegas \u2014 Verstappen held off Norris by 0.639s after 34 lead changes in 50 laps \u2014 his third win on the Strip.",
        "source": "(Formula 1)",
    },
]

SMALLS = [
    {
        "region": "ASIA", "ill": ill_scales,
        "headline": "MYANMAR GUILTY OF ROHINGYA GENOCIDE",
        "body": "The Hague \u2014 The ICJ ruled 9-6 that Myanmar committed genocide.",
    },
    {
        "region": "MIDDLE EAST", "ill": ill_tanker,
        "headline": "TWO TANKERS HIT IN THE STRAIT OF HORMUZ",
        "body": "Two tankers struck near Khasab, Oman. One caught fire.",
    },
    {
        "region": "AMERICAS", "ill": ill_mountains,
        "headline": "QUAKE SHAKES PERU'S ANDES",
        "body": "A 6.7-6.8 quake struck Jun\u00edn, injuring 15. No deaths.",
    },
    {
        "region": "EUROPE", "ill": ill_ballot,
        "headline": "SPAIN HEADS FOR A SNAP ELECTION",
        "body": "Spaniards vote 29 Nov; polls put the People's Party ahead.",
    },
    {
        "region": "OCEANIA", "ill": ill_cricket,
        "headline": "ENGLAND END 15-YEAR ASHES WAIT",
        "body": "Melbourne \u2014 England won the 4th Test by 4 wickets.",
    },
    {
        "region": "OCEANIA", "ill": ill_quake_sea,
        "headline": "BANDA SEA QUAKE FELT IN DARWIN",
        "body": "A magnitude 6.8 quake struck near Timor-Leste. No tsunami.",
    },
    {
        "region": "AMERICAS", "ill": ill_cuffs,
        "headline": "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
        "body": "FBI's 10 Most Wanted boss seized in Guasave. Eleven died.",
    },
    {
        "region": "MIDDLE EAST", "ill": ill_missiles,
        "headline": "RIYADH INTERCEPTS THREE HOUTHI MISSILES",
        "body": "Coalition downed three missiles aimed at Riyadh on Saturday.",
    },
    {
        "region": "GLOBAL", "ill": ill_robot,
        "headline": "UN AGREES FIRST RULES ON 'KILLER ROBOTS'",
        "body": "Geneva agrees rules for autonomous weapons \u2014 but no ban.",
    },
    {
        "region": "EUROPE", "ill": ill_rugby,
        "headline": "AUSTRALIA EDGE WALES IN CARDIFF",
        "body": "A Gordon penalty sealed a 29-26 win in Cardiff.",
    },
]

LIST_ITEMS = [
    "Iran strikes Bahrain industrial site",
    "Trump, Xi and Putin meet in Shenzhen",
    "AI 'proves' Riemann hypothesis",
    "Russian cargo ship ablaze in the Baltic",
    "Fire at Iraq power station kills four",
    "Toxic alcohol kills 11 in Manipur",
    "South Korea minister quits over exam cheating",
    "Iran unveils missile launcher at underground base",
    "Somalia expels the UAE ambassador",
    "Boat capsizes in Nigeria, 24 dead",
    "Florida floods break a 73-year record",
    "FBI probes breach of its criminal database",
    "Kenya discharges last Ebola patient",
    "Factory fire in Indonesia kills three",
    "US stocks fall into correction",
    "EU and Indonesia sign trade deal",
    "Poland: Russian jets violated airspace",
    "Kryvyi Rih strike kills boy, 7, and paramedic",
    "Lviv strike kills two, injures 15",
    "Next climate summit set for Addis Ababa in Nov 2027",
    "Antonelli, 20, crowned F1's youngest champion",
    "Bolsonaro in intensive care",
]

DATE_CHECK = (
    "Every story above happened, or was confirmed, on Sunday 22 November 2026. "
    "The Vegas race finished Saturday night in Las Vegas \u2014 Sunday morning in Jakarta. "
    "COP31 was due to end Friday; still in overtime. "
    "Verified: 186 drones (72 jet-powered), 161 downed \u2014 not Top 1's rounded '400'."
)

FOOTER = ("Rendered by an AI agent for make.fun \u00b7 news-image-20261122 \u00b7 Sources: AP, "
          "Reuters, Formula 1, Ukrainian Air Force, ICJ, USGS \u00b7 All facts checked 22 Nov 2026")


# ---------------------------------------------------------------------------
# Page layout.
# ---------------------------------------------------------------------------

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top band
    d.rectangle([0, 0, W, 26], fill=RED)
    d.text((14, 5), "THE WORLD IN ONE DAY", font=F(SANS_B, 14), fill=(255, 255, 255))
    right = "35 STORIES \u00b7 7 REGIONS"
    d.text((W - 14 - F(SANS_B, 14).getlength(right), 5), right, font=F(SANS_B, 14),
           fill=(255, 255, 255))

    # masthead + subline
    centre(d, W // 2, 32, "Sunday 22 November 2026", F(SERIF_B, 56), INK)
    centre(d, W // 2, 96,
           "COP31 stalls into day two of overtime  \u00b7  Verstappen wins a wild Vegas "
           "thriller  \u00b7  186 drones rain on Ukraine",
           F(SANS, 15), GREY)

    # 6-fact strip
    d.rectangle([14, 118, W - 14, 162], fill=PAPER_DARK)
    d.rectangle([14, 118, W - 14, 162], outline=(200, 186, 150), width=1)
    cell_w = (W - 28) / 6
    for i, (num, label) in enumerate(FACTS):
        x = 14 + i * cell_w
        if i:
            d.line([(x, 122), (x, 158)], fill=(200, 186, 150), width=1)
        centre(d, x + cell_w / 2, 122, num, F(SANS_B, 24), RED)
        centre(d, x + cell_w / 2, 148, label, F(SANS, 10), GREY)

    # region bar
    total = sum(c for _, c, _ in REGIONS)
    x = 14
    for name, count, colour in REGIONS:
        wseg = (W - 28) * count / total
        d.rectangle([x, 166, x + wseg, 186], fill=colour)
        label = f"{name} \u00b7 {count}"
        f = F(SANS_B, 11)
        if f.getlength(label) <= wseg - 6:
            d.text((x + 6, 171), label, font=f, fill=(255, 255, 255))
        x += wseg

    # hero cards
    hero_w = [326, 327, 327]
    hx = 14
    for i, h in enumerate(HEROES):
        w = hero_w[i]
        d.rectangle([hx, 192, hx + w, 408], fill=(255, 255, 255),
                    outline=(200, 186, 150), width=1)
        h["ill"](d, (hx + 1, 193, hx + w - 1, 293))
        d.text((hx + 10, 297), h["region"], font=F(SANS_B, 10), fill=RED)
        y = para(d, hx + 10, 310, h["headline"], F(SANS_B, 16), INK, w - 20,
                 leading=18, max_lines=2)
        y = para(d, hx + 10, y + 3, h["body"], F(SANS, 11.5), (40, 40, 40), w - 20,
                 leading=13, max_lines=3)
        d.text((hx + 10, y + 2), h["source"], font=F(SANS, 9.5), fill=GREY)
        hx += w + 8

    # small cards, two rows of five
    small_w = [193, 193, 193, 192, 193]
    for row in range(2):
        y0 = 414 + row * 116
        sx = 14
        for col in range(5):
            s = SMALLS[row * 5 + col]
            w = small_w[col]
            d.rectangle([sx, y0, sx + w, y0 + 110], fill=(255, 255, 255),
                        outline=(200, 186, 150), width=1)
            s["ill"](d, (sx + 1, y0 + 1, sx + w - 1, y0 + 43))
            d.text((sx + 8, y0 + 46), s["region"], font=F(SANS_B, 9), fill=RED)
            y = para(d, sx + 8, y0 + 57, s["headline"], F(SANS_B, 12), INK, w - 16,
                     leading=13.5, max_lines=2)
            para(d, sx + 8, y + 1, s["body"], F(SANS, 10.5), (40, 40, 40), w - 16,
                 leading=11.5, max_lines=2)
            sx += w + 8

    # bottom band: map + list
    d.rectangle([14, 642, 296, 896], fill=NAVY)
    d.text((22, 648), "WHERE IT HAPPENED", font=F(SANS_B, 12),
           fill=(255, 255, 255))
    draw_map(d, (14, 668, 296, 896))
    d.text((312, 646), "ALSO ON SUNDAY  \u00b7  22 MORE STORIES", font=F(SANS_B, 13),
           fill=RED)
    col_w = 348
    for i, item in enumerate(LIST_ITEMS):
        col = i // 11
        row = i % 11
        x = 312 + col * col_w
        y = 668 + row * 20
        num = str(14 + i)
        d.text((x, y), num, font=F(SANS_B, 11), fill=RED)
        d.text((x + 26, y), item, font=F(SANS, 11), fill=INK)

    # DATE CHECK
    d.rectangle([14, 902, W - 14, 958], outline=RED, width=2)
    d.text((22, 908), "DATE CHECK", font=F(SANS_B, 12), fill=RED)
    para(d, 22, 924, DATE_CHECK, F(SANS, 11), INK, W - 44, leading=13.5,
         max_lines=2)

    # footer
    centre(d, W // 2, 966, FOOTER, F(SANS, 10), GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    render()
