#!/usr/bin/env python3
"""Kurzclip im Hochformat (1080x1920) mit eingebrannten Untertiteln und Urteils-Stempel.

Aufruf wie render.py:
  python3 render_short.py short.json grafik.png ausgabe.mp4 [--nur-ton] [--bild T]
Nutzt Ton, Untertitel und Kamerafahrt aus render.py; nur das Layout ist eigenes.
"""
import argparse
import math
import os
import subprocess
import sys
import time

import numpy as np
from PIL import Image, ImageDraw

import render as R

W, H, FPS = 1080, 1920, 25
BG = (247, 239, 227)
INK, ACCENT = R.INK, R.ACCENT
PIC = (40, 430, 1040, 1250)
VERDICT = {
    'belegt': ((52, 128, 86), 'check'),
    'teilweise': ((190, 136, 30), 'tilde'),
    'falsch': ((178, 52, 48), 'cross'),
}
# knappere Pausen als im langen Video
R.GAP_SENT, R.GAP_SCENE, R.PRE, R.LEAD, R.TAIL = 0.18, 0.55, 0.35, 0.45, 1.4
R.PIC = PIC
R.MAX_SCALE = 3.4


def base_frame(sc):
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    y = 150
    if sc.get('kicker'):
        d.text((W // 2, y), sc['kicker'].upper(), font=R.font(R.INTER.format('Bold'), 36), fill=ACCENT, anchor='mt')
        y += 62
    fh = R.font(R.SERIF_B, 78)
    for line in R.wrap(d, sc['headline'], fh, W - 120):
        d.text((W // 2, y), line, font=fh, fill=INK, anchor='mt')
        y += 86
    return img


def verdict_layer(v):
    col, icon = VERDICT[v['type']]
    layer = Image.new('RGBA', (W, 130), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = R.font(R.INTER.format('Bold'), 50)
    tw = d.textlength(v['label'], font=f)
    bw = int(tw + 150)
    x0 = (W - bw) // 2
    d.rounded_rectangle([x0, 10, x0 + bw, 120], radius=55, fill=col)
    cx, cy = x0 + 62, 65
    if icon == 'check':
        d.line([(cx - 22, cy), (cx - 6, cy + 18), (cx + 24, cy - 18)], fill='white', width=10, joint='curve')
    elif icon == 'cross':
        d.line([(cx - 18, cy - 18), (cx + 18, cy + 18)], fill='white', width=10)
        d.line([(cx - 18, cy + 18), (cx + 18, cy - 18)], fill='white', width=10)
    else:
        d.arc([cx - 24, cy - 14, cx, cy + 14], 200, 340, fill='white', width=9)
        d.arc([cx, cy - 14, cx + 24, cy + 14], 20, 160, fill='white', width=9)
    d.text((x0 + 112, 65), v['label'], font=f, fill='white', anchor='lm')
    return layer


def chunks(cfg):
    """Untertitel in kurze Happen (max. 2 Zeilen à ca. 24 Zeichen), Zeit anteilig nach Zeichen."""
    out = []
    for sc in cfg['scenes']:
        for t0, dur, text in sc['st']:
            import re
            clauses = re.split(r'(?<=[,:.?!])\s+', text)          # zuerst an Satzzeichen trennen
            joined = []
            for c in clauses:                                     # "Tipp eins:" mit dem Folgenden verbinden
                if joined and len(joined[-1]) < 12 and joined[-1].endswith(':'):
                    joined[-1] += ' ' + c
                else:
                    joined.append(c)
            parts = []
            for c in joined:
                cur, sub = [], []
                for w in c.split():
                    if cur and len(' '.join(cur + [w])) > 40:
                        sub.append(' '.join(cur))
                        cur = []
                    cur.append(w)
                sub.append(' '.join(cur))
                if len(sub) > 1 and len(sub[-1]) < 12:          # keine Waisen wie "Stress."
                    tail = sub.pop()
                    sub[-1] += ' ' + tail
                parts.extend(sub)
            merged = []
            for p in parts:                                       # kurze Happen ("wann und wie,") anhaengen
                if merged and len(p) < 15 and len(merged[-1]) + len(p) <= 44:
                    merged[-1] += ' ' + p
                else:
                    merged.append(p)
            parts = merged
            n = sum(len(p) for p in parts)
            a = t0
            for p in parts:
                b = a + dur * len(p) / n
                out.append((a, b, p))
                a = b
    return out


class Short:
    def __init__(self, sc, src):
        self.sc, self.src = sc, src
        self.base = base_frame(sc)
        st = sc['st']
        v = sc.get('verdict')
        self.v_layer = verdict_layer(v) if v else None
        self.v_t = st[v.get('at', 0)][0] + 0.2 if v else None
        self.shots = []
        for j, sh in enumerate(sc['shots']):
            t0 = sc['v0'] if j == 0 else st[sh['at']][0] - 0.25
            size, a, b = R.fit_box(sh['a'], sh.get('b'), src.size)
            if sh.get('zoom') == 'out':
                a, b = b, a
            self.shots.append({'t0': t0, 'size': size, 'a': a, 'b': b})
        for j, sh in enumerate(self.shots):
            sh['t1'] = self.shots[j + 1]['t0'] if j + 1 < len(self.shots) else sc['v1']

    def shot(self, j, t):
        sh = self.shots[j]
        u = R.ease((t - sh['t0']) / (sh['t1'] - sh['t0'] + R.XF_SHOT))
        box = tuple(a + (b - a) * u for a, b in zip(sh['a'], sh['b']))
        pic = self.src.resize(sh['size'], Image.BICUBIC, box=box)
        img = self.base.copy()
        px = PIC[0] + (PIC[2] - PIC[0] - sh['size'][0]) // 2
        py = PIC[1] + (PIC[3] - PIC[1] - sh['size'][1]) // 2
        img.paste(pic, (px, py), R.mask(sh['size']))
        return img

    def frame(self, t):
        j = max([i for i, sh in enumerate(self.shots) if sh['t0'] <= t] or [0])
        img = self.shot(j, t)
        if j + 1 < len(self.shots) and t > self.shots[j]['t1'] - R.XF_SHOT:
            img = Image.blend(img, self.shot(j + 1, self.shots[j + 1]['t0']),
                              (t - (self.shots[j]['t1'] - R.XF_SHOT)) / R.XF_SHOT)
        if self.v_layer is not None and t >= self.v_t:
            a = min((t - self.v_t) / 0.25, 1.0)
            s = 1.25 - 0.25 * a                         # Stempel: kurz gross, dann normal
            lay = self.v_layer.resize((int(W * s), int(130 * s)), Image.BICUBIC)
            if a < 1:
                lay.putalpha(lay.getchannel('A').point(lambda p: int(p * a)))
            img.paste(lay, ((W - lay.width) // 2, 1290 - (lay.height - 130) // 2), lay)
        return img


def draw_sub(img, text):
    d = ImageDraw.Draw(img)
    f = R.font(R.INTER.format('ExtraBold'), 60)
    lines = R.wrap(d, text, f, W - 140)
    y = 1470
    for line in lines[:2]:
        d.text((W // 2, y), line, font=f, fill=INK, anchor='mt', stroke_width=6, stroke_fill=BG)
        y += 76


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('szenen')
    ap.add_argument('grafik')
    ap.add_argument('ausgabe')
    ap.add_argument('--nur-ton', action='store_true')
    ap.add_argument('--bild', type=float, action='append')
    ap.add_argument('--ton-dir')
    ap.add_argument('--cache', default=None, help='Standard: tts_cache neben dem Drehbuch')
    args = ap.parse_args()
    args.cache = args.cache or os.path.join(os.path.dirname(os.path.abspath(args.szenen)), 'tts_cache')
    import json
    cfg = json.load(open(args.szenen, encoding='utf-8'))
    total, pcm = R.build_audio(cfg, args)
    stem = os.path.splitext(args.ausgabe)[0]
    R.write_wav(stem + '.wav', pcm)
    R.write_srt(cfg, stem + '.srt')
    print(f'Gesamtdauer {total:.1f} s')
    if args.nur_ton:
        return
    src = Image.open(args.grafik).convert('RGB')
    scenes = [Short(sc, src) for sc in cfg['scenes']]
    subs = chunks(cfg)

    def full(t):
        k = max(i for i, sc in enumerate(cfg['scenes']) if sc['v0'] <= t)
        img = scenes[k].frame(t)
        if k + 1 < len(scenes) and t > cfg['scenes'][k]['v1'] - R.XF_SCENE:
            nxt = scenes[k + 1].frame(cfg['scenes'][k + 1]['v0'])
            img = Image.blend(img, nxt, (t - (cfg['scenes'][k]['v1'] - R.XF_SCENE)) / R.XF_SCENE)
        cur = [p for a, b, p in subs if a <= t < b + 0.12]
        if cur:
            draw_sub(img, cur[-1])
        arr = np.array(img)
        x = int(W * min(t / total, 1))
        arr[:8, :] = R.TRACK
        arr[:8, :x] = ACCENT
        return arr

    if args.bild:
        for t in args.bild:
            Image.fromarray(full(t)).save(f'{stem}_bild_{t:.0f}.png')
        return
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-i', stem + '.wav', '-map', '0:v', '-map', '1:a',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p',
           '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2',
           '-movflags', '+faststart', '-t', f'{total:.2f}', args.ausgabe]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t_start = time.time()
    for f in range(int(math.ceil(total * FPS))):
        p.stdin.write(full(f / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        sys.exit('ffmpeg-Fehler')
    print(f'fertig: {args.ausgabe} ({time.time() - t_start:.0f} s)')


if __name__ == '__main__':
    main()
