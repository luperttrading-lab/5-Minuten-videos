# Auftrag: Faktencheck-Video „Tomatenmark“ (für eine eigene Sitzung)

Erteilt am 01.11.2026 aus der Sitzung „5-Minuten-Videos“ im Auftrag des Nutzers. Ziel: ein YouTube-Video von 5–6 Minuten
nach **allen** Regeln der `CLAUDE.md` (Ablauf, Gestaltung, Bilder, Hörprobe). Referenz für das fertige Format:
`themen/magnesium2/` (Drehbuch, Bilder, Faktencheck, Hörprobe).

## Vorlage
`vorlage/aquarell.png` und `vorlage/knete.png` (Gemini Notebook). Behauptungen darin, alle zu prüfen:
- Tomatenmark liefert bis zu 20-mal mehr verwertbares Lykopin als frische Tomaten (zerkleinerte Zellwände).
- Hitze und Öl wandeln all-trans- in leichter aufnehmbares cis-Lykopin um.
- Mit Olivenöl über 80 % höhere Aufnahme.
- Lykopin fängt freie Radikale im Gehirn, reichert sich im Stirnhirn an und steigert BDNF (Grafik schreibt „BUNF“).
- 35 g Tomatenmark täglich = bessere Konzentration und Namensgedächtnis bei 40- bis 55-Jährigen.
- 55 % geringeres Schlaganfallrisiko; fördert Stickstoffmonoxid; senkt LDL um etwa 10 %.
- Schutz der Leber (Fettverbrennung, Fettleber-Risiko), mehr Bifidobakterien im Darm.
- Synthetisches Lykopin (Kapseln) ist wirkungslos, nur der natürliche Komplex zählt.
- Schützt Frauen vor Knochenabbau nach den Wechseljahren; senkt bei Männern das Prostatakrebs-Risiko.

## Ablauf (Kurzfassung der CLAUDE.md, dort gilt der volle Text)
1. **Behauptungen sammeln, wo die Zuschauer sind:** 4–6 populäre deutsche YouTube-Videos zu Tomatenmark/Lykopin suchen
   (z. B. `yt-dlp "ytsearch10:Tomatenmark Lykopin Gehirn" --flat-playlist`), Transkripte mit dem Skill
   youtube-transkript, Beschreibungen auf Affiliate-Links und eigene Produkte prüfen. Transkripte nie einchecken.
   Dem Nutzer eine Behauptungsmatrix als Bild zeigen (Vorbild `themen/magnesium2/behauptungen_youtube.png`).
2. **Faktencheck** mit Agent und Websuche, DOIs prüfen, `faktencheck.md` mit Quellenverzeichnis.
   Produktgebundene Empfehlungen ohne unabhängige Stütze kommen gar nicht ins Video. Keine Namen von Ärzten/Kanälen.
3. **Drehbuch** ≈ 720 Wörter (Christian spricht ≈ 2,27 W/s, also ≈ 5:20 + Pausen), 7–8 Szenen, jede mit Handlungstipp,
   Du-Ansprache, kaum Prozentzahlen (Vergleiche statt Zahlen). Entwurf dem Nutzer zeigen, bevor Ton erzeugt wird.
4. **Bilder:** GPT Image 2 über `werkzeug/bilder.py`, 2 pro Szene (Situation + Tipp), Erklärbilder für Abläufe
   (z. B. Lykopin: Tomate → Hitze und Öl → Darm → Blut → Gehirn). Fürs Handy: Motiv groß, Beschriftung groß.
   Bildbogen dem Nutzer zeigen und freigeben lassen.
5. **Ton und Hörprobe:** `render.py --nur-ton`, `betonung.py`, Hörprobe als Artifact (`hoerprobe.py`, dann
   `declare_capabilities` mit `{"db": {}, "comments": {}}`). Markierungen per `db_list` lesen, Korrekturen mit
   vorher/nachher. **Erst rendern, wenn der Nutzer die Hörprobe abgenommen hat.**
6. **Rendern, Beschreibung, 480p** an den Nutzer schicken.

## Zusammenarbeit
- Du arbeitest direkt mit dem Nutzer (Deutsch, Du, kritisch, Aussagen markieren mit [Sicher]/[Wahrscheinlich]/[Vermutung],
  kurze Antworten, Bilder statt Text, Kostenzeile mit `tools/kosten.py`, Push-Nachricht aufs Handy, wenn etwas fertig ist).
- Arbeite nur in `themen/tomatenmark/`. Änderungen an `werkzeug/` oder `CLAUDE.md` nur, wenn nötig, und dann klein.
  Vor jedem Push `git pull --rebase origin main`: Eine zweite Sitzung arbeitet parallel im selben Repo.
