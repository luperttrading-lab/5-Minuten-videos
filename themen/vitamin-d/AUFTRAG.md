# Auftrag: Probevideo „Vitamin D“, komplett ohne Rückfragen

Erteilt am 03.11.2026 aus der Sitzung „Fünf-Minuten-Infovideo“ im Auftrag des Nutzers.

**Wortlaut des Nutzers:** „Produziere die Bilder und alles nach den bisherigen Richtlinien und rendere ohne Rückfragen schon ein fünfminütiges Probevideo mit echter Stimme. Dabei musst du überlegen, was alles wichtig ist, was ins Video rein muss.“

## Was von der CLAUDE.md abweicht (nur für dieses Probevideo)
- **Keine Freigaben vor Ton, Bildern oder Rendern.** Normalerweise zeigst du Entwurf, Bildbogen und Hörprobe vorher. Hier triffst du alle Entscheidungen selbst und renderst durch.
- **Danach** baust du die übliche Vorschau-Seite mit Hörprobe, Bildwahl und Abnahmekasten. Darüber kann der Nutzer später korrigieren. Deine eigenen Entscheidungen listest du dort unter „zur Info“ auf, kurz und mit Grund.
- **Alles andere gilt unverändert:** Faktencheck vor dem Drehbuch, kein ungeprüfter Punkt, dreistufige Ampel mit „Beweislage:“, nummerierte Quellen, Kachel-Einstieg, Stimme Christian, Bilder mit GPT Image 2 über `werkzeug/bilder.py` nach `themen/stil/bildleitfaden.md`, Betonungsprüfung, Herkunft der Behauptungen nicht nennen, Affiliate- und Produktempfehlungen raus, Videos nicht als Datei in den Chat, sondern über die Vorschau-Seite.
- Der Fahrplan sah Vitamin D erst nach der Überarbeitung der alten Videos vor. Der Nutzer zieht das Thema jetzt bewusst vor.

## Was wichtig ist und ins Video gehört
Die folgende Liste sind Kandidaten, keine Fakten. Jeden Punkt prüfen, Zahlen aus Primärquellen holen.
1. **Woher Vitamin D kommt:**
   - Bildung über UVB in der Haut, wenig aus Lebensmitteln (Fettfisch, UV-Pilze).
   - In Deutschland reicht die Sonne etwa von Oktober bis März kaum für die Eigenbildung.
   - Einflussfaktoren: Alter, Hauttyp, Übergewicht, Sonnencreme. Faustregel mit der Schattenlänge prüfen.
2. **Wie verbreitet ein Mangel wirklich ist:**
   - RKI-Daten zu den Anteilen unter 30 und unter 50 nmol/l.
   - Mangel und „suboptimal“ unterscheiden.
   - Einheiten nmol/l und ng/ml (Faktor 2,5), dazu der Streit um Zielwerte (50, 75, „100+“).
3. **Testen:** Endocrine-Society-Leitlinie 2024 (keine Routine-Tests, Gruppen für eine Einnahme ohne Test), IGeL für Gesunde, Risikogruppen.
4. **Was die großen Studien zeigen:**
   - Hauptstudien: VITAL (Manson 2019), D-Health (Neale 2022), DO-HEALTH, ViDA.
   - Endpunkte: Krebs, Herz, Sterblichkeit, Stürze und Brüche bei Normalversorgten.
   - Krebssterblichkeit (Meta-Analysen), Atemwegsinfekte (Jolliffe 2021), COVID (CORONAVIT), Depression (VITAL-DEP), Diabetes (D2d, Pittas 2023), Autoimmunerkrankungen (Hahn 2022).
   - Telomere: Zhu 2025, AJCN, VITAL-Substudie. Nur ein Surrogat, die Medienzeile „Altern um drei Jahre gebremst“ prüfen.
5. **Megadosen:**
   - Behauptungen wie „10.000 IE täglich“ oder „60.000 IE täglich“.
   - Risiken: Hyperkalzämie, Nierenschäden, Vergiftungsfälle. Bolus-Gaben und Stürze (Sanders 2010).
   - Grenzwerte: BfR höchstens 20 µg pro Tag aus Nahrungsergänzungsmitteln, EFSA-Obergrenze 100 µg, DGE-Schätzwert 20 µg ohne Eigenbildung.
   - Stiftung Warentest: viele Präparate überdosiert.
6. **Kombinationen:** Vitamin K2 (Belege?) und Magnesium als Kofaktor (Dai 2018), nur kurz.
7. **Wo es klar sinnvoll ist:** Rachitis-Vorbeugung bei Säuglingen, Ältere bzw. Pflegeheim, Schwangere nach Leitlinie.
8. **Behauptungen sammeln:** 4–6 populäre deutsche Vitamin-D-Videos, Vorgehen wie im Guanfacin-AUFTRAG. YouTube blockierte am 02.11. Einzelabrufe (HTTP 429). Ist das noch so, mit `player_client=web_embedded` nach CLAUDE.md von `fragen-allgemein` versuchen, sonst Titel, Beschreibungen und Presse nutzen. Notiere, was nicht ging.

**Umfang:** 7–8 Szenen plus Kachel-Einstieg, jede Szene mit einem Handlungstipp, Du-Ansprache, wenige Prozentzahlen. Etwa 680–720 Wörter, Ziel 5:00–5:30.
**Bildideen** (Motiv groß, kurze Beschriftungen, alles prüfen): Sonnenstand Sommer gegen Winter, UVB auf Haut, Blutröhrchen und Laborwert, Waage oder Dosis als Erklärbild, große Studie als Menschenmenge, Warnbild für Megadosen, Lebensmittel, Säugling mit Tropfen. Keine Präparate mit Markennamen.
**Hinweis im Video und in der Beschreibung:** „kein Ersatz für ärztlichen Rat“. Keine Dosierungsanleitungen über die offiziellen Empfehlungen hinaus.

## Abgabe
- Video vollständig rendern, `beschreibung.py` laufen lassen, die Vorschau-Seite mit fester URL veröffentlichen (Video 720p/12 fps höchstens 16 MB, Hörprobe, Bildwahl, Abnahmekasten).
- Dem Nutzer kurz berichten. Erste Zeile „Deine Aufgabe: …“ mit Link und Ort auf der Seite: ansehen, Stellen markieren, abnehmen.
- Push-Nachricht aufs Handy, Kostenzeile mit `tools/kosten.py`. Nenne die ElevenLabs-Zeichen und die Bild-Credits. Stand vorher: 62.589 von 125.526 ElevenLabs-Zeichen verbraucht.
- Nur in `themen/vitamin-d/` arbeiten, `werkzeug/` und `CLAUDE.md` nur klein und wenn nötig. Vor jedem Push `git pull --rebase origin main`, denn andere Sitzungen arbeiten im selben Repo.

## Zum Nutzer
Trader, Statistiker, Finanzmathematiker. Diktiert per Sprache, Erkennungsfehler mitdenken („Gitarre“ = GitHub, „Or“ = PR, „Leven“ = ElevenLabs). Will kurze Antworten und Bilder statt Text. Deutsch, Du, kritisch, Aussagen markieren mit [Sicher]/[Wahrscheinlich]/[Vermutung].
