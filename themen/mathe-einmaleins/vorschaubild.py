#!/usr/bin/env python3
"""YouTube-Vorschaubilder (1280 × 720) für die Reihe „Kopfrechnen“: ein festes Design für alle Folgen.

Nutzerwunsch 05.11.: alle Vorschaubilder der Reihe gleich aufgebaut (Wiedererkennung). Fest sind Schrift (Inter
ExtraBold), Farben (Teal, Einer orange und violett wie im Video), Aufbau und das Zeichen „KOPFRECHNEN“; nur die
Aufgabe und der Name des Tricks wechseln. Ganz per Code, Formeln nie per KI-Bild.

Drei Stile zur Wahl, je an drei Folgen gezeigt (16 · 18 echt, die anderen beiden als Beispiel aus dem Folgenplan
`themen/mathe-tricks/folgen.py`, Namen dort noch nicht festgelegt).

Aufruf: python3 vorschaubild.py <ausgabeordner> [stil]     (ohne stil: alle Stile und die Vergleichsbögen)
"""
import os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
_argv, sys.argv = sys.argv, [sys.argv[0], '/dev/null']   # regel.py liest beim Import argv
import regel as G                                          # noqa: E402
sys.argv = _argv
from PIL import Image, ImageDraw                           # noqa: E402
from regel import Bild, INTER_X, INK, GRAU, TEAL, CA, CB, K, zeile, band  # noqa: E402

WEISS = '#ffffff'
# Folgen: Aufgabe als (Text, Farbe)-Teile; None = Grundfarbe des Stils. Rechnungen geprüft: 16·18 = 288,
# 47·11 = 517, 35² = 1225.
FOLGEN = [
    dict(id='zehner', aufgabe=[('1', None), ('6', CA), (' · ', None), ('1', None), ('8', CB)], name='Der Zehner-Trick'),
    dict(id='elfer', aufgabe=[('4', CA), ('7', CB), (' · 11', None)], name='Der Elfer-Trick'),
    dict(id='fuenfer', aufgabe=[('3', CA), ('5', CB), ('²', None)], name='Der Fünfer-Trick'),
]


def fertig(b, pfad):
    b.img.resize((1280, 720), Image.LANCZOS).save(pfad)
    return pfad


def teile(folge, grund_farbe, frage_farbe):
    return [(s, c or grund_farbe) for s, c in folge['aufgabe']] + [(' = ?', frage_farbe)]


def papier(folge, pfad):
    """Warmes Papier wie im Video, unten eine durchgehende Teal-Leiste mit Name und Reihe."""
    b = Bild(G.grund())
    zeile(b, teile(folge, INK, GRAU), 640, 285, 200, INTER_X)
    band(b, 0, 560, 1280, 720, TEAL, 1.0, r=0)
    b.text(folge['name'], 60, 640, 68, WEISS, INTER_X, anker='l')
    b.text('KOPFRECHNEN', 1220, 640, 40, '#bfe3df', INTER_X, anker='r')
    return fertig(b, pfad)


def rahmen(folge, pfad):
    """Papier in einem dicken Teal-Rahmen, oben links ein Reiter „KOPFRECHNEN“, der Name als dunkles Band."""
    b = Bild(G.grund())
    d = 26
    for x0, y0, x1, y1 in ((0, 0, 1280, d), (0, 720 - d, 1280, 720), (0, 0, d, 720), (1280 - d, 0, 1280, 720)):
        band(b, x0, y0, x1, y1, TEAL, 1.0, r=0)
    band(b, 0, 0, 440, 100, TEAL, 1.0, r=0)
    b.text('KOPFRECHNEN', 56, 56, 42, WEISS, INTER_X, anker='l')
    zeile(b, teile(folge, INK, GRAU), 640, 320, 190, INTER_X)
    g = 60
    w = G.breite(folge['name'], INTER_X, g) + 1.3 * g
    band(b, 640 - w / 2, 560 - 0.95 * g, 640 + w / 2, 560 + 0.95 * g, INK, 1.0, r=0.35 * g)
    b.text(folge['name'], 640, 560, g, WEISS, INTER_X)
    return fertig(b, pfad)


def dunkel(folge, pfad):
    """Dunkler Grund (sticht auf der hellen YouTube-Seite heraus), Ziffern hell, Name als Teal-Band."""
    b = Bild(INK)
    for y in range(16, 720, 32):                           # feines Punktraster wie im Video, hell auf dunkel
        for x in range(16, 1280, 32):
            b.kreis(x, y, 1.4, '#ffffff', alpha=0.07)
    b.text('KOPFRECHNEN', 56, 64, 42, '#5fc4b8', INTER_X, anker='l')
    zeile(b, teile(folge, WEISS, '#9aa0ad'), 640, 300, 200, INTER_X)
    g = 62
    w = G.breite(folge['name'], INTER_X, g) + 1.3 * g
    band(b, 640 - w / 2, 560 - 0.95 * g, 640 + w / 2, 560 + 0.95 * g, TEAL, 1.0, r=0.35 * g)
    b.text(folge['name'], 640, 560, g, WEISS, INTER_X)
    return fertig(b, pfad)


STILE = dict(papier=('Papier mit Teal-Leiste unten', papier), rahmen=('Teal-Rahmen mit Reiter', rahmen),
             dunkel=('Dunkler Grund', dunkel))


def bogen(stil, pfade, pfad):
    """Drei Vorschaubilder eines Stils nebeneinander, so klein wie in der YouTube-Liste auf dem Handy."""
    W_, H_ = 1280, 720
    img = Image.new('RGB', (W_, H_), '#ffffff')
    d = ImageDraw.Draw(img)
    from animationen import schrift
    f1, f2 = schrift(INTER_X, 34), schrift(INTER_X, 22)
    d.text((80, 22), STILE[stil][0], font=f1, fill=INK)
    d.text((80, 66), 'gleicher Aufbau für jede Folge – nur Aufgabe und Name wechseln', font=f2, fill=GRAU)
    for q, (x, y) in zip(pfade, ((80, 115), (700, 115), (390, 412))):
        img.paste(Image.open(q).resize((500, 281), Image.LANCZOS), (x, y))
    img.save(pfad)
    return pfad


if __name__ == '__main__':
    ziel = sys.argv[1]
    os.makedirs(ziel, exist_ok=True)
    stile = sys.argv[2:] or list(STILE)
    for s in stile:
        pfade = [STILE[s][1](f, os.path.join(ziel, f'vb_{s}_{f["id"]}.png')) for f in FOLGEN]
        print(bogen(s, pfade, os.path.join(ziel, f'bogen_{s}.png')))
