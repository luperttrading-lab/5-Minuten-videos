# Mathe-Videos: Stilprobe (04.11.2026)

Nutzerfrage: „Welche Stile gibt es insgesamt? Kurze Videos, 15 Sekunden, damit man sieht, wie welcher wirkt.“
Dieselbe Szene (13 · 17 = 15² − 2² = 221, Rechteck 17 × 13 → Streifen 2 × 13 umlegen → Quadrat 15 × 15 ohne Ecke 2 × 2)
in zehn Stilen, ohne Ton, komplett per Code gezeichnet (PIL), keine KI-Bilder.

- `python3 stilprobe.py <ausordner> [stil …]` rendert die Videos (≈ 1 min je Stil), `--bild <s>` ein Standbild
- Stile: flat, whiteboard, kreide, dunkel, heft, blaupause, swiss, comic, pixel, neon
- Schriften: `werkzeug/schriften/` (Google Fonts, OFL)
- Hochzahlen setzt das Skript selbst (Bangers zeichnet „²“ in voller Größe); Comic-Formeln in Inter, weil Bangers „=“ wie „:“ zeichnet;
  Pixelschrift ohne „−“ → Bindestrich
- Vorschau-Seite: https://claude.ai/artifact/PVisw26MxXcVy1NJngcMFu (`vorschau.json`, Videos liegen nur im Scratchpad, MP4s nicht einchecken)
