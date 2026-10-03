#!/usr/bin/env python3
"""Render a CurioMondo weather hero over the ISTAT 2026 regional boundaries.

The forecast text is supplied by the newsroom. The map geometry comes from
ISTAT (CC BY 4.0) via the 2026 regional GeoJSON at
https://raw.githubusercontent.com/guglielmo/geojson-italy/main/geojson/limits_IT_regions.geojson.
Never draw borders or city positions with an image generator. A generated
photograph is used only in the decorative header and foot of the graphic.

Usage: python3 tools/render_meteo_map.py --config forecast.json \
       --geojson regions.geojson --background illustration.png --output map.png
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, AA = 1800, 1200, 2
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
NAVY = "#08294a"
INK = "#123c5a"
TEAL = "#12646e"
SEAWATER = "#dfedf4"
LAND = "#ecf2d8"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(BOLD if bold else FONT, size * AA)


def box(draw: ImageDraw.ImageDraw, coords: tuple[int, int, int, int], fill: str,
        radius: int = 0, outline: str | None = None, width: int = 1) -> None:
    xy = tuple(round(v * AA) for v in coords)
    draw.rounded_rectangle(xy, radius=radius * AA, fill=fill, outline=outline,
                           width=width * AA)


def xy(lon: float, lat: float) -> tuple[int, int]:
    # Equirectangular projection at 42° N, suitable for a national locator map.
    return (round((245 + (lon - 6.6) * math.cos(math.radians(42)) * 80) * AA),
            round((165 + (47.1 - lat) * 80) * AA))


def draw_regions(draw: ImageDraw.ImageDraw, geojson: dict) -> None:
    for feature in geojson["features"]:
        geometry = feature["geometry"]
        polygons = ([geometry["coordinates"]] if geometry["type"] == "Polygon"
                    else geometry["coordinates"])
        for polygon in polygons:
            exterior = [xy(*point[:2]) for point in polygon[0]]
            if len(exterior) >= 3:
                draw.polygon(exterior, fill=LAND, outline="#a2b69b", width=2 * AA)
            for hole in polygon[1:]:
                draw.polygon([xy(*point[:2]) for point in hole], fill=SEAWATER)


# Label anchors are editorial placements, not fabricated geography. They sit
# in or next to the corresponding ISTAT polygon, with compact names where the
# map's scale makes the full bilingual form unreadable.
REGIONS = [
    ("Valle d’Aosta", 7.45, 45.74, -120, -36),
    ("Piemonte", 8.15, 44.80, -22, 12),
    ("Liguria", 9.12, 44.06, -56, 47),
    ("Lombardia", 10.20, 45.60, 85, -35),
    ("Trentino-Alto Adige", 11.35, 46.47, 15, 4),
    ("Veneto", 11.92, 45.59, -5, 23),
    ("Friuli-Venezia Giulia", 13.02, 46.18, 100, -35),
    ("Emilia-Romagna", 11.32, 44.38, 7, -14),
    ("Toscana", 11.08, 43.23, -85, 45),
    ("Marche", 13.18, 43.47, 21, 0),
    ("Umbria", 12.43, 42.96, 17, 7),
    ("Lazio", 12.40, 41.72, -65, 10),
    ("Abruzzo", 13.75, 42.27, 26, -18),
    ("Molise", 14.60, 41.65, 40, -4),
    ("Campania", 14.64, 40.78, -20, -18),
    ("Puglia", 16.60, 41.36, 36, 13),
    ("Basilicata", 16.09, 40.25, -2, 9),
    ("Calabria", 16.43, 39.20, 59, 7),
    ("Sicilia", 13.83, 37.45, 10, 18),
    ("Sardegna", 9.05, 40.05, -45, 18),
]

CITIES = [
    ("Torino", 7.6869, 45.0703, -90, -54),
    ("Milano", 9.1900, 45.4642, -45, -55),
    ("Genova", 8.9463, 44.4056, -20, 26),
    ("Venezia", 12.3155, 45.4408, 18, -57),
    ("Bologna", 11.3426, 44.4949, 12, 28),
    ("Firenze", 11.2558, 43.7696, -53, 28),
    ("Roma", 12.4964, 41.9028, -17, 29),
    ("Napoli", 14.2681, 40.8518, -55, 29),
    ("Bari", 16.8719, 41.1171, 16, 19),
    ("Palermo", 13.3615, 38.1157, -95, -52),
    ("Cagliari", 9.1106, 39.2238, -105, 10),
]


def weather_icon(draw: ImageDraw.ImageDraw, cx: int, cy: int,
                 kind: str, size: int = 35) -> None:
    x, y, radius = cx * AA, cy * AA, size * AA
    if kind == "sun":
        for index in range(12):
            angle = index * math.pi / 6
            a = (x + math.cos(angle) * radius * 1.42,
                 y + math.sin(angle) * radius * 1.42)
            b = (x + math.cos(angle) * radius * 1.82,
                 y + math.sin(angle) * radius * 1.82)
            draw.line((*a, *b), fill="#dfa92c", width=6 * AA)
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill="#ffc64b",
                     outline="#e2a52b", width=3 * AA)
    elif kind == "cloud":
        draw.ellipse((x-radius, y-radius//3, x+radius//2, y+radius), fill="#a5bfcb")
        draw.ellipse((x-radius//2, y-radius, x+radius, y+radius//2), fill="#b3cbd3")
        draw.rounded_rectangle((x-radius, y, x+radius, y+radius), radius=radius//3,
                               fill="#a5bfcb")


def photo_crop(path: Path, width: int, height: int) -> Image.Image:
    src = Image.open(path).convert("RGB")
    scale = max(width / src.width, height / src.height)
    src = src.resize((round(src.width * scale), round(src.height * scale)),
                     Image.Resampling.LANCZOS)
    left = (src.width - width) // 2
    top = (src.height - height) // 2
    return src.crop((left, top, left + width, top + height))


def render(config: dict, geojson: dict, background: Path, output: Path) -> None:
    canvas = Image.new("RGB", (W * AA, H * AA), "#f2f6f5")
    canvas.paste(photo_crop(background, W * AA, 168 * AA), (0, 0))
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    box(od, (0, 0, W, 168), "#062946d8")
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(canvas)
    draw.text((66 * AA, 29 * AA), "METEO ITALIA", fill="#ffffff", font=font(60, True))
    draw.text((66 * AA, 103 * AA), config["period"], fill="#d7eff4", font=font(36))
    box(draw, (1252, 41, 1743, 126), "#eff7f6", radius=18)
    draw.text((1281 * AA, 65 * AA), "OGGI E PROSSIMI 7 GIORNI",
              fill=NAVY, font=font(25, True))

    box(draw, (37, 181, 1161, 1104), SEAWATER, radius=24)
    for lon in (8, 10, 12, 14, 16, 18):
        a = xy(lon, 47.1); b = xy(lon, 35.6)
        draw.line((a, b), fill="#c8dde6", width=AA)
    for lat in (36, 38, 40, 42, 44, 46):
        a = xy(6.6, lat); b = xy(18.6, lat)
        draw.line((a, b), fill="#c8dde6", width=AA)
    draw_regions(draw, geojson)

    # Symbols summarize nationwide conditions, with isolated clouds shown as
    # possibilities. The map deliberately contains no city-level temperatures.
    for kind, lon, lat in config["map_symbols"]:
        x, y = xy(lon, lat)
        weather_icon(draw, round(x / AA), round(y / AA), kind, 24)

    for name, lon, lat, dx, dy in REGIONS:
        x, y = xy(lon, lat)
        tx, ty = x + dx * AA, y + dy * AA
        # A pale halo keeps the regional boundaries visible behind the text.
        draw.text((tx, ty), name, fill="#1a665e", font=font(18, True),
                  anchor="mm", stroke_width=3 * AA, stroke_fill="#f7f9ec")

    for name, lon, lat, dx, dy in CITIES:
        x, y = xy(lon, lat)
        lx, ly = x + dx * AA, y + dy * AA
        f = font(23, True)
        extent = draw.textbbox((0, 0), name, font=f)
        width = extent[2] - extent[0]
        box(draw, (round(lx / AA), round(ly / AA),
                   round((lx + width) / AA) + 22, round(ly / AA) + 37),
            "#ffffff", radius=9, outline="#abbdc1", width=1)
        draw.line((x, y, lx + width // 2, ly + 18 * AA),
                  fill="#6d8390", width=2 * AA)
        draw.ellipse((x-6*AA, y-6*AA, x+6*AA, y+6*AA),
                     fill=NAVY, outline="#ffffff", width=3 * AA)
        draw.text((lx + 11*AA, ly + 2*AA), name, fill=NAVY, font=f)

    box(draw, (58, 1038, 1140, 1088), "#ffffff", radius=11)
    draw.text((77*AA, 1048*AA), "Confini regionali ISTAT 2026 (CC BY 4.0)  •  città in posizione geografica",
              fill="#2d556c", font=font(21))

    box(draw, (1181, 181, 1762, 1104), "#ffffff", radius=24)
    box(draw, (1202, 205, 1741, 290), "#0b5271", radius=17)
    draw.text((1230*AA, 228*AA), "SITUAZIONE E TENDENZA", fill="#ffffff", font=font(29, True))
    stages = config["stages"]
    positions = [(312, 458), (476, 620), (638, 782), (800, 945)]
    for stage, (top, bottom) in zip(stages, positions):
        box(draw, (1202, top, 1741, bottom), "#f3f8fa", radius=15)
        weather_icon(draw, 1261, top+66, stage["icon"], 25)
        draw.text((1324*AA, (top+24)*AA), stage["label"],
                  fill=TEAL, font=font(27, True))
        draw.text((1324*AA, (top+64)*AA), stage["summary"],
                  fill=NAVY, font=font(25, True))
        draw.text((1324*AA, (top+105)*AA), stage["detail"],
                  fill=INK, font=font(21))
    # The sky photograph is explicitly illustrative and has no map content.
    strip = photo_crop(background, 539 * AA, 113 * AA).filter(ImageFilter.GaussianBlur(3 * AA))
    canvas.paste(strip, (1202 * AA, 963 * AA))
    shade = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    box(sd, (1202, 963, 1741, 1076), "#062946ba", radius=13)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shade).convert("RGB")
    draw = ImageDraw.Draw(canvas)
    draw.text((1227*AA, 982*AA), "Carta illustrativa, non bollettino ufficiale",
              fill="#ffffff", font=font(20, True))
    draw.text((1227*AA, 1020*AA), "Consulta gli aggiornamenti locali",
              fill="#d7eff4", font=font(21))
    draw.text((50*AA, 1125*AA), config["footer"], fill="#34566d", font=font(23))

    canvas.resize((W, H), Image.Resampling.LANCZOS).save(output, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    for key in ("config", "geojson", "background", "output"):
        parser.add_argument(f"--{key}", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    geojson = json.loads(args.geojson.read_text(encoding="utf-8"))
    assert len(geojson["features"]) == 20
    render(config, geojson, args.background, args.output)


if __name__ == "__main__":
    main()
