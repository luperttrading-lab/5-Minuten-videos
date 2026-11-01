# Auftrag: Faktencheck-Video „Guanfacin“ (für eine eigene Sitzung)

Erteilt am 01.11.2026 aus der Sitzung „5-Minuten-Videos“ im Auftrag des Nutzers. Ziel: ein YouTube-Video von 5–6 Minuten
nach **allen** Regeln der `CLAUDE.md`. Referenz für das fertige Format: `themen/magnesium2/` (Drehbuch, Bilder,
Faktencheck, Hörprobe). Eine Vorlage-Grafik gibt es nicht: Die Behauptungen kommen aus YouTube und dem Netz.

## Besonderheit: verschreibungspflichtiges Medikament
- Keine Dosierungsempfehlungen, keine Anleitung zum Selbstversuch, kein „bestellen“ oder „ausprobieren“.
  Handlungstipps lauten „Sprich mit deiner Ärztin oder deinem Arzt über …“.
- Primärquellen zusätzlich zu Studien: Fachinformation (Intuniv), EMA/EPAR, BfArM, G-BA/IQWiG-Nutzenbewertung,
  AWMF-S3-Leitlinie ADHS, Cochrane, NICE. Zulassungsstatus (wer, wofür, ab welchem Alter) exakt prüfen.
- Nebenwirkungen und Risiken ehrlich: z. B. Blutdruckabfall, langsamer Puls, Müdigkeit, Ohnmacht, Blutdruckanstieg
  beim abrupten Absetzen (prüfen, nicht übernehmen). Off-Label-Gebrauch (Erwachsene, Angst, PTBS, Tics, „Nootropikum“)
  klar als solchen kennzeichnen.
- Herstellerstudien (Shire/Takeda) als solche nennen.

## Ablauf (Kurzfassung der CLAUDE.md, dort gilt der volle Text)
1. **Behauptungen sammeln:** 4–6 populäre deutsche (ggf. auch englische) YouTube-Videos zu Guanfacin suchen
   (`yt-dlp "ytsearch10:Guanfacin ADHS" --flat-playlist`, auch „Guanfacin Erfahrung“, „Intuniv“), Transkripte mit dem
   Skill youtube-transkript, Beschreibungen auf Affiliate-Links, Telemedizin-/Rezept-Angebote und eigene Produkte prüfen.
   Transkripte nie einchecken. Behauptungsmatrix als Bild (Vorbild `themen/magnesium2/behauptungen_youtube.png`).
2. **Faktencheck** mit Agent und Websuche, DOIs prüfen, `faktencheck.md` mit Quellenverzeichnis.
3. **Drehbuch** ≈ 720 Wörter (Christian ≈ 2,27 W/s → ≈ 5:20 + Pausen), 7–8 Szenen, jede mit Handlungstipp, Du-Ansprache,
   kaum Prozentzahlen. Mögliche Szenen: Was ist Guanfacin (Wirkweise im Stirnhirn, kein Stimulans), für wen zugelassen,
   wie gut wirkt es im Vergleich, Nebenwirkungen/Absetzen, Erwachsene und Off-Label, Mythen, Fazit.
   Entwurf dem Nutzer zeigen, bevor Ton erzeugt wird.
4. **Bilder:** GPT Image 2 über `werkzeug/bilder.py`, 2 pro Szene, Erklärbilder für Abläufe (z. B. Signal im
   präfrontalen Kortex, Alpha-2A-Rezeptor als Bremse/Filter). Fürs Handy: Motiv groß, Beschriftung groß.
   Keine Tablettenpackungen mit Markennamen. Bildbogen freigeben lassen.
5. **Ton und Hörprobe:** `render.py --nur-ton`, `betonung.py`, Hörprobe als Artifact (`hoerprobe.py`), Abnahme mit
   „Übernehmen/Nochmal“ und „Hörprobe abnehmen“. Werkzeugnamen: Gibt es `publish_files`/`declare_capabilities` nicht,
   das Artifact-Tool mit `capabilities: {"db": {}, "comments": {}}` nutzen und Markierungen mit `ArtifactData`
   (Sammlung `markierungen`) lesen und schreiben. **Erst rendern, wenn der Nutzer abgenommen hat.**
6. **Rendern, Beschreibung (mit Hinweis „kein Ersatz für ärztlichen Rat“), 480p** an den Nutzer schicken.

## Zusammenarbeit
- Direkt mit dem Nutzer: Deutsch, Du, kritisch, Aussagen markieren mit [Sicher]/[Wahrscheinlich]/[Vermutung], kurze
  Antworten, Bilder statt Text, Kostenzeile mit `tools/kosten.py`, Push-Nachricht aufs Handy, wenn etwas fertig ist.
- Nur in `themen/guanfacin/` arbeiten; `werkzeug/` und `CLAUDE.md` nur, wenn nötig, und dann klein.
  Vor jedem Push `git pull --rebase origin main`: Andere Sitzungen arbeiten parallel im selben Repo.
