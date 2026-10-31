"""Korrigiert KI-Fehler der Magnesium-Grafik: Fantasie-Schrift auf dem Röhrchen entfernen, „Zin“ → „Zn“."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

im = Image.open(sys.argv[1]).convert('RGB')
a = np.asarray(im).astype(np.int16).copy()
lum = a.mean(axis=2)


def fill(box, light_thr, grow=5):
    """Dunkle Schrift in box per Diffusion aus der Umgebung auffuellen (einfaches Inpainting)."""
    global a
    x0, y0, x1, y1 = box
    lr = lum[y0:y1, x0:x1]
    m = Image.fromarray(((lr <= light_thr) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(grow))
    mask = np.zeros(lum.shape, bool)
    mask[y0:y1, x0:x1] = np.asarray(m) > 0
    work = a.astype(np.float32)
    work[mask] = np.median(a[y0:y1, x0:x1][lr > light_thr], axis=0)
    for _ in range(120):
        blur = np.asarray(Image.fromarray(work.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32)
        work[mask] = blur[mask]
    a = work.astype(np.int16)


fill((414, 880, 440, 1037), 200, grow=3)          # Röhrchen-Etikett leer
fill((1226, 2284, 1295, 2324), 120)       # „Zin“ auf der Münze
img = Image.fromarray(a.clip(0, 255).astype(np.uint8))
d = ImageDraw.Draw(img)
f = ImageFont.truetype('/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf', 50)
d.text((1260, 2304), 'Zn', font=f, fill=(25, 25, 30), anchor='mm')
img.save(sys.argv[2])
print('fertig', sys.argv[2])
