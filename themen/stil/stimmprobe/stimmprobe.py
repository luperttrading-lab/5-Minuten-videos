#!/usr/bin/env python3
"""Stimmprobe für die Videoreihe: derselbe Abschnitt (Guanfacin, Szene 3) mit mehreren ElevenLabs-Stimmen.

Aufruf: python3 stimmprobe.py [ausordner]. Kandidaten aus dem Seneca-Duell (seneca-audio/messung/stimmen, Runde 1 und 2b):
Plätze 2–4 der Endrunde (Alexander, Marko, Marcus), dazu Leo Liest (Runde 1 vorn) und die aktuelle Stimme Christian.
Helmut Stieglbauer bleibt Seneca vorbehalten. Gleiche Einstellungen wie render.py (eleven_v4, Stimm-Standard), danach
alle auf −16 LUFS (wie das Video), damit Lautstärke den Vergleich nicht verzerrt. Ton-Cache in tts_cache/.
"""
import json, os, subprocess, sys
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', '..', '..', 'werkzeug'))
import render  # noqa: E402

STIMMEN = [
    ('christian', 'NBqeXKdZHweef6y0B67V', 'Christian – Warm and Captivating', 'aktuelle Stimme der Reihe; Seneca-Duell Runde 1: 59 %, Platz 9 von 25'),
    ('alexander', 'kkJxCnlRCckmfFvzDW5Q', 'Alexander – Deep TV Narrator', 'Seneca-Duell Runde 1: 81 % (Platz 1), Runde 2b: 71 % (Platz 2), Endrunde'),
    ('marko', 'PTDRoXRJnOXDLIs03WqF', 'Marko – Gentle and Quiet', 'Runde 1: 68 %, Runde 2b: 69 % (Platz 3), Endrunde'),
    ('marcus', 'mN2MS5qHVRhNpqcfTpaV', 'Marcus – Emphatic and Reflective', 'Runde 1: 69 %, Runde 2b: 56 % (Platz 4), Endrunde'),
    ('leo', '9T2VzpdyzVPMLIjcYVqp', 'Leo Liest – Deep and calm', 'Runde 1: 81 % (Platz 2), Runde 2b: 42 %'),
]
szenen = json.load(open(os.path.join(HIER, '..', '..', 'guanfacin', 'szenen.json'), encoding='utf-8'))
say = lambda s: s if isinstance(s, str) else s['say']
TEXT = ' '.join(say(s) for s in szenen['scenes'][3]['sentences'][:5])

aus = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, 'seite')
os.makedirs(os.path.join(aus, 'audio'), exist_ok=True)
cache = os.path.join(HIER, 'tts_cache'); os.makedirs(cache, exist_ok=True)
ergebnis = []
for key, vid, name, notiz in STIMMEN:
    mp3, al = render.tts_eleven(TEXT, {'voice_id': vid, 'model': 'eleven_v4'}, cache)
    ziel = os.path.join(aus, 'audio', key + '.mp3')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
                    '-ar', '44100', '-ac', '1', '-b:a', '128k', ziel], check=True)
    ende = al['character_end_times_seconds'][-1]; anfang = next(t for c, t in zip(al['characters'], al['character_start_times_seconds']) if c.strip())
    woerter = len(TEXT.split())
    f0 = None
    try:
        import parselmouth
        p = parselmouth.Sound(mp3).to_pitch(pitch_floor=60, pitch_ceiling=250)
        v = [x for x in p.selected_array['frequency'] if x > 0]; v.sort(); f0 = round(v[len(v) // 2], 1) if v else None
    except Exception as e:
        print('F0 nicht gemessen:', e)
    ergebnis.append({'key': key, 'id': vid, 'name': name, 'notiz': notiz, 'datei': f'audio/{key}.mp3',
                     'dauer': round(ende, 2), 'wps': round(woerter / (ende - anfang), 2), 'f0': f0,
                     'video_min': round(750 / (woerter / (ende - anfang)) / 60 + 0.45, 2)})
    print(f"{name}: {ende:.1f} s, {woerter / (ende - anfang):.2f} W/s, F0 {f0} Hz")
json.dump({'text': TEXT, 'stimmen': ergebnis}, open(os.path.join(aus, 'stimmen.json'), 'w'), ensure_ascii=False, indent=1)
