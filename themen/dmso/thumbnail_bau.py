"""YouTube-Thumbnail (1280x720), Stil G: Bild ohne Schrift (GPT Image 2, 16:9), Titel per PIL. Aufruf: python3 thumbnail_bau.py"""
import os, sys
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', 'schulprojekt-vitamin-d', 'erklaervideo')); sys.path.insert(0, os.path.join(HIER, '..', '..', 'werkzeug'))
import bilder_bau as BB
MOTIV = ("on the right half of the image: a large old-fashioned glass laboratory flask with a perfectly clear liquid, its lower part "
         "covered in sparkling white frost and ice crystals, cold blue vapor curling around it, a few tiny round cells floating safely "
         "inside the liquid. The entire left half of the image is a calm, plain, light empty paper background with no objects, reserved for a title.")
REGEL = BB.KEIN_TEXT + ' Absolutely no words or letters anywhere. Wide 16:9 composition, the motif large and bold for a small phone thumbnail.'
os.makedirs(os.path.join(HIER, 'thumbnail'), exist_ok=True)
ziel = os.path.join(HIER, 'thumbnail', 'bild_G.jpg')
if not os.path.exists(ziel):
    print('Credits', round(BB.erzeuge(BB.STILE['G'] + REGEL, MOTIV, ziel, config={'size': '2048x1152'}), 1))

from PIL import Image, ImageDraw, ImageFont, ImageFilter
SERIF_B = '/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf'
haupt, akzent = (44, 52, 68), (176, 92, 52)
im = Image.open(ziel).convert('RGB').resize((1280, 720), Image.LANCZOS)
schatten = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(schatten)
texte = [((70, 90), 'DMSO', 210, akzent), ((76, 380), 'Vom Lösungs-', 84, haupt), ((76, 480), 'mittel zum', 84, haupt), ((76, 580), 'Kälteschutz', 84, haupt)]
for (x, y), t, g, _ in texte:
    d.text((x + 4, y + 5), t, font=ImageFont.truetype(SERIF_B, g), fill=(255, 255, 255, 170))
im = Image.alpha_composite(im.convert('RGBA'), schatten.filter(ImageFilter.GaussianBlur(6)))
d = ImageDraw.Draw(im)
for (x, y), t, g, f in texte:
    d.text((x, y), t, font=ImageFont.truetype(SERIF_B, g), fill=f)
im.convert('RGB').save(os.path.join(HIER, 'thumbnail', 'thumbnail_G.jpg'), quality=90)
print('Thumbnail gesetzt')
