#!/usr/bin/env python3
"""Betonungs-Vorfilter fuer die Szenen-Aufnahmen: python3 betonung.py szenen.json [--abstand 5]

Verfahren aus dem Seneca-Hoerspiel (seneca-audio/werkzeuge/betonung.py): Tonhoehengipfel je Wort (Praat), markiert,
wenn der hoechste Gipfel eines Sprechabschnitts auf einem Funktionswort liegt, nicht am Abschnittsanfang, und mindestens
--abstand Halbtoene ueber dem hoechsten Inhaltswort. Wortzeiten kommen hier aus den ElevenLabs-Zeitmarken im tts_cache.
Schwelle 5 HT war fuer die Stimme Helmut geeicht; fuer Christian an gemeldeten Fehlern nachpruefen.
Ersetzt das Ohr nicht: Kontrastbetonung ist richtig und wird trotzdem markiert.
"""
import base64, glob, json, os, re, subprocess, sys, tempfile
import numpy as np
import parselmouth

FUNKTION = set("""
der die das den dem des ein eine einen einem einer eines
ich du er sie es wir ihr uns euch mich dich sich mir dir ihm ihn ihnen man
mein meine meinen meinem meiner meines dein deine deinen deinem deiner deines sein seine seinen seinem seiner seines
ihre ihren ihrem ihrer ihres unser unsere unseren unserem unserer unseres euer eure euren eurem eurer
an am auf aus bei beim bis durch für gegen hinter in im ins mit nach neben ohne seit über um unter von vom vor zu zum zur
zwischen wegen
und oder aber denn dass wenn als wie ob weil doch sondern sowie
ist sind war waren wird werden wurde wurden hat haben hatte hatten sei seien wäre wären bin bist seid habe hast
würde würden kann können muss müssen soll sollen will wollen darf dürfen
""".split())
ENDE = tuple(",.;:!?–")
norm = lambda w: re.sub(r"[^a-zäöüß]", "", w.lower())


def woerter(al):
    """Woerter mit Start/Ende aus der Zeichen-Ausrichtung."""
    ch, s, e = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    W, cur = [], None
    for c, a, b in zip(ch, s, e):
        if c.isspace():
            if cur: W.append(cur); cur = None
            continue
        if cur is None: cur = {'w': '', 's': a, 'e': b}
        cur['w'] += c; cur['e'] = b
    if cur: W.append(cur)
    return W


def pruefe(mp3, W, abstand):
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, 't.wav')
        subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', mp3, '-ac', '1', wav], check=True)
        p = parselmouth.Sound(wav).to_pitch_ac(time_step=0.01, pitch_floor=60, pitch_ceiling=260)
    f0, t = p.selected_array['frequency'], p.xs()
    med = np.median(f0[f0 > 0])
    G = []
    for w in W:
        f = f0[(t >= w['s']) & (t <= w['e']) & (f0 > 0)]
        G.append(float(np.quantile(12 * np.log2(f / med), 0.95)) if len(f) >= 3 else None)
    A, jetzt = [], []
    for i, w in enumerate(W):
        jetzt.append(i)
        if w['w'].rstrip('“”»«"\'').endswith(ENDE) or i == len(W) - 1:
            A.append(jetzt); jetzt = []
    erg = []
    for a in A:
        g = [(i, G[i]) for i in a if G[i] is not None]
        if len(g) < 3: continue
        top = max(g, key=lambda x: x[1])[0]
        inhalt = [x for i, x in g if norm(W[i]['w']) not in FUNKTION]
        dd = G[top] - max(inhalt) if inhalt else float('inf')
        erg.append({'i': top, 'von': W[a[0]]['s'], 'woerter': [W[i]['w'] for i in a], 'pos': a.index(top), 'abstand': dd,
                    'funktion': norm(W[top]['w']) in FUNKTION and top != a[0]})
    return erg


def main():
    args = sys.argv[1:]
    abstand = 5.0
    if '--abstand' in args:
        i = args.index('--abstand'); abstand = float(args[i + 1]); del args[i:i + 2]
    basis = os.path.dirname(os.path.abspath(args[0]))
    cfg = json.load(open(args[0], encoding='utf-8'))
    zp = os.path.join(basis, 'video_zeitplan.json')
    v0 = {z['id']: z['v0'] for z in json.load(open(zp))} if os.path.exists(zp) else {}
    texte = {sc['id']: ' '.join(s if isinstance(s, str) else s.get('say', s['t']) for s in sc['sentences']) for sc in cfg['scenes']}
    n = knapp = 0
    for f in sorted(glob.glob(os.path.join(basis, 'tts_cache', '*.json'))):
        d = json.load(open(f))
        al = d.get('alignment')
        if not al: continue
        txt = ''.join(al['characters'])
        sid = next((k for k, v in texte.items() if v.strip() == txt.strip()), None)
        if sid is None: continue
        with tempfile.NamedTemporaryFile(suffix='.mp3') as tmp:
            tmp.write(base64.b64decode(d['audio_base64'])); tmp.flush()
            for e in pruefe(tmp.name, woerter(al), abstand):
                if not e['funktion']: continue
                satz = ' '.join(w.upper() if j == e['pos'] else w for j, w in enumerate(e['woerter']))
                tv = v0.get(sid, 0) + e['von'] + 1.0
                if e['abstand'] >= abstand:
                    n += 1; print(f"{sid}  ~{int(tv // 60)}:{int(tv % 60):02d}  +{e['abstand']:.1f} HT  {satz}")
                elif e['abstand'] >= 3:
                    knapp += 1; print(f"  (knapp) {sid}  ~{int(tv // 60)}:{int(tv % 60):02d}  +{e['abstand']:.1f} HT  {satz}")
    print(f'{n} markiert (≥ {abstand} HT), {knapp} knapp darunter (3–{abstand} HT). Zeiten ≈ Videozeit.')


if __name__ == '__main__':
    main()
