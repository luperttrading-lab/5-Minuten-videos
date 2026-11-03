# Erklärvideo „Vitamin D: Das Sonnenhormon“ in acht Bildstilen (03.11.2026)

Auftrag des Nutzers: Stile C, D, E, G, H, I, J, L aus der Stilprobe, je ein Video, ein gemeinsamer Ton.
Format: Erklärvideo ohne Faktencheck-Ampel (Schulprojekt), Gliederung nach dem Vorschlag der Vitamin-D-Sitzung (03.11., 09:01).

- `drehbuch_bau.py` → `szenen_<Stil>.json` (gleicher Text, nur die Bilder wechseln; Quellen aus `themen/vitamin-d/`, neue per Crossref geprüft)
- `bilder_bau.py` (8 Stile × 8 Motive), `bilder_nachlauf.py` (7 Bilder mit strengeren Vorgaben neu: englische Notizen, falsche Skala, zu aufreizende Badeszene)
- Rendern: `python3 ../../../werkzeug/render.py szenen_C.json bilder/C/e1.jpg video_C.mp4` (Ton aus `tts_cache`, kostet nichts)
- Länge 5:15, 753 Wörter. Kosten: ElevenLabs ≈ 2.000 Zeichen (einmal), Bilder 1.308 Credits (71 Bilder)
- Vorschau-Seite: https://claude.ai/artifact/JVJwhsFJNfTkVCUPRMdcQ3
