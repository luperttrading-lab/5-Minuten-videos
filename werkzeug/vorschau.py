#!/usr/bin/env python3
"""Vorschau-Seite zum Anklicken statt Videodateien im Chat (Nutzerwunsch 02.11.: Dateien landen auf dem Handy und
belegen Speicher). Aufruf: python3 vorschau.py vorschau.json <ausordner>

vorschau.json: {"titel": "Guanfacin", "aufgabe": "…", "videos": [{"datei": "hook_vorschau.mp4", "titel": "Neuer Einstieg",
"notiz": "…", "stand": "02.11., 11:13", "pruefen": true}, …]} – neueste zuerst. Videos je höchstens 16 MB (Artifact-Grenze),
also 720p/12 fps fürs ganze Video, Einstiegsproben 720p. Kein Autoplay (Browser spielen dann stumm); Ton kommt mit dem
ersten Antippen. Je Video „passt“ / „ändern“ mit Notiz: Kommentar an Claude und Sammlung `vorschau_urteile` (Dokument-ID = Hash aus
Datei, Titel und Stand, damit alte Urteile nicht auf neu eingefügte Videos rutschen).
Als Artifact mit Fähigkeiten {"db": {}, "comments": {}} veröffentlichen, Dateien unter `videos/`.
"""
import hashlib, html, json, os, shutil, subprocess, sys

cfg_pfad, aus = sys.argv[1], sys.argv[2]
basis = os.path.dirname(os.path.abspath(cfg_pfad))
cfg = json.load(open(cfg_pfad, encoding='utf-8'))
os.makedirs(os.path.join(aus, 'videos'), exist_ok=True)
esc = html.escape
karten = []
for i, v in enumerate(cfg['videos']):
    quelle = os.path.join(basis, v['datei'])
    groesse = os.path.getsize(quelle)
    if groesse > 16 * 1024 * 1024:
        sys.exit(f'{v["datei"]} ist {groesse / 1e6:.1f} MB, Grenze 16 MB')
    ziel = f'videos/v{i + 1}_{os.path.basename(v["datei"])}'
    shutil.copy(quelle, os.path.join(aus, ziel))
    poster = ziel[:-4] + '.jpg'                          # Standbild bei 4 s, sonst zeigt der Player das helle Einblenden
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(v.get('poster_bei', 4)), '-i', quelle, '-frames:v', '1',
                    '-vf', 'scale=960:-2', '-q:v', '4', os.path.join(aus, poster)], check=True)
    marke = '<span class="marke pruefen">zu prüfen</span>' if v.get('pruefen') else '<span class="marke info">zur Info</span>'
    vid = 'v_' + hashlib.sha1((v['datei'] + '|' + v['titel'] + '|' + v.get('stand', '')).encode()).hexdigest()[:10]
    karten.append(f'''<article class="video" id="v{i + 1}" data-id="{vid}" data-titel="{esc(v["titel"])}">
      <div class="kopfzeile"><h2>{esc(v["titel"])}</h2>{marke}</div>
      <p class="stand">Stand {esc(v.get("stand", ""))} · {groesse / 1e6:.1f} MB</p>
      <video controls playsinline preload="metadata" poster="{poster}" src="{ziel}"></video>
      <p class="notiz">{esc(v.get("notiz", ""))}</p>
      {'<div class="urteil"><button type="button" data-u="passt">✓ passt</button><button type="button" data-u="aendern">ändern</button></div><textarea rows="2" placeholder="Was soll anders werden?" aria-label="Notiz zu ' + esc(v["titel"]) + '"></textarea><div class="zeile"><button type="button" class="senden">An Claude</button><span class="melde" role="status" aria-live="polite"></span></div>' if v.get('pruefen') else ''}
    </article>''')

seite = f'''<title>{esc(cfg["titel"])} · Vorschau</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
  /* Eine Spalte, je Fassung eine Karte mit Player; die neueste oben. */
  :root {{ --grund: #f4f1ec; --karte: #ffffff; --tinte: #1f2430; --grau: #646b75; --linie: #ddd6cc; --akzent: #324e7a;
    --akzent-text: #ffffff; --gut: #2f7d50; --pruefen: #a35a12; --pruefen-grund: #fbebd9; }}
  @media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --grund: #15181d; --karte: #1e232a; --tinte: #e8eaee;
    --grau: #9aa3ad; --linie: #2f3640; --akzent: #8fb0e3; --akzent-text: #10151c; --gut: #6fcf97; --pruefen: #f0b067;
    --pruefen-grund: #3a2a17; color-scheme: dark }} }}
  :root[data-theme="dark"] {{ --grund: #15181d; --karte: #1e232a; --tinte: #e8eaee; --grau: #9aa3ad; --linie: #2f3640;
    --akzent: #8fb0e3; --akzent-text: #10151c; --gut: #6fcf97; --pruefen: #f0b067; --pruefen-grund: #3a2a17; color-scheme: dark }}
  * {{ box-sizing: border-box; }}
  body {{ background: var(--grund); color: var(--tinte); font: 16px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }}
  main {{ max-width: 760px; margin: 0 auto; display: grid; gap: 18px; padding-block: 24px 48px;
    padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
  h1 {{ margin: 0; font: 700 clamp(24px, 6vw, 34px)/1.15 Georgia, "Times New Roman", serif; text-wrap: balance; }}
  .aufgabe {{ margin: 0; padding: 12px 14px; border-left: 4px solid var(--pruefen); background: var(--pruefen-grund); border-radius: 6px; }}
  .video {{ display: grid; gap: 8px; padding: 14px; background: var(--karte); border: 1px solid var(--linie); border-radius: 14px; }}
  .kopfzeile {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 10px; }}
  .video h2 {{ margin: 0; font: 650 19px/1.3 system-ui, sans-serif; }}
  .marke {{ font: 600 12px/1 system-ui, sans-serif; letter-spacing: .05em; text-transform: uppercase; padding: 4px 8px; border-radius: 6px; }}
  .marke.pruefen {{ background: var(--pruefen-grund); color: var(--pruefen); }}
  .marke.info {{ background: var(--linie); color: var(--grau); }}
  .stand, .notiz {{ margin: 0; font-size: 14px; color: var(--grau); }}
  video {{ width: 100%; max-width: 100%; aspect-ratio: 16 / 9; background: #000; border-radius: 10px; }}
  .urteil {{ display: flex; gap: 8px; }}
  .urteil button, .senden {{ border: 1px solid var(--linie); background: none; color: var(--tinte); border-radius: 999px; padding: 9px 16px;
    font: 600 15px/1 system-ui, sans-serif; cursor: pointer; }}
  .urteil button[aria-pressed="true"][data-u="passt"] {{ background: var(--gut); border-color: var(--gut); color: var(--karte); }}
  .urteil button[aria-pressed="true"][data-u="aendern"] {{ background: var(--pruefen); border-color: var(--pruefen); color: var(--karte); }}
  .senden {{ background: var(--akzent); border-color: var(--akzent); color: var(--akzent-text); border-radius: 10px; }}
  textarea {{ width: 100%; font: 16px/1.4 system-ui, sans-serif; color: var(--tinte); background: var(--grund); border: 1px solid var(--linie);
    border-radius: 8px; padding: 8px 10px; resize: vertical; }}
  .zeile {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }}
  .melde {{ font-size: 14px; color: var(--gut); }}
  button:focus-visible, textarea:focus-visible {{ outline: 3px solid var(--akzent); outline-offset: 2px; }}
</style>
<main>
  <h1>{esc(cfg["titel"])} · Vorschau</h1>
  <p class="aufgabe"><b>Deine Aufgabe:</b> {esc(cfg.get("aufgabe", "Video antippen, ansehen, dann „passt“ oder „ändern“."))} Ton kommt beim Antippen von ▶; nichts wird heruntergeladen.</p>
  {"".join(karten)}
</main>
<script>
(function () {{
  var TITEL = {json.dumps(cfg["titel"], ensure_ascii=False)}, db = null, kom = null, anClaude = false, urteil = {{}};
  document.querySelectorAll("video").forEach(function (v) {{ v.addEventListener("play", function () {{
    document.querySelectorAll("video").forEach(function (w) {{ if (w !== v) w.pause(); }}); v.muted = false; }}); }});
  document.querySelectorAll(".video").forEach(function (k) {{
    var id = k.dataset.id, ta = k.querySelector("textarea"), melde = k.querySelector(".melde");
    k.querySelectorAll(".urteil button").forEach(function (b) {{ b.addEventListener("click", function () {{
      urteil[id] = b.dataset.u; k.querySelectorAll(".urteil button").forEach(function (x) {{ x.setAttribute("aria-pressed", String(x === b)); }});
      if (b.dataset.u === "aendern" && ta) ta.focus();
      if (db) db.collection("vorschau_urteile").doc(id).set({{ video: k.dataset.titel, urteil: b.dataset.u, notiz: ta ? ta.value.trim() : "", zeit: new Date().toISOString() }}).catch(function () {{}});
    }}); }});
    var s = k.querySelector(".senden"); if (!s) return;
    s.addEventListener("click", function () {{
      var text = "Vorschau " + TITEL + ": " + k.dataset.titel + " – " + ({{ passt: "PASST", aendern: "ÄNDERN" }}[urteil[id]] || "ohne Urteil") + (ta.value.trim() ? "\\nNotiz: " + ta.value.trim() : "");
      if (db) db.collection("vorschau_urteile").doc(id).set({{ video: k.dataset.titel, urteil: urteil[id] || null, notiz: ta.value.trim(), zeit: new Date().toISOString() }}).catch(function () {{}});
      if (!kom || !anClaude) {{ melde.textContent = db ? "Gespeichert. Claude liest es beim nächsten Mal." : "Bitte Claude im Chat Bescheid geben."; return; }}
      s.disabled = true;
      kom.anchorFor(k).then(function (a) {{ return kom.sendToClaude({{ anchor: a, text: text.slice(0, 3900) }}); }})
        .then(function () {{ melde.textContent = "An Claude geschickt ✓"; }}, function (e) {{ melde.textContent = e && e.code === "consent_required" ? "Gespeichert. Zum Senden bitte die Freigabe erlauben." : "Gespeichert, Senden fehlgeschlagen."; }})
        .then(function () {{ s.disabled = false; }});
    }});
  }});
  if (window.claude && claude.use) {{
    claude.use("db").then(function (d) {{ if (d) db = d; }}).catch(function () {{}});
    claude.use("comments").then(function (c) {{ if (!c || !c.canSendToClaude) return; kom = c;
      c.canSendToClaude().then(function (v) {{ anClaude = v === "available"; }}, function () {{}}); }}).catch(function () {{}});
  }}
}})();
</script>
'''
open(os.path.join(aus, 'index.html'), 'w', encoding='utf-8').write(seite)
print(f'{aus}/index.html: {len(cfg["videos"])} Videos')
