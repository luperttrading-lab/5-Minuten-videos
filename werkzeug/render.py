#!/usr/bin/env python3
"""Info-Video aus Ausschnitten einer Grafik plus Sprachausgabe.

Aufruf:
  python3 render.py szenen.json grafik.png ausgabe.mp4            # komplettes Video
  python3 render.py szenen.json grafik.png ausgabe.mp4 --nur-ton  # nur Ton, Zeitplan, Untertitel
  python3 render.py szenen.json grafik.png ausgabe.mp4 --vorschau # Kontaktbogen statt Video

Ton: je Satz eine edge-tts-Datei (zwischengespeichert in tts_cache/). Die Tonquelle ist austauschbar:
mit --ton-dir liest das Skript je Satz <szene>_<nr>.mp3/.wav aus einem Ordner (z. B. ElevenLabs-Exporte).
"""
import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, SR = 1920, 1080, 25, 44100
PAPER = (250, 243, 234)
INK = (34, 38, 50)
ACCENT = (50, 78, 122)
MUTED = (120, 114, 110)
TRACK = (232, 223, 212)
LEVELS = {
    'stark': ((52, 128, 86), 3, 'gut belegt'),
    'mittel': ((190, 136, 30), 2, 'teilweise belegt'),
    'schwach': ((206, 98, 46), 1, 'schwach belegt'),
    'keine': ((178, 52, 48), 0, 'nicht belegt'),
}
# Marker je Stichpunkt: Farbe und Zeichen
MARKS = {
    'stark': ((52, 128, 86), 'check', 'belegt'),
    'mittel': ((190, 136, 30), 'tilde', 'teilweise'),
    'offen': ((138, 132, 126), 'frage', 'keine Studien'),
    'keine': ((178, 52, 48), 'cross', 'nicht haltbar'),
}


def draw_mark(d, cx, cy, r, kind):
    col, sym, _ = MARKS[kind]
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    w = max(3, round(r / 4.2))
    k = r * 0.5
    if sym == 'check':
        d.line([(cx - k, cy + 0.05 * r), (cx - 0.15 * r, cy + k * 0.85), (cx + k * 1.05, cy - k * 0.8)],
               fill='white', width=w, joint='curve')
    elif sym == 'cross':
        d.line([(cx - k * 0.8, cy - k * 0.8), (cx + k * 0.8, cy + k * 0.8)], fill='white', width=w)
        d.line([(cx - k * 0.8, cy + k * 0.8), (cx + k * 0.8, cy - k * 0.8)], fill='white', width=w)
    elif sym == 'tilde':
        d.arc([cx - k * 1.3, cy - k * 0.5, cx, cy + k * 0.5], 200, 340, fill='white', width=w)
        d.arc([cx, cy - k * 0.5, cx + k * 1.3, cy + k * 0.5], 20, 160, fill='white', width=w)
    else:
        d.text((cx, cy + 1), '?', font=font(INTER.format('Bold'), int(r * 1.45)), fill='white', anchor='mm')
INTER = '/usr/share/fonts/opentype/inter/Inter-{}.otf'
SERIF_B = '/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf'
TX0, TX1 = 100, 760            # Textspalte links
PIC = (830, 64, 1864, 1004)    # Bildfeld rechts
GAP_SENT, GAP_SCENE, PRE, LEAD, TAIL = 0.28, 0.75, 0.6, 1.0, 2.0
XF_SCENE, XF_SHOT, FADE = 0.6, 0.5, 0.45
MAX_SCALE = 3.4

_fonts = {}


def font(path, size):
    if (path, size) not in _fonts:
        _fonts[(path, size)] = ImageFont.truetype(path, size)
    return _fonts[(path, size)]


def wrap(draw, text, fnt, width):
    lines, cur = [], ''
    for word in text.split():
        test = (cur + ' ' + word).strip()
        if draw.textlength(test, font=fnt) <= width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- Ton
def decode(path, tempo=1.0):
    af = ['-af', f'atempo={tempo}'] if abs(tempo - 1) > 1e-3 else []
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path] + af + ['-f', 's16le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def trim(x, thr_db=-45, margin=0.04):
    env = np.abs(x)
    thr = 10 ** (thr_db / 20) * max(env.max(), 1e-6)
    idx = np.where(env > thr)[0]
    if len(idx) == 0:
        return x
    m = int(margin * SR)
    return x[max(idx[0] - m, 0):idx[-1] + m]


def tts_edge(text, voice, rate, cache):
    key = hashlib.sha1(f'{voice}|{rate}|{text}'.encode()).hexdigest()[:16]
    mp3 = os.path.join(cache, key + '.mp3')
    if not os.path.exists(mp3):
        cmd = ['edge-tts', '--voice', voice, f'--rate={rate}', '--text', text, '--write-media', mp3 + '.tmp']
        if os.environ.get('HTTPS_PROXY'):
            cmd[1:1] = ['--proxy', os.environ['HTTPS_PROXY']]
        for attempt in range(5):
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode == 0 and os.path.getsize(mp3 + '.tmp') > 1000:
                os.replace(mp3 + '.tmp', mp3)
                break
            time.sleep(2 ** attempt)
        else:
            sys.exit(f'TTS fehlgeschlagen: {text[:60]} … {r.stderr[-300:]}')
    return trim(decode(mp3))


def tts_eleven(text, cfg, cache):
    """Eine Szene am Stueck ueber ElevenLabs, mit Zeitmarken je Zeichen. Zwischengespeichert."""
    import base64
    import urllib.error
    import urllib.request
    sig = f"el|{cfg['voice_id']}|{cfg['model']}|{json.dumps(cfg.get('voice_settings'), sort_keys=True)}|{text}"
    js = os.path.join(cache, hashlib.sha1(sig.encode()).hexdigest()[:16] + '.json')
    if not os.path.exists(js):
        body = {'text': text, 'model_id': cfg['model']}
        if cfg.get('voice_settings'):
            body['voice_settings'] = cfg['voice_settings']
        url = (f"https://api.elevenlabs.io/v1/text-to-speech/{cfg['voice_id']}/with-timestamps"
               f"?output_format=mp3_44100_128")
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={
            'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    data, cost = r.read(), r.headers.get('character-cost')
                break
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503) and attempt < 3:
                    time.sleep(3 * 2 ** attempt)
                    continue
                sys.exit(f'ElevenLabs HTTP {e.code}: {e.read()[:300]}')
        with open(js + '.tmp', 'wb') as f:
            f.write(data)
        os.replace(js + '.tmp', js)
        with open(os.path.join(cache, 'elevenlabs_log.jsonl'), 'a') as f:
            f.write(json.dumps({'zeit': time.strftime('%Y-%m-%d %H:%M:%S'), 'zeichen': len(text),
                                'character_cost': cost, 'model': cfg['model'], 'voice': cfg['voice_id'],
                                'datei': os.path.basename(js)}) + '\n')
        print(f'  ElevenLabs: {len(text)} Zeichen, berechnet {cost}', flush=True)
    d = json.load(open(js))
    mp3 = js[:-5] + '.mp3'
    if not os.path.exists(mp3):
        with open(mp3, 'wb') as f:
            f.write(base64.b64decode(d['audio_base64']))
    return mp3, d['alignment']


def scene_eleven(sc, cfg, cache):
    """Szenen-Ton plus Satzanfaenge (s) relativ zum Ton."""
    says = [sentence(s)[1] for s in sc['sentences']]
    text = ' '.join(says)
    mp3, al = tts_eleven(text, cfg, cache)
    tempo = cfg.get('tempo', 1.0)
    x = decode(mp3, tempo)
    thr = 10 ** (-45 / 20) * max(np.abs(x).max(), 1e-6)
    idx = np.where(np.abs(x) > thr)[0]
    a, b = max(idx[0] - int(0.04 * SR), 0), idx[-1] + int(0.06 * SR)
    x = x[a:b]
    lead = a / SR
    starts = al['character_start_times_seconds']
    scale = len(starts) / max(len(text), 1)          # falls die Zeitmarken nicht 1:1 zum Text passen
    pos, out = 0, []
    for s in says:
        i = min(int(round(pos * scale)), len(starts) - 1)
        out.append(max(starts[i] / tempo - lead, 0.0))
        pos += len(s) + 1
    sc['_align'] = {'text': text, 'starts': starts, 'tempo': tempo, 'lead': lead, 'scale': scale}
    return x, out


def number_sources(cfg):
    """Quellen nach erstem Auftreten durchnummerieren; Kurzzeile je Szene, Nummern fuer die Beschreibung."""
    reg = cfg.get('quellen')
    if not reg:
        return []
    order = []
    for sc in cfg['scenes']:
        for q in sc.get('quellen', []):
            if q not in reg:
                sys.exit(f'Quelle fehlt im Verzeichnis: {q}')
            if q not in order:
                order.append(q)
        if sc.get('quellen'):
            sc['source'] = 'Quellen: ' + ' · '.join(f"[{order.index(q) + 1}] {reg[q]['kurz']}" for q in sc['quellen'])
    cfg['_order'] = order
    return order


def sentence(s):
    """Satz als (Anzeigetext, Sprechtext)."""
    return (s, s) if isinstance(s, str) else (s['t'], s.get('say', s['t']))


def build_audio(cfg, args):
    os.makedirs(args.cache, exist_ok=True)
    clips, t = [], 0.0
    eleven = cfg.get('tts') == 'elevenlabs' and not args.ton_dir
    for k, sc in enumerate(cfg['scenes']):
        sc['v0'] = t
        t += LEAD if k == 0 else PRE
        sc['st'] = []
        if eleven:                                     # Szene am Stueck, Satzzeiten aus den Zeitmarken
            pcm, rel = scene_eleven(sc, cfg, args.cache)
            sc['_align']['t0'] = t
            end = len(pcm) / SR
            for i, s in enumerate(sc['sentences']):
                nxt = rel[i + 1] if i + 1 < len(rel) else end
                sc['st'].append((t + rel[i], nxt - rel[i], sentence(s)[0]))
            clips.append((t, pcm))
            t += end + GAP_SCENE - PRE
            continue
        for i, s in enumerate(sc['sentences']):
            shown, say = sentence(s)
            if args.ton_dir:
                base = os.path.join(args.ton_dir, f"{sc['id']}_{i + 1:02d}")
                path = next((base + e for e in ('.wav', '.mp3', '.flac') if os.path.exists(base + e)), None)
                if not path:
                    sys.exit(f'fehlt: {base}.mp3')
                pcm = trim(decode(path))
            else:
                pcm = tts_edge(say, cfg['voice'], cfg['rate'], args.cache)
            dur = len(pcm) / SR
            sc['st'].append((t, dur, shown))
            clips.append((t, pcm))
            t += dur + GAP_SENT
        t += GAP_SCENE - GAP_SENT - PRE
    total = t + PRE + TAIL
    for k, sc in enumerate(cfg['scenes']):
        sc['v1'] = cfg['scenes'][k + 1]['v0'] if k + 1 < len(cfg['scenes']) else total
    buf = np.zeros(int(total * SR) + SR, np.float32)
    for t0, pcm in clips:
        i = int(t0 * SR)
        buf[i:i + len(pcm)] += pcm
    peak = np.abs(buf).max()
    buf = buf / peak * 0.89 if peak > 0 else buf
    return total, (buf * 32767).astype(np.int16)


def write_wav(path, pcm):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def srt_time(t):
    ms = int(round(t * 1000))
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'


def write_srt(cfg, path):
    cues = []
    for sc in cfg['scenes']:
        for t0, dur, text in sc['st']:
            parts = [text]
            if len(text) > 84 and ', ' in text:          # lange Saetze am mittleren Komma teilen
                cut = min((abs(i - len(text) / 2), i) for i in range(len(text)) if text.startswith(', ', i))[1]
                parts = [text[:cut + 1], text[cut + 2:]]
            n = sum(len(p) for p in parts)
            a = t0
            for p in parts:
                b = a + dur * len(p) / n
                cues.append((a, b + 0.15, p))
                a = b
    with open(path, 'w', encoding='utf-8') as f:
        for i, (a, b, p) in enumerate(cues, 1):
            f.write(f'{i}\n{srt_time(a)} --> {srt_time(b)}\n{p}\n\n')


# ---------------------------------------------------------------- Bild
def panel_states(sc):
    """Vollbilder (ohne Grafik) fuer 0..n sichtbare Stichpunkte."""
    base = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(base)
    y = 104
    if sc.get('kicker'):
        f = font(INTER.format('SemiBold'), 25)
        d.text((TX0, y), sc['kicker'].upper(), font=f, fill=ACCENT)
        y += 52
    fh = font(SERIF_B, 64)
    for line in wrap(d, sc['headline'], fh, TX1 - TX0):
        d.text((TX0, y), line, font=fh, fill=INK)
        y += 72
    y += 18
    d.rectangle([TX0, y, TX0 + 90, y + 5], fill=ACCENT)
    y += 44
    ev = sc.get('evidence')
    if ev:
        col, dots, label = LEVELS[ev['level']]
        by = 850
        fb = font(INTER.format('SemiBold'), 25)
        txt = 'Beweislage: ' + ev.get('label', label)
        tw = d.textlength(txt, font=fb)
        bw = int(tw + 52)                              # nur Farbe und Text, keine Punkte (waeren doppelt)
        tint = tuple(int(c * 0.14 + p * 0.86) for c, p in zip(col, PAPER))
        d.rounded_rectangle([TX0, by, TX0 + bw, by + 54], radius=27, fill=tint, outline=col, width=2)
        d.text((TX0 + 26, by + 12), txt, font=fb, fill=col)
        used = {b.get('ev') for b in sc.get('bullets', [])}
        if used - {None}:                              # Legende statt Fliesstext
            fl = font(INTER.format('Regular'), 21)
            xx, yy = TX0, by + 84
            kinds = ['stark', 'mittel'] + (['offen'] if 'offen' in used else []) + ['keine']
            for kind in kinds:
                draw_mark(d, xx + 11, yy, 11, kind)
                d.text((xx + 28, yy), MARKS[kind][2], font=fl, fill=MUTED, anchor='lm')
                xx += 28 + int(d.textlength(MARKS[kind][2], font=fl)) + 26
        elif ev.get('note'):
            fn = font(INTER.format('Regular'), 22)
            yy = by + 70
            for line in wrap(d, ev['note'], fn, TX1 - TX0 + 20):
                d.text((TX0, yy), line, font=fn, fill=MUTED)
                yy += 30
    if sc.get('source'):
        fs = font(INTER.format('Regular'), 19)
        lines = wrap(d, sc['source'], fs, 1700)
        yy = H - 30 - 26 * len(lines)
        for line in lines:
            d.text((TX0, yy), line, font=fs, fill=MUTED)
            yy += 26
    states = [base]
    fb = font(INTER.format('Medium'), 34)
    for b in sc.get('bullets', []):
        img = states[-1].copy()
        d = ImageDraw.Draw(img)
        lines = wrap(d, b['t'], fb, TX1 - TX0 - 50)
        if b.get('ev'):
            draw_mark(d, TX0 + 15, y + 22, 16, b['ev'])
        else:
            d.ellipse([TX0 + 9, y + 16, TX0 + 21, y + 28], fill=ACCENT)
        for line in lines:
            d.text((TX0 + 46, y), line, font=fb, fill=INK)
            y += 45
        y += 20
        states.append(img)
    if y > 830:
        print(f"WARNUNG {sc['id']}: Stichpunkte reichen bis y={y}, ueberlappen die Ampel")
    return states


_masks = {}


def mask(size):
    if size not in _masks:
        m = Image.new('L', size, 0)
        ImageDraw.Draw(m).rounded_rectangle([26, 26, size[0] - 27, size[1] - 27], radius=40, fill=255)
        _masks[size] = m.filter(ImageFilter.GaussianBlur(17))
    return _masks[size]


def fit_box(a, b, img_size):
    """Zielgroesse im Bildfeld und Endbox mit gleichem Seitenverhaeltnis wie a."""
    aw, ah = a[2] - a[0], a[3] - a[1]
    asp = aw / ah
    bw_max, bh_max = PIC[2] - PIC[0], PIC[3] - PIC[1]
    pw, ph = (bw_max, round(bw_max / asp)) if asp > bw_max / bh_max else (round(bh_max * asp), bh_max)
    if pw / aw > MAX_SCALE:                       # kleine Ausschnitte nicht matschig aufblasen
        pw, ph = round(aw * MAX_SCALE), round(ah * MAX_SCALE)
    if b is None:
        z = 0.95
        cx, cy = (a[0] + a[2]) / 2, (a[1] + a[3]) / 2
        b = [cx - aw * z / 2, cy - ah * z / 2, cx + aw * z / 2, cy + ah * z / 2]
    else:
        cx, cy, bw = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2, b[2] - b[0]
        b = [cx - bw / 2, cy - bw / asp / 2, cx + bw / 2, cy + bw / asp / 2]
    out = []
    for box in (a, b):
        x0, y0, x1, y1 = map(float, box)
        dx = -min(x0, 0) - max(x1 - img_size[0], 0)
        dy = -min(y0, 0) - max(y1 - img_size[1], 0)
        out.append((x0 + dx, y0 + dy, x1 + dx, y1 + dy))
    return (pw, ph), out[0], out[1]


BILD_DIR = '.'
_bilder = {}


def quelle(obj, src):
    """Bildquelle eines Ausschnitts/einer Kachel: eigenes Bild (`bild`, relativ zum Drehbuch) oder die Grafik.
    Ohne `a` gilt das ganze Bild."""
    img = src
    if obj.get('bild'):
        pfad = os.path.join(BILD_DIR, obj['bild'])
        if pfad not in _bilder:
            _bilder[pfad] = Image.open(pfad).convert('RGB')
        img = _bilder[pfad]
    a = obj.get('a') or [0, 0, img.size[0], img.size[1]]
    return img, a


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return 0.5 * u + 0.5 * (0.5 - 0.5 * math.cos(math.pi * u))


class Scene:
    def __init__(self, sc, src):
        self.sc, self.src = sc, src
        self.states = panel_states(sc)
        st = sc['st']
        self.bullet_t = []
        for b in sc.get('bullets', []):                 # gleiche Satznummer: nacheinander einblenden
            t = st[b.get('at', 0)][0] + 0.15
            if self.bullet_t and t <= self.bullet_t[-1]:
                t = self.bullet_t[-1] + 1.1
            self.bullet_t.append(t)
        self.shots = []
        for j, sh in enumerate(sc['shots']):
            t0 = sc['v0'] if j == 0 else st[sh['at']][0] - 0.35
            img, a0 = quelle(sh, src)
            size, a, b = fit_box(a0, a0 if sh.get('zoom') == 'none' else sh.get('b'), img.size)
            if sh.get('zoom') == 'out':
                a, b = b, a
            self.shots.append({'t0': t0, 'size': size, 'a': a, 'b': b, 'img': img})
        for j, sh in enumerate(self.shots):
            sh['t1'] = self.shots[j + 1]['t0'] if j + 1 < len(self.shots) else sc['v1']

    def panel(self, t):
        n = sum(1 for bt in self.bullet_t if bt <= t)
        img = self.states[n]
        if n > 0 and t - self.bullet_t[n - 1] < FADE:
            img = Image.blend(self.states[n - 1], img, (t - self.bullet_t[n - 1]) / FADE)
        return img

    def frame_shot(self, j, t, panel):
        sh = self.shots[j]
        u = ease((t - sh['t0']) / (sh['t1'] - sh['t0'] + XF_SHOT))
        box = tuple(a + (b - a) * u for a, b in zip(sh['a'], sh['b']))
        pic = sh['img'].resize(sh['size'], Image.BICUBIC, box=box)
        if sh['size'][0] / (box[2] - box[0]) > 1.8:
            pic = pic.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=2))
        img = panel.copy()
        px = PIC[0] + (PIC[2] - PIC[0] - sh['size'][0]) // 2
        py = PIC[1] + (PIC[3] - PIC[1] - sh['size'][1]) // 2
        img.paste(pic, (px, py), mask(sh['size']))
        return img

    def frame(self, t):
        panel = self.panel(t)
        j = max(i for i, sh in enumerate(self.shots) if sh['t0'] <= t) if t >= self.shots[0]['t0'] else 0
        img = self.frame_shot(j, t, panel)
        if j + 1 < len(self.shots) and t > self.shots[j]['t1'] - XF_SHOT:
            nxt = self.frame_shot(j + 1, self.shots[j + 1]['t0'], panel)
            img = Image.blend(img, nxt, (t - (self.shots[j]['t1'] - XF_SHOT)) / XF_SHOT)
        return img


def progress(arr, t, total):
    x = int(W * min(t / total, 1))
    arr[H - 6:, :] = TRACK
    arr[H - 6:, :x] = ACCENT


class AgendaScene:
    """Einstieg mit Kapitel-Kacheln: sechs Bilder auf einen Blick, beim Aufzaehlen nacheinander hervorgehoben."""
    TW, TH, GAP, Y0, ROW = 540, 300, 45, 212, 388

    def __init__(self, sc, src):
        self.sc, self.src = sc, src
        st = sc['st']
        self.shots = [{'t0': sc['v0'], 't1': sc['v1']}]          # fuer den Kontaktbogen
        hi = sc.get('hervorheben_at')
        self.h0 = st[hi][0] if hi is not None else None
        self.h1 = self.h0 + st[hi][1] if hi is not None else None
        wts = [word_time(sc, k['wort']) if k.get('wort') else None for k in sc['kacheln']]
        self.wt = [w - 0.15 for w in wts] if all(w is not None for w in wts) else None
        lg = sc.get('legende_at')
        self.lg = st[lg][0] if lg is not None else None
        self.x0 = (W - 3 * self.TW - 2 * self.GAP) // 2
        self.base = Image.new('RGB', (W, H), PAPER)
        d = ImageDraw.Draw(self.base)
        if sc.get('kicker'):
            d.text((W // 2, 70), sc['kicker'].upper(), font=font(INTER.format('SemiBold'), 26), fill=ACCENT, anchor='mt')
        d.text((W // 2, 112), sc['headline'], font=font(SERIF_B, 70), fill=INK, anchor='mt')
        self.cards = []
        for i, k in enumerate(sc['kacheln']):
            cx = self.x0 + (i % 3) * (self.TW + self.GAP)
            cy = self.Y0 + (i // 3) * self.ROW
            d.rounded_rectangle([cx, cy, cx + self.TW, cy + self.TH + 62], radius=22, fill=(255, 250, 243),
                                outline=(232, 223, 212), width=2)
            d.ellipse([cx + 18, cy + self.TH + 8, cx + 58, cy + self.TH + 48], fill=ACCENT)
            d.text((cx + 38, cy + self.TH + 28), str(i + 1), font=font(INTER.format('Bold'), 24), fill='white', anchor='mm')
            d.text((cx + 72, cy + self.TH + 28), k['t'], font=font(INTER.format('SemiBold'), 30), fill=INK, anchor='lm')
            kimg, box = quelle(k, src)
            bw, bh = box[2] - box[0], box[3] - box[1]
            sc_ = min((self.TW - 40) / bw, (self.TH - 30) / bh)
            size = (int(bw * sc_), int(bh * sc_))
            self.cards.append({'x': cx, 'y': cy, 'box': box, 'size': size, 'img': kimg})
        self.legend = Image.new('RGBA', (W, 60), (0, 0, 0, 0))
        dl = ImageDraw.Draw(self.legend)
        fl = font(INTER.format('Medium'), 28)
        items = [('stark', 'belegt'), ('mittel', 'teilweise'), ('keine', 'nicht haltbar')]
        widths = [44 + int(dl.textlength(t, font=fl)) for _, t in items]
        xx = (W - sum(widths) - 60 * (len(items) - 1)) // 2
        for (kind, t), w in zip(items, widths):
            draw_mark(dl, xx + 15, 30, 15, kind)
            dl.text((xx + 40, 30), t, font=fl, fill=INK, anchor='lm')
            xx += w + 60

    def frame(self, t):
        img = self.base.copy()
        d = ImageDraw.Draw(img)
        u = ease((t - self.sc['v0']) / (self.sc['v1'] - self.sc['v0']))
        active = None
        if self.h0 is not None and self.h0 <= t < self.h1 + 0.6:
            if self.wt:                                      # am gesprochenen Stichwort
                past = [i for i, wt in enumerate(self.wt) if wt <= t]
                active = past[-1] if past else None
            else:
                active = min(int((t - self.h0) / ((self.h1 - self.h0) / len(self.cards))), len(self.cards) - 1)
        for i, c in enumerate(self.cards):
            x0, y0, x1, y1 = c['box']
            z = 0.06 * u                                     # langsames Hineinzoomen
            dx, dy = (x1 - x0) * z / 2, (y1 - y0) * z / 2
            pic = c['img'].resize(c['size'], Image.BICUBIC, box=(x0 + dx, y0 + dy, x1 - dx, y1 - dy))
            if active is not None and i != active:
                pic = Image.blend(pic, Image.new('RGB', pic.size, (255, 250, 243)), 0.55)
            px = c['x'] + (self.TW - c['size'][0]) // 2
            py = c['y'] + 15 + (self.TH - 30 - c['size'][1]) // 2
            img.paste(pic, (px, py), mask(c['size']))
            if i == active:
                d.rounded_rectangle([c['x'] - 3, c['y'] - 3, c['x'] + self.TW + 3, c['y'] + self.TH + 65],
                                    radius=24, outline=ACCENT, width=6)
        if self.lg is not None and t >= self.lg:
            a = min((t - self.lg) / FADE, 1.0)
            lay = self.legend.copy()
            if a < 1:
                lay.putalpha(lay.getchannel('A').point(lambda p: int(p * a)))
            img.paste(lay, (0, 990), lay)
        return img


def word_time(sc, word, after=0.0):
    """Zeitpunkt (s, absolut), an dem ein Wort gesprochen wird; None ohne Zeitmarken."""
    al = sc.get('_align')
    if not al:
        return None
    i = al['text'].find(word)
    if i < 0:
        return None
    k = min(int(round(i * al['scale'])), len(al['starts']) - 1)
    return al['t0'] + al['starts'][k] / al['tempo'] - al['lead']


def make_scene(sc, src):
    return AgendaScene(sc, src) if sc.get('layout') == 'kacheln' else Scene(sc, src)


def render(cfg, src, total, out_mp4, wav, srt):
    scenes = [make_scene(sc, src) for sc in cfg['scenes']]
    first = {}
    n = int(math.ceil(total * FPS))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '24', '-pix_fmt', 'yuv420p',
           '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2',
           '-movflags', '+faststart', '-t', f'{total:.2f}', out_mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    k = 0
    t_start = time.time()
    for f in range(n):
        t = f / FPS
        while k + 1 < len(scenes) and t >= scenes[k + 1].sc['v0']:
            k += 1
        img = scenes[k].frame(t)
        if k + 1 < len(scenes) and t > scenes[k].sc['v1'] - XF_SCENE:
            if k + 1 not in first:
                first[k + 1] = scenes[k + 1].frame(scenes[k + 1].sc['v0'])
            img = Image.blend(img, first[k + 1], (t - (scenes[k].sc['v1'] - XF_SCENE)) / XF_SCENE)
        if f < FPS // 2:                               # Einblenden aus Papierfarbe
            img = Image.blend(Image.new('RGB', (W, H), PAPER), img, f / (FPS // 2))
        arr = np.array(img)
        progress(arr, t, total)
        p.stdin.write(arr.tobytes())
        if f % (FPS * 30) == 0:
            print(f'  {t:6.1f} s / {total:.1f} s  ({time.time() - t_start:.0f} s Rechenzeit)', flush=True)
    p.stdin.close()
    if p.wait() != 0:
        sys.exit('ffmpeg-Fehler')


def preview(cfg, src, path):
    scenes = [make_scene(sc, src) for sc in cfg['scenes']]
    thumbs = []
    for s in scenes:
        for sh in s.shots:
            t = (sh['t0'] + sh['t1']) / 2
            thumbs.append(s.frame(min(t + 30, s.sc['v1'] - XF_SCENE - 0.01) if False else t).resize((480, 270)))
    cols = 4
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new('RGB', (cols * 490, rows * 280), 'white')
    for i, th in enumerate(thumbs):
        sheet.paste(th, ((i % cols) * 490, (i // cols) * 280))
    sheet.save(path)
    print('Kontaktbogen:', path, len(thumbs), 'Einstellungen')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('szenen')
    ap.add_argument('grafik')
    ap.add_argument('ausgabe')
    ap.add_argument('--nur-ton', action='store_true')
    ap.add_argument('--vorschau', action='store_true')
    ap.add_argument('--ton-dir')
    ap.add_argument('--bild', type=float, action='append', help='Einzelbild bei Sekunde T als PNG')
    ap.add_argument('--cache', default=None, help='Standard: tts_cache neben dem Drehbuch')
    args = ap.parse_args()
    args.cache = args.cache or os.path.join(os.path.dirname(os.path.abspath(args.szenen)), 'tts_cache')
    cfg = json.load(open(args.szenen, encoding='utf-8'))
    global BILD_DIR
    BILD_DIR = os.path.dirname(os.path.abspath(args.szenen))
    number_sources(cfg)
    total, pcm = build_audio(cfg, args)
    stem = os.path.splitext(args.ausgabe)[0]
    write_wav(stem + '.wav', pcm)
    write_srt(cfg, stem + '.srt')
    words = sum(len(sentence(s)[0].split()) for sc in cfg['scenes'] for s in sc['sentences'])
    speech = sum(d for sc in cfg['scenes'] for _, d, _ in sc['st'])
    print(f'Gesamtdauer {total:.1f} s ({int(total // 60)}:{int(total % 60):02d}), {words} Woerter, '
          f'Tempo {words / speech:.2f} W/s Sprechzeit')
    for sc in cfg['scenes']:
        print(f"  {sc['id']:<4} {sc['v0']:6.1f}–{sc['v1']:6.1f} s  ({sc['v1'] - sc['v0']:5.1f} s)  {sc['headline'][:50]}")
    json.dump([{k: sc[k] for k in ('id', 'v0', 'v1', 'st')} for sc in cfg['scenes']],
              open(stem + '_zeitplan.json', 'w'), ensure_ascii=False, indent=1)
    if args.nur_ton:
        return
    src = Image.open(args.grafik).convert('RGB')
    if args.bild:
        scenes = [make_scene(sc, src) for sc in cfg['scenes']]
        for t in args.bild:
            k = max(i for i, sc in enumerate(cfg['scenes']) if sc['v0'] <= t)
            scenes[k].frame(t).save(f'{stem}_bild_{t:.0f}.png')
            print('Bild', t)
        return
    if args.vorschau:
        preview(cfg, src, stem + '_vorschau.png')
        return
    render(cfg, src, total, args.ausgabe, stem + '.wav', stem + '.srt')
    print('fertig:', args.ausgabe)


if __name__ == '__main__':
    main()
