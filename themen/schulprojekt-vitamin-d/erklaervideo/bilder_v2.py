"""Zweite Bildrunde (Nutzerwunsch 03.11. abends):
- Szenenbilder eigens im Format 5:4 (1280x1024) für das Bildfeld neben dem Text, statt Ausschnitte aus den 16:9-Kachelbildern.
- Etwa alle 6–12 Sekunden ein neues Bild (Bildwechsel an Satzanfängen, siehe SZENEN in drehbuch_bau.py).
- Sonnenbad mit Mann und Frau (nicht nur eine Frau im Bikini), glatte Haut ohne Funken/Punkte (Knete sah nach Ausschlag aus).
Aufruf: python3 bilder_v2.py [STIL ...]"""
import sys, os, json
from concurrent.futures import ThreadPoolExecutor
import bilder_bau as BB

HAUT = ' Smooth clean natural skin without spots, dots, sparkles or speckles.'
FORMAT = ' Landscape 5:4 composition: the main motif is large, centered and fills most of the frame, nothing important at the edges.'
KT = BB.KEIN_TEXT + ' Absolutely no words or letters anywhere, not on signs, books, screens, posters or labels.'

# Schlüssel = Dateiname, Wert = (Motiv, Textregel)
SZENE = {
 # v1 Ein Hormon aus Licht
 'v1a': ("close view of a person's bare forearm and shoulder in bright warm sunlight, the sun visible in the corner, soft golden light on the skin", KT),
 'v1b': ("a simple friendly stylized liver and a kidney floating side by side, a single glowing golden droplet travels along a dotted path from the liver to the kidney", KT),
 'v1c': ("a strong healthy stylized bone next to a flexed arm muscle, small white calcium crystals flowing gently into the bone", KT),
 'v1d': ("a plate with grilled herring and salmon fillets, a halved boiled egg and a few mushrooms on a wooden table", KT),
 # v2 Sonne richtig nutzen
 'v2a': ("a man in swim shorts and a woman in a modest one-piece swimsuit sitting side by side on towels on a green lawn at midday, the sun high in the sky, very short shadows, warm golden light, natural relaxed pose", KT + HAUT),
 'v2b': ("a young man in a t-shirt and shorts walking happily through a sunny summer park at midday, the sun high in the sky", KT + HAUT),
 'v2c': ("a man and a woman in swimwear standing at the shore of a lake at midday, the sun high above, short shadows, both relaxed", KT + HAUT),
 'v2d': ("a town street in winter, a low pale sun just above the rooftops, very long shadows on the snow, people in thick coats, scarves and hats", KT),
 'v2e': ("an elderly man in a sun hat and a young woman with dark skin sitting on a park bench in the sun, the woman applying sunscreen to her arm", KT + HAUT),
 'v2f': ("a person standing in a garden at noon with a very short shadow directly under their feet, the sun straight overhead", KT + HAUT),
 # v3 Dein Wert in ng/ml
 'v3a': ("a friendly doctor holding up a small blood sample tube with a red cap in a bright clinic room, a patient smiling", KT),
 'v3b': ("a blood sample tube with a red cap next to two plain empty measuring columns with no scale marks, one horizontal line connects the same height on both columns",
         BB.nur("exactly two labels: '20 ng/ml' under the left column and '50 nmol/l' under the right column") + ' No other words.'),
 'v3c': ("a large simple gauge dial with three colored zones red, yellow and green and a needle pointing into the green zone, no numbers", KT),
 'v3d': ("a grey winter day in a German town square, many people in winter coats, pale light, overcast sky", KT),
 'v3e': ("a patient and a doctor sitting at a desk, the patient points at a blank sheet of paper and asks a question, friendly atmosphere", KT),
 # v4 Wie viel du brauchst
 'v4a': ("a small plain unlabeled dropper bottle releasing a single golden drop onto a spoon, bright morning light", KT),
 'v4b': ("a large calm green protective shield standing in front of a small plain unlabeled dropper bottle on a table", KT),
 'v4c': ("two adults of clearly different body size standing side by side, friendly and respectful, each holding a small plain unlabeled dropper bottle, the larger person's bottle slightly bigger", KT + HAUT),
 'v4d': ("two researchers at a table discussing, one pointing at an empty blank chalkboard behind them, coffee cups", KT),
 'v4e': ("a breakfast table with avocado slices, boiled eggs, nuts and a spoon holding a single golden drop", KT),
 'v4f': ("a doctor and a patient sitting together and talking, a small plain unlabeled dropper bottle on the table between them", KT),
 # v5 Was Studien zeigen
 'v5a': ("a large friendly crowd of people of all ages split into two groups, two scientists in white coats with clipboards stand in front and compare them", KT),
 'v5b': ("a doctor and a middle-aged patient shaking hands happily in a bright consulting room", KT),
 'v5c': ("a woman stretching her hands and knees comfortably in a sunny living room, moving freely and smiling", KT + HAUT),
 'v5d': ("a family on a walk in autumn leaves, one person holding a tissue, the others healthy and cheerful", KT),
 'v5e': ("a few stylized chromosomes floating in soft light, each with small glowing caps at both ends", KT),
 'v5f': ("an older couple hiking cheerfully on a sunny hill path", KT + HAUT),
 'v5g': ("a person by a window in winter holding a warm cup, a pale low sun outside over snowy roofs", KT),
 # v6 Wer besonders profitiert
 'v6a': ("a mother gently giving her baby a single drop from a small spoon, cozy nursery", KT),
 'v6b': ("an elderly woman in an armchair by a sunny window in a care home, a friendly nurse beside her", KT),
 'v6c': ("an office worker at a desk under artificial lamp light, late evening, the window dark", KT),
 'v6d': ("a pregnant woman standing by a bright window, hand on her belly, calm and happy", KT),
 # v7 Fazit
 'v7a': ("a split scene: on the left half a bright summer park with a person in t-shirt and shorts enjoying the sun, on the right half a cozy winter kitchen where the same person takes a single golden drop with breakfast", KT),
 'v7b': ("a man and a woman in t-shirts and shorts walking together through a sunny summer park at midday", KT + HAUT),
 'v7c': ("a cozy winter breakfast table by a frosty window, a spoon with a single golden drop", KT),
 'v7d': ("a doctor nodding and smiling at a patient during a calm conversation", KT),
 'v7e': ("a group of happy people of all ages in a sunny meadow, relaxed and cheerful", KT + HAUT),
}
# neue 16:9-Kachel fürs Sonnenkapitel (Mann und Frau statt Frau im Bikini)
KACHEL = {'e2a': (SZENE['v2a'][0], SZENE['v2a'][1])}
GROESSE = {'szene': {'size': '1280x1024'}, 'kachel': {'size': '2048x1152'}}

def eins(job):
    stil, key, art = job
    ziel = f'bilder/{stil}/{key}.jpg' if art == 'szene' else f'bilder/{stil}/{key}_v2.jpg'
    if os.path.exists(ziel):
        return stil, key, 0.0
    motiv, regel = (SZENE if art == 'szene' else KACHEL)[key]
    fmt = FORMAT if art == 'szene' else BB.GEMEINSAM
    try:
        return stil, key, BB.erzeuge(BB.STILE[stil] + fmt + regel, motiv, ziel, config=GROESSE[art])
    except Exception as e:
        msg = e.read()[:300] if hasattr(e, 'read') else str(e)[:300]
        print('FEHLER', stil, key, msg, flush=True)
        return stil, key, 0.0

if __name__ == '__main__':
    stile = sys.argv[1:] or list(BB.STILE)
    jobs = [(s, k, 'szene') for s in stile for k in SZENE]
    if os.environ.get('MIT_KACHEL'):
        jobs += [(s, k, 'kachel') for s in stile for k in KACHEL]
    with ThreadPoolExecutor(8) as ex:
        erg = list(ex.map(eins, jobs))
    kosten = json.load(open('bilder_kosten.json'))
    for s, k, c in erg:
        if c:
            kosten[f'{s}/{k} (v2)'] = round(c, 1)
    json.dump(kosten, open('bilder_kosten.json', 'w'), indent=1, sort_keys=True)
    print('neu erzeugt:', sum(1 for *_, c in erg if c), 'Bilder,', round(sum(c for *_, c in erg), 1), 'Credits')
    json.dump({'szene': SZENE, 'kachel': KACHEL, 'groesse': GROESSE}, open('bilder_prompts_v2.json', 'w'), ensure_ascii=False, indent=1)
