#!/usr/bin/env python3
"""Klangprobe für Tempo und Tonlage der Sprecherstimme (Nutzerwunsch 02.11.): zwei Ausschnitte aus dem fertigen
Guanfacin-Ton (aufbereitet), je Tonlage eine vorab berechnete Fassung (Rubber Band, Formanten erhalten, Tempo bleibt).
Das Tempo regelt die Seite live (playbackRate mit erhaltener Tonhöhe). Aufruf: python3 klangprobe.py [ausordner]
"""
import json, os, subprocess, sys
HIER = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(HIER, '..', '..', 'guanfacin')
aus = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, 'seite')
os.makedirs(os.path.join(aus, 'audio'), exist_ok=True)
zp = {z['id']: z for z in json.load(open(os.path.join(G, 'video_zeitplan.json')))}
g3 = zp['g3']['st']
AUSSCHNITTE = {'einstieg': (0.0, 24.0, 'Einstieg (0:00–0:24)'),
               'fachteil': (g3[0][0] - 0.3, g3[3][0] + g3[3][1] + 0.3, 'Fachteil: Wie gut wirkt es? (Szene 3)')}
STUFEN = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
for key, (a, b, _) in AUSSCHNITTE.items():
    for ht in STUFEN:
        af = f'rubberband=pitch={2 ** (ht / 12):.6f}:formant=preserved:pitchq=quality' if ht else 'anull'
        ziel = os.path.join(aus, 'audio', f'{key}_{ht:+.1f}.mp3')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.2f}', '-to', f'{b:.2f}', '-i', os.path.join(G, 'video.wav'),
                        '-af', af + ',afade=t=in:d=0.05', '-ac', '1', '-b:a', '96k', ziel], check=True)
json.dump({'ausschnitte': {k: v[2] for k, v in AUSSCHNITTE.items()}, 'stufen': STUFEN},
          open(os.path.join(aus, 'klangprobe.json'), 'w'), ensure_ascii=False)
print('fertig', len(STUFEN) * len(AUSSCHNITTE), 'Dateien')
