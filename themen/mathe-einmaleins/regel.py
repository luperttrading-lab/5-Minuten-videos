#!/usr/bin/env python3
"""Erklärvideo mit Ton: Kopfrechnen mit zwei Zahlen von 11 bis 19 (dritte Fassung, Nutzerwunsch 04.11.:
„schöner und verständlicher, das ganze Video“).

    (10 + a)(10 + b) = 10·(10 + a + b) + a·b
    Schritt 1  Einer rüber:        16 + 8 = 24   (oder 18 + 6 = 24)
    Schritt 2  mal 10:             240
    Schritt 3  Einer · Einer dazu: + 6 · 8 = 48  →  288
    Sonderfall a + b = 10: 200 + a·b (11·19 = 209 … 15·15 = 225); Vorsicht 15·14: 190 + 20 = 210

Aufbau: Einstieg → Trick (Ziffern wandern) → Warum (Fläche, Streifen nach unten = Schritt 1–3) → Andersherum
(Streifen nach rechts) → Sonderfall (die 200 bleiben, nur die Ecke wächst) → Vorsicht (eine Spalte fehlt) →
Merke + Übung mit Denkpause. Eine Schritte-Karte rechts verbindet Regel und Bild.

Bilder per Code, Ton ElevenLabs (Christian, eleven_v4, Tempo 1,05) mit Zeitmarken: Jede Einblendung hängt an einem
gesprochenen Wort. Ausgabe 1920 × 1080, 30 Bilder/s, in vier Teilen parallel gerendert.

Aufruf: python3 regel.py <ausgabe.mp4> [--nur-ton] [--bild <s>[,<s>…]]
"""
import math, os, subprocess, sys, wave
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', '..', 'werkzeug'))
sys.path.insert(0, HIER)
import render as R                                         # noqa: E402  (ElevenLabs, Dekodieren, Tonaufbereitung)
from motivation import spruch                              # noqa: E402  (wechselnde Motivationssätze)
import animationen as A                                    # noqa: E402
from animationen import (Bild, INTER, INTER_X, breite, einfuegen, farbe, glatt, klemm, mischfarbe, mit_alpha,  # noqa
                         mix, p, zeile, zurueck)

W, H, K = A.W, A.H, A.K                                    # Zeichenkoordinaten 1280 × 720, intern 2× gezeichnet
OUT = (1920, 1080)
FPS = 30
CFG = {'voice_id': 'NBqeXKdZHweef6y0B67V', 'model': 'eleven_v4', 'tempo': 1.05}
CACHE = os.path.join(HIER, 'tts_cache')
PAUSE = 0.7                                                # Stille zwischen Szenen
NACHLAUF = 2.5                                             # Stille nach dem letzten Satz
# Künstliche Atempausen AUS (Messung 04.11.): Christian pausiert an Satzenden schon selbst 200–500 ms; zusätzliche
# 0,35 s machten es abgehackt, und wo er Sätze zusammenzieht, lag die „Stille“ im Verschluss von k/d/b → Absetzer.
ATEMPAUSEN = False
DENKPAUSE = 6.0                                            # nach „Und jetzt du“: Uhr (3 s), dann die Lösung
SPRUCH, BRUECKE = spruch('mathe-einmaleins', 'schluss'), spruch('mathe-einmaleins', 'bruecke')

INK, GRAU, BG, HELL = '#2b2d42', '#6f7380', '#f6f1e7', '#e6dfd2'
CA, CB, CBLAU, CD = '#ff9f1c', '#8338ec', '#3a86ff', '#e63946'   # Einer der 1. Zahl orange, der 2. violett
TEAL, GRUEN = '#0f766e', '#2a9d4a'

SZENEN = [
    dict(id='hook', kicker='Kopfrechnen', text=(
        'Sechzehn mal achtzehn. Im Kopf, in drei Sekunden? Mit diesem Trick schaffst du das für alle Zahlen von elf '
        'bis neunzehn.')),
    dict(id='regel', kicker='Der Trick', text=(
        'Schritt eins: Nimm den Einer der zweiten Zahl, also die Acht, und zähl ihn zur ersten Zahl dazu. Sechzehn '
        'plus acht gibt vierundzwanzig. Schritt zwei: Nimm das mal zehn, also häng eine Null an. Aus vierundzwanzig wird '
        'zweihundertvierzig. Schritt drei: Multipliziere die beiden Einer, sechs mal acht gleich achtundvierzig, und '
        'zähl das dazu. Zweihundertvierzig plus achtundvierzig macht zweihundertachtundachtzig.')),
    dict(id='warum', kicker='Warum klappt das?', text=(
        BRUECKE + ' Warum das klappt, zeigt ein Rechteck aus sechzehn mal achtzehn Kästchen. Wir teilen es in vier Teile: zehn '
        'mal zehn, zehn mal acht, sechs mal zehn und eine kleine Ecke, sechs mal acht. Jetzt drehen wir den Streifen '
        'zehn mal acht und legen ihn unten an. Das ist Schritt eins: Das lange Rechteck ist sechzehn plus acht, also '
        'vierundzwanzig Kästchen hoch. Es ist zehn breit, also mal zehn: zweihundertvierzig. Das ist Schritt zwei. '
        'Übrig bleibt die kleine Ecke, sechs mal acht. Das ist Schritt drei.')),
    dict(id='andersrum', kicker='Andersherum', text=(
        'Du kannst auch umgekehrt den Einer der ersten Zahl zur zweiten zählen: Achtzehn plus sechs ist ebenfalls '
        'vierundzwanzig. Im Bild legst du dann den anderen Streifen, sechs mal zehn, rechts an. Wieder zehn mal '
        'vierundzwanzig. Kein Zufall: Beide Male rechnest du zehn plus sechs plus acht.')),
    dict(id='sonderfall', kicker='Sonderfall', text=(
        'Besonders schnell geht es, wenn die beiden Einer zusammen zehn ergeben. Dann ist das lange Rechteck immer '
        'genau zwanzig breit, also zweihundert. Du rechnest nur noch zweihundert plus Einer mal Einer. Elf mal '
        'neunzehn: zweihundertneun. Zwölf mal achtzehn: zweihundertsechzehn. Und so weiter bis fünfzehn mal '
        'fünfzehn: zweihundertfünfundzwanzig. Die zweihundert bleiben, nur die Ecke wächst.')),
    dict(id='vorsicht', kicker='Vorsicht', text=(
        'Aber Vorsicht: Bei fünfzehn mal vierzehn ergeben die Einer nur neun. Das lange Rechteck ist dann nur '
        'neunzehn breit, also hundertneunzig und nicht zweihundert. Dazu kommt die Ecke, fünf mal vier gleich '
        'zwanzig. Zusammen zweihundertzehn, nicht zweihundertzwanzig.')),
    dict(id='merke', kicker='Merke', pause=DENKPAUSE, text=(   # Nutzerwunsch 04.11.: die langen Sätze, nicht die Kurzformen
        'Merk dir die drei Schritte: Einer zur anderen Zahl, egal, welche. Eine Null anhängen. Beide Einer multiplizieren '
        'und dazuzählen. Und jetzt du: dreizehn mal vierzehn.')),
    dict(id='schluss', kicker='Merke', anhang=True, text=(   # gehört zum Kapitel „Merke“, läuft nach der Lösung
        'Hat es bei dir länger als drei Sekunden gedauert? Ganz normal. Mit ein bisschen Übung schaffst du das auch '
        'so schnell. ' + SPRUCH)),
]


def pause(sc):
    return sc.get('pause', PAUSE)


# ---------------------------------------------------------------- Ton und Zeitplan
def ton_und_zeitplan():
    os.makedirs(CACHE, exist_ok=True)
    stuecke, t = [], 0.0
    for sc in SZENEN:
        mp3, al = R.tts_eleven(sc['text'], CFG, CACHE)
        x = R.decode(mp3, CFG['tempo'])
        thr = 10 ** (-45 / 20) * np.abs(x).max()
        idx = np.where(np.abs(x) > thr)[0]
        a, b = max(idx[0] - int(0.04 * R.SR), 0), idx[-1] + int(0.08 * R.SR)
        x = x[a:b]
        sc['_starts'] = al['character_start_times_seconds']
        sc['_skala'] = len(sc['_starts']) / max(len(sc['text']), 1)
        sc['_lead'] = a / R.SR
        # Atempausen: nach Satzende 0,35 s, nach Doppelpunkt 0,15 s – aber NUR, wo der Ton wirklich still ist.
        # Die Zeitmarken sind nur auf ≈ 40 ms genau, und oft spricht die Stimme ohne Lücke weiter; ein Schnitt dort
        # zerhackt ein Wort (Nutzer 04.11.: „mehrere Sprechabsetzer“). Gemessen: 25 von 41 alten Schnitten lagen im Wort.
        enden, txt, pausen = al['character_end_times_seconds'], sc['text'], []
        schwelle = 20 * np.log10(np.abs(x).max()) - 42      # 42 dB unter der Spitze gilt als Stille
        for i in range(len(txt) - 2):
            if txt[i] in '.?!:' and txt[i + 1] == ' ':
                j = min(int(round(i * sc['_skala'])), len(enden) - 1)
                j2 = min(int(round((i + 2) * sc['_skala'])), len(enden) - 1)
                von = enden[j] / CFG['tempo'] - sc['_lead'] - 0.03
                bis = sc['_starts'][j2] / CFG['tempo'] - sc['_lead'] + 0.06
                tc = stille_stelle(x, von, bis, schwelle)
                if ATEMPAUSEN and tc is not None:
                    pausen.append((tc, 0.15 if txt[i] == ':' else 0.35))
        grenzen = sum(1 for i in range(len(txt) - 2) if txt[i] in '.?!:' and txt[i + 1] == ' ')
        sc['_pausen_bericht'] = f'{len(pausen)} von {grenzen} Satzgrenzen mit Pause'
        stuecke_x, letzt = [], 0
        for tc, d in pausen:
            k = int(tc * R.SR)
            stuecke_x += [x[letzt:k], np.zeros(int(d * R.SR), np.float32)]
            letzt = k
        x = np.concatenate(stuecke_x + [x[letzt:]])
        sc['_pausen'] = pausen
        sc['start'] = t
        sc['dauer'] = len(x) / R.SR
        stuecke += [x, np.zeros(int(pause(sc) * R.SR), np.float32)]
        t += sc['dauer'] + pause(sc)
    stuecke.append(np.zeros(int(NACHLAUF * R.SR), np.float32))
    return np.concatenate(stuecke), t + NACHLAUF


def stille_stelle(x, von, bis, schwelle):
    """Leiseste Stelle (10-ms-Fenster) zwischen `von` und `bis` in Sekunden, falls sie unter `schwelle` dB liegt."""
    a, b = int(max(0.0, von) * R.SR), int(bis * R.SR)
    fenster, schritt = int(0.01 * R.SR), int(0.0025 * R.SR)
    if b - a < fenster:
        return None
    bestes, ort = 0.0, None
    for k in range(a, b - fenster, schritt):
        pegel = 20 * np.log10(np.sqrt(np.mean(x[k:k + fenster] ** 2)) + 1e-9)
        if ort is None or pegel < bestes:
            bestes, ort = pegel, k + fenster // 2
    return ort / R.SR if bestes < schwelle else None


def C(sc, wort, nach=None):
    """Sekunde (relativ zur Szene), in der `wort` gesprochen wird; mit `nach` erst hinter diesem Stichwort suchen."""
    start = sc['text'].find(nach) + len(nach) if nach else 0
    i = sc['text'].find(wort, start)
    if i < 0:
        sys.exit(f'Stichwort fehlt in {sc["id"]}: {wort}')
    j = min(int(round(i * sc['_skala'])), len(sc['_starts']) - 1)
    t = max(0.0, sc['_starts'][j] / CFG['tempo'] - sc['_lead'])
    return t + sum(d for tc, d in sc.get('_pausen', []) if tc <= t)


# ---------------------------------------------------------------- Gestaltung
_grund = None


def grund():
    """Warmes Papier mit feinem Punktraster und weicher Vignette (einmal berechnet)."""
    global _grund
    if _grund is None:
        img = Image.new('RGB', (W * K, H * K), farbe(BG)[:3])
        d = ImageDraw.Draw(img, 'RGBA')
        for y in range(16, H, 32):
            for x in range(16, W, 32):
                d.ellipse([(x - 1.4) * K, (y - 1.4) * K, (x + 1.4) * K, (y + 1.4) * K], fill=(120, 100, 70, 34))
        v = Image.new('L', img.size, 0)
        ImageDraw.Draw(v).ellipse([-0.2 * W * K, -0.3 * H * K, 1.2 * W * K, 1.3 * H * K], fill=255)
        v = v.filter(ImageFilter.GaussianBlur(160))
        _grund = Image.composite(img, Image.new('RGB', img.size, (222, 210, 190)), v)
    return _grund


_karten = {}


def karte(b, x, y, w, h, alpha=1.0, r=22):
    """Weiße Karte mit runden Ecken und weichem Schatten."""
    if alpha <= 0:
        return
    key = (int(w), int(h), r)
    if key not in _karten:
        m = 34
        img = Image.new('RGBA', (int((w + 2 * m) * K), int((h + 2 * m) * K)), (0, 0, 0, 0))
        sch = Image.new('RGBA', img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sch).rounded_rectangle([m * K, (m + 8) * K, (m + w) * K, (m + h + 8) * K], radius=r * K,
                                              fill=(70, 50, 25, 55))
        img.alpha_composite(sch.filter(ImageFilter.GaussianBlur(12 * K)))
        ImageDraw.Draw(img).rounded_rectangle([m * K, m * K, (m + w) * K, (m + h) * K], radius=r * K,
                                              fill=(255, 255, 255, 255))
        _karten[key] = (img, m)
    img, m = _karten[key]
    einfuegen(b.img, mit_alpha(img, alpha), (x - m) * K, (y - m) * K)


def band(b, x0, y0, x1, y1, c, a, r=14):
    if a > 0:
        b.d.rounded_rectangle([x0 * K, y0 * K, x1 * K, y1 * K], radius=r * K, fill=farbe(c, 255 * a))


def ein(t, start, dauer=0.5):
    return glatt(p(t, start, dauer))


def einblenden(b, teile, x, y, g, t, start, pfad=INTER_X, anker='m'):
    a = ein(t, start)
    if a > 0:
        zeile(b, teile, x, y + 16 * (1 - a), g, pfad, alpha=a, anker=anker)


def mitten(teile, x, g, pfad=INTER_X):
    """x-Mitten der Teile einer zentrierten Zeile."""
    ws = [breite(s, pfad, g) for s, _ in teile]
    x0, aus = x - sum(ws) / 2, []
    for w in ws:
        aus.append(x0 + w / 2)
        x0 += w
    return aus


def uhr(b, cx, cy, r, f, alpha=1.0):
    """Drei-Sekunden-Uhr: Ring läuft ab, innen 3 – 2 – 1."""
    if alpha <= 0:
        return
    box = [(cx - r) * K, (cy - r) * K, (cx + r) * K, (cy + r) * K]
    b.d.ellipse(box, outline=farbe(HELL, 255 * alpha), width=int(9 * K))
    if f < 1:
        b.d.arc(box, start=-90 + 360 * klemm(f), end=270, fill=farbe(TEAL, 255 * alpha), width=int(9 * K))
    b.text(str(max(1, 3 - int(klemm(f) * 3))), cx, cy, r * 0.95, INK, INTER_X, alpha=alpha)


def teil(b, w, h, u, col, mx, my, winkel=0.0, skala=1.0, zentrum=(0, 0), gitter=0.3, rand=1.0, alpha=1.0):
    """Rechteck aus w × h Kästchen (Kantenlänge u), Mitte (mx, my), gedreht, optional um `zentrum` skaliert.
    Gitterlinien bleiben sichtbar, damit man die Kästchen zählen kann."""
    c, s = math.cos(math.radians(winkel)), math.sin(math.radians(winkel))
    zx, zy = zentrum

    def f(a, bb):
        px, py = (a - w / 2) * u, (bb - h / 2) * u
        X, Y = mx + px * c + py * s, my - px * s + py * c
        return (zx + (X - zx) * skala, zy + (Y - zy) * skala)

    pts = [f(0, 0), f(w, 0), f(w, h), f(0, h)]
    b.poly(pts, col, alpha=alpha, schatten=5)
    if gitter > 0:
        i = 1
        while i < w - 1e-6:
            b.linie([f(i, 0), f(i, h)], '#ffffff', 1.3, alpha=gitter * alpha)
            i += 1
        j = 1
        while j < h - 1e-6:
            b.linie([f(0, j), f(w, j)], '#ffffff', 1.3, alpha=gitter * alpha)
            j += 1
    if rand > 0:
        b.poly(pts, None, '#ffffff', 3, alpha=rand * alpha)
    return f(w / 2, h / 2)


def beschriftung(b, rechnung, wert, x, y, a, gross=36):
    """Zweizeilig im Teil: oben die Rechnung, darunter der Wert."""
    if a <= 0:
        return
    b.text(rechnung, x, y - 21, 25, '#ffffff', INTER, alpha=klemm(a) * 0.92)
    b.text(wert, x, y + 13, gross, '#ffffff', INTER_X, skala=a, alpha=klemm(a))


def funken(b, t, start, cx, cy, r0=46, r1=150, n=16, dauer=0.8, fy=0.75):
    """Kleiner Funkenkranz um ein Ergebnis (Belohnung, Nutzerwunsch 04.11.: „etwas ansprechender“), 0,8 s."""
    f = p(t, start, dauer)
    if not 0 < f < 1:
        return
    aus = 1 - (1 - f) ** 3                                 # schnell raus, sanft auslaufen
    farben = [GRUEN, CA, CB, CBLAU, CD]
    for k in range(n):
        w = 2 * math.pi * (k + 0.37 * ((k * 7) % 5) / 5) / n
        r = mix(r0, r1 * (0.85 + 0.3 * ((k * 3) % 4) / 3), aus)
        b.kreis(cx + r * math.cos(w), cy + fy * r * math.sin(w), 6.5 - 3.5 * f, farben[k % len(farben)],
                alpha=0.9 * (1 - f) ** 1.4)


def spur(b, ort, t, c, n=7, abstand=0.045, r=5.0, alpha=0.4):
    """Flugspur: Punkte an den Orten der letzten Augenblicke; ort(tt) gibt (x, y) oder None (nicht im Flug)."""
    for k in range(1, n + 1):
        q = ort(t - k * abstand)
        if q is not None:
            b.kreis(q[0], q[1], r * (1 - 0.1 * k), c, alpha=alpha * (1 - k / (n + 1)))


def klammer_waagrecht(b, x0, x1, y, c, a):
    b.linie([(x0, y + 9), (x0, y), (x1, y), (x1, y + 9)], c, 3, alpha=a)


def klammer_senkrecht(b, y0, y1, x, c, a):
    b.linie([(x + 9, y0), (x, y0), (x, y1), (x + 9, y1)], c, 3, alpha=a)


# ---------------------------------------------------------------- Schritte-Karte (verbindet Regel und Bild)
def schritte(b, t, x0, y0, w, zeilen, ergebnis=None, titel='Der Trick', alpha=1.0, dim=False, g_erg=46):
    """zeilen: dict(nr, farbe, titel, teile, t_titel, t_rech, aktiv=(von, bis)); dim = nicht aktive Zeilen blass."""
    h = 66 + len(zeilen) * 104 + (84 if ergebnis else 12)
    karte(b, x0, y0, w, h, alpha)
    if alpha <= 0:
        return
    b.text(titel.upper(), x0 + 30, y0 + 38, 22, GRAU, INTER_X, anker='l', alpha=alpha)
    for i, z in enumerate(zeilen):
        yy = y0 + 66 + i * 104 + 44
        at = ein(t, z.get('t_titel', -1)) * alpha
        if at <= 0:
            continue
        akt = 0.0
        if 'aktiv' in z:
            von, bis = z['aktiv']
            akt = ein(t, von, 0.3) * (1 - ein(t, bis, 0.3))
        band(b, x0 + 14, yy - 48, x0 + w - 14, yy + 48, z.get('farbe', TEAL), 0.13 * akt * alpha)
        stufe = (0.45 + 0.55 * akt) if dim else 1.0
        a = at * stufe
        b.kreis(x0 + 52, yy, 23, z.get('farbe', TEAL), alpha=a)
        b.text(z['nr'], x0 + 52, yy, 25, '#ffffff', INTER_X, alpha=a)
        b.text(z['titel'], x0 + 92, yy - 22, 25, GRAU, INTER, anker='l', alpha=a)
        ar = ein(t, z.get('t_rech', -1)) * a
        if ar > 0:
            zeile(b, z['teile'], x0 + 92, yy + 17, 36, INTER_X, alpha=ar, anker='l')
    if ergebnis:
        teile, te = ergebnis
        a = ein(t, te) * alpha
        if a > 0:
            yy = y0 + h - 46
            b.linie([(x0 + 30, yy - 38), (x0 + w - 30, yy - 38)], HELL, 2, alpha=a)
            zeile(b, teile, x0 + w / 2, yy, g_erg, INTER_X, alpha=a)


def trick_zeilen(t1t, t1r, t2t, t2r, t3t, t3r, aktiv=None):
    aktiv = aktiv or [None, None, None]
    z = [dict(nr='1', farbe=CB, titel='Einer rüber', t_titel=t1t, t_rech=t1r,
              teile=[('16', INK), (' + ', INK), ('8', CB), (' = 24', INK)]),
         dict(nr='2', farbe=TEAL, titel='mal 10', t_titel=t2t, t_rech=t2r,
              teile=[('24 · 10 = ', INK), ('240', TEAL)]),
         dict(nr='3', farbe=CD, titel='Einer · Einer dazu', t_titel=t3t, t_rech=t3r,
              teile=[('+ ', INK), ('6', CA), (' · ', INK), ('8', CB), (' = ', INK), ('48', CD)])]
    for zz, a in zip(z, aktiv):
        if a:
            zz['aktiv'] = a
    return z


ERG288 = [('16 · 18 = ', INK), ('288', GRUEN)]


# ---------------------------------------------------------------- Szenen
def s_hook(b, sc, t):
    q = zurueck(p(t, 0.0, 0.7))
    tu = C(sc, 'drei Sekunden')
    loes = zurueck(p(t, tu + 3.0, 0.6))                    # nach der Uhr: die Lösung
    g = 140 * (0.6 + 0.4 * q)
    tick = max(math.sin(math.pi * p(t, tu + k, 0.3)) for k in range(3))   # „?“ pocht mit den drei Ticks
    zeile(b, [('16', INK), (' · ', INK), ('18', INK), (' = ?', GRAU)], 640, 270, g, INTER_X,
          alpha=klemm(q * 2) * (1 - klemm(loes * 2)), effekte={3: dict(skala=1 + 0.1 * tick)})
    if loes > 0:
        pos = zeile(b, [('16', INK), (' · ', INK), ('18', INK), (' = ', GRAU), ('288', GRUEN)], 640, 270, g, INTER_X,
                    alpha=klemm(loes * 2), effekte={4: dict(skala=0.6 + 0.4 * loes)})
        funken(b, t, tu + 3.05, pos[4], 270, r0=70, r1=190)
    a = ein(t, tu, 0.3)
    uhr(b, 640, 455, 52, (t - tu) / 3.0, alpha=a * (1 - ein(t, tu + 2.85, 0.3)))
    t0 = C(sc, 'elf bis')
    for i, n in enumerate(range(11, 20)):
        q = zurueck(p(t, t0 + i * 0.08, 0.4))
        if q > 0:
            hervor = n in (16, 18)
            if hervor:
                band(b, 640 + (i - 4) * 104 - 40, 590 - 34, 640 + (i - 4) * 104 + 40, 590 + 34, CBLAU, 0.12 * klemm(q))
            b.text(str(n), 640 + (i - 4) * 104, 590, 46, CBLAU if hervor else GRAU, INTER_X, skala=q, alpha=klemm(q))


def s_regel(b, sc, t):
    T = {k: C(sc, w) for k, w in dict(
        s1='Schritt eins', acht='die Acht', flug='zur ersten Zahl', z24='gibt vierundzwanzig', s2='Schritt zwei',
        null='eine Null', z240='wird zweihundert', s3='Schritt drei', f68='sechs mal acht', z48='gleich acht',
        summe='Zweihundertvierzig plus', z288='macht zwei').items()}
    X, YT, G = 400, 175, 112                               # Bühne links: oben die Aufgabe
    YR, GR, Y3, XS = 345, 92, 462, 560                     # Zeile 240, Zeile 48, rechter Rand der Addition
    oben = [('1', INK), ('6', CA), (' · ', INK), ('1', INK), ('8', CB)]
    cs = mitten(oben, X, G)
    p8 = math.sin(math.pi * p(t, T['acht'], 0.6))
    p68 = math.sin(math.pi * p(t, T['f68'], 0.6))
    t_zweite, t_mult = C(sc, 'Einer der zweiten Zahl'), C(sc, 'Multipliziere')
    au = ein(t, t_zweite, 0.4) * (1 - ein(t, T['flug'] + 0.6, 0.4))
    w1 = breite('1', INTER_X, G)
    if au > 0:                                             # „die zweite Zahl“: 18 unterstrichen
        b.linie([(cs[3] - w1 / 2, YT + 64), (cs[4] + w1 / 2, YT + 64)], CB, 6, alpha=au)
    for i, farbe_i, von, bis in ((4, CB, T['acht'], T['flug'] + 0.4), (1, CA, t_mult, T['f68'] + 0.5),
                                 (4, CB, t_mult, T['f68'] + 0.5)):
        ar = ein(t, von, 0.3) * (1 - ein(t, bis, 0.3))
        if ar > 0:                                         # Ring um die gemeinte Ziffer, solange von ihr die Rede ist
            r = 58
            b.d.ellipse([(cs[i] - r) * K, (YT - r) * K, (cs[i] + r) * K, (YT + r) * K], fill=farbe(farbe_i, 30 * ar),
                        outline=farbe(farbe_i, 220 * ar), width=int(4 * K))
    for i, ((s, c), cx) in enumerate(zip(oben, cs)):
        sk = 1 + 0.28 * max(p8 if i == 4 else 0, p68 if i in (1, 4) else 0)
        b.text(s, cx, YT, G, c, INTER_X, skala=sk)
    # Schritt 1: 16 und die 8 wandern nach unten und werden zu 24
    fl = glatt(p(t, T['flug'], 1.1))

    def ort8(tt):                                          # die 8 auf ihrem Bogen (für die Flugspur)
        f = glatt(p(tt, T['flug'], 1.1))
        return None if not 0 < f < 1 else (mix(cs[4], zc[2], f), mix(YT, YR, f) - math.sin(f * math.pi) * 110)
    m24 = glatt(p(t, T['z24'], 0.45))
    ziel = [('16', INK), (' + ', INK), ('8', CB)]
    zc = mitten(ziel, X, GR)
    spur(b, ort8, t, CB)
    if fl > 0 and m24 < 1:
        a = 1 - m24
        b.text('16', mix((cs[0] + cs[1]) / 2, zc[0], fl), mix(YT, YR, fl), mix(G, GR, fl), INK, INTER_X,
               alpha=a * klemm(fl * 3))
        b.text(' + ', zc[1], YR, GR, INK, INTER_X, alpha=a * fl)
        b.text('8', mix(cs[4], zc[2], fl), mix(YT, YR, fl) - math.sin(fl * math.pi) * 110, mix(G, GR, fl), CB, INTER_X,
               alpha=a * klemm(fl * 3))
    # Schritt 2: eine Null fällt an die 24
    sm = glatt(p(t, T['summe'], 0.8))                      # Umbau zur schriftlichen Addition
    w2, w0 = breite('24', INTER_X, GR), breite('0', INTER_X, GR)
    nul = p(t, T['null'], 0.55)
    rueck = glatt(p(t, T['null'], 0.35))
    links = X - (w2 + w0 * rueck) / 2
    dx = (XS - (X + (w2 + w0) / 2)) * sm
    c240 = mischfarbe(INK, TEAL, p(t, T['z240'], 0.4))
    if m24 > 0:
        b.text('24', links + w2 / 2 + dx, YR, GR, c240, INTER_X, skala=0.6 + 0.4 * zurueck(m24), alpha=m24)
    if nul > 0:
        b.text('0', links + w2 + w0 / 2 + dx, YR - 120 * (1 - zurueck(nul)), GR, c240, INTER_X, alpha=klemm(nul * 2))
        b.text('· 10', X + dx, YR - 72, 32, GRAU, INTER_X, alpha=glatt(nul * 2) * (1 - sm))
    # Schritt 3: die Einer 6 und 8 wandern nach unten und werden zu 48
    f3 = glatt(p(t, T['f68'] + 0.05, 0.7))                # landet, bevor „gleich achtundvierzig“ kommt
    m48 = glatt(p(t, T['z48'], 0.45))
    ziel3 = [('6', CA), (' · ', INK), ('8', CB)]
    zc3 = mitten(ziel3, X, GR * 0.9)

    def ort3(tt, i):                                       # 6 (links herum) und 8 (rechts herum)
        f = glatt(p(tt, T['f68'] + 0.05, 0.7))
        if not 0 < f < 1:
            return None
        bg = math.sin(f * math.pi) * 190
        return (mix(cs[1], zc3[0], f) - bg, mix(YT, Y3, f)) if i == 0 else (mix(cs[4], zc3[2], f) + bg, mix(YT, Y3, f))
    spur(b, lambda tt: ort3(tt, 0), t, CA)
    spur(b, lambda tt: ort3(tt, 1), t, CB)
    if f3 > 0 and m48 < 1:
        a = 1 - m48
        bogen = math.sin(f3 * math.pi) * 190                # seitlich um die 240 herum, nicht durch sie hindurch
        b.text('6', mix(cs[1], zc3[0], f3) - bogen, mix(YT, Y3, f3), mix(G, GR * 0.9, f3), CA,
               INTER_X, alpha=a * klemm(f3 * 3))
        b.text(' · ', zc3[1], Y3, GR * 0.9, INK, INTER_X, alpha=a * f3)
        b.text('8', mix(cs[4], zc3[2], f3) + bogen, mix(YT, Y3, f3), mix(G, GR * 0.9, f3), CB,
               INTER_X, alpha=a * klemm(f3 * 3))
    w48, w240 = breite('48', INTER_X, GR), w2 + w0
    if m48 > 0:
        b.text('48', mix(X, XS - w48 / 2, sm), Y3, GR, CD, INTER_X, skala=0.6 + 0.4 * zurueck(m48), alpha=m48)
    if sm > 0:                                             # schriftliche Addition
        b.text('+', XS - w240 - 46, Y3, GR, INK, INTER_X, alpha=sm)
        b.linie([(XS - w240 - 80, 522), (mix(XS - w240 - 80, XS + 12, sm), 522)], INK, 5)
    q = zurueck(p(t, T['z288'], 0.6))
    if q > 0:
        w288 = breite('288', INTER_X, GR)
        b.text('288', XS - w288 / 2, 590, GR, GRUEN, INTER_X, skala=0.5 + 0.5 * q, alpha=klemm(q * 2))
        funken(b, t, T['z288'] + 0.05, XS - w288 / 2, 590, r0=70, r1=190)
        ring = p(t, T['z288'], 0.9)
        if 0 < ring < 1:
            r = 60 + 120 * ring
            b.d.ellipse([(XS - w288 / 2 - r) * K, (590 - r) * K, (XS - w288 / 2 + r) * K, (590 + r) * K],
                        outline=farbe(GRUEN, 160 * (1 - ring)), width=int(5 * K))
    # Karte rechts: die drei Schritte sammeln sich
    zeilen = trick_zeilen(T['s1'], T['z24'], T['s2'], T['z240'], T['s3'], T['z48'],
                          [(T['s1'], T['s2']), (T['s2'], T['s3']), (T['s3'], T['summe'])])
    schritte(b, t, 780, 120, 440, zeilen, (ERG288, T['z288']))


U = 20


def flaechen(b, t, wandert, T, RX, RY):
    """Rechteck 16 × 18 in vier Teilen; `wandert` = 'B' (10 × 8 nach unten → 24 hoch) oder 'C' (6 × 10 nach
    rechts → 24 breit). T: wachsen, teile, A–D (Beschriftung), drehen, k16 (erste Klammer), k24, lang, uebrig."""
    if 'wachsen' in T and p(t, T['wachsen'], KASKADE) < 1:
        return kaskade(b, t, T['wachsen'], RX, RY)
    wachsen = 1.0
    farbig = p(t, T['teile'], 0.6) if 'teile' in T else 1.0
    pd = glatt(p(t, T['drehen'], 1.8))
    lang = glatt(p(t, T['lang'], 0.7))
    zentrum = (RX + 9 * U, RY + 8 * U)
    # „Wir teilen es in vier Teile“: die Teile rücken ein paar Punkte auseinander, vor dem Drehen wieder zusammen
    los = 9 * ein(t, T['teile'], 0.4) * (1 - ein(t, T['drehen'] - 0.6, 0.4)) if 'teile' in T else 0.0
    weg_ = {'A': (-1, -1), 'B': (1, -1), 'C': (-1, 1), 'D': (1, 1)}
    stuecke = {'A': (10, 10, CBLAU, '10 · 10', '100', RX + 5 * U, RY + 5 * U),
               'B': (8, 10, CB, '10 · 8', '80', RX + 14 * U, RY + 5 * U),
               'C': (10, 6, CA, '6 · 10', '60', RX + 5 * U, RY + 13 * U),
               'D': (8, 6, CD, '6 · 8', '48', RX + 14 * U, RY + 13 * U)}
    for name, (w, h, col, rechnung, wert, mx, my) in stuecke.items():
        winkel = 0.0
        mx, my = mx + los * weg_[name][0], my + los * weg_[name][1]
        if name == wandert == 'B':
            mx, my = mix(mx, RX + 5 * U, pd) + math.sin(pd * math.pi) * 80, mix(my, RY + 20 * U, pd)
            winkel = 90 * pd
        elif name == wandert == 'C':
            mx, my = mix(mx, RX + 21 * U, pd), mix(my, RY + 5 * U, pd) + math.sin(pd * math.pi) * 70
            winkel = -90 * pd
        lx, ly = teil(b, w, h, U, mischfarbe('#a9c9e8', col, farbig), mx, my, winkel, wachsen, zentrum,
                      gitter=0.3, rand=farbig)
        if farbig > 0:
            a = zurueck(p(t, T[name], 0.5)) if name in T else 1.0
            if name != 'D':
                a *= 1 - lang
            beschriftung(b, rechnung, wert, lx, ly, a, 32 if name in 'CD' else 36)
    if 'wachsen' in T:                                     # zuerst 18 und 16 an den Kanten
        a1 = ein(t, T['wachsen'] + 0.3) * (1 - ein(t, T['teile'], 0.3))
        zeile(b, [('1', INK), ('8', CB)], RX + 9 * U, RY - 26, 32, INTER_X, alpha=a1)
        zeile(b, [('1', INK), ('6', CA)], RX - 36, RY + 8 * U, 32, INTER_X, alpha=a1)
    a2 = ein(t, T['teile'], 0.4) if 'teile' in T else 1.0
    b.text('10', RX + 5 * U, RY - 26, 30, INK, INTER_X, alpha=a2)
    b.text('10', RX - 34, RY + 5 * U, 30, INK, INTER_X, alpha=a2)
    b.text('6', RX - 34, RY + 13 * U, 30, CA, INTER_X, alpha=a2 * ((1 - pd) if wandert == 'C' else 1))
    b.text('8', RX + 14 * U, RY - 26, 30, CB, INTER_X, alpha=a2 * ((1 - pd) if wandert == 'B' else 1))
    a16, a24 = ein(t, T['k16']), ein(t, T['k24'])
    if wandert == 'B':
        b.text('8', RX - 34, RY + 20 * U, 30, CB, INTER_X, alpha=a2 * pd)
        klammer_senkrecht(b, RY, RY + 16 * U, RX - 64, INK, a16)
        b.text('16', RX - 92, RY + 8 * U, 30, INK, INTER_X, alpha=a16)
        klammer_senkrecht(b, RY, RY + 24 * U, RX - 120, TEAL, a24)
        b.text('24', RX - 150, RY + 12 * U, 32, TEAL, INTER_X, alpha=a24)
        rahmen_, mitte, summe = ((RX - 5, RY - 5, RX + 10 * U + 5, RY + 24 * U + 5), (RX + 5 * U, RY + 12 * U),
                                 '100 + 60 + 80')
    else:
        b.text('6', RX + 21 * U, RY - 26, 30, CA, INTER_X, alpha=a2 * pd)
        klammer_waagrecht(b, RX, RX + 18 * U, RY - 52, INK, a16)
        b.text('18', RX + 9 * U, RY - 72, 30, INK, INTER_X, alpha=a16)
        klammer_waagrecht(b, RX, RX + 24 * U, RY - 96, TEAL, a24)
        b.text('24', RX + 12 * U, RY - 116, 32, TEAL, INTER_X, alpha=a24)
        rahmen_, mitte, summe = ((RX - 5, RY - 5, RX + 24 * U + 5, RY + 10 * U + 5), (RX + 12 * U, RY + 5 * U),
                                 '100 + 80 + 60')
    if lang > 0:                                           # 100, 80, 60 verschmelzen sichtbar zu 240
        x0, y0, x1, y1 = rahmen_
        b.d.rounded_rectangle([x0 * K, y0 * K, x1 * K, y1 * K], radius=6 * K, outline=farbe(TEAL, 255 * lang),
                              width=int(6 * K))
        band(b, mitte[0] - 92, mitte[1] - 56, mitte[0] + 92, mitte[1] + 44, TEAL, 0.85 * lang)
        b.text(summe, mitte[0], mitte[1] - 32, 23, '#ffffff', INTER, alpha=lang)
        b.text('240', mitte[0], mitte[1] + 6, 56, '#ffffff', INTER_X, alpha=lang)
    if 'uebrig' in T:
        puls = math.sin(math.pi * p(t, T['uebrig'], 0.7))
        if puls > 0:
            b.d.rounded_rectangle([(RX + 10 * U - 6) * K, (RY + 10 * U - 6) * K, (RX + 18 * U + 6) * K,
                                   (RY + 16 * U + 6) * K], radius=6 * K, outline=farbe(CD, 255 * puls), width=int(6 * K))


KASKADE = 1.15                                             # s, bis alle 16 × 18 Kästchen da sind


def kaskade(b, t, start, RX, RY):
    """Das Rechteck entsteht Kästchen für Kästchen, als Welle von oben links (statt aus der Mitte zu wachsen)."""
    f = p(t, start, KASKADE)
    b.d.rectangle([(RX + 3) * K, (RY + 5) * K, (RX + 18 * U + 3) * K, (RY + 16 * U + 5) * K],
                  fill=(0, 0, 0, int(38 * glatt(f * 1.2 - 0.2))))   # Schatten kommt mit
    for i in range(18):
        for j in range(16):
            q = zurueck(p(t, start + (i + j) / 32 * 0.8, 0.35))
            if q <= 0:
                continue
            cx, cy, h = RX + (i + 0.5) * U, RY + (j + 0.5) * U, (U - 1.3) * q / 2
            b.d.rectangle([(cx - h) * K, (cy - h) * K, (cx + h) * K, (cy + h) * K], fill=farbe('#a9c9e8'))
    a1 = ein(t, start + 0.3)                               # 18 und 16 an den Kanten wie sonst
    zeile(b, [('1', INK), ('8', CB)], RX + 9 * U, RY - 26, 32, INTER_X, alpha=a1)
    zeile(b, [('1', INK), ('6', CA)], RX - 36, RY + 8 * U, 32, INTER_X, alpha=a1)


def s_warum(b, sc, t):
    T = dict(wachsen=C(sc, 'Rechteck aus'), teile=C(sc, 'vier Teile'), A=C(sc, 'zehn mal', 'vier Teile'),
             B=C(sc, 'zehn mal acht', 'vier Teile'), C=C(sc, 'sechs mal zehn'), D=C(sc, 'sechs mal acht'), drehen=C(sc, 'drehen'),
             k16=C(sc, 'sechzehn plus acht'), k24=C(sc, 'vierundzwanzig Kästchen'), lang=C(sc, 'also mal zehn'),
             uebrig=C(sc, 'Übrig'))
    s1, s2, s3 = C(sc, 'Schritt eins'), C(sc, 'zehn breit'), C(sc, 'Übrig')
    weg = 1 - ein(t, T['wachsen'] - 0.5, 0.4)               # Brücke („Klingt nach Zauberei? Ist es nicht.“) links groß
    if weg > 0:
        teile = BRUECKE.split('? ', 1)
        if len(teile) == 2:
            b.text(teile[0] + '?', 400, 300, 50, INK, INTER_X, alpha=weg * ein(t, 0.0))
            b.text(teile[1], 400, 380, 50, TEAL, INTER_X, alpha=weg * ein(t, C(sc, teile[1])))
        else:
            b.text(BRUECKE, 400, 340, 44, INK, INTER_X, alpha=weg * ein(t, 0.0))
    flaechen(b, t, 'B', T, 250, 132)
    zeilen = trick_zeilen(-1, -1, -1, -1, -1, -1, [(s1, s2), (s2, s3), (s3, sc['dauer'] + 2)])
    schritte(b, t, 780, 120, 440, zeilen, (ERG288, -1), dim=True)


def s_andersrum(b, sc, t):
    T = dict(drehen=C(sc, 'legst du'), k16=C(sc, 'Wieder'), k24=C(sc, 'Wieder') + 0.7, lang=C(sc, 'Wieder') + 0.4)
    flaechen(b, t, 'C', T, 220, 190)
    ah = ein(t, C(sc, 'Einer der ersten'), 0.3) * (1 - ein(t, T['drehen'], 0.3))
    if ah > 0:
        b.d.rounded_rectangle([(220 - 6) * K, (190 + 10 * U - 6) * K, (220 + 10 * U + 6) * K, (190 + 16 * U + 6) * K],
                              radius=6 * K, outline=farbe(CA, 255 * ah), width=int(6 * K))
        b.text('6', 220 - 34, 190 + 13 * U, 30 * (1 + 0.25 * ah), CA, INTER_X)
    t18 = C(sc, 'Achtzehn plus')
    t10 = C(sc, 'rechnest du zehn')                        # nicht 'zehn plus sechs': steckt in 'Acht-zehn plus sechs'
    zeilen = [dict(nr='8', farbe=CB, titel='Einer der 2. Zahl rüber',
                   teile=[('16', INK), (' + ', INK), ('8', CB), (' = 24', INK)]),
              dict(nr='6', farbe=CA, titel='Einer der 1. Zahl rüber', t_titel=t18, t_rech=t18,
                   teile=[('18', INK), (' + ', INK), ('6', CA), (' = 24', INK)], aktiv=(t18, t10))]
    schritte(b, t, 780, 150, 440, zeilen, ([('beides: 10 + ', INK), ('6', CA), (' + ', INK), ('8', CB)], t10),
             titel='Einer rüber: zwei Wege', g_erg=36)


FAELLE = [(11, 19), (12, 18), (13, 17), (14, 16), (15, 15)]


def langes_rechteck(b, a, bb, x0, y0, u, alpha=1.0, gitter=0.3):
    """Form nach Schritt 1 (Streifen rechts angelegt): A, B, C nebeneinander, Ecke D unter B.
    a = Einer der ersten Zahl, bb = Einer der zweiten; Breite 10 + a + bb Spalten."""
    teil(b, 10, 10, u, CBLAU, x0 + 5 * u, y0 + 5 * u, gitter=gitter, alpha=alpha)
    teil(b, bb, 10, u, CB, x0 + (10 + bb / 2) * u, y0 + 5 * u, gitter=gitter, alpha=alpha)
    teil(b, a, 10, u, CA, x0 + (10 + bb + a / 2) * u, y0 + 5 * u, gitter=gitter, alpha=alpha)
    teil(b, bb, a, u, CD, x0 + (10 + bb / 2) * u, y0 + (10 + a / 2) * u, gitter=gitter, alpha=alpha)


def s_sonderfall(b, sc, t):
    th, tz, tn = C(sc, 'zusammen zehn'), C(sc, 'zwanzig breit'), C(sc, 'nur noch')
    zeiten = [C(sc, 'Elf mal'), C(sc, 'Zwölf mal'), C(sc, 'Und so'), C(sc, 'Und so') + 1.0,
              C(sc, 'fünfzehn mal fünfzehn')]
    t200, tecke = C(sc, 'Die zweihundert'), C(sc, 'Ecke wächst')
    a, an = ein(t, 0.15), ein(t, tn)                       # Überschrift sofort: vorher war das Bild 2 s leer
    zeile(b, [('Einer zusammen 10', GRAU)], 640, 112, 38, INTER_X, alpha=a * (1 - an))
    zeile(b, [('Einer zusammen 10:  ', GRAU), ('200 + ', TEAL), ('Einer · Einer', CD)], 640, 112, 38, INTER_X,
          alpha=a * an)
    karte(b, 60, 168, 600, 440, ein(t, zeiten[0] - 0.4))   # Tabelle links
    k = -1
    for i, tk in enumerate(zeiten):
        if t >= tk:
            k = i
    for i, ((x, y), tk) in enumerate(zip(FAELLE, zeiten)):
        aa, bb = x - 10, y - 10
        yy = 222 + i * 82
        ai = ein(t, tk)
        if ai <= 0:
            continue
        if i == k:
            band(b, 76, yy - 36, 644, yy + 36, CD, 0.10 * ai)
        stufe = 1.0 if i == k else 0.55
        zeile(b, [(f'{x} · {y} = ', INK), ('200', TEAL), (' + ', INK), (f'{aa} · {bb}', CD),
                  (f' = {200 + aa * bb}', INK)], 360, yy + 12 * (1 - ai), 38, INTER_X, alpha=ai * stufe)
    ad = ein(t, tz)                                        # rechts: 20 Spalten, die Ecke wächst von 1 × 9 bis 5 × 5
    if ad > 0:
        a_, b_ = 1.0, 9.0
        for (x, y), tk in zip(FAELLE[1:], zeiten[1:]):
            f = glatt(p(t, tk, 0.7))
            a_, b_ = mix(a_, x - 10, f), mix(b_, y - 10, f)
        u, x0, y0 = 15, 730, 230
        langes_rechteck(b, a_, b_, x0, y0, u, alpha=ad)
        p200 = math.sin(math.pi * p(t, t200, 0.8))
        b.d.rounded_rectangle([(x0 - 5) * K, (y0 - 5) * K, (x0 + 20 * u + 5) * K, (y0 + 10 * u + 5) * K], radius=6 * K,
                              outline=farbe(TEAL, 255 * ad), width=int((5 + 4 * p200) * K))
        band(b, x0 + 10 * u - 64, y0 + 5 * u - 30, x0 + 10 * u + 64, y0 + 5 * u + 30, TEAL, 0.85 * ad)
        b.text('200', x0 + 10 * u, y0 + 5 * u, 46, '#ffffff', INTER_X, alpha=ad, skala=1 + 0.12 * p200)
        klammer_waagrecht(b, x0, x0 + 20 * u, y0 - 26, TEAL, ad)
        b.text('20 Spalten', x0 + 10 * u, y0 - 48, 26, TEAL, INTER_X, alpha=ad)
        if k >= 0:
            x, y = FAELLE[k]
            pe = 1 + 0.15 * math.sin(math.pi * p(t, tecke, 0.8))
            b.text(f'{x - 10} · {y - 10} = {(x - 10) * (y - 10)}', x0 + (10 + b_) * u + 18, y0 + (10 + a_ / 2) * u, 32,
                   CD, INTER_X, anker='l', alpha=ad, skala=pe)


def s_vorsicht(b, sc, t):
    t9, t19, t190 = C(sc, 'nur neun'), C(sc, 'neunzehn breit'), C(sc, 'hundertneunzig')
    tnicht, t54 = C(sc, 'und nicht zweihundert'), C(sc, 'fünf mal vier')
    tz, t220 = C(sc, 'Zusammen'), C(sc, 'nicht zweihundertzwanzig')
    zeile(b, [('1', INK), ('5', CA), (' · ', INK), ('1', INK), ('4', CB)], 300, 110, 66, INTER_X, alpha=ein(t, 0))
    zeile(b, [('Einer: ', GRAU), ('5', CA), (' + ', INK), ('4', CB), (' = 9', CD), ('  (nicht 10)', CD)], 300, 172, 30,
          INTER_X, alpha=ein(t, t9))
    u, x0, y0 = 18, 110, 270
    ad = ein(t, t19)
    if ad > 0:
        teil(b, 10, 10, u, CBLAU, x0 + 5 * u, y0 + 5 * u, alpha=ad)
        teil(b, 4, 10, u, CB, x0 + 12 * u, y0 + 5 * u, alpha=ad)
        teil(b, 5, 10, u, CA, x0 + 16.5 * u, y0 + 5 * u, alpha=ad)
        klammer_waagrecht(b, x0, x0 + 19 * u, y0 - 26, TEAL, ad)
        b.text('19 Spalten', x0 + 9.5 * u, y0 - 48, 26, TEAL, INTER_X, alpha=ad)
    an = ein(t, tnicht)
    if an > 0:                                             # die fehlende 20. Spalte, gestrichelt
        xs = x0 + 19 * u
        for k in range(0, 10, 2):
            b.linie([(xs + 3, y0 + k * u + 3), (xs + 3, y0 + (k + 1) * u - 3)], CD, 3, alpha=an)
            b.linie([(xs + u - 3, y0 + k * u + 3), (xs + u - 3, y0 + (k + 1) * u - 3)], CD, 3, alpha=an)
        b.text('fehlt: 10', xs + u + 14, y0 + 5 * u, 28, CD, INTER_X, anker='l', alpha=an)
    a190 = ein(t, t190, 0.6)
    if a190 > 0:
        b.d.rounded_rectangle([(x0 - 5) * K, (y0 - 5) * K, (x0 + 19 * u + 5) * K, (y0 + 10 * u + 5) * K], radius=6 * K,
                              outline=farbe(TEAL, 255 * a190), width=int(6 * K))
        band(b, x0 + 9.5 * u - 60, y0 + 5 * u - 28, x0 + 9.5 * u + 60, y0 + 5 * u + 28, TEAL, 0.85 * a190)
        b.text('190', x0 + 9.5 * u, y0 + 5 * u, 42, '#ffffff', INTER_X, alpha=a190)
    ae = zurueck(p(t, t54, 0.6))
    if ae > 0:
        teil(b, 4, 5, u, CD, x0 + 12 * u, y0 + 12.5 * u, skala=0.4 + 0.6 * klemm(ae),
             zentrum=(x0 + 12 * u, y0 + 12.5 * u), alpha=klemm(ae * 2))
        b.text('20', x0 + 12 * u, y0 + 12.5 * u, 32, '#ffffff', INTER_X, alpha=klemm(ae))
    zeilen = [dict(nr='1', farbe=CB, titel='Einer rüber', t_titel=t19, t_rech=t19,
                   teile=[('15', INK), (' + ', INK), ('4', CB), (' = 19', INK)], aktiv=(t19, t190)),
              dict(nr='2', farbe=TEAL, titel='mal 10', t_titel=t190, t_rech=t190,
                   teile=[('19 · 10 = ', INK), ('190', TEAL)], aktiv=(t190, t54)),
              dict(nr='3', farbe=CD, titel='Einer · Einer dazu', t_titel=t54, t_rech=t54,
                   teile=[('+ ', INK), ('5', CA), (' · ', INK), ('4', CB), (' = ', INK), ('20', CD)], aktiv=(t54, tz))]
    schritte(b, t, 640, 120, 560, zeilen, ([('15 · 14 = ', INK), ('210', GRUEN)], tz), titel='15 · 14',
             alpha=ein(t, t19 - 0.5))                     # keine leere Karte am Anfang
    funken(b, t, tz + 0.1, mitten([('15 · 14 = ', INK), ('210', GRUEN)], 920, 46)[1], 120 + 462 - 46, r0=60, r1=170, fy=0.6)
    a = ein(t, t220)
    if a > 0:                                              # „nicht 220“, die 220 durchgestrichen
        y = 120 + 66 + 3 * 104 + 84 + 40
        b.text('nicht 220', 920, y, 34, CD, INTER_X, alpha=a)
        w = breite('220', INTER_X, 34)
        x1 = 920 + breite('nicht 220', INTER_X, 34) / 2
        ps = glatt(p(t, t220 + 0.3, 0.4))
        if ps > 0:
            b.linie([(x1 - w - 4, y + 8), (mix(x1 - w - 4, x1 + 4, ps), y + 8 - 16 * ps)], CD, 5, alpha=a)


MERKSAETZE = [('1', CB, ['Einer zur anderen Zahl –', 'egal, welche'], 'Einer zur'),
              ('2', TEAL, ['Eine Null anhängen'], 'Eine Null'),
              ('3', CD, ['Beide Einer multiplizieren', 'und dazuzählen'], 'Beide Einer')]


def merkkarte(b, sc, t, x0=80, y0=130, w=590):
    """Merkzettel: genau die Sätze, die gesprochen werden, groß und fett; jeder erscheint, wenn er gesagt wird."""
    tdu = C(sc, 'Und jetzt du')
    zeiten = [C(sc, wort) for *_, wort in MERKSAETZE] + [tdu]
    h = 70 + sum(30 + 44 * len(z) for _, _, z, _ in MERKSAETZE) + 10
    karte(b, x0, y0, w, h)
    b.text('MERKE', x0 + 30, y0 + 38, 22, GRAU, INTER_X, anker='l')
    y = y0 + 70
    for k, (nr, col, zeilen, _) in enumerate(MERKSAETZE):
        hoehe = 30 + 44 * len(zeilen)
        a = ein(t, zeiten[k])
        akt = ein(t, zeiten[k], 0.3) * (1 - ein(t, zeiten[k + 1], 0.3))
        band(b, x0 + 14, y + 2, x0 + w - 14, y + hoehe - 6, col, 0.13 * akt)
        if a > 0:
            dy = 12 * (1 - a)
            b.kreis(x0 + 52, y + 15 + 22 + dy, 23, col, alpha=a)
            b.text(nr, x0 + 52, y + 15 + 22 + dy, 25, '#ffffff', INTER_X, alpha=a)
            for j, z in enumerate(zeilen):
                b.text(z, x0 + 92, y + 15 + 22 + 44 * j + dy, 34, INK, INTER_X, anker='l', alpha=a)
        y += hoehe


def s_merke(b, sc, t):
    tdu = C(sc, 'Und jetzt du')
    merkkarte(b, sc, t)
    a = ein(t, tdu)
    karte(b, 700, 130, 490, 450, a)
    if a <= 0:
        return
    b.text('UND JETZT DU', 730, 168, 22, GRAU, INTER_X, anker='l', alpha=a)
    zeile(b, [('1', INK), ('3', CA), (' · ', INK), ('1', INK), ('4', CB), (' = ?', GRAU)], 945, 245, 64, INTER_X,
          alpha=a)
    te = sc['dauer'] + 0.2                                 # Denkpause mit Uhr, dann die Lösung
    au = ein(t, te, 0.3) * (1 - ein(t, te + 3.0, 0.3))
    uhr(b, 945, 400, 62, (t - te) / 3.0, alpha=au * a)
    loes = [([('13', INK), (' + ', INK), ('4', CB), (' = 17', INK)], te + 3.2),
            ([('17 · 10 = ', INK), ('170', TEAL)], te + 3.8),
            ([('+ ', INK), ('3', CA), (' · ', INK), ('4', CB), (' = ', INK), ('12', CD)], te + 4.4)]
    for i, (teile, tl) in enumerate(loes):
        einblenden(b, teile, 945, 335 + i * 62, 38, t, tl)
    einblenden(b, [('= ', INK), ('182', GRUEN)], 945, 530, 56, t, te + 5.1)
    funken(b, t, te + 5.25, mitten([('= ', INK), ('182', GRUEN)], 945, 56)[1], 530, r0=60, r1=170, fy=0.6)


def s_schluss(b, sc, t):
    """Übung mit Lösung bleibt stehen, darunter der Motivationssatz."""
    m = next(x for x in SZENEN if x['id'] == 'merke')
    s_merke(b, m, m['dauer'] + 30)
    a = ein(t, 0.1)
    if a > 0:
        band(b, 190, 604 + 10 * (1 - a), 1090, 684 + 10 * (1 - a), TEAL, 0.94 * a, r=20)
        w = ein(t, C(sc, 'Mit ein bisschen'), 0.5)        # erst aus-, dann einblenden: nie zwei Texte übereinander
        b.text('Länger als drei Sekunden? Ganz normal.', 640, 644, 30, '#ffffff', INTER_X, alpha=a * (1 - klemm(w * 2)))
        b.text('Mit ein bisschen Übung schaffst du das auch.', 640, 628, 25, '#ffffff', INTER, alpha=a * klemm(w * 2 - 1))
        a2 = ein(t, C(sc, SPRUCH))
        b.text(SPRUCH, 640, 660 + 10 * (1 - a), 32, '#ffffff', INTER_X, alpha=a * a2, skala=0.85 + 0.15 * zurueck(a2))


KLAENGE = {  # Stichwort (oder '#ende' = Ende des Sprechtexts), Klang, Versatz in s – passend zu den Einblendungen
    # Nutzer 04.11.: kein „Plopp“ (fallender Ton, klang wie „Boing“). Glöckchen nur an den vier grünen Ergebnissen,
    # dort zusammen mit den Funken: ein Zeichen für „fertig gerechnet“.
    'hook': [('drei Sekunden', 'tick', 0), ('drei Sekunden', 'tick', 1), ('drei Sekunden', 'tick', 2),
             ('drei Sekunden', 'ding', 3.0)],
    'regel': [('zur ersten Zahl', 'wusch', 0), ('sechs mal acht', 'wusch', 0.05), ('macht zwei', 'ding', 0)],
    'warum': [('drehen', 'wusch', 0)],
    'andersrum': [('legst du', 'wusch', 0)],
    'vorsicht': [('und nicht zweihundert', 'tief', 0), ('Zusammen', 'ding', 0)],
    'merke': [('#ende', 'tick', 0.2), ('#ende', 'tick', 1.2), ('#ende', 'tick', 2.2), ('#ende', 'ding', 5.3)],
}


def klang(art):
    sr = R.SR
    def zeit(d):
        return np.arange(int(d * sr)) / sr
    if art == 'plopp':                                     # weiches „Plopp“: Ton fällt von 700 auf 420 Hz
        t = zeit(0.12)
        f = 420 + 280 * np.exp(-t * 40)
        y = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 32) * np.minimum(1, t * 400) * 0.10
    elif art == 'tick':
        t = zeit(0.05)
        y = np.sin(2 * np.pi * 1600 * t) * np.exp(-t * 120) * 0.05
    elif art == 'ding':                                    # Glöckchen: Grundton mit zwei Obertönen
        t = zeit(1.2)
        y = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in ((1046, 0.06, 3.5), (1568, 0.03, 5),
                                                                              (2093, 0.015, 7)))
        y *= np.minimum(1, t * 300)
    elif art == 'wusch':                                   # Luftzug: gefiltertes Rauschen, schwillt an und ab
        t = zeit(0.5)
        rng = np.random.default_rng(7)
        n = rng.standard_normal(len(t))
        aus, z = np.zeros_like(n), 0.0
        for i, v in enumerate(n):                          # Tiefpass mit steigender Grenzfrequenz
            k = 0.04 + 0.25 * (i / len(n))
            z += k * (v - z)
            aus[i] = z
        y = aus * np.sin(np.pi * t / 0.5) ** 2 * 0.09
    else:                                                  # 'tief': gedämpfter Doppelton für „Achtung“
        t = zeit(0.45)
        y = (np.sin(2 * np.pi * 196 * t) + np.sin(2 * np.pi * 207 * t)) * np.exp(-t * 6) * np.minimum(1, t * 200) * 0.05
    return y.astype(np.float32)


# ---------------------------------------------------------------- Ton: Knackser und Zischeln (Nutzer 04.11.: „Knistern“)
# Gemessen: Die Sprachausgabe liefert vereinzelte Klicks in Sprechpausen (≈ 20 in 2:50, z. B. bei 1,8 s, 3,8 s, 5,7 s),
# nach der Anhebung auf −16 LUFS hörbar. Gedämpft werden nur kurze Hochton-Spitzen mit Stille davor, die sofort wieder
# abklingen; Konsonanten (t, k, p gehen in Behauchung über) bleiben. Dazu ein sanfter Tiefpass bei 12 kHz.
def _hochpass(x, fc, sr):
    n = 1 << int(np.ceil(np.log2(len(x) + 1)))
    F = np.fft.rfft(x, n)
    F[np.fft.rfftfreq(n, 1 / sr) < fc] = 0
    return np.fft.irfft(F, n)[:len(x)]


def entknacksen(x, sr, bericht=None):
    """Einzelne Knackser (Klicks der Sprachausgabe) dämpfen, Konsonanten bleiben.
    Knackser = Hochton-Spitze (> 5 kHz) in 2-ms-Fenstern, die
      • mindestens 6× über dem gleitenden Median (50 ms) liegt,
      • vorher leise ist (−28 … −3 ms: Gesamtpegel unter −42 dBFS) und
      • sofort wieder abklingt (+4 … +20 ms: Hochton unter einem Viertel der Spitze) –
    ein t/k/p-Knall dagegen geht in Behauchung oder Vokal über und bleibt unberührt.
    Gedämpft wird das Fenster ±2 ms um −20 dB mit 1-ms-Rampen."""
    w = int(0.002 * sr)
    n = len(x) // w
    h = _hochpass(x, 5000, sr)
    eh = np.sqrt((h[:n * w].reshape(n, w) ** 2).mean(1)) + 1e-9
    ev = np.sqrt((x[:n * w].reshape(n, w) ** 2).mean(1)) + 1e-9
    k = 25
    med = np.median(np.lib.stride_tricks.sliding_window_view(np.pad(eh, (k // 2, k // 2), mode='edge'), k), axis=1)
    kand = np.where((eh > 6 * med) & (eh > 10 ** (-58 / 20)))[0]
    g = np.ones(len(x))
    rampe = int(0.001 * sr)
    treffer = []
    for i in kand:
        if i < 15 or i + 11 > n:
            continue
        vorher = np.sqrt((ev[i - 14:i - 1] ** 2).mean())
        nachher = eh[i + 2:i + 10].max()
        if vorher < 10 ** (-42 / 20) and nachher < eh[i] / 4:
            a, b = max(0, (i - 1) * w), min(len(x), (i + 2) * w)
            seg = np.full(b - a, 0.1)
            r = min(rampe, (b - a) // 2)
            seg[:r] = np.linspace(1, 0.1, r)
            seg[-r:] = np.linspace(0.1, 1, r)
            g[a:b] = np.minimum(g[a:b], seg)
            treffer.append(i * w / sr)
    if bericht is not None:
        bericht.extend(treffer)
    return (x * g).astype(np.float32)


def tiefpass(x, sr, fc=12000, breite=1500):
    """Sanfter Tiefpass (Kosinus-Flanke fc ± breite/2): nimmt Zischeln und Knistern über 12 kHz, die Stimme bleibt."""
    n = 1 << int(np.ceil(np.log2(len(x) + 1)))
    F = np.fft.rfft(x, n)
    f = np.fft.rfftfreq(n, 1 / sr)
    m = np.clip((fc + breite / 2 - f) / breite, 0, 1)
    F *= 0.5 - 0.5 * np.cos(np.pi * m)
    return np.fft.irfft(F, n)[:len(x)].astype(np.float32)


def klangspur(n_samples):
    spur = np.zeros(n_samples, np.float32)
    for sc in SZENEN:
        for wort, art, versatz in KLAENGE.get(sc['id'], []):
            t0 = sc['start'] + (sc['dauer'] if wort == '#ende' else C(sc, wort)) + versatz
            y = klang(art)
            k = int(t0 * R.SR)
            if k < n_samples:
                spur[k:k + len(y)] += y[:n_samples - k]
    return spur


ZEICHNER = {'hook': s_hook, 'regel': s_regel, 'warum': s_warum, 'andersrum': s_andersrum, 'sonderfall': s_sonderfall,
            'vorsicht': s_vorsicht, 'merke': s_merke, 'schluss': s_schluss}


# ---------------------------------------------------------------- Rahmen: Kapitelname und Fortschritt
def kapitel():
    """Kapitel = Szenen, ein Anhang (anhang=True) zählt zum vorigen: [(nummer, start, dauer)]."""
    aus = []
    for s in SZENEN:
        d = s['dauer'] + pause(s)
        if s.get('anhang') and aus:
            n, st, dd = aus[-1]
            aus[-1] = (n, st, dd + d)
        else:
            aus.append((len(aus), s['start'], d))
    return aus


def rahmen(b, i, tl, t):
    sc = SZENEN[i]
    nr = sum(1 for s in SZENEN[:i + 1] if not s.get('anhang')) - 1
    a = 1.0 if sc.get('anhang') else ein(tl, 0, 0.4)
    sp = 1.0 if sc.get('anhang') else zurueck(p(tl, 0.05, 0.45))   # Kapitelnummer springt auf
    dx = 0.0 if sc.get('anhang') else 18 * (1 - glatt(p(tl, 0.1, 0.5)))    # Kapitelname gleitet von rechts herein
    if nr > 0:
        b.kreis(78, 46, 17 * sp, TEAL, alpha=a)
        b.text(str(nr), 78, 46, 21, '#ffffff', INTER_X, alpha=a, skala=max(sp, 0.02))
    b.text(sc['kicker'].upper(), (106 if nr > 0 else 60) + dx, 46, 22, GRAU, INTER_X, anker='l', alpha=a)
    kap = kapitel()
    gesamt = sum(d for _, _, d in kap)
    x, y = 60, 700
    for _, st, d in kap:
        w = (1160 - 6 * (len(kap) - 1)) * d / gesamt
        b.linie([(x, y), (x + w, y)], HELL, 5)
        f = klemm((t - st) / d)
        if f > 0:
            b.linie([(x, y), (x + w * f, y)], TEAL, 5)
        x += w + 6


def szene_bei(t):
    for i, sc in enumerate(SZENEN):
        if t < sc['start'] + sc['dauer'] + pause(sc):
            return i
    return len(SZENEN) - 1


def zeichne(i, tl, t):
    b = Bild(grund())
    ZEICHNER[SZENEN[i]['id']](b, SZENEN[i], tl)
    rahmen(b, i, tl, t)
    return b.img.resize(OUT, Image.LANCZOS)


def bild(t):
    i = szene_bei(t)
    sc = SZENEN[i]
    out = zeichne(i, t - sc['start'], t)
    ende = sc['start'] + sc['dauer'] + pause(sc)
    if i + 1 < len(SZENEN) and t > ende - 0.4:             # weiche Überblendung am Ende der Pause
        out = Image.blend(out, zeichne(i + 1, 0.0, t), glatt((t - (ende - 0.4)) / 0.4))
    return out


def rendere_teil(arg):
    k0, k1, pfad = arg
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s',
                           f'{OUT[0]}x{OUT[1]}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium',
                           '-crf', '19', '-pix_fmt', 'yuv420p', pfad], stdin=subprocess.PIPE)
    for k in range(k0, k1):
        ff.stdin.write(bild(k / FPS).tobytes())
    ff.stdin.close()
    ff.wait()
    return pfad


def main():
    args = sys.argv[1:]
    ziel = os.path.abspath(args[0])
    ton, gesamt = ton_und_zeitplan()
    print(f'Länge {gesamt:.1f} s, Wörter {sum(len(s["text"].split()) for s in SZENEN)}, '
          f'Zeichen {sum(len(s["text"]) for s in SZENEN)}')
    for sc in SZENEN:
        print(f'  {sc["id"]:11s} {sc["start"]:6.1f} s  +{sc["dauer"]:.1f}   {sc["_pausen_bericht"]}')
    if '--bild' in args:
        for s in args[args.index('--bild') + 1].split(','):
            bild(float(s)).resize((1280, 720), Image.LANCZOS).save(ziel.replace('.mp4', f'_{s}.png'))
        return
    wav = ziel.replace('.mp4', '.wav')
    with wave.open(wav, 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(R.SR)
        f.writeframes((np.clip(ton, -1, 1) * 32767).astype(np.int16).tobytes())
    R.aufbereiten(wav)
    with wave.open(wav) as f:                              # Geräusche erst nach der Aufbereitung (sonst greift das Gate)
        stimme = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32) / 32768
    knackser = []
    stimme = tiefpass(entknacksen(stimme, R.SR, knackser), R.SR)
    print(f'Knackser gedämpft: {len(knackser)}, Tiefpass 12 kHz')
    mix_ = np.clip(stimme + klangspur(len(stimme)), -0.97, 0.97)
    with wave.open(wav, 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(R.SR)
        f.writeframes((mix_ * 32767).astype(np.int16).tobytes())
    if '--nur-ton' in args:
        return
    n = int(gesamt * FPS)
    teile = 4
    grenzen = [n * i // teile for i in range(teile + 1)]
    auftraege = [(grenzen[i], grenzen[i + 1], ziel.replace('.mp4', f'_teil{i}.mp4')) for i in range(teile)]
    with Pool(teile) as pool:
        pfade = pool.map(rendere_teil, auftraege)
    liste = ziel.replace('.mp4', '_teile.txt')
    with open(liste, 'w') as f:
        f.writelines(f"file '{q}'\n" for q in pfade)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', liste, '-i', wav, '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', ziel], check=True)
    for q in pfade + [liste]:
        os.remove(q)
    print('fertig:', ziel)


if __name__ == '__main__':
    main()
