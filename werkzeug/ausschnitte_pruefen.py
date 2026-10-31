#!/usr/bin/env python3
"""Kontaktbogen aller Bildausschnitte im engsten Zoom. Aufruf: python3 ausschnitte_pruefen.py szenen.json bogen.png [grafik.png]"""
import sys, json
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image, ImageDraw
src = Image.open(sys.argv[3] if len(sys.argv) > 3 else 'grafik_korrigiert.png').convert('RGB')
cfg = json.load(open(sys.argv[1], encoding='utf-8'))
thumbs = []
for sc in cfg['scenes']:
    items = []
    if sc.get('layout') == 'kacheln':
        for j, k in enumerate(sc['kacheln']):
            items.append((f"{sc['id']} K{j+1}", k['a'], None, None))
    for j, sh in enumerate(sc.get('shots', [])):
        size, a, b = R.fit_box(sh['a'], sh['a'] if sh.get('zoom') == 'none' else sh.get('b'), src.size)
        if sh.get('zoom') == 'out':
            a, b = b, a
        tight = min((a, b), key=lambda x: (x[2]-x[0]) * (x[3]-x[1]))
        items.append((f"{sc['id']} E{j+1}", tight, size, sh))
    for name, box, size, sh in items:
        bw, bh = box[2]-box[0], box[3]-box[1]
        s = min(300 / bw, 260 / bh)
        tsize = (max(int(bw * s), 10), max(int(bh * s), 10))
        pic = src.resize(tsize, Image.BICUBIC, box=tuple(box))
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
