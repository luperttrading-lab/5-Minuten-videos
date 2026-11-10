"""YouTube-Thumbnails (1280x720) je Stil: Bild ohne Schrift (GPT Image 2, 16:9), Titel per PIL. Aufruf: python3 thumbnail_bau.py"""
import os, sys, json
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', 'schulprojekt-vitamin-d', 'erklaervideo')); sys.path.insert(0, os.path.join(HIER, '..', '..', 'werkzeug'))
import bilder_bau as BB
MOTIV = ("on the right half of the image: a large cracked egg with a glowing bright golden yolk, and beside it a single large white capsule "
         "that glows softly; warm dramatic light, a few tiny golden sparkles. The entire left half of the image is a calm, plain, "
         "slightly darker empty background with no objects, reserved for a title.")
REGEL = BB.KEIN_TEXT + ' Absolutely no words or letters anywhere. Wide 16:9 composition, the motif large and bold for a small phone thumbnail.'
os.makedirs(os.path.join(HIER, 'thumbnail'), exist_ok=True)
kosten = {}
for s in ('I', 'G', 'D'):
    ziel = os.path.join(HIER, 'thumbnail', f'bild_{s}.jpg')
    if not os.path.exists(ziel):
        kosten[s] = round(BB.erzeuge(BB.STILE[s] + REGEL, MOTIV, ziel, config={'size': '2048x1152'}), 1)
print('Credits', kosten)

# Titel setzen (eigene Schrift, keine KI-Schrift): „PEA“ groß, Unterzeile zweizeilig, Schatten für Lesbarkeit auf dem Handy
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SERIF_B = '/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf'
FARBE = {'I': ((255, 246, 228), (255, 196, 90)), 'G': ((44, 52, 68), (176, 92, 52)), 'D': ((255, 248, 236), (255, 200, 110))}
for s in ('I', 'G', 'D'):
    im = Image.open(os.path.join(HIER, 'thumbnail', f'bild_{s}.jpg')).convert('RGB').resize((1280, 720), Image.LANCZOS)
    haupt, akzent = FARBE[s]
    hell = s == 'G'
    schatten = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(schatten)
    texte = [((70, 90), 'PEA', 230, akzent), ((76, 400), 'Vom Eigelb', 86, haupt), ((76, 500), 'zur Schmerz-', 86, haupt), ((76, 600), 'forschung', 86, haupt)]
    for (x, y), t, g, _ in texte:
        d.text((x + 4, y + 5), t, font=ImageFont.truetype(SERIF_B, g), fill=(255, 255, 255, 170) if hell else (0, 0, 0, 200))
    schatten = schatten.filter(ImageFilter.GaussianBlur(6))
    im = Image.alpha_composite(im.convert('RGBA'), schatten)
    d = ImageDraw.Draw(im)
    for (x, y), t, g, f in texte:
        d.text((x, y), t, font=ImageFont.truetype(SERIF_B, g), fill=f)
    im.convert('RGB').save(os.path.join(HIER, 'thumbnail', f'thumbnail_{s}.jpg'), quality=90)
print('Thumbnails gesetzt')
