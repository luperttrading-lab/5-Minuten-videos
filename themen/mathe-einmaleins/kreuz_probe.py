#!/usr/bin/env python3
"""Probe (ohne Ton, ≈ 10 s): das Abweichungs-Kreuz für das Kapitel „Andersherum“ (Nutzerwunsch 04.11., Idee aus der
Video-Recherche: tecmath, vedisch „Nikhilam“). Neben jede Zahl kommt ihr Abstand zur 10 (16 → +6, 18 → +8); über Kreuz
addiert ergibt sich auf beiden Diagonalen dieselbe 24 – „andersherum“ in einem einzigen Bild. Danach wie gehabt:
mal 10, Abstände malnehmen, dazu.

    (10 + a)(10 + b) = 10 · (10 + a + b) + a · b,   16 + 8 = 18 + 6 = 10 + 6 + 8 = 24

Aufruf: python3 kreuz_probe.py <ausgabe.mp4> [--bild <s>]
"""
import math, os, subprocess, sys
from multiprocessing import Pool
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import regel as G                                          # noqa: E402  (Stil, Karten, Funken, Farben)
from regel import (CA, CB, CD, GRAU, GRUEN, INK, TEAL, INTER, INTER_X, K, Bild, ein, farbe, glatt, klemm,  # noqa
                   mix, p, zurueck)

FPS, DAUER = 30, 10.5
X16, XA, Y1, Y2, GZ, GA = 230, 520, 250, 410, 120, 96     # Zahlen links, Abstände rechts daneben
T = dict(zahlen=0.3, abstand=1.2, d1=2.2, d2=3.8, mitte=4.9, mal10=5.4, prod=6.6, erg=8.0)


def linie_teil(b, a, z, f, c, lw=7, alpha=1.0):
    """Linie von a nach z, zu Anteil f gezeichnet, mit runden Enden."""
    if f <= 0 or alpha <= 0:
        return
    e = (mix(a[0], z[0], f), mix(a[1], z[1], f))
    b.linie([a, e], c, lw, alpha=alpha)
    for q in (a, e):
        b.kreis(q[0], q[1], lw / 2, c, alpha=alpha)


def bild(t):
    b = Bild(G.grund())
    a = ein(t, 0, 0.4)                                     # Kapitelkopf wie im Video
    b.kreis(78, 46, 17 * zurueck(p(t, 0.05, 0.45)), TEAL, alpha=a)
    b.text('3', 78, 46, 21, '#ffffff', INTER_X, alpha=a)
    b.text('ANDERSHERUM', 106, 46, 22, GRAU, INTER_X, anker='l', alpha=a)

    # Wer gerade dran ist, bleibt kräftig; der Rest tritt zurück
    d1 = ein(t, T['d1'], 0.3) * (1 - ein(t, T['d2'], 0.3))
    d2 = ein(t, T['d2'], 0.3) * (1 - ein(t, T['mitte'], 0.3))
    pr = ein(t, T['prod'], 0.3) * (1 - ein(t, T['erg'], 0.3))
    blass = lambda an: 1 - 0.65 * an                       # noqa: E731
    a16, a18 = blass(max(d2, pr)), blass(max(d1, pr))
    a6, a8 = blass(d1), blass(d2)

    az = ein(t, T['zahlen'])
    b.text('16', X16, Y1 + 14 * (1 - az), GZ, INK, INTER_X, alpha=az * a16)
    b.text('18', X16, Y2 + 14 * (1 - az), GZ, INK, INTER_X, alpha=az * a18)
    for i, (txt, c, y, al) in enumerate((('+6', CA, Y1, a6), ('+8', CB, Y2, a8))):
        q = zurueck(p(t, T['abstand'] + 0.25 * i, 0.45))
        b.text(txt, XA, y, GA, c, INTER_X, skala=max(q, 0.01), alpha=klemm(q * 2) * al)
    b.text('Abstand zur 10', XA, Y2 + 82, 26, GRAU, INTER_X, alpha=ein(t, T['abstand'] + 0.5))

    # Das Kreuz: 16 → +8 und 18 → +6, beide ergeben 24
    l, r = X16 + 82, XA - 64
    linie_teil(b, (l, Y1 + 18), (r, Y2 - 18), glatt(p(t, T['d1'] + 0.1, 0.6)), CB)
    linie_teil(b, (l, Y2 - 18), (r, Y1 + 18), glatt(p(t, T['d2'] + 0.1, 0.6)), CA)
    am = zurueck(p(t, T['mitte'], 0.5))                    # wo sich die Diagonalen kreuzen: die gemeinsame 24
    if am > 0:
        cx, cy = (l + r) / 2, (Y1 + Y2) / 2
        G.band(b, cx - 44 * am, cy - 30 * am, cx + 44 * am, cy + 30 * am, TEAL, 0.95 * klemm(am * 2), r=14)
        b.text('24', cx, cy, 38, '#ffffff', INTER_X, skala=max(am, 0.01), alpha=klemm(am * 2))

    # Abstände malnehmen: senkrecht zwischen +6 und +8
    ap = ein(t, T['prod'], 0.4)
    if ap > 0:
        xs = XA + 78
        b.linie([(xs, Y1 + 4), (xs, Y2 - 4)], CD, 6, alpha=ap)
        b.kreis(xs, (Y1 + Y2) / 2, 9, CD, alpha=ap)
        b.text('6 · 8 = 48', xs + 22, (Y1 + Y2) / 2, 30, CD, INTER_X, anker='l', alpha=ein(t, T['prod'] + 0.3))

    zeilen = [dict(nr='↘', farbe=CB, titel='über Kreuz', t_titel=T['d1'], t_rech=T['d1'] + 0.6,
                   teile=[('16', INK), (' + ', INK), ('8', CB), (' = 24', INK)], aktiv=(T['d1'], T['d2'])),
              dict(nr='↗', farbe=CA, titel='oder andersherum', t_titel=T['d2'], t_rech=T['d2'] + 0.6,
                   teile=[('18', INK), (' + ', INK), ('6', CA), (' = 24', INK)], aktiv=(T['d2'], T['mal10'])),
              dict(nr='2', farbe=TEAL, titel='mal 10', t_titel=T['mal10'], t_rech=T['mal10'] + 0.4,
                   teile=[('24 · 10 = ', INK), ('240', TEAL)], aktiv=(T['mal10'], T['prod'])),
              dict(nr='3', farbe=CD, titel='Abstände malnehmen', t_titel=T['prod'], t_rech=T['prod'] + 0.5,
                   teile=[('+ ', INK), ('6', CA), (' · ', INK), ('8', CB), (' = ', INK), ('48', CD)],
                   aktiv=(T['prod'], T['erg']))]
    x0, y0, w = 790, 86, 430
    G.schritte(b, t, x0, y0, w, zeilen, ([('16 · 18 = ', INK), ('288', GRUEN)], T['erg']), titel='Das Kreuz',
               alpha=ein(t, T['d1'] - 0.4))
    h = 66 + len(zeilen) * 104 + 84
    G.funken(b, t, T['erg'] + 0.05, G.mitten([('16 · 18 = ', INK), ('288', GRUEN)], x0 + w / 2, 46)[1],
             y0 + h - 46, r0=60, r1=170, fy=0.6)
    return b.img.resize((1280, 720), Image.LANCZOS)


def teil(arg):
    k0, k1, pfad = arg
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1280x720',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '22',
                           '-pix_fmt', 'yuv420p', pfad], stdin=subprocess.PIPE)
    for k in range(k0, k1):
        ff.stdin.write(bild(k / FPS).tobytes())
    ff.stdin.close()
    ff.wait()
    return pfad


def main():
    ziel = os.path.abspath(sys.argv[1])
    if '--bild' in sys.argv:
        for s in sys.argv[sys.argv.index('--bild') + 1].split(','):
            bild(float(s)).save(ziel.replace('.mp4', f'_{s}.png'))
        return
    n, teile = int(DAUER * FPS), 4
    g = [n * i // teile for i in range(teile + 1)]
    with Pool(teile) as pool:
        pfade = pool.map(teil, [(g[i], g[i + 1], ziel.replace('.mp4', f'_t{i}.mp4')) for i in range(teile)])
    liste = ziel.replace('.mp4', '_teile.txt')
    with open(liste, 'w') as f:
        f.writelines(f"file '{q}'\n" for q in pfade)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', liste, '-c', 'copy',
                    '-movflags', '+faststart', ziel], check=True)
    for q in pfade + [liste]:
        os.remove(q)
    print('fertig:', ziel)


if __name__ == '__main__':
    main()
