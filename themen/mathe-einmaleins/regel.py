#!/usr/bin/env python3
"""Erklärvideo mit Ton: die allgemeine Regel fürs Multiplizieren zweier Zahlen von 11 bis 19.

    (10 + a)(10 + b) = 10·(10 + a + b) + a·b
    16 · 18:  16 + 8 = 24 (oder 18 + 6 = 24), mal 10 = 240, plus 6 · 8 = 48  →  288
    Sonderfall a + b = 10:  200 + a·b   (11·19 = 209 … 15·15 = 225)

Bilder per Code (Flächenmodell, Stil A aus animationen.py), Ton ElevenLabs (Christian, eleven_v4, Tempo 1,05) mit
Zeitmarken: Jede Einblendung hängt an einem gesprochenen Wort (`cue`), nicht an einer festen Sekunde.

Aufruf: python3 regel.py <ausgabe.mp4> [--nur-ton] [--bild <s>[,<s>…]]
"""
import json, math, os, subprocess, sys, wave
import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', '..', 'werkzeug'))
sys.path.insert(0, HIER)
import render as R                                         # noqa: E402  (ElevenLabs, Dekodieren, Tonaufbereitung)
from animationen import (Bild, INTER, INTER_X, W, H, breite, glatt, klemm, mischfarbe, mix, p, rechteck,  # noqa: E402
                         drehen, zeile, zurueck)

FPS = 30
CFG = {'voice_id': 'NBqeXKdZHweef6y0B67V', 'model': 'eleven_v4', 'tempo': 1.05}
CACHE = os.path.join(HIER, 'tts_cache')
PAUSE = 0.7                                                # Stille zwischen Szenen
NACHLAUF = 4.0                                             # nach dem letzten Satz: Auflösung der Übungsaufgabe

INK, GRAU, BG = '#2b2d42', '#7b7f8c', '#f6f1e7'
CA, CB, CBLAU, CD, GRUEN = '#ff9f1c', '#8338ec', '#3a86ff', '#e63946', '#2a9d4a'   # a = 6 orange, b = 8 violett

SZENEN = [
    dict(id='hook', kicker='Kopfrechnen', text=(
        'Sechzehn mal achtzehn, im Kopf, in drei Sekunden? Mit einem einfachen Trick klappt das für alle Zahlen '
        'von elf bis neunzehn.')),
    dict(id='regel', kicker='Die Regel', text=(
        'So geht es: Zur ersten Zahl addierst du den Einer der zweiten. Sechzehn plus acht macht vierundzwanzig. '
        'Das nimmst du mal zehn, also zweihundertvierzig. Dazu kommt das Produkt der beiden Einer: sechs mal acht '
        'gleich achtundvierzig. Zusammen zweihundertachtundachtzig.')),
    dict(id='andersrum', kicker='Andersherum', text=(
        'Es geht auch andersherum: Achtzehn plus sechs ist ebenfalls vierundzwanzig. Das ist kein Zufall, denn beide '
        'Male rechnest du zehn plus sechs plus acht.')),
    dict(id='warum', kicker='Warum stimmt das?', text=(
        'Warum das stimmt, zeigt ein Rechteck aus sechzehn mal achtzehn Kästchen. Es zerfällt in vier Teile: zehn mal '
        'zehn, zehn mal acht, sechs mal zehn und eine kleine Ecke, sechs mal acht. Jetzt drehen wir den Streifen '
        'sechs mal zehn und legen ihn rechts an. So entsteht ein langes Rechteck, zehn hoch und vierundzwanzig breit, '
        'also zweihundertvierzig Kästchen. Übrig bleibt die Ecke mit achtundvierzig.')),
    dict(id='sonderfall', kicker='Sonderfall', text=(
        'Ein Sonderfall: Ergeben die beiden Einer zusammen zehn, ist das lange Rechteck genau zwanzig breit. Dann '
        'rechnest du einfach zweihundert plus das Produkt der Einer. Elf mal neunzehn: zweihundertneun. Zwölf mal '
        'achtzehn: zweihundertsechzehn. Und so weiter, bis fünfzehn mal fünfzehn: zweihundertfünfundzwanzig. '
        'Je näher die beiden Zahlen beieinanderliegen, desto größer wird die Ecke.')),
    dict(id='vorsicht', kicker='Vorsicht', text=(
        'Aber Vorsicht: Die Abkürzung mit zweihundert gilt nur, wenn die Einer zusammen zehn ergeben. Fünfzehn mal '
        'vierzehn ist nicht zweihundertzwanzig. Mit der allgemeinen Regel: fünfzehn plus vier gleich neunzehn, mal '
        'zehn hundertneunzig, plus fünf mal vier, also zweihundertzehn. Probier es gleich selbst: dreizehn mal '
        'vierzehn.')),
]


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
        sc['start'] = t
        sc['dauer'] = len(x) / R.SR
        stuecke += [x, np.zeros(int(PAUSE * R.SR), np.float32)]
        t += sc['dauer'] + PAUSE
    stuecke.append(np.zeros(int(NACHLAUF * R.SR), np.float32))
    return np.concatenate(stuecke), t + NACHLAUF


def cue(sc, wort, nach=0):
    """Sekunde (relativ zur Szene), in der `wort` gesprochen wird; `nach` = ab welcher Textstelle gesucht wird."""
    i = sc['text'].find(wort, nach)
    if i < 0:
        sys.exit(f'Stichwort fehlt in {sc["id"]}: {wort}')
    j = min(int(round(i * sc['_skala'])), len(sc['_starts']) - 1)
    return max(0.0, sc['_starts'][j] / CFG['tempo'] - sc['_lead'])


def C(sc, wort, nach=None):
    """Zeitmarke mit Gedächtnis: gleiche Wörter später im Text über `nach` (ein vorheriges Stichwort) finden."""
    start = sc['text'].find(nach) + len(nach) if nach else 0
    return cue(sc, wort, start)


# ---------------------------------------------------------------- Bausteine
def kicker(b, sc, t):
    a = glatt(p(t, 0, 0.4))
    b.text(sc['kicker'].upper(), 60, 48, 22, GRAU, INTER_X, anker='l', alpha=a)


def ein(t, start, dauer=0.5):
    return glatt(p(t, start, dauer))


def einblenden(b, teile, x, y, g, t, start, pfad=INTER_X, anker='m'):
    a = ein(t, start)
    if a > 0:
        zeile(b, teile, x, y + 18 * (1 - a), g, pfad, alpha=a, anker=anker)


def zahl16_18(b, x, y, g, alpha=1.0):
    zeile(b, [('1', INK), ('6', CA), (' · ', INK), ('1', INK), ('8', CB)], x, y, g, INTER_X, alpha=alpha)


# ---------------------------------------------------------------- Szenen
def s_hook(b, sc, t):
    q = zurueck(p(t, 0.0, 0.7))
    b.text('16 · 18 = ?', 640, 300, 120, INK, INTER_X, skala=0.5 + 0.5 * q, alpha=klemm(q * 2))
    t0 = C(sc, 'elf')
    for i, n in enumerate(range(11, 20)):
        q = zurueck(p(t, t0 + i * 0.09, 0.4))
        b.text(str(n), 640 + (i - 4) * 100, 470, 46, CBLAU if n in (16, 18) else GRAU, INTER_X, skala=q, alpha=klemm(q))


def s_regel(b, sc, t):
    zahl16_18(b, 640, 120, 64)
    y0, dy, g = 250, 82, 56
    einblenden(b, [('16', INK), (' + ', INK), ('8', CB), (' = 24', INK)], 640, y0, g, t, C(sc, 'Sechzehn plus'))
    einblenden(b, [('24 · 10 = ', INK), ('240', CBLAU)], 640, y0 + dy, g, t, C(sc, 'mal zehn'))
    einblenden(b, [('6', CA), (' · ', INK), ('8', CB), (' = ', INK), ('48', CD)], 640, y0 + 2 * dy, g, t,
               C(sc, 'sechs mal acht'))
    einblenden(b, [('240 + 48 = ', INK), ('288', GRUEN)], 640, y0 + 3 * dy, g + 8, t, C(sc, 'Zusammen'))
    a = ein(t, C(sc, 'Zur ersten'))
    if a > 0:
        b.poly(rechteck(150, 610, 980, 70), '#ffffff', alpha=a, schatten=4)
        b.text('Erste Zahl + Einer der zweiten, mal 10, plus Einer · Einer', 640, 645, 28, INK, alpha=a)


def s_andersrum(b, sc, t):
    zahl16_18(b, 640, 120, 64)
    einblenden(b, [('16', INK), (' + ', INK), ('8', CB), (' = 24', INK)], 380, 290, 56, t, 0.0)
    einblenden(b, [('18', INK), (' + ', INK), ('6', CA), (' = 24', INK)], 900, 290, 56, t, C(sc, 'Achtzehn plus'))
    t0 = C(sc, 'zehn plus sechs')
    a = ein(t, t0)
    if a > 0:
        for x in (380, 900):                               # zwei Pfeile nach unten in die Mitte
            b.linie([(x, 340), (mix(x, 640, 0.6 * a), 340 + 90 * a)], GRAU, 3, alpha=a)
    einblenden(b, [('10', INK), (' + ', INK), ('6', CA), (' + ', INK), ('8', CB), (' = 24', INK)], 640, 480, 64, t,
               t0 + 0.3)
    einblenden(b, [('Beide Wege: ', GRAU), ('10 + beide Einer', INK)], 640, 580, 32, t, t0 + 1.0, INTER)


U, RX, RY = 20, 160, 150


def s_warum(b, sc, t):
    T = dict(rechteck=C(sc, 'Rechteck aus'), teile=C(sc, 'vier Teile'), A=C(sc, 'zehn mal', 'vier Teile'),
             B=C(sc, 'zehn mal acht'), Cc=C(sc, 'sechs mal zehn'), D=C(sc, 'sechs mal acht'), drehen=C(sc, 'drehen'),
             lang=C(sc, 'langes Rechteck'), breit=C(sc, 'vierundzwanzig breit'), uebrig=C(sc, 'Übrig'))
    wachsen = zurueck(p(t, T['rechteck'], 0.8))
    if wachsen <= 0:
        zahl16_18(b, 640, 360, 90)
        return
    teile = {'A': (0, 0, 10, 10, CBLAU, '100'), 'B': (10, 0, 8, 10, CB, '80'), 'C': (0, 10, 10, 6, CA, '60'),
             'D': (10, 10, 8, 6, CD, '48')}
    farbig = p(t, T['teile'], 0.6)
    pd = glatt(p(t, T['drehen'], 1.8))
    zus = glatt(p(t, T['lang'], 0.6))
    for name, (x, y, w, h, col, fl) in teile.items():
        col = mischfarbe('#a9c9e8', col, farbig)
        if name == 'C':
            cx0, cy0 = RX + 5 * U, RY + 13 * U
            cx1, cy1 = RX + 18 * U + 3 * U, RY + 5 * U
            mx, my = mix(cx0, cx1, pd), mix(cy0, cy1, pd) + math.sin(pd * math.pi) * 50
            pts = drehen(rechteck(-5 * U, -3 * U, 10 * U, 6 * U), -90 * pd, 0, 0, mx, my)
            lx, ly = mx, my
        else:
            cx, cy = RX + 9 * U, RY + 8 * U
            pts = [(cx + (px - cx) * wachsen, cy + (py - cy) * wachsen) for px, py in rechteck(RX + x * U, RY + y * U, w * U, h * U)]
            lx, ly = RX + (x + w / 2) * U, RY + (y + h / 2) * U
        b.poly(pts, col, schatten=5)
        if farbig > 0:
            b.poly(pts, None, '#ffffff', 2, alpha=farbig)
        a = zurueck(p(t, T[name if name != 'C' else 'Cc'], 0.5))
        if name in 'ABC':
            a *= 1 - zus
        b.text(fl, lx, ly, 34, '#ffffff', INTER_X, skala=a, alpha=klemm(a))
    # Kästchengitter, solange das Rechteck ganz ist
    ag = 0.45 * ein(t, T['rechteck'] + 0.4) * (1 - farbig)
    if ag > 0:
        for i in range(1, 18):
            b.linie([(RX + i * U, RY), (RX + i * U, RY + 16 * U)], '#ffffff', 1, alpha=ag)
        for j in range(1, 16):
            b.linie([(RX, RY + j * U), (RX + 18 * U, RY + j * U)], '#ffffff', 1, alpha=ag)
    a1 = ein(t, T['rechteck'] + 0.3) * (1 - ein(t, T['teile'], 0.3))
    b.text('18', RX + 9 * U, RY - 24, 30, INK, INTER_X, alpha=a1)
    b.text('16', RX - 32, RY + 8 * U, 30, INK, INTER_X, alpha=a1)
    a2 = ein(t, T['teile'], 0.4) * (1 - ein(t, T['drehen'], 0.3))
    for s_, x, y in (('10', RX + 5 * U, RY - 24), ('8', RX + 14 * U, RY - 24), ('10', RX - 32, RY + 5 * U),
                     ('6', RX - 32, RY + 13 * U)):
        b.text(s_, x, y, 28, INK, INTER_X, alpha=a2)
    if zus > 0:                                            # langes Rechteck 10 × 24
        b.poly(rechteck(RX - 4, RY - 4, 24 * U + 8, 10 * U + 8), None, GRUEN, 5, alpha=zus)
        b.text('240', RX + 12 * U, RY + 5 * U, 56, '#ffffff', INTER_X, alpha=zus)
        b.text('24', RX + 12 * U, RY - 26, 30, GRUEN, INTER_X, alpha=ein(t, T['breit']))
        b.text('10', RX - 32, RY + 5 * U, 30, GRUEN, INTER_X, alpha=ein(t, T['breit']))
        puls = math.sin(math.pi * p(t, T['uebrig'], 0.6))
        if puls > 0:
            b.poly(rechteck(RX + 10 * U - 4, RY + 10 * U - 4, 8 * U + 8, 6 * U + 8), None, CD, 5, alpha=puls)
    xr = 760
    einblenden(b, [('10 · 24 = ', INK), ('240', GRUEN)], xr, 220, 46, t, T['breit'], anker='l')
    einblenden(b, [('6 · 8 = ', INK), ('48', CD)], xr, 300, 46, t, T['uebrig'], anker='l')
    einblenden(b, [('16 · 18 = ', INK), ('288', GRUEN)], xr, 400, 52, t, T['uebrig'] + 1.2, anker='l')


def s_sonderfall(b, sc, t):
    einblenden(b, [('Einer zusammen 10:  ', GRAU), ('10 · 20 = 200', INK)], 640, 120, 40, t, C(sc, 'zwanzig breit'))
    reihen = [(11, 19, 'Elf mal'), (12, 18, 'Zwölf mal'), (13, 17, 'Und so'), (14, 16, 'Und so'), (15, 15, 'fünfzehn mal fünfzehn')]
    naeher = C(sc, 'Je näher')
    for i, (x, y, w) in enumerate(reihen):
        t0 = C(sc, w) + (0.5 if (x, w) == (14, 'Und so') else 0)
        a, b_ = x - 10, y - 10
        yy = 210 + i * 78
        einblenden(b, [(f'{x} · {y} = 200 + ', INK), (f'{a} · {b_}', CD), (f' = {200 + a * b_}', INK)], 560, yy, 44, t, t0)
        q = zurueck(p(t, t0 + 0.2, 0.5))                     # Ecke a × b als kleines Rechteck, wächst bis 5 × 5
        puls = 1 + 0.12 * math.sin(math.pi * p(t, naeher + i * 0.15, 0.5))
        s_ = 8 * q * puls
        if q > 0:
            b.poly(rechteck(900, yy - b_ * s_ / 2, a * s_ * 1.0, b_ * s_), CD, alpha=klemm(q), schatten=3)
    einblenden(b, [('Je näher beieinander, desto größer die Ecke', GRAU)], 640, 650, 30, t, naeher, INTER)


def s_vorsicht(b, sc, t):
    b.text('15 · 14', 640, 120, 80, INK, INTER_X, alpha=ein(t, 0))
    t1 = C(sc, 'nicht zweihundertzwanzig')
    a = ein(t, t1)
    w = 0
    if a > 0:
        w = breite('200 + 5 · 4 = 220', INTER_X, 44)
        b.text('200 + 5 · 4 = 220', 640, 210, 44, CD, INTER_X, alpha=a)
        ps = glatt(p(t, t1 + 0.4, 0.4))
        if ps > 0:
            b.linie([(640 - w / 2 - 10, 222), (640 - w / 2 - 10 + (w + 20) * ps, 200)], CD, 6)
    einblenden(b, [('15 + 4 = 19', INK)], 640, 310, 50, t, C(sc, 'fünfzehn plus'))
    einblenden(b, [('19 · 10 = 190', INK)], 640, 380, 50, t, C(sc, 'mal zehn', 'neunzehn'))
    einblenden(b, [('190 + 5 · 4 = ', INK), ('210', GRUEN)], 640, 450, 56, t, C(sc, 'plus fünf'))
    t3 = C(sc, 'Probier')
    a = ein(t, t3)
    if a > 0:
        b.poly(rechteck(330, 545, 620, 120), '#ffffff', alpha=a, schatten=4)
        b.text('Probier selbst:  13 · 14 = ?', 640, 580, 36, INK, INTER_X, alpha=a)
        ende = sc['dauer'] + 1.8                           # Auflösung erst nach einer Denkpause
        b.text('13 + 4 = 17,  170 + 3 · 4 = 182', 640, 630, 30, GRUEN, INTER_X, alpha=ein(t, ende, 0.6))


ZEICHNER = {'hook': s_hook, 'regel': s_regel, 'andersrum': s_andersrum, 'warum': s_warum, 'sonderfall': s_sonderfall,
            'vorsicht': s_vorsicht}


def szene_bei(t):
    for i, sc in enumerate(SZENEN):
        ende = sc['start'] + sc['dauer'] + PAUSE
        if t < ende or i == len(SZENEN) - 1:
            return i
    return len(SZENEN) - 1


def bild(t):
    i = szene_bei(t)
    sc = SZENEN[i]
    b = Bild(BG)
    kicker(b, sc, t - sc['start'])
    ZEICHNER[sc['id']](b, sc, t - sc['start'])
    out = b.fertig()
    # weiche Überblendung in den letzten 0,35 s der Pause
    ende = sc['start'] + sc['dauer'] + PAUSE
    if i + 1 < len(SZENEN) and t > ende - 0.35:
        nb = Bild(BG)
        nsc = SZENEN[i + 1]
        kicker(nb, nsc, 0)
        ZEICHNER[nsc['id']](nb, nsc, 0)
        from PIL import Image
        out = Image.blend(out, nb.fertig(), glatt((t - (ende - 0.35)) / 0.35))
    return out


def main():
    args = sys.argv[1:]
    ziel = args[0]
    ton, gesamt = ton_und_zeitplan()
    print(f'Länge {gesamt:.1f} s, Wörter {sum(len(s["text"].split()) for s in SZENEN)}, '
          f'Zeichen {sum(len(s["text"]) for s in SZENEN)}')
    for sc in SZENEN:
        print(f'  {sc["id"]:11s} {sc["start"]:6.1f} s  +{sc["dauer"]:.1f}')
    if '--bild' in args:
        for s in args[args.index('--bild') + 1].split(','):
            bild(float(s)).save(ziel.replace('.mp4', f'_{s}.png'))
        return
    wav = ziel.replace('.mp4', '.wav')
    with wave.open(wav, 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(R.SR)
        f.writeframes((np.clip(ton, -1, 1) * 32767).astype(np.int16).tobytes())
    R.aufbereiten(wav)
    if '--nur-ton' in args:
        return
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-i', wav, '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
                           '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart',
                           ziel], stdin=subprocess.PIPE)
    for k in range(int(gesamt * FPS)):
        ff.stdin.write(bild(k / FPS).tobytes())
    ff.stdin.close()
    ff.wait()
    print('fertig:', ziel)


if __name__ == '__main__':
    main()
