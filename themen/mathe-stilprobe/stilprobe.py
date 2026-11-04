#!/usr/bin/env python3
"""Stilprobe Mathe-Videos: dieselbe 15-Sekunden-Szene (13 · 17 = 15² − 2² = 221) in zehn Grafikstilen, ohne Ton.
Alles wird per Code gezeichnet (keine KI-Bilder), damit Zahlen und Formeln exakt stimmen.

Aufruf: python3 stilprobe.py <ausordner> [stil ...]      Bild statt Video: --bild <sekunde>
Szene: Rechteck 17 × 13 → Streifen 2 × 13 abschneiden, drehen, oben anlegen → Quadrat 15 × 15 ohne Ecke 2 × 2.
"""
import math, os, random, subprocess, sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HIER = os.path.dirname(os.path.abspath(__file__))
SCHRIFTEN = os.path.join(HIER, '..', '..', 'werkzeug', 'schriften')
W, H, FPS, DAUER = 1280, 720, 30, 15.0


def fc(name):
    return subprocess.check_output(['fc-match', '-f', '%{file}', name]).decode()


def datei(n):
    return os.path.join(SCHRIFTEN, n)


# ---------- Stile ----------
STILE = {
    'flat': dict(name='Flat Design', bg=('flach', '#fbf3e4'), ink='#2b2d42', f1='#ffb703', f2='#219ebc', hi='#e63946',
                 schrift_t=fc('Inter:extrabold'), schrift_m=fc('Inter:bold'), lw=4, schatten=True, ein='pop', rund=True),
    'whiteboard': dict(name='Whiteboard (Handzeichnung)', bg=('flach', '#fdfdfb'), ink='#1d1d1d', f1='#ffd166',
                       f2='#8ecae6', hi='#d62828', schrift_t=datei('Kalam-Bold.ttf'), schrift_m=datei('Kalam-Bold.ttf'),
                       lw=5, hand=1.6, wackeln=True, ein='schreiben', fuell_a=170),
    'kreide': dict(name='Kreidetafel', bg=('kreide', '#27443a'), ink='#f1f1e8', f1='#f6e27f', f2='#9ad0ec', hi='#f4978e',
                   schrift_t=datei('Caveat.ttf'), schrift_m=datei('Caveat.ttf'), lw=5, hand=2.0, korn=True, fuell_a=70,
                   ein='schreiben', groesse=1.25),
    'dunkel': dict(name='Dunkle Vektorgrafik', bg=('flach', '#0f1317'), ink='#e8e8e8', f1='#3b82c4', f2='#e8a93a',
                   hi='#fc6255', schrift_t=fc('DejaVu Serif'), schrift_m=fc('DejaVu Serif'), lw=3, glanz=0.7, fuell_a=120,
                   ein='schreiben'),
    'heft': dict(name='Schulheft (Karopapier)', bg=('karo', '#fbfbf6'), ink='#1f3f9c', f1='#a9cbff', f2='#ffd59a',
                 hi='#d7263d', schrift_t=datei('PatrickHand-Regular.ttf'), schrift_m=datei('PatrickHand-Regular.ttf'),
                 lw=3, hand=1.0, ein='schreiben', fuell_a=150, groesse=1.1),
    'blaupause': dict(name='Blaupause (Blueprint)', bg=('blau', '#1d4e89'), ink='#eaf2ff', f1='#eaf2ff', f2='#ffd166',
                      hi='#ffd166', schrift_t=fc('JetBrains Mono:bold'), schrift_m=fc('JetBrains Mono'), lw=2,
                      fuell_a=40, ein='tippen', massketten=True, groesse=0.85),
    'swiss': dict(name='Minimalistisch (Swiss Style)', bg=('flach', '#ffffff'), ink='#111111', f1='#e9e9e9',
                  f2='#e10600', hi='#e10600', schrift_t=fc('Inter Display:black'), schrift_m=fc('Inter:semibold'), lw=3,
                  ein='gleiten'),
    'comic': dict(name='Comic / Pop-Art', bg=('punkte', '#ffe14d'), ink='#111111', f1='#4cc9f0', f2='#f72585',
                  hi='#ff3b30', schrift_t=datei('Bangers-Regular.ttf'), schrift_m=datei('Bangers-Regular.ttf'),
                  schrift_f=fc('Inter Display:black'), lw=8,
                  ein='pop', textrand=True, titelfarbe='#ffffff', knall=True, groesse=1.15),
    'pixel': dict(name='Pixel-Art (Retro)', bg=('flach', '#1a1c2c'), ink='#f4f4f4', f1='#41a6f6', f2='#ffcd75',
                  hi='#ef7d57', schrift_t=datei('PressStart2P-Regular.ttf'), schrift_m=datei('PressStart2P-Regular.ttf'),
                  lw=4, pixel=True, ein='tippen', ersatz={' − ': '-', ' + ': '+', '−': '-'}),
    'neon': dict(name='Neon (Synthwave)', bg=('neon', '#1b0b3a'), ink='#f8f8ff', f1='#00e5ff', f2='#ff2bd6',
                 hi='#fffb00', schrift_t=fc('Inter:bold'), schrift_m=fc('Inter:semibold'), lw=4, glanz=1.5, fuell_a=45,
                 ein='schreiben'),
}


def farbe(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def klemm(x):
    return max(0.0, min(1.0, x))


def glatt(x):
    x = klemm(x)
    return x * x * (3 - 2 * x)


def zurueck(x):                                   # easeOutBack für „pop“
    x = klemm(x)
    c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def p(t, start, dauer):
    return klemm((t - start) / dauer)


# ---------- Geometrie der Szene (Grundkoordinaten 1280 × 720) ----------
U = 24
X0, Y0 = 110, 262                                  # linke obere Ecke des Rechtecks 17 × 13


class Leinwand:
    def __init__(self, s):
        self.s = s
        self.k = 0.25 if s.get('pixel') else 2.0       # Pixel-Art klein zeichnen, sonst 2× für Kantenglättung
        self.w, self.h = int(W * self.k), int(H * self.k)
        self.schriften = {}
        self.textcache = {}
        self.grund = self.hintergrund()
        if s.get('korn'):
            rnd = Image.frombytes('L', (self.w, self.h), os.urandom(self.w * self.h))
            self.kornmaske = rnd.point(lambda v: 175 + v * 80 // 255)

    # Schriften in Grundpixeln, für Pixel-Art auf 8er-Raster
    def schrift(self, pfad, g):
        if self.s.get('pixel'):
            px = 16 if g >= 60 else 8
        else:
            px = int(g * self.s.get('groesse', 1.0) * self.k)
        key = (pfad, px)
        if key not in self.schriften:
            self.schriften[key] = ImageFont.truetype(pfad, px)
        return self.schriften[key]

    def hintergrund(self):
        art, c = self.s['bg'][0], self.s['bg'][1]
        img = Image.new('RGBA', (self.w, self.h), farbe(c))
        d = ImageDraw.Draw(img, 'RGBA')
        k = self.k
        if art == 'kreide':
            rnd = random.Random(3)                     # Wischspuren: helle Wolken auf eigener Ebene, weichgezeichnet
            wolken = Image.new('RGBA', img.size, (255, 255, 255, 0))
            dw = ImageDraw.Draw(wolken)
            for _ in range(14):
                x, y, r = rnd.uniform(0, self.w), rnd.uniform(0, self.h), rnd.uniform(80, 260) * k
                dw.ellipse([x - r * 1.8, y - r, x + r * 1.8, y + r], fill=(255, 255, 255, 14))
            img.alpha_composite(wolken.filter(ImageFilter.GaussianBlur(40 * k)))
            rausch = Image.frombytes('L', (self.w, self.h), os.urandom(self.w * self.h)).point(lambda v: v // 22)
            img = Image.composite(Image.new('RGBA', img.size, (255, 255, 255, 255)), img,
                                  rausch.point(lambda v: v * 2))
        elif art == 'karo':
            for x in range(0, W, 28):
                d.line([(x * k, 0), (x * k, self.h)], fill=(120, 160, 210, 70), width=max(1, int(k)))
            for y in range(0, H, 28):
                d.line([(0, y * k), (self.w, y * k)], fill=(120, 160, 210, 70), width=max(1, int(k)))
            d.line([(70 * k, 0), (70 * k, self.h)], fill=(220, 60, 60, 160), width=int(2 * k))
        elif art == 'blau':
            for x in range(0, W, 24):
                a = 70 if x % 120 == 0 else 28
                d.line([(x * k, 0), (x * k, self.h)], fill=(255, 255, 255, a), width=max(1, int(k)))
            for y in range(0, H, 24):
                a = 70 if y % 120 == 0 else 28
                d.line([(0, y * k), (self.w, y * k)], fill=(255, 255, 255, a), width=max(1, int(k)))
        elif art == 'punkte':
            for y in range(0, H + 18, 18):
                for x in range(0, W + 18, 18):
                    r = 1.5 + 4.5 * ((x + y) / (W + H))
                    xx = x + (9 if (y // 18) % 2 else 0)
                    d.ellipse([(xx - r) * k, (y - r) * k, (xx + r) * k, (y + r) * k], fill=(255, 150, 0, 90))
        elif art == 'neon':
            for y in range(self.h):                    # Verlauf von Violett nach Fast-Schwarz
                f = y / self.h
                d.line([(0, y), (self.w, y)], fill=(int(27 * (1 - f) + 5 * f), int(11 * (1 - f) + 2 * f),
                                                    int(58 * (1 - f) + 15 * f), 255))
            hor = 620
            for i in range(-20, 21):                   # Perspektivgitter am Boden
                d.line([(W / 2 * k, hor * k), ((W / 2 + i * 120) * k, H * k)], fill=(255, 43, 214, 60), width=int(k))
            for j in range(1, 8):
                y = hor + (H - hor) * (j / 7) ** 1.8
                d.line([(0, y * k), (self.w, y * k)], fill=(255, 43, 214, 60), width=int(k))
        return img

    # ----- Linien -----
    def pfad_wackeln(self, pts, seed, t):
        amp = self.s.get('hand', 0)
        if not amp:
            return pts
        stufe = int(t * 8) if self.s.get('wackeln') else 0     # „boil“: Linien zittern 8× pro Sekunde
        rnd = random.Random(seed * 1000 + stufe)
        aus = []
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            n = max(2, int(math.hypot(x2 - x1, y2 - y1) / 18))
            for i in range(n):
                f = i / n
                aus.append((x1 + (x2 - x1) * f + rnd.uniform(-amp, amp), y1 + (y2 - y1) * f + rnd.uniform(-amp, amp)))
        aus.append((pts[-1][0] + rnd.uniform(-amp, amp), pts[-1][1] + rnd.uniform(-amp, amp)))
        return aus

    @staticmethod
    def teilpfad(pts, anteil):
        if anteil >= 1:
            return pts
        laengen = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
        ziel = sum(laengen) * anteil
        aus = [pts[0]]
        for (a, b), l in zip(zip(pts, pts[1:]), laengen):
            if ziel <= l:
                f = ziel / l if l else 0
                aus.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
                return aus
            aus.append(b)
            ziel -= l
        return aus

    def linie(self, d, pts, c, lw, anteil=1.0, alpha=1.0, seed=0, t=0, gestrichelt=False):
        if anteil <= 0 or alpha <= 0:
            return
        k = self.k
        pts = self.teilpfad(pts, anteil)
        if gestrichelt:
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                l = math.hypot(x2 - x1, y2 - y1)
                n = max(1, int(l / 14))
                for i in range(0, n, 2):
                    a, b = i / n, min(1, (i + 1) / n)
                    d.line([((x1 + (x2 - x1) * a) * k, (y1 + (y2 - y1) * a) * k),
                            ((x1 + (x2 - x1) * b) * k, (y1 + (y2 - y1) * b) * k)],
                           fill=farbe(c, int(255 * alpha)), width=max(1, int(lw * k)))
            return
        pts = self.pfad_wackeln(pts, seed, t)
        d.line([(x * k, y * k) for x, y in pts], fill=farbe(c, int(255 * alpha)), width=max(1, int(lw * k)),
               joint='curve')

    def flaeche(self, d, pts, c, alpha, seed=0, t=0):
        if alpha <= 0:
            return
        a = int(self.s.get('fuell_a', 255) * alpha)
        pts = self.pfad_wackeln(pts + [pts[0]], seed + 77, t) if self.s.get('hand') else pts
        d.polygon([(x * self.k, y * self.k) for x, y in pts], fill=farbe(c, a))

    # ----- Text -----
    def textbild(self, s, pfad, g, c, titel=False):
        for a, b in self.s.get('ersatz', {}).items():
            s = s.replace(a, b)
        key = (s, pfad, g, c, titel)
        if key not in self.textcache:
            f = self.schrift(pfad, g)
            rand = int(2.5 * self.k) if self.s.get('textrand') and titel else 0
            if '²' in s and not self.s.get('pixel'):
                self.textcache[key] = self.hochzahl_text(s, f, c, rand)
                return self.textcache[key]
            l, o, r, u = f.getbbox(s, stroke_width=rand)
            img = Image.new('RGBA', (r - l + 4, u - o + 4), (0, 0, 0, 0))
            dd = ImageDraw.Draw(img)
            if self.s.get('pixel'):
                dd.fontmode = '1'
            dd.text((-l + 2, -o + 2), s, font=f, fill=farbe(c), stroke_width=rand,
                    stroke_fill=farbe(self.s['ink']) if rand else None)
            self.textcache[key] = img
        return self.textcache[key]

    def hochzahl_text(self, s, f, c, rand):
        """Hochzahl selbst setzen (kleine, angehobene 2): Manche Schriften haben ein ² in voller Größe (Bangers)."""
        klein = ImageFont.truetype(f.path, int(f.size * 0.62))
        teile = s.split('²')
        asc, desc = f.getmetrics()
        breite = sum(f.getlength(t) for t in teile) + klein.getlength('2') * (len(teile) - 1) + 2 * rand + 8
        img = Image.new('RGBA', (int(breite), asc + desc + 2 * rand + 4), (0, 0, 0, 0))
        dd = ImageDraw.Draw(img)
        x, basis = 2 + rand, asc + rand + 2
        kw = dict(fill=farbe(c), stroke_width=rand, stroke_fill=farbe(self.s['ink']) if rand else None)
        for i, t in enumerate(teile):
            dd.text((x, basis), t, font=f, anchor='ls', **kw)
            x += f.getlength(t)
            if i < len(teile) - 1:
                dd.text((x + f.size * 0.03, basis - f.size * 0.36), '2', font=klein, anchor='ls', **kw)
                x += klein.getlength('2') + f.size * 0.06
        return img.crop(img.getbbox() or (0, 0, 1, 1))

    def text(self, ebene, s, xy, g, c, prog, anker='l', titel=False, art=None, formel=False):
        if prog <= 0:
            return
        art = art or self.s['ein']
        pfad = self.s['schrift_t'] if titel else self.s['schrift_m']
        if formel and self.s.get('schrift_f'):           # Bangers: „=“ sieht aus wie „:“, Formeln deshalb in Inter
            pfad, g = self.s['schrift_f'], g * 0.87
        if titel and self.s.get('titelfarbe') and c == self.s['ink']:
            c = self.s['titelfarbe']
        if art == 'tippen':
            n = max(0, min(len(s), int(round(len(s) * prog * 1.0001))))
            voll = self.textbild(s, pfad, g, c, titel)
            if n == 0:
                return
            img = self.textbild(s[:n], pfad, g, c, titel)
            vw = voll.width
        else:
            img = self.textbild(s, pfad, g, c, titel)
            vw = img.width
        k = self.k
        x, y = xy[0] * k, xy[1] * k
        if anker == 'm':
            x -= vw / 2
        alpha, skala, dx = 1.0, 1.0, 0.0
        if art == 'pop':
            skala, alpha = 0.3 + 0.7 * zurueck(prog), glatt(prog * 2)
        elif art == 'gleiten':
            dx, alpha = (1 - glatt(prog)) * 60 * k, glatt(prog)
        elif art == 'schreiben':
            breite = int(img.width * klemm(prog))
            if breite <= 0:
                return
            img = img.crop((0, 0, breite, img.height))
        elif art == 'blenden':
            alpha = glatt(prog)
        if skala != 1.0:
            nw, nh = max(1, int(img.width * skala)), max(1, int(img.height * skala))
            x += (img.width - nw) / 2
            y += (img.height - nh) / 2
            img = img.resize((nw, nh), Image.BILINEAR)
        if alpha < 1:
            img = img.copy()
            img.putalpha(img.getchannel('A').point(lambda v: int(v * alpha)))
        ebene.alpha_composite(img, (int(x + dx), int(y)))


# ---------- Bausteine der Szene ----------
def rechteck_pts(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def transform(pts, cx, cy, winkel, mx, my):
    """Punkte um (cx, cy) drehen und nach (mx, my) verschieben."""
    c, s = math.cos(winkel), math.sin(winkel)
    return [(mx + (x - cx) * c - (y - cy) * s, my + (x - cx) * s + (y - cy) * c) for x, y in pts]


def gitter(lw_x, lw_y, w, h):
    """Innere Gitterlinien eines Rechtecks aus w × h Einheiten, als Segmente in lokalen Koordinaten."""
    seg = [[(i * U, 0), (i * U, h * U)] for i in range(1, w)]
    seg += [[(0, j * U), (w * U, j * U)] for j in range(1, h)]
    return seg


def knall(d, lw, cx, cy, r, prog, s):
    if prog <= 0:
        return
    sk = zurueck(prog)
    pts = []
    for i in range(24):
        rr = r * sk * (1.0 if i % 2 == 0 else 0.62)
        a = i * math.pi / 12
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.6))
    lw.flaeche(d, pts, '#ffffff', 1.0)
    lw.linie(d, pts + [pts[0]], s['ink'], 6)


def bild(lw, t):
    s = lw.s
    k = lw.k
    ebene = Image.new('RGBA', (lw.w, lw.h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ebene, 'RGBA')
    ink, f1, f2, hi = s['ink'], s['f1'], s['f2'], s['hi']
    dick = s['lw']

    # Titel
    lw.text(ebene, '13 · 17 = ?', (640, 52), 68, ink, p(t, 0.2, 1.2), anker='m', titel=True, formel=True)

    # Restfläche 15 × 13 (bleibt liegen)
    rest = rechteck_pts(X0, Y0, 15 * U, 13 * U)
    p_rand = p(t, 1.4, 1.8)
    p_fuell = glatt(p(t, 2.8, 0.8))
    lw.flaeche(d, rest, f1, p_fuell, seed=1, t=t)

    # Streifen 2 × 13: zuerst rechts, ab 5 s gedreht und oben angelegt
    pb = glatt(p(t, 5.0, 2.6))
    cx0, cy0 = X0 + 16 * U, Y0 + 6.5 * U
    cx1, cy1 = X0 + 6.5 * U, Y0 - 1 * U
    hub = math.sin(pb * math.pi) * 90                       # kleiner Bogen beim Verschieben
    mx, my = cx0 + (cx1 - cx0) * pb, cy0 + (cy1 - cy0) * pb - hub
    winkel = -math.pi / 2 * pb
    lokal = rechteck_pts(-U, -6.5 * U, 2 * U, 13 * U)
    streifen = transform(lokal, 0, 0, winkel, mx, my)
    farbe_streifen = f2 if t >= 4.2 else f1
    a_streifen = p_fuell if t < 4.2 else 1.0
    lw.flaeche(d, streifen, farbe_streifen, a_streifen, seed=2, t=t)

    # Gitter (Einheitsquadrate), dünn
    a_gitter = 0.35 * p_fuell
    if a_gitter > 0:
        for seg in gitter(0, 0, 15, 13):
            lw.linie(d, [(X0 + x, Y0 + y) for x, y in seg], ink, max(1, dick * 0.35), alpha=a_gitter, seed=11, t=t)
        for seg in gitter(0, 0, 2, 13):
            seg = [(x - U, y - 6.5 * U) for x, y in seg]
            lw.linie(d, transform(seg, 0, 0, winkel, mx, my), ink, max(1, dick * 0.35), alpha=a_gitter, seed=12, t=t)

    # Umrisse: vor dem Schnitt das ganze Rechteck 17 × 13, danach Rest und Streifen getrennt
    if t < 4.2:
        lw.linie(d, rechteck_pts(X0, Y0, 17 * U, 13 * U) + [(X0, Y0)], ink, dick, anteil=p_rand, seed=3, t=t)
    else:
        lw.linie(d, rest + [rest[0]], ink, dick, seed=3, t=t)
        lw.linie(d, streifen + [streifen[0]], ink, dick, seed=4, t=t)
    # Schnittlinie blinkt kurz auf
    p_schnitt = p(t, 3.8, 0.6)
    if 0 < p_schnitt and t < 5.0:
        lw.linie(d, [(X0 + 15 * U, Y0 - 14), (X0 + 15 * U, Y0 + 13 * U + 14)], hi, dick * 1.2, anteil=p_schnitt,
                 gestrichelt=True)

    # Beschriftung der Seiten: zuerst 17 und 13, nach dem Umlegen 15 und 15
    a_alt = p(t, 2.4, 0.6) * (1 - p(t, 5.0, 0.4))
    a_neu = p(t, 7.8, 0.6)
    gb = 40
    if a_alt > 0:
        lw.text(ebene, '17', (X0 + 8.5 * U, Y0 + 13 * U + 18), gb, ink, a_alt, anker='m', art='blenden')
        lw.text(ebene, '13', (X0 - 62, Y0 + 6.5 * U - 24), gb, ink, a_alt, art='blenden')
        if s.get('massketten'):
            y = Y0 + 13 * U + 10
            lw.linie(d, [(X0, y), (X0 + 17 * U, y)], ink, 1.5, alpha=a_alt)
    if a_neu > 0:
        lw.text(ebene, '15', (X0 + 7.5 * U, Y0 + 13 * U + 18), gb, ink, a_neu, anker='m', art='blenden')
        lw.text(ebene, '15', (X0 - 62, Y0 + 5.5 * U - 24), gb, ink, a_neu, art='blenden')
        if s.get('massketten'):
            y = Y0 + 13 * U + 10
            lw.linie(d, [(X0, y), (X0 + 15 * U, y)], ink, 1.5, alpha=a_neu)
            x = X0 - 14
            lw.linie(d, [(x, Y0 - 2 * U), (x, Y0 + 13 * U)], ink, 1.5, alpha=a_neu)

    # Fehlende Ecke 2 × 2
    p_ecke = p(t, 8.2, 0.8)
    if p_ecke > 0:
        ecke = rechteck_pts(X0 + 13 * U, Y0 - 2 * U, 2 * U, 2 * U)
        lw.linie(d, ecke + [ecke[0]], hi, dick, anteil=p_ecke, gestrichelt=True)
        lw.text(ebene, '2²', (X0 + 15 * U + 14, Y0 - 2 * U - 6), 40, hi, p(t, 8.6, 0.6))

    # Rechnung rechts
    xr = 600
    lw.text(ebene, 'Mitte 15, Abstand 2', (xr, 196), 40, ink, p(t, 4.2, 1.0))
    lw.text(ebene, '13 · 17 = 15² − 2²', (xr, 280), 54, ink, p(t, 9.4, 1.2), formel=True)
    lw.text(ebene, '= 225 − 4', (xr + 140, 360), 54, ink, p(t, 10.8, 0.9), formel=True)
    if s.get('knall'):
        knall(d, lw, xr + 232, 488, 130, p(t, 11.9, 0.5), s)
    lw.text(ebene, '= 221', (xr + 140, 452), 64, hi, p(t, 12.0, 0.7), titel=True, formel=True)
    lw.text(ebene, '(a − b)(a + b) = a² − b²', (xr, 584), 40, ink, p(t, 12.6, 1.0), formel=True)

    # ----- Zusammensetzen -----
    if s.get('korn'):
        ebene.putalpha(ImageChops.multiply(ebene.getchannel('A'), lw.kornmaske))
    rahmen = lw.grund.copy()
    if s.get('schatten'):
        sch = Image.new('RGBA', ebene.size, (40, 30, 20, 0))
        sch.putalpha(ebene.getchannel('A').point(lambda v: v * 55 // 255).filter(ImageFilter.GaussianBlur(6 * k)))
        rahmen.alpha_composite(sch, (int(5 * k), int(8 * k)))
    if s.get('glanz'):
        klein = ebene.resize((lw.w // 4, lw.h // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(5))
        klein = klein.resize(ebene.size, Image.BILINEAR)
        g = s['glanz']
        klein.putalpha(klein.getchannel('A').point(lambda v: min(255, int(v * g))))
        rahmen.alpha_composite(klein)
    rahmen.alpha_composite(ebene)
    out = rahmen.convert('RGB')
    if lw.k != 1:
        out = out.resize((W, H), Image.NEAREST if s.get('pixel') else Image.LANCZOS)
    return out


def video(stil, aus):
    lw = Leinwand(STILE[stil])
    ziel = os.path.join(aus, f'{stil}.mp4')
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
                           '-pix_fmt', 'yuv420p', '-movflags', '+faststart', ziel], stdin=subprocess.PIPE)
    for i in range(int(DAUER * FPS)):
        ff.stdin.write(bild(lw, i / FPS).tobytes())
    ff.stdin.close()
    ff.wait()
    return ziel


if __name__ == '__main__':
    args = sys.argv[1:]
    aus = args.pop(0)
    os.makedirs(aus, exist_ok=True)
    sek = None
    if '--bild' in args:
        i = args.index('--bild')
        sek = float(args[i + 1])
        del args[i:i + 2]
    for stil in args or list(STILE):
        if sek is not None:
            bild(Leinwand(STILE[stil]), sek).save(os.path.join(aus, f'{stil}_{sek:g}.png'))
        else:
            print(video(stil, aus), flush=True)
