#!/usr/bin/env python3
"""Ergänzt die Hörprobe um Bildwahl und Kapitelnotizen: python3 bildwahl.py szenen.json <hoerprobe-ordner>

Je Szene stehen alle Bilder nebeneinander. Antippen wählt ein Bild, nochmal antippen wählt es ab; mehrere Bilder in der
Reihenfolge des Antippens = diese Bilder in dieser Reihenfolge im Video. Gespeichert in der Sammlung „bildwahl“
({szene, bilder: [..in Reihenfolge..], bild: erstes}). Dazu je Szene „Notiz zum ganzen Kapitel“: schreibt in die Sammlung
„kapitelnotizen“ und schickt die Notiz als Kommentar an Claude (allgemeine Änderungswünsche, keine Textstelle).
Lesen: ArtifactData list, Sammlungen „bildwahl“ und „kapitelnotizen“. Nach hoerprobe.py aufrufen, vor dem Veröffentlichen.
"""
import html, json, os, sys
from PIL import Image

szenen, aus = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'hoerprobe'
basis = os.path.dirname(os.path.abspath(szenen))
cfg = json.load(open(szenen, encoding='utf-8'))
os.makedirs(f'{aus}/bilder', exist_ok=True)
seite = open(f'{aus}/index.html', encoding='utf-8').read()
kap = html.escape(cfg.get('titel') or os.path.basename(basis))
for sc in cfg['scenes']:
    dateien = [b['datei'] for b in sc.get('bilder', [])]
    if not dateien:
        continue
    fig = []
    for d in dateien:
        name = os.path.basename(d)[:-4]
        Image.open(os.path.join(basis, d)).convert('RGB').resize((960, 540), Image.LANCZOS).save(f'{aus}/bilder/{name}.jpg', quality=82)
        fig.append(f'<button type="button" class="bw" data-sz="{sc["id"]}" data-bild="{name}">'
                   f'<img src="bilder/{name}.jpg" alt="Bild {name}" loading="lazy"><span>{name[-1]}</span></button>')
    anker = f'<p class="text" data-text="{sc["id"]}"></p>'
    assert anker in seite, sc['id']
    titel = html.escape(sc.get('headline') or sc.get('kapitel') or sc['id'])
    block = (f'<div class="bildwahl">{"".join(fig)}</div>\n'
             f'    <p class="bwhinweis" data-hinweis="{sc["id"]}">Bild antippen. Beide antippen = beide, in dieser Reihenfolge.</p>\n'
             f'    {anker}\n'
             f'    <details class="kapnotiz" data-kn="{sc["id"]}" data-titel="{titel}"><summary>Notiz zum ganzen Kapitel</summary>'
             f'<textarea rows="3" placeholder="Allgemeiner Wunsch zu dieser Szene, keine einzelne Textstelle"></textarea>'
             f'<div class="kn-zeile"><button type="button" class="kn-senden">An Claude</button><span class="kn-stand"></span></div></details>')
    seite = seite.replace(anker, block, 1)
css = '''
  .bildwahl { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .bw { position: relative; padding: 0; border: 3px solid transparent; border-radius: 10px; overflow: hidden; background: none; cursor: pointer; }
  .bw img { display: block; width: 100%; height: auto; }
  .bw span { position: absolute; left: 6px; top: 6px; background: rgba(0,0,0,.6); color: #fff; font: 600 14px/1 var(--ui); padding: 4px 7px; border-radius: 6px; }
  .bw.gewaehlt { border-color: var(--bronze); }
  .bw.gewaehlt span { background: var(--bronze); color: var(--stein); }
  .bw.gewaehlt span::after { content: " · " attr(data-n) "."; }
  .bwhinweis { margin: -6px 0 0; font-size: 13px; color: var(--grau); }
  .kapnotiz { border: 1px dashed var(--linie); border-radius: 10px; padding: 8px 12px; font-size: 14px; color: var(--grau); }
  .kapnotiz summary { cursor: pointer; color: var(--bronze); font: 600 13px/1.4 var(--ui); }
  .kapnotiz textarea { width: 100%; margin-top: 8px; font: 15px/1.4 var(--ui); color: var(--tinte); background: var(--stein); border: 1px solid var(--linie); border-radius: 8px; padding: 8px; resize: vertical; }
  .kn-zeile { display: flex; gap: 10px; align-items: center; margin-top: 6px; }
  .kn-senden { border: 0; border-radius: 8px; background: var(--bronze); color: var(--stein); font: 600 14px/1 var(--ui); padding: 9px 12px; cursor: pointer; }
  .kn-senden:disabled { background: var(--linie); color: var(--grau); cursor: default; }
  .kn-stand { font-size: 13px; }
</style>'''
js = '''
<script>
(function () {
  var KAPITEL = %s, wahl = {}, db = null, kom = null, anClaude = false;
  function zeige() {
    document.querySelectorAll(".bw").forEach(function (b) { var l = wahl[b.dataset.sz] || [], i = l.indexOf(b.dataset.bild);
      b.classList.toggle("gewaehlt", i >= 0); b.querySelector("span").dataset.n = i + 1; });
    document.querySelectorAll("[data-hinweis]").forEach(function (p) { var l = wahl[p.dataset.hinweis] || [];
      p.textContent = !db ? "Speicher nicht erreichbar." : l.length === 0 ? "Bild antippen. Beide antippen = beide, in dieser Reihenfolge."
        : l.length === 1 ? "Gewählt: nur Bild " + l[0].slice(-1) + " – gespeichert." : "Gewählt: erst " + l.map(function (x) { return x.slice(-1); }).join(", dann ") + " – gespeichert."; });
  }
  document.querySelectorAll(".bw").forEach(function (b) { b.addEventListener("click", function () {
    if (!db) return; var sz = b.dataset.sz, l = (wahl[sz] || []).slice(), i = l.indexOf(b.dataset.bild);
    if (i >= 0) l.splice(i, 1); else l.push(b.dataset.bild); wahl[sz] = l; zeige();
    db.collection("bildwahl").doc(sz).set({ szene: sz, bilder: l, bild: l[0] || null, zeit: new Date().toISOString() });
  }); });
  document.querySelectorAll(".kapnotiz").forEach(function (k) {
    var ta = k.querySelector("textarea"), kn = k.querySelector(".kn-senden"), st = k.querySelector(".kn-stand");
    kn.addEventListener("click", function () {
      var text = ta.value.trim(); if (!text || !db) return; kn.disabled = true;
      var sz = k.dataset.kn, id = sz + "-" + Date.now().toString(36), jetzt = new Date().toISOString();
      db.collection("kapitelnotizen").doc(id).set({ szene: sz, titel: k.dataset.titel, text: text, zeit: jetzt, status: "abgeschickt" });
      var t = "Hörprobe " + KAPITEL + ", Kapitelnotiz zu Szene " + sz + " (" + k.dataset.titel + ")\\nNotiz: " + text;
      var el = document.getElementById(sz) || document.querySelector("main");
      if (kom && anClaude) kom.anchorFor(el).then(function (a) { return kom.sendToClaude({ anchor: a, text: t.slice(0, 3900) }); })
        .then(function () { st.textContent = "An Claude geschickt ✓"; ta.value = ""; kn.disabled = false; },
              function (e) { st.textContent = e && e.code === "consent_required" ? "Gespeichert. Zum Senden an Claude bitte die Freigabe erlauben." : "Gespeichert, Senden fehlgeschlagen."; kn.disabled = false; });
      else { st.textContent = "Gespeichert ✓ (Claude liest es beim nächsten Mal)"; ta.value = ""; kn.disabled = false; }
    });
  });
  if (window.claude && claude.use) {
    claude.use("db").then(function (d) { if (!d) return; db = d; zeige();
      db.collection("bildwahl").onSnapshot(function (snap) { (snap.docs || []).forEach(function (x) { var v = x.data ? x.data() : x.d || x;
        if (v && v.szene) wahl[v.szene] = v.bilder || (v.bild ? [v.bild] : []); }); zeige(); });
    });
    claude.use("comments").then(function (c) { if (!c || !c.canSendToClaude) return; kom = c;
      c.canSendToClaude().then(function (v) { anClaude = v === "available"; }, function () {}); }).catch(function () {});
  } else zeige();
})();
</script>
</body>''' % json.dumps(kap, ensure_ascii=False)
assert '</style>' in seite
seite = seite.replace('</style>', css, 1)
seite = seite.replace('</body>', js, 1) if '</body>' in seite else seite.rstrip() + '\n' + js.replace('</body>', '')
open(f'{aus}/index.html', 'w', encoding='utf-8').write(seite)
print('Bildwahl und Kapitelnotizen eingefügt')
