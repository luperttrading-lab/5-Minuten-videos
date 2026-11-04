# Kopftrick 12 · 18 = 200 + 2 · 8 in fünf Animationsarten (04.11.2026)

Nutzerwunsch: „ganz unterschiedlich, nicht nur der Hintergrund geändert“.
Mathematik: (10 + a)(10 + b) = 100 + 10·(a + b) + a·b. Die Regel „200 + Produkt der Einer“ gilt NUR bei a + b = 10.
Das Beispiel des Nutzers 15 · 14 ist 210, nicht 220. Jedes Video zeigt das am Ende als Gegenprobe.

- `python3 animationen.py <ausordner> [art …]`, Standbilder mit `--bild 2.5,8,…`; je 21 s, ohne Ton, ≈ 1 min Rechenzeit je Art
- Arten: flaeche (Flächenmodell, weiche Übergänge), kinetik (kinetische Typografie, harte Schnitte, Kamera),
  handschrift (Bleistift schreibt, Kamera folgt), punkte (216 Partikel mit Leuchtspur), papier (Papierschnitt, Stop-Motion 12 fps)
- Zeichenfläche ist RGB: ImageDraw blendet halbtransparente Farben nur auf RGB, auf RGBA überschreibt es den Alphakanal
- Vorschau-Seite (gemeinsam für alle Mathe-Proben): `themen/mathe-stilprobe/vorschau.json` → https://claude.ai/artifact/PVisw26MxXcVy1NJngcMFu
