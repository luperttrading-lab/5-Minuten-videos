#!/usr/bin/env python3
"""Aquarellbilder pro Szene ueber Abacus RouteLLM (Nano Banana 2.1).

Aufruf: python3 bilder.py szenen.json [--nur ID ...] [--neu]
Jede Szene mit `bild_prompt` bekommt das Bild, das ihr erster Ausschnitt unter `bild` erwartet
(z. B. bilder/m1.png). Vorhandene Dateien bleiben, ausser mit --neu. Schluessel: ABACUS_API_KEY.
Kosten: usage.compute_points_used / 100 = Credits.
"""
import argparse, base64, json, os, sys, urllib.request

STIL = ('Ink and watercolor illustration on warm textured paper, loose expressive ink lines, soft washes, '
        'limited palette of dove blue, terracotta, ochre and sage, generous empty paper margins, calm and friendly. '
        'Absolutely no text, no letters, no numbers, no labels, no logos anywhere in the image. Aspect ratio 16:9 landscape.')
URL = 'https://routellm.abacus.ai/v1/chat/completions'


def erzeuge(prompt, ziel):
    body = {'model': 'gemini-nano-banana-2.1', 'modalities': ['image', 'text'],
            'image_config': {'aspect_ratio': '16:9'},
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
    a = ap.parse_args()
    basis = os.path.dirname(os.path.abspath(a.szenen))
    cfg = json.load(open(a.szenen, encoding='utf-8'))
    summe = 0.0
    for sc in cfg['scenes']:
        p = sc.get('bild_prompt')
        ziel = next((sh['bild'] for sh in sc.get('shots', []) if sh.get('bild')), None)
        if not p or not ziel or (a.nur and sc['id'] not in a.nur):
            continue
        pfad = os.path.join(basis, ziel)
        if os.path.exists(pfad) and not a.neu:
            print(f"{sc['id']}: vorhanden, {ziel}")
            continue
        try:
            c = erzeuge(p, pfad)
        except Exception as e:                      # ein Fehlschlag soll die anderen Bilder nicht stoppen
            print(f"{sc['id']}: FEHLER {e}", file=sys.stderr)
            continue
        summe += c
        print(f"{sc['id']}: {ziel}  {c:.1f} Credits")
    print(f'Summe: {summe:.1f} Credits')


if __name__ == '__main__':
    main()
