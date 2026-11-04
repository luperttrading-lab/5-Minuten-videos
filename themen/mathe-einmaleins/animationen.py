#!/usr/bin/env python3
"""Kopftrick „12 · 18 = 200 + 2 · 8“ in fünf Animationsarten (Nutzerwunsch 04.11.: „ganz unterschiedlich“, nicht nur
anderer Hintergrund). Ohne Ton, je 21 s, alles per Code gezeichnet.

Mathematik: (10 + a)(10 + b) = 100 + 10·(a + b) + a·b. Nur wenn a + b = 10, ergibt das 200 + a·b.
Gegenprobe im Video: 15 · 14 = 210, nicht 200 + 5·4 = 220 (5 + 4 = 9).

Aufruf: python3 animationen.py <ausordner> [art ...]      Standbild: --bild <sekunde>
Arten: flaeche (Flächenmodell, weiche Übergänge), kinetik (kinetische Typografie), handschrift (Stift schreibt,
Kamera folgt), punkte (Partikel fliegen), papier (Papierschnitt, Stop-Motion mit 12 Bildern/s)
"""
import math, os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HIER = os.path.dirname(os.path.abspath(__file__))
SCHRIFTEN = os.path.join(HIER, '..', '..', 'werkzeug', 'schriften')
W, H, FPS, DAUER, K = 1280, 720, 30, 21.0, 2


def fc(name):
    return subprocess.check_output(['fc-match', '-f', '%{file}', name]).decode()


INTER = fc('Inter:bold')
INTER_X = fc('Inter:extrabold')
DISPLAY = fc('Inter Display:black')
KALAM = os.path.join(SCHRIFTEN, 'Kalam-Bold.ttf')


# ---------- Hilfen ----------
def farbe(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), max(0, min(255, int(a))))


def mischfarbe(h1, h2, f):
    a, b = farbe(h1), farbe(h2)
    return '#%02x%02x%02x' % tuple(int(a[i] + (b[i] - a[i]) * klemm(f)) for i in range(3))


def klemm(x):
    return max(0.0, min(1.0, x))


def glatt(x):
    x = klemm(x)
    return x * x * (3 - 2 * x)


def zurueck(x):                                 # easeOutBack: kurz über das Ziel hinaus
    x = klemm(x)
    return 1 + 2.7 * (x - 1) ** 3 + 1.7 * (x - 1) ** 2


def p(t, start, dauer):
    return klemm((t - start) / dauer)


def mix(a, b, f):
    return a + (b - a) * f


_schriften, _sprites = {}, {}


def schrift(pfad, px):
    if (pfad, px) not in _schriften:
        _schriften[(pfad, px)] = ImageFont.truetype(pfad, px)
    return _schriften[(pfad, px)]


def sprite(s, pfad, g, c):
    """Text als RGBA-Bild; Grundlinie immer gleich weit oben, damit Zeilen gleicher Größe sauber fluchten."""
    px = max(4, int(round(g * K)))
    key = (s, pfad, px, c)
    if key not in _sprites:
        f = schrift(pfad, px)
        asc, desc = f.getmetrics()
        img = Image.new('RGBA', (int(f.getlength(s)) + 8, asc + desc + 8), (0, 0, 0, 0))
        ImageDraw.Draw(img).text((4, 4 + asc), s, font=f, fill=farbe(c), anchor='ls')
        _sprites[key] = img
    return _sprites[key]


def breite(s, pfad, g):
    return schrift(pfad, max(4, int(round(g * K)))).getlength(s) / K


def einfuegen(ziel, sp, x, y):
    """alpha_composite mit Beschnitt am Rand (Pillow verweigert negative Ziele)."""
    x, y = int(x), int(y)
    l, o = max(0, -x), max(0, -y)
    r, u = min(sp.width, ziel.width - x), min(sp.height, ziel.height - y)
    if r <= l or u <= o:
        return
    if ziel.mode == 'RGB':                                # Zeichenfläche: echtes Überblenden über die Maske
        teil = sp.crop((l, o, r, u))
        ziel.paste(teil, (x + l, y + o), teil)
        return
    ziel.alpha_composite(sp.crop((l, o, r, u)) if (l or o or r < sp.width or u < sp.height) else sp, (x + l, y + o))


def mit_alpha(sp, a):
    if a >= 1:
        return sp
    sp = sp.copy()
    sp.putalpha(sp.getchannel('A').point(lambda v: int(v * a)))
    return sp


class Bild:
    def __init__(self, grund):
        # RGB, nicht RGBA: ImageDraw blendet halbtransparente Farben nur auf RGB, auf RGBA überschreibt es den Alphakanal
        self.img = grund.convert('RGB') if isinstance(grund, Image.Image) else Image.new('RGB', (W * K, H * K), farbe(grund)[:3])
        self.d = ImageDraw.Draw(self.img, 'RGBA')
        self.marke = None

    @staticmethod
    def P(pts):
        return [(x * K, y * K) for x, y in pts]

    def poly(self, pts, fill=None, outline=None, lw=0, alpha=1.0, schatten=0):
        if alpha <= 0:
            return
        if schatten:
            self.d.polygon(self.P([(x + schatten * 0.6, y + schatten) for x, y in pts]), fill=(0, 0, 0, int(38 * alpha)))
        if fill:
            self.d.polygon(self.P(pts), fill=farbe(fill, 255 * alpha))
        if outline and lw:
            self.d.line(self.P(pts + [pts[0], pts[1]]), fill=farbe(outline, 255 * alpha), width=max(1, int(lw * K)),
                        joint='curve')

    def linie(self, pts, c, lw, alpha=1.0):
        if alpha > 0 and len(pts) > 1:
            self.d.line(self.P(pts), fill=farbe(c, 255 * alpha), width=max(1, int(lw * K)), joint='curve')

    def kreis(self, cx, cy, r, fill=None, alpha=1.0):
        if alpha > 0 and r > 0:
            self.d.ellipse([(cx - r) * K, (cy - r) * K, (cx + r) * K, (cy + r) * K], fill=farbe(fill, 255 * alpha))

    def text(self, s, x, y, g, c, pfad=INTER, anker='m', alpha=1.0, skala=1.0, dreh=0.0):
        """y = Mitte der Zeile; anker m/l/r bezieht sich auf x."""
        if alpha <= 0 or skala <= 0.01:
            return 0
        sp = sprite(s, pfad, g * skala, c)
        w = sp.width
        if dreh:
            sp = sp.rotate(dreh, resample=Image.BICUBIC, expand=True)
        sp = mit_alpha(sp, alpha)
        X = x * K - {'m': sp.width / 2, 'l': (sp.width - w) / 2, 'r': sp.width - (sp.width - w) / 2}[anker]
        einfuegen(self.img, sp, X, y * K - sp.height / 2)
        return w / K

    def fertig(self, zoom=1.0, cx=W / 2, cy=H / 2):
        img = self.img
        if zoom != 1.0:
            w, h = W / zoom, H / zoom
            cx = min(max(cx, w / 2), W - w / 2)
            cy = min(max(cy, h / 2), H - h / 2)
            img = img.crop((int((cx - w / 2) * K), int((cy - h / 2) * K), int((cx + w / 2) * K), int((cy + h / 2) * K)))
        out = img.convert('RGB').resize((W, H), Image.LANCZOS)
        if self.marke and self.marke[2] > 0:                 # Name der Art nach der Kamera, damit er nie angeschnitten wird
            text, c, a = self.marke
            lage = Image.new('RGBA', out.size, (0, 0, 0, 0))
            ImageDraw.Draw(lage).text((28, 18), text, font=schrift(INTER, 20), fill=farbe(c, 255 * a * 0.8))
            out = Image.alpha_composite(out.convert('RGBA'), lage).convert('RGB')
        return out


def rechteck(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def drehen(pts, winkel, cx, cy, mx, my):
    """Um (cx, cy) drehen (Grad, gegen den Uhrzeiger) und den Drehpunkt nach (mx, my) schieben."""
    a = math.radians(winkel)
    c, s = math.cos(a), math.sin(a)
    return [(mx + (x - cx) * c + (y - cy) * s, my - (x - cx) * s + (y - cy) * c) for x, y in pts]


def zeile(b, teile, x, y, g, pfad, alpha=1.0, anker='m', effekte=None):
    """Mehrfarbige Zeile aus (text, farbe)-Teilen; effekte[i] = dict(dy, skala, alpha) je Teil."""
    ws = [breite(s, pfad, g) for s, _ in teile]
    x0 = x - sum(ws) / 2 if anker == 'm' else x
    pos = []
    for i, ((s, c), w) in enumerate(zip(teile, ws)):
        e = (effekte or {}).get(i, {})
        b.text(s, x0 + w / 2, y + e.get('dy', 0), g, c, pfad, alpha=alpha * e.get('alpha', 1), skala=e.get('skala', 1))
        pos.append(x0 + w / 2)
        x0 += w
    return pos


def marke(b, t, text, c):
    """Name der Animationsart oben links, nur in den ersten Sekunden."""
    b.marke = (text, c, glatt(p(t, 0.1, 0.4)) * (1 - glatt(p(t, 3.0, 0.6))))


# ======================================================================
# 1  Flächenmodell, weiche Übergänge
# ======================================================================
def v_flaeche(t):
    INK, A, B_, C_, D_, GANZ = '#2b2d42', '#3a86ff', '#ff9f1c', '#ffbf69', '#e63946', '#8ecae6'
    b = Bild('#f6f1e7')
    marke(b, t, 'Flächenmodell · weiche Übergänge', INK)
    u, RX, RY = 22, 442, 160
    b.text('12 · 18 = ?', 640, 72, 60, INK, INTER_X, skala=0.4 + 0.6 * zurueck(p(t, 0.2, 0.8)), alpha=glatt(p(t, 0.2, 0.4)))

    teile = {  # name: (x, y, w, h) in Einheiten relativ zu RX/RY, Farbe, Ziel (x, y) in px, Drehung, Fläche
        'A': ((0, 0, 10, 10), A, (300, 160), 0, '100'),
        'B': ((10, 0, 8, 10), B_, (560, 160), 0, '80'),
        'C': ((0, 10, 10, 2), C_, None, 90, '20'),
        'D': ((10, 10, 8, 2), D_, (840, 160), 0, '16'),
    }
    explo = {'A': (-14, -14), 'B': (14, -14), 'C': (-14, 14), 'D': (14, 14)}
    wachsen = zurueck(p(t, 1.4, 1.0))
    if t < 4.6:                                            # ganzes Rechteck 18 × 12
        cx, cy = RX + 9 * u, RY + 6 * u
        pts = [(cx + (x - cx) * wachsen, cy + (y - cy) * wachsen) for x, y in rechteck(RX, RY, 18 * u, 12 * u)]
        b.poly(pts, GANZ, alpha=klemm(wachsen * 3), schatten=6)
        for i in range(1, 18):
            b.linie([(RX + i * u, RY), (RX + i * u, RY + 12 * u)], '#ffffff', 1, alpha=0.5 * p(t, 2.2, 0.5))
        for j in range(1, 12):
            b.linie([(RX, RY + j * u), (RX + 18 * u, RY + j * u)], '#ffffff', 1, alpha=0.5 * p(t, 2.2, 0.5))
        a = p(t, 2.3, 0.5) * (1 - p(t, 3.6, 0.4))
        b.text('18', RX + 9 * u, RY - 26, 34, INK, alpha=a)
        b.text('12', RX - 34, RY + 6 * u, 34, INK, alpha=a)
        ps = glatt(p(t, 3.6, 0.8))                          # Schnittlinien wachsen
        b.linie([(RX + 10 * u, RY - 10), (RX + 10 * u, RY - 10 + (12 * u + 20) * ps)], INK, 4, alpha=ps > 0)
        b.linie([(RX - 10, RY + 10 * u), (RX - 10 + (18 * u + 20) * ps, RY + 10 * u)], INK, 4, alpha=ps > 0)
        a2 = p(t, 3.8, 0.4)
        for s, x, y in (('10', RX + 5 * u, RY - 26), ('8', RX + 14 * u, RY - 26), ('10', RX - 34, RY + 5 * u),
                        ('2', RX - 34, RY + 11 * u)):
            b.text(s, x, y, 32, INK, alpha=a2)
    else:
        pe = glatt(p(t, 4.6, 0.6)) * (1 - glatt(p(t, 6.2, 0.6)))
        pz = glatt(p(t, 6.2, 1.4))                           # A, B, D an ihren Platz
        pc = glatt(p(t, 7.2, 1.6))                           # C dreht sich und legt sich an B
        verschmelzen = glatt(p(t, 9.3, 0.7))
        for name, ((x, y, w, h), col, ziel, dreh, flaeche) in teile.items():
            x0, y0 = RX + x * u + explo[name][0] * pe, RY + y * u + explo[name][1] * pe
            col = mischfarbe(GANZ, col, p(t, 4.6, 0.5))
            if name == 'C':
                col = mischfarbe(col, B_, verschmelzen)
                cx0, cy0 = x0 + w * u / 2, y0 + h * u / 2
                cx1, cy1 = 560 + 8 * u + u, 160 + 5 * u
                hub = math.sin(pc * math.pi) * 60
                mx, my = mix(cx0, cx1, pc), mix(cy0, cy1, pc) + hub
                pts = drehen(rechteck(-w * u / 2, -h * u / 2, w * u, h * u), dreh * pc, 0, 0, mx, my)
                lx, ly = mx, my
            else:
                xx, yy = mix(x0, ziel[0], pz), mix(y0, ziel[1], pz)
                pts = rechteck(xx, yy, w * u, h * u)
                lx, ly = xx + w * u / 2, yy + h * u / 2
            b.poly(pts, col, schatten=6)
            if name == 'B':
                b.poly(pts, None, '#ffffff', 2, alpha=0.6 * (1 - verschmelzen))
            a = zurueck(p(t, 5.0 + 0.15 * 'ABCD'.index(name), 0.5))
            if name in 'BC':
                a *= 1 - verschmelzen
            b.text(flaeche, lx, ly, 30 if name in 'CD' else 40, '#ffffff', INTER_X, skala=a, alpha=klemm(a))
        a = zurueck(p(t, 9.8, 0.5))
        b.text('100', 560 + 5 * u, 160 + 5 * u, 40, '#ffffff', INTER_X, skala=a, alpha=klemm(a))
        a = glatt(p(t, 10.2, 0.6))
        b.text('10 × 10', 300 + 5 * u, 405, 26, INK, alpha=a)
        b.text('10 × 10', 560 + 5 * u, 405, 26, INK, alpha=a)
        b.text('2 × 8', 840 + 4 * u, 235, 26, INK, alpha=a)
        a = glatt(p(t, 9.9, 0.6))
        b.text('80 + 20 = 100', 560 + 5 * u, 440, 24, '#8a5a00', alpha=a * (1 - glatt(p(t, 11.0, 0.5))))
    # Rechnung unten
    a = glatt(p(t, 11.2, 0.6))
    b.text('100 + 100 + 16 = 216', 640, 500 + 20 * (1 - a), 46, INK, INTER_X, alpha=a)
    a = glatt(p(t, 12.8, 0.6))
    zeile(b, [('12 · 18 = ', INK), ('200 + 2 · 8', D_)], 640, 560 + 20 * (1 - a), 40, INTER_X, alpha=a)
    a = glatt(p(t, 15.0, 0.6))
    if a > 0:
        b.poly(rechteck(160, 608, 960, 96), '#ffffff', alpha=a, schatten=4)
        b.text('Klappt nur, wenn die Einer zusammen 10 ergeben: 2 + 8 = 10', 640, 636, 26, INK, alpha=a)
        b.text('15 · 14: 5 + 4 = 9, also 210 und nicht 220', 640, 676, 26, D_, alpha=glatt(p(t, 16.8, 0.6)))
    return b.fertig()


# ======================================================================
# 2  Kinetische Typografie: nur Zahlen, Bewegung, Kamera, harte Schnitte
# ======================================================================
def v_kinetik(t):
    WS, Y, R = '#f5f5f5', '#ffd400', '#ff4d4d'
    b = Bild('#0d0d0d')
    marke(b, t, 'Kinetische Typografie · harte Schnitte', '#9a9a9a')
    zoom, cx, cy = 1.0, 640, 360
    F = DISPLAY
    if t < 4.6:
        a = glatt(p(t, 0, 0.3)) * (1 - glatt(p(t, 1.6, 0.4)))
        b.text('12 · 18', 640, 360 - 60 * p(t, 1.6, 0.4), 170, WS, F, skala=1.8 - 0.8 * zurueck(p(t, 0, 0.6)), alpha=a)
        teile = [('(10 + ', WS), ('2', WS), (') · (10 + ', WS), ('8', WS), (')', WS)]
        gelb = glatt(p(t, 3.0, 0.3))
        teile[1] = ('2', mischfarbe(WS, Y, gelb))
        teile[3] = ('8', mischfarbe(WS, Y, gelb))
        eff = {}
        for i in range(5):
            q = glatt(p(t, 1.9 + i * 0.08, 0.5))
            eff[i] = dict(dy=80 * (1 - q), alpha=q)
        pop = 1 + 0.35 * math.sin(math.pi * p(t, 3.0, 0.35))
        eff[1]['skala'] = eff[3]['skala'] = pop
        zeile(b, teile, 640, 330, 92, F, effekte=eff)
        q = zurueck(p(t, 3.6, 0.6))
        b.text('2 + 8 = 10', 640, mix(-80, 480, q), 80, Y, F, alpha=klemm(q * 2))
        if t > 4.2:                                          # Zoom in die 10, dann harter Schnitt
            zoom, cx, cy = 1 + 4 * glatt(p(t, 4.2, 0.4)) ** 2, 830, 480
    elif t < 8.6:
        zeilen = [('10 · 10 = ', '100', 230), ('10 · 2 = ', '20', 360), ('10 · 8 = ', '80', 490)]
        flug = glatt(p(t, 7.0, 0.8))
        for i, (l, r, y) in enumerate(zeilen):
            q = glatt(p(t, 4.7 + i * 0.5, 0.6))
            x = 640 + 700 * (1 - q)
            dreh = 10 * (1 - q)
            wl, wr = breite(l, F, 80), breite(r, F, 80)
            x0 = x - (wl + wr) / 2
            a_l = 1 - flug if i else 1
            b.text(l, x0 + wl / 2, y, 80, WS, F, alpha=klemm(q * 2) * a_l, dreh=dreh)
            if i == 0:
                b.text(r, x0 + wl + wr / 2, y, 80, WS, F, alpha=klemm(q * 2), dreh=dreh)
            elif flug < 1:                                   # 20 und 80 fliegen zusammen
                zx, zy = 940, 425
                b.text(r, mix(x0 + wl + wr / 2, zx, flug), mix(y, zy, flug), 80, Y, F, alpha=klemm(q * 2), dreh=dreh)
        q = zurueck(p(t, 7.8, 0.4))
        b.text('100', 940, 425, 110, Y, F, skala=q, alpha=klemm(q))
        blitz = 1 - p(t, 7.8, 0.2)
        if 0 < blitz < 1:
            b.poly(rechteck(0, 0, W, H), '#ffffff', alpha=0.3 * blitz)
    elif t < 9.9:
        q = glatt(p(t, 8.6, 0.8))
        b.text('100', mix(360, 640, q), 360, 150, WS, F, alpha=1 - p(t, 9.3, 0.1))
        b.text('+', 640, 360, 150, WS, F, alpha=1 - q)
        b.text('100', mix(920, 640, q), 360, 150, Y, F, alpha=1 - p(t, 9.3, 0.1))
        s = zurueck(p(t, 9.35, 0.4))
        b.text('200', 640, 360, 220, WS, F, skala=s, alpha=klemm(s))
        if t > 9.35:
            r = random.Random(int(t * FPS))
            stark = 18 * (1 - p(t, 9.35, 0.5))
            cx, cy = 640 + r.uniform(-stark, stark), 360 + r.uniform(-stark, stark)
            zoom = 1.04
    elif t < 15.5:
        q = glatt(p(t, 9.9, 0.6))
        z = glatt(p(t, 12.6, 1.4))                           # Kamera zieht zurück
        zoom = mix(1.25, 1.0, z)
        b.text('200', mix(640, 470, q), mix(360, 330, q), mix(220, 130, q), WS, F)
        q2 = glatt(p(t, 10.3, 0.5))
        morph = glatt(p(t, 11.2, 0.4))
        b.text('+ 2 · 8', 625 + 300 * (1 - q2), 330, 130 * 0.75, WS, F, anker='l', alpha=q2 * (1 - morph))
        b.text('+ 16', 625, 330, 130 * 0.75, Y, F, anker='l', alpha=morph)
        q3 = zurueck(p(t, 11.8, 0.6))
        b.text('= 216', 640, mix(800, 500, q3), 150, Y, F, alpha=klemm(q3 * 2))
        a = glatt(p(t, 13.2, 0.6))
        b.text('12 · 18', 640, 150, 80, '#9a9a9a', F, alpha=a)
    elif t < 17.6:
        woerter = [('Nur', WS), ('wenn', WS), ('2 + 8', Y), ('= 10', Y)]
        i = min(3, int((t - 15.5) / 0.52))
        q = p(t, 15.5 + i * 0.52, 0.25)
        b.text(woerter[i][0], 640, 360, 180, woerter[i][1], F, skala=1.4 - 0.4 * glatt(q), alpha=glatt(q * 2))
    else:
        b.text('15 · 14', 640, 210, 120, WS, F, alpha=glatt(p(t, 17.6, 0.2)))
        b.text('5 + 4 = 9', 640, 350, 80, R, F, alpha=glatt(p(t, 18.0, 0.3)))
        q = zurueck(p(t, 18.6, 0.5))
        b.text('= 210', 500, 510, 120, WS, F, skala=q, alpha=klemm(q))
        a = glatt(p(t, 19.0, 0.3))
        w = b.text('220', 900, 510, 120, R, F, alpha=a)
        ps = glatt(p(t, 19.3, 0.4))
        if ps > 0:
            b.linie([(900 - w / 2 - 10, 530), (900 - w / 2 - 10 + (w + 20) * ps, 490)], R, 10)
    return b.fertig(zoom, cx, cy)


# ======================================================================
# 3  Handschrift: Stift schreibt Zeile für Zeile, Kamera folgt dem Stift
# ======================================================================
BLAU, ROT = '#1e3a8a', '#d62828'
HS_ZEILEN = [  # text, start, zeichen/s, farbe, größe, einrücken (an „=“ ausrichten)
    ('12 · 18 = (10 + 2) · (10 + 8)', 0.4, 13, BLAU, 46, False),
    ('= 10·10 + 10·8 + 2·10 + 2·8', 3.1, 13, BLAU, 46, True),
    ('= 100 + 10·(8 + 2) + 2·8', 6.0, 13, BLAU, 46, True),
    ('= 100 + 100 + 16', 9.8, 13, BLAU, 46, True),
    ('= 216', 11.6, 10, BLAU, 46, True),
    ('Klappt nur, wenn die Einer zusammen 10 ergeben!', 13.2, 17, ROT, 36, False),
    ('15 · 14 = 100 + 10·9 + 20 = 210', 16.2, 15, BLAU, 40, False),
    ('und nicht 200 + 5·4 = 220', 18.6, 16, ROT, 34, False),
]
HS_X0, HS_Y0, HS_DY = 170, 120, 70


def hs_layout():
    x_gleich = HS_X0 + breite('12 · 18 ', KALAM, 46)
    aus = []
    for i, (s, start, cps, c, g, ein) in enumerate(HS_ZEILEN):
        x = x_gleich if ein else HS_X0
        y = HS_Y0 + i * HS_DY + (12 if i >= 5 else 0)
        dauer = len(s) / cps
        aus.append(dict(s=s, start=start, ende=start + dauer, c=c, g=g, x=x, y=y, w=breite(s, KALAM, g)))
    return aus


HS = None


def hs_stift(t):
    """Position der Stiftspitze und ob gerade geschrieben wird."""
    zs = HS
    for i, z in enumerate(zs):
        if z['start'] <= t <= z['ende']:
            f = (t - z['start']) / (z['ende'] - z['start'])
            return z['x'] + z['w'] * f, z['y'] + 14, True
        if t < z['start']:
            vorher = zs[i - 1] if i else None
            if vorher is None:
                return z['x'] - 40, z['y'] + 60, False
            px, py = vorher['x'] + vorher['w'], vorher['y'] + 14
            f = glatt(p(t, vorher['ende'], max(0.01, z['start'] - vorher['ende'])))
            return mix(px, z['x'], f), mix(py, z['y'] + 14, f), False
    z = zs[-1]
    return z['x'] + z['w'] + 60 * glatt(p(t, z['ende'], 0.8)), z['y'] + 14 + 300 * glatt(p(t, z['ende'] + 0.3, 0.8)), False


def hs_grund():
    img = Image.new('RGBA', (W * K, H * K), farbe('#fffef8'))
    d = ImageDraw.Draw(img, 'RGBA')
    for i in range(12):
        y = (HS_Y0 + 32 + i * HS_DY - 70) * K
        d.line([(0, y), (W * K, y)], fill=(120, 160, 220, 70), width=K)
    d.line([(130 * K, 0), (130 * K, H * K)], fill=(220, 60, 60, 120), width=2 * K)
    return img


HS_GRUND = None


def ellipse_pfad(cx, cy, rx, ry, anteil, start=-2.6):
    n = 60
    return [(cx + rx * math.cos(start + 2.2 * math.pi * i / n * anteil),
             cy + ry * math.sin(start + 2.2 * math.pi * i / n * anteil) + 2 * math.sin(i * 0.5)) for i in range(n + 1)]


def v_handschrift(t):
    global HS, HS_GRUND
    if HS is None:
        HS, HS_GRUND = hs_layout(), hs_grund()
    b = Bild(HS_GRUND)
    marke(b, t, 'Handschrift · Kamera folgt dem Stift', '#6b7280')
    for z in HS:
        f = p(t, z['start'], z['ende'] - z['start'])
        if f <= 0:
            continue
        sp = sprite(z['s'], KALAM, z['g'], z['c'])
        bw = int(4 * K + z['w'] * K * f)
        teil = sp.crop((0, 0, min(sp.width, bw), sp.height))
        einfuegen(b.img, teil, z['x'] * K - 4 * K, z['y'] * K - sp.height / 2)
    # Kreis um (8 + 2), rote Notiz mit Pfeil
    z2 = HS[2]
    vor = breite('= 100 + 10·', KALAM, 46)
    w8 = breite('(8 + 2)', KALAM, 46)
    kx, ky = z2['x'] + vor + w8 / 2, z2['y'] + 2
    pk = glatt(p(t, 8.1, 0.7))
    if pk > 0:
        b.linie(ellipse_pfad(kx, ky, w8 / 2 + 16, 30, pk), ROT, 3.5)
    nx0 = z2['x'] + z2['w'] + 50                         # Notiz rechts neben der Zeile
    a = p(t, 8.7, 0.6)
    if a > 0:
        sp = sprite('8 + 2 = 10 !', KALAM, 38, ROT)
        einfuegen(b.img, sp.crop((0, 0, int(sp.width * a), sp.height)), nx0 * K, ky * K - sp.height / 2)
    pa = glatt(p(t, 9.2, 0.5))                           # Pfeil unter der Zeile von der Notiz zum Kreis
    if pa > 0:
        pfad = [(nx0 + 20, ky + 24), (nx0 - 5, ky + 44), (kx + 30, ky + 46), (kx + 6, ky + 33)]
        teil = [pfad[0]]
        laengen = [math.hypot(q[0] - r[0], q[1] - r[1]) for r, q in zip(pfad, pfad[1:])]
        rest = sum(laengen) * pa
        for (r, q), l in zip(zip(pfad, pfad[1:]), laengen):
            f = min(1, rest / l)
            teil.append((mix(r[0], q[0], f), mix(r[1], q[1], f)))
            rest -= l
            if rest <= 0:
                break
        b.linie(teil, ROT, 3)
        if pa >= 1:
            b.linie([(kx + 4, ky + 50), (kx + 6, ky + 33), (kx + 22, ky + 40)], ROT, 3)
    # Ergebnis doppelt unterstreichen
    z4 = HS[4]
    for k, start in ((0, 12.3), (1, 12.6)):
        pu = glatt(p(t, start, 0.3))
        if pu > 0:
            y = z4['y'] + 28 + k * 9
            b.linie([(z4['x'] + 40, y), (z4['x'] + 40 + (z4['w'] - 30) * pu, y - 3)], ROT, 3.5)
    # Stift
    sx, sy, schreibt = hs_stift(t)
    if schreibt:
        sy += math.sin(t * 38) * 3
    lang, br = 150, 18
    winkel = math.radians(-38)
    ux, uy = math.cos(winkel), math.sin(winkel)        # entlang des Stifts (nach rechts oben)
    nx, ny = -uy, ux
    spitze = (sx, sy)
    holz = (sx + ux * 26, sy + uy * 26)
    ende = (sx + ux * lang, sy + uy * lang)
    def quer(pt, f):
        return [(pt[0] + nx * br / 2 * f, pt[1] + ny * br / 2 * f), (pt[0] - nx * br / 2 * f, pt[1] - ny * br / 2 * f)]
    h1, h2 = quer(holz, 1)
    e1, e2 = quer(ende, 1)
    g1, g2 = quer((sx + ux * (lang + 16), sy + uy * (lang + 16)), 1)
    b.poly([(sx + 8, sy + 10), (holz[0] + 10, holz[1] + 12), (ende[0] + 10, ende[1] + 12)], None)
    b.poly([h1, e1, e2, h2], '#f4c430')
    b.poly([e1, g1, g2, e2], '#f4a6b8')
    b.poly([spitze, h1, h2], '#e8c9a0')
    b.poly([spitze, quer((sx + ux * 9, sy + uy * 9), 1)[0], quer((sx + ux * 9, sy + uy * 9), 1)[1]], '#333333')
    # Kamera: folgt dem Stift (geglättet), am Ende Gesamtansicht
    xs = [hs_stift(t - d)[0] for d in (0, 0.2, 0.4, 0.6, 0.8)]
    ys = [hs_stift(t - d)[1] for d in (0, 0.2, 0.4, 0.6, 0.8)]
    cx, cy = sum(xs) / 5 - 120, sum(ys) / 5 + 40
    rein = glatt(p(t, 0.0, 1.5)) * (1 - glatt(p(t, 19.6, 1.2)))
    zoom = 1 + 0.4 * rein
    return b.fertig(zoom, mix(640, cx, rein), mix(360, cy, rein))


# ======================================================================
# 4  Punkte: 216 Partikel, die auftauchen, sich färben und umgruppieren
# ======================================================================
def v_punkte(t):
    NEU, A, B_, C_, D_, WS = '#cfd8ff', '#4cc9f0', '#f8961e', '#f9c74f', '#f72585', '#f1f5ff'
    b = Bild('#0b1020')
    marke(b, t, 'Punkte · Partikel fliegen', '#8090c0')
    s, X0, Y0 = 24, 436, 150
    b.text('12 · 18 = ?', 640, 70, 56, WS, INTER_X, alpha=glatt(p(t, 1.4, 0.5)))
    a = glatt(p(t, 2.0, 0.4)) * (1 - glatt(p(t, 3.4, 0.4)))
    b.text('Wie viele Punkte?', 640, 470, 34, '#8090c0', alpha=a)

    def ziel(i, j):
        if j < 10 and i < 10:
            return 'A', 260 + i * s, Y0 + j * s, 0
        if j < 10:
            return 'B', 560 + (i - 10) * s, Y0 + j * s, 0
        if i < 10:
            return 'C', 560 + (8 + (j - 10)) * s, Y0 + i * s, i * 2 + (j - 10)
        return 'D', 860 + (i - 10) * s, Y0 + (j - 10) * s, 0

    farben = {'A': A, 'B': B_, 'C': C_, 'D': D_}

    def ort(i, j, tt):
        g, zx, zy, n = ziel(i, j)
        sx, sy = X0 + i * s, Y0 + j * s
        if g == 'C':
            q = glatt(p(tt, 7.0 + n * 0.06, 0.9))
            return mix(sx, zx, q), mix(sy, zy, q) - math.sin(q * math.pi) * 80, g
        q = glatt(p(tt, 6.0, 1.0))
        return mix(sx, zx, q), mix(sy, zy, q), g

    for j in range(12):
        for i in range(18):
            auf = zurueck(p(t, 0.3 + (i + j) * 0.04, 0.35))
            if auf <= 0:
                continue
            x, y, g = ort(i, j, t)
            c = mischfarbe(NEU, farben[g], p(t, 3.6 + (i + j) * 0.03, 0.4))
            if g == 'C':
                c = mischfarbe(c, B_, p(t, 9.3, 0.5))
                for k, a in ((1, 0.35), (2, 0.2), (3, 0.1)):  # Leuchtspur
                    gx, gy, _ = ort(i, j, t - 0.04 * k)
                    if abs(gx - x) + abs(gy - y) > 2:
                        b.kreis(gx, gy, 7 - k, c, alpha=a)
            puls = 1 + 0.35 * math.sin(math.pi * p(t, 12.8, 0.5)) if g == 'D' else 1
            b.kreis(x, y, 12 * auf, c, alpha=0.10)
            b.kreis(x, y, 7 * auf * puls, c)
    a = glatt(p(t, 9.6, 0.6))
    if a > 0:
        for x0, w, h in ((260, 10, 10), (560, 10, 10), (860, 8, 2)):
            b.poly(rechteck(x0 - 16, Y0 - 16, (w - 1) * s + 32, (h - 1) * s + 32), None, '#8090c0', 1.5, alpha=a * 0.7)
        b.text('100', 260 + 4.5 * s, Y0 + 9 * s + 48, 36, A, INTER_X, alpha=a)
        b.text('100', 560 + 4.5 * s, Y0 + 9 * s + 48, 36, B_, INTER_X, alpha=a)
        b.text('16', 860 + 3.5 * s, Y0 + 1 * s + 48, 36, D_, INTER_X, alpha=a)
        b.text('80 + 20', 560 + 4.5 * s, Y0 + 9 * s + 84, 24, '#8090c0', alpha=a)
    a = glatt(p(t, 11.0, 0.6))
    b.text('100 + 100 + 16 = 216', 640, 520 + 16 * (1 - a), 46, WS, INTER_X, alpha=a)
    a = glatt(p(t, 12.6, 0.6))
    zeile(b, [('12 · 18 = ', WS), ('200 + 2 · 8', D_)], 640, 580 + 16 * (1 - a), 38, INTER_X, alpha=a)
    b.text('Klappt nur, wenn die Einer zusammen 10 ergeben (2 + 8).', 640, 640, 26, '#a8b4e0', alpha=glatt(p(t, 15.0, 0.6)))
    b.text('15 · 14: 5 + 4 = 9, also 210 und nicht 220', 640, 680, 26, D_, alpha=glatt(p(t, 16.8, 0.6)))
    return b.fertig()


# ======================================================================
# 5  Papierschnitt, Stop-Motion (12 Bilder/s, leichtes Zittern)
# ======================================================================
_papier = {}


def papier(w, h, col, seed, text=None, g=30, tc='#1a1a1a', pfad=INTER_X):
    """Papierstück mit unregelmäßigem Rand, Körnung und Schatten, als Sprite (Mitte = Mitte des Papiers)."""
    key = (w, h, col, seed, text, g)
    if key in _papier:
        return _papier[key]
    rnd = random.Random(seed)
    m = 24
    img = Image.new('RGBA', (int((w + 2 * m) * K), int((h + 2 * m) * K)), (0, 0, 0, 0))
    pts = []
    for (x1, y1), (x2, y2) in zip(rechteck(m, m, w, h), rechteck(m, m, w, h)[1:] + [(m, m)]):
        n = max(2, int(math.hypot(x2 - x1, y2 - y1) / 14))
        for i in range(n):
            f = i / n
            pts.append(((x1 + (x2 - x1) * f + rnd.uniform(-1.2, 1.2)) * K, (y1 + (y2 - y1) * f + rnd.uniform(-1.2, 1.2)) * K))
    sch = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sch).polygon([(x + 5 * K, y + 7 * K) for x, y in pts], fill=(40, 25, 10, 110))
    img.alpha_composite(sch.filter(ImageFilter.GaussianBlur(5 * K)))
    blatt = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(blatt).polygon(pts, fill=farbe(col))
    korn = Image.frombytes('L', img.size, bytes(rnd.getrandbits(8) for _ in range(img.size[0] * img.size[1])))
    hell = Image.new('RGBA', img.size, (255, 255, 255, 0))
    hell.putalpha(korn.point(lambda v: v // 14))
    blatt.alpha_composite(Image.composite(hell, Image.new('RGBA', img.size, (0, 0, 0, 0)), blatt.getchannel('A')))
    img.alpha_composite(blatt)
    if text:
        sp = sprite(text, pfad, g, tc)
        einfuegen(img, sp, img.width / 2 - sp.width / 2, img.height / 2 - sp.height / 2)
    _papier[key] = img
    return img


def legen(b, sp, cx, cy, dreh, skala=1.0):
    if skala != 1.0:
        sp = sp.resize((max(1, int(sp.width * skala)), max(1, int(sp.height * skala))), Image.BILINEAR)
    if dreh:
        sp = sp.rotate(dreh, resample=Image.BICUBIC, expand=True)
    einfuegen(b.img, sp, cx * K - sp.width / 2, cy * K - sp.height / 2)


_karton = None


def karton():
    global _karton
    if _karton is None:
        img = Image.new('RGBA', (W * K, H * K), farbe('#c9a46c'))
        rnd = Image.frombytes('L', img.size, os.urandom(img.size[0] * img.size[1])).filter(ImageFilter.GaussianBlur(1.2))
        dunkel = Image.new('RGBA', img.size, (90, 60, 25, 0))
        dunkel.putalpha(rnd.point(lambda v: max(0, v - 110) // 3))
        img.alpha_composite(dunkel)
        vign = Image.new('L', img.size, 0)
        ImageDraw.Draw(vign).ellipse([-W * K * 0.2, -H * K * 0.3, W * K * 1.2, H * K * 1.3], fill=255)
        vign = vign.filter(ImageFilter.GaussianBlur(120))
        schw = Image.new('RGBA', img.size, (50, 30, 10, 0))
        schw.putalpha(vign.point(lambda v: (255 - v) // 3))
        img.alpha_composite(schw)
        _karton = img
    return _karton


def v_papier(t):
    bild_nr = int(t * 12)
    t = bild_nr / 12                                          # Stop-Motion: Zeit springt in 1/12 s
    rnd = random.Random(bild_nr)
    b = Bild(karton())
    marke(b, t, 'Papierschnitt · Stop-Motion mit 12 Bildern pro Sekunde', '#4a3418')

    def wackel(seed):
        r = random.Random(bild_nr * 31 + seed)
        return r.uniform(-1.6, 1.6), r.uniform(-1.6, 1.6), r.uniform(-0.7, 0.7)

    def etikett(s, x, y, start, g=30, seed=0, dreh=0.0, col='#fbfaf5', tc='#1a1a1a'):
        if t < start:
            return
        q = p(t, start, 0.17)                                 # zwei Bilder lang zu groß: „fällt“ aufs Papier
        sp = papier(breite(s, INTER_X, g) + 30, g * 1.5, col, 500 + seed, s, g, tc)
        dx, dy, dd = wackel(seed + 99)
        legen(b, sp, x + dx, y + dy, dreh + dd, 1.15 - 0.15 * q)

    etikett('12 · 18 = ?', 640, 70, 0.3, 40, 1, -1.5)
    u, RX, RY = 22, 442, 170
    rein = glatt(p(t, 1.4, 1.5))
    TEAL, SENF, ROTP, ORANGE = '#2a9d8f', '#e9c46a', '#e76f51', '#f4a261'
    if t < 4.8:
        cx = mix(-300, RX + 9 * u, rein)
        dx, dy, dd = wackel(1)
        legen(b, papier(18 * u, 12 * u, ORANGE, 2), cx + dx, RY + 6 * u + dy, dd + 6 * (1 - rein))
        if t > 3.0:
            ps = glatt(p(t, 3.2, 1.0))                        # Bleistift-Schnittlinien
            for x0, y0, x1, y1 in ((RX + 10 * u, RY - 8, RX + 10 * u, RY + 12 * u + 8),
                                   (RX - 8, RY + 10 * u, RX + 18 * u + 8, RY + 10 * u)):
                n = 20
                for k in range(0, int(n * ps), 2):
                    b.linie([(mix(x0, x1, k / n), mix(y0, y1, k / n)), (mix(x0, x1, (k + 1) / n), mix(y0, y1, (k + 1) / n))],
                            '#3a3a3a', 3)
            etikett('10', RX + 5 * u, RY - 30, 3.3, 24, 3)
            etikett('8', RX + 14 * u, RY - 30, 3.4, 24, 4)
            etikett('10', RX - 40, RY + 5 * u, 3.5, 24, 5)
            etikett('2', RX - 40, RY + 11 * u, 3.6, 24, 6)
    else:
        pe = glatt(p(t, 4.8, 0.6)) * (1 - glatt(p(t, 6.0, 0.6)))
        pz = glatt(p(t, 6.0, 1.4))
        pc = glatt(p(t, 7.4, 1.6))
        teile = {'A': (0, 0, 10, 10, TEAL, (300, 170), (-16, -16)), 'B': (10, 0, 8, 10, SENF, (560, 170), (16, -16)),
                 'D': (10, 10, 8, 2, ROTP, (840, 170), (16, 16))}
        for k, (name, (x, y, w, h, col, z, ex)) in enumerate(teile.items()):
            x0, y0 = RX + x * u + ex[0] * pe, RY + y * u + ex[1] * pe
            xx, yy = mix(x0, z[0], pz), mix(y0, z[1], pz)
            dx, dy, dd = wackel(10 + k)
            legen(b, papier(w * u, h * u, col, 20 + k), xx + w * u / 2 + dx, yy + h * u / 2 + dy, dd)
        # C: 10 × 2, dreht sich um 90° und legt sich rechts an B
        cx0, cy0 = RX + 5 * u - 16 * pe, RY + 11 * u + 16 * pe
        cx1, cy1 = 560 + 8 * u + u, 170 + 5 * u
        dx, dy, dd = wackel(14)
        legen(b, papier(10 * u, 2 * u, SENF, 24), mix(cx0, cx1, pc) + dx, mix(cy0, cy1, pc) + math.sin(pc * math.pi) * 70 + dy,
              90 * pc + dd)
        if t < 9.4:
            etikett('80', 560 + 4 * u, 170 + 5 * u, 5.6, 28, 7)
        etikett('100', 300 + 5 * u, 170 + 5 * u, 9.6, 34, 8, 2)
        etikett('100', 560 + 5 * u, 170 + 5 * u, 9.8, 34, 9, -2)
        etikett('16', 840 + 4 * u, 170 + u, 10.0, 24, 10, 3)
    etikett('100 + 100 + 16 = 216', 470, 500, 11.2, 36, 11, -1)
    etikett('12 · 18 = 200 + 2 · 8', 470, 580, 12.8, 36, 12, 1.5, col='#fff1e6')
    if t >= 15.0:                                             # gelber Haftzettel
        q = p(t, 15.0, 0.17)
        zettel = papier(380, 210, '#fff275', 77)
        zettel = zettel.copy()
        for i, (s, c, g) in enumerate((('Klappt nur, wenn die', '#1a1a1a', 30), ('Einer zusammen 10 sind!', '#1a1a1a', 30),
                                      ('15 · 14 = 210, nicht 220', '#c0392b', 28))):
            if t >= 15.0 + (1.8 if i == 2 else 0):
                sp = sprite(s, KALAM, g, c)
                einfuegen(zettel, sp, zettel.width / 2 - sp.width / 2, (24 + 50 + i * 56) * K - sp.height / 2)
        dx, dy, dd = wackel(40)
        legen(b, zettel, 1030 + dx, 560 + dy, 4 + dd, 1.12 - 0.12 * q)
    return b.fertig()


ARTEN = {'flaeche': v_flaeche, 'kinetik': v_kinetik, 'handschrift': v_handschrift, 'punkte': v_punkte, 'papier': v_papier}


def video(art, aus):
    ziel = os.path.join(aus, f'{art}.mp4')
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
                           '-pix_fmt', 'yuv420p', '-movflags', '+faststart', ziel], stdin=subprocess.PIPE)
    letztes, cache = None, None
    for i in range(int(DAUER * FPS)):
        t = i / FPS
        if art == 'papier':                                   # nur 12 neue Bilder pro Sekunde
            nr = int(t * 12)
            if nr != letztes:
                cache, letztes = ARTEN[art](t).tobytes(), nr
            ff.stdin.write(cache)
        else:
            ff.stdin.write(ARTEN[art](t).tobytes())
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
        sek = [float(x) for x in args[i + 1].split(',')]
        del args[i:i + 2]
    for art in args or list(ARTEN):
        if sek is not None:
            for s in sek:
                ARTEN[art](s).save(os.path.join(aus, f'{art}_{s:g}.png'))
        else:
            print(video(art, aus), flush=True)
