#!/usr/bin/env python3
"""Hörprobe zum Mitlesen und Markieren: python3 hoerprobe.py szenen.json <ausordner> [--abstand 2]

Nach dem Rendern (video.wav, video_zeitplan.json, tts_cache). Baut <ausordner>/index.html und audio/*.mp3 aus der
Vorlage des Seneca-Hörspiels: ganzes Video und jede Szene einzeln, Text läuft mit, Tippen auf ein Wort spielt ab dort,
mit dem Stift markiert der Nutzer falsch betonte Wörter (Sammlung „markierungen“ im Speicher der Seite, lesen mit
db_list). Vom Betonungsfilter verdächtige Wörter haben eine Wellenlinie. Als Artifact veröffentlichen (publish_files),
danach declare_capabilities mit {"db": {}}.
"""
import base64, html, json, os, subprocess, sys, tempfile
HIER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HIER)
import betonung

args = sys.argv[1:]; abstand = 2.0
if '--abstand' in args:
    i = args.index('--abstand'); abstand = float(args[i + 1]); del args[i:i + 2]
szenen, aus = args
basis = os.path.dirname(os.path.abspath(szenen))
cfg = json.load(open(szenen, encoding='utf-8'))
zp = {z['id']: z for z in json.load(open(os.path.join(basis, 'video_zeitplan.json')))}
say = lambda s: s if isinstance(s, str) else s.get('say', s['t'])
cache = {}
for f in [x for x in os.listdir(os.path.join(basis, 'tts_cache')) if x.endswith('.json')]:
    d = json.load(open(os.path.join(basis, 'tts_cache', f)))
    if d.get('alignment'): cache[''.join(d['alignment']['characters']).strip()] = d
os.makedirs(os.path.join(aus, 'audio'), exist_ok=True)
wav = os.path.join(basis, 'video.wav')
mm = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'
esc = html.escape

alle, szenen_w, verdacht = [], {}, {}
for sc in cfg['scenes']:
    d = cache[' '.join(say(s) for s in sc['sentences']).strip()]
    al = d['alignment']; text = ''.join(al['characters']); W = betonung.woerter(al)
    # Satzanfang im Szenenton (Zeichenposition -> Zeit), Video-Startzeit des Satzes aus dem Zeitplan
    pos, starts = 0, []
    for s in sc['sentences']:
        k = text.find(say(s).strip()[:20], pos); starts.append((k, al['character_start_times_seconds'][k])); pos = k + 1
    st = zp[sc['id']]['st']
    ci, i0 = 0, len(alle)
    for w in W:
        k = text.find(w['w'], ci); ci = k + len(w['w'])
        si = max(j for j, (p, _) in enumerate(starts) if p <= k)
        alle.append({'w': w['w'], 't': round(st[si][0] + (w['s'] - starts[si][1]), 3)})
    szenen_w[sc['id']] = (i0, len(alle) - 1)
    with tempfile.NamedTemporaryFile(suffix='.mp3') as tmp:
        tmp.write(base64.b64decode(d['audio_base64'])); tmp.flush()
        for e in betonung.pruefe(tmp.name, W, abstand):
            if e['funktion'] and e['abstand'] >= abstand:
                verdacht[i0 + e['i']] = e['abstand']

ende = max(z['v1'] for z in zp.values())
subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', wav, '-ac', '1', '-b:a', '96k', os.path.join(aus, 'audio', 'ganz.mp3')], check=True)
S = {'ganz': {'datei': 'audio/ganz.mp3', 'dauer': round(ende, 3), 'w': alle, 'mark': sorted(verdacht), 'i0': 0, 'a': 0}}


def tafel(k, titel, unter, befund=''):
    t = f'''  <section class="stelle" id="{k}" data-an="false" aria-labelledby="t-{k}">
    <div class="zeile">
      <button type="button" class="knopf" data-k="{k}" data-name="{esc(titel)}" aria-label="{esc(titel)} abspielen"></button>
      <div class="titel"><b id="t-{k}">{esc(titel)}</b><span>{esc(unter)}</span></div>
    </div>
    <p class="text" data-text="{k}"></p>
    <div class="balken"><i data-balken="{k}"></i></div>'''
    return t + (f'\n    <dl><dt>Filter</dt><dd>{befund}</dd></dl>' if befund else '') + '\n  </section>'


teile = [tafel('ganz', 'Ganzes Video', f"{mm(ende)} · {cfg.get('voice_name', '').split(' - ')[0]}")]
teile.append('  <h2 class="abschnitt">Szene für Szene</h2>')
for sc in cfg['scenes']:
    a, e = zp[sc['id']]['v0'], zp[sc['id']]['v1']
    i0, i1 = szenen_w[sc['id']]
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-ss', f'{a:.3f}', '-to', f'{e:.3f}', '-i', wav, '-ac', '1', '-b:a', '96k',
                    os.path.join(aus, 'audio', sc['id'] + '.mp3')], check=True)
    S[sc['id']] = {'datei': f"audio/{sc['id']}.mp3", 'dauer': round(e - a, 3), 'i0': i0, 'a': round(a, 3),
                   'w': [{'w': x['w'], 't': round(x['t'] - a, 3)} for x in alle[i0:i1 + 1]],
                   'mark': [m - i0 for m in sorted(verdacht) if i0 <= m <= i1]}
    n = len(S[sc['id']]['mark'])
    teile.append(tafel(sc['id'], sc['headline'], f'bei {mm(a)} · {mm(e - a)}', f'{n} Wort verdächtig (Wellenlinie)' if n == 1 else (f'{n} Wörter verdächtig (Wellenlinie)' if n else '')))

kopf = f'''  <header class="kopf">
    <span class="eyebrow">{esc(cfg.get('titel', ''))}</span>
    <h1>Hörprobe</h1>
    <p class="lead">Oben das ganze Video, darunter jede Szene. Tippe auf ▶ oder auf ein Wort, der Text läuft mit. Falsche Betonung: unten auf „Markieren“, dann das Wort antippen, gern mit Notiz. Wörter mit Wellenlinie hat der Betonungsfilter als verdächtig gemeldet (ab {abstand:g} Halbtönen auf einem kleinen Wort).</p>
  </header>
'''
fuss = '  <p class="fuss">Ich lese deine Markierungen direkt aus der Seite und erzeuge die betroffenen Sätze neu, in zwei bis drei Fassungen zur Auswahl.</p>'
seite = open(os.path.join(HIER, 'hoerprobe_vorlage.html'), encoding='utf-8').read()
seite = (seite.replace('{{TITEL}}', f"{cfg.get('titel', 'Video')} · Hörprobe")
         .replace('{{BESCHREIBUNG}}', 'Sprechtext zum Mitlesen und Markieren falsch betonter Wörter.')
         .replace('{{INHALT}}', kopf + '\n'.join(teile) + '\n\n' + fuss)
         .replace('{{DATEN}}', json.dumps(S, ensure_ascii=False)).replace('{{KAPITEL}}', json.dumps(os.path.basename(basis))))
open(os.path.join(aus, 'index.html'), 'w', encoding='utf-8').write(seite)
print(f'{aus}/index.html: {len(S)} Tafeln, {len(alle)} Wörter, {len(verdacht)} verdächtig')
