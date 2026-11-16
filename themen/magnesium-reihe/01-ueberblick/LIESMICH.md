# Folge 1 „Magnesium: Was du wirklich wissen musst“ (14.11.2026)

Auftrag: `AUFTRAG.md`, Reihe: `../konzept.md`. Vorbild `themen/l-theanin/`.
- `recherche_A.md` (Nachprüfung, 2024–2026), `recherche_B.md` (Körper, Risikogruppen, Wechselwirkungen, Lebensmittel,
  Behauptungen), `faktencheck.md` (je Satz Stand und Quelle).
- `drehbuch_bau.py` → `szenen.json` / `szenen_G.json`; `szenen_hoerprobe.json` = Aussprache eingesetzt (für hoerprobe.py).
  Aussprache vorläufig: Citrat → Zitrat, Bisglycinat → Bisglyzinat, ATP → A T P. Hook-Wort „Zitrat“ (Sprechtext).
- Ton: 6:05, 788 Wörter, ElevenLabs 2.340 Zeichen berechnet. `betonung.py`: 0 markiert, 1 knapp (m5 „belegt ist das kaum“).
- Bilder: `bilder_bau.py`, 43 Szenen 5:4 + 12 Kacheln (k1–k6 Einstieg, r2–r7 Karte der Reihe) + Vorschaubild,
  787 + 6 Credits; 2 Prompts („transparent human body“) vom Filter abgelehnt und umformuliert. Alle angesehen.
- Hörprobe: https://claude.ai/artifact/JD623ifE4cG9jvVS9qSSVg (11 Stellen im Abnahme-Kasten).
- Hörprobe vom Nutzer am 14.11. abgenommen (11/11 „passt“), `abnahme.json` auf erledigt.
- Gerendert 14.11.: `render.py szenen.json bilder/G/k1.jpg video.mp4`; Startbild-Zeile auf „Tageszeit: nie verglichen.“
  gekürzt (längere Fassungen liefen ins Glas). Vorschau 720p/12 fps 13,1 MB, 1080p fürs Handy 48,3 MB (880k, zwei Durchgänge).
- Vorschau-Seite: https://claude.ai/artifact/RT23abh5FpQbhjia7SUSib (mit Vorschaubild und Beschreibung).
- 14.11. abends: Titel „Was du wirklich wissen musst“ (Nutzerwahl), Vorschaubild und Beschreibung angepasst; keine Kommentarfrage. Offen: Abnahme des Videos.
- 15.11.: Startbild wie das Vorschaubild (`hook_stil: vorschaubild`, `hook_untertitel`, neu in `werkzeug/render.py`: Titel terrakotta 210 px, Untertitel weicht der ersten Zeile, kein Zierstrich, kein Schleier), Nutzerwunsch. Neu gerendert, Vorschau-Seite oben „Startbild wie Vorschaubild“. `startbild_neu.jpg` = Standbilder 0,6 / 3 / 9 / 13,5 s.
- 15.11. Umbau Folge 1 (Nutzer: „Folge 1 umbauen“, Vorschläge der Hauptsitzung): Einstieg ohne Inhaltsverzeichnis,
  neue Reihenfolge Brauchst du es? → Wem es hilft → Wo es nicht hilft (Wende Wadenkrämpfe) → Welche Form? (mit
  Bittersalz-Geschichte, `recherche_C.md`) → Sicher einnehmen → Aus dem Essen → Fazit → Karte als offene Fragen.
  Altes Drehbuch im Git-Verlauf. Ton 6:13, 826 Wörter, ElevenLabs ≈ 2.440 Zeichen berechnet; 7 neue Bilder 200,5 Credits.
  A/B-Test von Titeln und Vorschaubildern: später (Nutzer 15.11.). Keine lange Fassung (Nutzer: keine Werbeunterbrechungen).
  Beschreibung künftig: „Keine Sponsoren, keine Affiliate-Links, keine eigenen Produkte.“
- 15.11. nachmittags: Hörprobe des Umbaus abgenommen (9/9), gerendert (6:13), Stichpunkt „Bittersalz: Epsom, überliefert 1618“, Beschreibung mit „Unabhängig: keine Sponsoren …“ und neuem Untertitel. Vorschau-Seite oben „Folge 1 · Umbau“, 1080p 49,2 MB.
- 15.11. abends: Startvarianten A (Übersicht gesprochen), B (ohne Übersicht), C (Übersicht kurz, ruhig) als
  `szenen_startA/B/C.json`, je 48 s (`render.py … --bis 48`), Seite https://claude.ai/artifact/D764YLpaH2aMtENdawPWWH.
  Neu in `render.py`: `kapitel_nr` je Szene → Lücken im Fortschrittsbalken; `kacheln_ab` = Satzzahl → Startbild bis
  Szenenende, keine Kacheln; Vorschaubild-Stil zoomt nur 6 %. Kicker jetzt „Kapitel n · …“. ElevenLabs 308 Zeichen.
- 15.11. abends: Nutzer wählt Startvariante A (Übersicht gesprochen). Bluttest-Satz präzisiert („niedriger Wert zeigt Mangel an, normaler schließt nicht aus, kein besserer Test“), Tipp ohne „Wert prüfen lassen“. Ton 6:25, 467 Zeichen. Hörprobe mit 2 Stellen.
- 15.11. abends, Notizen des Nutzers: Start verrät die Tageszeit-Antwort nicht mehr (Verweis aufs fünfte Kapitel, rote Zeile „Eine davon: nie untersucht.“); Bluttest: „Für Gesunde bringt der Bluttest deshalb wenig …“. Ton 6:30, 670 Zeichen.
- 15.11. abends: Hörprobe abgenommen, Endfassung mit Start A gerendert (6:30), Vorschau-Seite oben „Endfassung mit Start A“, 1080p 49,0 MB (820k).
- 16.11.: Übersicht „In sechs Schritten klären wir: …“ (Nutzer: „wem es hilft“ doppelt), Bild m3g → m3d bei 1:44 (Nutzer: zweimal dasselbe Bild hintereinander). Ton 6:29, 172 Zeichen. Hörprobe 1 Stelle.
- 16.11.: abgenommen, gerendert (6:29), Vorschau-Seite oben „Endfassung 16.11.“.
