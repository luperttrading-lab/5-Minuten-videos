# Kopfrechnen üben – Übungs-App zu den Mathe-Videos

**Spielen:** https://luperttrading-lab.github.io/5-Minuten-videos/uebung/ (iPhone: *Teilen → Zum Home-Bildschirm*)

Nutzerwunsch 04.11.2026: „eine kleine App wie die Würfel-App, damit man das üben kann … Übung macht den Meister“.

- **Runde:** Start → 10 Aufgaben → Ende mit „x von 10 richtig“, **Ø Sekunden je Aufgabe**, schnellste Zeit, Liste aller
  Aufgaben mit Zeit, wechselndem Motivationsspruch und Ziel „unter drei Sekunden“ (wie im Video).
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
- **Stufen:** „Alle Zahlen“ (11–19 · 11–19, 10 verschiedene Paare je Runde) und „Einer ergeben 10“ (12 · 18 = 200 + 16).

## Sprechen
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
