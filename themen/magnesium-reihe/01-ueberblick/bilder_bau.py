"""Bilder für Folge 1 der Magnesium-Reihe „Magnesium: Brauchst du es überhaupt?“, nur Stil G (Aquarell und Tusche).
Vorlage: themen/l-theanin/bilder_bau.py.
Erzeuger und Regeln wie themen/dmso/bilder_bau.py. Szenenbilder 5:4 (1280x1024), Kacheln 16:9 (2048x1152), GPT Image 2.
Regeln (Auftrag): Gesichter mit Augen, Nase, Mund; keine Schrift; keine Dosen oder Flaschen mit Dosierangaben, keine Marken.
Fehler je Bild in bilder.log, Kosten in bilder_kosten.json. Aufruf: python3 bilder_bau.py   (NUR=t1a,k1 für Einzelne)"""
import sys, os, json, time
from concurrent.futures import ThreadPoolExecutor
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', '..', 'schulprojekt-vitamin-d', 'erklaervideo'))
sys.path.insert(0, os.path.join(HIER, '..', '..', '..', 'werkzeug'))
import bilder_bau as BB

STIL = BB.STILE['G']
FORMAT = ' Landscape 5:4 composition: the main motif is large, centered and fills most of the frame, nothing important at the edges.'
KT = BB.KEIN_TEXT + ' Absolutely no words or letters anywhere, not on signs, books, screens, posters, boxes, bottles, jars or labels. No numbers, no dosage information, no brand names or logos.'
GESICHT = ' Every visible face has clearly drawn eyes, nose and mouth and a natural expression. Nobody swallows pills. Everyone is fully and modestly dressed.'
R = KT + GESICHT

SZENE = {
 # m1 Wozu der Körper es braucht
 'm1a': ("a friendly adult human silhouette standing, and beside it on an old brass kitchen scale three large silver-and-gold coins, warm light", KT),
 'm1b': ("a school book anatomy chart: a pale blue skeleton drawing on the left, a terracotta drawing of an arm muscle in the middle, and on the right a single thin red blood vessel with only a few tiny silver dots", KT),
 'm1c': ("a busy little cell interior like a workshop: many small enzyme machines, each holding a tiny glowing silver ball, conveyor belts and gears, playful scientific illustration", KT),
 'm1d': ("two friendly round molecules arm in arm like a dancing pair: a larger one shaped like a small battery with three tails and a small shining silver ball, energy sparks around them", KT),
 'm1e': ("a flexed arm muscle drawn anatomically, relaxing: small blue calcium balls flow back into storage pockets, pushed gently by small silver balls", KT),
 'm1f': ("scientific illustration of a nerve cell membrane with a tube-shaped channel; a small shining silver ball sits in the channel opening like a cork in a bottle", KT),
 'm1g': ("two bean-shaped kidneys drawn like a careful sorting station: many small silver balls flow in, almost all are carried back on little conveyor belts, only a few drip out", KT),
 # m2 Wie viel und woher
 'm2a': ("a woman and a man at a breakfast table in a bright kitchen, smiling, a bowl of oatmeal, whole grain bread and a glass of water in front of them", R),
 'm2b': ("a nutrition scientist at a desk looking at a big hand-drawn bell curve on paper, holding a pencil, thoughtful expression", R),
 'm2c': ("a still life on a wooden table: bowls of sunflower seeds, almonds, cashews, rolled oats, lentils and chickpeas, a loaf of dark whole grain bread", KT),
 'm2d': ("a German family dinner table seen from above with sliced bread, cheese, a bottle of sparkling mineral water without label and cups of coffee", KT),
 'm2e': ("a glass of sparkling mineral water with bubbles next to a plain glass bottle without any label, sunlight shining through, a few small silver sparkles in the water", KT),
 'm2f': ("two heaps of flour side by side: a brown whole grain heap with bran flakes and wheat ears, and a white fluffy heap; above the brown one six small silver balls, above the white one only one", KT),
 'm2g': ("a hand placing a slice of dark whole grain bread and a bowl of brown rice next to a slice of white toast and a bowl of white rice, swapping them, kitchen counter", KT),
 # m3 Mangel: selten oder häufig?
 'm3a': ("a crowd of people in a town square, each with a small grey question mark shape floating above, one person in front shrugging with a friendly face", R),
 'm3b': ("a large group of people standing in a meadow, about one in four lightly highlighted in warm ochre, the others in muted blue, seen from a slight distance", R),
 'm3c': ("a dinner plate with food being weighed and written down by a researcher with a clipboard, an old yellowed calendar page and a dusty file folder beside it", R),
 'm3d': ("a doctor's waiting room with a few calm patients sitting on chairs, a friendly nurse at the door", R),
 'm3e': ("a still life of everyday risk factors: a blister pack of plain stomach pills without writing, a glass of beer, a blood sugar meter without numbers and a hot water bottle, arranged on a table", KT),
 'm3f': ("a blood sample tube held up to the light in a laboratory, and beside it a large iceberg in the sea where only the small tip is above the water", KT),
 'm3g': ("a friendly woman doctor taking a blood sample from the arm of a calm middle-aged man in a bright consulting room", R),
 # m4 Präparate und Formen
 'm4a': ("a pharmacy shelf with many plain jars and boxes in different colors and sizes, all without any writing or labels, soft light", KT),
 'm4b': ("two glasses of water side by side: in the left a white powder dissolves completely into clear water with bubbles, in the right a white powder stays as a cloudy sediment at the bottom", KT),
 'm4c': ("a laboratory balance scale with two pans almost level, only a tiny difference, a scientist bending down looking closely with a magnifying glass", R),
 'm4d': ("three plain white pills without markings lying in a row on a white cloth, each with a small identical silver sparkle, a magnifying glass above them", KT),
 'm4e': ("expensive looking plain glass jars without labels on velvet in a luxury display case, and in front an empty laboratory table with a lonely question mark shape made of paper", KT),
 'm4f': ("a person sitting slightly uncomfortable holding the belly, a glass of water on the table, a bathroom door in the background, gentle humor, no nudity", R),
 'm4g': ("a hand turning a plain white supplement box without any writing to look at its side, a magnifying glass resting on the table", KT),
 # m5 Wofür belegt, wofür nicht
 'm5a': ("a strong arm muscle drawn anatomically, beside it a plain supplement box without any writing; a small balance shows that adding more silver balls does not make the muscle bigger", KT),
 'm5b': ("a hospital room with a pregnant woman resting in bed, an infusion drip bag on a stand connected to her arm, a midwife checking calmly", R),
 'm5c': ("a blood pressure cuff on an upper arm with a simple round dial without numbers, the needle moving slightly down, a calm older man", R),
 'm5d': ("a woman resting in a darkened room with a cool cloth on her forehead, a doctor holding a thick book of guidelines nearby", R),
 'm5e': ("a person sleeping peacefully in bed under a crescent moon, beside the bed a small stack of thin study papers and a few plain white capsules", R),
 'm5f': ("an elderly man sitting on the edge of his bed at night holding his calf, two identical plain pill bottles without labels on the nightstand", R),
 # m6 Selbstanwendung
 'm6a': ("a pill organizer with two compartments, morning sun and moon symbols drawn, each holding one plain white tablet, a glass of water next to it", KT),
 'm6b': ("two bean-shaped kidneys drawn in a friendly way, one healthy and pink, one pale and tired, a doctor's stethoscope lying beside them", KT),
 'm6c': ("two plain pill boxes without labels on a table with a large clock between them showing the passage of a few hours, a calendar of the day beside", KT),
 'm6d': ("a sunrise on the left and a moonlit night on the right in one landscape, in the middle a plain glass of water and a grey question mark shape", KT),
 'm6e': ("a woman doctor and a middle-aged man sitting at a desk talking, a plain white jar without label and a sheet of paper on the desk, friendly bright consulting room", R),
 # m7 Fazit
 'm7a': ("a day landscape divided into morning and evening, a calm person in the middle shrugging and smiling, sunrise on one side and moon on the other", R),
 'm7b': ("two plain white pills without markings on a scale that is almost perfectly level", KT),
 'm7c': ("a happy family sharing a colorful healthy meal with whole grain bread, nuts, vegetables and water, warm kitchen", R),
 'm7d': ("a person walking along a forest path holding a simple paper map, three friendly signposts without writing, sunlight", R),
 # Umbau 15.11.
 'm2x': ("a crowd of people in a park seen from slightly above; a few of them softly highlighted in warm ochre light, among them an older man with a blood pressure cuff and a woman holding her temple, a friendly doctor walking towards them", R),
 'm3y': ("a pregnant woman sitting on the edge of her bed at night, holding her calf with a slightly pained face, her partner sitting beside her with a hand on her shoulder", R),
 'm4x': ("an old 17th century apothecary shop with wooden shelves and plain ceramic jars without any writing, on the counter a large bowl of glittering white crystals", KT),
 'm4y': ("Surrey, southern England, 1618, a dry summer: a common with yellowed but still grassy meadow, hedgerows and old oak trees, gentle green-brown rolling downs under an English sky with clouds; a man in simple 1600s English clothes and hat beside a small muddy pool of water in a hoof print hollow; healthy well-fed brown and white cows sniff the water and turn away from it", R),
 'm4z': ("an 18th century chemist's laboratory with glass retorts, a small furnace and dishes of white powder, a scientist in a powdered wig carefully pouring a liquid", R),
}
KACHEL = {
 'k7': ("a friendly doctor talking to a small group of three different people in a bright consulting room: an older man, a middle-aged woman and a young woman, warm hopeful mood", R),
 'k8': ("an older man sitting on the edge of his bed at night holding his calf, a plain pill bottle without label on the nightstand, a grey question mark shape above", R),
 'k1': ("a school book anatomy chart with a pale blue skeleton drawing and a terracotta arm muscle drawing side by side, a few small silver sparkles around them", KT),
 'k2': ("a still life of sunflower seeds, almonds, oats, whole grain bread, lentils and a glass of sparkling water", KT),
 'k3': ("a doctor holding a blood sample tube up to the light, a calm patient sitting beside her", R),
 'k4': ("a pharmacy shelf with many plain jars and boxes in different colors, all without writing, one hand reaching for a jar", R),
 'k5': ("two researchers at a table with stacks of papers and a balance scale, discussing calmly", R),
 'k6': ("a person at a kitchen table holding a glass of water and a plain white tablet, a pill organizer and a clock beside, thoughtful", R),
 'r2': ("a landscape split into a sunrise morning half and a moonlit evening half, a glass of water in the middle", KT),
 'r3': ("several plain jars and pills of different shapes and colors arranged side by side on a table for comparison, magnifying glass", KT),
 'r4': ("a calf muscle and a hand with slightly trembling fingers, a doctor's stethoscope beside, soft concern", R),
 'r5': ("a measuring cup overflowing with water on a table, a stop hand gesture drawn as a friendly simple sign without letters", KT),
 'r6': ("a person sleeping peacefully under a crescent moon in a cozy bedroom", R),
 'r7': ("a stressed person at a desk with papers, taking a deep calm breath, a window with trees", R),
}
GROESSE = {'szene': {'size': '1280x1024'}, 'kachel': {'size': '2048x1152'}}


def log(text):
    with open(os.path.join(HIER, 'bilder.log'), 'a') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + text + '\n')


def eins(job):
    key, art = job
    ziel = os.path.join(HIER, 'bilder', 'G', key + '.jpg')
    if os.path.exists(ziel):
        return key, 0.0
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    motiv, regel = (SZENE if art == 'szene' else KACHEL)[key]
    fmt = FORMAT if art == 'szene' else BB.GEMEINSAM
    try:
        c = BB.erzeuge(STIL + fmt + regel, motiv, ziel, config=GROESSE[art])
        log(f'ok G/{key} {c:.1f}')
        return key, c
    except Exception as e:
        msg = e.read()[:300] if hasattr(e, 'read') else str(e)[:300]
        log(f'FEHLER G/{key} {msg}')
        print('FEHLER', key, msg, flush=True)
        return key, 0.0


if __name__ == '__main__':
    nur = os.environ.get('NUR')
    jobs = [(k, 'kachel') for k in KACHEL] + [(k, 'szene') for k in SZENE]
    if nur:
        jobs = [j for j in jobs if j[0] in nur.split(',')]
    with ThreadPoolExecutor(8) as ex:
        erg = list(ex.map(eins, jobs))
    pfad = os.path.join(HIER, 'bilder_kosten.json')
    kosten = json.load(open(pfad)) if os.path.exists(pfad) else {}
    for k, c in erg:
        if c:
            kosten[f'G/{k}'] = round(c, 1)
    json.dump(kosten, open(pfad, 'w'), indent=1, sort_keys=True)
    print('neu erzeugt:', sum(1 for _, c in erg if c), 'Bilder,', round(sum(c for _, c in erg), 1), 'Credits; gesamt',
          round(sum(kosten.values()), 1))
    json.dump({'stil': STIL, 'szene': SZENE, 'kachel': KACHEL, 'groesse': GROESSE},
              open(os.path.join(HIER, 'bilder_prompts.json'), 'w'), ensure_ascii=False, indent=1)
