# Erklärvideo „PEA: Vom Eigelb zur Schmerzforschung“ in drei Bildstilen (09.11.2026)

Auftrag: `AUFTRAG.md`. Nutzerwunsch beim Drehbuch (09.11.): kein Faktencheck, sondern Ton des Schulprojekts, „etwas softer“.

- `faktencheck.md`: Recherche mit Quellenverzeichnis (Crossref geprüft), Grundlage des Texts.
- `drehbuch_bau.py` → `szenen_I.json`, `szenen_G.json`, `szenen_D.json` (gleicher Text, nur die Bilder wechseln), `szenen.json` für Ton und Hörprobe.
  Aussprache: „PEA“ → „Pe-E-A“, „Palmitoylethanolamid“ → „Palmito-yl-ethanol-amid“ (Proben in `aussprache/`, Abgleich mit Aufnahme des Nutzers).
- `bilder_bau.py`: 43 Szenenbilder 5:4 + 6 Kacheln 16:9 je Stil, GPT Image 2; Kosten in `bilder_kosten.json`, Protokoll `bilder.log`.
  Nach Sichtprüfung neu: Mastzelle (p4b/p4c, sah in G und D wie ein Blatt aus), I/p2e (Märchenkostüm, altes als `p2e_alt.jpg`).
- Rendern: `python3 ../../werkzeug/render.py szenen_I.json bilder/I/k1.jpg video_I.mp4` (Ton aus `tts_cache`, kostet nichts), je ≈ 9 min.
- Hörprobe: `szenen_hoerprobe.json` (Aussprache eingesetzt, weil `hoerprobe.py` das Wörterbuch nicht kennt), `abnahme.json`.
- Länge 5:28, 696 Wörter. Kosten: ElevenLabs 2.233 Zeichen berechnet (+ 84 für Proben), Bilder 2847.9 Credits (alle Läufe laut Protokoll).
- Hörprobe: https://claude.ai/artifact/EibXMPZqGXqobvYcoKDNCc · Vorschau: https://claude.ai/artifact/WFP4EfTXEfea2RS5owMZRd
