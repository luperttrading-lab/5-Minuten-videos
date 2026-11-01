#!/usr/bin/env python3
"""Aquarellbilder pro Szene ueber Abacus RouteLLM (GPT Image 2, 2048x1152 = 16:9, ≈ 6 Credits pro Bild).

Aufruf: python3 bilder.py szenen.json [--nur DATEI-ODER-ID ...] [--neu] [--modell gpt_image2]
Jede Szene listet ihre Bilder unter `bilder: [{datei, prompt}]` (Pfade relativ zum Drehbuch).
Vorhandene Dateien bleiben, ausser mit --neu. Schluessel: ABACUS_API_KEY.
Kosten: usage.compute_points_used / 100 = Credits. Stil: themen/stil/bildleitfaden.md.
"""
import argparse, base64, json, os, sys, urllib.request

STIL = ('Ink and watercolor illustration on warm textured paper, loose expressive ink lines, soft washes, '
        'limited palette of dove blue, terracotta, ochre and sage, calm and friendly. '
        'Composition for a phone screen: the main motif is large and fills most of the frame, with only a slim margin of plain paper, nothing cut off at the edges; few, big, clearly readable elements, any label large and legible. '
        'Absolutely no text, no letters, no numbers, no labels, no logos, no faces on suns or objects anywhere in the image.')
MODELLE = {'gpt_image2': {'size': '2048x1152'}, 'gpt_image25': {'size': '2048x1152'},
           'gemini-nano-banana-2.1': {'aspect_ratio': '16:9'}}
URL = 'https://routellm.abacus.ai/v1/chat/completions'


def erzeuge(prompt, ziel, modell='gpt_image2'):
    body = {'model': modell, 'modalities': ['image', 'text'],
            'image_config': MODELLE[modell],
            'messages': [{'role': 'user', 'content': f'Generate an image. {STIL} Motif: {prompt}'}]}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={
        'Authorization': 'Bearer ' + os.environ['ABACUS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=240) as r:
        d = json.load(r)
    url = d['choices'][0]['message']['images'][0]['image_url']['url']
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    with open(ziel, 'wb') as f:
        f.write(base64.b64decode(url.split(',', 1)[1]))
    return d.get('usage', {}).get('compute_points_used', 0) / 100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('szenen')
    ap.add_argument('--nur', nargs='*')
    ap.add_argument('--neu', action='store_true')
    ap.add_argument('--modell', default='gpt_image2', choices=list(MODELLE))
    a = ap.parse_args()
    basis = os.path.dirname(os.path.abspath(a.szenen))
    cfg = json.load(open(a.szenen, encoding='utf-8'))
    summe = 0.0
    auftraege = []
    for sc in cfg['scenes']:
        for b in sc.get('bilder', []):
            if not a.nur or sc['id'] in a.nur or b['datei'] in a.nur:
                auftraege.append((sc['id'], b['datei'], b['prompt']))
    for sid, datei, prompt in auftraege:
        pfad = os.path.join(basis, datei)
        if os.path.exists(pfad) and not a.neu:
            print(f'{sid}: vorhanden, {datei}')
            continue
        try:
            c = erzeuge(prompt, pfad, a.modell)
        except Exception as e:                      # ein Fehlschlag soll die anderen Bilder nicht stoppen
            print(f'{sid}: FEHLER {datei}: {e}', file=sys.stderr)
            continue
        summe += c
        print(f'{sid}: {datei}  {c:.1f} Credits')
    print(f'Summe: {summe:.1f} Credits')


if __name__ == '__main__':
    main()
