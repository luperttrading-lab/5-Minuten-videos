"""Bilder fürs Erklärvideo „DMSO: Vom Lösungsmittel zum Kälteschutz“, nur Stil G (Aquarell und Tusche).
Erzeuger und Regeln wie themen/pea/bilder_bau.py. Szenenbilder 5:4 (1280x1024), Kacheln 16:9 (2048x1152), GPT Image 2.
Zusatzregel DMSO (Auftrag): niemand trinkt, reibt sich ein oder spritzt; keine Flaschen mit Dosierangaben.
Fehler je Bild in bilder.log, Kosten in bilder_kosten.json. Aufruf: python3 bilder_bau.py   (NUR=d1a,k1 für Einzelne)"""
import sys, os, json, time
from concurrent.futures import ThreadPoolExecutor
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', 'schulprojekt-vitamin-d', 'erklaervideo'))
sys.path.insert(0, os.path.join(HIER, '..', '..', 'werkzeug'))
import bilder_bau as BB

STIL = BB.STILE['G']
FORMAT = ' Landscape 5:4 composition: the main motif is large, centered and fills most of the frame, nothing important at the edges.'
KT = BB.KEIN_TEXT + ' Absolutely no words or letters anywhere, not on signs, books, screens, posters, boxes, bottles or labels.'
GESICHT = ' Every visible face has clearly drawn eyes, nose and mouth and a friendly natural expression. Nobody drinks, swallows, rubs anything on their skin or injects anything.'
R = KT + GESICHT

SZENE = {
 # d1 Ein Stoff aus dem Labor (1860er)
 'd1a': ("a 19th-century chemistry laboratory with wooden shelves, glass retorts, a small flame burner and daylight from a tall window", KT),
 'd1b': ("a 19th-century chemist with a beard and a waistcoat carefully pouring a liquid from one glass flask into another, holding his nose slightly, curious expression", R),
 'd1c': ("an old leather-bound scientific journal lying open on a wooden desk next to a small glass vial with a perfectly clear liquid, quill and inkwell", KT),
 'd1d': ("a simple friendly ball-and-stick molecule model: one large yellow sulfur ball in the middle, one red oxygen ball on top, two small grey carbon balls with tiny white hydrogen balls on the sides", KT),
 'd1e': ("a large paper mill by a river with stacked logs of wood in front, steam rising, rolls of paper", KT),
 'd1f': ("a glass flask in a refrigerator: the clear liquid inside has turned into white crystals, small frost on the glass", KT),
 # d2 Kälteschutz für Zellen (1959)
 'd2a': ("two British scientists in white lab coats in a 1950s laboratory, one man and one woman, looking at a frosty glass tube they hold up together", R),
 'd2b': ("inside view: round red blood cells being pierced by sharp jagged ice crystals, cold blue light", KT),
 'd2c': ("round healthy red blood cells floating calmly in a cold blue liquid, protected by a soft golden glow, few small harmless ice crystals far away", KT),
 'd2d': ("a modern cryo laboratory: a technician in gloves lifts a rack of small plain tubes out of a tank with white cold vapor", R),
 'd2e': ("a patient resting in a hospital bed with a calm expression, a nurse checking the drip stand, bright room", R),
 'd2f': ("a large steel cryo tank with white cold vapor flowing out, next to it a smiling doctor talking with a recovered patient", R),
 # d3 Der große Hype (1960er)
 'd3a': ("a 1960s surgeon in a white coat and a chemist in a suit and tie talking excitedly at a lab bench, a misty Oregon forest visible through the window", R),
 'd3b': ("a simple cross-section diagram of human skin in layers, small blue droplets passing quickly from the surface down through all layers, carrying tiny colored particles along", KT),
 'd3c': ("a 1960s newsstand with many plain newspapers without readable text, a crowd of excited people in 1960s clothes gathering around it", R),
 'd3d': ("a long queue of people in 1960s clothes waiting in front of a pharmacy, some with a bandaged ankle or an arm in a sling", R),
 'd3e': ("a veterinarian in a 1960s lab gently examining the eyes of a calm beagle dog with a small lamp", R),
 'd3f': ("a closed laboratory door with a big red stop barrier in front of it, papers lying on the floor, 1960s setting", KT),
 'd3g': ("a large magnifying glass over a close-up of a healthy human eye in profile, calm mood, soft light", KT),
 # d4 Wofür es zugelassen ist
 'd4a': ("a small green sprout growing out of an old closed science book on a desk, morning light", KT),
 'd4b': ("a female urologist in a white coat explaining a simple anatomical model of a bladder to a woman patient at a desk, friendly atmosphere", R),
 'd4c': ("two groups of patients in a waiting room, the group on the left looks noticeably more relaxed and content than the group on the right", R),
 'd4d': ("a hospital oncology ward: a nurse gently places a cool compress on the forearm of a seated patient next to a drip stand", R),
 'd4e': ("an alpine landscape with snowy mountains, in front a simple plain tube of gel without any label and a soft bandage on a wooden table", KT),
 'd4f': ("a pharmacist in a modern German pharmacy carefully mixing an ointment with a pestle and a glass plate in the back room", R),
 'd4g': ("an old 1980s pharmacy counter with a small plain ointment tube without label; beside it a round inset shows small blue droplets carrying a little golden particle down into skin layers", KT),
 'd4h': ("a veterinarian in a stable kindly examining the foreleg of a brown horse, a friendly dog sitting nearby", R),
 # d5 Was Studien zeigen
 'd5a': ("a long scroll of paper unrolled across a table with many small simple pictograms (joint, bladder, cell, skin), a researcher looking at it thoughtfully", R),
 'd5b': ("a doctor carefully examining the swollen red hand of a seated patient, warm consulting room", R),
 'd5c': ("two small identical plain unlabeled cream jars on a table, a balance scale between them perfectly level", KT),
 'd5d': ("an older man sitting on a park bench, holding his knee, mildly uncomfortable expression, autumn leaves", R),
 'd5e': ("a researcher in a lab coat sniffing the air with a surprised expression, a small cartoon cloud of garlic bulbs floating nearby, a blindfold lying on the table", R),
 'd5f': ("a stack of old yellowed scientific papers and a few small notebooks on a dusty archive desk, a magnifying glass on top", KT),
 'd5g': ("a jogger sitting on a running track holding her ankle, another runner talking to her, sunny day", R),
 'd5h': ("a petri dish under a lab lamp: small glowing medicine particles go dark and dull when touched by clear drops, scientific illustration", KT),
 # d6 Selbstanwendung: was kritisch ist
 'd6a': ("a person at a kitchen table looking thoughtfully at a laptop showing an online shop with plain unlabeled bottles, hand on chin", R),
 'd6b': ("a simple cross-section of skin layers: small blue droplets carry little dark dirt particles and colorful paint flecks down through the skin, warning red tint", KT),
 'd6c': ("a large industrial metal drum and plain chemical canisters in a warehouse, a big red warning triangle without any text painted on the wall", KT),
 'd6d': ("a forearm with a red irritated patch of skin, beside it a small cartoon cloud of garlic bulbs, clinical illustration", KT),
 'd6e': ("two plain pill boxes without labels next to each other with a red zigzag lightning bolt between them, a simple nerve drawn like a branching tree in the background", KT),
 'd6f': ("a plain empty drinking glass on a table with a large red crossed-out circle drawn over it, no liquid inside", KT),
 'd6g': ("a large red stop hand in front of a plain dark brown glass bottle without label and a yellow chemical hazard pictogram of a skull without text", KT),
 'd6h': ("a woman doctor and a young man sitting at a desk in a friendly conversation, a plain pill box on the desk, bright modern consulting room", R),
 # d7 Fazit
 'd7a': ("a winding path through a landscape like a journey: an old 19th-century glass flask at the start, then a paper mill, a frosty cryo tank, a hospital and a doctor at the end", KT),
 'd7b': ("a female urologist and a patient shaking hands warmly in a bright consulting room", R),
 'd7c': ("a scientist looking through a large magnifying glass at a small pile of question marks drawn as simple shapes, curious expression", R),
 'd7d': ("a doctor and a patient sitting together at a desk, smiling, warm soft light", R),
}
KACHEL = {
 'k1': ("a 19th-century chemist with a beard in his laboratory holding up a glass flask with a perfectly clear liquid against the window light", R),
 'k2': ("a modern cryo laboratory: a scientist in gloves lifts a rack of small plain tubes out of a steel tank, white cold vapor swirling", R),
 'k3': ("a 1960s crowd of enthusiastic people and press photographers with old flash cameras around a smiling surgeon in a white coat", R),
 'k4': ("a woman doctor in a hospital explaining something to a patient, and in the background a veterinarian with a brown horse visible through a window", R),
 'k5': ("two researchers comparing two plain unlabeled cream jars on a lab bench, a balance scale between them, papers and a microscope", R),
 'k6': ("a person at a kitchen table thoughtfully looking at a plain unlabeled brown glass bottle, a doctor in a small framed picture on the wall behind, cautious mood", R),
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
