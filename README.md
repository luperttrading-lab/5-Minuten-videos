# 5-Minuten-Videos

Kurze Gesundheits-Faktenchecks als Erklärvideo: Bildausschnitte mit Kamerafahrt, Tafelbild mit Beweislage-Markern,
synthetische Sprecherstimme (ElevenLabs), nummerierte Quellen.

| Thema | Länge | Ordner |
|---|---|---|
| Chronischer Stress: Was hilft wirklich? | 6:01 (auch als zwei Teile) | `themen/stress/` |
| Magnesium: Was stimmt wirklich? | 5:10 | `themen/magnesium/` |

Werkzeuge in `werkzeug/`, Ablauf und Regeln in `CLAUDE.md`. Voraussetzungen: Python 3 mit Pillow und numpy, ffmpeg,
für den Ton `ELEVENLABS_API_KEY` in der Umgebung.

    cd themen/magnesium
    python3 ../../werkzeug/render.py szenen.json grafik_korrigiert.png video.mp4
    python3 ../../werkzeug/beschreibung.py szenen.json video_zeitplan.json
