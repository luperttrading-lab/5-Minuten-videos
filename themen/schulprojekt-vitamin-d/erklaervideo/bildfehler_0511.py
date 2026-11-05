"""Nutzerhinweise 05.11. abends: Pipettenflasche tropft von der falschen Seite, Tachometer gebeult.
Geprüft in allen acht Stilen; eindeutig betroffen: D/v4a, H/v4a, I/e4 (Tropfen unten aus der Flasche), D/v3c, G/v3c (Rand nicht rund).
Alte Bilder bleiben als *_alt0511.jpg."""
import os, json
from concurrent.futures import ThreadPoolExecutor
import bilder_bau as BB
from bilder_v2 import FORMAT, KT, GROESSE

PIPETTE = ("a glass dropper pipette with a rubber bulb hovers above a spoon, its thin glass tip points straight down and a single "
           "golden drop falls from the very tip of the pipette into the spoon; beside the spoon stands a small plain unlabeled "
           "open glass bottle without its cap. The drop comes only from the pipette tip, never from the bottom or side of a bottle. No hands.")
TACHO = ("a large simple gauge dial seen straight from the front, its round face and rim form a perfectly round, smooth, undeformed circle; "
         "in the upper half a semicircular arc divided into three colored zones red, yellow and green, a single needle pointing into the green zone, "
         "no numbers, no tick marks")
JOBS = [  # (Stil, Datei, Motiv, Regel, Format, Größe)
 ('D', 'v4a', PIPETTE + ' Bright morning light.', KT, FORMAT, GROESSE['szene']),
 ('H', 'v4a', PIPETTE + ' Bright morning light.', KT, FORMAT, GROESSE['szene']),
 ('I', 'e4', PIPETTE + ' Next to it a breakfast with avocado, boiled eggs and a few nuts, bright morning light.', BB.KEIN_TEXT, BB.GEMEINSAM, GROESSE['kachel']),
 ('D', 'v3c', TACHO, KT, FORMAT, GROESSE['szene']),
 ('G', 'v3c', TACHO, KT, FORMAT, GROESSE['szene']),
]

def eins(job):
    stil, key, motiv, regel, fmt, groesse = job
    ziel, alt = f'bilder/{stil}/{key}.jpg', f'bilder/{stil}/{key}_alt0511.jpg'
    if os.path.exists(ziel) and not os.path.exists(alt):
        os.rename(ziel, alt)
    return stil, key, BB.erzeuge(BB.STILE[stil] + fmt + regel, motiv, ziel, config=groesse)

if __name__ == '__main__':
    with ThreadPoolExecutor(5) as ex:
        erg = list(ex.map(eins, JOBS))
    kosten = json.load(open('bilder_kosten.json'))
    for s, k, c in erg:
        kosten[f'{s}/{k} (Bildfehler 05.11.)'] = round(c, 1)
        print(s, k, round(c, 1), 'Credits')
    json.dump(kosten, open('bilder_kosten.json', 'w'), indent=1, sort_keys=True)
    print('Summe', round(sum(c for *_, c in erg), 1))
