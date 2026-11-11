# Erklärvideo „L-Theanin: Was der Stoff aus dem Tee kann“, Stil G Aquarell (11.11.2026)

Auftrag: `AUFTRAG.md`. Vorbild `themen/dmso/`.

- `recherche_A.md`, `recherche_B.md`: zwei unabhängige Recherchen (Geschichte/Recht, Studien/Sicherheit), rund 115 DOIs per
  Crossref geprüft. `faktencheck.md`: Kernaussagen und Tabelle „Anwendungen mit Einordnung“.
- `abgleich_infografik.md`: Abgleich mit der Infografik des Nutzers (`vorlage/`, erst nach Faktencheck und Drehbuch-Entwurf
  geöffnet). 12 Aussagen: 1 falsch (FDA), 3 nicht belegt, Rest teilweise richtig oder überzogen. Übernommen: Reaktionszeit
  allein, Cortisol. Weggelassen: Dosistabelle und Zeitpunkte, „2:1“, „Sweet Spot“.
- `drehbuch_bau.py` → `szenen_G.json` und `szenen.json` (Ton). Aussprache (Nutzerwahl 11.11., Fassungen 1 und 6, entspricht dem gerenderten Ton): „L-Theanin“ wie geschrieben,
  Uji → Udschi, Yajiro → Jadschiro, Gyokuro → Gjokuro, Matcha → Mattscha (Proben in `aussprache/`, Auswahl-Seite
  `aussprache_wahl/`).
- `bilder_bau.py`: 56 Szenenbilder 5:4 + 6 Kacheln 16:9, GPT Image 2; Protokoll `bilder.log` (0 Fehler). Alle angesehen,
  4 verworfen und neu erzeugt (t5c wirkte wie Bestechung, t5h zu klein, t6d zeigte den Reichstag, t7g Gesicht verdeckt).
- Rendern: `python3 ../../werkzeug/render.py szenen_G.json bilder/G/k1.jpg video_G.mp4` (Ton aus `tts_cache`, ≈ 5 min).
- Vorschau: `ffmpeg … fps=12, 1280x720, crf 36, AAC 128k aus video_G.wav` (crf 30 ergab 27 MB, Grenze 16 MB).
- Hörprobe: `szenen_hoerprobe.json` (Aussprache eingesetzt), `abnahme.json` (12 Stellen mit Fachwörtern und Namen).
- Ton geprüft: `betonung.py` 0 Auffälligkeiten; Spracherkennung (faster-whisper small, lokal) ohne Textfehler, hört
  „Theanin“ im Fließtext als „Tianin“ (deshalb die Auswahl-Seite).
- Länge 6:44, 903 Wörter. Kosten: ElevenLabs 2.637 Zeichen berechnet + 225 für Proben; Bilder 1.138,5 Credits
  (1.046,0 + 92,5 für die vier Ersatzbilder) + Thumbnail 5,7.
- Aussprache-Wahl: https://claude.ai/artifact/WDfh22zFteGxPZ4ZkpvUDA · Hörprobe: https://claude.ai/artifact/4ENxj1UdQcgmf3CyzaJttz ·
  Vorschau: https://claude.ai/artifact/ANpb1VumDoVJmDEp6ug13a
