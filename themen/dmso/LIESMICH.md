# Erklärvideo „DMSO: Vom Lösungsmittel zum Kälteschutz“, Stil G Aquarell (10.11.2026)

Auftrag: `AUFTRAG.md` (mit Nachtrag: Anwendungen mit Einordnung in Worten, Szene zur Selbstanwendung). Vorbild `themen/pea/`.

- `faktencheck.md`: Recherche mit Quellenverzeichnis (29 DOIs per Crossref geprüft), Tabelle „Anwendungen mit Einordnung“.
- `drehbuch_bau.py` → `szenen_G.json` und `szenen.json` (Ton). Aussprache Fassung 4 (Nutzerwahl 11.11.):
  „Dimethylsulfoxid“ → „Dimethyl-sulfoxid“, „DMSO“ → „D. M. S. O.“ (vorher klang „DMSO“ am Satzanfang wie „Der MSO“) (Proben in `aussprache/`, Auswahl-Seite `aussprache_wahl/`).
- `bilder_bau.py`: 47 Szenenbilder 5:4 + 6 Kacheln 16:9, GPT Image 2; Kosten `bilder_kosten.json`, Protokoll `bilder.log` (0 Fehler).
  Alle Bilder angesehen; Zusatzregel: niemand trinkt, reibt sich ein oder spritzt, keine Flaschen mit Dosierangaben.
- Rendern: `python3 ../../werkzeug/render.py szenen_G.json bilder/G/k1.jpg video_G.mp4` (Ton aus `tts_cache`, ≈ 5 min).
- Hörprobe: `szenen_hoerprobe.json` (Aussprache eingesetzt), `abnahme.json` (8 Stellen mit Fachwörtern).
- Länge 6:51, 847 Wörter. Kosten: ElevenLabs 2.596 + 368 + 2.608 Zeichen berechnet (+ 262 für Proben), Bilder 1.195,8 Credits + Thumbnail 6,0.
- Aussprache-Wahl: https://claude.ai/artifact/YGnFti5qA63jjkSUZukhTL · Hörprobe: https://claude.ai/artifact/HqUuG1ZiJH8frTwNpvBvMy ·
  Vorschau: https://claude.ai/artifact/Qf5YPvSLQKYwzmbXMfi5vP
