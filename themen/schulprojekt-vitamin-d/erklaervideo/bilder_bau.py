"""Bilder fürs Erklärvideo „Vitamin D: Das Sonnenhormon“ in acht Stilen (Nutzerwahl 03.11.: C D E G H I J L).
Je Stil dieselben acht Motive, GPT Image 2 über werkzeug/bilder.py. Aufruf: python3 bilder_bau.py [STIL ...]"""
import sys, os, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'werkzeug'))
import bilder
import base64, urllib.request


def erzeuge(stil, motiv, ziel, modell='gpt_image2', config=None):
    """Wie bilder.erzeuge, aber mit dem Stil als Parameter (bilder.STIL ist global, mit Threads sonst ein Wettlauf)."""
    body = {'model': modell, 'modalities': ['image', 'text'], 'image_config': config or bilder.MODELLE[modell],
            'messages': [{'role': 'user', 'content': f'Generate an image. {stil} Motif: {motiv}'}]}
    req = urllib.request.Request(bilder.URL, data=json.dumps(body).encode(), headers={
        'Authorization': 'Bearer ' + os.environ['ABACUS_API_KEY'], 'Content-Type': 'application/json'})
    for versuch in range(3):
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                d = json.load(r)
            break
        except Exception as e:
            if versuch == 2:
                raise
    url = d['choices'][0]['message']['images'][0]['image_url']['url']
    import io
    from PIL import Image
    Image.open(io.BytesIO(base64.b64decode(url.split(',', 1)[1]))).convert('RGB').save(ziel, quality=92, optimize=True)
    return d.get('usage', {}).get('compute_points_used', 0) / 100

# Stile ohne Hinweise auf Etiketten (sonst schreibt das Modell Text in Bilder, die keinen haben sollen)
STILE = {
 'C': 'Layered cut-paper diorama, handcrafted 3D paper art with visible paper layers and soft shadows, warm bright colors, photographed in soft studio light, playful and tactile.',
 'D': 'Claymation style 3D scene, figures and objects sculpted from colorful modeling clay with a visible fingerprint texture, soft studio lighting, cheerful, shallow depth of field.',
 'E': 'Isometric 3D illustration of a tiny diorama world on a floating square piece of ground, soft pastel colors, smooth rounded shapes, gentle soft lighting, clean and cute. The diorama is large and fills most of the frame.',
 'G': 'Ink and watercolor illustration on warm textured off-white paper, loose expressive black ink lines, soft washes of dusty blue, terracotta, ochre and sage green, calm editorial magazine style.',
 'H': 'Clean-line European comic book style (ligne claire), bold uniform black outlines, flat bright colors, simple shading, a single comic panel with a thin black border.',
 'I': '3D animated feature film style, appealing stylized characters with large expressive eyes, soft subsurface skin, warm cinematic lighting, rich colors, polished family movie look.',
 'J': 'Doodle drawn with blue ballpoint pen and a few colored markers on squared school notebook paper, playful hand-drawn arrows and little stars around the scene. The sun has no face.',
 'L': 'Retro 16-bit pixel art like a classic video game scene, crisp visible pixels, limited bright palette, chunky clouds and trees.',
}
GEMEINSAM = (' Wide 16:9 landscape composition for a phone screen: the main motif is large and fills most of the frame, '
             'few big clearly readable elements, nothing cut off at the edges.')
KEIN_TEXT = ' No text, no letters, no numbers, no labels, no logos anywhere in the image.'

def nur(label):
    return (f" The only text in the image is {label}, spelled exactly like that and appearing exactly once. "
            "No other words, letters, numbers or logos anywhere.")

MOTIVE = {
 'e1': ("a person standing outdoors in sunshine, sun rays touch the bare skin of the arm; a glowing golden droplet travels "
        "from the skin along a simple dotted arrow to a stylized liver and then to a kidney, both drawn as simple friendly "
        "shapes floating beside the person", nur("the single label 'Vitamin D' next to the glowing droplet")),
 'e2a': ("a person in swimwear lying relaxed on a towel on a green lawn at midday in strong summer sun, the sun high in the sky, "
         "a very short shadow, lots of bare skin, tiny glowing golden sparks rising from the sunlit skin", KEIN_TEXT),
 'e2b': ("a town street in winter: a low pale sun just above the rooftops, very long shadows on the snow, people in thick coats, "
         "scarves and hats so that only their faces are visible", KEIN_TEXT),
 'e3': ("a blood sample tube with a red cap standing next to a big simple measuring scale with two columns side by side, "
        "a marker line connects the same height on both columns", nur("exactly two labels: '20 ng/ml' on the left column and '50 nmol/l' on the right column")),
 'e4': ("a small plain unlabeled dropper bottle releasing a single golden drop onto a spoon, next to a breakfast with avocado, "
        "boiled eggs and a few nuts, bright morning light", KEIN_TEXT),
 'e5': ("a large friendly crowd of people of all ages seen slightly from above, split into two groups; scientists in white coats "
        "with clipboards stand in front and compare the groups", KEIN_TEXT),
 'e6': ("one scene with four people side by side: a happy baby, an elderly woman in an armchair by a window, a young man with "
        "dark skin, and an office worker at a desk under artificial light", KEIN_TEXT),
 'e7': ("a split scene: on the left half a bright summer park with a person in t-shirt and shorts enjoying the sun, on the right "
        "half a cozy winter kitchen where the same person takes a single golden drop with breakfast", KEIN_TEXT),
}

def eins(job):
    stil, key = job
    ziel = f'bilder/{stil}/{key}.jpg'  # JPEG q92: Repo kleiner (PNG wäre 213 MB)
    if os.path.exists(ziel):
        return stil, key, 0.0
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    motiv, regel = MOTIVE[key]
    return stil, key, erzeuge(STILE[stil] + GEMEINSAM + regel, motiv, ziel)

if __name__ == '__main__':
    stile = sys.argv[1:] or list(STILE)
    jobs = [(s, k) for s in stile for k in MOTIVE]
    with ThreadPoolExecutor(6) as ex:
        erg = list(ex.map(eins, jobs))
    kosten = {}
    if os.path.exists('bilder_kosten.json'):
        kosten = json.load(open('bilder_kosten.json'))
    for s, k, c in erg:
        if c:
            kosten[f'{s}/{k}'] = round(c, 1)
    json.dump(kosten, open('bilder_kosten.json', 'w'), indent=1, sort_keys=True)
    print('neu erzeugt:', sum(1 for _, _, c in erg if c), 'Bilder,', round(sum(c for _, _, c in erg), 1), 'Credits')
    json.dump({'stile': STILE, 'gemeinsam': GEMEINSAM, 'motive': MOTIVE}, open('bilder_prompts.json', 'w'), ensure_ascii=False, indent=1)
