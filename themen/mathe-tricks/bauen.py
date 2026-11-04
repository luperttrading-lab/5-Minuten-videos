#!/usr/bin/env python3
"""Baut rechentricks.html und rechentricks.pdf aus tricks.py, pruefung.json und quellen.txt.

Aufruf: python3 pruefung.py && python3 bauen.py
Zwei Durchgänge: erst PDF rendern, Seitenzahlen der Kapitel aus dem Text lesen,
dann mit Seitenzahlen im Inhaltsverzeichnis neu rendern. Seitenbilder: --bilder
"""
import html
import json
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

from tricks import KATEGORIEN as _K1, T as _T1, TOP15
from tricks2 import NEUE_KATEGORIEN as _K2, T2
from tricks3 import NEUE_KATEGORIEN as _K3, T3
from folgen import STAFFELN

_REIHE = "A M S Q D P T E U L Z G K W N X R F".split()
_ALLE_K = dict(_K1 + _K2 + _K3)
KATEGORIEN = [(k, _ALLE_K[k]) for k in _REIHE]
T = sorted(_T1 + T2 + T3, key=lambda t: (_REIHE.index(t["id"][0]), int(t["id"][1:])))

HIER = Path(__file__).parent
PRUEF = json.loads((HIER / "pruefung.json").read_text())
LINKTEST = json.loads((HIER / "linktest.json").read_text())

SPRACHEN = OrderedDict([
    ("de", "Deutsch"), ("en", "Englisch"), ("fr", "Französisch"), ("es", "Spanisch"),
    ("it", "Italienisch"), ("ru", "Russisch"), ("ja", "Japanisch"), ("zh", "Chinesisch"),
    ("hi", "Hindi"), ("en-IN", "Englisch (Indien, Nepal)"),
])
KURZ = {"en-NP": "en-IN"}


def quellen_lesen():
    roh = []
    for zeile in (HIER / "quellen.txt").read_text().splitlines():
        if not zeile.strip() or zeile.startswith("#"):
            continue
        ids, sprache, titel, url = [s.strip() for s in zeile.split(" | ")]
        sprache = KURZ.get(sprache, sprache)
        roh.append((ids.split(","), sprache, titel, url))
    # eine Nummer je URL, sortiert nach Sprache, dann Titel
    je_url = OrderedDict()
    for ids, sp, titel, url in roh:
        e = je_url.setdefault(url, {"sprache": sp, "titel": titel, "url": url, "ids": set()})
        e["ids"].update(i.strip() for i in ids)
    reihe = list(SPRACHEN)
    liste = sorted(je_url.values(), key=lambda e: (reihe.index(e["sprache"]), e["titel"].lower()))
    for n, e in enumerate(liste, 1):
        e["nr"] = n
    zu_trick = defaultdict(list)
    for e in liste:
        for i in e["ids"]:
            zu_trick[i].append(e)
    return liste, zu_trick


QUELLEN, ZU_TRICK = quellen_lesen()
e = html.escape


def sterne(n):
    return '<span class="st">' + "★" * n + '<span class="leer">' + "★" * (3 - n) + "</span></span>"


def zitate(tid):
    qs = sorted(ZU_TRICK.get(tid, []), key=lambda q: q["nr"])
    if not qs:
        return '<span class="warn">keine geprüfte Quelle gefunden</span>'
    return " ".join(f'<a href="#q{q["nr"]}">[{q["nr"]}]</a><span class="lang">{q["sprache"]}</span>' for q in qs)


def karte(t):
    proben = t.get("proben", [t["id"]])
    pr = "<br>".join(("✓ " if PRUEF[p]["ok"] else "✗ ") + e(PRUEF[p]["text"]) for p in proben)
    vorh = '<span class="vorh">Video vorhanden</span>' if t.get("vorhanden") else ""
    return f"""
<div class="karte{' vorhanden' if t.get('vorhanden') else ''}" id="t{t['id']}">
  <div class="kopf"><span class="id">{t['id']}</span><span class="name">{e(t['name'])}</span>{vorh}
    <span class="meta"><span class="stufe">{e(t['stufe'])}</span> Video {sterne(t['video'])} App {sterne(t['app'])}</span></div>
  <div class="orig">{e(t['orig'])}</div>
  <div class="formel">{e(t['formel'])}</div>
  <table class="felder">
    <tr><th>Beispiel</th><td>{e(t['beispiel'])}</td></tr>
    <tr><th>Warum</th><td>{e(t['warum'])}</td></tr>
    <tr><th>Grenzen</th><td>{e(t['grenzen'])}</td></tr>
    <tr><th>Geprüft</th><td class="pr">{pr}</td></tr>
    <tr><th>Quellen</th><td class="qu">{zitate(t['id'])}</td></tr>
  </table>
</div>"""


def seite(seiten=None):
    seiten = seiten or {}
    nach_id = {t["id"]: t for t in T}
    n_proben = len(PRUEF)
    n_ok = sum(1 for v in PRUEF.values() if v["ok"])
    sprachen_benutzt = [s for s in SPRACHEN if any(q["sprache"] == s for q in QUELLEN)]

    def snr(key):
        return f'<span class="snr">{seiten.get(key, "")}</span>'

    toc = [f'<li><a href="#top15">Top 15: am besten für Video und Übung</a>{snr("top15")}</li>',
           f'<li><a href="#folgen">Folgenplan der Videoreihe</a>{snr("folgen")}</li>',
           f'<li><a href="#legende">Lesehilfe und Prüfverfahren</a>{snr("legende")}</li>']
    for k, titel in KATEGORIEN:
        anz = sum(1 for t in T if t["id"].startswith(k) and re.fullmatch(k + r"\d+", t["id"]))
        toc.append(f'<li><a href="#k{k}">{e(titel)}</a> <span class="anz">({anz})</span>{snr("k" + k)}</li>')
    toc.append(f'<li><a href="#quellen">Quellenverzeichnis nach Sprache</a>{snr("quellen")}</li>')

    top = []
    for rang, tid in enumerate(TOP15, 1):
        t = nach_id[tid]
        vorh = ' <span class="vorh">Video vorhanden</span>' if t.get("vorhanden") else ""
        top.append(f"<tr><td class='r'>{rang}</td><td><a href='#t{tid}'><b>{e(t['name'])}</b></a> "
                   f"<span class='kid'>{tid}</span>{vorh}</td><td class='f'>{e(t['formel'])}</td>"
                   f"<td>{e(t['beispiel'])}</td><td class='c'>{sterne(t['video'])}</td><td class='c'>{sterne(t['app'])}</td></tr>")

    folgen_html, nr = [], 0
    for st_nr, (st_titel, fs) in enumerate(STAFFELN, 1):
        zeilen = []
        for titel, ids in fs:
            nr += 1
            haupt = nach_id[ids[0]]
            dazu = ", ".join(f"<a href='#t{i}'>{e(nach_id[i]['name'])}</a>" for i in ids[1:])
            app = max(ids, key=lambda i: nach_id[i]["app"])
            uebung = (f"<a href='#t{app}'>{app}</a>" if nach_id[app]["app"] >= 2 else "–")
            vorh = ' <span class="vorh">Video vorhanden</span>' if any(nach_id[i].get("vorhanden") for i in ids) else ""
            zeilen.append(f"<tr><td class='r'>{nr}</td><td><b>{e(titel)}</b>{vorh}</td>"
                          f"<td><a href='#t{ids[0]}'>{e(haupt['name'])}</a> <span class='kid'>{ids[0]}</span></td>"
                          f"<td class='dazu'>{dazu}</td><td class='c'>{e(haupt['stufe'])}</td><td class='c'>{uebung}</td></tr>")
        folgen_html.append(f"<h3>Staffel {st_nr}: {e(st_titel)} ({len(fs)} Folgen)</h3>"
                           f"<table class='folgen'><tr><th>#</th><th>Folge</th><th>Haupttrick</th><th>dazu</th><th>Stufe</th><th>Übung</th></tr>"
                           f"{''.join(zeilen)}</table>")
    n_folgen = nr

    kap = []
    for k, titel in KATEGORIEN:
        karten = "".join(karte(t) for t in T if re.fullmatch(k + r"\d+", t["id"]))
        kap.append(f'<section class="kap" id="k{k}"><h2>{e(titel)}</h2>{karten}</section>')

    ql = []
    for s in sprachen_benutzt:
        eintr = []
        for q in QUELLEN:
            if q["sprache"] != s:
                continue
            code = LINKTEST.get(q["url"], "?")
            hinweis = "" if code == "200" else (
                f' <span class="hinweis">automatischer Linktest: {"keine Verbindung" if code == "000" else "HTTP " + code}'
                f'{" (Abruflimit)" if code == "429" else " (Bot-Sperre)" if code in ("403", "406", "503") else ""}; '
                f'beim Recherche-Abruf geladen</span>')
            ids = ", ".join(sorted(q["ids"], key=lambda x: (x[0], int(x[1:]))))
            eintr.append(f'<li id="q{q["nr"]}"><span class="qn">[{q["nr"]}]</span> {e(q["titel"])}<br>'
                         f'<a class="url" href="{e(q["url"])}">{e(q["url"])}</a>{hinweis}'
                         f'<span class="fuer"> · zu {ids}</span></li>')
        ql.append(f"<h3>{SPRACHEN[s]} ({len(eintr)})</h3><ol class='ql'>{''.join(eintr)}</ol>")

    ohne = [t["id"] for t in T if not any(ZU_TRICK.get(p) for p in [t["id"]])]
    stil = (HIER / "stil.css").read_text()
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Rechentricks – Sammlung</title>
<style>{stil}</style></head><body>
<section class="titel">
  <div class="ober">Themenvorrat für eine Mathe-Videoreihe und die Übungs-App</div>
  <h1>Rechentricks – Sammlung</h1>
  <div class="unter">Kopfrechnen, Überschlagen, Ergebnisse prüfen: {len(T)} Tricks in {len(KATEGORIEN)} Kategorien,
  jede exakte Regel per Python durchgerechnet, jede Faustregel mit gemessenem Fehler.</div>
  <div class="zahlen">
    <div><b>{len(T)}</b>Tricks</div><div><b>{n_ok}/{n_proben}</b>Rechenproben bestanden</div>
    <div><b>{n_folgen}</b>Folgen</div><div><b>{len(QUELLEN)}</b>Quellen</div><div><b>{len(sprachen_benutzt)}</b>Sprachen</div>
  </div>
  <div class="stand">Stand: 4. November 2026 · Quelle: <code>themen/mathe-tricks/</code> (tricks.py, pruefung.py, quellen.txt, bauen.py)</div>
  <h2 class="tochead">Inhalt</h2>
  <ol class="toc">{''.join(toc)}</ol>
</section>

<section id="top15"><h2>Top 15: am besten für Video und Übung</h2>
<p class="lead">Auswahl nach Sternen für Video und App: Die Antwort ist eine Zahl (passt zur Übungs-App), der Trick ist in
einem Satz erklärbar, die Algebra dahinter passt in ein 5-Minuten-Video, und er spart spürbar Zeit.</p>
<table class="top"><tr><th>#</th><th>Trick</th><th>Regel</th><th>Beispiel</th><th>Video</th><th>App</th></tr>{''.join(top)}</table>
</section>

<section id="folgen"><h2>Folgenplan der Videoreihe</h2>
<p class="lead">{n_folgen} Folgen in {len(STAFFELN)} Staffeln, von der Grundschule bis zur Finanzmathematik. Jede Folge hat einen
Haupttrick (trägt das Video) und kleine verwandte Tricks als Zugabe; jeder der {len(T)} Tricks kommt genau einmal vor.
„Übung“ nennt den Trick, der sich am besten für die Übungs-App eignet (mindestens zwei Sterne), sonst „–“.
Reihenfolge innerhalb einer Staffel: vom Leichten zum Schweren, Staffeln sind unabhängig voneinander drehbar.</p>
{''.join(folgen_html)}
</section>

<section id="legende"><h2>Lesehilfe und Prüfverfahren</h2>
<table class="leg">
<tr><th>Kärtchen</th><td>Name (Deutsch), darunter Originalname mit Sprache. Grauer Kasten: die Regel. Dann Beispiel, Begründung
(„Warum“), Gültigkeitsbereich („Grenzen“), Ergebnis der Rechenprobe („Geprüft“) und Quellen.</td></tr>
<tr><th>Stufe</th><td>GS = Grundschule · 5–8 = Klasse 5–8 · 9–13 = Klasse 9–13 · Erw. = Erwachsene.</td></tr>
<tr><th>Sterne</th><td><b>Video</b>: Wie gut trägt der Trick ein 5-Minuten-Erklärvideo (Aha-Effekt, Begründung zeigbar)?
<b>App</b>: Wie gut passt er in die Übungs-App (Antwort ist eine Zahl, 10 Aufgaben ziehbar, in Sekunden lösbar)?
Beides ist eine redaktionelle Einschätzung, keine Messung.</td></tr>
<tr><th>Geprüft</th><td><code>pruefung.py</code> rechnet jede exakte Regel über den genannten Bereich vollständig durch
(z. B. alle zweistelligen Zahlenpaare, alle Tage 1583–2499) oder mit vielen Zufallsfällen; Faustregeln bekommen den gemessenen
Fehler. Ergebnis dieser Fassung: {n_ok} von {n_proben} Proben bestanden. Regeln, die nur in einem engeren Bereich stimmen, haben
diese Grenze im Kärtchen.</td></tr>
<tr><th>Quellen</th><td>Nummer [n] verweist ins Quellenverzeichnis; dahinter das Sprachkürzel. Jede Quelle wurde bei der
Recherche abgerufen und beschreibt den Trick. Verzeichnis nach Sprache: {', '.join(SPRACHEN[s] for s in sprachen_benutzt)}.
Quellen mit Rechenfehlern (u. a. eine japanische Notizseite mit 17 · 19 = 326) wurden nicht aufgenommen.</td></tr>
<tr><th>Video vorhanden</th><td>Grün markiert: M8 (11–19 mal 11–19), Video in <code>themen/mathe-einmaleins/</code>.</td></tr>
</table>
{"<p class='warn'>Ohne Quelle: " + ", ".join(ohne) + "</p>" if ohne else ""}
</section>
{''.join(kap)}
<section id="quellen"><h2>Quellenverzeichnis nach Sprache</h2>
<p class="lead">{len(QUELLEN)} Quellen. Wikipedia-Artikel sind Einstiegsquellen; für Videos die dort genannte Primärliteratur
nachschlagen. Hinweis bei einzelnen Einträgen: Der spätere automatische Linktest wurde vom Server abgewiesen (Abruflimit
oder Bot-Sperre); die Seite war beim Recherche-Abruf erreichbar.</p>
{''.join(ql)}
</section>
</body></html>"""


def rendern(html_text, ziel):
    import subprocess
    (HIER / "rechentricks.html").write_text(html_text)
    subprocess.run(["node", str(HIER / "pdf_rendern.cjs"), str(HIER / "rechentricks.html"), str(ziel)], check=True)


def seiten_finden(pdf):
    from pypdf import PdfReader
    r = PdfReader(str(pdf))
    texte = [(pg.extract_text() or "") for pg in r.pages]
    ziele = {"top15": "Top 15", "folgen": "Folgenplan der Videoreihe", "legende": "Lesehilfe und Prüfverfahren",
             "quellen": "Quellenverzeichnis nach Sprache"}
    for k, titel in KATEGORIEN:
        ziele["k" + k] = titel
    erg = {}
    for key, titel in ziele.items():
        for i, tx in enumerate(texte[1:], 2):  # Titelseite (mit Inhaltsverzeichnis) überspringen
            erste = [z.strip() for z in tx.splitlines()[:4]]
            if any(z.startswith(titel) for z in erste):
                erg[key] = i
                break
    return erg, len(texte)


def main():
    pdf = HIER / "rechentricks.pdf"
    rendern(seite(), pdf)
    seiten, n = seiten_finden(pdf)
    rendern(seite(seiten), pdf)
    seiten2, n = seiten_finden(pdf)
    assert seiten == seiten2, (seiten, seiten2)
    fehlt = [k for k in ["top15", "folgen", "legende", "quellen"] + ["k" + k for k, _ in KATEGORIEN] if k not in seiten]
    print(f"{n} Seiten; Kapitel: {seiten}; ohne Seitenzahl: {fehlt}")
    if "--bilder" in sys.argv:
        import subprocess
        out = Path(sys.argv[sys.argv.index("--bilder") + 1])
        out.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-r", "70", "-png", str(pdf), str(out / "s")], check=True)


if __name__ == "__main__":
    main()
