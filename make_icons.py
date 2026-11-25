import os, sys
from PIL import Image, ImageDraw

RES = sys.argv[1] if len(sys.argv) > 1 else "android/app/src/main/res"
BG = (91, 63, 209)
FG = (255, 255, 255)
S = 4  # supersampling for smooth edges


def wheel(size, radius_ratio, transparent):
    big = size * S
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0) if transparent else BG + (255,))
    d = ImageDraw.Draw(img)
    k = radius_ratio / 0.34  # scale: launcher 1.0, foreground ~0.65
    c = big / 2
    w = big * 0.40 * k
    h = big * 0.50 * k
    x0, y0, x1, y1 = c - w / 2, c - h / 2 + big * 0.03 * k, c + w / 2, c + h / 2 + big * 0.03 * k
    lw = max(2, int(big * 0.055 * k))
    d.rounded_rectangle([x0, y0, x1, y1], radius=big * 0.06 * k, outline=FG, width=lw)
    cw, ch = w * 0.46, h * 0.16
    d.rounded_rectangle([c - cw / 2, y0 - ch / 2, c + cw / 2, y0 + ch / 2], radius=ch * 0.4, fill=FG)
    for i, f in enumerate((0.62, 0.62, 0.40)):
        ly = y0 + h * (0.30 + i * 0.22)
        d.line([x0 + w * 0.18, ly, x0 + w * 0.18 + w * f * 0.8, ly], fill=FG, width=max(2, int(lw * 0.75)))
    return img.resize((size, size), Image.LANCZOS)


SIZES = {"mdpi": (48, 108), "hdpi": (72, 162), "xhdpi": (96, 216), "xxhdpi": (144, 324), "xxxhdpi": (192, 432)}

for dens, (launcher, foreground) in SIZES.items():
    folder = os.path.join(RES, "mipmap-" + dens)
    if not os.path.isdir(folder):
        continue
    square = wheel(launcher, 0.34, False)
    square.save(os.path.join(folder, "ic_launcher.png"))
    mask = Image.new("L", (launcher, launcher), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, launcher - 1, launcher - 1], fill=255)
    rounded = Image.new("RGBA", (launcher, launcher), (0, 0, 0, 0))
    rounded.paste(square, (0, 0), mask)
    rounded.save(os.path.join(folder, "ic_launcher_round.png"))
    wheel(foreground, 0.22, True).save(os.path.join(folder, "ic_launcher_foreground.png"))

values = os.path.join(RES, "values")
if os.path.isdir(values):
    with open(os.path.join(values, "ic_launcher_background.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#5B3FD1</color>\n</resources>\n')
print("icons done")
