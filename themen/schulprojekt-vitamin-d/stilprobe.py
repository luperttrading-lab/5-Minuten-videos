"""Stilprobe fürs Schulprojekt: dasselbe Motiv in sechs Bildstilen (GPT Image 2 über werkzeug/bilder.py)."""
import sys, os, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'werkzeug'))
import bilder

MOTIV = ("a young woman in a t-shirt and shorts sitting relaxed on a park bench in bright midday summer sun, "
         "a big sun high in the sky, a short shadow under the bench, tiny glowing golden sparks rising from the "
         "sunlit skin of her arms and legs, and exactly one short label reading 'Vitamin D' next to the sparks")
GEMEINSAM = (" Wide 16:9 landscape composition for a phone screen: the main motif is large and fills most of the frame, "
             "few big clearly readable elements, nothing cut off at the edges. The only text in the image is the single "
             "label 'Vitamin D', spelled exactly like that. No other text, no logos.")
STILE = {
 'a_kreide': 'Chalk drawing on a dark green school blackboard, white and pastel chalk lines, slightly smudged, hand-drawn explanatory sketch like a good teacher draws it, handwritten chalk label.',
 'b_vektor': 'Modern flat vector illustration, bold simple geometric shapes, vibrant warm colors on a deep navy background, soft gradients and a subtle glow, clean and friendly science explainer look, label in a clean bold sans-serif font.',
 'c_papier': 'Layered cut-paper diorama, handcrafted 3D paper art with visible paper layers and soft shadows, warm bright colors, photographed in soft studio light, playful and tactile, label cut out of paper.',
 'd_knete': 'Claymation style 3D scene, figure and objects sculpted from colorful modeling clay with a visible fingerprint texture, soft studio lighting, cheerful, shallow depth of field, label made of clay letters.',
 'e_isometrisch': 'Isometric 3D illustration of a tiny diorama world on a floating square piece of ground, soft pastel colors, smooth rounded shapes, gentle soft lighting, clean and cute, label on a small clean sign.',
 'f_lehrtafel': 'Vintage 1950s school wall chart illustration, lithographic print look, muted mustard, teal, brick red and cream colors, fine line work, educational poster aesthetic, label in classic serif lettering.',
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
    json.dump({'motiv': MOTIV, 'gemeinsam': GEMEINSAM, 'stile': STILE}, open('stilprobe/prompts.json', 'w'), ensure_ascii=False, indent=1)
