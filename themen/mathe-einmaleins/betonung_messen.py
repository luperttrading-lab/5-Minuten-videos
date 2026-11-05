"""Betonung von „Einerziffer(n)“ in drei Fassungen messen: je Silbe Dauer, Lautstärke (dB) und Tonhöhe (Hz, Praat).
Zeitgrenzen der Silben aus den ElevenLabs-Zeitmarken je Zeichen (Rohton, Tempo 1,00)."""
import sys, os, json, subprocess, re
import numpy as np, parselmouth
sys.path.insert(0, '/home/user/5-Minuten-videos/themen/mathe-einmaleins')
os.chdir('/home/user/5-Minuten-videos/themen/mathe-einmaleins')
import regel as G
sys.argv = ['x', 'ziffer', '/dev/null']
import hoerprobe_merke as H

def wav_aus(mp3, ziel):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-ac', '1', '-ar', '44100', ziel], check=True)

def silben(wort):
    w = wort.replace('-', '')
    lo = w.lower()
    i_z = lo.index('ziffer')
    grenzen = [0, 2, i_z, i_z + 3, len(w)]          # Ei | ner | zif | fer(n)
    # auf Indizes im Original mit Bindestrich umrechnen
    abb, k = [], 0
    for j, ch in enumerate(wort):
        if ch != '-':
            abb.append(j)
    abb.append(len(wort))
    return [(abb[a], abb[b] if b < len(abb) else len(wort)) for a, b in zip(grenzen, grenzen[1:])], ['Ei', 'ner', 'zif', 'fer(n)']

ergebnis = {}
for name in ('ziffer', 'bindestrich', 'gross'):
    text = H.FASSUNGEN[name][0]
    mp3, al = G.R.tts_eleven(text, G.CFG, G.CACHE)
    st, en = al['character_start_times_seconds'], al['character_end_times_seconds']
    wav = fos.environ.get('BETONUNG_ORDNER', '/tmp') + '/{name}.wav'
    wav_aus(mp3, wav)
    snd = parselmouth.Sound(wav)
    pitch = snd.to_pitch(time_step=0.005, pitch_floor=70, pitch_ceiling=300)
    inten = snd.to_intensity(time_step=0.005)
    pt, pf = pitch.xs(), pitch.selected_array['frequency']
    it, iv = inten.xs(), inten.values[0]
    zeilen = []
    for m in re.finditer(r'Einer-?Ziffern?|EINERziffern?|Einerziffern?', text):
        wort, a0 = m.group(0), m.start()
        sp, namen = silben(wort)
        werte = []
        for (s0, s1), sn in zip(sp, namen):
            t0, t1 = st[a0 + s0], (st[a0 + s1] if a0 + s1 < len(st) and s1 < len(wort) else en[a0 + len(wort) - 1])
            f = pf[(pt >= t0) & (pt < t1)]; f = f[f > 0]
            db = iv[(it >= t0) & (it < t1)]
            werte.append(dict(silbe=sn, ms=round((t1 - t0) * 1000), hz=round(float(np.median(f)), 1) if len(f) else None,
                              hz_max=round(float(f.max()), 1) if len(f) else None, db=round(float(db.max()), 1) if len(db) else None))
        zeilen.append(dict(wort=wort, silben=werte))
    ergebnis[name] = zeilen
json.dump(ergebnis, open(os.environ.get('BETONUNG_ORDNER', '/tmp') + '/werte.json', 'w'),
          ensure_ascii=False, indent=1)
for name, zeilen in ergebnis.items():
    for z in zeilen:
        s = z['silben']
        ei, zif = s[0], s[2]
        st_ = 12 * np.log2(ei['hz_max'] / zif['hz_max']) if ei['hz_max'] and zif['hz_max'] else float('nan')
        print(f"{name:12s} {z['wort']:14s} " + ' | '.join(f"{x['silbe']}: {x['ms']} ms, {x['hz']} Hz (max {x['hz_max']}), {x['db']} dB" for x in s)
              + f"  →  Ei−zif: {st_:+.1f} Halbtöne, {ei['db'] - zif['db']:+.1f} dB, Dauer {ei['ms']}/{zif['ms']}")
