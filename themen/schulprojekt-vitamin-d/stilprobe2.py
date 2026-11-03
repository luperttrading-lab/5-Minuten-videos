"""Stilprobe Teil 2 fürs Schulprojekt: dasselbe Motiv in sechs weiteren Bildstilen (G–L), GPT Image 2 über werkzeug/bilder.py.
Motiv und gemeinsamer Prompt unverändert aus stilprobe.py, damit nur der Stil sich unterscheidet."""
import sys, os, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'werkzeug'))
import bilder
from stilprobe import MOTIV, GEMEINSAM

STILE = {
 'g_aquarell': 'Ink and watercolor illustration on warm textured off-white paper, loose expressive black ink lines, soft washes of dusty blue, terracotta, ochre and sage green, calm editorial magazine style, label hand-lettered in ink.',
 'h_comic': 'Clean-line European comic book style (ligne claire), bold uniform black outlines, flat bright colors, simple shading, a single comic panel with a thin black border, label in hand-lettered comic font.',
 'i_trickfilm': '3D animated feature film style, appealing stylized characters with large expressive eyes, soft subsurface skin, warm cinematic lighting, rich colors, polished family movie look, label on a small wooden sign.',
 'j_heft': 'Sketchnote doodle drawn with blue ballpoint pen and a few colored markers on squared school notebook paper, playful hand-drawn arrows and little stars, like a good student summary page, handwritten label.',
 'k_blaupause': 'Technical blueprint drawing, fine white construction lines on deep blueprint blue paper, precise outlines, dimension arrows and grid, scientific schematic look, label in white technical stencil lettering.',
 'l_pixel': 'Retro 16-bit pixel art like a classic video game scene, crisp visible pixels, limited bright palette, chunky clouds and trees, label in a blocky pixel font.',
}

def eins(k):
    bilder.STIL = STILE[k] + GEMEINSAM
    return k, bilder.erzeuge(MOTIV, f'stilprobe/{k}.png')

if __name__ == '__main__':
    with ThreadPoolExecutor(6) as ex:
        erg = list(ex.map(eins, STILE))
    for k, c in erg:
        print(f'{k}: {c:.1f} Credits')
    print('Summe:', round(sum(c for _, c in erg), 1))
    json.dump({'motiv': MOTIV, 'gemeinsam': GEMEINSAM, 'stile': STILE}, open('stilprobe/prompts2.json', 'w'), ensure_ascii=False, indent=1)
