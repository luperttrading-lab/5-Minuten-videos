"""Nachlauf 03.11.: sieben Bilder mit strengeren Vorgaben neu (englische Beschriftungen, falsche Skala, Badeszene zu aufreizend)."""
import json, os, sys
from concurrent.futures import ThreadPoolExecutor
import bilder_bau as BB

STRENG = (' Absolutely no words or letters of any kind anywhere else, not on signs, posters, books, organs or labels; '
          'no speech bubbles, no notes, no numbers.')
JOBS = {
 ('I', 'e2a'): ("a cheerful father and his young son in swim shorts sitting side by side on a towel on a green lawn at midday "
                "in strong summer sun, sun high in the sky, very short shadows, tiny glowing golden sparks rising from their "
                "sunlit skin; family-friendly, natural relaxed sitting pose", BB.KEIN_TEXT + STRENG),
 ('I', 'e3'): ("a blood sample tube with a red cap standing next to two plain empty measuring columns side by side with no scale "
               "marks, one horizontal glowing line connects the same height on both columns",
               BB.nur("exactly two labels: '20 ng/ml' under the left column and '50 nmol/l' under the right column") + STRENG),
 ('J', 'e1'): (BB.MOTIVE['e1'][0], BB.nur("the single label 'Vitamin D' next to the glowing droplet; the liver and kidney have no labels") + STRENG),
 ('J', 'e2a'): (BB.MOTIVE['e2a'][0], BB.KEIN_TEXT + STRENG),
 ('L', 'e1'): (BB.MOTIVE['e1'][0], BB.nur("the single label 'Vitamin D' next to the glowing droplet; the liver and kidney have no labels") + STRENG),
 ('L', 'e3'): ("a blood sample tube with a red cap standing next to two plain empty measuring columns side by side with no scale "
               "marks, one horizontal red line connects the same height on both columns",
               BB.nur("exactly two labels: '20 ng/ml' under the left column and '50 nmol/l' under the right column, letters large and clear") + STRENG),
 ('L', 'e7'): (BB.MOTIVE['e7'][0], BB.KEIN_TEXT + STRENG),
}

def eins(item):
    (stil, key), (motiv, regel) = item
    ziel = f'bilder/{stil}/{key}.jpg'
    return stil, key, BB.erzeuge(BB.STILE[stil] + BB.GEMEINSAM + regel, motiv, ziel)

if __name__ == '__main__':
    with ThreadPoolExecutor(7) as ex:
        erg = list(ex.map(eins, JOBS.items()))
    k = json.load(open('bilder_kosten.json'))
    for s, key, c in erg:
        k[f'{s}/{key} (Nachlauf)'] = round(c, 1)
        print(s, key, round(c, 1))
    json.dump(k, open('bilder_kosten.json', 'w'), indent=1, sort_keys=True)
