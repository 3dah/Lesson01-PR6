"""
Build The Mystery of Fire as a REAL Microsoft PowerPoint presentation via COM,
then export THAT presentation to PDF (18 slides → 18 pages).

Does not modify the HTML experience.
"""
from __future__ import annotations

import time
from pathlib import Path

import win32com.client
from win32com.client import constants

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "exports" / "assets"
PPTX_OUT = ROOT / "exports" / "powerpoint" / "The-Mystery-of-Fire.pptx"
PDF_OUT = ROOT / "exports" / "pdf" / "The-Mystery-of-Fire.pdf"
PREVIEW_DIR = ROOT / "exports" / "previews" / "pptx-slides"

# RGB as BGR integer for PowerPoint COM: R + G*256 + B*65536
def rgb(r, g, b):
    return r + (g << 8) + (b << 16)


BG = rgb(7, 11, 20)
AIR = rgb(94, 200, 255)
FRESH = rgb(158, 255, 240)
FIRE = rgb(255, 138, 61)
CORE = rgb(255, 229, 102)
MUTED = rgb(154, 166, 184)
TEXT = rgb(242, 245, 250)
WARN = rgb(226, 74, 59)
WOOD = rgb(139, 106, 69)
CLAY = rgb(47, 95, 168)
METAL = rgb(201, 162, 39)
WAX = rgb(243, 234, 216)
PANEL = rgb(16, 24, 40)

# 16:9 widescreen in points (1 inch = 72 pt)
SLIDE_W = 13.333 * 72
SLIDE_H = 7.5 * 72


def set_bg(slide):
    slide.FollowMasterBackground = False
    fill = slide.Background.Fill
    fill.Solid()
    fill.ForeColor.RGB = BG


def add_textbox(slide, text, left, top, width, height, *, size=18, color=TEXT, bold=False, align=1):
    """align: 1=left, 2=center, 3=right"""
    shape = slide.Shapes.AddTextbox(1, left, top, width, height)  # msoTextOrientationHorizontal=1
    tf = shape.TextFrame
    tf.WordWrap = True
    tr = tf.TextRange
    tr.Text = text
    tr.Font.Name = "Calibri"
    tr.Font.Size = size
    tr.Font.Bold = bold
    tr.Font.Color.RGB = color
    tr.ParagraphFormat.Alignment = align
    return shape


def add_kicker(slide, text):
    return add_textbox(slide, text.upper(), 40, 18, SLIDE_W - 80, 28, size=12, color=AIR, bold=True, align=2)


def add_title(slide, text, top=50, size=32):
    return add_textbox(slide, text, 40, top, SLIDE_W - 80, 60, size=size, color=TEXT, bold=True, align=2)


def add_sub(slide, text, top=110):
    return add_textbox(slide, text, 80, top, SLIDE_W - 160, 50, size=15, color=MUTED, bold=False, align=2)


def add_picture(slide, name, left, top, width, height=None):
    path = ASSETS / name
    if not path.exists():
        print("MISSING asset:", path)
        return None
    if height:
        return slide.Shapes.AddPicture(str(path), False, True, left, top, width, height)
    return slide.Shapes.AddPicture(str(path), False, True, left, top, width)


def add_notes(slide, teacher, science, question, answer, tip):
    slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text = (
        f"TEACHER EXPLANATION\n{teacher}\n\n"
        f"SCIENTIFIC POINT\n{science}\n\n"
        f"SUGGESTED STUDENT QUESTION\n{question}\n\n"
        f"EXPECTED ANSWER\n{answer}\n\n"
        f"TEACHING TIP\n{tip}"
    )


def add_rounded_rect(slide, left, top, width, height, fill, line=None):
    # msoShapeRoundedRectangle = 5
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


def choice_row(slide, letter, text, top, accent=AIR):
    circ = slide.Shapes.AddShape(9, 100, top, 36, 36)  # oval
    circ.Fill.Solid()
    circ.Fill.ForeColor.RGB = accent
    circ.Line.Visible = False
    circ.TextFrame.TextRange.Text = letter
    circ.TextFrame.TextRange.Font.Bold = True
    circ.TextFrame.TextRange.Font.Size = 14
    circ.TextFrame.TextRange.Font.Color.RGB = BG
    circ.TextFrame.TextRange.ParagraphFormat.Alignment = 2

    row = add_rounded_rect(slide, 150, top, 660, 40, PANEL, accent)
    row.TextFrame.TextRange.Text = "  " + text
    row.TextFrame.TextRange.Font.Size = 15
    row.TextFrame.TextRange.Font.Color.RGB = TEXT
    row.TextFrame.TextRange.Font.Name = "Calibri"
    return row


def fade_transition(slide):
    try:
        slide.SlideShowTransition.EntryEffect = 257  # ppEffectFade
        slide.SlideShowTransition.Speed = 2  # medium
    except Exception:
        pass


def draw_apparatus(slide, left, top, *, lid=True, gaps=False, flame=True, label=""):
    board = add_rounded_rect(slide, left, top + 160, 180, 18, WOOD)
    clay = slide.Shapes.AddShape(9, left + 50, top + 148, 80, 24)
    clay.Fill.Solid()
    clay.Fill.ForeColor.RGB = CLAY
    clay.Line.Visible = False
    if gaps:
        for dx in (40, 120):
            g = slide.Shapes.AddShape(9, left + dx, top + 152, 20, 16)
            g.Fill.Solid()
            g.Fill.ForeColor.RGB = BG
            g.Line.Visible = False
    candle = add_rounded_rect(slide, left + 78, top + 100, 24, 50, WAX)
    if flame:
        fl = slide.Shapes.AddShape(7, left + 78, top + 70, 24, 36)  # isosceles triangle
        fl.Fill.Solid()
        fl.Fill.ForeColor.RGB = FIRE
        fl.Line.Visible = False
    jar = add_rounded_rect(slide, left + 35, top + 40, 110, 130, PANEL, AIR)
    jar.Fill.Transparency = 0.35
    if lid:
        add_rounded_rect(slide, left + 28, top + 30, 124, 14, METAL)
    if label:
        add_textbox(slide, label, left, top + 185, 180, 24, size=12, color=MUTED, align=2)


def build():
    PPTX_OUT.parent.mkdir(parents=True, exist_ok=True)
    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

    # Ensure diagrams exist
    if not (ASSETS / "hero-flame.png").exists():
        import subprocess, sys
        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "generate_diagrams.py")], cwd=str(ROOT))

    ppt = win32com.client.Dispatch("PowerPoint.Application")
    ppt.Visible = 1
    # ppLayoutBlank = 12
    pres = ppt.Presentations.Add()
    pres.PageSetup.SlideWidth = SLIDE_W
    pres.PageSetup.SlideHeight = SLIDE_H

    def new_slide():
        # WithWindow custom layout blank: use layout 12
        s = pres.Slides.Add(pres.Slides.Count + 1, 12)
        set_bg(s)
        fade_transition(s)
        return s

    # ---- 1 Cover ----
    s = new_slide()
    add_kicker(s, "Interactive Science Experience  ·  Grade 6")
    add_title(s, "The Mystery of Fire", top=70, size=40)
    add_sub(s, "What does a flame need to keep burning?", top=140)
    add_textbox(s, "The Role of Air in Burning Things", 40, 190, SLIDE_W - 80, 30, size=16, color=FIRE, bold=True, align=2)
    add_picture(s, "hero-flame.png", 180, 230, 600, 280)
    add_notes(s,
        "Welcome students. Dim lights if possible. Show the title without answering yet.",
        "Tonight we investigate the role of air in burning.",
        "What do you already think a flame needs to keep burning?",
        "Fuel, heat, air/oxygen — accept all ideas for now.",
        "Protect the mystery; do not reveal conclusions yet.")

    # ---- 2 Mystery ----
    s = new_slide()
    add_kicker(s, "Chapter 01  ·  The Mystery")
    add_title(s, "What does a flame need to keep burning?")
    add_sub(s, "Air is all around us — invisible, but powerful.")
    add_picture(s, "hero-flame.png", 140, 170, 680, 340)
    add_notes(s,
        "Let students watch the flame image quietly.",
        "Air is invisible but may still matter for fire.",
        "Can something we cannot see still affect fire?",
        "Yes — air can affect fire even though we cannot see it.",
        "Invite predictions without judging correctness.")

    # ---- 3 Invisible air ----
    s = new_slide()
    add_kicker(s, "Chapter 02  ·  Invisible Air")
    add_title(s, "Air is everywhere.")
    add_sub(s, "You cannot see it. But can something invisible affect a flame?")
    add_picture(s, "air-hidden.png", 40, 170, 430, 300)
    add_picture(s, "air-revealed.png", 490, 170, 430, 300)
    add_textbox(s, "Before", 40, 480, 430, 24, size=12, color=MUTED, align=2)
    add_textbox(s, "Revealed", 490, 480, 430, 24, size=12, color=FRESH, align=2)
    add_notes(s,
        "Reveal the right image after discussion.",
        "Cyan particles visualize air — not literal colored air.",
        "If air is invisible, how can we study it?",
        "By observing effects when air is trapped or renewed.",
        "Emphasize visualization vs. literal colored air.")

    # ---- 4 Focus question ----
    s = new_slide()
    add_kicker(s, "Focus Question")
    add_title(s, "Can air affect fire?", size=36)
    add_sub(s, "Let's test it with a careful classroom experiment.")
    add_picture(s, "hero-flame.png", 220, 180, 520, 300)
    add_notes(s,
        "Transition from wonder to investigation.",
        "Experiments help us test ideas about invisible air.",
        "What equipment might help us trap or release air around a flame?",
        "Jar, lid, clay, candle — ways to control openings.",
        "Preview safety: teacher lights the candle.")

    # ---- 5 Experiment ----
    s = new_slide()
    add_kicker(s, "Chapter 03  ·  Experiment")
    add_title(s, "Build the investigation.")
    add_sub(s, "Board · Clay · Candle · Bottomless glass jar · Metal lid · Lighter (teacher only)")
    add_picture(s, "experiment-setup.png", 60, 160, 840, 300)
    warn = add_rounded_rect(s, 120, 480, 720, 36, rgb(42, 18, 20), WARN)
    warn.TextFrame.TextRange.Text = "Caution: Only the teacher should use the lighter to light the candle."
    warn.TextFrame.TextRange.Font.Size = 13
    warn.TextFrame.TextRange.Font.Color.RGB = rgb(255, 194, 188)
    warn.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    add_notes(s,
        "Assemble materials visibly. Assign observation roles.",
        "The jar is bottomless so we can control top and bottom openings.",
        "Why must only the teacher use the lighter?",
        "Fire safety — adults handle ignition.",
        "Keep clay ready for making bottom gaps later.")

    # ---- 6 Prediction ----
    s = new_slide()
    add_kicker(s, "Chapter 04  ·  Predict")
    add_title(s, "What do you think will happen?")
    add_sub(s, "If we seal the jar with a metal lid…")
    choice_row(s, "A", "The flame keeps burning the same.", 180)
    choice_row(s, "B", "The flame becomes weaker, then may go out.", 240, FIRE)
    choice_row(s, "C", "The flame goes out right away.", 300)
    add_textbox(s, "Vote as a class — then continue to test.", 40, 380, SLIDE_W - 80, 30, size=14, color=MUTED, align=2)
    add_notes(s,
        "Poll the room. Record votes without revealing the answer.",
        "We are about to trap air with the candle.",
        "Which choice matches a gradual change?",
        "B suggests gradual weakening.",
        "Do not confirm yet — discovery comes after observation.")

    # ---- 7 Closed jar ----
    s = new_slide()
    add_kicker(s, "Chapter 05  ·  The Closed Jar")
    add_title(s, "Trap the air.")
    add_sub(s, "Place the metal lid. Watch the air inside — and the flame.")
    add_picture(s, "sealed-1.png", 100, 160, 760, 340)
    add_notes(s,
        "Demonstrate sealing carefully.",
        "In a closed jar, air cannot be renewed from outside.",
        "What do you notice first — the flame or the air?",
        "Flame may look normal at first, then weaken.",
        "Ask students to time how long until change is visible.")

    # ---- 8 Flame out ----
    s = new_slide()
    add_kicker(s, "Chapter 06  ·  Observation")
    add_title(s, "The flame goes out.")
    add_sub(s, "The flame gradually weakens… then the candle goes out after a short time.")
    add_picture(s, "oxygen-strip.png", 40, 170, 880, 280)
    add_textbox(s, "Prediction check: B matches the observation best.", 40, 470, SLIDE_W - 80, 30, size=15, color=FRESH, bold=True, align=2)
    add_notes(s,
        "Walk the strip: full → used → almost gone → out.",
        "Available air decreases; flame strength falls with it.",
        "Did the flame die instantly or gradually?",
        "Gradually — then it went out.",
        "Connect back to student predictions kindly.")

    # ---- 9 Why ----
    s = new_slide()
    add_kicker(s, "Chapter 07  ·  Why?")
    add_title(s, "The air inside was used up.")
    add_sub(s, "In a closed jar, the air is used up. Once it runs out, the candle goes out.")
    for i, name in enumerate(["sealed-1.png", "sealed-2.png", "sealed-3.png", "sealed-4.png"]):
        add_picture(s, name, 20 + i * 235, 170, 220, 280)
    add_notes(s,
        "Walk left to right through the four frames.",
        "Closed system → air used up → burning stops.",
        "Why can't the candle keep burning forever under the lid?",
        "Fresh air cannot enter to replace used air.",
        "Avoid claiming exact oxygen percentages for Grade 6.")

    # ---- 10 Fresh air ----
    s = new_slide()
    add_kicker(s, "Chapter 08  ·  Fresh Air")
    add_title(s, "Fresh air in. Warm air out.")
    add_sub(s, "Gap at the bottom + opening at the top → air is constantly renewed.")
    add_picture(s, "airflow.png", 80, 155, 800, 350)
    add_notes(s,
        "Trace cyan arrows in, warm arrows out.",
        "Continuous renewal of air allows burning to continue.",
        "Which way does warm air tend to move?",
        "Upward — out the top opening.",
        "Introduce renew / replace gently.")

    # ---- 11 Bottom only ----
    s = new_slide()
    add_kicker(s, "Experiment nuance")
    add_title(s, "Bottom gap alone is not enough.")
    add_sub(s, "Lid on + small bottom gap → flame goes out after a slightly longer time.")
    add_picture(s, "bottom-only.png", 80, 155, 800, 350)
    add_notes(s,
        "Prevent the misconception that one opening is enough.",
        "Without a top exit, air cannot circulate well enough.",
        "Why might it last a little longer than fully sealed?",
        "A little air can enter — but not enough continuous renewal.",
        "Keep language Grade 6: renew, openings, continue burning.")

    # ---- 12 Aha compare ----
    s = new_slide()
    add_kicker(s, "Chapter 09  ·  The Aha Moment")
    add_title(s, "Closed vs. airflow.")
    add_sub(s, "Sealed air runs out. Continuous fresh air keeps burning going.")
    add_picture(s, "compare.png", 50, 155, 860, 350)
    add_notes(s,
        "Have students explain the difference to a partner.",
        "Both top and bottom openings matter for renewal in this setup.",
        "Which side would you use to keep a flame alive longer?",
        "The airflow side.",
        "Celebrate the aha — this is the core discovery.")

    # ---- 13 Editable shapes ----
    s = new_slide()
    add_kicker(s, "Diagram  ·  Editable shapes")
    add_title(s, "Build the science with shapes.")
    add_sub(s, "Closed (left) vs airflow (right) — PowerPoint objects you can edit.")
    draw_apparatus(s, 160, 160, lid=True, gaps=False, flame=False, label="CLOSED")
    draw_apparatus(s, 620, 160, lid=False, gaps=True, flame=True, label="AIRFLOW")
    # arrows
    a1 = s.Shapes.AddShape(33, 600, 320, 28, 40)  # down arrow-ish / right
    a1.Fill.Solid(); a1.Fill.ForeColor.RGB = FRESH; a1.Line.Visible = False
    a2 = s.Shapes.AddShape(1, 700, 120, 24, 40)  # up arrow
    a2.Fill.Solid(); a2.Fill.ForeColor.RGB = rgb(255, 176, 112); a2.Line.Visible = False
    add_notes(s,
        "Ungroup/edit these shapes live with students if useful.",
        "Visual model of chimney-style airflow.",
        "What do the cyan arrows mean? The warm arrow?",
        "Fresh air entering; warm air leaving.",
        "Keep editable — do not flatten this slide to a picture.")

    # ---- 14 Science ----
    s = new_slide()
    add_kicker(s, "Chapter 10  ·  The Science")
    add_title(s, "What is meant by burning?")
    add_sub(s, "A reaction between oxygen and a substance that produces heat and light.")
    chips = [("Fuel", rgb(240, 215, 176)), ("+", MUTED), ("Oxygen", AIR), ("+", MUTED), ("Heat", FIRE), ("→", MUTED), ("Heat + Light", CORE)]
    x = 70
    for label, col in chips:
        if label in ("+", "→"):
            add_textbox(s, label, x, 220, 40, 40, size=22, color=col, bold=True, align=2)
            x += 45
        else:
            chip = add_rounded_rect(s, x, 210, 120, 50, PANEL, col)
            chip.TextFrame.TextRange.Text = label
            chip.TextFrame.TextRange.Font.Size = 16
            chip.TextFrame.TextRange.Font.Color.RGB = col
            chip.TextFrame.TextRange.ParagraphFormat.Alignment = 2
            x += 135
    add_picture(s, "combustion.png", 100, 290, 760, 220)
    add_notes(s,
        "Read the definition aloud together.",
        "Combustion: oxygen + substance → heat + light.",
        "Is oxygen the only thing needed?",
        "No — also a substance (fuel) and conditions for the reaction (heat).",
        "Keep the official definition wording close to the source lesson.")

    # ---- 15 Real world ----
    s = new_slide()
    add_kicker(s, "Chapter 11  ·  Real World")
    add_title(s, "Where do we see this?")
    add_sub(s, "Burning needs a continuous supply of fresh air.")
    add_picture(s, "real-world.png", 60, 155, 840, 300)
    add_textbox(s, "Candle · Fireplace · Gas stove · Engine", 40, 470, SLIDE_W - 80, 30, size=14, color=MUTED, align=2)
    add_notes(s,
        "Ask for local examples (campfire, kitchen, heater).",
        "Real systems are designed so air can renew.",
        "Why do fireplaces have chimneys?",
        "To let warm air out so fresh air can enter.",
        "Keep connections concrete for Grade 6.")

    # ---- 16 Challenge ----
    s = new_slide()
    add_kicker(s, "Chapter 12  ·  Science Challenge")
    add_title(s, "Which candle burns longer?")
    add_sub(s, "Choose carefully — then reveal.")
    choice_row(s, "A", "Candle A — jar sealed with a lid, no gaps.", 180)
    choice_row(s, "B", "Candle B — lid on, but a small gap only at the bottom.", 240)
    choice_row(s, "C", "Candle C — gap at the bottom and open at the top.", 300, FRESH)
    ans = add_rounded_rect(s, 100, 380, 760, 50, rgb(14, 32, 36), FRESH)
    ans.TextFrame.TextRange.Text = "Answer: C — both openings renew air so burning can continue."
    ans.TextFrame.TextRange.Font.Size = 16
    ans.TextFrame.TextRange.Font.Bold = True
    ans.TextFrame.TextRange.Font.Color.RGB = FRESH
    ans.TextFrame.TextRange.ParagraphFormat.Alignment = 2
    add_textbox(s, "B lasts a bit longer than A, but still goes out.", 40, 450, SLIDE_W - 80, 28, size=13, color=MUTED, align=2)
    # Appear animation on answer if possible
    try:
        eff = s.TimeLine.MainSequence.AddEffect(ans, 1)  # msoAnimEffectAppear
    except Exception:
        pass
    add_notes(s,
        "Hide/reveal the answer when presenting live.",
        "Correct: both openings (bottom + top).",
        "Why isn't B good enough?",
        "Bottom-only gap still cannot fully renew air with the lid on.",
        "Use as formative check before conclusions.")

    # ---- 17 Conclusions ----
    s = new_slide()
    add_kicker(s, "Final Discovery")
    add_title(s, "Air plays an important role in burning.")
    add_sub(s, "Fresh air must continuously be supplied for burning to continue.")
    conclusions = [
        "1. Air has a role in burning.",
        "2. Fresh air must constantly flow in and out for burning to continue.",
        "3. Where air is not renewed, things cannot continue burning.",
    ]
    for i, text in enumerate(conclusions):
        pill = add_rounded_rect(s, 90, 180 + i * 80, 780, 60, rgb(14, 26, 42), AIR)
        pill.TextFrame.TextRange.Text = "  " + text
        pill.TextFrame.TextRange.Font.Size = 16
        pill.TextFrame.TextRange.Font.Color.RGB = TEXT
    add_notes(s,
        "Read each conclusion slowly. Ask students to restate in their own words.",
        "These three statements are the authoritative lesson takeaways.",
        "Can you give one sentence that captures all three?",
        "Burning needs fresh air renewed; without renewal, fire stops.",
        "Post these on the board for the rest of the week.")

    # ---- 18 Remember ----
    s = new_slide()
    add_kicker(s, "Remember")
    add_title(s, "Investigation complete.")
    add_sub(s, "Air is invisible — but essential for a flame to keep burning.")
    add_picture(s, "compare.png", 100, 160, 760, 280)
    add_textbox(s, "Fuel + Oxygen + Heat  →  Heat + Light", 40, 460, SLIDE_W - 80, 30, size=16, color=FIRE, bold=True, align=2)
    add_notes(s,
        "Close by returning to the opening question — now students can answer it.",
        "Air (with oxygen) is required for continued burning; renewal matters.",
        "What does a flame need to keep burning?",
        "Fuel, heat, and a continuous supply of fresh air (oxygen).",
        "Optional: replay the HTML experience as a station rotation.")

    # Save PPTX
    if PPTX_OUT.exists():
        PPTX_OUT.unlink()
    # ppSaveAsOpenXMLPresentation = 24
    pres.SaveAs(str(PPTX_OUT), 24)
    slide_count = pres.Slides.Count
    print(f"SAVED PPTX: {PPTX_OUT} slides={slide_count}")

    if slide_count != 18:
        raise RuntimeError(f"Expected 18 slides, got {slide_count}")

    # Export THAT presentation to PDF via PowerPoint
    if PDF_OUT.exists():
        PDF_OUT.unlink()
    # ppSaveAsPDF = 32
    pres.SaveAs(str(PDF_OUT), 32)
    print(f"EXPORTED PDF: {PDF_OUT}")

    # Preview thumbnails
    try:
        for f in PREVIEW_DIR.glob("*.PNG"):
            f.unlink()
        pres.Export(str(PREVIEW_DIR), "PNG")
        print("PREVIEW exported to", PREVIEW_DIR)
    except Exception as e:
        print("Preview export warning:", e)

    # Close
    pres.Close()
    # Leave PowerPoint running? Quit to clean up.
    try:
        ppt.Quit()
    except Exception:
        pass

    return slide_count


def verify():
    import time
    time.sleep(0.5)
    assert PPTX_OUT.exists(), f"Missing {PPTX_OUT}"
    assert PDF_OUT.exists(), f"Missing {PDF_OUT}"
    pptx_size = PPTX_OUT.stat().st_size
    pdf_size = PDF_OUT.stat().st_size
    assert pptx_size > 50_000, f"PPTX too small: {pptx_size}"
    assert pdf_size > 50_000, f"PDF too small: {pdf_size}"

    # Reopen PPTX in PowerPoint to count slides
    ppt = win32com.client.Dispatch("PowerPoint.Application")
    ppt.Visible = 1
    pres = ppt.Presentations.Open(str(PPTX_OUT), WithWindow=False)
    slides = pres.Slides.Count
    pres.Close()
    try:
        ppt.Quit()
    except Exception:
        pass

    # Count PDF pages
    import pymupdf
    doc = pymupdf.open(str(PDF_OUT))
    pages = doc.page_count
    doc.close()

    print("VERIFY pptx_exists=True pdf_exists=True")
    print(f"VERIFY slides={slides} pdf_pages={pages}")
    print(f"VERIFY pptx_bytes={pptx_size} pdf_bytes={pdf_size}")
    if slides != 18 or pages != 18:
        raise RuntimeError(f"Count mismatch: slides={slides} pages={pages}")
    return slides, pages


if __name__ == "__main__":
    build()
    slides, pages = verify()
    print("SUCCESS", slides, pages)
