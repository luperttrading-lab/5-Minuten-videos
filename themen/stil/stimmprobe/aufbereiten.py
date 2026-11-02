#!/usr/bin/env python3
"""Aufbereitung der Stimmprobe nach der Seneca-Kette (seneca-audio/werkzeuge/kette.py): Rauschunterdrückung
(highpass 60 Hz, anlmdn, sanftes Gate, Versatz von anlmdn ausgeglichen), De-Esser gegen Zischen, dann lineare
Verstärkung auf −16 LUFS mit Limiter statt dynamischem loudnorm (das hob bei Christian das Grundrauschen auf −50 dB).
Eine einzige MP3-Kodierung mit 192 kbit/s. Aufruf: python3 aufbereiten.py [seitenordner]."""
import json, os, re, subprocess, sys
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', '..', '..', 'werkzeug'))
import render  # noqa: E402
RAUSCH = ("highpass=f=60,anlmdn=s=0.0007,agate=threshold=0.01:ratio=3:range=0.15:attack=5:release=200:knee=6:detection=rms,"
          "atrim=start_sample=353,apad=pad_len=353")
KETTE = RAUSCH + ",deesser=i=0.5:m=0.5:f=0.5"
ff = lambda *a: subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', *a], check=True)

def lufs(f):
    o = subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-i', f, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1])

aus = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, 'seite')
daten = json.load(open(os.path.join(aus, 'stimmen.json'), encoding='utf-8'))
cache = os.path.join(HIER, 'tts_cache')
for s in daten['stimmen']:
    mp3, _ = render.tts_eleven(daten['text'], {'voice_id': s['id'], 'model': 'eleven_v4'}, cache)
    tmp = os.path.join(aus, 'audio', s['key'] + '.tmp.wav')
    for art, kette in (('roh', 'anull'), ('auf', KETTE)):
        ff('-i', mp3, '-af', kette, '-ar', '44100', '-ac', '1', tmp)
        g = -16 - lufs(tmp)
        ziel = os.path.join(aus, 'audio', f"{s['key']}_{art}.mp3")
        ff('-i', tmp, '-af', f'volume={g:.2f}dB,alimiter=limit=0.84:level=disabled', '-ar', '44100', '-ac', '1', '-b:a', '192k', ziel)
        s['datei_' + art] = f"audio/{s['key']}_{art}.mp3"
    os.remove(tmp)
    print(s['key'], 'ok')
json.dump(daten, open(os.path.join(aus, 'stimmen.json'), 'w'), ensure_ascii=False, indent=1)
