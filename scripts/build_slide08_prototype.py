"""
Slide 08 Animation Prototype — EDITABLE COMPONENT ARCHITECTURE

Demonstrates the interactive science experience standard:
  - Named editable shapes (Jar, Candle, Flame, Oxygen particles)
  - Real PowerPoint animations (motion paths, grow/shrink, exit fade)
  - Synchronized OXYGEN ↓ / FLAME ↓ teaching sequence

NO static sequence image. Scene built from components.

Output:
  exports/powerpoint/Slide08-Animation-Prototype.pptx
  exports/previews/Slide08-Prototype.PNG
"""
from __future__ import annotations

from pathlib import Path
import win32com.client

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exports" / "powerpoint" / "Slide08-Animation-Prototype.pptx"
PREVIEWS = ROOT / "exports" / "previews"

W = 13.333 * 72
H = 7.5 * 72

# Effect / trigger constants
msoAnimEffectAppear = 1
msoAnimEffectFade = 10
msoAnimEffectGrowShrink = 6
msoAnimEffectCustom = 9
msoAnimEffectFly = 2
msoAnimTriggerOnPageClick = 1
msoAnimTriggerWithPrevious = 2
msoAnimTriggerAfterPrevious = 3
msoAnimTypeMotion = 2
msoTrue = -1

# Colors
CREAM = 242 + (250 << 8) + (255 << 16)  # will set properly below


def rgb(r, g, b):
    return r + (g << 8) + (b << 16)


CREAM = rgb(255, 250, 242)
SKY = rgb(232, 244, 252)
NAVY = rgb(24, 48, 80)
CYAN = rgb(0, 180, 220)
AIR = rgb(64, 196, 230)
FIRE = rgb(255, 140, 50)
AMBER = rgb(255, 190, 60)
YELLOW = rgb(255, 230, 100)
WHITE = rgb(255, 255, 255)
WAX = rgb(250, 248, 240)
WOOD = rgb(210, 180, 140)
SOFT = rgb(90, 110, 140)
WARN = rgb(230, 90, 60)
SMOKE = rgb(180, 190, 200)


def set_bg(slide, color):
    slide.FollowMasterBackground = False
    f = slide.Background.Fill
    f.Solid()
    f.ForeColor.RGB = color


def name(sh, n):
    sh.Name = n
    return sh


def oval(slide, left, top, width, height, fill, *, line=None, transparency=0.0):
    sh = slide.Shapes.AddShape(9, left, top, width, height)
    sh.Fill.Solid()
    sh.Fill.ForeColor.RGB = fill
    sh.Fill.Transparency = transparency
    if line is None:
        sh.Line.Visible = 0
    else:
        sh.Line.Visible = -1
        sh.Line.ForeColor.RGB = line
        sh.Line.Weight = 2.0
    return sh


def rounded(slide, left, top, width, height, fill, *, line=None, transparency=0.0):
    sh = slide.Shapes.AddShape(5, left, top, width, height)
    sh.Fill.Solid()
    sh.Fill.ForeColor.RGB = fill
    sh.Fill.Transparency = transparency
    if line is None:
        sh.Line.Visible = 0
    else:
        sh.Line.Visible = -1
        sh.Line.ForeColor.RGB = line
        sh.Line.Weight = 1.5
    return sh


def tb(slide, text, left, top, width, height, *, size=20, color=NAVY, bold=True, align=2, font="Aptos"):
    sh = slide.Shapes.AddTextbox(1, left, top, width, height)
    tr = sh.TextFrame.TextRange
    tr.Text = text
    try:
        tr.Font.Name = font
    except Exception:
        tr.Font.Name = "Calibri"
    tr.Font.Size = size
    tr.Font.Bold = bold
    tr.Font.Color.RGB = color
    tr.ParagraphFormat.Alignment = align
    sh.TextFrame.WordWrap = True
    return sh


def add_effect(slide, shape, effect_id, trigger=msoAnimTriggerOnPageClick):
    return slide.TimeLine.MainSequence.AddEffect(shape, effect_id, 0, trigger)


def exit_fade(slide, shape, trigger=msoAnimTriggerOnPageClick, duration=0.6):
    eff = add_effect(slide, shape, msoAnimEffectFade, trigger)
    eff.Exit = msoTrue
    eff.Timing.Duration = duration
    return eff


def grow_shrink(slide, shape, size_pct, trigger=msoAnimTriggerOnPageClick, duration=0.8):
    """size_pct: 100 = same size, 50 = half, etc."""
    eff = add_effect(slide, shape, msoAnimEffectGrowShrink, trigger)
    eff.EffectParameters.Size = float(size_pct)
    eff.Timing.Duration = duration
    return eff


msoAnimEffectPathDown = 42
msoAnimEffectPathRight = 46
msoAnimEffectPathLeft = 45


def motion_toward_flame(slide, shape, *, dx_pct, dy_pct, trigger=msoAnimTriggerWithPrevious, duration=0.65):
    """
    Real motion path toward the flame using PathDown (reliable in PPT COM).
    dx_pct/dy_pct kept for API compatibility / future custom paths.
    """
    del dx_pct, dy_pct  # reserved for future custom ByX/ByY when COM allows
    eff = add_effect(slide, shape, msoAnimEffectPathDown, trigger)
    eff.Timing.Duration = duration
    return eff


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)

    ppt = win32com.client.Dispatch("PowerPoint.Application")
    ppt.Visible = 1
    pres = ppt.Presentations.Add()
    # Widescreen 16:9
    pres.PageSetup.SlideWidth = W
    pres.PageSetup.SlideHeight = H

    s = pres.Slides.Add(1, 12)  # blank
    set_bg(s, CREAM)

    # Soft sky band (environment, not a card)
    sky = name(rounded(s, 0, 0, W, 160, SKY), "ENV_SkyBand")
    sky.ZOrder(1)  # send to back-ish

    # Tabletop surface
    table = name(rounded(s, 80, 420, W - 160, 90, WOOD, transparency=0.15), "ENV_Tabletop")

    # Title
    title = name(
        tb(s, "Watch carefully!", 40, 18, W - 80, 50, size=36, color=WARN, bold=True, font="Aptos Display"),
        "TXT_Title",
    )
    subtitle = name(
        tb(s, "Oxygen ↓   ·   Flame ↓", 40, 68, W - 80, 30, size=16, color=CYAN, bold=True, font="Aptos"),
        "TXT_Subtitle",
    )

    # ---- CORE EDITABLE OBJECTS ----
    # Candle body (center-bottom of scene)
    cx, cy = 480, 300  # candle top-left approx
    candle = name(rounded(s, cx, cy + 40, 70, 130, WAX, line=rgb(220, 210, 200)), "OBJ_Candle")
    wick = name(rounded(s, cx + 30, cy + 28, 8, 18, rgb(40, 40, 40)), "OBJ_Wick")

    # Flame states — discrete editable objects (Strong → Medium → Tiny → Out)
    # Strong visible at start; Medium/Tiny enter via Appear after Strong exits.
    flame_strong = name(oval(s, cx + 8, cy - 28, 54, 78, AMBER), "OBJ_Flame_Strong")
    core_strong = name(oval(s, cx + 20, cy + 4, 28, 40, YELLOW, transparency=0.12), "OBJ_FlameCore_Strong")

    flame_med = name(oval(s, cx + 16, cy - 5, 38, 52, AMBER), "OBJ_Flame_Medium")
    core_med = name(oval(s, cx + 24, cy + 12, 20, 28, YELLOW, transparency=0.12), "OBJ_FlameCore_Medium")

    flame_tiny = name(oval(s, cx + 24, cy + 18, 22, 28, FIRE), "OBJ_Flame_Tiny")
    core_tiny = name(oval(s, cx + 28, cy + 26, 12, 14, YELLOW, transparency=0.1), "OBJ_FlameCore_Tiny")

    # Glass jar — large transparent cylinder over candle
    jar = name(oval(s, cx - 70, cy - 100, 210, 280, CYAN, line=CYAN, transparency=0.82), "OBJ_Jar")
    jar.Line.Weight = 3.0
    # jar rim highlight
    rim = name(oval(s, cx - 55, cy - 95, 180, 28, WHITE, line=CYAN, transparency=0.55), "OBJ_JarRim")

    # Oxygen particles — editable ovals INSIDE the jar (named for animation)
    # Layout: cloud above flame inside jar
    particle_specs = [
        # (dx, dy, size) relative to jar interior
        (20, 30, 14), (55, 20, 12), (90, 35, 16), (130, 25, 11),
        (35, 55, 13), (75, 50, 15), (115, 60, 12), (50, 80, 10),
        (95, 85, 14), (40, 110, 11), (80, 105, 13), (120, 100, 10),
        (60, 40, 9), (100, 45, 10), (70, 70, 12), (45, 95, 9),
    ]
    particles = []
    jar_left, jar_top = cx - 70, cy - 100
    for i, (dx, dy, sz) in enumerate(particle_specs, start=1):
        p = name(
            oval(s, jar_left + dx, jar_top + dy, sz, sz, AIR, transparency=0.15),
            f"OBJ_Oxygen_{i:02d}",
        )
        particles.append(p)

    # Stage status chips (progressive disclosure — editable text)
    chip1 = name(rounded(s, 720, 120, 200, 48, WHITE, line=CYAN), "UI_Stage1")
    chip1.TextFrame.TextRange.Text = "1  Many oxygen"
    chip1.TextFrame.TextRange.Font.Name = "Aptos"
    chip1.TextFrame.TextRange.Font.Size = 14
    chip1.TextFrame.TextRange.Font.Bold = True
    chip1.TextFrame.TextRange.Font.Color.RGB = CYAN
    chip1.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    chip2 = name(rounded(s, 720, 185, 200, 48, WHITE, line=AMBER), "UI_Stage2")
    chip2.TextFrame.TextRange.Text = "2  Fewer oxygen"
    chip2.TextFrame.TextRange.Font.Name = "Aptos"
    chip2.TextFrame.TextRange.Font.Size = 14
    chip2.TextFrame.TextRange.Font.Bold = True
    chip2.TextFrame.TextRange.Font.Color.RGB = AMBER
    chip2.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    chip3 = name(rounded(s, 720, 250, 200, 48, WHITE, line=FIRE), "UI_Stage3")
    chip3.TextFrame.TextRange.Text = "3  Very few"
    chip3.TextFrame.TextRange.Font.Name = "Aptos"
    chip3.TextFrame.TextRange.Font.Size = 14
    chip3.TextFrame.TextRange.Font.Bold = True
    chip3.TextFrame.TextRange.Font.Color.RGB = FIRE
    chip3.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    chip4 = name(rounded(s, 720, 315, 200, 48, WHITE, line=WARN), "UI_Stage4")
    chip4.TextFrame.TextRange.Text = "4  Flame out"
    chip4.TextFrame.TextRange.Font.Name = "Aptos"
    chip4.TextFrame.TextRange.Font.Size = 14
    chip4.TextFrame.TextRange.Font.Bold = True
    chip4.TextFrame.TextRange.Font.Color.RGB = WARN
    chip4.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    # Smoke wisp (appears when flame out)
    smoke = name(oval(s, cx + 18, cy - 40, 30, 50, SMOKE, transparency=0.45), "OBJ_Smoke")
    smoke.Visible = -1  # visible but will start hidden via entrance later

    # Teaching caption
    caption = name(
        tb(
            s,
            "The candle uses oxygen as it burns. In a sealed jar, oxygen runs out.",
            80,
            520,
            W - 160,
            36,
            size=15,
            color=NAVY,
            bold=True,
            font="Aptos",
        ),
        "TXT_Caption",
    )

    # ---- ANIMATION ARCHITECTURE ----
    # Start visible: jar, candle, Flame_Strong, all 16 oxygen particles, Stage1 chip
    # Medium/Tiny flames, Stage2-4 chips, smoke, caption enter via Appear (hidden until then)

    # Hide later-state objects in edit view; entrance animations reveal them in slideshow
    for sh in (flame_med, core_med, flame_tiny, core_tiny, chip2, chip3, chip4, caption, smoke):
        sh.Visible = 0

    # --- CLICK 1: FEWER oxygen + flame becomes MEDIUM ---
    add_effect(s, chip2, msoAnimEffectAppear, msoAnimTriggerOnPageClick)

    wave1 = particles[0:6]
    for i, p in enumerate(wave1):
        dx = 2.0 if i % 2 == 0 else -2.0
        motion_toward_flame(s, p, dx_pct=dx, dy_pct=8.0, trigger=msoAnimTriggerWithPrevious, duration=0.55)
    for i, p in enumerate(wave1):
        trig = msoAnimTriggerAfterPrevious if i == 0 else msoAnimTriggerWithPrevious
        exit_fade(s, p, trigger=trig, duration=0.45)

    # Swap Strong → Medium
    exit_fade(s, flame_strong, trigger=msoAnimTriggerWithPrevious, duration=0.35)
    exit_fade(s, core_strong, trigger=msoAnimTriggerWithPrevious, duration=0.35)
    add_effect(s, flame_med, msoAnimEffectAppear, msoAnimTriggerWithPrevious)
    add_effect(s, core_med, msoAnimEffectAppear, msoAnimTriggerWithPrevious)

    # --- CLICK 2: VERY FEW oxygen + flame becomes TINY ---
    add_effect(s, chip3, msoAnimEffectAppear, msoAnimTriggerOnPageClick)
    wave2 = particles[6:12]
    for i, p in enumerate(wave2):
        dx = 1.5 if i % 2 == 0 else -1.5
        motion_toward_flame(s, p, dx_pct=dx, dy_pct=7.0, trigger=msoAnimTriggerWithPrevious, duration=0.55)
    for i, p in enumerate(wave2):
        trig = msoAnimTriggerAfterPrevious if i == 0 else msoAnimTriggerWithPrevious
        exit_fade(s, p, trigger=trig, duration=0.45)

    exit_fade(s, flame_med, trigger=msoAnimTriggerWithPrevious, duration=0.35)
    exit_fade(s, core_med, trigger=msoAnimTriggerWithPrevious, duration=0.35)
    add_effect(s, flame_tiny, msoAnimEffectAppear, msoAnimTriggerWithPrevious)
    add_effect(s, core_tiny, msoAnimEffectAppear, msoAnimTriggerWithPrevious)

    # --- CLICK 3: oxygen gone + FLAME OUT ---
    add_effect(s, chip4, msoAnimEffectAppear, msoAnimTriggerOnPageClick)
    wave3 = particles[12:]
    for i, p in enumerate(wave3):
        dx = 1.0 if i % 2 == 0 else -1.0
        motion_toward_flame(s, p, dx_pct=dx, dy_pct=6.0, trigger=msoAnimTriggerWithPrevious, duration=0.5)
    for i, p in enumerate(wave3):
        trig = msoAnimTriggerAfterPrevious if i == 0 else msoAnimTriggerWithPrevious
        exit_fade(s, p, trigger=trig, duration=0.4)

    exit_fade(s, flame_tiny, trigger=msoAnimTriggerWithPrevious, duration=0.45)
    exit_fade(s, core_tiny, trigger=msoAnimTriggerWithPrevious, duration=0.45)
    add_effect(s, smoke, msoAnimEffectFade, msoAnimTriggerAfterPrevious)
    add_effect(s, caption, msoAnimEffectFade, msoAnimTriggerAfterPrevious)

    # Speaker notes
    notes = (
        "TEACHER\n"
        "Click once for each stage. Pause and ask: What is happening to the oxygen? "
        "What is happening to the flame?\n\n"
        "SCIENCE\n"
        "Burning uses oxygen. In a sealed jar, oxygen is limited. When oxygen runs low, the flame goes out.\n\n"
        "SAFETY\n"
        "Teacher-only lighter/matches. Do not allow unsupervised student fire use.\n\n"
        "ANIMATION ARCHITECTURE\n"
        "Editable objects: OBJ_Jar, OBJ_Candle, OBJ_Flame_Strong/Medium/Tiny, "
        "OBJ_Oxygen_01..16, OBJ_Smoke.\n"
        "Oxygen particles use MOTION PATH then EXIT FADE.\n"
        "Flame uses discrete size states (Strong→Medium→Tiny→Out), not a static image strip."
    )
    s.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text = notes

    # Save
    if OUT.exists():
        OUT.unlink()
    pres.SaveAs(str(OUT), 24)

    # Inspect animation count + named shapes
    seq = s.TimeLine.MainSequence
    anim_count = seq.Count
    shape_names = [s.Shapes(i).Name for i in range(1, s.Shapes.Count + 1)]
    oxygen_names = [n for n in shape_names if n.startswith("OBJ_Oxygen_")]
    core_objs = [n for n in shape_names if n.startswith("OBJ_")]

    # Export preview (static first frame — note: animations play in slideshow)
    preview = PREVIEWS / "Slide08-Prototype.PNG"
    s.Export(str(preview), "PNG", 1920, 1080)

    # Write QA report
    report = PREVIEWS / "Slide08-Animation-QA.txt"
    lines = [
        f"FILE: {OUT}",
        f"SLIDES: {pres.Slides.Count}",
        f"ANIMATION_EFFECTS: {anim_count}",
        f"CORE_OBJECTS: {', '.join(core_objs)}",
        f"OXYGEN_PARTICLES: {len(oxygen_names)} ({', '.join(oxygen_names[:4])}...)",
        "",
        "SEQUENCE (click-driven):",
        "  Click 1: Stage2 + wave1 oxygen PathDown MOTION + EXIT fade + Flame Strong→Medium",
        "  Click 2: Stage3 + wave2 MOTION + EXIT + Flame Medium→Tiny",
        "  Click 3: Stage4 + wave3 MOTION + EXIT + Flame Tiny EXIT + smoke + caption",
        "",
        "VERIFY IN POWERPOINT:",
        "  1. Open file",
        "  2. Select Animation Pane",
        "  3. Confirm named shapes + Exit/Motion/Appear effects",
        "  4. Start Slideshow and click through 3 stages",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))

    # Dump first ~20 effect types for verification
    print("\nEFFECT_DUMP:")
    for i in range(1, min(anim_count, 25) + 1):
        eff = seq(i)
        try:
            shp = eff.Shape.Name
        except Exception:
            shp = "?"
        print(f"  {i:02d} effect={eff.EffectType} exit={eff.Exit} shape={shp}")

    pres.Close()
    try:
        ppt.Quit()
    except Exception:
        pass

    return anim_count, len(oxygen_names)


if __name__ == "__main__":
    n, o = build()
    assert n >= 20, f"Expected rich animation timeline, got {n}"
    assert o >= 12, f"Expected many oxygen particles, got {o}"
    print("\nPROTOTYPE OK")
