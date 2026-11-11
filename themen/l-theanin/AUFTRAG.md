# Auftrag: Erklärvideo „L-Theanin“ im Aquarell-Stil (Schulprojekt-Format)

Erteilt am 11.11.2026 aus der Sitzung „Fünf-Minuten-Infovideo“ im Auftrag des Nutzers. Lege diesen Text als ersten Schritt unter `themen/l-theanin/AUFTRAG.md` ab und committe ihn.

**Wortlaut des Nutzers (diktiert, geglättet):** „Ich würde gern ein Video machen wie DMSO und PEA im Aquarellstil, sonst auch alles genauso recherchiert und dargestellt, und zwar über L-Theanin. Ich habe dir dazu ein Bild hinzugefügt. Das sollst du aber erst angucken, wenn du deine eigene Recherche fertig hast und in die Videoproduktion gehen könntest. Dann kannst du anhand dieses Bildes gucken, was du davon hältst, ob du Sachen vergessen hast oder ob dort Sachen falsch sind, sodass du quasi noch meinen Check hast, ob alles im Video vorhanden ist.“

## Das Bild des Nutzers: erst nach der Recherche öffnen
- Die Datei liegt unter `themen/l-theanin/vorlage/infografik_nutzer_ERST_NACH_RECHERCHE.jpg`. Daneben steht eine `LIESMICH.md`.
- **Öffne das Bild nicht**, bevor `faktencheck.md` fertig ist und der Drehbuch-Entwurf steht. Auch Subagenten bekommen es vorher nicht. Die Recherche soll unabhängig vom Bild entstehen. Dieser Auftrag enthält deshalb bewusst keine Aussagen aus dem Bild.
- **Danach der Abgleich**, vor dem Ton:
  1. Jede Aussage des Bildes auflisten, auch Zahlen und Tabellen.
  2. Je Aussage: Was sagt unsere Recherche dazu? Urteil in Worten (stimmt, stimmt teilweise, nicht belegt, falsch) mit Quelle.
  3. Steht die Aussage im Drehbuch? Fehlt etwas gut Belegtes, ins Drehbuch aufnehmen. Fehlt etwas im Bild, das wir haben, ebenfalls notieren.
  4. Ergebnis als `themen/l-theanin/abgleich_infografik.md` ablegen. Im Abschlussbericht dem Nutzer kurz zeigen: was im Bild falsch oder überzogen ist, was wir daraus übernommen haben, was wir bewusst weglassen und warum.
- Für Aussagen, die erst durch das Bild auftauchen, gilt dieselbe Regel wie immer: erst prüfen, dann ins Video.

## Vorbild und Format
- **Vorbilder:** `themen/dmso/` (neuestes, vom Nutzer am 11.11. abgenommen) und `themen/pea/`. Lies zuerst `themen/dmso/AUFTRAG.md` samt Nachtrag und `themen/dmso/LIESMICH.md` und übernimm den Ablauf.
- **Format:** Erklärvideo ohne Ampel, Kicker „Erklärvideo“, Hook nennt zuerst das Thema, Kachel-Einstieg, etwa 6 Minuten, höchstens etwa 7. Abschlusssatz und Tempo 1,05 wie in der `CLAUDE.md`.
- **Stil:** nur G, Aquarell und Tusche, Stil-Text wie in `themen/dmso/bilder_bau.py`.
- **Bilder:** eigene Szenenbilder im Format 5:4, Bildwechsel alle 6–12 Sekunden, 16:9-Kachelbilder für den Einstieg.
- **Bildregeln des Nutzers:**
  - Gesichter immer mit Augen, Nase und Mund. Profil oder Rückenansicht ist in Ordnung.
  - Keine englischen Notizen oder Schilder, keine anzüglichen Posen.
  - Beschriftungen nur kurz und auf Deutsch.
  - Keine Dosen oder Flaschen mit Dosierangaben, keine Markennamen.
  - Jedes Bild ansehen.

## Inhalt: gleicher Aufbau wie bei DMSO
Finde die Inhalte selbst. Die Stichworte unten sind nur ein Rahmen und ein paar Kandidaten zur Geschichte, keine Fakten. Jeden Punkt mit Primärquelle, DOI oder Behördentext prüfen.
- **Entdeckung und Entwicklung:**
  - Wer hat L-Theanin wann und worin entdeckt? Kandidat: Japan, um 1949/1950, in grünem Tee.
  - Was ist es chemisch, und wo kommt es sonst vor?
  - Wie viel steckt in einer Tasse Tee, und was verändert den Gehalt (Sorte, Beschattung)? Geschmack.
  - Wie wird es heute hergestellt? Seit wann wird es als Zusatz und als Präparat verkauft?
- **Wie es wirken soll:** Aufnahme, Weg ins Gehirn, vorgeschlagene Mechanismen. Trenne Tierdaten von Befunden am Menschen.
- **Wofür es eingesetzt und untersucht wird:** breite, positive Übersicht, damit man sich informieren kann. Sammle selbst, wofür es beworben wird. Jede Anwendung bekommt eine Einordnung in Worten, etwa „gut untersucht“, „in kleinen Studien untersucht“, „Erfahrungsberichte, kaum Studien“, „behauptet, nicht belegt“. Studiengröße, Dauer und Herstellerfinanzierung offen nennen. Viele Studien nutzen ein Markenprodukt; prüfe, wer bezahlt hat. Auch Kombinationen prüfen, die in Studien vorkommen.
- **Rechtsstatus und Sicherheit:** EU und Deutschland (EFSA, BfR, Verbraucherzentrale), USA, Japan. Was bedeuten die jeweiligen Einstufungen genau, und was nicht?
- **Selbstanwendung, was kritisch ist:** Nebenwirkungen, Wechselwirkungen mit Medikamenten, Schwangerschaft und Stillzeit, Kinder, Qualität der Präparate. Handlungstipp „Sprich mit Arzt oder Ärztin, bevor du …“.

## Grenzen
- **Keine Heilversprechen.** Positiv und neugierig erzählen, aber sagen, wo Belege dünn sind oder fehlen.
- **Dosierungen:** nur nennen, was Studien verwendet haben, als Beschreibung der Studie, nicht als Empfehlung. Keine Einnahme-Anleitung, kein „optimaler Zeitpunkt“ ohne Beleg.
- **Herkunft der Behauptungen** nicht nennen (Regel der `CLAUDE.md`).

## Ablauf (wie bei DMSO)
1. **Recherche** mit Subagent und Websuche, DOIs per Crossref prüfen. Ergebnis als `themen/l-theanin/faktencheck.md` mit Quellenverzeichnis und einer Tabelle „Anwendungen mit Einordnung“.
2. **Drehbuch-Entwurf:** `drehbuch_bau.py` erzeugt `szenen_G.json`.
3. **Abgleich mit dem Bild des Nutzers** (siehe oben), Drehbuch nachziehen.
4. **Aussprache:** Proben für „L-Theanin“ und weitere Fachwörter auf einer Auswahl-Seite. Bis zur Wahl eine sinnvolle Aussprache nehmen und unter „zur Info“ nennen.
5. **Ton** einmal erzeugen (ElevenLabs, Christian), dann `betonung.py`.
6. **Bilder:** Vorher die Kosten schätzen und nennen. DMSO brauchte 53 Bilder für rund 1.200 Credits. Fehler je Bild abfangen und protokollieren.
7. **Rendern** ohne weitere Rückfrage.
8. **Vorschau-Seite:** Video 720p, 12 fps, höchstens 16 MB, Ton AAC 128k aus der WAV, „passt“ und „ändern“, Hörprobe mit Abnahmekasten, YouTube-Beschreibung mit nummerierten Quellen und Hashtags, Vorschaubild.
9. **Abgabe:**
   - Antwort nach dem Aufbau der `CLAUDE.md`: oben kurz, am Ende „Deine Aufgabe“, die Links und die Kostenzeile.
   - Den Abgleich mit dem Bild kurz zeigen.
   - Push-Nachricht aufs Handy.
   - Danach eine Nachricht an die Hauptsitzung (`send_message` an `@parent`) mit den Links, der Länge, den Kosten (ElevenLabs-Zeichen, Bild-Credits) und zwei bis drei Sätzen zum Abgleich. Der Nutzer will die Ergebnisse auch dort finden.
10. **Ordner:** Nur in `themen/l-theanin/` arbeiten. Vor jedem Push `git pull --rebase origin main`.

## Zum Nutzer
- Trader, Statistiker, Finanzmathematiker. Er diktiert per Sprache, Erkennungsfehler mitdenken.
- Deutsch und Du, kritisch, Aussagen markieren mit [Sicher]/[Wahrscheinlich]/[Vermutung].
- Kurze Antworten, lieber Bilder als Text.
