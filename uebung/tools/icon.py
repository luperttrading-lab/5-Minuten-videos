#!/usr/bin/env python3
"""Home-Bildschirm-Symbol: „16·18“ in den Videofarben auf Papiergrund, darunter ein dunkelgrüner Balken.
Aufruf: python3 tools/icon.py (aus dem Ordner uebung/)"""
import subprocess
from PIL import Image, ImageDraw, ImageFont

def fc(n):
    return subprocess.check_output(['fc-match', '-f', '%{file}', n]).decode()

F = fc('Inter:extrabold')

def symbol(groesse, rand):
    k = 4
    s = groesse * k
    img = Image.new('RGB', (s, s), (246, 241, 231))
    d = ImageDraw.Draw(img)
    inner = s - 2 * rand * k
    f = ImageFont.truetype(F, int(inner * 0.30))
    teile = [('1', (43, 45, 66)), ('6', (232, 137, 12)), ('·', (43, 45, 66)), ('1', (43, 45, 66)), ('8', (131, 56, 236))]
    breite = sum(d.textlength(t, font=f) for t, _ in teile)
    x, y = (s - breite) / 2, s * 0.40
    for t, c in teile:
        d.text((x, y), t, font=f, fill=c, anchor='ls')
        x += d.textlength(t, font=f)
    d.rounded_rectangle([s * 0.5 - inner * 0.34, s * 0.52, s * 0.5 + inner * 0.34, s * 0.52 + inner * 0.16],
                        radius=inner * 0.05, fill=(15, 118, 110))
    f2 = ImageFont.truetype(F, int(inner * 0.12))
    d.text((s / 2, s * 0.52 + inner * 0.08), '288', font=f2, fill=(255, 255, 255), anchor='mm')
    return img.resize((groesse, groesse), Image.LANCZOS)

symbol(180, 0).save('apple-touch-icon.png')
symbol(192, 0).save('icon-192.png')
symbol(512, 0).save('icon-512.png')
symbol(512, 60).save('icon-maskable.png')
print('Symbole geschrieben')
