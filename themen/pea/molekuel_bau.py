"""Echte Strukturformel von PEA (C18H37NO2) statt KI-Fantasiemolekül (Nutzerfrage 11.11.: „Was für ein Baustein?“).
Koordinaten aus RDKit, gezeichnet mit PIL im Format der Szenenbilder (1280x1024), Farben je Stil.
Ausgabe: molekuel/p2d_<Stil>.jpg. Aufruf: python3 molekuel_bau.py"""
import os
from rdkit import Chem
from rdkit.Chem import AllChem
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HIER = os.path.dirname(os.path.abspath(__file__))
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SERIF_B = '/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf'
m = Chem.MolFromSmiles('CCCCCCCCCCCCCCCC(=O)NCCO')
AllChem.Compute2DCoords(m)
c = m.GetConformer()
P = [(c.GetAtomPosition(i).x, c.GetAtomPosition(i).y) for i in range(m.GetNumAtoms())]
# Kette waagrecht legen: Achse von Atom 0 zu Atom 18 (O der OH-Gruppe)
import math
a = math.atan2(P[20][1] - P[0][1], P[20][0] - P[0][0])
P = [(x * math.cos(-a) - y * math.sin(-a), x * math.sin(-a) + y * math.cos(-a)) for x, y in P]
xs, ys = [p[0] for p in P], [p[1] for p in P]
W, H = 1280, 1024
s = (W - 300) / (max(xs) - min(xs))
cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
Q = [((x - cx) * s + W / 2, -(y - cy) * s + H / 2 - 40) for x, y in P]
STIL = {  # Grund, Tinte, Fettsäure, Ethanolamin, Amidbindung
 'G': ((246, 239, 226), (40, 44, 56), (196, 150, 70), (96, 128, 160), (178, 86, 52)),
 'I': ((253, 243, 225), (52, 40, 32), (240, 170, 60), (70, 140, 200), (220, 80, 60)),
 'D': ((240, 228, 205), (70, 52, 40), (232, 160, 60), (80, 130, 190), (210, 80, 60)),
}
os.makedirs(os.path.join(HIER, 'molekuel'), exist_ok=True)
for stil, (grund, tinte, fett, eth, amid) in STIL.items():
    im = Image.new('RGB', (W, H), grund)
    d = ImageDraw.Draw(im)
    # farbige Unterlegung der beiden Teile
    def blase(idx, farbe):
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        for i in idx:
            x, y = Q[i]; ld.ellipse((x - 46, y - 46, x + 46, y + 46), fill=farbe + (70,))
        return lay.filter(ImageFilter.GaussianBlur(14))
    im = Image.alpha_composite(im.convert('RGBA'), blase(range(0, 17), fett))
    im = Image.alpha_composite(im, blase(range(17, 21), eth)).convert('RGB')
    d = ImageDraw.Draw(im)
    for b in m.GetBonds():
        i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
        (x1, y1), (x2, y2) = Q[i], Q[j]
        farbe, breite = (amid, 13) if {i, j} == {15, 17} else (tinte, 9)
        def kuerze(xa, ya, xb, yb, k):   # Linie vor Atomsymbol enden lassen
            L = math.hypot(xb - xa, yb - ya); return xa + (xb - xa) * k / L, ya + (yb - ya) * k / L
        A = m.GetAtomWithIdx(i).GetSymbol(); Bs = m.GetAtomWithIdx(j).GetSymbol()
        if A != 'C': x1, y1 = kuerze(x1, y1, x2, y2, 30)
        if Bs != 'C': x2, y2 = kuerze(x2, y2, x1, y1, 30 if j != 20 else 24)
        d.line((x1, y1, x2, y2), fill=farbe, width=breite)
        if b.GetBondTypeAsDouble() == 2:
            nx, ny = -(y2 - y1), x2 - x1; L = math.hypot(nx, ny); nx, ny = nx / L * 13, ny / L * 13
            d.line((x1 + nx, y1 + ny, x2 + nx, y2 + ny), fill=farbe, width=breite)
    f = ImageFont.truetype(SANS_B, 46); fh = ImageFont.truetype(SANS_B, 34)
    for i, at in enumerate(m.GetAtoms()):
        sym = at.GetSymbol()
        if sym == 'C': continue
        x, y = Q[i]
        if sym == 'N':                      # H unter das N, damit keine Bindung durch die Schrift läuft
            d.text((x, y), 'N', font=f, fill=amid, anchor='mm'); d.text((x, y + 42), 'H', font=fh, fill=amid, anchor='mm')
        else:
            if i == 20: d.text((x - 16, y), 'OH', font=f, fill=tinte, anchor='lm')
            else: d.text((x, y), 'O', font=f, fill=tinte, anchor='mm')
    fb = ImageFont.truetype(SERIF_B, 58); fk = ImageFont.truetype(SANS_B, 34)
    xa = (Q[0][0] + Q[15][0]) / 2; xb = min(sum(Q[i][0] for i in (17, 18, 19, 20)) / 4, W - 190)
    yu = max(y for _, y in Q) + 110
    d.text((xa, yu), 'Palmitinsäure', font=fb, fill=tinte, anchor='mm')
    d.text((xa, yu + 56), '16 Kohlenstoffe, auch in Palmöl', font=fk, fill=tinte, anchor='mm')
    d.text((xb, yu), 'Ethanolamin', font=fb, fill=tinte, anchor='mm')
    yo = min(y for _, y in Q) - 120
    d.text((W / 2, yo), 'PEA', font=ImageFont.truetype(SERIF_B, 96), fill=amid, anchor='mm')
    im.save(os.path.join(HIER, 'molekuel', f'p2d_{stil}.jpg'), quality=92)
print('fertig')
