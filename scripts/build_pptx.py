"""Build premium editable PPTX from the Mystery of Fire experience."""
from __future__ import annotations

from pathlib import Path
from copy import deepcopy

from pptx import Presentation
from pptx.util import Inches, Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "exports" / "assets"
OUT = ROOT / "exports" / "powerpoint" / "The-Mystery-of-Fire.pptx"

# Visual system (RGB)
BG = RGBColor(0x07, 0x0B, 0x14)
BG2 = RGBColor(0x0A, 0x12, 0x24)
AIR = RGBColor(0x5E, 0xC8, 0xFF)
OXYGEN = RGBColor(0x7A, 0xD7, 0xFF)
FRESH = RGBColor(0x9E, 0xFF, 0xF0)
FIRE = RGBColor(0xFF, 0x8A, 0x3D)
CORE = RGBColor(0xFF, 0xE5, 0x66)
MUTED = RGBColor(0x9A, 0xA6, 0xB8)
TEXT = RGBColor(0xF2, 0xF5, 0xFA)
WARN = RGBColor(0xE2, 0x4A, 0x3B)
WARM = RGBColor(0xFF, 0xB0, 0x70)
CLAY = RGBColor(0x2F, 0x5F, 0xA8)
WOOD = RGBColor(0x8B, 0x6A, 0x45)
METAL = RGBColor(0xC9, 0xA2, 0x27)
WAX = RGBColor(0xF3, 0xEA, 0xD8)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def set_slide_bg(slide, color=BG):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    # send to back
    spTree = slide.shapes._spTree
    sp = bg._element
    spTree.remove(sp)
    spTree.insert(2, sp)
    return bg


def add_text(slide, text, left, top, width, height, *, size=18, color=TEXT, bold=False, font="Sora", align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font
    try:
        tf._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}.get(anchor, "t"))
    except Exception:
        pass
    return box


def add_kicker(slide, text):
    return add_text(slide, text.upper(), Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35), size=11, color=AIR, bold=True, font="Sora", align=PP_ALIGN.CENTER)


def add_title(slide, text, top=Inches(0.65), size=32):
    return add_text(slide, text, Inches(0.8), top, Inches(11.7), Inches(0.9), size=size, color=TEXT, bold=True, font="Georgia", align=PP_ALIGN.CENTER)


def add_sub(slide, text, top=Inches(1.45)):
    return add_text(slide, text, Inches(1.5), top, Inches(10.3), Inches(0.7), size=14, color=MUTED, font="Sora", align=PP_ALIGN.CENTER)


def add_image(slide, name, left, top, width, height=None):
    path = ASSETS / name
    if not path.exists():
        return None
    if height:
        return slide.shapes.add_picture(str(path), left, top, width=width, height=height)
    return slide.shapes.add_picture(str(path), left, top, width=width)


def add_notes(slide, teacher: str, science: str, question: str, answer: str, tip: str):
    notes = slide.notes_slide
    tf = notes.notes_text_frame
    tf.text = (
        f"TEACHER EXPLANATION\n{teacher}\n\n"
        f"SCIENTIFIC POINT\n{science}\n\n"
        f"SUGGESTED STUDENT QUESTION\n{question}\n\n"
        f"EXPECTED ANSWER\n{answer}\n\n"
        f"TEACHING TIP\n{tip}"
    )


def pill(slide, text, left, top, width, height, fill, line_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line_color
    shape.line.width = Pt(1.5)
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = text
    run.font.size = Pt(14)
    run.font.color.rgb = TEXT
    run.font.name = "Sora"
    return shape


def choice_row(slide, letter, text, top, accent=AIR, highlight=False):
    # letter circle
    circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.6), top, Inches(0.45), Inches(0.45))
    circ.fill.solid()
    circ.fill.fore_color.rgb = accent
    circ.line.fill.background()
    tf = circ.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = letter
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = BG
    r.font.name = "Sora"
    # body
    fill = RGBColor(0x12, 0x2A, 0x28) if highlight else RGBColor(0x10, 0x18, 0x28)
    return pill(slide, f"  {text}", Inches(2.2), top, Inches(8.8), Inches(0.55), fill, accent)


def add_appear_animation(slide, shape, order: int):
    """Add a simple Appear animation via OOXML timing."""
    try:
        sp_id = shape._element.get("id") or shape._element.find(qn("p:cNvPr")).get("id")
    except Exception:
        cNvPr = shape._element.find(".//" + qn("p:cNvPr"))
        if cNvPr is None:
            return
        sp_id = cNvPr.get("id")

    timing_xml = f"""
    <p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
              xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
      <p:tnLst>
        <p:par>
          <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
            <p:childTnLst>
              <p:seq concurrent="1" nextAc="seek">
                <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
                  <p:childTnLst>
                    <p:par>
                      <p:cTn id="{10 + order}" fill="hold">
                        <p:stCondLst>
                          <p:cond delay="{order * 500}"/>
                        </p:stCondLst>
                        <p:childTnLst>
                          <p:par>
                            <p:cTn id="{100 + order}" fill="hold">
                              <p:stCondLst>
                                <p:cond delay="0"/>
                              </p:stCondLst>
                              <p:childTnLst>
                                <p:animEffect transition="in" filter="fade">
                                  <p:cBhvr>
                                    <p:cTn id="{200 + order}" dur="500"/>
                                    <p:tgtEl>
                                      <p:spTgt spid="{sp_id}"/>
                                    </p:tgtEl>
                                  </p:cBhvr>
                                </p:animEffect>
                              </p:childTnLst>
                            </p:cTn>
                          </p:par>
                        </p:childTnLst>
                      </p:cTn>
                    </p:par>
                  </p:childTnLst>
                </p:cTn>
              </p:seq>
            </p:childTnLst>
          </p:cTn>
        </p:par>
      </p:tnLst>
    </p:timing>
    """
    # Merge carefully: only set if no timing exists
    sld = slide._element
    existing = sld.find(qn("p:timing"))
    if existing is not None:
        return
    try:
        sld.append(parse_xml(timing_xml))
    except Exception:
        pass


def add_fade_transition(slide):
    sld = slide._element
    tr = parse_xml(
        '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med">'
        '<p:fade/></p:transition>'
    )
    existing = sld.find(qn("p:transition"))
    if existing is not None:
        sld.remove(existing)
    # insert before timing if any
    timing = sld.find(qn("p:timing"))
    if timing is not None:
        timing.addprevious(tr)
    else:
        sld.append(tr)


def draw_mini_apparatus(slide, left, top, *, lid=True, gaps=False, flame_on=True, label=""):
    """Editable PowerPoint shapes approximating the experiment."""
    # board
    board = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top + Inches(2.2), Inches(2.4), Inches(0.22))
    board.fill.solid()
    board.fill.fore_color.rgb = WOOD
    board.line.fill.background()
    # clay
    clay = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.7), top + Inches(2.05), Inches(1.0), Inches(0.28))
    clay.fill.solid()
    clay.fill.fore_color.rgb = CLAY
    clay.line.fill.background()
    if gaps:
        for dx in (0.55, 1.55):
            g = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(dx), top + Inches(2.08), Inches(0.28), Inches(0.2))
            g.fill.solid()
            g.fill.fore_color.rgb = BG
            g.line.fill.background()
    # candle
    candle = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(1.05), top + Inches(1.45), Inches(0.3), Inches(0.65))
    candle.fill.solid()
    candle.fill.fore_color.rgb = WAX
    candle.line.fill.background()
    if flame_on:
        flame = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, left + Inches(1.05), top + Inches(1.05), Inches(0.3), Inches(0.45))
        flame.fill.solid()
        flame.fill.fore_color.rgb = FIRE
        flame.line.fill.background()
        core = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, left + Inches(1.1), top + Inches(1.2), Inches(0.2), Inches(0.28))
        core.fill.solid()
        core.fill.fore_color.rgb = CORE
        core.line.fill.background()
    # jar
    jar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.45), top + Inches(0.55), Inches(1.5), Inches(1.7))
    jar.fill.solid()
    jar.fill.fore_color.rgb = RGBColor(0x18, 0x28, 0x38)
    jar.fill.fore_color.rgb = RGBColor(0x14, 0x22, 0x32)
    # make semi via line only look — use soft fill
    jar.line.color.rgb = OXYGEN
    jar.line.width = Pt(1.5)
    if lid:
        lid_s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.35), top + Inches(0.42), Inches(1.7), Inches(0.18))
        lid_s.fill.solid()
        lid_s.fill.fore_color.rgb = METAL
        lid_s.line.fill.background()
    if label:
        add_text(slide, label, left, top + Inches(2.55), Inches(2.4), Inches(0.3), size=11, color=MUTED, align=PP_ALIGN.CENTER)
    return jar


def build():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank = prs.slide_layouts[6]

    # 1 Cover
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_image(s, "title-bg.png", Inches(2.5), Inches(3.6), Inches(8.3), Inches(3.6))
    add_kicker(s, "Interactive Science Experience  ·  Grade 6")
    add_title(s, "The Mystery of Fire", top=Inches(1.5), size=44)
    add_sub(s, "What does a flame need to keep burning?", top=Inches(2.5))
    add_text(s, "The Role of Air in Burning Things", Inches(0.8), Inches(3.15), Inches(11.7), Inches(0.4), size=16, color=FIRE, bold=True, align=PP_ALIGN.CENTER)
    add_fade_transition(s)
    add_notes(
        s,
        "Welcome students. Dim lights if possible. Show the title and the central question without answering it yet.",
        "Burning needs a continuous relationship with air — tonight we investigate that.",
        "What do you already think a flame needs to keep burning?",
        "Students may say fuel, wood, wax, heat, oxygen, or air.",
        "Protect the mystery — do not reveal the conclusion yet.",
    )

    # 2 Question / Mystery
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Chapter 01  ·  The Mystery")
    add_title(s, "What does a flame need to keep burning?")
    add_sub(s, "Air is all around us — invisible, but powerful.")
    add_image(s, "hero-flame.png", Inches(1.5), Inches(2.2), Inches(10.3), Inches(4.8))
    add_fade_transition(s)
    add_notes(
        s,
        "Let students watch the flame image quietly for a few seconds.",
        "Air is invisible but may still matter for fire.",
        "Can something we cannot see still affect fire?",
        "Yes — air can affect fire even though we cannot see it.",
        "Invite predictions without judging correctness.",
    )

    # 3 Air everywhere
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Chapter 02  ·  Invisible Air")
    add_title(s, "Air is everywhere.")
    add_sub(s, "You cannot see it. But can something invisible affect a flame?")
    add_image(s, "air-hidden.png", Inches(0.6), Inches(2.2), Inches(5.8), Inches(4.5))
    add_image(s, "air-revealed.png", Inches(6.9), Inches(2.2), Inches(5.8), Inches(4.5))
    add_text(s, "Before", Inches(0.6), Inches(6.8), Inches(5.8), Inches(0.3), size=12, color=MUTED, align=PP_ALIGN.CENTER)
    add_text(s, "Revealed", Inches(6.9), Inches(6.8), Inches(5.8), Inches(0.3), size=12, color=FRESH, align=PP_ALIGN.CENTER)
    add_fade_transition(s)
    add_notes(
        s,
        "Reveal the right image after students discuss.",
        "Air surrounds the flame; cyan particles are a visualization, not something we normally see.",
        "If air is invisible, how can scientists study it?",
        "By observing effects — like what happens when air is trapped.",
        "Emphasize visualization vs. literal colored air.",
    )

    # 4 Can air affect fire?
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Focus Question")
    add_title(s, "Can air affect fire?", size=36)
    add_sub(s, "Let's test it with a careful classroom experiment.")
    add_image(s, "hero-flame.png", Inches(3.5), Inches(2.4), Inches(6.3), Inches(4.2))
    add_fade_transition(s)
    add_notes(
        s,
        "Transition from wonder to investigation.",
        "Experiments help us test ideas about invisible air.",
        "What equipment might help us trap or release air around a flame?",
        "A jar, lid, clay, candle — ways to control openings.",
        "Preview safety: teacher lights the candle.",
    )

    # 5 Experiment setup
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Chapter 03  ·  Experiment")
    add_title(s, "Build the investigation.")
    add_sub(s, "Board · Clay · Candle · Bottomless glass jar · Metal lid · Lighter (teacher only)")
    add_image(s, "experiment-setup.png", Inches(0.8), Inches(2.1), Inches(11.7), Inches(4.5))
    warn = pill(s, "  Caution: Only the teacher should use the lighter to light the candle.", Inches(2.2), Inches(6.7), Inches(8.9), Inches(0.45), RGBColor(0x2A, 0x12, 0x14), WARN)
    add_fade_transition(s)
    add_notes(
        s,
        "Assemble materials visibly. Assign observation roles.",
        "The jar is bottomless so we can control top and bottom openings.",
        "Why must only the teacher use the lighter?",
        "Fire safety — adults handle ignition.",
        "Keep clay ready for making bottom gaps later.",
    )

    # 6 Prediction
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Chapter 04  ·  Predict")
    add_title(s, "What do you think will happen?")
    add_sub(s, "If we seal the jar with a metal lid…")
    a = choice_row(s, "A", "The flame keeps burning the same.", Inches(2.4))
    b = choice_row(s, "B", "The flame becomes weaker, then may go out.", Inches(3.3), accent=FIRE)
    c = choice_row(s, "C", "The flame goes out right away.", Inches(4.2))
    add_text(s, "Click to choose as a class — then continue to test.", Inches(1), Inches(5.3), Inches(11.3), Inches(0.4), size=13, color=MUTED, align=PP_ALIGN.CENTER)
    add_fade_transition(s)
    add_notes(
        s,
        "Poll the room. Record votes without revealing the answer.",
        "We are about to trap air with the candle.",
        "Which choice matches a gradual change?",
        "B suggests gradual weakening.",
        "Do not confirm yet — discovery comes after observation.",
    )

    # 7 Closed jar
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Chapter 05  ·  The Closed Jar")
    add_title(s, "Trap the air.")
    add_sub(s, "Place the metal lid. Watch the air inside — and the flame.")
    add_image(s, "sealed-1.png", Inches(1.2), Inches(2.1), Inches(10.9), Inches(4.8))
    add_fade_transition(s)
    add_notes(
        s,
        "Demonstrate sealing carefully.",
        "In a closed jar, air cannot be renewed from outside.",
        "What do you notice first — the flame or the air?",
        "Flame may look normal at first, then weaken.",
        "Ask students to time how long until change is visible.",
    )

    # 8 Flame goes out
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Chapter 06  ·  Observation")
    add_title(s, "The flame goes out.")
    add_sub(s, "The flame gradually weakens… then the candle goes out after a short time.")
    add_image(s, "oxygen-strip.png", Inches(0.6), Inches(2.2), Inches(12.1), Inches(4.0))
    add_text(s, "Prediction check: B matches the observation best.", Inches(1), Inches(6.5), Inches(11.3), Inches(0.4), size=14, color=FRESH, bold=True, align=PP_ALIGN.CENTER)
    add_fade_transition(s)
    add_notes(
        s,
        "Animate discussion along the strip: full → used → almost gone → out.",
        "Available air decreases; flame strength falls with it.",
        "Did the flame die instantly or gradually?",
        "Gradually — then it went out.",
        "Connect back to student predictions kindly.",
    )

    # 9 Why
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Chapter 07  ·  Why?")
    add_title(s, "The air inside was used up.")
    add_sub(s, "In a closed jar, the air is used up. Once it runs out, the candle goes out.")
    for i, name in enumerate(["sealed-1.png", "sealed-2.png", "sealed-3.png", "sealed-4.png"]):
        add_image(s, name, Inches(0.4 + i * 3.2), Inches(2.3), Inches(3.0), Inches(3.8))
    add_fade_transition(s)
    add_notes(
        s,
        "Walk left to right through the four frames.",
        "Closed system → air used up → burning stops.",
        "Why can't the candle keep burning forever under the lid?",
        "Fresh air cannot enter to replace used air.",
        "Avoid claiming exact oxygen percentages for Grade 6.",
    )

    # 10 Fresh air
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Chapter 08  ·  Fresh Air")
    add_title(s, "Fresh air in. Warm air out.")
    add_sub(s, "Gap at the bottom + opening at the top → air is constantly renewed.")
    add_image(s, "airflow.png", Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.9))
    add_fade_transition(s)
    add_notes(
        s,
        "Trace cyan arrows in, warm arrows out with your finger or laser.",
        "Continuous renewal of air allows burning to continue.",
        "Which way does warm air tend to move?",
        "Upward — out the top opening.",
        "Introduce the word renew / replace gently.",
    )

    # 11 Bottom only nuance
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Experiment nuance")
    add_title(s, "Bottom gap alone is not enough.")
    add_sub(s, "Lid on + small bottom gap → flame goes out after a slightly longer time.")
    add_image(s, "bottom-only.png", Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.9))
    add_fade_transition(s)
    add_notes(
        s,
        "This prevents a common misconception: one opening is not a full chimney.",
        "Without a top exit, air cannot circulate well enough.",
        "Why might it last a little longer than fully sealed?",
        "A little air can sneak in — but not enough continuous renewal.",
        "Keep language Grade 6: renew, openings, continue burning.",
    )

    # 12 Aha compare
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Chapter 09  ·  The Aha Moment")
    add_title(s, "Closed vs. airflow.")
    add_sub(s, "Sealed air runs out. Continuous fresh air keeps burning going.")
    add_image(s, "compare.png", Inches(0.5), Inches(2.0), Inches(12.3), Inches(5.0))
    add_fade_transition(s)
    add_notes(
        s,
        "Have students explain the difference to a partner.",
        "Both top and bottom openings matter for renewal in this setup.",
        "Which side would you use to keep a flame alive longer?",
        "The airflow side.",
        "Celebrate the aha — this is the core discovery.",
    )

    # 13 Editable apparatus compare
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Diagram  ·  Editable shapes")
    add_title(s, "Build the science with shapes.")
    add_sub(s, "Closed (left) vs airflow (right) — constructed from PowerPoint objects.")
    draw_mini_apparatus(s, Inches(2.2), Inches(2.2), lid=True, gaps=False, flame_on=False, label="CLOSED")
    draw_mini_apparatus(s, Inches(8.5), Inches(2.2), lid=False, gaps=True, flame_on=True, label="AIRFLOW")
    # arrows as chevrons
    for i, (x, y, rot, col) in enumerate(
        [
            (Inches(8.2), Inches(4.3), 40, FRESH),
            (Inches(10.7), Inches(4.3), -40, FRESH),
            (Inches(9.55), Inches(2.0), 0, WARM),
        ]
    ):
        ar = s.shapes.add_shape(MSO_SHAPE.UP_ARROW if col == WARM else MSO_SHAPE.RIGHT_ARROW, x, y, Inches(0.35), Inches(0.55))
        ar.fill.solid()
        ar.fill.fore_color.rgb = col
        ar.line.fill.background()
        if col == FRESH:
            ar.rotation = 225 if i == 0 else 135
    add_fade_transition(s)
    add_notes(
        s,
        "Ungroup/edit these shapes live on the board if you want to rebuild the diagram with students.",
        "Visual model of chimney-style airflow.",
        "What do the cyan arrows mean? The warm arrow?",
        "Fresh air entering; warm air leaving.",
        "Keep editable — avoid converting this slide to a picture.",
    )

    # 14 Science
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Chapter 10  ·  The Science")
    add_title(s, "What is meant by burning?")
    add_sub(s, "A reaction between oxygen and a substance that produces heat and light.")
    # editable equation chips
    chips = [("Fuel", RGBColor(0xF0, 0xD7, 0xB0)), ("+", MUTED), ("Oxygen", OXYGEN), ("+", MUTED), ("Heat", FIRE), ("→", MUTED), ("Heat + Light", CORE)]
    x = Inches(1.0)
    for label, col in chips:
        if label in ("+", "→"):
            add_text(s, label, x, Inches(3.5), Inches(0.5), Inches(0.6), size=22, color=col, align=PP_ALIGN.CENTER)
            x += Inches(0.55)
        else:
            chip = slide_chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(3.4), Inches(1.7), Inches(0.7))
            slide_chip.fill.solid()
            slide_chip.fill.fore_color.rgb = RGBColor(0x10, 0x18, 0x28)
            slide_chip.line.color.rgb = col
            tf = slide_chip.text_frame
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run()
            r.text = label
            r.font.size = Pt(16)
            r.font.color.rgb = col
            r.font.name = "Georgia"
            x += Inches(1.9)
    add_image(s, "combustion.png", Inches(1.5), Inches(4.4), Inches(10.3), Inches(2.5))
    add_fade_transition(s)
    add_notes(
        s,
        "Read the definition aloud together.",
        "Combustion: oxygen + substance → heat + light.",
        "Is oxygen the only thing needed?",
        "No — also a substance (fuel) and conditions for the reaction (heat).",
        "Keep the official definition wording close to the source lesson.",
    )

    # 15 Real world
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Chapter 11  ·  Real World")
    add_title(s, "Where do we see this?")
    add_sub(s, "Burning needs a continuous supply of fresh air.")
    add_image(s, "real-world.png", Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.2))
    examples = [
        ("Candle", "Needs surrounding air"),
        ("Fireplace", "Chimney renews air"),
        ("Gas stove", "Designed for airflow"),
        ("Engine", "Takes in air to burn fuel"),
    ]
    for i, (t, d) in enumerate(examples):
        add_text(s, f"{t}: {d}", Inches(0.6 + i * 3.15), Inches(6.4), Inches(3.0), Inches(0.6), size=11, color=MUTED, align=PP_ALIGN.CENTER)
    add_fade_transition(s)
    add_notes(
        s,
        "Ask for local examples (campfire, kitchen, heater).",
        "Real systems are designed so air can renew.",
        "Why do fireplaces have chimneys?",
        "To let warm air out so fresh air can enter.",
        "Keep connections concrete for Grade 6.",
    )

    # 16 Challenge
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Chapter 12  ·  Science Challenge")
    add_title(s, "Which candle burns longer?")
    add_sub(s, "Choose carefully — then reveal.")
    choice_row(s, "A", "Candle A — jar sealed with a lid, no gaps.", Inches(2.4))
    choice_row(s, "B", "Candle B — lid on, but a small gap only at the bottom.", Inches(3.3))
    choice_row(s, "C", "Candle C — gap at the bottom and open at the top.", Inches(4.2), accent=FRESH, highlight=True)
    add_text(s, "Answer: C — both openings renew air so burning can continue.", Inches(1), Inches(5.5), Inches(11.3), Inches(0.5), size=16, color=FRESH, bold=True, align=PP_ALIGN.CENTER)
    add_text(s, "B lasts a bit longer than A, but still goes out.", Inches(1), Inches(6.1), Inches(11.3), Inches(0.4), size=12, color=MUTED, align=PP_ALIGN.CENTER)
    add_fade_transition(s)
    add_notes(
        s,
        "Hide the answer text initially (animate Appear) if presenting live.",
        "Correct: both openings (bottom + top).",
        "Why isn't B good enough?",
        "Bottom-only gap still cannot fully renew air with the lid on.",
        "Use as formative check before conclusions.",
    )

    # 17 Big idea / conclusions
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Final Discovery")
    add_title(s, "Air plays an important role in burning.")
    add_sub(s, "Fresh air must continuously be supplied for burning to continue.")
    conclusions = [
        "1. Air has a role in burning.",
        "2. Fresh air must constantly flow in and out for burning to continue.",
        "3. Where air is not renewed, things cannot continue burning.",
    ]
    for i, text in enumerate(conclusions):
        pill(s, f"  {text}", Inches(1.5), Inches(2.5 + i * 1.0), Inches(10.3), Inches(0.75), RGBColor(0x0E, 0x1A, 0x2A), AIR)
    add_fade_transition(s)
    add_notes(
        s,
        "Read each conclusion slowly. Ask students to restate in their own words.",
        "These three statements are the authoritative lesson takeaways.",
        "Can you give one sentence that captures all three?",
        "Burning needs fresh air renewed; without renewal, fire stops.",
        "Post these on the board for the rest of the week.",
    )

    # 18 Remember
    s = prs.slides.add_slide(blank)
    set_slide_bg(s)
    add_kicker(s, "Remember")
    add_title(s, "Investigation complete.")
    add_sub(s, "Air is invisible — but essential for a flame to keep burning.")
    add_image(s, "compare.png", Inches(1.5), Inches(2.2), Inches(10.3), Inches(4.0))
    add_text(s, "Fuel + Oxygen + Heat  →  Heat + Light", Inches(1), Inches(6.4), Inches(11.3), Inches(0.4), size=16, color=FIRE, bold=True, align=PP_ALIGN.CENTER)
    add_fade_transition(s)
    add_notes(
        s,
        "Close by returning to the opening question — now students can answer it.",
        "Air (with oxygen) is required for continued burning; renewal matters.",
        "What does a flame need to keep burning?",
        "Fuel, heat, and a continuous supply of fresh air (oxygen).",
        "Optional: replay the HTML experience as a station rotation.",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT))
    print("PPTX →", OUT)
    print("slides:", len(prs.slides))


if __name__ == "__main__":
    build()
