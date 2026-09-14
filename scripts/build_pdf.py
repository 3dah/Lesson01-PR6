"""Build premium educational PDF from the Mystery of Fire experience content."""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "exports" / "assets"
FONTS = ROOT / "exports" / "fonts"
OUT = ROOT / "exports" / "pdf" / "The-Mystery-of-Fire.pdf"

# Visual system
BG = (7 / 255, 11 / 255, 20 / 255)
AIR = (94 / 255, 200 / 255, 255 / 255)
OXYGEN = (122 / 255, 215 / 255, 255 / 255)
FRESH = (158 / 255, 255 / 255, 240 / 255)
FIRE = (255 / 255, 138 / 255, 61 / 255)
CORE = (255 / 255, 229 / 255, 102 / 255)
MUTED = (154 / 255, 166 / 255, 184 / 255)
TEXT = (242 / 255, 245 / 255, 250 / 255)
WARN = (226 / 255, 74 / 255, 59 / 255)
WARM = (255 / 255, 176 / 255, 112 / 255)

PAGE = landscape(A4)  # cinematic widescreen-ish lesson pages
W, H = PAGE


def register_fonts():
    body = "Helvetica"
    display = "Times-Bold"
    body_b = "Helvetica-Bold"
    sora = FONTS / "Sora-Regular.ttf"
    sora_b = FONTS / "Sora-SemiBold.ttf"
    # Prefer static Sora; skip variable Fraunces (reportlab often renders it incorrectly)
    if sora.exists():
        try:
            pdfmetrics.registerFont(TTFont("Sora", str(sora)))
            body = "Sora"
        except Exception:
            pass
    if sora_b.exists():
        try:
            pdfmetrics.registerFont(TTFont("Sora-SemiBold", str(sora_b)))
            body_b = "Sora-SemiBold"
            display = "Sora-SemiBold"  # reliable dark-theme headlines
        except Exception:
            pass
    return display, body, body_b


DISPLAY, BODY, BODY_B = register_fonts()


class Doc:
    def __init__(self):
        OUT.parent.mkdir(parents=True, exist_ok=True)
        self.c = pdfcanvas.Canvas(str(OUT), pagesize=PAGE)
        self.page_num = 0
        self.total_hint = 16

    def bg(self):
        self.c.setFillColorRGB(*BG)
        self.c.rect(0, 0, W, H, fill=1, stroke=0)
        # warm floor glow
        self.c.setFillColorRGB(1, 0.4, 0.15, alpha=0.08)
        self.c.circle(W / 2, 0, 220, fill=1, stroke=0)
        # cool top glow
        self.c.setFillColorRGB(*AIR, alpha=0.06)
        self.c.circle(W / 2, H, 260, fill=1, stroke=0)

    def footer(self, label: str):
        self.page_num += 1
        self.c.setFillColorRGB(*MUTED)
        self.c.setFont(BODY, 8)
        self.c.drawString(24 * mm, 10 * mm, "The Mystery of Fire  ·  Grade 6 Science")
        self.c.drawRightString(W - 24 * mm, 10 * mm, f"{label}   {self.page_num}")

    def kicker(self, text: str, y=H - 22 * mm):
        self.c.setFillColorRGB(*AIR)
        self.c.setFont(BODY_B, 9)
        self.c.drawCentredString(W / 2, y, text.upper())

    def title(self, text: str, y=H - 40 * mm, size=28):
        self.c.setFillColorRGB(*TEXT)
        self.c.setFont(DISPLAY, size)
        self.c.drawCentredString(W / 2, y, text)

    def subtitle(self, text: str, y=H - 52 * mm, width=170 * mm):
        self.c.setFillColorRGB(*MUTED)
        self.c.setFont(BODY, 11)
        self._wrap_centered(text, W / 2, y, width, 14)

    def _wrap_centered(self, text, x, y, max_w, leading):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if self.c.stringWidth(trial, BODY, 11) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        for i, line in enumerate(lines):
            self.c.drawCentredString(x, y - i * leading, line)

    def img(self, name, x, y, w, h):
        path = ASSETS / name
        if not path.exists():
            return
        self.c.drawImage(ImageReader(str(path)), x, y, width=w, height=h, preserveAspectRatio=True, mask="auto")

    def pill(self, text, x, y, w, h, stroke, fill_alpha=0.08):
        self.c.setStrokeColorRGB(*stroke)
        self.c.setFillColorRGB(*stroke, alpha=fill_alpha)
        self.c.roundRect(x, y, w, h, 10, fill=1, stroke=1)

    def finish(self):
        self.c.showPage()

    def save(self):
        self.c.save()


def page_cover(d: Doc):
    d.bg()
    d.img("hero-flame.png", 40 * mm, 25 * mm, W - 80 * mm, 85 * mm)
    d.kicker("Interactive Science Experience  ·  Grade 6")
    d.title("The Mystery of Fire", size=34)
    d.subtitle("What does a flame need to keep burning?")
    d.c.setFillColorRGB(*FIRE)
    d.c.setFont(BODY_B, 11)
    d.c.drawCentredString(W / 2, 22 * mm, "The Role of Air in Burning Things")
    d.footer("Cover")
    d.finish()


def page_question(d: Doc):
    d.bg()
    d.kicker("Chapter 01  ·  The Mystery")
    d.title("What does a flame need to keep burning?")
    d.subtitle("Air is all around us — invisible, but powerful. Tonight we investigate its role in fire.")
    d.img("hero-flame.png", 35 * mm, 28 * mm, W - 70 * mm, 95 * mm)
    d.footer("Mystery")
    d.finish()


def page_air(d: Doc):
    d.bg()
    d.kicker("Chapter 02  ·  Invisible Air")
    d.title("Air is everywhere.")
    d.subtitle("You cannot see it. But can something invisible affect a flame?")
    # two panels
    d.img("air-hidden.png", 20 * mm, 30 * mm, 120 * mm, 68 * mm)
    d.img("air-revealed.png", W / 2 + 5 * mm, 30 * mm, 120 * mm, 68 * mm)
    d.c.setFillColorRGB(*MUTED)
    d.c.setFont(BODY, 9)
    d.c.drawCentredString(80 * mm, 26 * mm, "Before — air is invisible")
    d.c.setFillColorRGB(*FRESH)
    d.c.drawCentredString(W / 2 + 65 * mm, 26 * mm, "Revealed — air surrounds the flame")
    d.footer("Invisible Air")
    d.finish()


def page_experiment(d: Doc):
    d.bg()
    d.kicker("Chapter 03  ·  Experiment")
    d.title("Build the investigation.")
    d.subtitle("Wooden board, clay, candle, bottomless glass jar, metal lid — lighter used only by the teacher.")
    d.img("experiment-setup.png", 25 * mm, 32 * mm, W - 50 * mm, 85 * mm)
    d.pill("Caution: Only the teacher should use the lighter to light the candle.", 55 * mm, 18 * mm, W - 110 * mm, 10 * mm, WARN, 0.12)
    d.c.setFillColorRGB(1, 0.76, 0.74)
    d.c.setFont(BODY, 8)
    d.c.drawCentredString(W / 2, 21 * mm, "Caution: Only the teacher should use the lighter to light the candle.")
    d.footer("Experiment")
    d.finish()


def page_prediction(d: Doc):
    d.bg()
    d.kicker("Chapter 04  ·  Predict")
    d.title("What do you think will happen?")
    d.subtitle("If we seal the jar with a metal lid, what happens to the flame?")
    choices = [
        ("A", "The flame keeps burning the same."),
        ("B", "The flame becomes weaker, then may go out."),
        ("C", "The flame goes out right away."),
    ]
    y = 95 * mm
    for letter, text in choices:
        d.pill("", 55 * mm, y, W - 110 * mm, 18 * mm, AIR, 0.06)
        d.c.setFillColorRGB(*AIR)
        d.c.circle(70 * mm, y + 9 * mm, 6 * mm, fill=1, stroke=0)
        d.c.setFillColorRGB(*BG)
        d.c.setFont(BODY_B, 12)
        d.c.drawCentredString(70 * mm, y + 6.5 * mm, letter)
        d.c.setFillColorRGB(*TEXT)
        d.c.setFont(BODY, 12)
        d.c.drawString(85 * mm, y + 6.5 * mm, text)
        y -= 24 * mm
    d.c.setFillColorRGB(*MUTED)
    d.c.setFont(BODY, 9)
    d.c.drawCentredString(W / 2, 22 * mm, "Make your prediction — then turn the page to investigate.")
    d.footer("Prediction")
    d.finish()


def page_closed(d: Doc):
    d.bg()
    d.kicker("Chapter 05  ·  The Closed Jar")
    d.title("Trap the air.")
    d.subtitle("Close the jar with the metal lid. The air inside is trapped with the flame.")
    d.img("sealed-1.png", 30 * mm, 28 * mm, W - 60 * mm, 90 * mm)
    d.footer("Closed Jar")
    d.finish()


def page_goes_out(d: Doc):
    d.bg()
    d.kicker("Chapter 06  ·  Observation")
    d.title("The flame goes out.")
    d.subtitle("The flame gradually weakens… then the candle goes out after a short time.")
    d.img("oxygen-strip.png", 20 * mm, 45 * mm, W - 40 * mm, 70 * mm)
    d.c.setFillColorRGB(*MUTED)
    d.c.setFont(BODY, 9)
    d.c.drawCentredString(W / 2, 28 * mm, "Best prediction match: B — the flame becomes weaker, then may go out.")
    d.footer("Flame Out")
    d.finish()


def page_why(d: Doc):
    d.bg()
    d.kicker("Chapter 07  ·  Why?")
    d.title("The air inside was used up.")
    d.subtitle("In a closed jar, the air is used up. Once it runs out, the candle goes out.")
    # four sealed frames
    for i, name in enumerate(["sealed-1.png", "sealed-2.png", "sealed-3.png", "sealed-4.png"]):
        x = 12 * mm + i * 70 * mm
        d.img(name, x, 35 * mm, 65 * mm, 55 * mm)
    d.c.setFillColorRGB(*FRESH)
    d.c.setFont(BODY_B, 11)
    d.c.drawCentredString(W / 2, 22 * mm, "No fresh air can enter → burning cannot continue.")
    d.footer("Why")
    d.finish()


def page_fresh(d: Doc):
    d.bg()
    d.kicker("Chapter 08  ·  Fresh Air")
    d.title("Fresh air in. Warm air out.")
    d.subtitle("With a gap at the bottom and an opening at the top, air is constantly renewed.")
    d.img("airflow.png", 25 * mm, 30 * mm, W - 50 * mm, 90 * mm)
    d.footer("Fresh Air")
    d.finish()


def page_bottom_only(d: Doc):
    d.bg()
    d.kicker("Important nuance from the experiment")
    d.title("A bottom gap alone is not enough.")
    d.subtitle("With the lid still on and only a small gap at the bottom, the flame goes out after a slightly longer time.")
    d.img("bottom-only.png", 25 * mm, 30 * mm, W - 50 * mm, 90 * mm)
    d.footer("Bottom Gap")
    d.finish()


def page_aha(d: Doc):
    d.bg()
    d.kicker("Chapter 09  ·  The Aha Moment")
    d.title("Closed vs. airflow.")
    d.subtitle("Sealed air runs out. Continuous fresh air keeps burning going.")
    d.img("compare.png", 15 * mm, 28 * mm, W - 30 * mm, 95 * mm)
    d.footer("Aha")
    d.finish()


def page_science(d: Doc):
    d.bg()
    d.kicker("Chapter 10  ·  The Science")
    d.title("What is meant by burning?")
    d.subtitle("Burning (combustion) is a reaction between oxygen and a substance that produces heat and light.")
    d.img("combustion.png", 20 * mm, 40 * mm, W - 40 * mm, 75 * mm)
    d.footer("Science")
    d.finish()


def page_world(d: Doc):
    d.bg()
    d.kicker("Chapter 11  ·  Real World")
    d.title("Where do we see this?")
    d.subtitle("Candles, fireplaces, stoves, engines — burning needs a continuous supply of fresh air.")
    d.img("real-world.png", 20 * mm, 35 * mm, W - 40 * mm, 80 * mm)
    items = [
        "Candle — needs surrounding air",
        "Fireplace — chimney renews air",
        "Gas stove — designed for airflow",
        "Engine — takes in air to burn fuel",
    ]
    d.c.setFont(BODY, 8)
    d.c.setFillColorRGB(*MUTED)
    for i, t in enumerate(items):
        d.c.drawCentredString(40 * mm + i * 55 * mm, 22 * mm, t)
    d.footer("Real World")
    d.finish()


def page_challenge(d: Doc):
    d.bg()
    d.kicker("Chapter 12  ·  Science Challenge")
    d.title("Which candle burns longer?")
    d.subtitle("Use what you discovered about openings and fresh air.")
    choices = [
        ("A", "Candle A — jar sealed with a lid, no gaps."),
        ("B", "Candle B — lid on, but a small gap only at the bottom."),
        ("C", "Candle C — gap at the bottom and open at the top."),
    ]
    y = 95 * mm
    for letter, text in choices:
        stroke = FRESH if letter == "C" else AIR
        d.pill("", 45 * mm, y, W - 90 * mm, 18 * mm, stroke, 0.08 if letter == "C" else 0.05)
        d.c.setFillColorRGB(*stroke)
        d.c.circle(60 * mm, y + 9 * mm, 6 * mm, fill=1, stroke=0)
        d.c.setFillColorRGB(*BG)
        d.c.setFont(BODY_B, 12)
        d.c.drawCentredString(60 * mm, y + 6.5 * mm, letter)
        d.c.setFillColorRGB(*TEXT)
        d.c.setFont(BODY, 11)
        d.c.drawString(75 * mm, y + 6.5 * mm, text)
        y -= 22 * mm
    d.c.setFillColorRGB(*FRESH)
    d.c.setFont(BODY_B, 10)
    d.c.drawCentredString(W / 2, 20 * mm, "Answer: C — both openings let air renew so burning can continue.")
    d.footer("Challenge")
    d.finish()


def page_conclusions(d: Doc):
    d.bg()
    d.kicker("Final Discovery")
    d.title("Air plays an important role in burning.")
    d.subtitle("Fresh air must continuously be supplied for burning to continue.")
    conclusions = [
        "Air has a role in burning.",
        "One of the most important conditions for things to continue burning is that fresh air must constantly flow in and out.",
        "In a place where air is not renewed, things cannot continue burning.",
    ]
    y = 95 * mm
    for i, text in enumerate(conclusions, 1):
        d.pill("", 40 * mm, y, W - 80 * mm, 20 * mm, AIR, 0.07)
        d.c.setFillColorRGB(*FRESH)
        d.c.setFont(BODY_B, 10)
        d.c.drawString(50 * mm, y + 8 * mm, f"{i}.")
        d.c.setFillColorRGB(*TEXT)
        d.c.setFont(BODY, 10)
        # wrap manually for long line
        if len(text) > 90:
            d.c.drawString(60 * mm, y + 12 * mm, text[:78])
            d.c.drawString(60 * mm, y + 4 * mm, text[78:])
        else:
            d.c.drawString(60 * mm, y + 8 * mm, text)
        y -= 26 * mm
    d.footer("Discovery")
    d.finish()


def page_remember(d: Doc):
    d.bg()
    d.kicker("Remember")
    d.title("Investigation complete.")
    d.subtitle("Air is invisible — but essential for a flame to keep burning.")
    d.img("compare.png", 40 * mm, 35 * mm, W - 80 * mm, 75 * mm)
    d.c.setFillColorRGB(*FIRE)
    d.c.setFont(BODY_B, 12)
    d.c.drawCentredString(W / 2, 22 * mm, "Fuel + Oxygen + Heat  →  Heat + Light")
    d.footer("Remember")
    d.finish()


def main():
    d = Doc()
    page_cover(d)
    page_question(d)
    page_air(d)
    page_experiment(d)
    page_prediction(d)
    page_closed(d)
    page_goes_out(d)
    page_why(d)
    page_fresh(d)
    page_bottom_only(d)
    page_aha(d)
    page_science(d)
    page_world(d)
    page_challenge(d)
    page_conclusions(d)
    page_remember(d)
    d.save()
    print("PDF →", OUT)


if __name__ == "__main__":
    main()
