#!/usr/bin/env python3
"""Kontaktbogen aller Bildausschnitte (weitester Zoom, wie zu Beginn der Einstellung). Aufruf: python3 ausschnitte_pruefen.py szenen.json bogen.png [grafik.png]"""
import sys, json
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image, ImageDraw
src = Image.open(sys.argv[3] if len(sys.argv) > 3 else 'grafik_korrigiert.png').convert('RGB')
cfg = json.load(open(sys.argv[1], encoding='utf-8'))
R.BILD_DIR = os.path.dirname(os.path.abspath(sys.argv[1]))
thumbs = []
for sc in cfg['scenes']:
    items = []
    if sc.get('layout') == 'kacheln':
        for j, k in enumerate(sc['kacheln']):
            img, a = R.quelle(k, src, 500 / 270)
            items.append((f"{sc['id']} K{j+1}", a, None, None, img))
    for j, sh in enumerate(sc.get('shots', [])):
        img, a0 = R.quelle(sh, src)
        b0 = sh.get('b')
        if isinstance(sh.get('zoom'), (int, float)):
            z = 1 - sh['zoom']; cx, cy = (a0[0] + a0[2]) / 2, (a0[1] + a0[3]) / 2
            hw, hh = (a0[2] - a0[0]) * z / 2, (a0[3] - a0[1]) * z / 2
            b0 = [cx - hw, cy - hh, cx + hw, cy + hh]
        size, a, b = R.fit_box(a0, a0 if sh.get('zoom') == 'none' else b0, img.size)
        if sh.get('zoom') == 'out':
            a, b = b, a
        tight = max((a, b), key=lambda x: (x[2]-x[0]) * (x[3]-x[1]))
        items.append((f"{sc['id']} E{j+1}", tight, size, sh, img))
    for name, box, size, sh, img in items:
        bw, bh = box[2]-box[0], box[3]-box[1]
        s = min(300 / bw, 260 / bh)
        tsize = (max(int(bw * s), 10), max(int(bh * s), 10))
        pic = img.resize(tsize, Image.BICUBIC, box=tuple(box))
        if size:   # Maske wie im Video (skaliert)
            m = R.mask(size).resize(tsize)
            bg = Image.new('RGB', tsize, R.PAPER); bg.paste(pic, (0, 0), m); pic = bg
        t = Image.new('RGB', (320, 300), 'white')
        t.paste(pic, ((320 - tsize[0]) // 2, 4 + (260 - tsize[1]) // 2))
        ImageDraw.Draw(t).text((6, 272), name, font=R.font(R.INTER.format('Bold'), 20), fill=(200, 30, 30))
        thumbs.append(t)
cols = 6
rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new('RGB', (cols * 325, rows * 305), (200, 200, 200))
for i, t in enumerate(thumbs):
    sheet.paste(t, ((i % cols) * 325, (i // cols) * 305))
sheet.save(sys.argv[2]); print(len(thumbs), 'Ausschnitte')
