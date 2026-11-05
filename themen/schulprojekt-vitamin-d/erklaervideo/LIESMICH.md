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

## Nachtrag 05.11. (Nutzerwunsch, Vitamin-D-Sitzung)
- v1: Kalzium-Satz eindeutig („Vitamin D hilft dem Darm, Kalzium aus der Nahrung aufzunehmen. Vitamin D selbst steckt dagegen nur in wenigen Lebensmitteln …“).
- v2: Winter „kein Vitamin D“ statt „kaum“, mit 45 Grad und Schattenregel; Quelle Webb, Kline, Holick 1988 (Edmonton 52° N: Oktober bis März keine Bildung, doi 10.1210/jcem-67-2-373, per Crossref geprüft).
- v3: Einheiten-Warnung umgedreht: „sonst hältst du einen Mangel fälschlich für einen guten Wert: 25 Nanomol sehen gut aus, sind aber nur 10 Nanogramm.“
- Neuer Ton für v1–v3 (952 Zeichen berechnet), 5:28, 779 Wörter. G und I neu gerendert, 720p/24 fps mit AAC 160 kbit/s an den Nutzer. Die anderen sechs Stile sind noch auf dem alten Text, neu rendern kostet keinen Ton.
- 05.11. mittags, zweite Runde: v2 nennt die Werte („fast alle 20 ng/ml, aber nur jeder Vierte 32“, Rhodes 2010). v1-Tipp mit Quecksilber-Hinweis: „Hering oder Lachs ein- bis zweimal pro Woche … Große Raubfische wie Hai oder Schwertfisch meidest du besser“, Quelle BfR 047/2023 (Hering 0,036, Hai 0,71, Schwertfisch 0,66 mg/kg Quecksilber im Mittel). 5:37, 794 Wörter. G und I neu gerendert.
- 05.11., 14:30: Alle acht Stile mit neuem Text neu gerendert, Vergleichsseite ausgetauscht (gleiche URL, G und I oben; 720p/12 fps, Ton AAC 128 kbit/s direkt aus der WAV, je 10–14 MB). Grund: Der Nutzer hatte auf der Vergleichsseite noch die alten Fassungen vom 03.11. gehört. `vorschau.json` verweist jetzt auf lokale Dateien `vorschau_neu_<Stil>.mp4` (nicht eingecheckt, aus Drehbuch und tts_cache neu baubar).
- 05.11., 15:05: Nutzernotiz zu J „Die Figuren sollten immer ein Gesicht haben“ → `gesichter_J.py`: v2a (Sonnenbad, auch Kachel), v2d (Winterstraße), v5g (Frau am Fenster), v6c (Büro) mit sichtbaren Gesichtern neu, 136,8 Credits; alte Bilder als `*_ohne_gesicht.jpg`. J neu gerendert, Vergleichsseite aktualisiert. Offen: Rückenansichten auch in C, G, H, L (Fenster, Winterstraße).
