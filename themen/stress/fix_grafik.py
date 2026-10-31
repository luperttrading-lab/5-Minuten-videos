"""Korrigiert die Tippfehler der KI-Grafik: Text wegmalen (Inpainting) und richtig neu setzen."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC, DST = sys.argv[1], sys.argv[2]
FONT = '/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf'
im = Image.open(SRC).convert('RGB')
a = np.asarray(im.convert('L')).astype(int)

# (Suchbox um das falsche Wort, falscher Text, richtiger Text)
FIXES = [
    ((110, 1488, 250, 1516), 'Unerladigte', 'Unerledigte'),
    ((110, 1516, 250, 1545), 'Aufgeben', 'Aufgaben'),
    ((285, 1410, 380, 1442), 'Surgen', 'Sorgen'),
    ((525, 1500, 625, 1532), 'E-Malls', 'E-Mails'),
    ((1320, 1172, 1368, 1206), '3-3', '3–5', 'h'),
]

def bbox(box, thr=90):
    x0, y0, x1, y1 = box
    ys, xs = np.where(a[y0:y1, x0:x1] < thr)
    return x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1

try:
    import cv2
except ImportError:
    cv2 = None

out = np.asarray(im).copy()
boxes = []
for box, wrong, right, *mode in FIXES:
    bx = bbox(box)
    boxes.append((bx, wrong, right, mode[0] if mode else 'w'))
    x0, y0, x1, y1 = bx
    m = 3
    region = out[y0 - m:y1 + m, x0 - m:x1 + m]
    if cv2 is not None:
        mask = np.zeros(out.shape[:2], np.uint8)
        dark = (a[y0 - m:y1 + m, x0 - m:x1 + m] < 200).astype(np.uint8) * 255
        dark = cv2.dilate(dark, np.ones((5, 5), np.uint8))
        mask[y0 - m:y1 + m, x0 - m:x1 + m] = dark
        out = cv2.inpaint(out, mask, 6, cv2.INPAINT_TELEA)
    else:
        light = region[a[y0 - m:y1 + m, x0 - m:x1 + m] > 200]
        region[:] = np.median(light, axis=0)

img = Image.fromarray(out)
d = ImageDraw.Draw(img)
for (x0, y0, x1, y1), wrong, right, mode in boxes:
    # Schriftgroesse so waehlen, dass das falsche Wort genau die Originalbreite haette
    size = 10
    while True:
        f = ImageFont.truetype(FONT, size + 1)
        l, t, r, b = d.textbbox((0, 0), wrong, font=f)
        if (mode == 'w' and r - l > (x1 - x0)) or (mode == 'h' and b - t > (y1 - y0)):
            break
        size += 1
    f = ImageFont.truetype(FONT, size)
    wl, wt, wr, wb = d.textbbox((0, 0), wrong, font=f)
    l, t, r, b = d.textbbox((0, 0), right, font=f)
    # Breitenmodus: zentriert; Hoehenmodus (Zeilenende): linksbuendig
    left = (x0 + x1) / 2 - (r - l) / 2 if mode == 'w' else x0
    d.text((left - l, y0 - wt), right, font=f, fill=(24, 24, 30))
img.save(DST)
print('fertig', DST)
