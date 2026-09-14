"""Generate shared cinematic diagram assets for PDF + PPTX exports."""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exports" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

BG = (7, 11, 20, 255)
BG_SOFT = (10, 18, 36, 255)
AIR = (94, 200, 255)
OXYGEN = (122, 215, 255)
FRESH = (158, 255, 240)
FIRE = (255, 138, 61)
CORE = (255, 229, 102)
HEAT = (255, 77, 46)
WARM = (255, 176, 112)
CLAY = (47, 95, 168)
WOOD = (139, 106, 69)
METAL = (201, 162, 39)
WAX = (243, 234, 216)
TEXT = (242, 245, 250)
MUTED = (154, 166, 184)


def canvas(w=1600, h=900, color=BG):
    img = Image.new("RGBA", (w, h), color)
    draw = ImageDraw.Draw(img)
    # atmospheric vignette
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(12):
        a = int(18 + i * 6)
        od.ellipse(
            [w * 0.15 - i * 30, h * 0.55 - i * 20, w * 0.85 + i * 30, h * 1.2 + i * 40],
            fill=(255, 100, 40, a // 3),
        )
    img = Image.alpha_composite(img, overlay)
    return img, ImageDraw.Draw(img)


def glow_circle(img, xy, r, color, strength=90):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = xy
    for i in range(8, 0, -1):
        a = int(strength * (i / 8) * 0.35)
        d.ellipse([x - r * i / 3, y - r * i / 3, x + r * i / 3, y + r * i / 3], fill=(*color[:3], a))
    return Image.alpha_composite(img, layer)


def draw_flame(draw, x, y, scale=1.0, strength=1.0):
    if strength <= 0.02:
        # smoke
        for i in range(6):
            sx = x + random.randint(-10, 10)
            sy = y - 20 - i * 12
            draw.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=(160, 170, 180, 40))
        return
    h = 70 * scale * strength
    w = 24 * scale * strength
    # outer
    draw.polygon(
        [(x, y + 4), (x + w, y - h * 0.35), (x + w * 0.2, y - h), (x - w * 0.55, y - h * 0.35)],
        fill=(*FIRE, int(230 * strength)),
    )
    draw.ellipse([x - w * 0.55, y - h * 0.55, x + w * 0.55, y + 6], fill=(*FIRE, int(200 * strength)))
    # tip
    draw.polygon(
        [(x, y - 2), (x + w * 0.35, y - h * 0.45), (x, y - h * 0.95), (x - w * 0.3, y - h * 0.45)],
        fill=(*CORE, int(240 * strength)),
    )
    # wick
    draw.line([(x, y + 6), (x, y - 8 * strength)], fill=(40, 28, 18, 220), width=max(2, int(2 * scale)))


def draw_board(draw, cx, by, bw=420, bh=28):
    draw.rounded_rectangle([cx - bw / 2, by, cx + bw / 2, by + bh], radius=6, fill=WOOD)
    draw.rounded_rectangle([cx - bw / 2, by, cx + bw / 2, by + 8], radius=4, fill=(166, 124, 82))


def draw_clay(draw, cx, by, gaps=False):
    draw.ellipse([cx - 70, by - 18, cx + 70, by + 18], fill=CLAY)
    if gaps:
        draw.ellipse([cx - 78, by - 12, cx - 52, by + 10], fill=(30, 22, 14))
        draw.ellipse([cx + 52, by - 12, cx + 78, by + 10], fill=(30, 22, 14))


def draw_candle(draw, cx, by, lit_strength=1.0):
    draw.rounded_rectangle([cx - 16, by - 70, cx + 16, by], radius=5, fill=WAX)
    draw.line([(cx, by - 70), (cx, by - 78)], fill=(40, 28, 18), width=2)
    draw_flame(draw, cx, by - 78, scale=1.15, strength=lit_strength)


def draw_jar(draw, cx, top, bottom, lid=False):
    left, right = cx - 90, cx + 90
    # glass body
    draw.rounded_rectangle([left, top, right, bottom], radius=16, outline=(190, 220, 240, 180), width=3)
    # glass fill tint
    overlay_pts = [left + 4, top + 4, right - 4, bottom - 4]
    draw.rounded_rectangle(overlay_pts, radius=14, fill=(180, 210, 230, 28))
    draw.line([(left + 14, top + 20), (left + 14, bottom - 24)], fill=(230, 250, 255, 70), width=2)
    if lid:
        draw.rounded_rectangle([left - 8, top - 14, right + 8, top + 6], radius=5, fill=METAL)
        draw.rectangle([left + 20, top - 8, left + 90, top - 5], fill=(255, 255, 255, 60))


def draw_oxygen(draw, cx, top, bottom, count=40, level=1.0):
    random.seed(42)
    n = max(0, int(count * level))
    for _ in range(n):
        x = random.randint(cx - 70, cx + 70)
        y = random.randint(int(top + 30), int(bottom - 40))
        r = random.randint(2, 5)
        a = random.randint(90, 180)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(*OXYGEN, a))


def draw_airflow_arrows(draw, cx, top, bottom, full=True):
    # bottom in
    for side, dx in ((-1, 28), (1, -28)):
        x0 = cx + side * 110
        y0 = bottom - 6
        draw.line([(x0, y0), (x0 - side * 18, y0 - 36)], fill=FRESH, width=3)
        draw.polygon(
            [(x0 - side * 18, y0 - 36), (x0 - side * 8, y0 - 28), (x0 - side * 26, y0 - 26)],
            fill=FRESH,
        )
    if full:
        for ox in (-20, 0, 20):
            draw.line([(cx + ox, top + 8), (cx + ox, top - 40)], fill=WARM, width=3)
            draw.polygon(
                [(cx + ox, top - 40), (cx + ox - 7, top - 28), (cx + ox + 7, top - 28)],
                fill=WARM,
            )


def save(img: Image.Image, name: str):
    path = OUT / name
    img.convert("RGB").save(path, "PNG", quality=95)
    print("wrote", path.name)
    return path


def hero_flame():
    img, draw = canvas(1600, 900)
    img = glow_circle(img, (800, 620), 120, FIRE, 110)
    draw = ImageDraw.Draw(img)
    draw_candle(draw, 800, 720, 1.0)
    save(img, "hero-flame.png")


def invisible_air(revealed=True):
    img, draw = canvas()
    draw_candle(draw, 800, 700, 1.0)
    random.seed(7)
    for _ in range(90 if revealed else 0):
        x, y = random.randint(80, 1520), random.randint(80, 820)
        r = random.randint(2, 4)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(*OXYGEN, random.randint(60, 160)))
    save(img, "air-revealed.png" if revealed else "air-hidden.png")


def experiment_setup():
    img, draw = canvas()
    cx, by = 800, 700
    draw_board(draw, cx, by)
    draw_clay(draw, cx, by)
    draw_candle(draw, cx, by - 8, 1.0)
    draw_jar(draw, cx, by - 260, by - 8, lid=False)
    # material labels strip
    labels = ["Board", "Clay", "Candle", "Jar", "Lid", "Lighter*"]
    for i, lab in enumerate(labels):
        x = 180 + i * 220
        draw.rounded_rectangle([x, 80, x + 180, 130], radius=20, outline=AIR, width=2)
        draw.text((x + 24, 95), lab, fill=TEXT)
    save(img, "experiment-setup.png")


def sealed_sequence():
    for i, level in enumerate([1.0, 0.65, 0.35, 0.0]):
        img, draw = canvas()
        cx, by = 800, 720
        draw_board(draw, cx, by)
        draw_clay(draw, cx, by)
        strength = 0.0 if level < 0.08 else 0.25 + level * 0.75
        draw_candle(draw, cx, by - 8, strength)
        draw_oxygen(draw, cx, by - 260, by - 8, level=level)
        draw_jar(draw, cx, by - 260, by - 8, lid=True)
        # meter
        draw.rounded_rectangle([560, 80, 1040, 110], radius=10, fill=(255, 255, 255, 25))
        draw.rounded_rectangle([560, 80, 560 + 480 * level, 110], radius=10, fill=OXYGEN)
        draw.text((560, 120), "Available air inside the jar", fill=MUTED)
        save(img, f"sealed-{i+1}.png")


def airflow_diagram():
    img, draw = canvas()
    cx, by = 800, 720
    draw_board(draw, cx, by)
    draw_clay(draw, cx, by, gaps=True)
    draw_candle(draw, cx, by - 8, 1.0)
    draw_oxygen(draw, cx, by - 260, by - 8, level=1.0)
    draw_jar(draw, cx, by - 260, by - 8, lid=False)
    draw_airflow_arrows(draw, cx, by - 260, by - 8, full=True)
    draw.text((520, 70), "FRESH AIR ENTERS", fill=FRESH)
    draw.text((540, by - 300), "WARM AIR LEAVES", fill=WARM)
    save(img, "airflow.png")


def bottom_only():
    img, draw = canvas()
    cx, by = 800, 720
    draw_board(draw, cx, by)
    draw_clay(draw, cx, by, gaps=True)
    draw_candle(draw, cx, by - 8, 0.25)
    draw_oxygen(draw, cx, by - 260, by - 8, level=0.25)
    draw_jar(draw, cx, by - 260, by - 8, lid=True)
    draw_airflow_arrows(draw, cx, by - 260, by - 8, full=False)
    draw.text((480, 70), "Bottom gap only — flame still goes out", fill=(255, 176, 168))
    save(img, "bottom-only.png")


def compare():
    img, draw = canvas(1600, 900)
    for idx, (mode, ox) in enumerate((("CLOSED", 420), ("AIRFLOW", 1180))):
        cx, by = ox, 700
        draw.rounded_rectangle([ox - 260, 60, ox + 260, 840], radius=20, outline=(148, 176, 210, 60), width=2)
        draw.text((ox - 50, 90), mode, fill=(255, 176, 168) if idx == 0 else FRESH)
        draw_board(draw, cx, by, bw=300)
        gaps = idx == 1
        lid = idx == 0
        strength = 0.0 if idx == 0 else 1.0
        draw_clay(draw, cx, by, gaps=gaps)
        # stronger flame visibility
        if strength > 0:
            img = glow_circle(img, (cx, by - 100), 70, FIRE, 100)
            draw = ImageDraw.Draw(img)
        draw_candle(draw, cx, by - 8, strength)
        draw_oxygen(draw, cx, by - 240, by - 8, count=50, level=0.12 if idx == 0 else 1.0)
        draw_jar(draw, cx, by - 240, by - 8, lid=lid)
        if idx == 1:
            draw_airflow_arrows(draw, cx, by - 240, by - 8, full=True)
            draw.text((ox - 90, 150), "FRESH AIR IN", fill=FRESH)
            draw.text((ox - 100, by - 280), "WARM AIR OUT", fill=WARM)
        else:
            draw.text((ox - 70, 150), "AIR USED UP", fill=(255, 176, 168))
            draw.text((ox - 80, by - 280), "FLAME OUT", fill=(255, 176, 168))
    save(img, "compare.png")


def combustion_equation():
    img, draw = canvas(1600, 700)
    chips = [
        ("Fuel", (240, 215, 176), 180),
        ("+", MUTED, 340),
        ("Oxygen", OXYGEN, 420),
        ("+", MUTED, 620),
        ("Heat", FIRE, 700),
        ("→", MUTED, 900),
        ("Heat + Light", CORE, 1000),
    ]
    for text, color, x in chips:
        if text in ("+", "→"):
            draw.text((x, 320), text, fill=color)
        else:
            draw.rounded_rectangle([x, 280, x + 170, 360], radius=30, outline=color, width=2)
            draw.text((x + 28, 308), text, fill=color)
    draw.text((420, 420), "Burning (combustion): oxygen + a substance → heat and light", fill=MUTED)
    save(img, "combustion.png")


def real_world():
    img, draw = canvas(1600, 900)
    panels = [
        (200, "Candle", FIRE),
        (600, "Fireplace", HEAT),
        (1000, "Gas stove", WARM),
        (1400, "Engine", AIR),
    ]
    for x, title, accent in panels:
        draw.rounded_rectangle([x - 150, 200, x + 150, 700], radius=18, outline=(148, 176, 210, 80), width=2)
        img = glow_circle(img, (x, 420), 50, accent, 70)
        draw = ImageDraw.Draw(img)
        draw.text((x - 40, 620), title, fill=TEXT)
    save(img, "real-world.png")


def oxygen_depletion_strip():
    img, draw = canvas(1600, 500, BG)
    stages = [1.0, 0.66, 0.33, 0.0]
    labels = ["Air full", "Air used", "Almost gone", "Flame out"]
    for i, (lv, lab) in enumerate(zip(stages, labels)):
        x0 = 80 + i * 380
        draw.rounded_rectangle([x0, 80, x0 + 320, 420], radius=16, outline=(148, 176, 210, 70), width=2)
        # particles
        random.seed(i + 3)
        n = int(24 * lv)
        for _ in range(n):
            px = random.randint(x0 + 40, x0 + 280)
            py = random.randint(120, 280)
            draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(*OXYGEN, 160))
        draw_flame(draw, x0 + 160, 360, scale=1.0, strength=0 if lv == 0 else lv)
        if i < 3:
            draw.text((x0 + 300, 230), "↓", fill=MUTED)
        draw.text((x0 + 90, 440), lab, fill=MUTED)
    save(img, "oxygen-strip.png")


def title_bg():
    img, draw = canvas(1920, 1080)
    img = glow_circle(img, (960, 900), 180, FIRE, 140)
    draw = ImageDraw.Draw(img)
    draw_candle(draw, 960, 980, 1.0)
    save(img, "title-bg.png")


def main():
    random.seed(1)
    hero_flame()
    invisible_air(False)
    invisible_air(True)
    experiment_setup()
    sealed_sequence()
    airflow_diagram()
    bottom_only()
    compare()
    combustion_equation()
    real_world()
    oxygen_depletion_strip()
    title_bg()
    print("diagrams complete →", OUT)


if __name__ == "__main__":
    main()
