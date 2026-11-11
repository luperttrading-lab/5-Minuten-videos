"""PEA als Kugel-Stab-Modell (Nutzerwunsch 11.11.: Kugeln wie im alten Bild, aber chemisch richtig, ohne Palmfrucht).
Echte 3D-Geometrie (RDKit, Kette gestreckt), alle 56 Atome (18 C, 37 H, 1 N, 2 O), Kugeln je Stil schattiert.
Ausgabe: molekuel/p2d_kugeln_<Stil>.jpg (1280x1024). Aufruf: python3 kugeln_bau.py"""
import os, math, random
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolTransforms as T
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HIER = os.path.dirname(os.path.abspath(__file__))
m = Chem.AddHs(Chem.MolFromSmiles('CCCCCCCCCCCCCCCC(=O)NCCO'))
AllChem.EmbedMolecule(m, randomSeed=7); AllChem.MMFFOptimizeMolecule(m)
c = m.GetConformer()
kette = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20]   # C1..C16, N, C, C, O
KNICK = {int(k): float(v) for k, v in (x.split(':') for x in os.environ.get('KNICK', '3:65,8:-65,13:65').split(',') if x)}
for k in range(len(kette) - 3):
    a, b, cc, d = kette[k:k + 4]
    T.SetDihedralDeg(c, a, b, cc, d, KNICK.get(k, 180.0))                         # gestreckt, an wenigen Stellen gedreht (Kette ist beweglich)
X = np.array([list(c.GetAtomPosition(i)) for i in range(m.GetNumAtoms())])
X -= X.mean(0)
u, s, vt = np.linalg.svd(X[[i for i in range(m.GetNumAtoms()) if m.GetAtomWithIdx(i).GetSymbol() != 'H']], full_matrices=False)
X = X @ vt.T                                                                       # Hauptachse = x
def rot(X, ax, deg):
    t = math.radians(deg); cs, sn = math.cos(t), math.sin(t)
    R = {'x': [[1, 0, 0], [0, cs, -sn], [0, sn, cs]], 'y': [[cs, 0, sn], [0, 1, 0], [-sn, 0, cs]], 'z': [[cs, -sn, 0], [sn, cs, 0], [0, 0, 1]]}[ax]
    return X @ np.array(R).T
X = rot(X, 'x', float(os.environ.get('RX', 15)))          # Zickzack sichtbar machen, H oben/unten und vorn/hinten
X = rot(X, 'z', float(os.environ.get('RZ', 0)))          # leicht schräg, nutzt die Bildhöhe
if X[20, 0] < X[0, 0]: X[:, 0] *= -1                                               # Ethanolamin rechts
W, H = 1280, 1024
xs, ys = X[:, 0], X[:, 1]
sk = min((W - 220) / (xs.max() - xs.min()), (H - 330) / (ys.max() - ys.min()))
P = [((x - (xs.max() + xs.min()) / 2) * sk + W / 2, -(y - (ys.max() + ys.min()) / 2) * sk + H / 2 - 40, z) for x, y, z in X]
R = {'C': 0.42, 'N': 0.42, 'O': 0.42, 'H': 0.26}
STIL_ALLE = {  # Grund oben, Grund unten, C, N, O, H, Stab, Umriss
 'G': ((247, 240, 226), (240, 228, 205), (150, 168, 132), (96, 130, 168), (196, 98, 70), (242, 236, 222), (120, 110, 100), (60, 56, 52)),
 'I': ((255, 236, 205), (232, 170, 110), (90, 100, 110), (70, 120, 220), (225, 70, 60), (250, 250, 250), (210, 210, 215), None),
 'D': ((236, 222, 196), (214, 196, 166), (110, 150, 110), (80, 120, 190), (215, 90, 70), (248, 240, 225), (190, 170, 140), None),
}
STIL = {k: v for k, v in STIL_ALLE.items() if k in os.environ.get('NUR_STIL', 'GID')}
def kugel(r, farbe, stil):
    n = int(2 * r) + 4; im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); px = im.load()
    for yy in range(n):
        for xx in range(n):
            dx, dy = (xx - n / 2) / r, (yy - n / 2) / r; q = dx * dx + dy * dy
            if q > 1: continue
            dz = math.sqrt(1 - q)
            l = max(0, (-0.45 * dx - 0.55 * dy + 0.7 * dz))                       # Licht von links oben
            if stil == 'I':
                f = 0.35 + 0.75 * l; sp = max(0, l) ** 28 * 1.2
            elif stil == 'D':
                f = 0.55 + 0.5 * l + random.uniform(-0.03, 0.03); sp = max(0, l) ** 10 * 0.18
            else:
                f = 0.72 + 0.35 * l; sp = 0
            col = [min(255, int(ch * f + 255 * sp)) for ch in farbe]
            a = 255 if stil != 'G' else int(235 * min(1, (1 - q) * 6 + 0.55))
            px[xx, yy] = tuple(col) + (a,)
    return im
for stil, (g1, g2, cC, cN, cO, cH, stab, umriss) in STIL.items():
    random.seed(1)
    bg = Image.new('RGB', (W, H)); d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / H; d.line((0, y, W, y), fill=tuple(int(g1[i] * (1 - t) + g2[i] * t) for i in range(3)))
    if stil == 'G':  # Papier: feines Rauschen
        no = (np.random.default_rng(3).normal(0, 6, (H, W, 1))).astype(np.int16)
        bg = Image.fromarray(np.clip(np.array(bg).astype(np.int16) + no, 0, 255).astype(np.uint8))
    im = bg.convert('RGBA')
    # weicher Schatten unter dem Molekül
    sch = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sch)
    for x, y, z in P:
        sd.ellipse((x - 30, y + 150 - 14, x + 30, y + 150 + 14), fill=(60, 40, 20, 40))
    im = Image.alpha_composite(im, sch.filter(ImageFilter.GaussianBlur(22)))
    # Stäbe und Kugeln nach Tiefe sortiert zeichnen
    teile = []
    for b in m.GetBonds():
        i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx(); teile.append((min(P[i][2], P[j][2]) - 0.5, 'b', i, j, b.GetBondTypeAsDouble()))
    for i, at in enumerate(m.GetAtoms()):
        teile.append((P[i][2], 'a', i, at.GetSymbol(), 0))
    teile.sort(key=lambda t: t[0])
    d = ImageDraw.Draw(im)
    farbe = {'C': cC, 'N': cN, 'O': cO, 'H': cH}
    cache = {}
    for z, art, i, j, typ in teile:
        if art == 'b':
            (x1, y1, _), (x2, y2, _) = P[i], P[j]
            if typ == 2:
                nx, ny = -(y2 - y1), x2 - x1; L = math.hypot(nx, ny); nx, ny = nx / L * 8, ny / L * 8
                for sgn in (1, -1):
                    if umriss: d.line((x1 + sgn * nx, y1 + sgn * ny, x2 + sgn * nx, y2 + sgn * ny), fill=umriss, width=9)
                    d.line((x1 + sgn * nx, y1 + sgn * ny, x2 + sgn * nx, y2 + sgn * ny), fill=stab, width=6)
            else:
                if umriss: d.line((x1, y1, x2, y2), fill=umriss, width=12)
                d.line((x1, y1, x2, y2), fill=stab, width=8)
        else:
            sym = j; r = R[sym] * sk * (1 + 0.04 * z)
            key = (sym, int(r))
            if key not in cache: cache[key] = kugel(r, farbe[sym], stil)
            k = cache[key]; x, y, _ = P[i]
            if umriss:
                d.ellipse((x - r - 2, y - r - 2, x + r + 2, y + r + 2), outline=umriss, width=3)
            im.alpha_composite(k, (int(x - k.width / 2), int(y - k.height / 2)))
            d = ImageDraw.Draw(im)
    # dezente Beschriftung unten: welcher Teil ist was
    f = ImageFont.truetype('/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf', 50)
    tinte = (60, 56, 52) if stil != 'I' else (70, 40, 20)
    xa = sum(P[i][0] for i in range(16)) / 16; xb = min(sum(P[i][0] for i in (17, 18, 19, 20)) / 4, W - 170)
    yu = H - 150
    d.text((xa, yu), 'Palmitinsäure', font=f, fill=tinte, anchor='mm')
    d.text((xb, yu), 'Ethanolamin', font=f, fill=tinte, anchor='mm')
    im.convert('RGB').save(os.path.join(HIER, 'molekuel', f'p2d_kugeln_{stil}' + os.environ.get('SUFFIX', '') + '.jpg'), quality=92)
    print(stil)
