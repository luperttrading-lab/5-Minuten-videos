# Kopfrechnen üben – Übungs-App zu den Mathe-Videos

**Spielen:** https://luperttrading-lab.github.io/5-Minuten-videos/uebung/ (iPhone: *Teilen → Zum Home-Bildschirm*)

Nutzerwunsch 04.11.2026: „eine kleine App wie die Würfel-App, damit man das üben kann … Übung macht den Meister“.

- **Runde:** Start → 10 Aufgaben → Ende mit „x von 10 richtig“, **Ø Sekunden je Aufgabe**, schnellste Zeit, Liste aller
  Aufgaben mit Zeit, wechselndem Motivationsspruch und Ziel „unter drei Sekunden“ (wie im Video).
- **Antworten:** tippen (Tastenfeld; bei dreistelligen Ergebnissen wird nach der 3. Ziffer geprüft) oder **sprechen**.
  Beides geht in derselben Runde, 🎤 schaltet um.
- **Fehler:** kurz rot, dann der Lösungsweg mit den drei Schritten aus dem Video (Einer rüber · mal 10 · Einer · Einer dazu),
  „Weiter“ (beim Sprechen nach 6 s von selbst).
- **Verlauf:** letzte Runden und bester Schnitt (Runden mit ≥ 8 richtig) im Gerät (localStorage).
- **Stufen:** „Alle Zahlen“ (11–19 · 11–19, 10 verschiedene Paare je Runde) und „Einer ergeben 10“ (12 · 18 = 200 + 16).

## Sprechen
Erkennung im Gerät mit Vosk (WebAssembly) und dem kleinen deutschen Modell, beides von der **Würfel-App** geladen
(`/wuerfel/sprache/` auf derselben Adresse luperttrading-lab.github.io – einmal geladen, nutzen beide Apps denselben
Speicher). Apples eigene Erkennung ist in Home-Bildschirm-Apps gesperrt (WebKit-Bug 225298). Grammatik: nur Zahlwörter
0 … 999 (`zahlGrammatik()` in `aufgaben.js`), das Modell liefert z. B. „zweihundert achtundachtzig“ → 288.
Sagt man „zweihundert … achtundachtzig“ mit Pause, wartet die App 1,5 s auf den Rest.
Geprüft mit Christians Stimme (ElevenLabs) als Ersatz-Mikrofon: 10 von 10 bzw. 18 von 18 richtig verstanden, Runde nur
mit Sprechen fehlerfrei. Am iPhone und mit Kinderstimmen noch ungeprüft.

## Neue Übung zu einem neuen Video
In `aufgaben.js` ein Objekt in `UEBUNGEN` ergänzen: `id`, `titel`, `video`, `stufen`, `erzeuge(stufe, anzahl)`,
`aufgabe(...)` → `{frage, loesung}`, `weg(aufgabe)` → Schritte für den Lösungsweg. Dann `APP_VERSION` in `index.html`
hochzählen. (Die Startseite zeigt bisher eine Übung; bei der zweiten kommt eine Auswahl dazu.)

## Prüfen
- `node tests/uebung.mjs [bildordner]` – Zahlwörter, Runde mit Tippen (9/10, Lösungsweg, Ende, Verlauf), Aufgaben-Erzeugung
- `node tests/sprechen.mjs folge.wav` – Sprechen mit Ersatz-Mikrofon (Aufnahme nicht im Repo, siehe Kopf der Datei)
- Update-Mechanismus nach Skill app-update-iphone: `APP_VERSION`, `sw.js` Netz zuerst, Tipp auf „Version …“ prüft
