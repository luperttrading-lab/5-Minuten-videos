"""Bilder fürs Erklärvideo „PEA: Vom Eigelb zur Schmerzforschung“ in drei Stilen (Nutzerwunsch 09.11.: 3D, Aquarell, Knete).
Stiltexte, Erzeuger und Regeln aus themen/schulprojekt-vitamin-d/erklaervideo (bilder_bau.py, bilder_v2.py).
Szenenbilder 5:4 (1280x1024), Kacheln 16:9 (2048x1152), GPT Image 2 über ChatLLM. Fehler je Bild werden protokolliert
(bilder.log), Kosten je Bild in bilder_kosten.json. Aufruf: python3 bilder_bau.py [STIL ...]"""
import sys, os, json, time
from concurrent.futures import ThreadPoolExecutor
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', 'schulprojekt-vitamin-d', 'erklaervideo'))
sys.path.insert(0, os.path.join(HIER, '..', '..', 'werkzeug'))
import bilder_bau as BB

STILE = {k: BB.STILE[k] for k in ('I', 'G', 'D')}
FORMAT = ' Landscape 5:4 composition: the main motif is large, centered and fills most of the frame, nothing important at the edges.'
KT = BB.KEIN_TEXT + ' Absolutely no words or letters anywhere, not on signs, books, screens, posters, boxes, bottles or labels.'
GESICHT = ' Every visible face has clearly drawn eyes, nose and mouth and a friendly natural expression.'
HAUT = ' Smooth clean natural skin without spots, dots, sparkles or speckles. Whole figures, no skin close-ups.'
R = KT + GESICHT
RH = KT + GESICHT + HAUT

SZENE = {
 # p1 Das Eigelb-Rätsel (1940er)
 'p1a': ("a New York street in the 1940s with brownstone houses and old cars, children playing on the sidewalk", R),
 'p1b': ("a 1940s hospital room: a child with fever lying in bed, a caring mother beside the bed, a doctor listens to the child's chest with a stethoscope", RH),
 'p1c': ("a 1940s doctor in a white coat sitting at a wooden desk, thoughtfully looking at a cracked egg in a bowl with a bright yellow yolk", RH),
 'p1d': ("children in a 1940s children's home sitting cheerfully at a long table, a nurse serves bowls of yellow egg yolk pudding", RH),
 'p1e': ("a cute healthy guinea pig eating from a little bowl of food mixed with egg yolk in a clean bright lab enclosure, a scientist watches kindly", R),
 'p1f': ("a magnifying glass held over a glowing golden egg yolk in a bowl, mysterious warm light, a sense of discovery", KT),
 # p2 Der Stoff wird gefunden (1957)
 'p2a': ("two chemists, a man and a woman, in white coats in a large 1950s pharmaceutical laboratory full of glassware", RH),
 'p2b': ("on a lab bench: a glass dish with egg yolk, a bowl of soybeans and a bowl of peanuts, each connected by glass tubes to one central flask", KT),
 'p2c': ("a 1950s chemist proudly holding up a glass flask in which fine white crystals sparkle", RH),
 'p2d': ("a simple friendly ball-and-stick molecule model: a long zigzag chain of balls linked to a small round building block, a palm fruit beside it", KT),
 'p2e': ("a friendly adult standing relaxed, a soft translucent overlay shows small golden glows in many places of the body", RH),
 'p2f': ("a happy healthy guinea pig hopping in a bright lab enclosure, a 1950s scientist in a white coat smiles at it", R),
 # p3 Eine Grippetablette (1970er)
 'p3a': ("a 1970s Central European town square in winter with an old tram, snow on the roofs, people in warm coats", RH),
 'p3b': ("young soldiers in plain green uniforms standing in a row in a barracks hall, a medic hands out small white pills", RH),
 'p3c': ("two 1970s factory workers in overalls at a workbench, one cheerful and healthy, the other sneezing into a handkerchief", RH),
 'p3d': ("an old-fashioned 1970s pharmacy shelf with one small plain white pill box standing alone, light dust in the air", KT),
 'p3e': ("a scientist in an archive gently blowing dust off a plain unlabeled folder taken from a long shelf", RH),
 'p3f': ("a person resting in bed under a cozy blanket with a cup of tea, a doctor sitting beside the bed talking kindly", RH),
 # p4 Die Nobelpreisträgerin (1990er)
 'p4a': ("an elegant elderly female scientist with white hair in a 1990s laboratory, smiling and talking with a younger colleague next to a microscope", RH),
 'p4b': ("inside the human body: a single round ball-shaped immune cell filled with many small purple granules floats in soft pink human tissue and releases little red sparks; an animal cell, not a plant, not a leaf, no slit", KT),
 'p4c': ("inside the human body: tiny golden droplets settle on a few round ball-shaped immune cells filled with small purple granules in soft pink tissue; the cells look calm and release no more red sparks; animal cells, not plant cells, no slits", KT),
 'p4d': ("a glowing golden brake lever inside a soft pink tissue landscape, gently slowing down a stream of red sparks", KT),
 'p4e': ("a green hemp leaf next to a large lock, a golden key that clearly does not fit the lock", KT),
 'p4f': ("a lively 1990s research team discussing around a table with microscopes and plain papers, full of energy", RH),
 # p5 Wie PEA wirken könnte
 'p5a': ("a modern bright laboratory with palm trees visible through the window, two researchers working with pipettes", RH),
 'p5b': ("inside a cell: a small golden molecule flips a large switch on the cell nucleus, red flames around it dim down", KT),
 'p5c': ("two cute white lab mice in a clean bright cage, one sniffing curiously", KT),
 'p5d': ("two similar friendly ball-and-stick molecules side by side like siblings, one golden and one pink", KT),
 'p5e': ("small scissor-shaped enzymes are distracted by golden molecules, so a pink molecule stays intact, surrounded by its golden companions", KT),
 'p5f': ("a researcher holding a petri dish, a friendly white lab mouse on the bench, thoughtful expression", RH),
 # p6 Was Studien heute zeigen
 'p6a': ("a modern pharmacy shelf with several plain unlabeled white bottles and a few white capsules in front", KT),
 'p6b': ("a person in a bright kitchen holding a plain unlabeled white capsule bottle and looking at it curiously", RH),
 'p6c': ("a middle-aged woman sitting on a sofa, one hand on her lower back, a mildly uncomfortable expression", RH),
 'p6d': ("two researchers with clipboards comparing two small groups of patients sitting on chairs, one group looks a little more relaxed", RH),
 'p6e': ("a small group of six patients in a waiting room, on the table several identical plain unlabeled capsule bottles", RH),
 'p6f': ("two identical white capsules on two small plates, a researcher looks at them with a puzzled expression", RH),
 'p6g': ("a relaxed person taking a white capsule with a glass of water at a sunny breakfast table", RH),
 'p6h': ("a doctor and a patient sitting at a desk in a friendly conversation, a plain unlabeled capsule bottle on the desk", RH),
 # p7 Fazit
 'p7a': ("a winding path through a landscape like a journey: an egg at the start, then a glass flask, a small pill box, a microscope and a capsule at the end", KT),
 'p7b': ("a calm happy person standing in soft light, a gentle golden glow around them", RH),
 'p7c': ("a smiling researcher looking at a small green sprout growing on the lab bench, hopeful mood", RH),
 'p7d': ("a large diverse research team of many people in a bright modern institute, working together", RH),
 'p7e': ("a doctor and a patient shaking hands warmly in a bright consulting room", RH),
}
KACHEL = {
 'k1': ("a 1940s doctor in a white coat kindly hands a bowl with a bright egg yolk to a smiling child sitting in a hospital bed, sunny ward", RH),
 'k2': ("two 1950s chemists, a man and a woman, at a lab bench with glass flasks, an egg, soybeans and peanuts, one flask with glowing white crystals", RH),
 'k3': ("a 1970s pharmacy counter in a snowy Central European town, a pharmacist hands a small plain pill box to a customer in a winter coat and scarf", RH),
 'k4': ("an elegant elderly female scientist with white hair looking through a microscope in a 1990s laboratory, warm light", RH),
 'k5': ("inside a cell: a small golden molecule turns a switch on the cell nucleus, red inflammation sparks turn into calm blue light", KT),
 'k6': ("a doctor and a middle-aged woman patient talking at a desk, a plain unlabeled capsule bottle on the desk, bright modern room", RH),
}
GROESSE = {'szene': {'size': '1280x1024'}, 'kachel': {'size': '2048x1152'}}


def log(text):
    with open(os.path.join(HIER, 'bilder.log'), 'a') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + text + '\n')


def eins(job):
    stil, key, art = job
    ziel = os.path.join(HIER, 'bilder', stil, key + '.jpg')
    if os.path.exists(ziel):
        return stil, key, 0.0
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    motiv, regel = (SZENE if art == 'szene' else KACHEL)[key]
    fmt = FORMAT if art == 'szene' else BB.GEMEINSAM
    try:
        c = BB.erzeuge(STILE[stil] + fmt + regel, motiv, ziel, config=GROESSE[art])
        log(f'ok {stil}/{key} {c:.1f}')
        return stil, key, c
    except Exception as e:
        msg = e.read()[:300] if hasattr(e, 'read') else str(e)[:300]
        log(f'FEHLER {stil}/{key} {msg}')
        print('FEHLER', stil, key, msg, flush=True)
        return stil, key, 0.0


if __name__ == '__main__':
    stile = sys.argv[1:] or list(STILE)
    nur = os.environ.get('NUR')                      # z. B. NUR=p1a,k1 für Tests
    jobs = [(s, k, 'kachel') for s in stile for k in KACHEL] + [(s, k, 'szene') for s in stile for k in SZENE]
    if nur:
        jobs = [j for j in jobs if j[1] in nur.split(',')]
    with ThreadPoolExecutor(8) as ex:
        erg = list(ex.map(eins, jobs))
    pfad = os.path.join(HIER, 'bilder_kosten.json')
    kosten = json.load(open(pfad)) if os.path.exists(pfad) else {}
    for s, k, c in erg:
        if c:
            kosten[f'{s}/{k}'] = round(c, 1)
    json.dump(kosten, open(pfad, 'w'), indent=1, sort_keys=True)
    print('neu erzeugt:', sum(1 for *_, c in erg if c), 'Bilder,', round(sum(c for *_, c in erg), 1), 'Credits; gesamt',
          round(sum(kosten.values()), 1))
    json.dump({'stile': STILE, 'szene': SZENE, 'kachel': KACHEL, 'groesse': GROESSE},
              open(os.path.join(HIER, 'bilder_prompts.json'), 'w'), ensure_ascii=False, indent=1)
