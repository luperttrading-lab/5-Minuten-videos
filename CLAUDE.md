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
5b. **Betonung prüfen:** `python3 ../../werkzeug/betonung.py szenen.json` (Vorfilter, Verfahren aus dem Seneca-Hörspiel),
   dann Hörprobe zum Mitlesen und Markieren: `python3 ../../werkzeug/hoerprobe.py szenen.json hoerprobe` (nach dem Rendern,
   braucht video.wav), als Artifact mit `publish_files` veröffentlichen, danach `declare_capabilities` mit
   `{"db": {}, "comments": {}}`. „An Claude“ auf der Seite schickt die Notiz als Kommentar und weckt die Sitzung.
   Langer Druck auf ein Wort markiert direkt. Danach `python3 ../../werkzeug/bildwahl.py szenen.json hoerprobe`: je Szene
   alle Bilder antippbar (mehrere = beide, in Reihenfolge; Sammlung `bildwahl`, Feld `bilder`) und „Notiz zum ganzen
   Kapitel“ (Sammlung `kapitelnotizen`, geht auch als Kommentar an Claude).
   **Abnahme ohne Suchen** (Nutzerwunsch 02.11.): Vor jeder Bitte um Abnahme `python3 ../../werkzeug/abnahme.py
   szenen.json hoerprobe abnahme.json` – Kasten ganz oben mit allen geänderten Stellen seit dem letzten Durchgang (je ▶,
   „passt“/„nochmal“) und EINEM Knopf „Abnehmen und rendern“ (Kommentar an Claude, Sammlung `abnahme`).
   **Nach jeder Runde aufräumen:** bearbeitete Markierungen per ArtifactData-Batch von `markierungen` nach
   `markierungen_erledigt` verschieben (nicht löschen), sonst stehen sie oben als „offen“. Nach dem Rendern in
   `abnahme.json` den Schlüssel `erledigt` setzen: Der Kasten zeigt dann nur „✓ Alles abgenommen, nichts offen“.
   Markierungen des Nutzers mit `db_list` (Sammlung `markierungen`) lesen, betroffene Sätze einzeln in 2–3 Fassungen neu.
   **Reihenfolge:** Korrekturen nur in die Hörprobe (vorher/nachher). Erst rendern, wenn der Nutzer die Hörprobe
   abgenommen hat.
   Abnahme auf der Seite: je Stelle „✓ Übernehmen“ / „Nochmal“ (Feld `abnahme` = ok | nochmal), dann „Hörprobe abnehmen“
   (Kommentar an Claude). Neue Fassungen: Satz aus dem tts_cache schneiden, `vorher`/`nachher` per db_write setzen.
6. **Rendern:** dasselbe ohne `--nur-ton` (≈ 4–5 min Rechenzeit), danach Kontrollbilder mit `--bild <Sekunde>`.
7. **Beschreibung und Teilen-Seite:** `python3 ../../werkzeug/beschreibung.py szenen.json video_zeitplan.json`
8. **Ausliefern:** 1080p (Master, nicht einchecken), 720p für die Teilen-Seite (Artifact), 480p zum Verschicken:
   `ffmpeg -i video.mp4 -vf "crop=1920:1072:0:0,fps=15,scale=854:480:flags=lanczos" -c:v libx264 -preset slow -crf 30
   -tune stillimage -profile:v main -pix_fmt yuv420p -c:a aac -b:a 64k -ac 1 -movflags +faststart video_480p.mp4`
   Videos über die Vorschau-Seite zeigen (siehe „Antworten an den Nutzer“), nicht als Datei. MP4s nie committen: Sie lassen sich aus Drehbuch, Grafik und Ton-Cache jederzeit neu rendern.

## Aufbau `szenen.json`
- Kopf: `tts` (`elevenlabs`), `voice_id`, `model`, `tempo`, `aussprache` (nur Sprechtext, z. B. `{"Guanfacin": "Guanfazihn"}`,
  Nutzerwahl 02.11.: Fachwörter vorher mit Proben anhören lassen), `titel`, `untertitel`, `fuss`, `quellen` (Verzeichnis
  `id → kurz, voll, url`).
- Erste Szene `layout: "kacheln"`: sechs Kapitel-Kacheln (`kacheln: [{t, a, wort}]`). Jede Kachel leuchtet auf, wenn ihr
  `wort` gesprochen wird (ElevenLabs-Zeitmarken). `hervorheben_at`/`legende_at` = Satznummer. Die Legende wird nur
  eingeblendet, **nicht gesprochen** (kein Satz „Grün heißt belegt …“, Nutzerwunsch 02.11.: stört den Einstieg).
  Hook vor den Kacheln: `hook_bild` (Vollbild, Zoom 12 %) bis Satz `kacheln_ab`, dann Überblendung zu den Kacheln.
  Im Hook immer Text (Nutzerwunsch 02.11.): `hook_titel` (Thema groß, z. B. „Guanfacin“) und `hook_zeilen`
  (`[{t, wort, art}]`, jede Zeile erscheint beim gesprochenen `wort`; `art: "urteil"` = rot, z. B. „Nicht alles davon
  hält.“). Hook-Bild mit leerer linker Hälfte bestellen (Platz für den Text). Kicker der Kachel-Szene nur
  „Faktencheck“ (kein „Info-Video“). Beispiel `themen/guanfacin/`.
- Weitere Szenen: `kicker`, `headline`, `sentences` (Text oder `{t: Anzeige, say: Sprechtext}`; Zahlen im
  Sprechtext ausschreiben), `bullets` (`{t, at, ev}` mit `ev` = `stark` | `mittel` | `keine`), `evidence`
  (`level`, `label`), `quellen` (IDs aus dem Verzeichnis), `shots` (`{a: [x0,y0,x1,y1], at, zoom}`, `zoom` =
  `out` | `none`, Standard: 5 % hinein). Eigenes Bild statt Grafik: `bild: "bilder/x.png"` (relativ zum
  Drehbuch, auch in Kacheln); ohne `a` wird das ganze Bild gezeigt.

## Gestaltungsregeln
- Zahlen sparsam: kaum Prozentzahlen, höchstens eine Zahl pro Satz. Lieber Brüche und Vergleiche („jeder Vierte“,
  „von zwei Dritteln auf ein Zehntel“, „so viel wie in ein, zwei Mandeln“). Die Zuschauer sind keine Statistiker.
- Jede Szene endet mit einem Handlungstipp, Ansprache mit „du“. Beide Formen nennen, nicht gendern: „Arzt oder
  Ärztin“ (nicht nur „Ärztin“, kein Stern, kein Doppelpunkt; Nutzerwunsch 02.11.).
- Marker beziehen sich auf die geprüfte Aussage („Funkstrahlung als Stressor ✕“), nicht auf unseren Satz dazu.
- Ampel nur Farbe und Text, keine Punkte. Legende immer dreistufig: belegt / teilweise / nicht haltbar. Keine blaue
  vierte Stufe mehr (Nutzerentscheidung 02.11. abends, ersetzt die Regel vom Nachmittag): Sie sortierte junge, dünne
  Belege vor Gelb ein, obwohl sie oft schwächer sind, und kam in der ganzen Reihe nur einmal vor. Stattdessen bei Gelb
  der Zusatz `"neu": true` oder `"neu": "erst eine kleine Studie"` (Kästchen unter dem Stichpunkt, Standardtext „erst
  wenige, kleine Studien“); nur bei `ev: "mittel"`, nie bei Rot (liest sich sonst wie „eine Studie zeigt, dass es falsch
  ist“). Alte Drehbücher mit `ev: "frueh"` rendert `render.py` automatisch als Gelb mit Zusatz.
  Gefährliche Behauptungen zusätzlich `"gefahr": true` (⚠). Farbe = Stärke der Belege, Zeichen = Eigenschaft.
  Rote Stichpunkte: Behauptung in Anführungszeichen, dahinter rot „ist falsch“ (Nutzerwahl 02.11., `ROT_STIL` B im Renderer).
  Unterscheidung (Nutzerentscheidung 02.11.): „ist falsch“ nur bei Gegenbeleg (Studien zeigen das Gegenteil);
  fehlen Belege ganz (nicht untersucht, nur Hersteller-Kleinststudie), `"unbelegt": true` → rot „ist nicht belegt“.
  Beide bleiben Rot („nicht haltbar“): Eine unbelegte Behauptung ist nicht richtig, aber auch nicht widerlegt.
  Startbild (Kacheln): vor der Ampel steht „Beweislage:“, oben bleibt „Faktencheck“ (Nutzerwahl 02.11.: dasselbe Wort
  wie im Kasten jeder Szene; die Ampel misst die Belege, nicht unsere Meinung). Schrift fürs Handy vergrößert: Legende
  auf dem Startbild 36 px, in den Szenen 28 px, Kasten „Beweislage: …“ 30 px.
- Quellen durchnummeriert nach erstem Auftreten, im Video „Quellen: [n] Autor Jahr“. Die YouTube-Beschreibung hat
  nackte URLs (YouTube macht nur die klickbar), höchstens 5000 Zeichen, mit Kapitelzeiten.
- Bildausschnitte: Schrift ganz oder gar nicht, keine halben Nachbarmotive, kein Rahmenstrich der Grafik. Bei
  Schrift am Rand `zoom: "none"`. Tippfehler und Fantasieschrift der KI-Grafiken vorher korrigieren (`fix_grafik.py`).
  Falsche Aussagen im Bild nur zeigen, wenn das Video sie richtigstellt.
- Keine durchlaufende Gesamtgrafik als Einstieg.
- **Hook in den ersten 8–10 Sekunden** (Nutzerentscheidung 02.11., Strategiepapier `themen/beratung/strategiepapier.pdf`):
  **zuerst das Thema nennen** („Guanfacin: …“, Nutzerwunsch 02.11., Hook dadurch ≈ 9,6 s abgenommen), dann ein Satz mit
  der stärksten Behauptung und einem offenen Versprechen, ohne Begrüßung, erst danach die Kacheln.
  Zuspitzen ja, täuschen nein; der Hook wird im Video eingelöst.
- **Abschlusssatz** jedes Videos, gesprochen nach dem Fazit (Nutzerentscheidung 02.11.): „Gut, dass du dich informierst.
  Das Video kann das Gespräch mit Arzt oder Ärztin unterstützen, aber nicht ersetzen. Bis zum nächsten Video!“
  („Bis zum nächsten Video!“ ergänzt am 02.11.: freundlicher Ausklang statt Zeigefinger.) Ersetzt „Dieses Video ersetzt
  keinen ärztlichen Rat“. Nicht den HWG-Pflichttext („… fragen Sie Ihre Ärztin, Ihren Arzt oder in Ihrer Apotheke“)
  nachahmen, er klingt nach Arzneimittelwerbung. Konkrete Sicherheitssätze („nie plötzlich absetzen“) bleiben in der Szene.
- Stimme: ElevenLabs „Christian – Warm and Captivating“ (`NBqeXKdZHweef6y0B67V`), Modell `eleven_v4`, **Tempo 1,05**
  (Nutzerentscheidung 02.11., `"tempo": 1.05` im Drehbuch, wirkt nachträglich ohne neuen Ton). Grund: Bei 1,00 sprach er
  3,94 Silben/s, langsamer als alle 12 gemessenen deutschen Erklärvideos (Median 4,48; Kurzgesagt/Simplicissimus
  4,16–4,36); 1,05 ergibt ≈ 4,14 Silben/s ≈ 2,28 Wörter/s, also 6 Minuten ≈ 780 Wörter. Messung:
  `themen/stil/sprechtempo/`.
  Stimme am 02.11. bestätigt (Sprecherprobe gegen Alexander, Marko, Marcus, Leo: `themen/stil/stimmprobe/`).
- Tonaufbereitung fest im Renderer (Nutzerentscheidung 02.11.): Rauschunterdrückung und De-Esser wie im Seneca-Projekt,
  lineare Verstärkung auf −16 LUFS statt dynamischem loudnorm (`AUFBEREITUNG` in `werkzeug/render.py`, abschaltbar mit
  `"aufbereitung": false`). Grund: Roh rauschte Christian in Pausen bei −50 dB („blechern, knisternd“). Die Antworten (JSON mit Audio und Zeitmarken) in
  `tts_cache/` einchecken, dann kosten Neu-Renders nichts.

## Zugänge (Cloud-Umgebung „Standard“)
- `ELEVENLABS_API_KEY`: vorhanden. Creator-Plan, 125.526 Zeichen pro Monat; ein 5-Minuten-Video kostet ≈ 2.000.
- **Bilder: GPT Image 2 (`gpt_image2`, 2048×1152, ≈ 6 Credits) über `werkzeug/bilder.py`, vom Nutzer am 31.10. gewählt.**
  Im Prompt „pill“ statt „tablet“ (sonst Tablet-Computer).
  Bilder fürs Handy: Motiv groß, Fläche ausnutzen, wenige große Elemente, Beschriftung gut lesbar (Leitfaden).
  Einzelne kurze Beschriftungen („Vitamin D“, „Mg“) schreibt GPT Image 2 korrekt; trotzdem jedes Bild prüfen.
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
- **Videos nie als Datei in den Chat** (Nutzerwunsch 02.11.: landen auf dem Handy, belegen Speicher, spielen dort
  stumm). Stattdessen je Thema eine feste Vorschau-Seite: `python3 ../../werkzeug/vorschau.py vorschau.json vorschau`,
  als Artifact mit `{"db": {}, "comments": {}}` veröffentlichen und immer dieselbe URL aktualisieren; neueste Fassung
  oben, „zu prüfen“ / „zur Info“, je Video höchstens 16 MB (ganzes Video 720p/12 fps). Dateien (480p, 1080p) nur,
  wenn der Nutzer sie ausdrücklich will, z. B. 1080p für den Upload. Einstieg testen: `render.py … --bis 17`.
- **Aufbau jeder Antwort** (Nutzerwunsch 05.11., gilt für alle Sitzungen; ersetzt „Deine Aufgabe“ als erste Zeile und
  „Link wiederholen“): oben kurz, was gemacht wurde. **Am Ende**, in dieser Reihenfolge:
  1. Bilder und Dateien erst jetzt schicken (`SendUserFile`), nicht mitten im Text.
  2. **„Deine Aufgabe: …“** – jede offene Entscheidung oder Abnahme als kurzer Arbeitsauftrag, auch wenn sie oben schon
     erwähnt wurde: Link, Ort auf der Seite, Zahl der Stellen („oben im Kasten, 10 Stellen, dann grüner Knopf“). Nie
     nur „bitte abnehmen“ (Suchzeit). Nichts offen: kein Aufgabenblock.
  3. Die festen Links des Projekts als beschriftete Liste, jeden **genau einmal** (Mathe: drei, siehe dort); der
     Arbeitsauftrag verweist darauf („Auswahl-Seite, Link unten“) statt den Link zu wiederholen.
  4. Kostenzeile.
  **Jeder offene Punkt mit eigenem Link** (Nutzerwunsch 02.11.), auch Entscheidungen, die im Chat beantwortet werden:
  Vergleichsbilder dafür als Eintrag auf die Vorschau-Seite (Standbild als kurzes Video, „passt“ = übernehmen), damit
  alles Offene an einem Ort mit Link liegt. Nie ein Kürzel („Variante D“) ohne Bild und Link wiederholen.
  Reine Textentscheidungen (z. B. Titel) direkt im Chat als nummerierte Liste, ohne Bildtafel (Nutzerwunsch 05.11.).
- Am Ende jeder Antwort genau eine Kostenzeile: `python3 tools/kosten.py` ausführen, Ausgabe wörtlich als letzte Zeile.
- Jede Internetadresse als klickbarer Markdown-Link.

## Mathe-Videos (`themen/mathe-*`, eigenes Format ohne Ampel)
- Vorlage: `themen/mathe-einmaleins/regel.py` (Bilder ganz per Code, Formeln nie per KI-Bild; Einblendungen hängen an
  gesprochenen Wörtern). Vorschau-Seite aller Mathe-Proben: `themen/mathe-stilprobe/vorschau.json`.
- **Am Schluss immer ein Motivationssatz** (Nutzerwunsch 04.11.), z. B. nach einer Übung: „Länger als vier Sekunden? Ganz
  normal. Mit ein bisschen Übung schaffst du das auch.“ plus ein **wechselnder Spruch** („Das ist kein Hexenwerk.“, „Das
  ist keine Raketenwissenschaft.“ …) aus `werkzeug/motivation.py` (`spruch(thema, 'schluss')`; `'bruecke'` für Übergänge).
  Ein Thema behält seinen Spruch, neue Themen bekommen den seltensten. Sprüche gern ergänzen.
- **Zu jedem Mathe-Video eine Übung** in der App `uebung/` (https://luperttrading-lab.github.io/5-Minuten-videos/uebung/,
  Nutzerwunsch 04.11.: 10 Aufgaben, tippen oder sprechen, richtig gezählt, Ø-Zeit). Neue Übung in `uebung/aufgaben.js`,
  `APP_VERSION` hochzählen, `node uebung/tests/uebung.mjs` muss „Alles grün“ melden. Details `uebung/LIESMICH.md`.
- **Links am Ende jeder Antwort** (Nutzerwunsch 05.11. abends, ersetzt „nur der gebrauchte Link“), beschriftet, damit
  das fertige Video nicht zwischen den Proben gesucht werden muss:
  - **Fertige Videos:** [Kopfrechnen · fertige Videos](https://claude.ai/artifact/KtWyuT3JFmgu3yVphKcAH4) – nur die
    abgenommenen Fassungen mit YouTube-Titel (Kopieren-Knopf) und Vorschaubild. Nach jeder Abnahme `fertig.json` in
    `themen/mathe-stilprobe/` nachziehen, `python3 ../../werkzeug/fertig.py fertig.json <ordner>`, mit `publish_files`
    auf Slug `98f5e798-15cf-46ab-8792-8c95d9d0393f` (nur geänderte Dateien, alte entfernen).
  - **Auswahl und Proben:** [Mathe-Videos · Vorschau](https://claude.ai/artifact/PVisw26MxXcVy1NJngcMFu)
  - **App:** [Kopfrechnen üben](https://luperttrading-lab.github.io/5-Minuten-videos/uebung/)
- **Ziel vier Sekunden** (Nutzerentscheidung 05.11.): Video und App-Stufe „Alle Zahlen“ sagen „in vier Sekunden“ (Uhr
  `UHR = 4` in `regel.py`), der Sonderfall „Einer ergeben 10“ bleibt bei drei (`ziel` je Stufe in `uebung/aufgaben.js`).
  Grund: Drei Sekunden mit Rechnen frustrieren; die meistgesehenen Videos nennen 3–5 s, tecmath für genau diesen Trick 4 s.
- **Name des Tricks** (Nutzerwahl 05.11., Serie geplant: `themen/mathe-tricks/`, 127 Folgen): kurzer Name („Der
  Zehner-Trick“), im Einstieg gesprochen („Mit dem Zehner-Trick schaffst du das …“) und als Band unter der Aufgabe
  eingeblendet, sobald die Lösung steht. Kein eigenes Startbild vor dem Einstieg (kostet die ersten Sekunden); oben links
  bleibt „Kopfrechnen“ als Name der Reihe, wie die App.
- **YouTube-Vorschaubild der Reihe** (Nutzerwahl 05.11.: ein Design für alle Folgen, Wiedererkennung): Stil „Papier mit
  Teal-Leiste unten“ aus `themen/mathe-einmaleins/vorschaubild.py` (`papier`): Aufgabe groß mit „= ?“, Einer orange und
  violett wie im Video, unten die grüne Leiste mit Name des Tricks links und „KOPFRECHNEN“ rechts. Je Folge nur Aufgabe
  und Name in `FOLGEN` ändern, keine Uhr (nicht jeder Trick hat ein Zeitversprechen). Fertig: `vorschaubild_zehner.png`.
- **YouTube-Titel nach Suchbegriffen** (Nutzerwunsch 05.11.: „was am meisten gesucht wird“): vorher die
  YouTube-Suchvorschläge abfragen (`https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=de&gl=de&q=…`;
  zeigt, was gesucht wird, nicht wie oft). Stand 05.11.: „großes Einmaleins“ (Tricks, im Kopf rechnen), „im Kopf
  multiplizieren“, „Kopfrechnen Trick multiplizieren“, „Zahlen von 11 bis 19 im Kopf multiplizieren“; niemand sucht
  „malnehmen“ oder eine konkrete Aufgabe wie „16 mal 18“. Aufbau (Nutzerwahl 05.11.): Name des Tricks vorn, dann
  ein Suchwort („großes Einmaleins“ statt „Kopfrechnen“, das steht schon im Vorschaubild), dann das Beispiel mit dem
  Versprechen, z. B. „Zehner-Trick: großes Einmaleins im Kopf – 16 · 18 in 4 Sekunden“. Titel je Folge in `youtube.md`.
- **Eigener YouTube-Kanal für die Mathe-Videos** (Nutzerentscheidung 05.11.), getrennt von den Gesundheits-Faktenchecks.
  Später evtl. „Statistik leicht gemacht“; ob eigener Kanal oder zusammen mit Kopfrechnen, ist offen.
- **Endbildschirm** (Nutzerwahl 05.11., Szene `abspann` in `regel.py`): nach dem Motivationssatz gesprochen „Noch ein
  Trick? Hier geht's weiter. Und damit du keinen verpasst: Abonnier den Kanal.“ (für jede Folge gleich, kein bestimmtes
  Video ankündigen), dann `ABSPANN` = 8 s still. Bild: „Noch ein Trick?“, zwei Flächen für Video-Empfehlungen, Kreis
  „Kanal abonnieren“; YouTube Studio legt die Elemente darauf (nur letzte 5–20 s, nicht bei „für Kinder gemacht“).
  Muss vor dem Hochladen im Video sein. Idee für später (Nutzer 05.11., noch nicht einbauen): Abo-Knopf zum Schluss
  animiert „drücken“.
- **Geprüft und verworfen** (Nutzerentscheidung 04.11.): Abweichungs-Kreuz (tecmath/vedisch, Probe `kreuz_probe.py`) –
  unser Flächenmodell mit „Andersherum“ erklärt es besser. Recherche der meistgesehenen Videos zum Trick: kein anderer
  Rechenweg, nur andere Darstellungen (Fläche ohne Drehen, von rechts rechnen, Finger bis 15, Basis 20).
- **Merksätze so sprechen, wie sie dastehen** (Nutzerwunsch 04.11.): keine Kurzformen („Einer rüber“), die man nur
  lesend versteht; der Merkzettel zeigt genau die gesprochenen Sätze.
- **Geräusche sparsam** (Nutzer 04.11.): kein „Plopp“ (klang wie „Boing“); Glöckchen nur zusammen mit den Funken an den
  grünen Endergebnissen. Klicks der Sprachausgabe in Pausen dämpft `entknacksen` in `regel.py` (≈ 30 → 5), dazu
  Tiefpass 12 kHz. Vorschau-Ton direkt aus der WAV kodieren (`-map 1:a`, AAC 160k), nicht AAC aus AAC.
- **Keine künstlichen Pausen in den Ton schneiden** (Messung 04.11.): Christian pausiert an Satzenden selbst 200–500 ms,
  die Zeitmarken sind nur auf ≈ 40 ms genau, Schnitte landeten im Wort („Sprechabsetzer“).

## Themenideen
- Fahrplan aus dem Strategiepapier (vom Nutzer am 02.11. gutgeheißen, erst angehen, wenn die fünf vorhandenen Videos
  nach Vorlage v2 überarbeitet sind): Vitamin D (Telomere, Testen, Megadosen), Mikroplastik im Gehirn, Kollagen,
  Berberin („natürliches Ozempic“), Magnesium-L-Threonat. Reserve: Kreatin fürs Gehirn, 16:8-Essen, Ashwagandha.
- Magnesium und Vitamin D im Detail (Aktivierung, Dai 2018, Cheung 2022), angekündigt in Magnesium 2.
