"""Ergänzt die Hörprobe um eine Bildwahl: je Szene beide Bilder, Antippen speichert die Wahl (Sammlung „bildwahl“)."""
import json, os, sys
from PIL import Image
aus = sys.argv[1] if len(sys.argv) > 1 else 'hoerprobe'
cfg = json.load(open('szenen.json', encoding='utf-8'))
os.makedirs(f'{aus}/bilder', exist_ok=True)
seite = open(f'{aus}/index.html', encoding='utf-8').read()
for sc in cfg['scenes']:
    dateien = [b['datei'] for b in sc.get('bilder', [])]
    if not dateien: continue
    fig = []
    for d in dateien:
        n = os.path.basename(d)[:-4] + '.jpg'
        Image.open(d).convert('RGB').resize((960, 540), Image.LANCZOS).save(f'{aus}/bilder/{n}', quality=82)
        fig.append(f'<button type="button" class="bw" data-sz="{sc["id"]}" data-bild="{os.path.basename(d)[:-4]}">'
                   f'<img src="bilder/{n}" alt="Bild {os.path.basename(d)[:-4]}" loading="lazy"><span>{os.path.basename(d)[-5]}</span></button>')
    anker = f'<p class="text" data-text="{sc["id"]}"></p>'
    assert anker in seite, sc['id']
    seite = seite.replace(anker, f'<div class="bildwahl">{"".join(fig)}</div>\n    <p class="bwhinweis" data-hinweis="{sc["id"]}">Welches Bild passt besser? Antippen.</p>\n    ' + anker, 1)
css = '''
  .bildwahl { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .bw { position: relative; padding: 0; border: 3px solid transparent; border-radius: 10px; overflow: hidden; background: none; cursor: pointer; }
  .bw img { display: block; width: 100%; height: auto; }
  .bw span { position: absolute; left: 6px; top: 6px; background: rgba(0,0,0,.6); color: #fff; font: 600 14px/1 var(--ui); padding: 4px 7px; border-radius: 6px; }
  .bw.gewaehlt { border-color: var(--bronze); }
  .bw.gewaehlt span::after { content: " ✓"; }
  .bwhinweis { margin: -6px 0 0; font-size: 13px; color: var(--grau); }
</style>'''
js = '''
<script>
(function () {
  var wahl = {}, db = null;
  function zeige() {
    document.querySelectorAll(".bw").forEach(function (b) { b.classList.toggle("gewaehlt", wahl[b.dataset.sz] === b.dataset.bild); });
    document.querySelectorAll("[data-hinweis]").forEach(function (p) { var w = wahl[p.dataset.hinweis];
      p.textContent = w ? "Gewählt: Bild " + w.slice(-1) + " – gespeichert." : (db ? "Welches Bild passt besser? Antippen." : "Speicher nicht erreichbar."); });
  }
  document.querySelectorAll(".bw").forEach(function (b) { b.addEventListener("click", function () {
    if (!db) return; var sz = b.dataset.sz; wahl[sz] = b.dataset.bild; zeige();
    db.collection("bildwahl").doc(sz).set({ szene: sz, bild: b.dataset.bild, zeit: new Date().toISOString() });
  }); });
  if (window.claude && claude.use) claude.use("db").then(function (d) { if (!d) return; db = d; zeige();
    db.collection("bildwahl").onSnapshot(function (snap) { (snap.docs || []).forEach(function (x) { var v = x.data ? x.data() : x.d || x; if (v && v.szene) wahl[v.szene] = v.bild; }); zeige(); });
  });
})();
</script>
</body>'''
assert '</style>' in seite
seite = seite.replace('</style>', css, 1)
seite = seite.replace('</body>', js, 1) if '</body>' in seite else seite.rstrip() + '\n' + js.replace('</body>', '')
open(f'{aus}/index.html', 'w', encoding='utf-8').write(seite)
print('Bildwahl eingefügt')
