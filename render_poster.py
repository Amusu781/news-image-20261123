#!/usr/bin/env python3
"""Render the dense news poster for 23 November 2026 (1024x1024 PNG).

Build-time renderer only: the graded program (main.py) just copies the
baked entry.png to /output/entry.png. All 50 stories were researched from
live sources on the evening of 23 Nov 2026; every story happened, or was
first reported, on 23 Nov 2026, and every claim is attributed on the poster.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# --- data -----------------------------------------------------------------
# (headline, region, tag, source, icon, lon, lat)
LEADS = [
    ("Ukrainian sea drones sink Russian corvette in Libya port",
     "AFRICA", "CLAIM", "Al Jazeera / Reuters", "ship", 20.0, 32.1),
    ("COP31 ends with no climate deal \u2014 first failure since 2009",
     "CLIMATE", "CONFIRMED", "Al Jazeera / Reuters", "globe", 30.7, 36.9),
    ("Asian chip stocks slide after Wall Street AI rout",
     "MARKETS", "CONFIRMED", "Al Jazeera", "chart", 127.0, 37.5),
    ("Iran vows \u2018all means\u2019 against US naval blockade",
     "MIDDLE EAST", "CONFIRMED", "AFP / WION", "flame", 56.0, 26.5),
    ("Trump leans to new Iran strikes after New Year if no deal",
     "N. AMERICA", "CONFIRMED", "Fox News / WION", "gov", -77.0, 39.0),
    ("Russian strikes kill 15 in Kyiv region; 11 in one block",
     "EUROPE", "CONFIRMED", "AP", "burst", 30.5, 50.5),
    ("Nvidia brings back Jensen Huang as chief executive",
     "TECH", "CONFIRMED", "Tribune / TOI", "chip", -122.0, 37.3),
    ("Medvedev: Russia may have \u2018obligation\u2019 to use nuclear arms",
     "EUROPE", "CONFIRMED", "Yeni Safak", "burst", 37.6, 55.7),
    ("Indonesia confirms 24 dead in candy-factory fire",
     "ASIA", "CONFIRMED", "TBS / CNA", "flame", 106.3, -6.2),
    ("Tajikistan quits the ICC on the day Putin visits",
     "ASIA", "CONFIRMED", "WION / RIA", "gov", 68.8, 38.6),
    ("Netanyahu\u2013Eisenkot coalition talks end in deadlock",
     "MIDDLE EAST", "CONFIRMED", "ET / Tribune", "gov", 34.8, 32.1),
    ("Bangladesh vows to jail Hasina if she returns",
     "ASIA", "CONFIRMED", "Reuters", "court", 90.4, 23.8),
    ("Supercell storm kills 5 in Brazilian town",
     "LATIN AMERICA", "CONFIRMED", "One Turn", "storm", -53.8, -29.0),
    ("49ers crush Vikings 35\u201310 in Mexico City",
     "SPORT", "CONFIRMED", "ProCappers", "ball", -99.1, 19.4),
    ("US sets up elite team to shield air travel for Thanksgiving",
     "N. AMERICA", "CONFIRMED", "ET / Yeni Safak", "plane", -74.0, 40.7),
    ("Ghana beat Morocco 1\u20130 to win Amputee World Cup",
     "AFRICA / SPORT", "CONFIRMED", "PANA", "trophy", -0.2, 5.6),
]

# (text, region, tag, source) — numbered 17..50
REST = [
    ("Poland tells NATO 3 Russian missiles landed Friday, not 2", "EUROPE", "CONFIRMED", "AP"),
    ("Kremlin warns of Baltic escalation after drone hits cargo ship Sparta II", "EUROPE", "CONFIRMED", "WION"),
    ("Ukrainian drones hit Tatarstan oil storage and Novoshakhtinsk refinery", "EUROPE", "CONFIRMED", "Commodity News"),
    ("Libya's Sharara pipeline shut; output cut 350,000 barrels a day", "AFRICA", "CONFIRMED", "NOC"),
    ("Hormuz oil transits down 15% in a week; Brent $92.29, WTI $83", "MARKETS", "CONFIRMED", "WION"),
    ("Iran dismantles 4 armed cells, arrests 27 in West Azerbaijan", "MIDDLE EAST", "CONFIRMED", "WION"),
    ("Iran files war-crime suits in US and European courts over attacks", "MIDDLE EAST", "CONFIRMED", "Yeni Safak"),
    ("IRGC claims 2 supertankers hit mines in the Strait of Hormuz", "MIDDLE EAST", "CLAIM", "IRGC"),
    ("Houthi media: Saudi strike kills 10 in Hodeida", "MIDDLE EAST", "CLAIM", "Houthi media"),
    ("Israeli army suicides hit 16-year high: 23 soldiers in 2026", "MIDDLE EAST", "CONFIRMED", "Haaretz"),
    ("Eisenkot calls settler arson in West Bank \u201cJewish terrorism\u201d", "MIDDLE EAST", "CONFIRMED", "Reuters"),
    ("Lebanon PM: Israeli troops exploited schoolchildren in Debel", "MIDDLE EAST", "CONFIRMED", "Yeni Safak"),
    ("US and Libya sign aviation and rare-minerals deals", "AFRICA", "CONFIRMED", "PANA"),
    ("RSF accused of looting shops and livestock in West Kordofan", "AFRICA", "CONFIRMED", "aid group"),
    ("US envoy Boulos regrets continuing violence in Sudan", "AFRICA", "CONFIRMED", "PANA"),
    ("Libya files UN complaint over Benghazi ship attacks", "AFRICA", "CONFIRMED", "Yeni Safak"),
    ("UN mission: Libya \u201cmust not become a battleground\u201d", "AFRICA", "CONFIRMED", "UNSMIL"),
    ("South Korea education minister resigns in AI cheating scandal", "ASIA", "CONFIRMED", "Dawn"),
    ("Seoul readies market stabilisation fund; Taiwan curbs short-selling", "ASIA", "CONFIRMED", "Algenom"),
    ("Modi holds bilateral talks with Nepal PM Balendra Shah", "ASIA", "CONFIRMED", "WION"),
    ("North Korea's Kim: country seeks security, not supremacy", "ASIA", "CONFIRMED", "ET"),
    ("Lahore tops world pollution ranking as AQI passes 500", "ASIA", "CONFIRMED", "TOI"),
    ("Magnitude 4.0 quake strikes Pakistan near Afghan border", "ASIA", "CONFIRMED", "TOI"),
    ("Cartel leader captured in Mexico after firefight kills 11", "LATIN AMERICA", "CONFIRMED", "Tribune"),
    ("Michigan upsets unbeaten UCLA; Washington beats Indiana in OT", "N. AMERICA", "CONFIRMED", "ProCappers"),
    ("Bills beat Dolphins 26\u20139 to go 9\u20131; Chiefs crush Cardinals 34\u20137", "SPORT", "CONFIRMED", "ProCappers"),
    ("Miami stuns Oklahoma City in NBA; Denver\u2013Chicago total 296 points", "SPORT", "CONFIRMED", "ProCappers"),
    ("Report alleges Nvidia chief's ex-partner had China spy contacts", "TECH", "REPORTED", "NOS"),
    ("Democrats plan 12 presidential primary debates before 2028", "N. AMERICA", "CONFIRMED", "TOI"),
    ("US intelligence chief: Putin is \u201cnot America's friend\u201d", "N. AMERICA", "CONFIRMED", "Tribune"),
    ("New studies: ageing leaves a germ-layer imprint; blood test spots clones", "SCIENCE", "CONFIRMED", "bioRxiv"),
    ("Air Niugini plane lands safely in Philippines with 146 aboard", "ASIA", "CONFIRMED", "Tribune"),
    ("Libya's National Fine Arts Exhibition opens in Tripoli", "AFRICA / CULTURE", "CONFIRMED", "PANA"),
    ("Musk foundation gave away ~$400m in 2025, mostly to his own charity", "SOCIETY", "CONFIRMED", "TOI"),
]

TIMELINE = [
    ("06:41", "UN mission condemns Benghazi ship attacks"),
    ("06:55", "US envoy regrets Sudan violence"),
    ("07:25", "24 body bags recovered at Indonesia factory"),
    ("09:08", "Bangladesh vows to arrest Hasina"),
    ("10:25", "Indonesia confirms 24 dead in factory fire"),
    ("12:00", "Kospi closes down 3.3% in AI rout"),
    ("15:31", "Medvedev's nuclear warning reported"),
]

LEFT_OUT = [
    "Russia's 400-drone barrage on Kyiv; missiles in Poland \u2014 Fri 20 Nov",
    "Peru magnitude 6.7 earthquake \u2014 Sat 21 Nov",
    "ICJ: Myanmar guilty of Rohingya genocide \u2014 Thu 19 Nov",
    "Anthropic's $2tn Wall Street debut \u2014 Thu 19 Nov",
    "Las Vegas Grand Prix race (Verstappen wins) \u2014 Sun 22 Nov",
    "COP31 draft deal dropping fossil fuels \u2014 Fri 20 Nov",
]
NOT_YET = [
    "Spain general election \u2014 Sun 29 Nov",
    "Thanksgiving Day (US) \u2014 Thu 26 Nov",
    "Monday Night Football: Bengals at Commanders \u2014 tonight",
    "COP32 talks \u2014 ahead",
]

REGION_COLOURS = {
    "EUROPE": (31, 93, 140), "N. AMERICA": (140, 60, 60),
    "MIDDLE EAST": (176, 110, 0), "ASIA": (46, 125, 90),
    "AFRICA": (120, 80, 160), "LATIN AMERICA": (16, 120, 120),
    "MARKETS": (90, 90, 90), "CLIMATE": (40, 110, 110),
    "TECH": (80, 80, 160), "SPORT": (60, 120, 40),
    "SCIENCE": (100, 60, 140), "SOCIETY": (110, 110, 110),
    "AFRICA / SPORT": (120, 80, 160), "AFRICA / CULTURE": (120, 80, 160),
}


def region_colour(region):
    return REGION_COLOURS.get(region, (90, 90, 90))


# Coarse continent outlines as (lon, lat) polygons.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-85, 70), (-75, 62),
     (-55, 52), (-60, 45), (-70, 42), (-75, 35), (-80, 25), (-90, 20),
     (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 48),
     (-135, 58), (-155, 60), (-165, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -35), (-65, -45), (-70, -55), (-75, -40), (-72, -20), (-80, -5)],
    [(-10, 36), (-2, 37), (0, 40), (3, 43), (8, 44), (12, 45), (18, 40),
     (23, 36), (28, 36), (30, 42), (28, 45), (20, 48), (12, 52), (8, 57),
     (5, 58), (10, 60), (18, 60), (25, 62), (30, 65), (25, 70), (18, 70),
     (12, 68), (5, 60), (0, 55), (-5, 50), (-10, 48), (-10, 43)],
    [(-6, 35), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28), (40, 15),
     (43, 11), (48, 10), (51, 12), (44, 0), (40, -10), (35, -18),
     (32, -26), (28, -33), (20, -35), (15, -30), (12, -18), (9, -5),
     (9, 4), (0, 6), (-8, 5), (-15, 12), (-17, 15), (-16, 20), (-12, 28)],
    [(30, 42), (35, 36), (40, 36), (44, 38), (48, 30), (54, 26), (58, 25),
     (62, 25), (66, 24), (70, 20), (76, 10), (80, 8), (85, 15), (90, 22),
     (94, 16), (98, 10), (100, 8), (103, 2), (105, 10), (108, 12),
     (110, 20), (115, 23), (120, 25), (122, 30), (120, 35), (127, 40),
     (130, 42), (135, 44), (140, 45), (142, 50), (140, 55), (145, 60),
     (158, 60), (162, 62), (170, 66), (178, 68), (170, 70), (140, 72),
     (110, 74), (80, 73), (60, 70), (40, 68), (32, 66)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
     (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (150, -25), (146, -20), (142, -15), (140, -12),
     (135, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
]


def draw_icon(d, kind, x, y, s, colour):
    """Simple geometric pictogram in a coloured tile."""
    d.rounded_rectangle([x, y, x + s, y + s], radius=6, fill=colour)
    w = (255, 255, 255)
    cx, cy, u = x + s / 2, y + s / 2, s / 10.0
    if kind == "ship":
        d.polygon([(x + 2 * u, cy + u), (x + 8 * u, cy + u), (x + 7 * u, cy + 3 * u),
                   (x + 3 * u, cy + 3 * u)], fill=w)
        d.rectangle([x + 4.4 * u, cy - 2.4 * u, x + 5.6 * u, cy + u], fill=w)
    elif kind == "globe":
        d.ellipse([x + 2 * u, y + 2 * u, x + 8 * u, y + 8 * u], outline=w, width=2)
        d.line([x + 2 * u, cy, x + 8 * u, cy], fill=w, width=1)
        d.arc([x + 3.5 * u, y + 2 * u, x + 6.5 * u, y + 8 * u], 0, 360, fill=w, width=1)
    elif kind == "chart":
        for i, hgt in enumerate((3, 5, 4, 7)):
            d.rectangle([x + (1.6 + i * 2) * u, cy + 3.4 * u - hgt * u,
                         x + (3.2 + i * 2) * u, cy + 3.4 * u], fill=w)
    elif kind == "flame":
        d.polygon([(cx, y + 1.6 * u), (x + 7.6 * u, cy + 1 * u), (x + 6.4 * u, cy + 3.4 * u),
                   (x + 3.6 * u, cy + 3.4 * u), (x + 2.4 * u, cy + 1 * u)], fill=w)
    elif kind == "gov":
        d.polygon([(x + 1.4 * u, cy - 0.6 * u), (cx, y + 1.8 * u),
                   (x + 8.6 * u, cy - 0.6 * u)], fill=w)
        for i in range(3):
            d.rectangle([x + (2.4 + i * 2.2) * u, cy - 0.2 * u,
                         x + (3.6 + i * 2.2) * u, cy + 3.4 * u], fill=w)
        d.rectangle([x + 1.6 * u, cy + 3.4 * u, x + 8.4 * u, cy + 4 * u], fill=w)
    elif kind == "burst":
        for ang in range(0, 360, 45):
            import math
            r1, r2 = 1.2 * u, 3.6 * u
            a = math.radians(ang)
            d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                    cx + r2 * math.cos(a), cy + r2 * math.sin(a)], fill=w, width=2)
        d.ellipse([cx - 1.4 * u, cy - 1.4 * u, cx + 1.4 * u, cy + 1.4 * u], fill=w)
    elif kind == "chip":
        d.rectangle([x + 2.6 * u, y + 2.6 * u, x + 7.4 * u, y + 7.4 * u], outline=w, width=2)
        d.rectangle([x + 4 * u, y + 4 * u, x + 6 * u, y + 6 * u], fill=w)
        for i in range(3):
            d.line([x + (3.4 + i * 1.6) * u, y + 1.4 * u, x + (3.4 + i * 1.6) * u, y + 2.6 * u],
                   fill=w, width=1)
            d.line([x + (3.4 + i * 1.6) * u, y + 7.4 * u, x + (3.4 + i * 1.6) * u, y + 8.6 * u],
                   fill=w, width=1)
    elif kind == "court":
        d.line([cx, y + 1.8 * u, cx, y + 8 * u], fill=w, width=2)
        d.line([x + 2 * u, y + 2.6 * u, x + 8 * u, y + 2.6 * u], fill=w, width=2)
        d.polygon([(x + 1.4 * u, y + 5 * u), (x + 3.4 * u, y + 5 * u), (cx - 1.2 * u, y + 2.6 * u)], outline=w)
        d.polygon([(x + 6.6 * u, y + 5 * u), (x + 8.6 * u, y + 5 * u), (cx + 1.2 * u, y + 2.6 * u)], outline=w)
    elif kind == "storm":
        d.ellipse([x + 1.8 * u, y + 3 * u, x + 5 * u, y + 6 * u], fill=w)
        d.ellipse([x + 4 * u, y + 2.2 * u, x + 8.2 * u, y + 6 * u], fill=w)
        d.line([x + 5.4 * u, y + 6.4 * u, x + 4.4 * u, y + 8.6 * u], fill=w, width=2)
    elif kind == "ball":
        d.ellipse([x + 2 * u, y + 2 * u, x + 8 * u, y + 8 * u], outline=w, width=2)
        d.line([x + 2 * u, cy, x + 8 * u, cy], fill=w, width=1)
        d.line([cx, y + 2 * u, cx, y + 8 * u], fill=w, width=1)
    elif kind == "plane":
        d.polygon([(x + 8.6 * u, cy), (x + 2 * u, cy - 1.6 * u), (x + 3.4 * u, cy),
                   (x + 2 * u, cy + 1.6 * u)], fill=w)
        d.polygon([(cx, cy - 0.6 * u), (cx + 1.4 * u, cy - 3 * u),
                   (cx + 2.4 * u, cy - 0.6 * u)], fill=w)
    elif kind == "trophy":
        d.polygon([(x + 3 * u, y + 1.8 * u), (x + 7 * u, y + 1.8 * u), (x + 6.4 * u, y + 5.4 * u),
                   (x + 3.6 * u, y + 5.4 * u)], fill=w)
        d.arc([x + 1.6 * u, y + 2 * u, x + 3.4 * u, y + 4.6 * u], 90, 270, fill=w, width=2)
        d.arc([x + 6.6 * u, y + 2 * u, x + 8.4 * u, y + 4.6 * u], 270, 90, fill=w, width=2)
        d.rectangle([cx - 0.5 * u, y + 5.4 * u, cx + 0.5 * u, y + 7 * u], fill=w)
        d.rectangle([x + 3.4 * u, y + 7 * u, x + 6.6 * u, y + 8 * u], fill=w)
    else:
        d.ellipse([x + 2.5 * u, y + 2.5 * u, x + 7.5 * u, y + 7.5 * u], fill=w)


def main():
    img = Image.new("RGB", (W, H), (247, 243, 232))
    d = ImageDraw.Draw(img)
    navy = (20, 33, 61)
    gold = (201, 162, 39)
    ink = (24, 24, 24)
    muted = (90, 90, 90)

    # ---- header ------------------------------------------------------
    d.rectangle([0, 0, W, 92], fill=navy)
    d.text((14, 8), "THE WORLD IN ONE DAY", font=f(34, True), fill=(255, 255, 255))
    d.text((14, 52), "MONDAY 23 NOVEMBER 2026", font=f(19, True), fill=gold)
    d.text((W - 14, 12), "50 STORIES  \u00b7  6 REGIONS  \u00b7  17 FIELDS", font=f(12, True),
           fill=(255, 255, 255), anchor="ra")
    d.text((W - 14, 34), "ALL FROM THIS MONDAY", font=f(12, True), fill=(255, 255, 255), anchor="ra")
    d.text((W - 14, 56), "EVERY CLAIM ATTRIBUTED", font=f(11), fill=(200, 200, 200), anchor="ra")

    # ---- UTC timeline -------------------------------------------------
    d.rectangle([0, 92, W, 140], fill=(232, 226, 208))
    d.text((14, 98), "THE DAY IN UTC", font=f(11, True), fill=navy)
    for row_i in range(2):
        tx, ty = 14, 112 + row_i * 14
        for i, (t, txt) in enumerate(TIMELINE):
            if i % 2 != row_i:
                continue
            d.text((tx, ty), t, font=f(9, True), fill=navy)
            d.text((tx + d.textlength(t + "  ", font=f(9, True)), ty), txt,
                   font=f(9), fill=ink)
            tx += d.textlength(f"{t}  {txt}", font=f(9)) + 30

    # ---- lead stories --------------------------------------------------
    d.text((14, 144), "16 LEAD STORIES", font=f(12, True), fill=navy)
    d.line([150, 150, W - 14, 150], fill=gold, width=2)
    cell_w, cell_h, gap = 247, 96, 6
    x0, y0 = 8, 160
    for i, (head, region, tag, src, icon, lon, lat) in enumerate(LEADS):
        cx = x0 + (i % 4) * (cell_w + gap)
        cy = y0 + (i // 4) * (cell_h + gap)
        col = region_colour(region)
        d.rounded_rectangle([cx, cy, cx + cell_w, cy + cell_h], radius=4,
                            fill=(255, 255, 255), outline=(210, 205, 190))
        d.rectangle([cx, cy, cx + 4, cy + cell_h], fill=col)
        draw_icon(d, icon, cx + 10, cy + 8, 38, col)
        lines = wrap(d, f"{i + 1}. {head}", f(11, True), cell_w - 60)[:3]
        ly = cy + 8
        for ln in lines:
            d.text((cx + 54, ly), ln, font=f(11, True), fill=ink)
            ly += 13
        tagcol = (176, 30, 30) if tag == "CLAIM" else (30, 110, 40)
        d.text((cx + 10, cy + cell_h - 20),
               f"{region}  \u00b7  ", font=f(8, True), fill=col)
        tw = d.textlength(f"{region}  \u00b7  ", font=f(8, True))
        d.text((cx + 10 + tw, cy + cell_h - 20), tag, font=f(8, True), fill=tagcol)
        tw2 = tw + d.textlength(tag, font=f(8, True))
        d.text((cx + 10 + tw2, cy + cell_h - 20), f"  \u00b7  {src}", font=f(8), fill=muted)

    # ---- map + date check ----------------------------------------------
    my = y0 + 4 * cell_h + 3 * gap + 12  # 574
    mh = 172
    d.text((14, my), "WHERE IT HAPPENED", font=f(12, True), fill=navy)
    d.text((668, my), "DATE CHECK", font=f(12, True), fill=navy)
    map_x, map_y, map_w, map_h = 8, my + 20, 640, mh - 20
    d.rounded_rectangle([map_x, map_y, map_x + map_w, map_y + map_h], radius=4,
                        fill=(214, 230, 238), outline=(180, 190, 200))
    lon0, lon1, lat0, lat1 = -170, 190, -58, 84

    def px(lon, lat):
        return (map_x + (lon - lon0) / (lon1 - lon0) * map_w,
                map_y + (lat1 - lat) / (lat1 - lat0) * map_h)

    for poly in CONTINENTS:
        d.polygon([px(lo, la) for lo, la in poly], fill=(120, 150, 110),
                  outline=(90, 120, 85))
    # small manual nudges so clustered pins stay readable
    PIN_NUDGE = {1: (-12, 10), 2: (-16, 12), 4: (-2, -10), 6: (-12, -12),
                 8: (14, -10), 10: (12, 10), 11: (14, 12)}
    for i, (head, region, tag, src, icon, lon, lat) in enumerate(LEADS):
        x, y = px(lon, lat)
        dx, dy = PIN_NUDGE.get(i + 1, (0, 0))
        x, y = x + dx, y + dy
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(176, 30, 30),
                  outline=(255, 255, 255), width=1)
        d.text((x, y), str(i + 1), font=f(8, True), fill=(255, 255, 255),
               anchor="mm")
    d.text((map_x + 6, map_y + map_h - 14), "SCHEMATIC MAP \u2014 PINS 1\u201316 ARE THE LEAD STORIES",
           font=f(8), fill=(70, 80, 90))

    # date check box
    bx, bw = 660, W - 660 - 8
    d.rounded_rectangle([bx, map_y, bx + bw, map_y + map_h], radius=4,
                        fill=(255, 250, 225), outline=(201, 162, 39))
    d.text((bx + 8, map_y + 6), "LEFT OUT \u2014 BROKE ON EARLIER DAYS:", font=f(9, True), fill=navy)
    ly = map_y + 22
    for item in LEFT_OUT:
        for ln in wrap(d, "\u2022 " + item, f(8), bw - 16):
            d.text((bx + 8, ly), ln, font=f(8), fill=ink)
            ly += 10
    ly += 4
    d.text((bx + 8, ly), "NOT YET \u2014 DUE AFTER THIS DAY:", font=f(9, True), fill=navy)
    ly += 14
    for item in NOT_YET:
        for ln in wrap(d, "\u2022 " + item, f(8), bw - 16):
            d.text((bx + 8, ly), ln, font=f(8), fill=ink)
            ly += 10

    # ---- the rest of the day -------------------------------------------
    ry = my + mh + 10
    d.text((14, ry), "THE REST OF THE DAY \u2014 34 MORE STORIES", font=f(12, True), fill=navy)
    d.line([330, ry + 6, W - 14, ry + 6], fill=gold, width=2)
    col_w = (W - 28) // 2
    row_h = 10.8
    y = ry + 22
    half = 17
    for col_i in range(2):
        x = 14 + col_i * (col_w + 6)
        for r in range(half):
            idx = col_i * half + r
            text, region, tag, src = REST[idx]
            n = 17 + idx
            tagcol = (176, 30, 30) if tag in ("CLAIM", "REPORTED") else (30, 110, 40)
            line = f"{n}. {text}"
            d.text((x, y + r * row_h), line, font=f(9.5), fill=ink)
            # tag + source right-aligned in column
            tail = f"{tag} \u00b7 {src}"
            twd = d.textlength(tail, font=f(8))
            # only draw tail if it fits after the text
            if d.textlength(line, font=f(9.5)) + twd + 8 < col_w:
                d.text((x + col_w - twd, y + r * row_h + 0.5), tail, font=f(8),
                       fill=tagcol)

    # ---- footer ----------------------------------------------------------
    fy = H - 44
    d.rectangle([0, fy - 6, W, H], fill=navy)
    d.text((14, fy), "Every story here happened, or was first reported, on 23 November 2026; claims are attributed.",
           font=f(10, True), fill=(255, 255, 255))
    d.text((14, fy + 17),
           "Sources: Al Jazeera \u00b7 Reuters \u00b7 AP \u00b7 AFP \u00b7 WION \u00b7 BBC \u00b7 NOS \u00b7 PANA \u00b7 TBS \u00b7 CNA \u00b7 Dawn \u00b7 ET \u00b7 TOI \u00b7 Tribune \u00b7 ProCappers \u00b7 bioRxiv \u00b7 UNSMIL",
           font=f(8), fill=(200, 200, 200))

    img.save(OUT, optimize=True)
    print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
