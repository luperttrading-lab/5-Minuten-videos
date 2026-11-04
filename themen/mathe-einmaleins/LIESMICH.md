# Kopftrick 12 · 18 = 200 + 2 · 8 in fünf Animationsarten (04.11.2026)

Nutzerwunsch: „ganz unterschiedlich, nicht nur der Hintergrund geändert“.
Mathematik: (10 + a)(10 + b) = 100 + 10·(a + b) + a·b. Die Regel „200 + Produkt der Einer“ gilt NUR bei a + b = 10.
Das Beispiel des Nutzers 15 · 14 ist 210, nicht 220. Jedes Video zeigt das am Ende als Gegenprobe.

- `python3 animationen.py <ausordner> [art …]`, Standbilder mit `--bild 2.5,8,…`; je 21 s, ohne Ton, ≈ 1 min Rechenzeit je Art
- Arten: flaeche (Flächenmodell, weiche Übergänge), kinetik (kinetische Typografie, harte Schnitte, Kamera),
  handschrift (Bleistift schreibt, Kamera folgt), punkte (216 Partikel mit Leuchtspur), papier (Papierschnitt, Stop-Motion 12 fps)
- Zeichenfläche ist RGB: ImageDraw blendet halbtransparente Farben nur auf RGB, auf RGBA überschreibt es den Alphakanal
- Vorschau-Seite (gemeinsam für alle Mathe-Proben): `themen/mathe-stilprobe/vorschau.json` → https://claude.ai/artifact/PVisw26MxXcVy1NJngcMFu

## Erklärvideo mit Ton: `regel.py` (04.11.)
- Allgemeine Regel 16 · 18 = (16 + 8) · 10 + 6 · 8 = 288, beide Richtungen, Flächenbeweis (Streifen 6 × 10 drehen → 10 × 24), Sonderfall 11·19 … 15·15, Vorsicht 15 · 14 = 210, Übung 13 · 14 = 182
- `python3 regel.py <ziel.mp4> [--nur-ton] [--bild s,…]`; Einblendungen hängen an gesprochenen Wörtern (ElevenLabs-Zeitmarken)
- 2:02, 244 Wörter, ElevenLabs 708 Zeichen berechnet; Ton in `tts_cache/` (JSON eingecheckt)

## Dritte Fassung (04.11., „schöner und verständlicher, das ganze Video“)
- Drei benannte Schritte: Einer rüber · mal 10 · Einer · Einer dazu. Eine Schritte-Karte rechts verbindet Regel und Bild
  (leuchtet in den Flächenszenen beim passenden Schritt auf)
- Trick mit wandernden Ziffern (8 springt zur 16, Null fällt an die 24, 6 und 8 werden 48, schriftliche Addition)
- Sonderfall: Form mit 20 Spalten, die Ecke wächst von 1 × 9 bis 5 × 5. Vorsicht: 19 Spalten, die 20. fehlt (−10)
- Merkzettel und Übung 13 · 14 mit Drei-Sekunden-Uhr. Kästchen-Gitter in allen Flächen, Fortschrittsbalken, Kapitelnummern
- 1920 × 1080, in vier Teilen parallel gerendert (≈ 3 min). Länge 2:39, 319 Wörter, ElevenLabs ≈ 830 Zeichen berechnet
- Achtung beim Stichwort-Suchen: „zehn plus sechs“ steckt in „acht*zehn plus sechs*“
- Vierte Runde (04.11.): Atempausen an Satzenden (0,4 s, nach Doppelpunkt 0,15 s; Zeitmarken verschoben), Markierungen der gemeinten Ziffern, Auflösung „= 288“ nach der Uhr, leise synthetische Geräusche (KLAENGE, 15–20 dB unter der Stimme), 6 und 8 fliegen um die 240 herum. Länge 2:52
