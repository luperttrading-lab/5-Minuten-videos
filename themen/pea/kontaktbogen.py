"""Kontaktbogen je Stil zur Sichtprüfung: python3 kontaktbogen.py I G D  →  kontakt_<Stil>.jpg (nicht einchecken)."""
import sys, os, glob
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
for stil in sys.argv[1:]:
    dateien = sorted(glob.glob(f'bilder/{stil}/*.jpg'), key=lambda p: (not os.path.basename(p).startswith('k'), p))
    dateien = [d for d in dateien if '_alt' not in d]
    W, H, n = 400, 320, 7
    bogen = Image.new('RGB', (n * W, ((len(dateien) + n - 1) // n) * H), 'white')
    for i, d in enumerate(dateien):
        im = Image.open(d); im.thumbnail((W - 6, H - 6))
        x, y = (i % n) * W, (i // n) * H
        bogen.paste(im, (x + 3, y + 3))
        ImageDraw.Draw(bogen).text((x + 8, y + 6), os.path.basename(d)[:-4], font=F, fill='white', stroke_width=3, stroke_fill='black')
    bogen.save(f'kontakt_{stil}.jpg', quality=82)
    print(stil, len(dateien))
