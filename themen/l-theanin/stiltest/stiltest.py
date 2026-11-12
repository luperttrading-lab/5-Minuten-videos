"""Stiltest 12.11.: drei Abwandlungen von Stil G (Aquarell und Tusche) an drei Motiven des L-Theanin-Videos.
Aufruf: python3 stiltest.py"""
import sys, os, json
from concurrent.futures import ThreadPoolExecutor
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', '..', 'schulprojekt-vitamin-d', 'erklaervideo'))
sys.path.insert(0, os.path.join(HIER, '..', '..', '..', 'werkzeug'))
import importlib.util
spec = importlib.util.spec_from_file_location('lt_bilder', os.path.join(HIER, '..', 'bilder_bau.py'))
LT = importlib.util.module_from_spec(spec); spec.loader.exec_module(LT)   # Motive und Regeln des L-Theanin-Videos
BB = LT.BB
STILE = {
 'A': "Loose wet-on-wet watercolor painting on warm textured off-white paper: flowing transparent washes with visible pigment blooms, soft bleeding edges and drips, only a few light sketchy ink lines, little detail, the motif fades into large areas of unpainted paper at the edges like a vignette. Dusty blue, terracotta, ochre and sage green.",
 'B': "Ink and watercolor illustration on warm textured off-white paper, loose expressive black ink lines, mostly pale muted washes of grey-blue and ochre, with ONE strong luminous accent color, a vivid fresh tea green, used only on the most important element; generous unpainted paper around the motif, calm editorial magazine style.",
 'C': "Bold expressive urban-sketch style in ink and watercolor on warm textured off-white paper: confident thick-and-thin brush-pen lines, dramatic light and shadow, strong diagonal composition and an unusual close viewpoint, lively paint splashes and spatters, saturated terracotta, deep blue, ochre and sage green.",
}
MOTIVE = ['t1b', 't3c', 't5i']


def eins(job):
    s, k = job
    ziel = os.path.join(HIER, f'{s}_{k}.jpg')
    if os.path.exists(ziel):
        return 0.0
    motiv, regel = LT.SZENE[k]
    try:
        return BB.erzeuge(STILE[s] + LT.FORMAT + regel, motiv, ziel, config={'size': '1280x1024'})
    except Exception as e:
        print('FEHLER', s, k, e.read()[:200] if hasattr(e, 'read') else str(e)[:200]); return 0.0


with ThreadPoolExecutor(9) as ex:
    c = list(ex.map(eins, [(s, k) for s in STILE for k in MOTIVE]))
print('Credits', round(sum(c), 1))
