"""Nutzerwunsch 05.11.: Figuren immer mit Gesicht. Vier J-Bilder neu (alte als *_ohne_gesicht.jpg aufbewahrt)."""
import os, json
from concurrent.futures import ThreadPoolExecutor
import bilder_bau as BB
from bilder_v2 import SZENE, FORMAT, GROESSE

GESICHT = (' Every person shows a clearly drawn friendly face with eyes, nose and mouth, facing the viewer or in three-quarter view;'
           ' no blank or featureless faces, nobody seen only from behind, no face hidden.')
NEU = {
 'v2a': SZENE['v2a'][0] + ', both smiling towards the viewer',
 'v5g': 'a person standing by a window in winter, turned three-quarters towards the viewer so the friendly face is clearly visible, holding a warm cup, a pale low sun outside over snowy roofs',
 'v6c': 'an office worker sitting upright at a desk under artificial lamp light in the late evening, the window dark, looking a bit tired but friendly towards the viewer',
 'v2d': 'a town street in winter, a low pale sun just above the rooftops, very long shadows on the snow, a few people in thick coats, scarves and hats walking towards the viewer with friendly visible faces',
}

def eins(key):
    ziel = f'bilder/J/{key}.jpg'
    alt = f'bilder/J/{key}_ohne_gesicht.jpg'
    if os.path.exists(ziel) and not os.path.exists(alt):
        os.rename(ziel, alt)
    regel = SZENE[key][1]
    return key, BB.erzeuge(BB.STILE['J'] + FORMAT + regel + GESICHT, NEU[key], ziel, config=GROESSE['szene'])

if __name__ == '__main__':
    with ThreadPoolExecutor(4) as ex:
        erg = list(ex.map(eins, NEU))
    kosten = json.load(open('bilder_kosten.json'))
    for k, c in erg:
        kosten[f'J/{k} (Gesicht 05.11.)'] = round(c, 1)
        print(k, round(c, 1), 'Credits')
    json.dump(kosten, open('bilder_kosten.json', 'w'), indent=1, sort_keys=True)
    print('Summe', round(sum(c for _, c in erg), 1))
