import json, os, re, sys, glob
S = sys.argv[1]
def sek(t): h, m, s = t.split(':'); return int(h) * 3600 + int(m) * 60 + float(s)
def silben(w):
    w = w.lower()
    if not re.search('[a-zäöüß]', w): return 0
    return max(1, len(re.findall('[aeiouyäöü]+', w)))
def vtt_woerter(pfad):
    out = []; cue = None
    for z in open(pfad, encoding='utf-8'):
        z = z.rstrip('\n')
        m = re.match(r'(\d\d:\d\d:\d\d\.\d+) -->', z)
        if m: cue = sek(m.group(1)); continue
        if '<c>' in z and cue is not None:
            teile = re.split(r'<(\d\d:\d\d:\d\d\.\d+)>', z)
            erst = re.sub('<[^>]+>', '', teile[0]).strip()
            if erst: out.append((cue, erst))
            for i in range(1, len(teile), 2):
                w = re.sub('<[^>]+>', '', teile[i + 1]).strip()
                if w: out.append((sek(teile[i]), w))
    return out
def mess(ws, dauer, name, views=None):
    a, b = 0.15 * dauer, 0.85 * dauer
    ww = [(t, w) for t, w in ws if a <= t < b]
    if len(ww) < 50: return None
    syl = [silben(w) for _, w in ww]
    gesamt = sum(syl) / (b - a)
    sprech = 0.0
    for (t, w), (t2, _), s in zip(ww, ww[1:], syl):
        sprech += min(t2 - t, 0.25 + 0.14 * s)        # längere Lücken = Pause
    art = sum(syl[:-1]) / sprech
    wpm = 60 * len(ww) / (b - a)
    return dict(name=name, silben_s=gesamt, artikulation=art, wpm=wpm, views=views, n=len(ww))
erg = []
for d in sorted(glob.glob(S + '/*/')):
    vtts = glob.glob(d + 'v.de-orig.vtt') or glob.glob(d + 'v.de.vtt')
    if not vtts: continue
    info = json.load(open(d + 'v.info.json'))
    r = mess(vtt_woerter(vtts[0]), info['duration'], f"{info['channel']}: {info['title'][:48]}", info.get('view_count'))
    if r: erg.append(r)
# unser Video: Wortzeiten aus der Hörprobe (ElevenLabs-Zeitmarken)
h = open('/home/user/5-Minuten-videos/themen/guanfacin/hoerprobe/index.html', encoding='utf-8').read()
m = re.search(r'var S = (\{.*?\}), KAP', h, re.S)
S_ = json.loads(m.group(1)); ws = [(x['t'], x['w']) for x in S_['ganz']['w']]
unser = mess(ws, S_['ganz']['dauer'], 'UNSER Guanfacin (Tempo 1,00)')
erg.append(unser)
for f in (1.03, 1.05):
    erg.append(dict(name=f'UNSER Guanfacin bei {f:.2f}'.replace('.', ','), silben_s=unser['silben_s'] * f, artikulation=unser['artikulation'] * f, wpm=unser['wpm'] * f, views=None, n=0))
erg.sort(key=lambda r: r['silben_s'])
print(f"{'Video':58s} {'Silben/s':>8s} {'Artik.':>7s} {'W/min':>6s} {'Aufrufe':>9s}")
for r in erg:
    print(f"{r['name'][:58]:58s} {r['silben_s']:8.2f} {r['artikulation']:7.2f} {r['wpm']:6.0f} {(str(round(r['views']/1e3))+' T') if r['views'] else '':>9s}")
json.dump(erg, open(S + '/ergebnis.json', 'w'), ensure_ascii=False, indent=1)
