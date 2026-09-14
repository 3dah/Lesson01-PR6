"""
V2 Visual Rebuild — cinematic art-directed PowerPoint via Microsoft PowerPoint COM.
Outputs:
  exports/powerpoint/The-Mystery-of-Fire-V2.pptx
  exports/pdf/The-Mystery-of-Fire-V2.pdf
Does NOT modify V1 files or the HTML experience.
"""
from __future__ import annotations

from pathlib import Path
import win32com.client

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "exports" / "assets-v2"
PPTX = ROOT / "exports" / "powerpoint" / "The-Mystery-of-Fire-V2.pptx"
PDF = ROOT / "exports" / "pdf" / "The-Mystery-of-Fire-V2.pdf"
PREVIEWS = ROOT / "exports" / "previews-v2"

SLIDE_W = 13.333 * 72
SLIDE_H = 7.5 * 72


def rgb(r, g, b):
    return r + (g << 8) + (b << 16)


BG = rgb(7, 11, 20)
AIR = rgb(94, 200, 255)
FRESH = rgb(158, 255, 240)
FIRE = rgb(255, 138, 61)
TEXT = rgb(248, 248, 246)
MUTED = rgb(200, 208, 218)
SOFT = rgb(180, 190, 205)


def set_bg(slide):
    slide.FollowMasterBackground = False
    f = slide.Background.Fill
    f.Solid()
    f.ForeColor.RGB = BG


def full_bleed(slide, filename):
    path = ASSETS / filename
    if not path.exists():
        raise FileNotFoundError(path)
    # Cover entire slide
    return slide.Shapes.AddPicture(str(path), False, True, 0, 0, SLIDE_W, SLIDE_H)


def veil(slide, top, height, darkness=0.55):
    """Semi-transparent dark band for typography legibility — not a card."""
    sh = slide.Shapes.AddShape(1, 0, top, SLIDE_W, height)  # rectangle
    sh.Fill.Solid()
    sh.Fill.ForeColor.RGB = BG
    sh.Fill.Transparency = max(0.0, min(0.85, 1.0 - darkness))
    sh.Line.Visible = False
    return sh


def textbox(slide, text, left, top, width, height, *, size=18, color=TEXT, bold=False, align=2, font="Calibri"):
    sh = slide.Shapes.AddTextbox(1, left, top, width, height)
    tr = sh.TextFrame.TextRange
    tr.Text = text
    tr.Font.Name = font
    tr.Font.Size = size
    tr.Font.Bold = bold
    tr.Font.Color.RGB = color
    tr.ParagraphFormat.Alignment = align  # 1 left 2 center 3 right
    sh.TextFrame.WordWrap = True
    return sh


def headline(slide, text, top=36, size=36):
    return textbox(slide, text, 48, top, SLIDE_W - 96, 56, size=size, color=TEXT, bold=True, align=2, font="Georgia")


def subline(slide, text, top=92, size=15, color=MUTED):
    return textbox(slide, text, 80, top, SLIDE_W - 160, 36, size=size, color=color, bold=False, align=2)


def label(slide, text, left, top, width=180, size=12, color=AIR):
    return textbox(slide, text, left, top, width, 24, size=size, color=color, bold=True, align=1)


def notes(slide, teacher, science, q, a, tip):
    slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text = (
        f"TEACHER EXPLANATION\n{teacher}\n\n"
        f"SCIENTIFIC POINT\n{science}\n\n"
        f"STUDENT QUESTION\n{q}\n\n"
        f"EXPECTED ANSWER\n{a}\n\n"
        f"TIP\n{tip}"
    )


def fade(slide):
    try:
        slide.SlideShowTransition.EntryEffect = 257
        slide.SlideShowTransition.Speed = 2
    except Exception:
        pass


def new_slide(pres):
    s = pres.Slides.Add(pres.Slides.Count + 1, 12)
    set_bg(s)
    fade(s)
    return s


def build():
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    PPTX.parent.mkdir(parents=True, exist_ok=True)
    PDF.parent.mkdir(parents=True, exist_ok=True)

    ppt = win32com.client.Dispatch("PowerPoint.Application")
    ppt.Visible = 1
    pres = ppt.Presentations.Add()
    pres.PageSetup.SlideWidth = SLIDE_W
    pres.PageSetup.SlideHeight = SLIDE_H

    # 01 Mystery
    s = new_slide(pres)
    full_bleed(s, "v2-01-mystery-flame.png")
    veil(s, 0, 130, 0.62)
    headline(s, "THE MYSTERY OF FIRE", 28, 40)
    subline(s, "What does a flame need to keep burning?", 88)
    notes(s, "Open in silence. Let the flame hold attention.", "Central investigation question.", "What might a flame need?", "Fuel, heat, air — gather ideas.", "Do not answer yet.")

    # 02 Air everywhere
    s = new_slide(pres)
    full_bleed(s, "v2-02-air-everywhere.png")
    veil(s, 0, 120, 0.58)
    headline(s, "AIR IS EVERYWHERE")
    subline(s, "You cannot see it — but it can affect fire.")
    notes(s, "Point out the space around us is filled with air.", "Air occupies space even when invisible.", "Can invisible things affect fire?", "Yes.", "Particles are a visualization aid.")

    # 03 What is burning
    s = new_slide(pres)
    full_bleed(s, "v2-03-combustion.png")
    veil(s, 0, 110, 0.55)
    headline(s, "WHAT IS BURNING?")
    subline(s, "Heat + Fuel + Oxygen  →  Combustion  →  Heat + Light")
    notes(s, "Walk the mechanism: inputs → reaction → products.", "Combustion: oxygen + substance → heat and light.", "What three things meet?", "Heat, fuel, oxygen.", "Keep Grade 6 language.")

    # 04 Let's test it
    s = new_slide(pres)
    full_bleed(s, "v2-04-still-life.png")
    veil(s, SLIDE_H - 90, 90, 0.65)
    headline(s, "LET'S TEST IT", SLIDE_H - 78, 28)
    subline(s, "Candle · Glass jar · Lid · Clay · Board · Lighter (teacher only)", SLIDE_H - 42, 13, MUTED)
    notes(s, "Name each object. Teacher-only lighter.", "Controlled experiment tools.", "Why a glass jar?", "To trap or allow air around the flame.", "Safety first.")

    # 05 Setup
    s = new_slide(pres)
    full_bleed(s, "v2-05-setup.png")
    veil(s, 0, 100, 0.5)
    headline(s, "THE EXPERIMENT")
    subline(s, "A candle. A transparent jar. Controlled openings.")
    notes(s, "Describe the physical setup.", "Bottomless jar lets us control top and bottom.", "What can we change?", "Lid on/off, gaps in clay.", "Keep apparatus large on screen.")

    # 06 Prediction
    s = new_slide(pres)
    full_bleed(s, "v2-06-prediction-states.png")
    veil(s, 0, 100, 0.58)
    headline(s, "WHAT WILL HAPPEN?")
    subline(s, "A strong   ·   B weaker   ·   C out")
    # stage labels along bottom
    veil(s, SLIDE_H - 56, 56, 0.55)
    textbox(s, "A — KEEPS BURNING", 40, SLIDE_H - 42, 280, 28, size=12, color=FIRE, bold=True, align=2)
    textbox(s, "B — BECOMES WEAKER", 320, SLIDE_H - 42, 300, 28, size=12, color=FIRE, bold=True, align=2)
    textbox(s, "C — GOES OUT", 640, SLIDE_H - 42, 260, 28, size=12, color=SOFT, bold=True, align=2)
    notes(s, "Class vote before sealing.", "Prediction before observation.", "Which shows gradual change?", "B.", "Do not confirm yet.")

    # 07 Closed jar
    s = new_slide(pres)
    full_bleed(s, "v2-07-closed-jar.png")
    veil(s, SLIDE_H - 80, 80, 0.6)
    headline(s, "THE AIR CAN'T BE REPLACED", SLIDE_H - 62, 26)
    notes(s, "Emphasize enclosure and trapped volume.", "Closed system: air cannot renew.", "What is trapped with the flame?", "A limited amount of air.", "Almost no other text — let the image speak.")

    # 08 Watch carefully
    s = new_slide(pres)
    full_bleed(s, "v2-08-watch-sequence.png")
    veil(s, 0, 90, 0.55)
    headline(s, "WATCH CAREFULLY", 24, 32)
    subline(s, "Strong  →  Weaker  →  Out", 78)
    notes(s, "Trace the sequence left to right.", "Flame weakens as available air runs low.", "Instant or gradual?", "Gradual, then out.", "Match to prediction B.")

    # 09 Why
    s = new_slide(pres)
    full_bleed(s, "v2-09-why-oxygen.png")
    veil(s, 0, 100, 0.55)
    headline(s, "WHY DID IT GO OUT?")
    subline(s, "More air → stronger flame   ·   Less air → weaker flame   ·   Air used up → out")
    notes(s, "Connect particle density to flame strength.", "In a closed jar, air is used up.", "Why can't it burn forever sealed?", "No fresh air enters.", "Avoid exact oxygen percentages.")

    # 10 Gap
    s = new_slide(pres)
    full_bleed(s, "v2-10-gap-air.png")
    veil(s, 0, 100, 0.5)
    headline(s, "WHAT IF FRESH AIR CAN ENTER?")
    subline(s, "A path for new air — but renewal still matters.")
    notes(s, "Show the gap as a doorway for air.", "Opening allows possible inflow.", "Does any hole guarantee burning forever?", "No — continuous replacement matters.", "Preview bottom-only nuance verbally.")

    # 11 Fresh air airflow
    s = new_slide(pres)
    full_bleed(s, "v2-11-airflow.png")
    veil(s, 0, 90, 0.48)
    headline(s, "FRESH AIR ENTERS")
    # annotation labels as editable text
    label(s, "FRESH AIR ↓", 60, 420, 160, 13, AIR)
    label(s, "OXYGEN → FLAME", 380, 300, 200, 13, FRESH)
    label(s, "WARM AIR ↑", 700, 140, 160, 13, FIRE)
    notes(s, "Trace bottom in → flame → top out.", "Air constantly renewed with both openings.", "Which way does warm air move?", "Up and out.", "Key teaching slide.")

    # 12 Keeps burning
    s = new_slide(pres)
    full_bleed(s, "v2-12-keeps-burning.png")
    veil(s, SLIDE_H - 100, 100, 0.58)
    headline(s, "IT KEEPS BURNING", SLIDE_H - 82, 30)
    subline(s, "Fresh air keeps supplying what the flame needs.", SLIDE_H - 42, 14)
    notes(s, "Contrast with sealed outcome.", "Continuous supply allows continued burning.", "What changed from the sealed jar?", "Air can be renewed.", "Hold on the strong flame.")

    # 13 Compare
    s = new_slide(pres)
    full_bleed(s, "v2-13-compare.png")
    veil(s, 0, 90, 0.55)
    headline(s, "CLOSED  vs  OPEN")
    textbox(s, "AIR RUNS OUT", 80, SLIDE_H - 50, 300, 28, size=13, color=SOFT, bold=True, align=2)
    textbox(s, "AIR RENEWED", SLIDE_W - 380, SLIDE_H - 50, 300, 28, size=13, color=FRESH, bold=True, align=2)
    notes(s, "Partner explain left vs right.", "Both openings support renewal in this experiment.", "Which keeps burning?", "Open / airflow side.", "Aha moment.")

    # 14 Mechanism
    s = new_slide(pres)
    full_bleed(s, "v2-14-mechanism.png")
    veil(s, 0, 110, 0.55)
    headline(s, "WHY DOES THIS HAPPEN?")
    subline(s, "FUEL + OXYGEN + HEAT  →  COMBUSTION  →  HEAT + LIGHT")
    notes(s, "Return to the definition as culmination.", "Official combustion meaning.", "What products appear?", "Heat and light.", "Keep wording source-aligned.")

    # 15 Big idea
    s = new_slide(pres)
    full_bleed(s, "v2-15-big-idea.png")
    veil(s, SLIDE_H - 110, 110, 0.6)
    headline(s, "AIR PLAYS A KEY ROLE IN BURNING", SLIDE_H - 88, 28)
    notes(s, "Pause. Let the line land.", "Air is essential for continued burning.", "One-sentence takeaway?", "Burning needs renewed fresh air.", "Calm, memorable close of concept.")

    # 16 Real life
    s = new_slide(pres)
    full_bleed(s, "v2-16-real-life.png")
    veil(s, 0, 90, 0.55)
    headline(s, "REAL LIFE")
    subline(s, "Fireplace · Candle · Stove · Engine — each needs air.")
    notes(s, "Connect to student homes.", "Designed airflow in real systems.", "Why chimneys?", "Warm air out, fresh air in.", "Concrete examples.")

    # 17 Challenge
    s = new_slide(pres)
    full_bleed(s, "v2-17-challenge.png")
    veil(s, 0, 100, 0.58)
    headline(s, "WHICH ONE WILL KEEP BURNING?")
    subline(s, "Enclosed  ·  vs  ·  Airflow")
    notes(s, "Students choose before reveal.", "Airflow side continues; sealed goes out.", "Why?", "Fresh air can be renewed.", "Formative check.")

    # 18 Remember
    s = new_slide(pres)
    full_bleed(s, "v2-18-remember.png")
    veil(s, 0, 80, 0.5)
    headline(s, "REMEMBER", 22, 28)
    # three statements as typography, not cards
    veil(s, SLIDE_H - 150, 150, 0.62)
    textbox(s, "BURNING NEEDS OXYGEN", 60, SLIDE_H - 130, SLIDE_W - 120, 28, size=16, color=TEXT, bold=True, align=2)
    textbox(s, "FRESH AIR MUST BE SUPPLIED", 60, SLIDE_H - 95, SLIDE_W - 120, 28, size=16, color=FRESH, bold=True, align=2)
    textbox(s, "WITHOUT RENEWAL, THE FLAME GOES OUT", 60, SLIDE_H - 60, SLIDE_W - 120, 28, size=16, color=FIRE, bold=True, align=2)
    notes(s, "Read the three lines slowly.", "Authoritative conclusions.", "What does a flame need to keep burning?", "Fuel, heat, continuous fresh air.", "End on the image.")

    # Save
    if PPTX.exists():
        PPTX.unlink()
    pres.SaveAs(str(PPTX), 24)
    slides = pres.Slides.Count
    print("SAVED", PPTX, "slides=", slides)

    if PDF.exists():
        PDF.unlink()
    pres.SaveAs(str(PDF), 32)
    print("PDF", PDF)

    # Previews
    for f in PREVIEWS.glob("*.PNG"):
        f.unlink()
    try:
        PREVIEWS.mkdir(parents=True, exist_ok=True)
        pres.Export(str(PREVIEWS), "PNG")
        print("PREVIEWS", PREVIEWS)
    except Exception as e:
        print("preview warn", e)

    pres.Close()
    try:
        ppt.Quit()
    except Exception:
        pass
    return slides


def verify():
    import pymupdf
    assert PPTX.exists() and PDF.exists()
    ppt = win32com.client.Dispatch("PowerPoint.Application")
    ppt.Visible = 1
    pres = ppt.Presentations.Open(str(PPTX), WithWindow=False)
    slides = pres.Slides.Count
    pres.Close()
    try:
        ppt.Quit()
    except Exception:
        pass
    doc = pymupdf.open(str(PDF))
    pages = doc.page_count
    doc.close()
    print(f"VERIFY slides={slides} pages={pages} pptx={PPTX.stat().st_size} pdf={PDF.stat().st_size}")
    if slides != 18 or pages != 18:
        raise RuntimeError(f"count fail {slides}/{pages}")
    return slides, pages


if __name__ == "__main__":
    build()
    verify()
    print("V2 SUCCESS")
