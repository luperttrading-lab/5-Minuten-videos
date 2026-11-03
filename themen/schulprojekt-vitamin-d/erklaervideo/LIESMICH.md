# Erklärvideo „Vitamin D: Das Sonnenhormon“ in acht Bildstilen (03.11.2026)

Auftrag des Nutzers: Stile C, D, E, G, H, I, J, L aus der Stilprobe, je ein Video, ein gemeinsamer Ton.
Format: Erklärvideo ohne Faktencheck-Ampel (Schulprojekt), Gliederung nach dem Vorschlag der Vitamin-D-Sitzung (03.11., 09:01).

- `drehbuch_bau.py` → `szenen_<Stil>.json` (gleicher Text, nur die Bilder wechseln; Quellen aus `themen/vitamin-d/`, neue per Crossref geprüft)
- `bilder_bau.py` (8 Stile × 8 Motive), `bilder_nachlauf.py` (7 Bilder mit strengeren Vorgaben neu: englische Notizen, falsche Skala, zu aufreizende Badeszene)
- Rendern: `python3 ../../../werkzeug/render.py szenen_C.json bilder/C/e1.jpg video_C.mp4` (Ton aus `tts_cache`, kostet nichts)
- Länge 5:15, 753 Wörter. Kosten: ElevenLabs ≈ 2.000 Zeichen (einmal), Bilder 1.308 Credits (71 Bilder)
- Vorschau-Seite: https://claude.ai/artifact/JVJwhsFJNfTkVCUPRMdcQ3

## Zweite Fassung (03.11. abends, Nutzerwunsch)
- Eigene Szenenbilder im Format 5:4 (1280x1024, `bilder_v2.py`) statt Ausschnitten aus den 16:9-Kachelbildern; Bildwechsel alle 6–12 s
- Sonnenbad mit Mann und Frau, glatte Haut ohne Funken (Knete sah nach Ausschlag aus)
- Nach Sichtprüfung weggelassen: v5c (Pose auf allen vieren), G-v2c (knapper Bikini von hinten); C-Laborbild: altes e3 (Schrift im neuen abgeschnitten)
- ChatLLM-Credits während des Laufs aufgebraucht: J ohne neue Bilder für v6/v7 (alte Bilder), L ganz ohne neue Bilder,
  Kachel „Sonne“ aus dem Szenenbild v2a (16:9-Fassung `e2a_v2` fehlt). Nachholen: `python3 bilder_v2.py J L`, dann `drehbuch_bau.py` und rendern
- Kosten zweite Runde: 122 Bilder geloggt 1.751 Credits, 128 weitere ungeloggt (Lauf brach ab) ≈ 1.840 geschätzt, 2 Tests 35

## Nachtrag 03.11., 19:20: J und L vollständig
- Nach dem Auffüllen der Credits: 46 Bilder (J v6/v7, L alle Szenenbilder), 644,9 Credits. Alle acht Stile jetzt mit eigenen Szenenbildern.
