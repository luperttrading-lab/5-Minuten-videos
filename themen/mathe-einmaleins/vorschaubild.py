#!/usr/bin/env python3
"""YouTube-Vorschaubild (1280 × 720) für den Zehner-Trick, ganz per Code im Stil des Videos.

Drei Fassungen zur Wahl (Nutzerwunsch 05.11.). Fürs Handy: wenige, große Elemente; die Zahlen wie im Video gefärbt
(Einer der 1. Zahl orange, der 2. violett). Die Fläche stammt aus dem Video selbst (Bild bei 72 s, „Warum klappt das?“).

Aufruf: python3 vorschaubild.py <ausgabeordner>
"""
import os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
_argv, sys.argv = sys.argv, [sys.argv[0], '/dev/null']   # regel.py liest beim Import argv
import regel as G                                          # noqa: E402
sys.argv = _argv
from PIL import Image                                      # noqa: E402
from regel import Bild, INTER_X, INK, GRAU, TEAL, GRUEN, CA, CB, K, zeile, band, uhr, mitten  # noqa: E402

AUFGABE = [('1', INK), ('6', CA), (' · ', INK), ('1', INK), ('8', CB)]


def fertig(b, pfad):
    b.img.resize((1280, 720), Image.LANCZOS).save(pfad)
    print(pfad)


def name_band(b, x, y, g=50, breit=None):
    w = breit or G.breite('Der Zehner-Trick', INTER_X, g) + 2 * 0.6 * g
    band(b, x - w / 2, y - 0.95 * g, x + w / 2, y + 0.95 * g, TEAL, 1.0, r=0.4 * g)
    b.text('Der Zehner-Trick', x, y, g, '#ffffff', INTER_X)


def uhr_zeile(b, vor, nach, y, g):
    """„vor (4) nach“ als zentrierte Zeile; die Uhr ersetzt die Zahl 4."""
    r = 0.95 * g
    wv, wn, luft = G.breite(vor, INTER_X, g), G.breite(nach, INTER_X, g), 0.3 * g
    x = 640 - (wv + wn + 2 * r + 2 * luft) / 2
    b.text(vor, x, y, g, INK, INTER_X, anker='l')
    uhr(b, x + wv + luft + r, y, r, 0.0, sek=4)
    b.text(nach, x + wv + 2 * luft + 2 * r, y, g, INK, INTER_X, anker='l')


def frage(aus):
    """Die Aufgabe als Frage, darunter die Uhr: Wer klickt, will die Lösung sehen."""
    b = Bild(G.grund())
    zeile(b, AUFGABE + [(' = ?', GRAU)], 640, 250, 196, INTER_X)
    uhr_zeile(b, 'Im Kopf in', 'Sekunden?', 530, 80)
    fertig(b, os.path.join(aus, 'vorschaubild_frage.png'))


def flaeche(aus):
    """Links die Fläche aus dem Video (240 + 48), rechts Aufgabe und Ergebnis."""
    b = Bild(G.grund())
    bild = G.bild(72.0).resize((1280 * K, 720 * K), Image.LANCZOS)
    x0, y0, x1, y1 = 120, 85, 625, 625                     # Ausschnitt (1280er Koordinaten): Fläche samt 24-Klammer
    stueck = bild.crop((x0 * K, y0 * K, x1 * K, y1 * K))
    f = 1.2
    stueck = stueck.resize((int(stueck.width * f), int(stueck.height * f)), Image.LANCZOS)
    b.img.paste(stueck, (int(10 * K), int(30 * K)))
    zeile(b, AUFGABE, 960, 200, 150, INTER_X)
    zeile(b, [('= ', GRAU), ('288', GRUEN)], 960, 380, 150, INTER_X)
    name_band(b, 960, 570, 50)
    fertig(b, os.path.join(aus, 'vorschaubild_flaeche.png'))


def loesung(aus):
    """Aufgabe mit Lösung, darunter Uhr und Name: Das Versprechen steht im Bild."""
    b = Bild(G.grund())
    zeile(b, AUFGABE + [(' = ', GRAU), ('288', GRUEN)], 640, 210, 170, INTER_X)
    uhr_zeile(b, 'im Kopf in', 'Sekunden', 420, 76)
    name_band(b, 640, 600, 50)
    fertig(b, os.path.join(aus, 'vorschaubild_loesung.png'))


if __name__ == '__main__':
    ziel = sys.argv[1]
    os.makedirs(ziel, exist_ok=True)
    G.ton_und_zeitplan()
    for fn in (frage, flaeche, loesung):
        fn(ziel)
