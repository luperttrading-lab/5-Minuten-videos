# Kopfrechnen üben – Übungs-App zu den Mathe-Videos

**Spielen:** https://luperttrading-lab.github.io/5-Minuten-videos/uebung/ (iPhone: *Teilen → Zum Home-Bildschirm*)

Nutzerwunsch 04.11.2026: „eine kleine App wie die Würfel-App, damit man das üben kann … Übung macht den Meister“.

- **Runde:** Start (Übersicht) → Übungsseite „Bereit?“ (Sprache lädt, Mikrofon geht an; beim Sprechen ist „Los“ erst frei,
  wenn Ton ankommt, sonst „Ohne Sprechen los“) → **„Los“: ab hier zählt die Zeit** (Nutzerwunsch 04.11.) → 10 Aufgaben → Ende mit „x von 10 richtig“, **Ø Sekunden je Aufgabe**, schnellste Zeit, Liste aller
  Aufgaben mit Zeit, wechselndem Motivationsspruch und Ziel je Stufe (`ziel` in `aufgaben.js`): „Alle Zahlen“ unter vier Sekunden wie im Video, „Einer ergeben 10“ unter drei
  (Nutzerentscheidung 05.11., v1.9).
- **Antworten:** tippen (Tastenfeld; bei dreistelligen Ergebnissen wird nach der 3. Ziffer geprüft) oder **sprechen**.
  Beides geht in derselben Runde, 🎤 schaltet um.
- **Fehler:** falsche Zahl durchgestrichen, richtige daneben – genauso lange (0,8 s) wie bei richtig, kein Halt in der Runde
  (Nutzerwunsch 04.11.). Der Lösungsweg mit den drei Schritten steht im **Ergebnis** unter der Aufgabe.
- **Hörfehler:** Bei einer gesprochenen falschen Antwort im Ergebnis ein Knopf „Hörfehler – ich habe … gesagt“ → zählt richtig.
- **Mikrofon-Anzeige** unter der Kopfzeile, Farbe **und** Text: grau „Mikrofon aus – antippen“, gelb „Sprache lädt …“ /
  „Mikrofon wird eingeschaltet …“ / „kein Ton“, grün „Mikrofon an – sag die Zahl“ mit Pegel, rot bei Fehler. Antippen schaltet um.
- **Laden sichtbar:** Wählt man „Sprechen“, lädt das Modell sofort (Startseite zählt die Sekunden). Start während des Ladens
  zeigt „Sprache wird vorbereitet …“ mit „Solange tippen“. Reihenfolge: erst Modell, dann Mikrofon.
- **Verlauf:** letzte Runden und bester Schnitt (Runden mit ≥ 8 richtig) im Gerät (localStorage).
- **Stufen:** „Alle Zahlen“ (11–19 · 11–19, 10 verschiedene Paare je Runde, jedes zufällig gedreht, keins doppelt) und
  „Einer ergeben 10“ (12 · 18 = 200 + 16). Dort gibt es mit beiden Reihenfolgen nur 9 Aufgaben (15 · 15 einmal): alle 9 je
  einmal plus genau eine Wiederholung, nie 15 · 15, frühestens 4 Aufgaben später; nie dasselbe Paar direkt hintereinander,
  auch nicht verdreht (12 · 18 → 18 · 12). Nutzerwunsch 04.11., geprüft über 2000 Runden in `tests/uebung.mjs`.

**Sprüche nach Lage (v2.0, Nutzer 05.11.):** alles richtig und schnell → Lob (`LOB_SPRUECHE`), alles richtig, aber über
dem Ziel → Genauigkeit loben (`GENAU_SPRUECHE`), mit Fehlern → Mut machen (`SPRUECHE`); je Runde neu gewählt. „Ziel
geschafft“ nur mit mindestens 8 von 10 richtigen. Gesprochenes, das schon vor der Aufgabe begann, zählt nicht für sie
(sonst Zeiten von 0,0 s).

**Ziel sichtbar (v2.2, Nutzer 05.11.):** jede Stufen-Kachel zeigt „Ziel … s“; nach jeder richtigen Antwort ist die Zeit grün,
wenn sie unter dem Ziel der Stufe liegt, sonst grau. Ziele: Alle Zahlen 4 s, Einer ergeben 10 3 s, Quadrate 4 s, Mal 11 2 s.

**Versionen:** nach 0.6 folgt 1.7 (Nutzerwunsch 04.11.). Die Update-Prüfung vergleicht nur auf Gleichheit, der Sprung ist unkritisch.

## Sprechen
- **Zeitmessung beim Sprechen (v0.5, Messung 04.11.):** gezählt wird bis zum Ende des letzten Wortes, nicht bis die
  Erkennung meldet. Vosk meldet erst nach ≥ 0,5 s Stille (Endpunkt), mit Puffer und Rechenzeit im Test Ø 0,9 s
  (0,7 … 1,4 s; „zweihundert neun“ am längsten, weil noch „…undzwanzig“ folgen könnte). Wort-Zeitmarken (`setWords`)
  stimmen auf Ø 35 ms mit der Lautstärke überein. Umrechnung Strom → Seitenzeit: Minimum von Ankunft − Proben/Rate über
  die letzten 35 Tonblöcke. Ergebnisseite zeigt zusätzlich die Zeit bis zum ersten Wort und die Wartezeit der Erkennung.
  Sprech-Runden vor v0.5 (ohne `mess: 2`) zählen nicht mehr für „Bester Schnitt“.
- **v0.6 (Nutzerwunsch 04.11.): gezählt wird bis zum ANFANG der Antwort** (erstes Wort), weder Sprechen noch Erkennung.
  Zur Kontrolle auf der Ergebnisseite: bis nach „…hundert“ (Anfang des gerechneten Teils) und bis zum Ende der Antwort.
  Grund für die Kontrolle: Im Sonderfall beginnt jede Antwort mit „zweihundert“ – wer das sofort sagt und dabei rechnet,
  hat ein sehr kurzes „erstes Wort“; die wahre Rechenzeit liegt zwischen „erstes Wort“ und „nach …hundert“.
  „Bester Schnitt“ getrennt nach Tippen und Sprechen, beim Sprechen nur Runden mit `mess: 3`.
- **v1.7:** Ergebnisseite zeigt nur noch „Ø … je Aufgabe · schnellste …“ (Nutzerwunsch 04.11.: Erklärtext und
  Kontrollzeilen waren zu viel). Die Kontrollwerte `bisRest`, `bisEnde`, `warte` stehen weiter im Verlauf
  (localStorage `kopfrechnen.runden`) und je Aufgabe in `runde.ergebnisse` (`zweiter`, `schluss`, `roh`).
Erkennung im Gerät mit Vosk (WebAssembly) und dem kleinen deutschen Modell, beides von der **Würfel-App** geladen
(`/wuerfel/sprache/` auf derselben Adresse luperttrading-lab.github.io – einmal geladen, nutzen beide Apps denselben
Speicher). Apples eigene Erkennung ist in Home-Bildschirm-Apps gesperrt (WebKit-Bug 225298). Grammatik: nur Zahlwörter
0 … 999 (`zahlGrammatik()` in `aufgaben.js`), das Modell liefert z. B. „zweihundert achtundachtzig“ → 288.
Sagt man „zweihundert … achtundachtzig“ mit Pause, wartet die App 1,5 s auf den Rest.
Hörtest 04.11. (`tests/hoertest.mjs`, 108 Aufnahmen: Christian 67, Alexander 41 – dann war das Schlüssel-Kontingent leer):
sauber 100 % in allen Grammatiken; mit Handy-Klang, Hall und Rauschen (12 dB) **freie Zahlwörter 96 %** (Ende geht verloren,
„zweihundertacht“ → „zweihundert“), **jede Zahl 100–399 als Phrase 100 %**, nur die 45 Ergebnisse 100 %; bei 6 dB alle ≈ 61–67 %.
Gewählt: 100–399 (`antworten` in `aufgaben.js`) – nicht nur die Ergebnisse, sonst würde eine falsch gerechnete 223 als
richtige 221 „gehört“. Schlampige Formen („zwohundert…“, „zweihundertund…“, „einhundert…“) 10/10.
Am iPhone beobachtet (Nutzer 04.11.): einmal 221 als 223 verstanden – dafür der Knopf „Hörfehler“.

## Neue Übung zu einem neuen Video
In `aufgaben.js` ein Objekt in `UEBUNGEN` ergänzen: `id`, `titel`, `video`, `stufen`, `erzeuge(stufe, anzahl)`,
`aufgabe(...)` → `{frage, loesung}`, `weg(aufgabe)` → Schritte für den Lösungsweg. Dann `APP_VERSION` in `index.html`
hochzählen. (Die Startseite zeigt bisher eine Übung; bei der zweiten kommt eine Auswahl dazu.)

## Prüfen
- `node tests/uebung.mjs [bildordner]` – Zahlwörter, Runde mit Tippen (9/10, Lösungsweg, Ende, Verlauf), Aufgaben-Erzeugung
- `node tests/sprechen.mjs folge.wav` – Sprechen mit Ersatz-Mikrofon (Aufnahme nicht im Repo, siehe Kopf der Datei)
- Update-Mechanismus nach Skill app-update-iphone: `APP_VERSION`, `sw.js` Netz zuerst, Tipp auf „Version …“ prüft
