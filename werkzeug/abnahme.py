#!/usr/bin/env python3
"""Abnahme-Kasten oben auf der Hörprobe: python3 abnahme.py szenen.json <hoerprobe-ordner> abnahme.json

Damit der Nutzer nicht suchen muss (Wunsch 02.11.): ganz oben steht, was sich seit seinem letzten Durchgang geändert hat,
jede Stelle mit eigenem ▶ (spielt genau diesen Satz aus audio/ganz.mp3), je Stelle „passt“ / „nochmal“, und darunter
EIN Knopf „Abnehmen und rendern“ bzw. „Noch nicht“ mit Notiz. Beides geht als Kommentar an Claude (weckt die Sitzung)
und landet in der Sammlung `abnahme` (Dokument `gesamt`: status ok | nochmal, notiz, stellen).

abnahme.json: {"seit": "Durchgang vom 02.11., 9:13", "stellen": [{"suche": "Textanfang des Satzes", "was": "Kurzlabel"}]}
Die Sätze werden über ihren Textanfang im Zeitplan gefunden (robust gegen verschobene Satznummern).
Nach hoerprobe.py und bildwahl.py aufrufen, vor dem Veröffentlichen.
"""
import html, json, os, sys

szenen, aus, liste = sys.argv[1], sys.argv[2], sys.argv[3]
basis = os.path.dirname(os.path.abspath(szenen))
cfg = json.load(open(szenen, encoding='utf-8'))
zp = json.load(open(os.path.join(basis, 'video_zeitplan.json'), encoding='utf-8'))
ab = json.load(open(liste, encoding='utf-8'))
titel = {sc['id']: (sc.get('kapitel') or sc.get('headline') or sc['id']) for sc in cfg['scenes']}
stellen = []
for s in ab['stellen']:
    treffer = [(z['id'], t0, d, txt) for z in zp for (t0, d, txt) in z['st'] if txt.startswith(s['suche'])]
    if len(treffer) != 1:
        sys.exit(f'Stelle nicht eindeutig gefunden ({len(treffer)}): {s["suche"]}')
    sid, t0, d, txt = treffer[0]
    stellen.append({'id': f'a{len(stellen) + 1}', 'szene': sid, 'kapitel': titel.get(sid, sid), 'was': s['was'],
                    'text': txt, 't0': round(t0 - 0.15, 2), 't1': round(t0 + d + 0.25, 2)})
mm = lambda t: f'{int(t // 60)}:{int(t % 60):02d}'
items = ''.join(
    f'<li data-id="{s["id"]}"><button type="button" class="ab-play" data-t0="{s["t0"]}" data-t1="{s["t1"]}" '
    f'aria-label="Stelle {i + 1} anhören">▶</button><div class="ab-inhalt"><b>{i + 1}. {html.escape(s["was"])}</b>'
    f'<small>{html.escape(s["kapitel"])} · bei {mm(s["t0"] + 0.15)}</small><q>{html.escape(s["text"])}</q>'
    f'<div class="ab-urteil"><button type="button" data-u="ok">passt</button><button type="button" data-u="nochmal">nochmal</button></div>'
    f'</div></li>' for i, s in enumerate(stellen))
box = f'''<section class="ab-box" id="abnahme" aria-labelledby="ab-titel">
    <h2 id="ab-titel">Deine Abnahme: {len(stellen)} Stellen sind neu</h2>
    <p class="ab-lead">Seit {html.escape(ab.get("seit", "deinem letzten Durchgang"))}. Tippe ▶ bei jeder Stelle, dann „passt“ oder „nochmal“. Unten ein Knopf für alles.</p>
    <ol class="ab-liste">{items}</ol>
    <textarea id="ab-notiz" rows="2" placeholder="Notiz (nur nötig bei „nochmal“)"></textarea>
    <div class="ab-knoepfe"><button type="button" class="ab-ok" id="ab-ok">✓ Abnehmen und rendern</button>
    <button type="button" class="ab-nein" id="ab-nein">Noch nicht, Notiz an Claude</button></div>
    <p class="ab-stand" id="ab-stand" role="status" aria-live="polite"></p>
    <audio id="ab-ton" preload="none" src="audio/ganz.mp3"></audio>
  </section>
'''
css = '''
  .ab-box { display: grid; gap: 12px; padding: 16px; border: 2px solid var(--bronze); border-radius: 16px; background: var(--tafel-hoch); }
  .ab-box h2 { margin: 0; font: 600 20px/1.25 var(--ui); color: var(--bronze); }
  .ab-lead { margin: 0; font-size: 15px; color: var(--tinte); }
  .ab-liste { margin: 0; padding: 0; list-style: none; display: grid; gap: 10px; }
  .ab-liste li { display: flex; gap: 12px; align-items: flex-start; padding: 10px; border-radius: 12px; background: var(--stein); }
  .ab-play { flex: 0 0 auto; width: 44px; height: 44px; border-radius: 50%; border: 0; background: var(--bronze); color: var(--stein); font-size: 18px; cursor: pointer; }
  .ab-play.an { background: var(--tinte); }
  .ab-inhalt { display: grid; gap: 4px; min-width: 0; }
  .ab-inhalt b { font: 600 15px/1.3 var(--ui); }
  .ab-inhalt small { font-size: 13px; color: var(--grau); }
  .ab-inhalt q { font: 400 16px/1.45 var(--text); quotes: "„" "“"; }
  .ab-urteil { display: flex; gap: 8px; margin-top: 4px; }
  .ab-urteil button { border: 1px solid var(--linie); background: none; color: var(--tinte); border-radius: 999px; padding: 6px 12px; font: 600 14px/1 var(--ui); cursor: pointer; }
  .ab-urteil button[aria-pressed="true"][data-u="ok"] { background: var(--gruen-voll); border-color: var(--gruen-voll); color: #0d2214; }
  .ab-urteil button[aria-pressed="true"][data-u="nochmal"] { background: var(--rot-voll); border-color: var(--rot-voll); color: #fff; }
  #ab-notiz { width: 100%; font: 16px/1.4 var(--ui); color: var(--tinte); background: var(--stein); border: 1px solid var(--linie); border-radius: 10px; padding: 10px; }
  .ab-knoepfe { display: flex; flex-wrap: wrap; gap: 10px; }
  .ab-ok { flex: 1 1 auto; border: 0; border-radius: 12px; padding: 14px; font: 600 16px/1 var(--ui); background: var(--gruen-voll); color: #0d2214; cursor: pointer; }
  .ab-nein { flex: 0 1 auto; border: 1px solid var(--linie); border-radius: 12px; padding: 14px; font: 600 15px/1 var(--ui); background: none; color: var(--tinte); cursor: pointer; }
  .ab-ok:disabled, .ab-nein:disabled { opacity: .5; cursor: default; }
  .ab-stand { margin: 0; font-size: 14px; color: var(--gruen-voll); }
</style>'''
js = '''
<script>
(function () {
  var STELLEN = %s, KAP = %s, db = null, kom = null, anClaude = false, urteil = {}, ende = null, aktiv = null;
  var ton = document.getElementById("ab-ton"), stand = document.getElementById("ab-stand");
  function knopf(b, an) { b.classList.toggle("an", an); b.textContent = an ? "❚❚" : "▶"; }
  document.querySelectorAll(".ab-play").forEach(function (b) {
    b.addEventListener("click", function () {
      var seite = document.getElementById("ton"); if (seite && !seite.paused) seite.pause();
      if (aktiv === b && !ton.paused) { ton.pause(); return; }
      document.querySelectorAll(".ab-play").forEach(function (x) { knopf(x, false); });
      aktiv = b; ende = parseFloat(b.dataset.t1);
      var start = function () { ton.currentTime = parseFloat(b.dataset.t0); ton.play().catch(function () {}); knopf(b, true); };
      if (ton.readyState >= 1) start(); else { ton.addEventListener("loadedmetadata", start, { once: true }); ton.load(); }
    });
  });
  ton.addEventListener("timeupdate", function () { if (ende !== null && ton.currentTime >= ende) ton.pause(); });
  ton.addEventListener("pause", function () { if (aktiv) knopf(aktiv, false); });
  function zeige() {
    document.querySelectorAll(".ab-liste li").forEach(function (li) {
      li.querySelectorAll(".ab-urteil button").forEach(function (b) { b.setAttribute("aria-pressed", String(urteil[li.dataset.id] === b.dataset.u)); });
    });
  }
  document.querySelectorAll(".ab-liste li").forEach(function (li) {
    li.querySelectorAll(".ab-urteil button").forEach(function (b) { b.addEventListener("click", function () {
      urteil[li.dataset.id] = urteil[li.dataset.id] === b.dataset.u ? null : b.dataset.u; zeige();
      if (db) db.collection("abnahme_stellen").doc(li.dataset.id).set({ stelle: li.dataset.id, urteil: urteil[li.dataset.id] || null, zeit: new Date().toISOString() }).catch(function () {});
    }); });
  });
  function senden(status) {
    var notiz = document.getElementById("ab-notiz").value.trim();
    var zeilen = STELLEN.map(function (s, i) { var u = urteil[s.id]; return (i + 1) + ". " + s.was + ": " + (u === "ok" ? "passt" : u === "nochmal" ? "NOCHMAL" : "–"); });
    var text = "Hörprobe " + KAP + ": " + (status === "ok" ? "ABGENOMMEN, bitte rendern" : "NOCH NICHT abgenommen") + "\\n" + zeilen.join("\\n") + (notiz ? "\\nNotiz: " + notiz : "");
    if (db) db.collection("abnahme").doc("gesamt").set({ status: status, notiz: notiz, stellen: urteil, zeit: new Date().toISOString() }).catch(function () {});
    if (!kom || !anClaude) { stand.textContent = db ? "Gespeichert. Claude liest es beim nächsten Mal." : "Speicher nicht erreichbar – bitte Claude im Chat Bescheid geben."; return; }
    document.getElementById("ab-ok").disabled = document.getElementById("ab-nein").disabled = true;
    kom.anchorFor(document.getElementById("abnahme")).then(function (a) { return kom.sendToClaude({ anchor: a, text: text.slice(0, 3900) }); })
      .then(function () { stand.textContent = status === "ok" ? "Abgenommen ✓ – Claude rendert jetzt." : "An Claude geschickt ✓"; },
        function (e) { stand.textContent = e && e.code === "consent_required" ? "Gespeichert. Zum Senden bitte die Freigabe erlauben." : "Gespeichert, Senden fehlgeschlagen."; })
      .then(function () { document.getElementById("ab-ok").disabled = document.getElementById("ab-nein").disabled = false; });
  }
  document.getElementById("ab-ok").addEventListener("click", function () { senden("ok"); });
  document.getElementById("ab-nein").addEventListener("click", function () { senden("nochmal"); });
  if (window.claude && claude.use) {
    claude.use("db").then(function (d) { if (!d) return; db = d;
      db.collection("abnahme_stellen").onSnapshot(function (snap) { (snap.docs || []).forEach(function (x) { var v = x.data ? x.data() : x; if (v && v.stelle) urteil[v.stelle] = v.urteil || null; }); zeige(); }, function () {});
    }).catch(function () {});
    claude.use("comments").then(function (c) { if (!c || !c.canSendToClaude) return; kom = c;
      c.canSendToClaude().then(function (v) { anClaude = v === "available"; }, function () {}); }).catch(function () {});
  }
})();
</script>
</body>''' % (json.dumps([{'id': s['id'], 'was': s['was']} for s in stellen], ensure_ascii=False),
              json.dumps(cfg.get('titel') or os.path.basename(basis), ensure_ascii=False))

seite = open(os.path.join(aus, 'index.html'), encoding='utf-8').read()
anker = '</header>'
assert anker in seite and '</style>' in seite
seite = seite.replace(anker, anker + '\n  ' + box, 1).replace('</style>', css, 1)
seite = seite.replace('</body>', js, 1) if '</body>' in seite else seite.rstrip() + '\n' + js.replace('</body>', '')
open(os.path.join(aus, 'index.html'), 'w', encoding='utf-8').write(seite)
print(f'Abnahme-Kasten mit {len(stellen)} Stellen eingefügt')
