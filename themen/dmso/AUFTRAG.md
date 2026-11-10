# Auftrag: Erklärvideo „DMSO“ im Aquarell-Stil (Schulprojekt-Format)

Erteilt am 10.11.2026 aus der Sitzung „Fünf-Minuten-Infovideo“ im Auftrag des Nutzers.

**Wortlaut des Nutzers (diktiert):** „Kannst du eine Sitzung starten für ein Schulprojekt-Video über DMSO, genauso wie du es mit PEA gemacht hast, und zwar im Aquarell-Stil.“

Gemeint ist DMSO = Dimethylsulfoxid.

## Vorbild und Format
- **Neuestes Vorbild:** `themen/pea/` (`AUFTRAG.md`, `drehbuch_bau.py`, `bilder_bau.py`, `faktencheck.md`, Aussprache-Proben, Hörprobe mit Abnahme, `thumbnail_bau.py`, YouTube-Beschreibung mit Hashtags).
- **Format:** Erklärvideo ohne Ampel, Kicker „Erklärvideo“, Hook nennt zuerst das Thema, Kachel-Einstieg, etwa 5–6 Minuten. Abschlusssatz und Tempo 1,05 wie in der `CLAUDE.md`.
- **Stil:** nur G, Aquarell und Tusche, Stil-Text aus `themen/pea/bilder_bau.py` bzw. `schulprojekt-vitamin-d/erklaervideo/bilder_bau.py`.
- **Bilder:** eigene Szenenbilder im Format 5:4, Bildwechsel alle 6–12 Sekunden, 16:9-Kachelbilder für den Einstieg.
- **Bildregeln des Nutzers:** Gesichter immer mit Augen, Nase und Mund (Profil oder Rückenansicht in Ordnung); keine englischen Notizen oder Schilder, keine anzüglichen Posen; Beschriftungen nur kurz und auf Deutsch; jedes Bild ansehen.
- **Zusätzlich für DMSO:** keine Bilder von Menschen, die DMSO trinken, sich selbst einreiben oder spritzen. Keine Flaschen mit Dosierangaben.

## Inhalt: Entdeckung, Entwicklung, Anwendungen
Kandidaten, keine Fakten. Jeden mit Primärquelle, DOI oder Behördentext prüfen.
- **Entdeckung:** erste Herstellung 1866 durch Alexander Saytzeff. Nebenprodukt der Papier- und Zellstoffindustrie (Lignin), Lösungsmittel in Chemie und Industrie.
- **1960er:** Stanley Jacob und Robert Herschler (Oregon, Crown Zellerbach), der Hype um DMSO als Wundermittel. Stopp der klinischen Studien durch die FDA 1965 nach Linsenveränderungen bei Tieren und die spätere Neubewertung.
- **Zugelassene Anwendungen:** Blasenspülung bei interstitieller Zystitis (Rimso-50, FDA 1978); topische Präparate in Deutschland (welche, welche Wirkstoffe, z. B. ob Dolobene DMSO enthält); Kälteschutzmittel beim Einfrieren von Stammzellen, Blutstammzellen und Embryonen.
- **Eigenschaften:** dringt sehr gut durch die Haut und nimmt andere Stoffe mit (Vorsicht bei Verunreinigungen und gelösten Stoffen); knoblauchartiger Geruch über den Atem.
- **Studienlage:** wofür es Belege gibt (z. B. topisch bei Schmerzen und Entzündung, Komplexes Regionales Schmerzsyndrom) und wofür nicht. Größe und Qualität der Studien nennen.

## Grenzen
Das Schulprojekt-Format soll neugierig und positiv erzählen. Bei DMSO gibt es aber eine große Szene mit Selbstbehandlung, deshalb:
- **Keine Anleitung zur Selbstanwendung:** kein Trinken, keine Einnahme, keine Mischungen, keine Dosierungen, keine Konzentrationen für die Haut.
- **Keine Heilversprechen:** kein „gegen Krebs“, kein „Wundermittel“.
- **Keine Kombination mit Chlordioxid (MMS)** erwähnen, außer als klare Warnung, falls überhaupt nötig.
- **Risiken ehrlich nennen:** Hautreizung, Geruch, Mitnahme anderer Stoffe durch die Haut, Wechselwirkungen, Qualität von Industrie-DMSO. Handlungstipps: „Sprich mit Arzt oder Ärztin, bevor du …“.
- **Positiv sein dürfen:** Entdeckungsgeschichte, Chemie, Kälteschutz in der Medizin, zugelassene Anwendungen.
- **Herkunft der Behauptungen** nicht nennen (Regel der `CLAUDE.md`).

## Ablauf (wie bei PEA)
1. Recherche mit Subagent und Websuche, DOIs prüfen → `faktencheck.md` mit Quellenverzeichnis.
2. `drehbuch_bau.py` → `szenen_G.json`. Fachwörter („Dimethylsulfoxid“) als Aussprache-Probe; bis zur Wahl sinnvolle Aussprache, unter „zur Info“ nennen.
3. Ton einmal (ElevenLabs, Christian), dann `betonung.py`.
4. Bilder: Kosten vorher schätzen (≈ 40 × 10–20 Credits ≈ 400–800), Fehler je Bild abfangen und protokollieren.
5. Rendern ohne weitere Rückfrage.
6. Vorschau-Seite: 720p, 12 fps, ≤ 16 MB, AAC 128k aus der WAV, „passt“/„ändern“, Hörprobe mit Abnahmekasten, YouTube-Beschreibung mit nummerierten Quellen und Vorschaubild.
7. Abgabe nach Antwortaufbau der `CLAUDE.md`, Push-Nachricht, ElevenLabs-Zeichen und Bild-Credits nennen.
8. Nur in `themen/dmso/` arbeiten. Vor jedem Push `git pull --rebase origin main`.
