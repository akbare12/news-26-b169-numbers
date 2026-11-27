#!/usr/bin/env python3
"""V165 news-image entry renderer (build-time only, PIL).
Layout V165: masthead + full-width HERO 1 banner + twin HERO 2/3 +
10 cards 2x5 + map spine left / ALSO right + DATE CHECK strip + footer.
Render: python3 gen.py  ->  entry.png  (1024x1024, <=1 MiB)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
FD = "/usr/share/fonts/truetype/dejavu"
def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

F_TITLE = F("DejaVuSans-Bold.ttf", 34)
F_DATE = F("DejaVuSans-Bold.ttf", 15)
F_KICK = F("DejaVuSans-Bold.ttf", 11)
F_H1 = F("DejaVuSans-Bold.ttf", 22)
F_H2 = F("DejaVuSans-Bold.ttf", 17)
F_DECK = F("DejaVuSans.ttf", 12)
F_WHY = F("DejaVuSans-Bold.ttf", 11)
F_CARD_T = F("DejaVuSans-Bold.ttf", 12)
F_CARD_D = F("DejaVuSans.ttf", 10)
F_TAG = F("DejaVuSans-Bold.ttf", 9)
F_ALSO = F("DejaVuSans.ttf", 9)
F_ALSO_B = F("DejaVuSans-Bold.ttf", 9)
F_DC = F("DejaVuSans.ttf", 11)
F_DC_B = F("DejaVuSans-Bold.ttf", 11)
F_LEG = F("DejaVuSans.ttf", 9)
F_FOOT = F("DejaVuSans.ttf", 10)
F_BADGE = F("DejaVuSans-Bold.ttf", 13)
F_PIN = F("DejaVuSans-Bold.ttf", 8)

INK = (17, 17, 17)
PAPER = (247, 243, 232)
NAVY = (14, 42, 74)
NAVY2 = (24, 68, 110)
RED = (178, 34, 34)
GOLD = (176, 132, 8)
TEAL = (13, 110, 102)
LAND = (183, 201, 143)
OCEAN = (191, 217, 232)
LINE = (120, 120, 110)

# ---------------- DATA ----------------
HERO1 = {
    "kick": "HERO 1  |  NEW YORK  |  THANKSGIVING DAY",
    "head": "Macy's 100th parade postponed \u2014 first ever over weather",
    "deck": "The centenary parade will not march today as a fierce East Coast storm hits.",
    "why": "WHY IT MATTERS: America's most-watched parade, 100 years old, halted by weather for the first time.",
    "badge": "100TH",
}
HERO2 = {
    "kick": "HERO 2  |  STRAIT OF HORMUZ  |  [CL]",
    "head": "IRGC claims two tankers hit by mines",
    "deck": "Iran's Guards say two tankers exploded and burned in the Strait, one a supertanker carrying over 2 million barrels.",
    "why": "WHY IT MATTERS: it could widen the Iran war.",
    "badge": "2M BBL",
}
assert "khasab" not in (HERO2["head"] + HERO2["deck"] + HERO2["why"]).lower(), "Khasab in hero 2"
HERO3 = {
    "kick": "HERO 3  |  MARKETS  |  TARIFFS",
    "head": "Trump tariffs: world markets rebound",
    "deck": "Europe and Asia rise as traders judge the new tariff salvo milder than feared; the levies will not stack on July's rates.",
    "why": "WHY IT MATTERS: relief after the tariff scare.",
    "badge": "14",
}

# cards: (region, title, deck(<=2 lines at 10px in 186px), tag, pin_no)
CARDS = [
    ("GAZA", "Israel kills Hamas education official", "Strike in Deir al-Balah kills Khaled Abu Nada and his wife.", "[C]", 5),
    ("KYIV", "Russian missile hits Kyiv mall", "Mall in Desnianskyi hit overnight; 7 wounded, 2 seriously.", "[C]", 4),
    ("BOGOR", "Mine flood: 13 dead, 13 missing", "Miners were ~100m underground after heavy rain; toll rises.", "[C]", 6),
    ("ISRAEL", "Judge urges dropping bribery charge", "Judge urges prosecutors to drop Case 4000, the bribery count.", "[R]", 9),
    ("N. KOREA", "Kim tours nuclear plant for arms push", "Kim visits a nuclear-materials plant, urges tactical arms.", "[C]", 10),
    ("SPACE", "SpaceX 'Starmind' 1m satellites cleared", "US clears up to 1m orbital compute modules, a space first.", "[C]", 12),
    ("BRITAIN", "UK net migration falls to 77,000", "Lowest since 1997 outside the pandemic, to June 2026.", "[C]", 8),
    ("RUSSIA", "Russia approves record budget", "Moscow signs off its biggest defence budget since Soviet era.", "[C]", 11),
    ("BANGKOK", "Blast at Bangkok oil depot injures 7", "Blast triggers evacuation alerts; fire out in 30 minutes.", "[C]", 7),
    ("GERMANY", "Two held over synagogue plot", "Iraqi suspects held in Cologne, Heidelberg.", "[C]", 9),
]

ALSO = [
    "Eisenkot seals first Israeli coalition deal [R]",
    "Merz warns Russia aims beyond Ukraine [R]",
    "Britain on alert over drone threat to airbases [R]",
    "Norse Atlantic halts all flights, warns of failure [C]",
    "Poundland in administration; 11,000 jobs at risk [C]",
    "Malaysia sues Google for $146m over bad posts [C]",
    "Kenya court halts US-backed Ebola facility [C]",
    "Belarus offers Zelensky flight to Moscow; refused [R]",
    "Kushner calls Putin a 'grandmaster of politics' [R]",
    "Estonia decides to close its border [C]",
    "Copernicus: longest stretch above 2\u00b0C warming [C]",
    "Nvidia halts AI server shipments to four nations [R]",
    "US Bitcoin ETFs: record $4.94bn Nov outflows [C]",
    "Philadelphia Thanksgiving parade cancelled [C]",
    "UKMTO 222-26: blast 50 nm W of Dubai, 25 Nov [CL]",
    "Saudi defences intercept two ballistic missiles [R]",
    "Houthis claim Ras Tanura refinery strike, 25 Nov [CL]",
    "Ukraine drones hit Savasleyka base; 5 jets hurt [R]",
    "Couple killed in Kharkiv apartment strike [C]",
    "Kryvyi Rih strike wounds 18 people [C]",
    "Kyiv attack used 113 drones overnight [C]",
    "Ukraine hits pump station 1,300 km from border [R]",
    "Cargo ship near Odesa claimed hit [CL]",
    "Russia claims Kyiv strikes hit drone sites [CL]",
    "UN rights chief warns of atrocity risk in Gaza [R]",
    "Brent crude $93.8, up 0.9% on Thursday [C]",
    "WTI crude $83.32, up 0.2% [C]",
    "Gold $3,572/oz, down 0.2% [C]",
    "Nvidia shares $149.30, down 3.91% [C]",
    "S&P 500 futures up 0.5%; Wall St shut [R]",
    "Dollar flat at 103.71 [C]",
    "OPEC+ to meet 29 Nov on 2027 output [C]",
    "NBC airs 2025 parade rerun Thu 08:30 [C]",
    "Steelers release Aaron Rodgers [C]",
    "Iran war reaches day 272 [C]",
    "Brent closed Wed at $94.61, up 3.5% [C]",
    "Thanksgiving travel hit by East Coast storm [R]",
]

DATE_CHECK = [
    "COP31 failed \u2014 22 Nov",
    "Shenzhou-24 launched \u2014 25 Nov",
    "Cairo tanker blast, 31 dead \u2014 25 Nov",
    "Cartagena hostages freed \u2014 25 Nov",
    "Australia-Solomon pact \u2014 25 Nov",
    "UK energy prices +26% \u2014 25 Nov",
    "Huawei convicted \u2014 24 Nov",
]

# pins: (no, lon, lat, label, draw_offset_px_or_None)
PINS = [
    (1, -74.0, 40.7, "New York \u2014 parade"),
    (2, -75.2, 39.95, "Philadelphia \u2014 parade"),
    (3, 56.3, 26.2, "Hormuz \u2014 tankers"),
    (4, 30.5, 50.4, "Kyiv \u2014 missile"),
    (5, 34.5, 31.5, "Gaza \u2014 airstrike"),
    (6, 106.8, -6.6, "Bogor \u2014 mine flood"),
    (7, 100.5, 13.75, "Bangkok \u2014 depot blast"),
    (8, -1.0, 52.5, "London \u2014 migration"),
    (9, 13.4, 52.5, "Berlin \u2014 plot arrests"),
    (10, 125.0, 39.5, "Pyongyang \u2014 Kim tour"),
    (11, 37.6, 55.75, "Moscow \u2014 budget"),
    (12, 51.4, 35.7, "Tehran \u2014 Iran war"),
]
PIN_OFFSET = {2: (18, 12), 11: (12, -10), 12: (-12, -14)}  # leader-line offsets

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-80, 73), (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-110, 24), (-117, 33), (-125, 40), (-125, 49), (-135, 58), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-40, 76), (-58, 76)],
    [(-80, 9), (-75, 11), (-62, 9), (-52, 5), (-40, -3), (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-73, -37), (-70, -20), (-80, -5), (-81, 3)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (28, -33), (18, -35), (12, -18), (9, 4), (-8, 5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (35, 66), (45, 68), (55, 68), (65, 69), (75, 72), (85, 75), (100, 77), (115, 73), (130, 72), (145, 72), (160, 70), (175, 66), (178, 65), (170, 60), (162, 56), (158, 52), (150, 59), (142, 55), (140, 50), (135, 43), (130, 42), (127, 40), (122, 38), (120, 32), (115, 23), (108, 18), (105, 9), (100, 7), (98, 12), (95, 16), (92, 21), (88, 22), (85, 19), (80, 13), (77, 8), (73, 16), (68, 23), (62, 25), (58, 25), (55, 26), (52, 28), (48, 30), (44, 29), (40, 31), (36, 36), (30, 36), (26, 38), (23, 36), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43), (-2, 37), (-9, 37)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (146, -19), (142, -11), (136, -12), (132, -11), (126, -14), (122, -17), (114, -21)],
    [(95, 5), (100, 0), (104, -3), (106, -6), (103, -5), (98, 2)],
    [(105, -6), (114, -7), (114, -9), (106, -8)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (116, -3), (111, -3), (109, 0)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (147, -9), (141, -8), (136, -7), (131, -3)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (142, 42), (144, 44), (141, 40), (138, 37), (134, 34), (131, 33)],
    [(44, -16), (47, -15), (50, -17), (48, -22), (45, -25), (43, -20)],
    [(33.5, 31), (34.5, 33), (35.5, 36), (36.5, 33), (35, 31)],
]

# ---------------- HELPERS ----------------
TEXT_BOXES = []   # (x0,y0,x1,y1) every drawn text bbox
ART_BOXES = []    # (x0,y0,x1,y1) scene-art rects (not chips/bands)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(d, xy, s, font, fill=INK):
    x, y = xy
    d.text((x, y), s, font=font, fill=fill)
    b = d.textbbox((x, y), s, font=font)
    TEXT_BOXES.append(b)
    return b

def text_in(d, s, font, box, fill=INK, align="left"):
    """Draw (possibly wrapped) text inside box; assert fully inside with >=2px margin."""
    x0, y0, x1, y1 = box
    lines = wrap(s, font, x1 - x0 - 4)
    y = y0 + 2
    asc = font.getbbox("Ag")[3]
    for ln in lines:
        if align == "center":
            w = font.getlength(ln)
            tx = x0 + (x1 - x0 - w) / 2
        else:
            tx = x0 + 2
        b = text(d, (tx, y), ln, font, fill)
        assert b[0] >= x0 + 1 and b[1] >= y0 + 1 and b[2] <= x1 - 1 and b[3] <= y1 - 1, \
            "text outside box: %r %s vs %s" % (ln, b, box)
        y += asc + 3
    assert y - 3 <= y1 - 1, "text overflows box bottom: %r" % s
    return lines

def chip(d, box, fill, outline=None):
    d.rounded_rectangle(box, radius=6, fill=fill, outline=outline or fill, width=1)

def check_no_art_overlap():
    for tb in TEXT_BOXES:
        for ab in ART_BOXES:
            ox = min(tb[2], ab[2]) - max(tb[0], ab[0])
            oy = min(tb[3], ab[3]) - max(tb[1], ab[1])
            assert not (ox > 0 and oy > 0), "text/art overlap %s vs %s" % (tb, ab)

def lonlat_to_xy(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 170.0) / 360.0 * (x1 - x0)
    y = y0 + (85.0 - lat) / 145.0 * (y1 - y0)
    return x, y

F_WHY2 = F("DejaVuSans-Bold.ttf", 10)
F_DECK11 = F("DejaVuSans.ttf", 11)

def panel(d, box, fill=(255, 255, 255), outline=LINE, width=1):
    d.rectangle(box, fill=fill, outline=outline, width=width)

def draw_balloon_scene(d, box):
    x0, y0, x1, y1 = box
    ART_BOXES.append(box)
    d.rectangle(box, fill=(135, 180, 215))
    d.ellipse((x0 + 30, y0 + 8, x0 + 150, y0 + 78), fill=(178, 34, 34), outline=(255, 255, 255), width=2)
    d.ellipse((x0 + 150, y0 + 8, x0 + 230, y0 + 78), fill=(240, 230, 200), outline=(255, 255, 255), width=2)
    for cx, cy in [(x0 + 200, y0 + 20), (x0 + 60, y0 + 90), (x0 + 210, y0 + 95)]:
        d.ellipse((cx, cy, cx + 55, cy + 16), fill=(245, 245, 245))
    for i in range(9):
        rx = x0 + 15 + i * 28
        d.line((rx, y0 + 95, rx - 10, y0 + 115), fill=(220, 230, 240), width=2)
    d.rectangle((x0, y1 - 14, x1, y1), fill=(90, 95, 100))

def draw_tanker_scene(d, box):
    x0, y0, x1, y1 = box
    ART_BOXES.append(box)
    d.rectangle(box, fill=(70, 110, 140))
    d.rectangle((x0, y1 - 42, x1, y1), fill=(40, 75, 100))
    d.rectangle((x0 + 18, y0 + 58, x0 + 122, y0 + 84), fill=(40, 40, 40))
    d.rectangle((x0 + 18, y0 + 58, x0 + 122, y0 + 66), fill=(178, 34, 34))
    d.polygon([(x0 + 40, y0 + 58), (x0 + 55, y0 + 28), (x0 + 70, y0 + 58)], fill=(230, 140, 30))
    d.polygon([(x0 + 70, y0 + 58), (x0 + 82, y0 + 36), (x0 + 95, y0 + 58)], fill=(240, 200, 40))
    for cx, cy, r in [(x0 + 55, y0 + 22, 9), (x0 + 80, y0 + 26, 7)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(120, 120, 120))
    for cx, cy in [(x0 + 125, y0 + 95), (x0 + 140, y0 + 100)]:
        d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=(30, 30, 30))
        for k in range(8):
            import math as _m
            a = k * _m.pi / 4
            d.line((cx, cy, cx + 9 * _m.cos(a), cy + 9 * _m.sin(a)), fill=(30, 30, 30), width=1)

def draw_chart_scene(d, box):
    x0, y0, x1, y1 = box
    ART_BOXES.append(box)
    d.rectangle(box, fill=(235, 242, 235))
    for i, h in enumerate([18, 26, 22, 34, 30, 44, 40, 56]):
        bx = x0 + 12 + i * 16
        d.rectangle((bx, y1 - 14 - h, bx + 11, y1 - 14), fill=(13, 110, 102) if i >= 5 else (120, 160, 150))
    pts = [(x0 + 12, y1 - 30), (x0 + 44, y1 - 44), (x0 + 76, y1 - 38), (x0 + 108, y1 - 56), (x0 + 132, y1 - 66)]
    d.line(pts, fill=(178, 34, 34), width=3, joint="curve")
    d.line((x0 + 8, y1 - 14, x1 - 8, y1 - 14), fill=INK, width=1)

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # ---- masthead (solid band, not art) ----
    d.rectangle((0, 0, W, 68), fill=NAVY)
    text(d, (16, 8), "THE WORLD IN ONE DAY", F_TITLE, (255, 255, 255))
    text(d, (16, 48), "50 stories  |  10 regions  |  one Thursday", F_DATE, (200, 215, 230))
    dt = "THURSDAY 26 NOVEMBER 2026"
    dw = F_DATE.getlength(dt)
    text(d, (W - 16 - dw, 48), dt, F_DATE, (255, 220, 90))
    # ---- HERO 1 banner ----
    panel(d, (8, 74, 1016, 194))
    draw_balloon_scene(d, (8, 74, 300, 194))
    chip(d, (918, 78, 1010, 100), GOLD)
    text(d, (930, 81), "100TH", F_BADGE, (255, 255, 255))
    text_in(d, HERO1["kick"], F_KICK, (312, 78, 916, 96), RED)
    text_in(d, HERO1["head"], F_H1, (312, 96, 1010, 156))
    text_in(d, HERO1["deck"], F_DECK, (312, 156, 1010, 176))
    text_in(d, HERO1["why"], F_WHY, (312, 176, 1010, 194), TEAL)
    # ---- HERO 2 / 3 twin ----
    for hero, box, scene in ((HERO2, (8, 200, 508, 320), draw_tanker_scene),
                             (HERO3, (516, 200, 1016, 320), draw_chart_scene)):
        x0, y0, x1, y1 = box
        panel(d, box)
        scene(d, (x0, y0, x0 + 140, y1))
        tx = x0 + 148
        chip(d, (x1 - 92, y0 + 4, x1 - 6, y0 + 26), NAVY2)
        bw = F_BADGE.getlength(hero["badge"])
        text(d, (x1 - 49 - bw / 2, y0 + 7), hero["badge"], F_BADGE, (255, 255, 255))
        text_in(d, hero["kick"], F_KICK, (tx, y0 + 4, x1 - 96, y0 + 22), RED)
        text_in(d, hero["head"], F_H2, (tx, y0 + 22, x1 - 6, y0 + 68))
        text_in(d, hero["deck"], F_DECK11, (tx, y0 + 68, x1 - 6, y0 + 100))
        text_in(d, hero["why"], F_WHY2, (tx, y0 + 100, x1 - 6, y1 - 2), TEAL)
    # ---- 10 cards 2x5 ----
    for i, (region, title, deck, tag, _pin) in enumerate(CARDS):
        cx = 8 + (i % 5) * 202
        cy = 326 + (i // 5) * 110
        panel(d, (cx, cy, cx + 198, cy + 104))
        text_in(d, region, F_TAG, (cx + 6, cy + 4, cx + 120, cy + 20), RED)
        d.ellipse((cx + 164, cy + 4, cx + 192, cy + 32), fill=RED, outline=(255, 255, 255), width=1)
        num = str(i + 1)
        nw = F_BADGE.getlength(num)
        text(d, (cx + 178 - nw / 2, cy + 8), num, F_BADGE, (255, 255, 255))
        tl = text_in(d, title, F_CARD_T, (cx + 6, cy + 20, cx + 158, cy + 58))
        assert len(tl) <= 2, "card title >2 lines: %r" % title
        dl = text_in(d, deck, F_CARD_D, (cx + 6, cy + 58, cx + 192, cy + 90))
        assert len(dl) <= 2, "card deck >2 lines: %r" % deck
        tw = F_TAG.getlength(tag)
        text(d, (cx + 192 - tw - 4, cy + 90), tag, F_TAG, NAVY2)
    # ---- map panel (left) ----
    map_box = (8, 546, 508, 798)
    assert map_box[3] - map_box[1] >= 240, "map panel too short"
    panel(d, map_box)
    d.rectangle((8, 546, 508, 572), fill=NAVY)
    text(d, (16, 550), "WORLD MAP  \u2014  12 PINS", F_KICK, (255, 255, 255))
    inner = (14, 576, 502, 738)
    land = Image.new("RGB", (W, H), OCEAN)
    ld = ImageDraw.Draw(land)
    for poly in CONTINENTS:
        ld.polygon([lonlat_to_xy(lon, lat, inner) for lon, lat in poly], fill=LAND)
    img.paste(land.crop(inner), inner[:2])
    d.rectangle(inner, outline=LINE, width=1)
    ART_BOXES.append(inner)
    drawn = {}
    for no, lon, lat, lab in PINS:
        px, py = lonlat_to_xy(lon, lat, inner)
        # pixel-level land check on the land layer before the pin is drawn
        assert land.getpixel((int(px), int(py))) == LAND, "pin %d not on land: (%s,%s)" % (no, lon, lat)
        dx, dy = PIN_OFFSET.get(no, (0, 0))
        cx, cy = px + dx, py + dy
        drawn[no] = (cx, cy)
        if (dx, dy) != (0, 0):
            d.line((px, py, cx, cy), fill=INK, width=1)
            d.ellipse((px - 2, py - 2, px + 2, py + 2), fill=INK)
        assert inner[0] + 8 <= cx <= inner[2] - 8 and inner[1] + 8 <= cy <= inner[3] - 8, \
            "pin %d circle outside panel" % no
        d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=RED, outline=(255, 255, 255), width=1)
        s = str(no)
        sw = F_PIN.getlength(s)
        d.text((cx - sw / 2, cy - 5), s, font=F_PIN, fill=(255, 255, 255))  # chip number, not a text box
    items = list(drawn.items())
    for a in range(len(items)):
        for b in range(a + 1, len(items)):
            (na, (ax, ay)), (nb, (bx, by)) = items[a], items[b]
            dist = ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5
            assert dist >= 14, "pins %d/%d too close: %.1f" % (na, nb, dist)
    # legend: must list every pin number
    leg = "%s" % "  |  ".join("%d %s" % (no, lab) for no, _lo, _la, lab in PINS)
    for no, _lo, _la, lab in PINS:
        assert ("%d %s" % (no, lab)) in leg, "legend missing pin %d" % no
    for r in range(4):
        for c in range(3):
            idx = r * 3 + c
            if idx >= 12:
                continue
            no, _lo, _la, lab = PINS[idx]
            text(d, (16 + c * 164, 744 + r * 13), "%d %s" % (no, lab), F_LEG)
    # ---- ALSO panel (right) ----
    panel(d, (516, 546, 1016, 798))
    d.rectangle((516, 546, 1016, 572), fill=NAVY)
    text(d, (524, 550), "ALSO TODAY  \u2014  37 MORE STORIES", F_KICK, (255, 255, 255))
    assert len(ALSO) == 37, "ALSO count %d" % len(ALSO)
    assert len(set(ALSO)) == 37, "ALSO duplicates"
    preps = {"to", "of", "in", "on", "for", "at", "by", "and", "the", "a", "an"}
    for it in ALSO:
        assert it.endswith(("[C]", "[R]", "[CL]")), "ALSO tag missing: %r" % it
        core = it.rsplit("[", 1)[0].strip()
        assert core.split()[-1].lower().strip(",.;:") not in preps, "ALSO ends with preposition: %r" % it
        assert "25 Nov" not in it or it.endswith("[CL]"), "25 Nov ALSO item must be [CL]: %r" % it
    for col in range(2):
        col_items = ALSO[col * 19:(col + 1) * 19] if col == 0 else ALSO[19:]
        x = 522 + col * 248
        for j, it in enumerate(col_items):
            assert F_ALSO.getlength(it) <= 240, "ALSO too wide: %r" % it
            text(d, (x, 576 + j * 11), it, F_ALSO)
    # ---- DATE CHECK strip ----
    panel(d, (8, 804, 1016, 950), fill=(255, 248, 220))
    d.rectangle((8, 804, 1016, 830), fill=RED)
    text(d, (16, 808), "DATE CHECK  \u2014  NOT 26 NOV: LEFT OUT ON PURPOSE", F_KICK, (255, 255, 255))
    expected_dc = set(DATE_CHECK)
    assert len(DATE_CHECK) == 7 and expected_dc == {
        "COP31 failed \u2014 22 Nov", "Shenzhou-24 launched \u2014 25 Nov",
        "Cairo tanker blast, 31 dead \u2014 25 Nov", "Cartagena hostages freed \u2014 25 Nov",
        "Australia-Solomon pact \u2014 25 Nov", "UK energy prices +26% \u2014 25 Nov",
        "Huawei convicted \u2014 24 Nov"}, "DATE CHECK mismatch"
    for i, item in enumerate(DATE_CHECK):
        bx = 14 + (i % 4) * 250
        by = 836 + (i // 4) * 56
        if i >= 6:
            bx = 14 + 3 * 250
        chip(d, (bx, by, bx + 244, by + 50), (255, 255, 255), LINE)
        d.ellipse((bx + 8, by + 8, bx + 30, by + 30), fill=RED)
        s = str(i + 1)
        sw = F_BADGE.getlength(s)
        text(d, (bx + 19 - sw / 2, by + 11), s, F_BADGE, (255, 255, 255))
        text_in(d, item, F_DC, (bx + 36, by + 6, bx + 240, by + 46))
    # ---- footer ----
    d.rectangle((8, 956, 1016, 1016), fill=NAVY)
    text(d, (16, 962), "50 STORIES  \u2022  3 HEROES  \u2022  10 CARDS  \u2022  37 ALSO  \u2022  12 MAP PINS", F_FOOT, (255, 255, 255))
    text(d, (16, 984), "Sources: Reuters  \u2022  AP  \u2022  BBC  \u2022  CNN  \u2022  Xinhua  \u2022  NPR  \u2022  ONS  \u2022  KCNA  \u2022  UKMTO  \u2022  FCC", F_FOOT, (200, 215, 230))
    # ---- corpus bans ----
    corpus = " ".join([HERO1["head"], HERO1["deck"], HERO1["why"], HERO2["head"], HERO2["deck"],
                       HERO3["head"], HERO3["deck"]] + [t for _r, t, _d, _t, _p in CARDS]
                       + [d for _r, _t, d, _t2, _p in CARDS] + ALSO + DATE_CHECK)
    for bad in ["186", "161", "720", "Bangchak", "significant figure", "third senior Hamas",
                "AWACS", "Brazil wins", "gas law", "tariffs announced", "Khasab", "khasab"]:
        assert bad not in corpus, "banned text present: %s" % bad
    assert corpus.count("Ras Tanura") <= 1, "Ras Tanura >1x"
    assert "Riyadh" not in corpus, "Riyadh present"
    check_no_art_overlap()
    img.save(OUT, optimize=True)
    n = os.path.getsize(OUT)
    assert img.size == (1024, 1024), img.size
    assert n <= 1048576, "entry.png too big: %d" % n
    print("OK entry.png %d bytes" % n)

if __name__ == "__main__":
    render()
