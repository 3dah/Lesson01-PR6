"""
V3 — Bright, energetic Grade 6 science PowerPoint with native animations.
Outputs:
  exports/powerpoint/The-Mystery-of-Fire-V3.pptx
  exports/pdf/The-Mystery-of-Fire-V3.pdf
Does not modify V1/V2 or HTML.
"""
from __future__ import annotations

from pathlib import Path
import win32com.client

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "exports" / "assets-v3"
PPTX = ROOT / "exports" / "powerpoint" / "The-Mystery-of-Fire-V3.pptx"
PDF = ROOT / "exports" / "pdf" / "The-Mystery-of-Fire-V3.pdf"
PREVIEWS = ROOT / "exports" / "previews-v3"

W = 13.333 * 72
H = 7.5 * 72

# Animation effect type constants (Office)
msoAnimEffectAppear = 1
msoAnimEffectFade = 10
msoAnimEffectFly = 2
msoAnimEffectWipe = 22
msoAnimEffectGrowShrink = 6
msoAnimEffectPathDown = 42
msoAnimEffectPathUp = 47
msoAnimEffectPathRight = 46
msoAnimEffectPathLeft = 45
msoAnimTriggerOnPageClick = 1
msoAnimTriggerWithPrevious = 2
msoAnimTriggerAfterPrevious = 3


def rgb(r, g, b):
    return r + (g << 8) + (b << 16)


CREAM = rgb(255, 250, 242)
SKY = rgb(232, 244, 252)
WHITE = rgb(255, 255, 255)
NAVY = rgb(24, 48, 80)
CYAN = rgb(0, 180, 220)
AIR = rgb(64, 196, 230)
FIRE = rgb(255, 140, 50)
AMBER = rgb(255, 176, 64)
GREEN = rgb(46, 180, 110)
SOFT = rgb(90, 110, 140)
WARN = rgb(230, 90, 60)


def set_bg(slide, color=CREAM):
    slide.FollowMasterBackground = False
    f = slide.Background.Fill
    f.Solid()
    f.ForeColor.RGB = color


def pic(slide, name, left, top, width, height):
    p = ASSETS / name
    if not p.exists():
        raise FileNotFoundError(p)
    return slide.Shapes.AddPicture(str(p), False, True, left, top, width, height)


def tb(slide, text, left, top, width, height, *, size=20, color=NAVY, bold=True, align=2, font="Calibri"):
    sh = slide.Shapes.AddTextbox(1, left, top, width, height)
    tr = sh.TextFrame.TextRange
    tr.Text = text
    tr.Font.Name = font
    tr.Font.Size = size
    tr.Font.Bold = bold
    tr.Font.Color.RGB = color
    tr.ParagraphFormat.Alignment = align
    sh.TextFrame.WordWrap = True
    return sh


def rounded(slide, left, top, width, height, fill, line=None):
    sh = slide.Shapes.AddShape(5, left, top, width, height)
    sh.Fill.Solid()
    sh.Fill.ForeColor.RGB = fill
    if line is None:
        sh.Line.Visible = False
    else:
        sh.Line.Visible = True
        sh.Line.ForeColor.RGB = line
        sh.Line.Weight = 1.5
    return sh


def oval(slide, left, top, width, height, fill):
    sh = slide.Shapes.AddShape(9, left, top, width, height)
    sh.Fill.Solid()
    sh.Fill.ForeColor.RGB = fill
    sh.Line.Visible = False
    return sh


def anim(slide, shape, effect=msoAnimEffectAppear, trigger=msoAnimTriggerOnPageClick):
    try:
        e = slide.TimeLine.MainSequence.AddEffect(shape, effect, 0, trigger)
        return e
    except Exception as ex:
        print("anim warn", ex)
        return None


def anim_after(slide, shape, effect=msoAnimEffectFade):
    return anim(slide, shape, effect, msoAnimTriggerAfterPrevious)


def anim_with(slide, shape, effect=msoAnimEffectFade):
    return anim(slide, shape, effect, msoAnimTriggerWithPrevious)


def notes(slide, *parts):
    labels = ["TEACHER", "SCIENCE", "QUESTION", "ANSWER", "TIP"]
    body = []
    for i, p in enumerate(parts):
        body.append(f"{labels[i] if i < len(labels) else 'NOTE'}\n{p}")
    slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text = "\n\n".join(body)


def fade_trans(slide):
    try:
        slide.SlideShowTransition.EntryEffect = 257
        slide.SlideShowTransition.Speed = 2
    except Exception:
        pass


def new(pres, bg=CREAM):
    s = pres.Slides.Add(pres.Slides.Count + 1, 12)
    set_bg(s, bg)
    fade_trans(s)
    return s


def build():
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    PPTX.parent.mkdir(parents=True, exist_ok=True)

    ppt = win32com.client.Dispatch("PowerPoint.Application")
    ppt.Visible = 1
    pres = ppt.Presentations.Add()
    pres.PageSetup.SlideWidth = W
    pres.PageSetup.SlideHeight = H

    # ========== 01 Mystery ==========
    s = new(pres, CREAM)
    # sky band
    rounded(s, 0, 0, W, 220, SKY)
    img = pic(s, "v3-01-mystery.png", 180, 140, 600, 340)
    title = tb(s, "THE MYSTERY OF FIRE", 40, 30, W - 80, 50, size=36, color=NAVY, bold=True)
    q = tb(s, "What does a flame need to keep burning?", 40, 500, W - 80, 36, size=18, color=FIRE, bold=True)
    anim(s, img, msoAnimEffectFade)
    anim_after(s, title, msoAnimEffectAppear)
    anim_after(s, q, msoAnimEffectFly)
    notes(s, "Build excitement. Pause before the question.", "Central inquiry.", "What might fire need?", "Fuel, heat, air.", "Keep energy high.")

    # ========== 02 Air ==========
    s = new(pres, SKY)
    img = pic(s, "v3-02-air.png", 40, 100, 560, 380)
    title = tb(s, "AIR IS EVERYWHERE!", 620, 140, 320, 80, size=28, color=NAVY, bold=True, align=1)
    sub = tb(s, "You can't see it — but it's there.", 620, 240, 320, 60, size=16, color=SOFT, bold=False, align=1)
    whoosh = tb(s, "WHOOSH →", 620, 320, 280, 40, size=22, color=CYAN, bold=True, align=1)
    anim(s, img, msoAnimEffectWipe)
    anim_after(s, title, msoAnimEffectAppear)
    anim_after(s, sub, msoAnimEffectFade)
    anim_after(s, whoosh, msoAnimEffectFly)
    notes(s, "Reveal airflow as a surprise.", "Air fills the space around us.", "Can invisible air affect fire?", "Yes!", "Playful whoosh moment.")

    # ========== 03 Burning process ==========
    s = new(pres, CREAM)
    tb(s, "WHAT IS BURNING?", 40, 20, W - 80, 40, size=32, color=NAVY)
    # sequential chips as shapes
    heat = rounded(s, 60, 120, 160, 70, AMBER)
    heat.TextFrame.TextRange.Text = "HEAT"
    heat.TextFrame.TextRange.Font.Bold = True
    heat.TextFrame.TextRange.Font.Size = 18
    heat.TextFrame.TextRange.Font.Color.RGB = WHITE
    heat.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    fuel = rounded(s, 260, 120, 160, 70, rgb(210, 180, 140))
    fuel.TextFrame.TextRange.Text = "FUEL"
    fuel.TextFrame.TextRange.Font.Bold = True
    fuel.TextFrame.TextRange.Font.Size = 18
    fuel.TextFrame.TextRange.Font.Color.RGB = NAVY
    fuel.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    oxy = rounded(s, 460, 120, 160, 70, CYAN)
    oxy.TextFrame.TextRange.Text = "OXYGEN"
    oxy.TextFrame.TextRange.Font.Bold = True
    oxy.TextFrame.TextRange.Font.Size = 18
    oxy.TextFrame.TextRange.Font.Color.RGB = WHITE
    oxy.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    arrow1 = tb(s, "↓", 430, 200, 80, 40, size=28, color=NAVY)
    comb = rounded(s, 300, 250, 280, 70, FIRE)
    comb.TextFrame.TextRange.Text = "COMBUSTION!"
    comb.TextFrame.TextRange.Font.Bold = True
    comb.TextFrame.TextRange.Font.Size = 20
    comb.TextFrame.TextRange.Font.Color.RGB = WHITE
    comb.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    arrow2 = tb(s, "↓", 430, 330, 80, 40, size=28, color=NAVY)
    result = rounded(s, 260, 380, 360, 70, GREEN)
    result.TextFrame.TextRange.Text = "HEAT + LIGHT"
    result.TextFrame.TextRange.Font.Bold = True
    result.TextFrame.TextRange.Font.Size = 20
    result.TextFrame.TextRange.Font.Color.RGB = WHITE
    result.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    img = pic(s, "v3-03-burning.png", 660, 100, 280, 380)
    for sh, ef in [
        (heat, msoAnimEffectFly),
        (fuel, msoAnimEffectFly),
        (oxy, msoAnimEffectFly),
        (arrow1, msoAnimEffectAppear),
        (comb, msoAnimEffectGrowShrink),
        (arrow2, msoAnimEffectAppear),
        (result, msoAnimEffectFade),
        (img, msoAnimEffectFade),
    ]:
        anim(s, sh, ef)
    notes(s, "Click through each step slowly.", "Combustion needs heat, fuel, oxygen.", "What appears after combustion?", "Heat and light.", "Make it feel like building a recipe.")

    # ========== 04 Lab time ==========
    s = new(pres, SKY)
    title = tb(s, "LET'S TEST IT!", 40, 20, W - 80, 45, size=34, color=FIRE)
    img = pic(s, "v3-04-lab.png", 200, 90, 560, 340)
    lab = tb(s, "SCIENCE LAB TIME!", 40, 450, W - 80, 36, size=18, color=CYAN, bold=True)
    items = tb(s, "Candle  ·  Jar  ·  Lid  ·  Clay  ·  Board  ·  Lighter (teacher only)", 40, 500, W - 80, 30, size=14, color=SOFT, bold=False)
    anim(s, title, msoAnimEffectFly)
    anim_after(s, img, msoAnimEffectWipe)
    anim_after(s, lab, msoAnimEffectAppear)
    anim_after(s, items, msoAnimEffectFade)
    notes(s, "Cheerful lab energy.", "Teacher-only lighter.", "Name each tool.", "Jar controls air around flame.", "Safety first.")

    # ========== 05 Setup ==========
    s = new(pres, CREAM)
    title = tb(s, "EXPERIMENT SETUP", 40, 12, W - 80, 36, size=28, color=NAVY)
    img = pic(s, "v3-05-setup.png", 40, 60, 620, 380)
    c1 = rounded(s, 690, 90, 230, 70, WHITE, CYAN)
    c1.TextFrame.TextRange.Text = "1. Candle ready"
    c1.TextFrame.TextRange.Font.Size = 14
    c1.TextFrame.TextRange.Font.Bold = True
    c1.TextFrame.TextRange.Font.Color.RGB = NAVY
    c1.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    c2 = rounded(s, 690, 180, 230, 70, WHITE, AIR)
    c2.TextFrame.TextRange.Text = "2. Jar moves over"
    c2.TextFrame.TextRange.Font.Size = 14
    c2.TextFrame.TextRange.Font.Bold = True
    c2.TextFrame.TextRange.Font.Color.RGB = CYAN
    c2.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    c3 = rounded(s, 690, 270, 230, 70, WHITE, FIRE)
    c3.TextFrame.TextRange.Text = "3. Air around flame"
    c3.TextFrame.TextRange.Font.Size = 14
    c3.TextFrame.TextRange.Font.Bold = True
    c3.TextFrame.TextRange.Font.Color.RGB = FIRE
    c3.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    tip = tb(s, "Watch how the jar traps the air around the flame!", 40, 460, W - 80, 35, size=16, color=CYAN, bold=True)
    anim(s, title, msoAnimEffectAppear)
    anim_after(s, img, msoAnimEffectWipe)
    for c in (c1, c2, c3):
        anim(s, c, msoAnimEffectFly)
    anim_after(s, tip, msoAnimEffectFade)
    notes(s, "Show jar placement.", "Openings control airflow.", "What's around the flame?", "Air.", "Clear physical setup.")

    # ========== 06 Predict ==========
    s = new(pres, CREAM)
    title = tb(s, "WHAT DO YOU THINK\nWILL HAPPEN?", 40, 15, W - 80, 70, size=30, color=NAVY)
    img = pic(s, "v3-06-predict.png", 120, 110, 720, 300)
    a = rounded(s, 80, 440, 250, 55, WHITE, FIRE)
    a.TextFrame.TextRange.Text = "A  STRONG FLAME"
    a.TextFrame.TextRange.Font.Bold = True
    a.TextFrame.TextRange.Font.Size = 14
    a.TextFrame.TextRange.Font.Color.RGB = FIRE
    a.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    b = rounded(s, 360, 440, 250, 55, WHITE, AMBER)
    b.TextFrame.TextRange.Text = "B  SMALLER FLAME"
    b.TextFrame.TextRange.Font.Bold = True
    b.TextFrame.TextRange.Font.Size = 14
    b.TextFrame.TextRange.Font.Color.RGB = AMBER
    b.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    c = rounded(s, 640, 440, 250, 55, WHITE, SOFT)
    c.TextFrame.TextRange.Text = "C  FLAME OUT"
    c.TextFrame.TextRange.Font.Bold = True
    c.TextFrame.TextRange.Font.Size = 14
    c.TextFrame.TextRange.Font.Color.RGB = SOFT
    c.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    anim(s, title, msoAnimEffectAppear)
    anim_after(s, img, msoAnimEffectFade)
    anim(s, a, msoAnimEffectFly)
    anim(s, b, msoAnimEffectFly)
    anim(s, c, msoAnimEffectFly)
    notes(s, "Class vote — suspense!", "Predict before sealing.", "Which is gradual?", "B.", "Don't confirm yet.")

    # ========== 07 Closed ==========
    s = new(pres, SKY)
    title = tb(s, "THE CLOSED JAR", 40, 18, W - 80, 40, size=30, color=NAVY)
    img = pic(s, "v3-07-closed.png", 100, 80, 650, 380)
    trap = rounded(s, 780, 220, 150, 100, WHITE, CYAN)
    trap.TextFrame.TextRange.Text = "THE AIR\nIS TRAPPED\nINSIDE"
    trap.TextFrame.TextRange.Font.Size = 13
    trap.TextFrame.TextRange.Font.Bold = True
    trap.TextFrame.TextRange.Font.Color.RGB = CYAN
    trap.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    anim(s, title, msoAnimEffectAppear)
    anim_after(s, img, msoAnimEffectWipe)
    anim_after(s, trap, msoAnimEffectFly)
    notes(s, "Emphasize trapped air.", "Closed = no renewal.", "What's trapped?", "Limited air.", "Bright lab feel.")

    # ========== 08 Watch ==========
    s = new(pres, CREAM)
    title = tb(s, "WATCH CAREFULLY!", 40, 15, W - 80, 40, size=32, color=WARN)
    img = pic(s, "v3-08-watch.png", 60, 70, 840, 360)
    seq = tb(s, "BIG FLAME  →  smaller  →  tiny  →  OUT", 40, 460, W - 80, 35, size=18, color=FIRE, bold=True)
    oxy = tb(s, "Oxygen particles decrease at the same time!", 40, 505, W - 80, 28, size=14, color=CYAN, bold=True)
    anim(s, title, msoAnimEffectAppear)
    anim_after(s, img, msoAnimEffectFade)
    anim_after(s, seq, msoAnimEffectWipe)
    anim_after(s, oxy, msoAnimEffectAppear)
    notes(s, "Narrate the shrink.", "Cause and effect.", "Instant or gradual?", "Gradual then out.", "Key observation.")

    # ========== 09 Why ==========
    s = new(pres, SKY)
    title = tb(s, "WHY DID THE FLAME GO OUT?", 40, 15, W - 80, 40, size=28, color=NAVY)
    img = pic(s, "v3-09-why.png", 40, 80, 520, 380)
    step1 = rounded(s, 590, 100, 340, 55, WHITE, CYAN)
    step1.TextFrame.TextRange.Text = "1. Oxygen near the flame"
    step1.TextFrame.TextRange.Font.Size = 14
    step1.TextFrame.TextRange.Font.Bold = True
    step1.TextFrame.TextRange.Font.Color.RGB = CYAN
    step2 = rounded(s, 590, 180, 340, 55, WHITE, AMBER)
    step2.TextFrame.TextRange.Text = "2. Oxygen gets used up"
    step2.TextFrame.TextRange.Font.Size = 14
    step2.TextFrame.TextRange.Font.Bold = True
    step2.TextFrame.TextRange.Font.Color.RGB = AMBER
    step3 = rounded(s, 590, 260, 340, 55, WHITE, FIRE)
    step3.TextFrame.TextRange.Text = "3. Flame gets weaker"
    step3.TextFrame.TextRange.Font.Size = 14
    step3.TextFrame.TextRange.Font.Bold = True
    step3.TextFrame.TextRange.Font.Color.RGB = FIRE
    step4 = rounded(s, 590, 340, 340, 55, WHITE, WARN)
    step4.TextFrame.TextRange.Text = "4. Flame goes out"
    step4.TextFrame.TextRange.Font.Size = 14
    step4.TextFrame.TextRange.Font.Bold = True
    step4.TextFrame.TextRange.Font.Color.RGB = WARN
    anim(s, title, msoAnimEffectAppear)
    anim_after(s, img, msoAnimEffectFade)
    for st in (step1, step2, step3, step4):
        anim(s, st, msoAnimEffectFly)
    notes(s, "Sync clicks with story.", "Air used up → burning stops.", "Why sealed fails?", "No fresh air.", "Teaching climax.")

    # ========== 10 Fresh gap ==========
    s = new(pres, CREAM)
    title = tb(s, "WHAT IF FRESH AIR CAN ENTER?", 40, 12, W - 80, 40, size=28, color=NAVY)
    img = pic(s, "v3-10-fresh-gap.png", 40, 70, 620, 360)
    gap = rounded(s, 690, 100, 230, 70, WHITE, CYAN)
    gap.TextFrame.TextRange.Text = "Gap at the bottom"
    gap.TextFrame.TextRange.Font.Size = 13
    gap.TextFrame.TextRange.Font.Bold = True
    gap.TextFrame.TextRange.Font.Color.RGB = CYAN
    gap.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    flow = rounded(s, 690, 190, 230, 70, WHITE, AIR)
    flow.TextFrame.TextRange.Text = "Fresh air can flow in"
    flow.TextFrame.TextRange.Font.Size = 13
    flow.TextFrame.TextRange.Font.Bold = True
    flow.TextFrame.TextRange.Font.Color.RGB = AIR
    flow.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    whoosh = rounded(s, 690, 280, 230, 80, CYAN)
    whoosh.TextFrame.TextRange.Text = "WHOOSH!"
    whoosh.TextFrame.TextRange.Font.Size = 22
    whoosh.TextFrame.TextRange.Font.Bold = True
    whoosh.TextFrame.TextRange.Font.Color.RGB = WHITE
    whoosh.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    tip = tb(s, "An opening lets new air reach the flame.", 40, 455, W - 80, 35, size=16, color=NAVY, bold=True)
    anim(s, title, msoAnimEffectAppear)
    anim_after(s, img, msoAnimEffectWipe)
    anim(s, gap, msoAnimEffectFly)
    anim(s, flow, msoAnimEffectFly)
    anim(s, whoosh, msoAnimEffectGrowShrink)
    anim_after(s, tip, msoAnimEffectFade)
    notes(s, "Discovery energy!", "Opening allows inflow.", "Does any hole guarantee forever?", "No — renewal matters.", "Exciting turn.")

    # ========== 11 Airflow ==========
    s = new(pres, SKY)
    title = tb(s, "FRESH AIR ENTERS!", 40, 12, W - 80, 40, size=32, color=CYAN)
    img = pic(s, "v3-11-airflow.png", 80, 70, 700, 360)
    l1 = rounded(s, 800, 120, 140, 50, WHITE, CYAN)
    l1.TextFrame.TextRange.Text = "FRESH AIR ↓"
    l1.TextFrame.TextRange.Font.Size = 11
    l1.TextFrame.TextRange.Font.Bold = True
    l1.TextFrame.TextRange.Font.Color.RGB = CYAN
    l1.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    l2 = rounded(s, 800, 200, 140, 50, WHITE, AIR)
    l2.TextFrame.TextRange.Text = "OXYGEN →"
    l2.TextFrame.TextRange.Font.Size = 11
    l2.TextFrame.TextRange.Font.Bold = True
    l2.TextFrame.TextRange.Font.Color.RGB = AIR
    l2.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    l3 = rounded(s, 800, 280, 140, 50, WHITE, FIRE)
    l3.TextFrame.TextRange.Text = "WARM AIR ↑"
    l3.TextFrame.TextRange.Font.Size = 11
    l3.TextFrame.TextRange.Font.Bold = True
    l3.TextFrame.TextRange.Font.Color.RGB = FIRE
    l3.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    anim(s, title, msoAnimEffectAppear)
    anim_after(s, img, msoAnimEffectFade)
    for lab in (l1, l2, l3):
        anim(s, lab, msoAnimEffectFly)
    notes(s, "Trace the loop.", "Bottom in, top out.", "Warm air direction?", "Up!", "Most exciting visual.")

    # ========== 12 Keeps burning ==========
    s = new(pres, CREAM)
    title = tb(s, "IT KEEPS BURNING!", 40, 12, W - 80, 40, size=34, color=GREEN)
    img = pic(s, "v3-12-keeps-burning.png", 40, 65, 620, 360)
    s1 = rounded(s, 690, 90, 230, 65, WHITE, CYAN)
    s1.TextFrame.TextRange.Text = "Fresh air enters"
    s1.TextFrame.TextRange.Font.Size = 13
    s1.TextFrame.TextRange.Font.Bold = True
    s1.TextFrame.TextRange.Font.Color.RGB = CYAN
    s1.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    s2 = rounded(s, 690, 175, 230, 65, WHITE, AIR)
    s2.TextFrame.TextRange.Text = "Oxygen reaches flame"
    s2.TextFrame.TextRange.Font.Size = 13
    s2.TextFrame.TextRange.Font.Bold = True
    s2.TextFrame.TextRange.Font.Color.RGB = AIR
    s2.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    s3 = rounded(s, 690, 260, 230, 65, GREEN)
    s3.TextFrame.TextRange.Text = "Flame grows strong!"
    s3.TextFrame.TextRange.Font.Size = 13
    s3.TextFrame.TextRange.Font.Bold = True
    s3.TextFrame.TextRange.Font.Color.RGB = WHITE
    s3.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    aha = tb(s, "AHA! Fresh air keeps supplying oxygen.", 40, 450, W - 80, 35, size=18, color=FIRE, bold=True)
    anim(s, title, msoAnimEffectGrowShrink)
    anim_after(s, img, msoAnimEffectFade)
    for sh in (s1, s2, s3):
        anim(s, sh, msoAnimEffectFly)
    anim_after(s, aha, msoAnimEffectAppear)
    notes(s, "Celebrate discovery!", "Continuous supply → continues burning.", "What changed?", "Air can renew.", "Payoff moment.")

    # ========== 13 Compare ==========
    s = new(pres, SKY)
    title = tb(s, "CLOSED  vs  OPEN", 40, 15, W - 80, 40, size=32, color=NAVY)
    img = pic(s, "v3-13-compare.png", 60, 70, 840, 360)
    left = tb(s, "Air runs out → OUT", 80, 450, 350, 30, size=16, color=WARN, bold=True, align=2)
    right = tb(s, "Air renewed → BURNS", 520, 450, 350, 30, size=16, color=GREEN, bold=True, align=2)
    anim(s, title, msoAnimEffectAppear)
    anim_after(s, img, msoAnimEffectWipe)
    anim(s, left, msoAnimEffectFly)
    anim(s, right, msoAnimEffectFly)
    notes(s, "Partner compare.", "Both openings help renewal.", "Which lasts?", "Open side.", "Aha comparison.")

    # ========== 14 Mechanism ==========
    s = new(pres, CREAM)
    tb(s, "WHY DOES THIS HAPPEN?", 40, 15, W - 80, 40, size=28, color=NAVY)
    parts = [
        (60, "HEAT", AMBER, WHITE),
        (220, "FUEL", rgb(210, 180, 140), NAVY),
        (380, "OXYGEN", CYAN, WHITE),
    ]
    shapes = []
    for x, label, fill, tc in parts:
        sh = rounded(s, x, 90, 140, 60, fill)
        sh.TextFrame.TextRange.Text = label
        sh.TextFrame.TextRange.Font.Bold = True
        sh.TextFrame.TextRange.Font.Size = 16
        sh.TextFrame.TextRange.Font.Color.RGB = tc
        sh.TextFrame.TextRange.ParagraphFormat.Alignment = 2
        shapes.append(sh)
    plus1 = tb(s, "+", 175, 100, 40, 40, size=24, color=NAVY)
    plus2 = tb(s, "+", 335, 100, 40, 40, size=24, color=NAVY)
    down = tb(s, "↓  COMBUSTION  ↓", 200, 170, 300, 40, size=18, color=FIRE, bold=True)
    result = rounded(s, 180, 230, 340, 60, GREEN)
    result.TextFrame.TextRange.Text = "HEAT + LIGHT"
    result.TextFrame.TextRange.Font.Bold = True
    result.TextFrame.TextRange.Font.Size = 18
    result.TextFrame.TextRange.Font.Color.RGB = WHITE
    result.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    img = pic(s, "v3-14-mechanism.png", 560, 80, 380, 400)
    for sh in shapes:
        anim(s, sh, msoAnimEffectFly)
    anim_after(s, plus1, msoAnimEffectAppear)
    anim_with(s, plus2, msoAnimEffectAppear)
    anim(s, down, msoAnimEffectAppear)
    anim(s, result, msoAnimEffectGrowShrink)
    anim_after(s, img, msoAnimEffectFade)
    notes(s, "Build the chain.", "Source-aligned definition.", "Products?", "Heat + light.", "Culmination.")

    # ========== 15 Big idea ==========
    s = new(pres, SKY)
    title = tb(s, "AIR HELPS FIRE KEEP BURNING", 40, 12, W - 80, 40, size=30, color=NAVY)
    img = pic(s, "v3-15-big-idea.png", 40, 65, 700, 380)
    tag = rounded(s, 760, 160, 170, 160, WHITE, CYAN)
    tag.TextFrame.TextRange.Text = "FRESH AIR\nKEEPS THE\nFLAME\nALIVE"
    tag.TextFrame.TextRange.Font.Size = 14
    tag.TextFrame.TextRange.Font.Bold = True
    tag.TextFrame.TextRange.Font.Color.RGB = CYAN
    tag.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    tip = tb(s, "Fresh air surrounds the flame — and keeps it burning.", 40, 465, W - 80, 35, size=16, color=NAVY, bold=True)
    anim(s, title, msoAnimEffectAppear)
    anim_after(s, img, msoAnimEffectFade)
    anim_after(s, tag, msoAnimEffectGrowShrink)
    anim_after(s, tip, msoAnimEffectFly)
    notes(s, "Let it land.", "Air is essential for continued burning.", "One sentence?", "Fire needs renewed fresh air.", "Memorable.")

    # ========== 16 Real life ==========
    s = new(pres, CREAM)
    title = tb(s, "REAL LIFE!", 40, 15, W - 80, 40, size=32, color=FIRE)
    img = pic(s, "v3-16-reallife.png", 60, 70, 840, 360)
    sub = tb(s, "Candle · Fireplace · Stove · Engine — each needs air!", 40, 460, W - 80, 35, size=16, color=CYAN, bold=True)
    anim(s, title, msoAnimEffectFly)
    anim_after(s, img, msoAnimEffectWipe)
    anim_after(s, sub, msoAnimEffectAppear)
    notes(s, "Connect to home.", "Designed airflow.", "Why chimneys?", "Warm out, fresh in.", "Exciting transfer.")

    # ========== 17 Challenge ==========
    s = new(pres, SKY)
    title = tb(s, "SCIENCE CHALLENGE!", 40, 10, W - 80, 36, size=28, color=WARN)
    q = tb(s, "WHICH ONE WILL KEEP BURNING?", 40, 48, W - 80, 32, size=20, color=NAVY, bold=True)
    img = pic(s, "v3-17-challenge.png", 40, 90, 640, 320)
    left = rounded(s, 700, 110, 220, 70, WHITE, WARN)
    left.TextFrame.TextRange.Text = "A  Closed jar"
    left.TextFrame.TextRange.Font.Size = 14
    left.TextFrame.TextRange.Font.Bold = True
    left.TextFrame.TextRange.Font.Color.RGB = WARN
    left.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    right = rounded(s, 700, 200, 220, 70, WHITE, GREEN)
    right.TextFrame.TextRange.Text = "B  Open air"
    right.TextFrame.TextRange.Font.Size = 14
    right.TextFrame.TextRange.Font.Bold = True
    right.TextFrame.TextRange.Font.Color.RGB = GREEN
    right.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    ans = rounded(s, 120, 430, 720, 55, GREEN)
    ans.TextFrame.TextRange.Text = "Answer: B — fresh air keeps coming in!"
    ans.TextFrame.TextRange.Font.Size = 15
    ans.TextFrame.TextRange.Font.Bold = True
    ans.TextFrame.TextRange.Font.Color.RGB = WHITE
    ans.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    anim(s, title, msoAnimEffectAppear)
    anim_after(s, q, msoAnimEffectFly)
    anim_after(s, img, msoAnimEffectFade)
    anim(s, left, msoAnimEffectFly)
    anim(s, right, msoAnimEffectFly)
    anim(s, ans, msoAnimEffectAppear)  # click to reveal
    notes(s, "Suspense then reveal.", "Airflow continues; sealed goes out.", "Why?", "Renewal.", "Interactive feel.")

    # ========== 18 Remember ==========
    s = new(pres, CREAM)
    title = tb(s, "REMEMBER!", 40, 15, W - 80, 40, size=32, color=NAVY)
    img = pic(s, "v3-18-remember.png", 280, 70, 400, 250)
    r1 = rounded(s, 120, 350, 720, 45, WHITE, CYAN)
    r1.TextFrame.TextRange.Text = "1.  BURNING NEEDS OXYGEN"
    r1.TextFrame.TextRange.Font.Size = 16
    r1.TextFrame.TextRange.Font.Bold = True
    r1.TextFrame.TextRange.Font.Color.RGB = NAVY
    r1.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    r2 = rounded(s, 120, 410, 720, 45, WHITE, GREEN)
    r2.TextFrame.TextRange.Text = "2.  FRESH AIR MUST BE SUPPLIED"
    r2.TextFrame.TextRange.Font.Size = 16
    r2.TextFrame.TextRange.Font.Bold = True
    r2.TextFrame.TextRange.Font.Color.RGB = GREEN
    r2.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    r3 = rounded(s, 120, 470, 720, 45, WHITE, FIRE)
    r3.TextFrame.TextRange.Text = "3.  WITHOUT FRESH AIR, THE FLAME GOES OUT"
    r3.TextFrame.TextRange.Font.Size = 16
    r3.TextFrame.TextRange.Font.Bold = True
    r3.TextFrame.TextRange.Font.Color.RGB = FIRE
    r3.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    anim(s, title, msoAnimEffectAppear)
    anim_after(s, img, msoAnimEffectFade)
    for r in (r1, r2, r3):
        anim(s, r, msoAnimEffectFly)
    notes(s, "Read slowly together.", "Three takeaways.", "What does a flame need?", "Fuel, heat, continuous fresh air.", "Strong ending.")

    # Save
    if PPTX.exists():
        PPTX.unlink()
    pres.SaveAs(str(PPTX), 24)
    n = pres.Slides.Count
    print("SAVED", PPTX, "slides=", n)
    if PDF.exists():
        PDF.unlink()
    pres.SaveAs(str(PDF), 32)
    print("PDF", PDF)
    for f in PREVIEWS.glob("*.PNG"):
        f.unlink()
    try:
        PREVIEWS.mkdir(parents=True, exist_ok=True)
        pres.Export(str(PREVIEWS), "PNG")
    except Exception as e:
        print("preview warn", e)
    pres.Close()
    try:
        ppt.Quit()
    except Exception:
        pass
    return n


def verify():
    import pymupdf
    assert PPTX.exists() and PDF.exists()
    ppt = win32com.client.Dispatch("PowerPoint.Application")
    ppt.Visible = 1
    p = ppt.Presentations.Open(str(PPTX), WithWindow=False)
    slides = p.Slides.Count
    # count animations on a few key slides
    anim_counts = []
    for i in [1, 3, 8, 11, 18]:
        try:
            anim_counts.append((i, p.Slides(i).TimeLine.MainSequence.Count))
        except Exception:
            anim_counts.append((i, -1))
    p.Close()
    try:
        ppt.Quit()
    except Exception:
        pass
    d = pymupdf.open(str(PDF))
    pages = d.page_count
    d.close()
    print("VERIFY slides", slides, "pages", pages, "anims", anim_counts)
    print("sizes", PPTX.stat().st_size, PDF.stat().st_size)
    if slides != 18 or pages != 18:
        raise RuntimeError("count fail")
    return slides, pages


if __name__ == "__main__":
    build()
    verify()
    print("V3 SUCCESS")
