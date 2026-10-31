#!/usr/bin/env python3
"""Beschreibungstext (YouTube) und Teilen-Seite aus Drehbuch und Zeitplan erzeugen.
Titel, Untertitel und Fusszeile kommen aus dem Drehbuch (titel, untertitel, fuss).

Aufruf: python3 beschreibung.py szenen.json zeitplan.json
Schreibt beschreibung_youtube.txt und web_teilen/index.html. Quellen tragen dieselben Nummern wie im Video.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render  # noqa: E402

TITEL = 'Chronischer Stress: Was hilft wirklich?'
UNTER = 'Ein Faktencheck populärer Anti-Stress-Tipps. Jeder Punkt ist gegen Studien geprüft; die Marker zeigen, wie gut er belegt ist.'
FUSS = 'Sprecherstimme synthetisch (ElevenLabs). Illustrationen KI-generiert, Tippfehler korrigiert. Kein Ersatz für ärztlichen Rat.'


def zeit(t):
    return f'{int(t // 60)}:{int(t % 60):02d}'


def main():
    cfg = json.load(open(sys.argv[1], encoding='utf-8'))
    global TITEL, UNTER, FUSS
    TITEL, UNTER, FUSS = cfg.get('titel', TITEL), cfg.get('untertitel', UNTER), cfg.get('fuss', FUSS)
    plan = {z['id']: z for z in json.load(open(sys.argv[2], encoding='utf-8'))}
    order = render.number_sources(cfg)
    reg = cfg['quellen']
    kapitel = [(plan[sc['id']]['v0'], sc.get('kapitel', sc['headline'])) for sc in cfg['scenes']]

    # ---- YouTube: reiner Text, Links werden dort automatisch klickbar
    def text(kurz):
        q = [f"[{i}] {reg[k]['kurz'] if kurz else reg[k]['voll']}: {reg[k]['url']}" for i, k in enumerate(order, 1)]
        return '\n'.join([TITEL, UNTER, '', 'Kapitel'] + [f'{zeit(t)} {n}' for t, n in kapitel] +
                         ['', 'Quellen (Nummern wie im Video)'] + q + ['', FUSS]) + '\n'
    out = text(False)
    if len(out) > 4900:                     # YouTube erlaubt 5000 Zeichen
        out = text(True)
    open('beschreibung_youtube.txt', 'w', encoding='utf-8').write(out)
    print(f'beschreibung_youtube.txt: {len(out)} Zeichen, {len(order)} Quellen')

    # ---- Teilen-Seite
    kurz = ('  <h2>Kurzfassung (1 Minute)</h2>\n  <div class="short"><video controls playsinline preload="metadata" src="kurz.mp4"></video></div>\n'
            if cfg.get('kurzfassung') else '')
    kap = '\n'.join(f'    <button data-t="{t:.1f}">{zeit(t)} · {html.escape(n)}</button>' for t, n in kapitel)
    qu = '\n'.join(f'      <li><a href="{html.escape(reg[k]["url"])}">{html.escape(reg[k]["voll"])}</a></li>'
                   for k in order)
    page = f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITEL}</title>
<style>
  :root {{ color-scheme: light dark; --ink:#222632; --muted:#6f6a66; --bg:#faf3ea; --card:#fffaf3; --accent:#324e7a; --line:#e6dccf; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --ink:#ece7e0; --muted:#a8a29b; --bg:#1c1b1a; --card:#262422; --accent:#8fb0e3; --line:#3a3633; }} }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font:16px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif; }}
  main {{ max-width:780px; margin:0 auto; padding:22px 16px 56px; }}
  h1 {{ font-family: Georgia, "Times New Roman", serif; font-size:1.7rem; line-height:1.2; margin:.1em 0 .35em; }}
  .lead {{ color:var(--muted); margin:0 0 18px; }}
  video {{ width:100%; border-radius:12px; display:block; background:#000; }}
  .kap {{ display:flex; flex-wrap:wrap; gap:6px; margin:12px 0 26px; }}
  .kap button {{ font:inherit; font-size:.85rem; padding:6px 10px; border-radius:999px; border:1px solid var(--line); background:var(--card); color:var(--ink); cursor:pointer; }}
  h2 {{ font-size:1.15rem; margin:28px 0 10px; }}
  .short video {{ max-width:340px; margin:0 auto; }}
  details {{ background:var(--card); border-radius:12px; padding:12px 14px; border:1px solid var(--line); }}
  summary {{ cursor:pointer; font-weight:600; }}
  ol {{ margin:10px 0 0; padding-left:30px; }} li {{ margin:4px 0; font-size:.92rem; }}
  a {{ color:var(--accent); }}
  .fuss {{ color:var(--muted); font-size:.85rem; margin-top:26px; }}
</style>
</head>
<body>
<main>
  <h1>{TITEL}</h1>
  <p class="lead">{UNTER}</p>
  <video id="v" controls playsinline preload="metadata" src="video.mp4"></video>
  <div class="kap">
{kap}
  </div>
{kurz}  <h2>Quellen</h2>
  <details><summary>Alle {len(order)} Quellen (Nummern wie im Video)</summary>
    <ol>
{qu}
    </ol>
  </details>
  <p class="fuss">{FUSS}</p>
</main>
<script>
  const v = document.getElementById('v');
  document.querySelectorAll('.kap button').forEach(b => b.addEventListener('click', () => {{
    v.currentTime = parseFloat(b.dataset.t); v.play().catch(() => {{}});
  }}));
</script>
</body>
</html>
'''
    os.makedirs('web_teilen', exist_ok=True)
    open('web_teilen/index.html', 'w', encoding='utf-8').write(page)
    print('web_teilen/index.html geschrieben')


if __name__ == '__main__':
    main()
