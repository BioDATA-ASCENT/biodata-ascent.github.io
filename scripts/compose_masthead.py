from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "biodata-ascent-masthead-v2.png"
OUTPUT = ROOT / "assets" / "biodata-ascent-masthead-v3.png"
FONT = "/System/Library/Fonts/Avenir Next.ttc"

NAVY = (0, 28, 72, 255)
TEAL = (0, 160, 176, 255)

RUNS = [
    ("A", True),
    ("I, ", False),
    ("S", True),
    ("cience, ", False),
    ("C", True),
    ("loud, ", False),
    ("E", True),
    ("xploration, ", False),
    ("N", True),
    ("etworks, and ", False),
    ("T", True),
    ("echnology", False),
]


def fonts(size: int):
    # Avenir Next Demi Bold and Medium closely match the geometric wordmark.
    return {
        True: ImageFont.truetype(FONT, size, index=2),
        False: ImageFont.truetype(FONT, size, index=5),
    }


def line_width(draw: ImageDraw.ImageDraw, selected_fonts) -> float:
    return sum(draw.textlength(text, font=selected_fonts[emphasis]) for text, emphasis in RUNS)


logo = Image.open(SOURCE).convert("RGBA")
measure = ImageDraw.Draw(Image.new("RGBA", (1, 1)))

font_size = 58
selected = fonts(font_size)
while line_width(measure, selected) > logo.width - 150:
    font_size -= 1
    selected = fonts(font_size)

gap = 2
bottom_padding = 4
ascent = max(font.getmetrics()[0] for font in selected.values())
descent = max(font.getmetrics()[1] for font in selected.values())
baseline = logo.height + gap + ascent

canvas = Image.new("RGBA", (logo.width, baseline + descent + bottom_padding), (0, 0, 0, 0))
canvas.alpha_composite(logo)
draw = ImageDraw.Draw(canvas)

width = line_width(draw, selected)
x = (logo.width - width) / 2
for text, emphasis in RUNS:
    font = selected[emphasis]
    draw.text(
        (x, baseline),
        text,
        font=font,
        fill=TEAL if emphasis else NAVY,
        anchor="ls",
    )
    x += draw.textlength(text, font=font)

canvas.save(OUTPUT, optimize=True)
print(f"Wrote {OUTPUT} ({canvas.width}x{canvas.height}, subtitle {font_size}px)")
