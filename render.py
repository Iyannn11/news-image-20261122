#!/usr/bin/env python3
"""Render the R4 news broadsheet: 35 verified stories, Sunday 22 November 2026.

Fresh code, written from the design spec. Layout (1024x1024, roomier than the
50-story edition on purpose): red header, serif masthead, deck, 6-fact strip,
3 big cards, 2 rows of 5 small cards, a proper-aspect world map strip with a
region tally + DATE CHECK panel, and a 22-item list in 2 columns.
Deterministic: fixed fonts, fixed strings, no timestamps, no randomness.
"""
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "stories.json").read_text())

W, H = 1024, 1024
PAPER = (253, 248, 238)
INK = (28, 26, 23)
RED = (180, 35, 24)
MUTED = (107, 100, 90)
CARD = (255, 255, 255)
CARD_BORDER = (221, 213, 195)
OCEAN = (233, 238, 242)
LAND = (216, 210, 189)
LAND_LINE = (179, 169, 141)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y, len(lines)


# ---------------------------------------------------------------- continents
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 26), (-85, 30), (-90, 21), (-95, 19), (-97, 26), (-105, 23),
     (-110, 29), (-117, 33), (-125, 40), (-125, 49), (-135, 58),
     (-155, 60), (-165, 60)],
    # South America
    [(-80, 10), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-40, -5),
     (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-55, -35), (-65, -40),
     (-68, -50), (-70, -55), (-73, -45), (-73, -35), (-72, -20), (-77, -12),
     (-80, -3), (-81, 5)],
    # Africa
    [(-17, 15), (-10, 30), (-5, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (43, 11), (51, 10), (40, 0), (40, -10), (35, -18), (32, -26),
     (26, -33), (18, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 4),
     (-13, 8), (-17, 12)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53), (8, 57),
     (10, 59), (5, 60), (12, 56), (18, 56), (21, 55), (24, 58), (28, 60),
     (30, 62), (25, 65), (20, 70), (15, 68), (10, 62), (5, 58), (0, 55),
     (-5, 50), (-9, 43), (-10, 37)],
    # Asia
    [(30, 62), (40, 68), (55, 69), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (162, 56), (156, 51),
     (142, 45), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38),
     (120, 32), (115, 23), (108, 18), (105, 10), (100, 8), (98, 15),
     (95, 16), (92, 21), (88, 22), (85, 19), (80, 15), (77, 8), (74, 20),
     (70, 23), (66, 25), (61, 25), (57, 26), (52, 28), (50, 30), (48, 30),
     (44, 29), (40, 32), (36, 36), (33, 36), (30, 36), (27, 37), (26, 40),
     (28, 45), (30, 50), (35, 55), (40, 60)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41),
     (143, 43), (145, 44), (142, 44), (140, 40), (137, 37), (133, 35),
     (130, 33)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (137, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -11), (140, -17),
     (136, -15), (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
     (118, -20), (114, -21)],
]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 0

    # ---- red header bar -------------------------------------------------
    d.rectangle([0, 0, W, 30], fill=RED)
    f_head_l = font(F_SANS_B, 17)
    f_head_r = font(F_SANS_B, 15)
    d.text((24, 6), DATA["edition"], font=f_head_l, fill=(255, 255, 255))
    right = DATA["header_counts"]
    d.text((W - 24 - d.textlength(right, font=f_head_r), 7), right,
           font=f_head_r, fill=(255, 255, 255))
    y = 34

    # ---- masthead --------------------------------------------------------
    f_mast = font(F_SERIF_B, 56)
    mast = DATA["date"]
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, y), mast,
           font=f_mast, fill=INK)
    y += 66

    # ---- deck ------------------------------------------------------------
    f_deck = font(F_SERIF_I, 20)
    deck = DATA["deck"]
    d.text(((W - d.textlength(deck, font=f_deck)) / 2, y), deck,
           font=f_deck, fill=(74, 68, 60))
    y += 24 + 4

    # ---- 6-fact strip ----------------------------------------------------
    f_fact_lab = font(F_SANS_B, 11)
    f_fact = font(F_SANS, 12)
    cell_w, cell_h, gap = 156, 60, 8
    fx = 24
    region_colours = {r[0]: r[2] for r in DATA["region_counts"]}
    fact_colours = ["#1f4e79", "#be185d", "#7e22ce", "#b45309", "#be185d",
                    "#1f4e79"]
    for i, fact in enumerate(DATA["facts"]):
        x = fx + i * (cell_w + gap)
        d.rectangle([x, y, x + cell_w, y + cell_h], fill=CARD,
                    outline=CARD_BORDER)
        d.rectangle([x, y, x + cell_w, y + 3],
                    fill=fact_colours[i])
        d.text((x + 8, y + 8), fact["label"], font=f_fact_lab,
               fill=fact_colours[i])
        lines = wrap(d, fact["text"], f_fact, cell_w - 16)
        assert len(lines) <= 2, f"fact {i} wraps to {len(lines)} lines"
        yy = y + 26
        for ln in lines:
            d.text((x + 8, yy), ln, font=f_fact, fill=INK)
            yy += 15
    y += cell_h + 4

    # ---- 3 big cards -----------------------------------------------------
    big_h = 200
    bw, bgap = 320, 8
    f_kick = font(F_SANS_B, 12)
    f_big_head = font(F_SANS_B, 26)
    f_big_body = font(F_SANS, 15)
    f_big_tag = font(F_SANS, 12)
    for i, story in enumerate(DATA["big"]):
        x = 24 + i * (bw + bgap)
        d.rectangle([x, y, x + bw, y + big_h], fill=CARD,
                    outline=CARD_BORDER)
        d.rectangle([x, y, x + bw, y + 6], fill=story["color"])
        yy = y + 14
        d.text((x + 14, yy), story["kicker"], font=f_kick,
               fill=story["color"])
        yy += 20
        yy, n_head = draw_wrapped(d, x + 14, yy, story["head"], f_big_head,
                                  bw - 28, INK, 31)
        assert n_head <= 2, f"big head {i} wraps to {n_head}"
        yy += 4
        yy, n_body = draw_wrapped(d, x + 14, yy, story["body"], f_big_body,
                                  bw - 28, (58, 54, 48), 19)
        assert n_body <= 4, f"big body {i} wraps to {n_body}"
        d.text((x + 14, y + big_h - 22), story["tag"], font=f_big_tag,
               fill=MUTED)
    y += big_h + 4

    # ---- 2 rows of 5 small cards ----------------------------------------
    small_h = 126
    sw, sgap = 188, 8
    f_tag = font(F_SANS_B, 11)
    f_sm_head = font(F_SANS_B, 15)
    f_sm_body = font(F_SANS, 12)
    for row in range(2):
        for col in range(5):
            story = DATA["small"][row * 5 + col]
            x = 24 + col * (sw + sgap)
            yy = y + row * (small_h + 8)
            d.rectangle([x, yy, x + sw, yy + small_h], fill=CARD,
                        outline=CARD_BORDER)
            d.rectangle([x, yy, x + sw, yy + 3], fill=story["color"])
            ty = yy + 10
            tag = f"{story['region']} · {story.get('loc_name', '')}".strip(" ·")
            assert d.textlength(tag, font=f_tag) <= sw - 20, \
                f"small tag {story['n']} too wide: {tag}"
            d.text((x + 10, ty), tag, font=f_tag, fill=story["color"])
            ty += 17
            ty, n_head = draw_wrapped(d, x + 10, ty, story["head"],
                                      f_sm_head, sw - 20, INK, 18)
            assert n_head <= 2, f"small head {story['n']} wraps to {n_head}"
            ty += 3
            _, n_body = draw_wrapped(d, x + 10, ty, story["body"],
                                     f_sm_body, sw - 20, (58, 54, 48), 15)
            assert n_body <= 3, f"small body {story['n']} wraps to {n_body}"
    y += 2 * small_h + 8 + 4

    # ---- map label -------------------------------------------------------
    f_map_lab = font(F_SANS_B, 13)
    d.text((24, y), "WHERE IT HAPPENED", font=f_map_lab, fill=INK)
    y += 18

    # ---- map strip: proper-aspect world map + side panel -----------------
    map_h = 136
    map_w = 377  # 377/136 = 2.77, matches 360 lon / 130 lat
    mx, my = 24, y
    d.rectangle([mx, my, mx + map_w, my + map_h], fill=OCEAN,
                outline=CARD_BORDER)

    def proj(lon, lat):
        px = mx + (lon + 180.0) / 360.0 * map_w
        py = my + (75.0 - lat) / 130.0 * map_h
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=LAND_LINE)
    for loc in DATA["map_locations"]:
        px, py = proj(loc["lon"], loc["lat"])
        r = 4
        d.ellipse([px - r, py - r, px + r, py + r], fill=loc["color"],
                  outline=(255, 255, 255), width=1)

    # side panel: region tally + DATE CHECK
    px0 = mx + map_w + 16
    px1 = W - 24
    f_tally_lab = font(F_SANS_B, 12)
    f_tally = font(F_SANS, 13)
    d.text((px0, my + 2), "STORIES BY REGION", font=f_tally_lab, fill=INK)
    ty = my + 24
    col_w = (px1 - px0) // 2
    for i, (name, count, colour) in enumerate(DATA["region_counts"]):
        cx = px0 + (i % 2) * col_w
        cy = ty + (i // 2) * 18
        d.ellipse([cx, cy + 3, cx + 9, cy + 12], fill=colour)
        d.text((cx + 14, cy), f"{name} · {count}", font=f_tally,
               fill=INK)
    dc_y = ty + 4 * 18 + 8
    dc_h = my + map_h - dc_y
    assert dc_h >= 32, f"DATE CHECK box too short: {dc_h}"
    d.rectangle([px0, dc_y, px1, dc_y + dc_h], outline=RED, width=2)
    f_dc = font(F_SANS, 12)
    dc_lines = wrap(d, DATA["date_check"], f_dc, px1 - px0 - 20)
    assert len(dc_lines) <= 2, f"DATE CHECK wraps to {len(dc_lines)}"
    dyy = dc_y + 8
    for ln in dc_lines:
        d.text((px0 + 10, dyy), ln, font=f_dc, fill=INK)
        dyy += 14
    # red DATE CHECK label on the box's top edge
    f_dc_lab = font(F_SANS_B, 11)
    lab = " DATE CHECK "
    lw = d.textlength(lab, font=f_dc_lab)
    d.rectangle([px0 + 12, dc_y - 8, px0 + 12 + lw, dc_y + 6], fill=RED)
    d.text((px0 + 12, dc_y - 8), lab, font=f_dc_lab, fill=(255, 255, 255))
    y = my + map_h + 4

    # ---- list header -----------------------------------------------------
    f_list_head = font(F_SANS_B, 14)
    d.text((24, y), "ALSO ON SUNDAY · 22 MORE STORIES", font=f_list_head,
           fill=INK)
    y += 18 + 2

    # ---- 22-item list, 2 columns ----------------------------------------
    f_list_b = font(F_SANS_B, 13)
    f_list = font(F_SANS, 13)
    col_x = [24, 512]
    col_w = 488
    row_h = 15
    for i, item in enumerate(DATA["list"]):
        cx = col_x[i // 11]
        cy = y + (i % 11) * row_h
        head = f"{item['n']}. {item['label']} — "
        hw = d.textlength(head, font=f_list_b)
        assert hw + d.textlength(item["clause"], font=f_list) <= col_w, \
            f"list item {item['n']} too wide"
        d.text((cx, cy), head, font=f_list_b, fill=INK)
        d.text((cx + hw, cy), item["clause"], font=f_list,
               fill=(58, 54, 48))
    y += 11 * row_h + 4

    # ---- footer ----------------------------------------------------------
    f_foot = font(F_SANS, 11)
    foot = DATA["footer"]
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, y), foot,
           font=f_foot, fill=MUTED)
    y += 16
    assert y <= H, f"layout overflows: y={y}"

    out = HERE / "entry.png"
    img.save(out, "PNG", optimize=True)
    raw = out.read_bytes()
    print(f"entry.png: {len(raw)} bytes, "
          f"sha256 {hashlib.sha256(raw).hexdigest()}")
    print(f"layout ends at y={y} of {H}")
    return out


if __name__ == "__main__":
    render()
