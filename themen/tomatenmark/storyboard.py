"""Storyboard: je Szene Bild a/b links, Sprechtext rechts (ab welchem Satz Bild b läuft), Ampel-Stichpunkte."""
import json, textwrap
from PIL import Image, ImageDraw, ImageFont
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'
f, fb, fh = ImageFont.truetype(F + '.ttf', 22), ImageFont.truetype(F + '-Bold.ttf', 22), ImageFont.truetype(F + '-Bold.ttf', 32)
FARBE = {'stark': '#2e7d4f', 'mittel': '#b8860b', 'keine': '#b5382e'}
c = json.load(open('szenen.json'))
IW, IH, TX, W = 560, 315, 600, 1500
bloecke = []
for sc in c['scenes'][1:]:
    shots = sc['shots']; b_at = shots[1].get('at', 0)
    bl = {b['at']: b for b in sc.get('bullets', [])}
    zeilen = []
    for i, s in enumerate(sc['sentences']):
        t = s['t'] if isinstance(s, dict) else s
        if i == b_at: zeilen.append(('marke', '▼ ab hier Bild b'))
        for j, z in enumerate(textwrap.wrap(t, 62 if t.startswith('Dein Tipp') else 70)):
            zeilen.append(('tipp' if t.startswith('Dein Tipp') else 'text', ('• ' if j == 0 else '  ') + z))
        if i in bl: zeilen.append((bl[i]['ev'], '    ▶ ' + bl[i]['t']))
    h = max(2 * IH + 70, 60 + 30 * len(zeilen)) + 30
    im = Image.new('RGB', (W, h), '#f8f4ec'); d = ImageDraw.Draw(im)
    d.text((20, 12), f"{sc['id'][1]}  {sc['headline']}", font=fh, fill='#1f2a3a')
    for k, s in enumerate(shots[:2]):
        y = 60 + k * (IH + 10)
        im.paste(Image.open(s['bild']).convert('RGB').resize((IW, IH)), (20, y))
        d.rectangle((20, y, 70, y + 34), fill='#1f2a3a'); d.text((30, y + 4), 'ab'[k], font=fb, fill='white')
    y = 62
    for art, z in zeilen:
        farbe = {'text': '#1f2a3a', 'tipp': '#46597f', 'marke': '#c0543a'}.get(art, FARBE.get(art))
        d.text((TX, y), z, font=fb if art not in ('text',) else f, fill=farbe); y += 30
    d.line((0, h - 2, W, h - 2), fill='#d8cbb4', width=3)
    bloecke.append(im)
gesamt = Image.new('RGB', (W, sum(b.height for b in bloecke)), '#f8f4ec')
y = 0
for b in bloecke: gesamt.paste(b, (0, y)); y += b.height
gesamt.save('storyboard.png'); print(gesamt.size)
