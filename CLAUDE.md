# 5-Minuten-Videos: Gesundheits-Faktenchecks

Info-Videos für YouTube (Ziel ≈ 6 Minuten, ≈ 720 Wörter; Teile unter 5 Minuten nur für die Prüfung durch Gemini) zu Gesundheitsthemen,
die viele Menschen interessieren. Format: Faktencheck populärer Aussagen, oft aus NotebookLM-/Gemini-Infografiken.
Fertige Beispiele: `themen/stress/`, `themen/magnesium/`.

## Ablauf je Thema (`themen/<thema>/`)
1. **Vorlage sichten:** Grafiken nach `vorlage/`, alle Behauptungen aus Grafiken und Begleittext auflisten.
2. **Faktencheck vor dem Drehbuch:** jede Behauptung gegen Primärquellen, Meta-Analysen, Leitlinien und Behörden
   (DGE, BfR, EFSA, WHO, Cochrane) prüfen, DOIs auf Auflösbarkeit testen. Gut geeignet: ein Subagent mit WebSearch.
   - Kein Punkt geht ungeprüft ins Video. „Ungeprüft“ gibt es nicht als Kategorie.
   - Was gesucht und nicht untersucht gefunden wurde, sagt der Sprechtext ehrlich, es bekommt aber keinen Stichpunkt.
   - Interessenkonflikte (Herstellerstudien), Tierstudien und Studiengröße nennen.
   - Behauptungen sammeln, wo die Zuschauer sind: Transkripte populärer YouTube-Videos (Skill youtube-transkript),
     Videobeschreibungen auf Affiliate-Links, Rabattcodes und eigene Produkte prüfen. Transkripte nie einchecken.
   - Empfehlungen, die an eigene Produkte oder Affiliate-Links gebunden sind, kommen gar nicht ins Video (auch nicht
     widerlegt), außer eine unabhängige Quelle oder Studien stützen sie. Mehrere Videos desselben Anbieters zählen nicht
     als Bestätigung.
   - Herkunft der Behauptungen im Video nicht nennen: weder Ärzte noch Videos, Kanäle oder Aufrufzahlen. Neutral
     formulieren: „Oft heißt es …“, „Eine verbreitete Empfehlung lautet …“, „Viele raten …“.
3. **Drehbuch `szenen.json`:** siehe Aufbau unten.
4. **Bildausschnitte prüfen:** `python3 ../../werkzeug/ausschnitte_pruefen.py szenen.json bogen.png grafik_korrigiert.png`
5. **Ton und Länge prüfen:** `python3 ../../werkzeug/render.py szenen.json grafik_korrigiert.png video.mp4 --nur-ton`
6. **Rendern:** dasselbe ohne `--nur-ton` (≈ 4–5 min Rechenzeit), danach Kontrollbilder mit `--bild <Sekunde>`.
7. **Beschreibung und Teilen-Seite:** `python3 ../../werkzeug/beschreibung.py szenen.json video_zeitplan.json`
8. **Ausliefern:** 1080p (Master, nicht einchecken), 720p für die Teilen-Seite (Artifact), 480p zum Verschicken:
   `ffmpeg -i video.mp4 -vf "crop=1920:1072:0:0,fps=15,scale=854:480:flags=lanczos" -c:v libx264 -preset slow -crf 30
   -tune stillimage -profile:v main -pix_fmt yuv420p -c:a aac -b:a 64k -ac 1 -movflags +faststart video_480p.mp4`
   Dateien dem Nutzer im Chat schicken. MP4s nie committen: Sie lassen sich aus Drehbuch, Grafik und Ton-Cache jederzeit neu rendern.

## Aufbau `szenen.json`
- Kopf: `tts` (`elevenlabs`), `voice_id`, `model`, `tempo`, `titel`, `untertitel`, `fuss`, `quellen` (Verzeichnis
  `id → kurz, voll, url`).
- Erste Szene `layout: "kacheln"`: sechs Kapitel-Kacheln (`kacheln: [{t, a, wort}]`). Jede Kachel leuchtet auf, wenn ihr
  `wort` gesprochen wird (ElevenLabs-Zeitmarken). `hervorheben_at`/`legende_at` = Satznummer. Am Ende des Einstiegs
  wird die Legende gesprochen: „Grün heißt belegt, gelb teilweise, rot nicht haltbar.“
- Weitere Szenen: `kicker`, `headline`, `sentences` (Text oder `{t: Anzeige, say: Sprechtext}`; Zahlen im
  Sprechtext ausschreiben), `bullets` (`{t, at, ev}` mit `ev` = `stark` | `mittel` | `keine`), `evidence`
  (`level`, `label`), `quellen` (IDs aus dem Verzeichnis), `shots` (`{a: [x0,y0,x1,y1], at, zoom}`, `zoom` =
  `out` | `none`, Standard: 5 % hinein). Eigenes Bild statt Grafik: `bild: "bilder/x.png"` (relativ zum
  Drehbuch, auch in Kacheln); ohne `a` wird das ganze Bild gezeigt.

## Gestaltungsregeln
- Zahlen sparsam: kaum Prozentzahlen, höchstens eine Zahl pro Satz. Lieber Brüche und Vergleiche („jeder Vierte“,
  „von zwei Dritteln auf ein Zehntel“, „so viel wie in ein, zwei Mandeln“). Die Zuschauer sind keine Statistiker.
- Jede Szene endet mit einem Handlungstipp, Ansprache mit „du“.
- Marker beziehen sich auf die geprüfte Aussage („Funkstrahlung als Stressor ✕“), nicht auf unseren Satz dazu.
- Ampel nur Farbe und Text, keine Punkte. Legende: belegt / teilweise / nicht haltbar.
- Quellen durchnummeriert nach erstem Auftreten, im Video „Quellen: [n] Autor Jahr“. Die YouTube-Beschreibung hat
  nackte URLs (YouTube macht nur die klickbar), höchstens 5000 Zeichen, mit Kapitelzeiten.
- Bildausschnitte: Schrift ganz oder gar nicht, keine halben Nachbarmotive, kein Rahmenstrich der Grafik. Bei
  Schrift am Rand `zoom: "none"`. Tippfehler und Fantasieschrift der KI-Grafiken vorher korrigieren (`fix_grafik.py`).
  Falsche Aussagen im Bild nur zeigen, wenn das Video sie richtigstellt.
- Keine durchlaufende Gesamtgrafik als Einstieg.
- Stimme: ElevenLabs „Christian – Warm and Captivating“ (`NBqeXKdZHweef6y0B67V`), Modell `eleven_v4`, Tempo 1,0;
  spricht ≈ 2,1 Wörter/s, also 5 Minuten ≈ 600 Wörter. Die Antworten (JSON mit Audio und Zeitmarken) in
  `tts_cache/` einchecken, dann kosten Neu-Renders nichts.

## Zugänge (Cloud-Umgebung „Standard“)
- `ELEVENLABS_API_KEY`: vorhanden. Creator-Plan, 125.526 Zeichen pro Monat; ein 5-Minuten-Video kostet ≈ 2.000.
- **Bilder: GPT Image 2 (`gpt_image2`, 2048×1152, ≈ 6 Credits) über `werkzeug/bilder.py`, vom Nutzer am 31.10. gewählt.**
  Im Prompt „pill“ statt „tablet“ (sonst Tablet-Computer).
- `ABACUS_API_KEY` (ChatLLM/RouteLLM) für eigene Bilder: vorhanden. `POST https://routellm.abacus.ai/v1/chat/completions`,
  Modell `gemini-nano-banana-2.1`, `"modalities":["image","text"]`, `"image_config":{"aspect_ratio":"16:9"}`;
  Bild als Base64 in `choices[0].message.images[0].image_url.url`, 1376×768, ≈ 15–20 s.
  Kosten: `usage.compute_points_used` / 100 = Credits (am 31.10. gemessen: 4.175 Punkte = 41,8 Credits), ≈ 40 Credits
  pro Bild ≈ 2,7 ct im Abo (laut Nutzer 20 $ = 30.000 Credits), ≈ 4 ct nachgekauft (10 $ = 10.000). Credits erneuern
  sich am 5. des Monats. Weitere Bildmodelle (gleicher Endpunkt, gemessen 31.10., Abrechnung exakt bestätigt):
  `gpt_image25` / `gpt_image2` mit `"image_config":{"size":"1536x1024"}` (3:2, auf 16:9 zuschneiden) ≈ 6 Credits
  pro Bild; `gemini-3-pro-image` (Nano Banana Pro) ≈ 139 Credits, ohne sichtbaren Gewinn. Vergleich:
  `themen/stil/modelltest/modellvergleich.png`. Stil „Tusche und Aquarell auf warmem Papier, lockere Tuschelinien,
  Taubenblau, Terrakotta, Ocker, Salbei, kein Text“. Stil und Regeln: `themen/stil/bildleitfaden.md`, Referenz `themen/magnesium2/bildbogen.png`. Nächster Schritt: ein Skript
  `werkzeug/bilder.py`, das pro Szene ein 16:9-Bild ohne Schrift erzeugt. Jedes Bild vor dem Rendern ansehen (Schrift,
  Motiv, Stil, inhaltlich richtig).
- Gamma-Bilder: Gratis-Plan reicht nicht (Fehler 402).
- Schlüssel nie ausgeben, nie in Dateien oder den Chat. Das Repo ist öffentlich: keine Schlüssel, keine Stimmproben des
  Nutzers (geklonte Stimme „Lupert“) einchecken.

## Antworten an den Nutzer
- Kurz halten und Bilder zeigen statt viel Text (Kontaktbogen, Stichbilder, Vorher/nachher).
- Am Ende jeder Antwort genau eine Kostenzeile: `python3 tools/kosten.py` ausführen, Ausgabe wörtlich als letzte Zeile.
- Jede Internetadresse als klickbarer Markdown-Link. Wurde ein Artifact oder eine Datei veröffentlicht: den Link als letzte
  Zeile vor der Kostenzeile wiederholen (`**Link:** [Name](URL)`).

## Themenideen
- Magnesium und Vitamin D im Detail (Aktivierung, Dai 2018, Cheung 2022), angekündigt in Magnesium 2.
