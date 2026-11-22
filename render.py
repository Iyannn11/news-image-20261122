#!/usr/bin/env python3
"""Render the News 22 Round 3 broadsheet (50 stories) to entry.png.

Reads stories.json from this directory, draws a 1024x1024 PNG with PIL.
Deterministic: fixed layout, fixed fonts, no timestamps, no randomness.
"""
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
PAPER = (253, 249, 240)
INK = (17, 17, 17)
RED = (200, 16, 46)
RED_DARK = (160, 12, 36)
MUTED = (90, 84, 74)
LINE = (40, 40, 40)
CARD = (255, 255, 255)
OCEAN = (220, 234, 245)
LAND = (232, 223, 204)
LAND_EDGE = (178, 168, 140)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF = FONT_DIR / "DejaVuSerif.ttf"
SERIF_B = FONT_DIR / "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR / "DejaVuSans.ttf"
SANS_B = FONT_DIR / "DejaVuSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(str(path), size)


def wrap(text, font, max_w):
    """Word-wrap text to a list of lines fitting max_w pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if font.getlength(trial) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_lines(dr, x, y, lines, font, fill, leading):
    for i, ln in enumerate(lines):
        dr.text((x, y + i * leading), ln, font=font, fill=fill)
    return y + len(lines) * leading


def region_color(region, counts):
    for name, _n, col in counts:
        if name == region:
            return col
    return "#333333"


# Simplified continent outlines (lon, lat) — stylised world map.
CONTINENTS = [
    [(-168, 66), (-155, 58), (-140, 60), (-128, 52), (-124, 42), (-120, 34),
     (-114, 29), (-108, 24), (-100, 18), (-93, 16), (-87, 13), (-82, 9),
     (-79, 9), (-83, 15), (-87, 20), (-91, 19), (-97, 26), (-94, 30),
     (-88, 30), (-82, 28), (-80, 32), (-76, 35), (-74, 40), (-70, 42),
     (-66, 45), (-60, 47), (-56, 50), (-62, 55), (-68, 58), (-75, 62),
     (-82, 66), (-92, 66), (-102, 68), (-115, 69), (-128, 70), (-142, 70),
     (-155, 71), (-165, 68)],
    [(-79, 9), (-75, 11), (-68, 11), (-60, 7), (-53, 4), (-50, 0),
     (-44, -3), (-38, -6), (-35, -9), (-38, -15), (-40, -22), (-46, -26),
     (-52, -31), (-57, -35), (-62, -40), (-66, -46), (-69, -52), (-71, -50),
     (-73, -44), (-73, -37), (-71, -30), (-70, -22), (-76, -15), (-80, -6),
     (-81, 0)],
    [(-10, 36), (-9, 43), (-2, 44), (-4, 48), (0, 51), (4, 53), (8, 56),
     (10, 59), (16, 56), (20, 55), (23, 58), (20, 62), (14, 65), (20, 68),
     (26, 71), (31, 70), (38, 68), (46, 68), (54, 68), (62, 69), (68, 70),
     (62, 72), (55, 70), (48, 67), (44, 63), (40, 58), (36, 54), (32, 50),
     (30, 47), (27, 44), (23, 41), (20, 40), (17, 41), (13, 44), (8, 44),
     (4, 43), (0, 39), (-2, 37), (-6, 36)],
    [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-14, 11),
     (-12, 8), (-8, 5), (-2, 5), (3, 6), (8, 4), (12, 0), (13, -6),
     (12, -12), (13, -18), (15, -23), (17, -29), (19, -34), (25, -34),
     (30, -30), (34, -26), (37, -21), (40, -14), (41, -8), (44, -2),
     (48, 0), (51, 7), (50, 11), (44, 11), (41, 15), (38, 19), (36, 23),
     (34, 28), (31, 31), (26, 33), (20, 34), (14, 34), (8, 34), (2, 35)],
    [(28, 41), (33, 42), (38, 44), (43, 45), (48, 46), (53, 47), (58, 48),
     (63, 48), (68, 49), (73, 50), (78, 51), (83, 52), (88, 53), (93, 55),
     (98, 57), (103, 59), (108, 60), (113, 62), (118, 63), (123, 62),
     (128, 61), (133, 60), (138, 58), (141, 53), (141, 47), (137, 43),
     (132, 42), (128, 39), (125, 39), (121, 38), (119, 33), (117, 28),
     (113, 23), (110, 20), (107, 16), (105, 10), (103, 7), (100, 8),
     (98, 12), (95, 16), (92, 21), (89, 22), (86, 20), (83, 18), (80, 14),
     (77, 8), (76, 11), (73, 17), (70, 21), (67, 24), (63, 25), (59, 25),
     (56, 26), (57, 23), (59, 20), (55, 17), (51, 14), (48, 13), (45, 12),
     (43, 13), (44, 16), (46, 20), (48, 24), (50, 27), (48, 30), (44, 32),
     (40, 35), (36, 36), (33, 36), (30, 37)],
    [(114, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (140, -14), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14),
     (122, -17), (118, -20)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (178, -37),
     (175, -40), (172, -43), (169, -46)],
    [(-55, 60), (-45, 60), (-40, 64), (-30, 68), (-20, 70), (-25, 76),
     (-40, 80), (-55, 76), (-60, 70)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-2, 50)],
]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (82.0 - lat) / 140.0 * (y1 - y0)
    return x, y


def draw_globe(dr, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    r = min(x1 - x0, y1 - y0) / 2 - 2
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(66, 135, 200),
               outline=(31, 78, 121), width=2)
    dr.ellipse([cx - r * 0.45, cy - r * 0.55, cx + r * 0.25, cy - r * 0.05],
               fill=(46, 139, 87))
    dr.ellipse([cx - r * 0.2, cy + r * 0.15, cx + r * 0.55, cy + r * 0.6],
               fill=(46, 139, 87))
    dr.ellipse([cx - r * 0.7, cy + r * 0.25, cx - r * 0.3, cy + r * 0.55],
               fill=(46, 139, 87))
    dr.ellipse([cx + r * 0.55, cy - r * 0.75, cx + r * 0.95, cy - r * 0.35],
               fill=(245, 200, 80))


def draw_race(dr, box):
    x0, y0, x1, y1 = box
    dr.rectangle([x0, y0, x1, y1], fill=(214, 231, 245))
    dr.rectangle([x0, y0 + 26, x1, y1 - 2], fill=(52, 58, 66))
    for dx in range(0, int(x1 - x0), 26):
        dr.rectangle([x0 + dx + 4, (y0 + y1) / 2 - 1, x0 + dx + 18,
                      (y0 + y1) / 2 + 1], fill=(255, 255, 255))
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2 + 2
    dr.rounded_rectangle([cx - 46, cy - 8, cx + 46, cy + 6], radius=5,
                         fill=(200, 16, 46))
    dr.rounded_rectangle([cx - 16, cy - 17, cx + 14, cy - 6], radius=4,
                         fill=(160, 12, 36))
    dr.rectangle([cx - 10, cy - 15, cx + 8, cy - 8], fill=(180, 220, 245))
    dr.ellipse([cx - 38, cy + 4, cx - 22, cy + 14], fill=(12, 12, 12))
    dr.ellipse([cx + 22, cy + 4, cx + 38, cy + 14], fill=(12, 12, 12))
    dr.ellipse([cx - 34, cy + 7, cx - 26, cy + 11], fill=(200, 200, 200))
    dr.ellipse([cx + 26, cy + 7, cx + 34, cy + 11], fill=(200, 200, 200))
    dr.ellipse([x0 + 12, y0 + 4, x0 + 26, y0 + 18], fill=(250, 210, 90))


def draw_city(dr, box):
    x0, y0, x1, y1 = box
    dr.rectangle([x0, y0, x1, y1], fill=(24, 32, 52))
    for sx, sy in [(x0 + 30, y0 + 10), (x0 + 90, y0 + 16), (x0 + 150, y0 + 8)]:
        dr.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    base = y1 - 4
    heights = [26, 40, 18, 34, 44, 22, 30, 38, 16, 28]
    bw = (x1 - x0 - 12) / len(heights)
    for i, hh in enumerate(heights):
        bx = x0 + 6 + i * bw
        dr.rectangle([bx, base - hh, bx + bw - 3, base], fill=(12, 18, 34))
        for wy in range(3):
            dr.rectangle([bx + 3, base - hh + 5 + wy * 9, bx + 7,
                          base - hh + 9 + wy * 9], fill=(250, 200, 90))
    for bx, by, r in [(x0 + 60, y0 + 12, 10), (x0 + 190, y0 + 8, 12),
                      (x0 + 260, y0 + 16, 9)]:
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            dr.line([(bx, by), (bx + r * math.cos(rad), by + r * math.sin(rad))],
                    fill=(255, 140, 40), width=2)
        dr.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(255, 180, 60))


def main():
    data = json.loads((HERE / "stories.json").read_text(encoding="utf-8"))
    counts = data["region_counts"]
    img = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(img)
    dr.rectangle([4, 4, W - 5, H - 5], outline=INK, width=2)

    # ---- header ----
    dr.text((14, 12), data["edition"], font=f(SANS_B, 15), fill=RED)
    hc = data["header_counts"]
    w = dr.textlength(hc, font=f(SANS_B, 13))
    dr.text((W - 14 - w, 13), hc, font=f(SANS_B, 13), fill=INK)
    dr.line([(14, 40), (W - 14, 40)], fill=RED, width=2)

    # ---- masthead + deck ----
    mast = data["date"]
    mw = dr.textlength(mast, font=f(SERIF_B, 46))
    dr.text(((W - mw) / 2, 48), mast, font=f(SERIF_B, 46), fill=INK)
    deck = data["deck"]
    dw = dr.textlength(deck, font=f(SERIF, 15))
    dr.text(((W - dw) / 2, 104), deck, font=f(SERIF, 15), fill=MUTED)

    # ---- region bar ----
    parts = []
    for name, n, col in counts:
        parts.append((name, n, col))
    seg = "  ·  ".join(f"{name} {n}" for name, n, _ in parts)
    sw = dr.textlength(seg, font=f(SANS_B, 12))
    x = (W - sw) / 2
    for name, n, col in parts:
        sq = f"{name} {n}"
        dr.rectangle([x, 128, x + 9, 137], fill=col)
        dr.text((x + 13, 126), sq, font=f(SANS_B, 12), fill=INK)
        x += dr.textlength(sq, font=f(SANS_B, 12)) + 13
        if name != parts[-1][0]:
            dot = "·"
            dr.text((x, 126), dot, font=f(SANS_B, 12), fill=MUTED)
            x += dr.textlength("  ·  ", font=f(SANS_B, 12))
    dr.line([(14, 146), (W - 14, 146)], fill=LINE, width=1)

    # ---- fact strip (6 columns) ----
    fy0, fy1 = 152, 210
    col_w = (W - 28) / 6
    for i, fac in enumerate(data["facts"]):
        cx0 = 14 + i * col_w
        if i > 0:
            dr.line([(cx0 - 2, fy0 + 2), (cx0 - 2, fy1 - 2)], fill=(200, 192, 176),
                    width=1)
        dr.ellipse([cx0 + 2, fy0 + 2, cx0 + 20, fy0 + 20], fill=RED)
        num = str(fac["n"])
        nw = dr.textlength(num, font=f(SANS_B, 11))
        dr.text((cx0 + 11 - nw / 2, fy0 + 4), num, font=f(SANS_B, 11),
                fill=(255, 255, 255))
        dr.text((cx0 + 24, fy0 + 3), fac["label"], font=f(SANS_B, 11),
                fill=RED)
        lines = wrap(fac["text"], f(SANS, 10), col_w - 8)
        draw_lines(dr, cx0 + 2, fy0 + 24, lines[:3], f(SANS, 10), INK, 12)
    dr.line([(14, 214), (W - 14, 214)], fill=LINE, width=1)

    # ---- 3 big cards ----
    by0, by1 = 222, 388
    bw_ = (W - 28 - 8) / 3
    for i, card in enumerate(data["big"]):
        x0 = 14 + i * (bw_ + 4)
        x1 = x0 + bw_
        dr.rectangle([x0, by0, x1, by1], fill=CARD, outline=INK, width=1)
        dr.rectangle([x0, by0, x1, by0 + 46], fill=RED)
        lines = wrap(card["banner"], f(SANS_B, 16), bw_ - 52)
        draw_lines(dr, x0 + 8, by0 + 6, lines[:2], f(SANS_B, 16),
                   (255, 255, 255), 19)
        dr.ellipse([x1 - 36, by0 + 8, x1 - 10, by0 + 34], fill=(255, 255, 255))
        num = str(card["n"])
        nw = dr.textlength(num, font=f(SANS_B, 13))
        dr.text((x1 - 23 - nw / 2, by0 + 12), num, font=f(SANS_B, 13),
                fill=RED)
        art_box = (x0 + 4, by0 + 50, x1 - 4, by0 + 98)
        if card["art"] == "globe":
            draw_globe(dr, art_box)
        elif card["art"] == "race":
            draw_race(dr, art_box)
        else:
            draw_city(dr, art_box)
        blines = wrap(card["body"], f(SANS, 12), bw_ - 16)
        draw_lines(dr, x0 + 8, by0 + 104, blines[:3], f(SANS, 12), INK, 14)
        foot = f"No. {card['n']} · {card['place']} · {card['region']}"
        dr.text((x0 + 8, by1 - 16), foot, font=f(SANS_B, 10),
                fill=region_color(card["region"], counts))

    # ---- 10 small cards, 2 rows x 5 ----
    sw_ = (W - 28 - 16) / 5
    for row in range(2):
        y0 = 396 + row * 98
        y1 = y0 + 90
        for col in range(5):
            card = data["small"][row * 5 + col]
            x0 = 14 + col * (sw_ + 4)
            x1 = x0 + sw_
            dr.rectangle([x0, y0, x1, y1], fill=CARD, outline=INK, width=1)
            dr.rectangle([x0, y0, x1, y0 + 4],
                         fill=region_color(card["region"], counts))
            dr.ellipse([x1 - 24, y0 + 9, x1 - 8, y0 + 25], fill=RED)
            num = str(card["n"])
            nw = dr.textlength(num, font=f(SANS_B, 10))
            dr.text((x1 - 16 - nw / 2, y0 + 11), num, font=f(SANS_B, 10),
                    fill=(255, 255, 255))
            hlines = wrap(card["head"], f(SANS_B, 12), sw_ - 34)
            draw_lines(dr, x0 + 7, y0 + 9, hlines[:2], f(SANS_B, 12), INK, 14)
            blines = wrap(card["body"], f(SANS, 10), sw_ - 14)
            draw_lines(dr, x0 + 7, y0 + 40, blines[:3], f(SANS, 10), INK, 12)
            dr.text((x0 + 7, y1 - 14), card["region"], font=f(SANS_B, 9),
                    fill=region_color(card["region"], counts))

    # ---- map band ----
    dr.text((14, 600), "WHERE IT HAPPENED", font=f(SANS_B, 13), fill=INK)
    later = data["later_today"]
    lw = dr.textlength(later, font=f(SANS, 10))
    dr.text((W - 14 - lw, 602), later, font=f(SANS, 10), fill=MUTED)
    mbox = (14, 620, W - 14, 720)
    dr.rectangle(mbox, fill=OCEAN, outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mbox) for lon, lat in poly]
        dr.polygon(pts, fill=LAND, outline=LAND_EDGE)
    all_stories = data["big"] + data["small"] + data["list"]
    for st in all_stories:
        px, py = project(st["loc"][0], st["loc"][1], mbox)
        if st["n"] <= 13:
            dr.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                       outline=(255, 255, 255), width=1)
            num = str(st["n"])
            nw = dr.textlength(num, font=f(SANS_B, 8))
            dr.text((px - nw / 2, py - 5), num, font=f(SANS_B, 8),
                    fill=(255, 255, 255))
        else:
            dr.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5],
                       fill=RED_DARK)
    cap = "Red numbers 1–13 are the front-page cards; every dot is one of the 50 stories."
    cw = dr.textlength(cap, font=f(SANS, 10))
    dr.text(((W - cw) / 2, 726), cap, font=f(SANS, 10), fill=MUTED)

    # ---- ALSO ON SUNDAY list, 3 columns x 13 rows ----
    dr.text((14, 744), "ALSO ON SUNDAY · 37 MORE STORIES",
            font=f(SANS_B, 13), fill=INK)
    dr.line([(14, 762), (W - 14, 762)], fill=LINE, width=1)
    col_w = (W - 28 - 16) / 3
    for i, item in enumerate(data["list"]):
        col = i // 13
        row = i % 13
        x0 = 14 + col * (col_w + 8)
        y = 770 + row * 15.5
        dr.text((x0, y), f"{item['n']}.", font=f(SANS_B, 11), fill=RED)
        num_w = dr.textlength(f"{item['n']}. ", font=f(SANS_B, 11))
        label = item["label"] + " — "
        lw_ = dr.textlength(label, font=f(SANS_B, 11))
        dr.text((x0 + num_w, y), label, font=f(SANS_B, 11), fill=INK)
        clause = item["clause"]
        max_cw = col_w - num_w - lw_
        cf = f(SANS, 10)
        clipped = False
        while cf.getlength(clause) > max_cw and len(clause) > 4:
            clause = clause[:-4].rstrip() + "…"
            clipped = True
        if clipped:
            print(f"CLIPPED list item {item['n']}: {clause}")
        dr.text((x0 + num_w + lw_, y + 1), clause, font=cf, fill=(60, 56, 50))

    # ---- date check box + footer ----
    dr.rectangle([14, 968, W - 14, 994], outline=RED, width=2)
    dc = data["date_check"]
    dcw = dr.textlength(dc, font=f(SANS_B, 10))
    dr.text(((W - dcw) / 2, 976), dc, font=f(SANS_B, 10), fill=RED_DARK)
    foot = data["footer"]
    fw = dr.textlength(foot, font=f(SANS, 10))
    dr.text(((W - fw) / 2, 1002), foot, font=f(SANS, 10), fill=MUTED)

    out = HERE / "entry.png"
    img.save(out, format="PNG")
    print(f"wrote {out} {img.size}")


if __name__ == "__main__":
    main()
