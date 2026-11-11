"""Bilder fürs Erklärvideo „L-Theanin: Was der Stoff aus dem Tee kann“, nur Stil G (Aquarell und Tusche).
Erzeuger und Regeln wie themen/dmso/bilder_bau.py. Szenenbilder 5:4 (1280x1024), Kacheln 16:9 (2048x1152), GPT Image 2.
Regeln (Auftrag): Gesichter mit Augen, Nase, Mund; keine Schrift; keine Dosen oder Flaschen mit Dosierangaben, keine Marken.
Fehler je Bild in bilder.log, Kosten in bilder_kosten.json. Aufruf: python3 bilder_bau.py   (NUR=t1a,k1 für Einzelne)"""
import sys, os, json, time
from concurrent.futures import ThreadPoolExecutor
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', 'schulprojekt-vitamin-d', 'erklaervideo'))
sys.path.insert(0, os.path.join(HIER, '..', '..', 'werkzeug'))
import bilder_bau as BB

STIL = BB.STILE['G']
FORMAT = ' Landscape 5:4 composition: the main motif is large, centered and fills most of the frame, nothing important at the edges.'
KT = BB.KEIN_TEXT + ' Absolutely no words or letters anywhere, not on signs, books, screens, posters, boxes, bottles, jars or labels. No numbers, no dosage information, no brand names or logos.'
GESICHT = ' Every visible face has clearly drawn eyes, nose and mouth and a natural expression. Nobody swallows pills. Everyone is fully and modestly dressed.'
R = KT + GESICHT

SZENE = {
 # t1 Entdeckt im Tee
 't1a': ("green terraced tea fields on gentle hills near a Japanese town with a river and a wooden bridge, traditional roofs, morning mist", KT),
 't1b': ("a Japanese scientist around 1949 in a white lab coat and round glasses in a simple laboratory, examining green tea leaves in a glass dish, glass flasks around him", R),
 't1c': ("a glass dish with fine colorless needle-shaped crystals on a wooden lab bench, beside it a small heap of dried green tea leaves and a 1940s microscope", KT),
 't1d': ("tea bushes covered by traditional straw and bamboo shade screens in a Japanese tea garden, soft dim light under the screens, a farmer checking the leaves", R),
 't1e': ("a friendly simple ball-and-stick molecule model of a small amino acid with grey, red, blue and white balls, lying on fresh green tea leaves", KT),
 't1f': ("cross-section of a tea plant in the soil: the roots glow softly golden and small golden dots travel up through the stem into the young top leaves", KT),
 't1g': ("a bay bolete mushroom with a chestnut-brown cap and yellowish pores growing in forest moss between pine needles", KT),
 't1h': ("a bowl of green tea with gentle steam on a wooden table, beside it a small bowl of clear broth and dried seaweed, warm savory mood", KT),
 # t2 Vom Blatt zur Kapsel
 't2a': ("close-up of dark green shaded tea leaves, next to them a bamboo whisk and a ceramic bowl with bright green whisked powdered tea", KT),
 't2b': ("a teapot pouring green tea into a simple cup, beside it a small sand timer, a tiny heap of white powder on a spoon next to the cup", KT),
 't2d': ("shelves of a Japanese grocery shop with plain unlabeled drink bottles and sweets, and in front a few plain white capsules in a small dish", KT),
 't2e': ("one single plain white capsule on the left and a long row of many teacups filled with tea on the right, a balance scale between them", KT),
 't2f': ("a surprised young woman holding a plain white capsule between two fingers and looking at a tea leaf in her other hand, questioning expression", R),
 't2g': ("a clean modern factory hall with shiny steel fermentation tanks and glass columns, a technician in a white coat checking a gauge; a round inset shows tiny rod-shaped bacteria", R),
 # t3 Wie es wirken soll
 't3a': ("a simple side view of a human body silhouette: small golden dots travel from the stomach into red blood vessels; beside it a simple curve that rises quickly and falls again, no numbers", KT),
 't3b': ("a white laboratory rat sitting calmly on a lab bench, above it a simple drawing of a small brain with golden dots entering it", KT),
 't3c': ("scientific illustration of a nerve cell surface with cup-shaped docking sites: a few small golden balls sit loosely in the cups while larger blue balls fit perfectly", KT),
 't3e': ("a person with eyes closed sitting relaxed in a chair wearing an EEG cap with thin wires, soft smooth waves drawn floating above the head", R),
 't3f': ("split picture: on the left a person resting with eyes closed and large smooth waves above the head, on the right the same person concentrating at a desk with small flat waves above the head", R),
 't3g': ("a very small group of eight volunteers sitting in a tiny room for a study, a researcher with a clipboard, in the background a large tea factory visible through the window", R),
 't3h': ("a strip of paper with smooth wave lines coming out of a measuring device, beside it a person shrugging with a neutral questioning expression", R),
 # t4 Stress, Schlaf und Angst
 't4a': ("three simple pictograms side by side as watercolor vignettes: a person relaxing in an armchair, a crescent moon over a bed, a person focused at a desk with a lamp", R),
 't4b': ("a researcher at a large desk stacking many scientific papers into one tall neat pile, a magnifying glass in her hand", R),
 't4c': ("a student before an exam at a desk with a stressed face, and beside her the same student slightly calmer; the difference is small", R),
 't4d': ("two groups of people sitting on chairs, both groups look equally relaxed, between them a level balance scale, a calendar with four plain rows on the wall", R),
 't4e': ("a person waking up in bed in the morning, stretching and looking a little more rested, soft sunlight through the curtains", R),
 't4f': ("a sleep laboratory: a sleeping person in bed with a few sensors, a monitor showing uneven wavy lines; on the bedside table several different plain capsules and tablets mixed in a dish", R),
 't4g': ("a worried person sitting on a sofa hugging a cushion, a doctor sitting opposite listening kindly, two identical plain white capsules on the table", R),
 # t5 Konzentration, Koffein und mehr
 't5a': ("a cup of tea in the center; from it rise two friendly symbols: a roasted coffee bean on the left and a green tea leaf on the right, connected by a soft arc", KT),
 't5b': ("a young man at a computer doing an attention test with colored shapes on the screen, looking alert, a cup of tea beside him", R),
 't5c': ("a large tea company headquarters with tea chests and a delivery truck in the foreground; a paved path leads from the company straight to a small university laboratory building where two researchers in lab coats stand at the door", R),
 't5d': ("a hand pressing a large button in a reaction test, beside it a stopwatch; one side of the picture has a fast hare and the other a slow tortoise", KT),
 't5e': ("a hand holding a coffee cup that trembles slightly with small motion lines, beside it a blood pressure cuff on an arm with a simple dial", KT),
 't5f': ("five children sitting on small chairs in a row in a bright room, a friendly researcher kneeling in front of them with a clipboard", R),
 't5g': ("a psychiatrist and a patient in a calm consulting room; on the desk a plain pill box and beside it one single plain white capsule", R),
 't5h': ("five large round watercolor medallions arranged in two rows filling the whole picture, each with one big simple pictogram: a heart, a shield, a bathroom scale, an elderly head in profile with eye, nose and mouth, a round cell; a small grey question mark shape beside each", KT),
 't5i': ("an older woman sitting comfortably by a window with a cup of tea in her hands, calm smile, a cat on the windowsill", R),
 # t6 Was Behörden sagen
 't6a': ("a simple world map in watercolor with four spots softly highlighted: Europe, North America, Canada and Japan, each marked by a small plain flagless pin", KT),
 't6b': ("a panel of five experts at a long table in a European office reviewing stacks of papers, one of them shaking her head gently", R),
 't6c': ("a plain white supplement box without any writing, a large empty speech bubble above it crossed out with a red line", KT),
 't6d': ("a plain modern three-storey German government office building with flat roof and many windows, a small federal eagle emblem without text beside the entrance; in the foreground a plain drink bottle without label stands behind a red and white barrier", KT),
 't6e': ("a businessman in a suit proudly stamping his own document with a big round stamp, while an official at a desk behind him just looks on with folded hands", R),
 't6f': ("a red maple leaf in the background, in front a person sitting relaxed in an armchair with a calm face and a plain white box without writing on a side table", R),
 't6g': ("four different plain rubber stamps standing in a row on a desk, and behind them a large grey question mark shape drawn on paper", KT),
 # t7 Selbstanwendung: was kritisch ist
 't7a': ("a person at a kitchen table looking thoughtfully at a laptop showing an online shop with plain unlabeled white jars, hand on chin", R),
 't7b': ("a group of relaxed study volunteers chatting with a doctor who gives a thumbs up, bright room", R),
 't7c': ("a wall calendar with only the first few pages colored and a long row of blank grey pages fading into fog, a small hourglass in front", KT),
 't7d': ("two plain pill boxes without labels next to each other with a red zigzag lightning bolt between them, a crescent moon and a pillow in the background", KT),
 't7e': ("a pregnant woman and a mother with a baby in her arms sitting together on a bench, and a child playing beside them, a soft grey question mark shape above", R),
 't7f': ("two identical molecule models facing each other like mirror images with a mirror between them, a laboratory scale and six plain white jars without labels behind", KT),
 't7g': ("a tired person sitting on the edge of the bed at night, looking up with a weary face that is fully visible, hands resting on the knees; through the open door a friendly doctor is waiting in warm light", R),
 't7h': ("a woman doctor and a young man sitting at a desk in a friendly conversation, a plain white jar without label on the desk, bright modern consulting room", R),
 # t8 Fazit
 't8a': ("a winding path through a landscape like a journey: shaded Japanese tea fields at the start, then an old laboratory, a modern factory, and a single plain white capsule at the end", KT),
 't8b': ("a relaxed person at a desk with a cup of tea, working calmly and attentively, a small coffee bean and a tea leaf lying beside the cup", R),
 't8c': ("a scientist looking through a large magnifying glass at a small pile of question marks drawn as simple shapes, curious expression", R),
 't8d': ("a doctor and a patient sitting together at a desk, smiling, a pot of green tea and two cups between them, warm soft light", R),
}
KACHEL = {
 'k1': ("a Japanese scientist around 1949 in a white lab coat and round glasses holding up a glass dish with green tea leaves, tea fields visible through the window", R),
 'k2': ("a fresh green tea leaf on the left turning into a single plain white capsule on the right, a small factory in the soft background", KT),
 'k3': ("a human head in profile with a softly glowing brain and smooth gentle waves flowing out of it, a tea leaf floating nearby", R),
 'k4': ("two researchers at a table with stacks of papers, a balance scale and a laptop with plain bar shapes, discussing calmly", R),
 'k5': ("an official at a desk with a large round rubber stamp, files and a plain white box without writing in front of him, a simple world map on the wall", R),
 'k6': ("a person at a kitchen table thoughtfully looking at a plain white jar without label, a cup of tea beside it, cautious mood", R),
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
