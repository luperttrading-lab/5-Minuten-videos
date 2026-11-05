"""Bildkorrektur 05.11. (übernommen: nur D; die J-Bilder liegen als *_vorschlag_gesicht.jpg bei, J hat die Vitamin-D-Sitzung mit gesichter_J.py korrigiert).
 (Urteile des Nutzers auf der Vergleichsseite):
- D: Nahaufnahme von Arm/Schulter wirkt krank, Oberarm mit Muskel und Knochen unschön -> ganze, glatte Knetfiguren statt Hautnahaufnahmen.
- J: Figuren sollen immer ein Gesicht haben -> gesichtslose oder abgewandte Figuren neu.
Alte Fassungen bleiben als *_alt0511.jpg erhalten."""
import os, shutil, json
from concurrent.futures import ThreadPoolExecutor
import bilder_bau as BB
import bilder_v2 as B2

GLATT = (' The clay surfaces are smooth, soft and evenly polished like fresh modeling clay; skin is one smooth even color, '
         'no cracks, bumps, pores, dots or rough texture on skin.')
GESICHT = (' Every person shows a clearly drawn friendly face with eyes, nose and mouth, turned toward the viewer or toward each other; '
           'no faceless figures, no figures seen from behind, no hidden faces.')
JOBS = {
 ('D', 'v1a'): ("a cute clay figure of a young woman standing in a sunny meadow, stretching one bare arm toward the bright sun, "
                "warm golden sunlight on her arm, the whole figure visible from head to feet", B2.KT + GLATT),
 ('D', 'v1c'): ("a cheerful clay figure of a man proudly flexing his arm muscle next to a big friendly cartoon bone character with a smiling face, "
                "small white calcium beads flowing gently into the bone, whole figures visible", B2.KT + GLATT),
 ('J', 'v2a'): (B2.SZENE['v2a'][0], B2.KT + B2.HAUT + GESICHT),
 ('J', 'v4c'): (B2.SZENE['v4c'][0], B2.KT + GESICHT),
 ('J', 'v4d'): ("two researchers sitting at a table facing each other and smiling, one pointing at an empty blank chalkboard on the side wall, coffee cups", B2.KT + GESICHT),
 ('J', 'v6c'): ("an office worker sitting upright at a desk under artificial lamp light in the late evening, looking a bit tired but awake, the window dark", B2.KT + GESICHT),
 ('J', 'v7a'): ("a split scene: on the left half a bright summer park with a smiling person in t-shirt and shorts facing the viewer and enjoying the sun, "
                "on the right half a cozy winter kitchen where the same smiling person takes a single golden drop with breakfast", B2.KT + GESICHT),
}

def eins(item):
    (stil, key), (motiv, regel) = item
    ziel = f'bilder/{stil}/{key}.jpg'
    alt = f'bilder/{stil}/{key}_alt0511.jpg'
    if not os.path.exists(alt):
        shutil.copy(ziel, alt)
    tmp = f'bilder/{stil}/{key}_neu.jpg'
    c = BB.erzeuge(BB.STILE[stil] + B2.FORMAT + regel, motiv, tmp, config=B2.GROESSE['szene'])
    return stil, key, c

if __name__ == '__main__':
    with ThreadPoolExecutor(7) as ex:
        erg = list(ex.map(eins, JOBS.items()))
    k = json.load(open('bilder_kosten.json'))
    for s, key, c in erg:
        k[f'{s}/{key} (Fix 05.11.)'] = round(c, 1)
        print(s, key, round(c, 1))
    json.dump(k, open('bilder_kosten.json', 'w'), indent=1, sort_keys=True)
    print('Summe', round(sum(c for *_, c in erg), 1))
