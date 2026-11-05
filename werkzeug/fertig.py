#!/usr/bin/env python3
"""Seite „fertige Videos“: je Folge nur die abgenommene Fassung, ohne Auswahl und Proben (Nutzerwunsch 05.11.:
das aktuelle Video nicht auf der Vorschau-Seite suchen müssen). Mit YouTube-Titel (Kopieren-Knopf) und Vorschaubild.

Aufruf: python3 fertig.py fertig.json <ausgabeordner>
fertig.json: {"titel": …, "videos": [{"name", "datei" (720p), "youtube_titel", "vorschaubild", "stand", "laenge"}]}
Pfade relativ zu fertig.json oder absolut. Die Dateien heißen nach dem Namen der Folge, damit ein Neu-Hochladen nur
die geänderte Folge betrifft.
"""
import html, json, os, re, shutil, sys

cfg_pfad, aus = sys.argv[1], sys.argv[2]
basis = os.path.dirname(os.path.abspath(cfg_pfad))
cfg = json.load(open(cfg_pfad, encoding='utf-8'))
os.makedirs(os.path.join(aus, 'dateien'), exist_ok=True)
esc = html.escape
karten = []
for v in cfg['videos']:
    kurz = re.sub(r'[^a-z0-9]+', '-', v['name'].lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')).strip('-')
    stand = re.sub(r'[^0-9]+', '', v.get('stand', ''))     # neue Fassung = neuer Name, kein alter Stand im Zwischenspeicher
    video = f'dateien/{kurz}_{stand}.mp4'
    bild = f'dateien/{kurz}_{stand}_vorschaubild.png'
    q = os.path.join(basis, v['datei'])
    if os.path.getsize(q) > 16 * 1024 * 1024:
        sys.exit(f'{q}: größer als 16 MB')
    shutil.copy(q, os.path.join(aus, video))
    shutil.copy(os.path.join(basis, v['vorschaubild']), os.path.join(aus, bild))
    karten.append(f'''<article>
  <h2>{esc(v["name"])}</h2>
  <p class="stand">Fertig seit {esc(v.get("stand", ""))} · {esc(v.get("laenge", ""))}</p>
  <video controls playsinline preload="metadata" poster="{bild}" src="{video}"></video>
  <h3>YouTube-Titel</h3>
  <div class="titel"><span>{esc(v["youtube_titel"])}</span><button type="button" data-text="{esc(v["youtube_titel"])}">Kopieren</button></div>
  <h3>Vorschaubild</h3>
  <img src="{bild}" alt="Vorschaubild {esc(v["name"])}">
</article>''')

seite = f'''<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(cfg["titel"])}</title>
<style>
  :root {{ --grund: #f6f1e7; --karte: #ffffff; --tinte: #2b2d42; --grau: #6f7380; --teal: #0f766e; --linie: #e6dfd2; }}
  @media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --grund: #1d1f2b; --karte: #2b2d42;
    --tinte: #f1ede4; --grau: #a9adb8; --linie: #3a3d55; }} }}
  :root[data-theme="dark"] {{ --grund: #1d1f2b; --karte: #2b2d42; --tinte: #f1ede4; --grau: #a9adb8; --linie: #3a3d55; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--grund); color: var(--tinte); font: 16px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }}
  main {{ max-width: 760px; margin: 0 auto; padding: 20px 16px 48px; }}
  h1 {{ font: 700 24px/1.2 system-ui, sans-serif; margin: 4px 0 4px; }}
  .unter {{ color: var(--grau); margin: 0 0 20px; }}
  article {{ background: var(--karte); border: 1px solid var(--linie); border-radius: 14px; padding: 16px; margin-bottom: 20px; }}
  h2 {{ margin: 0; font: 700 20px/1.3 system-ui, sans-serif; }}
  h3 {{ margin: 18px 0 6px; font: 600 13px/1 system-ui, sans-serif; letter-spacing: .05em; text-transform: uppercase; color: var(--grau); }}
  .stand {{ color: var(--grau); margin: 2px 0 12px; font-size: 14px; }}
  video, img {{ width: 100%; border-radius: 10px; display: block; background: #000; }}
  img {{ background: none; border: 1px solid var(--linie); }}
  .titel {{ display: flex; gap: 10px; align-items: center; }}
  .titel span {{ flex: 1; font-weight: 600; }}
  button {{ font: 600 15px/1 system-ui, sans-serif; padding: 10px 14px; border-radius: 10px; border: 0; background: var(--teal);
    color: #fff; cursor: pointer; white-space: nowrap; }}
</style></head>
<body><main>
<h1>{esc(cfg["titel"])}</h1>
<p class="unter">Nur die abgenommenen Fassungen. Auswahl und Proben stehen auf der Vorschau-Seite.</p>
{"".join(karten)}
</main>
<script>
document.querySelectorAll('button[data-text]').forEach(b => b.addEventListener('click', async () => {{
  try {{ await navigator.clipboard.writeText(b.dataset.text); b.textContent = 'Kopiert ✓'; }}
  catch (e) {{ b.textContent = 'Bitte markieren'; }}
  setTimeout(() => b.textContent = 'Kopieren', 2000);
}}));
</script>
</body></html>'''
open(os.path.join(aus, 'index.html'), 'w', encoding='utf-8').write(seite)
print(os.path.join(aus, 'index.html'), len(karten), 'Videos')
