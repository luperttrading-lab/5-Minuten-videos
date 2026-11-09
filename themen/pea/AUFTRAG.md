# Auftrag: Erklärvideo „PEA – Entdeckung und Entwicklung“ in drei Bildstilen

Erteilt am 09.11.2026 aus der Sitzung „Fünf-Minuten-Infovideo“ im Auftrag des Nutzers.

**Wortlaut des Nutzers (diktiert):** „Kannst du ein Video zu PEA machen, über die Entdeckung und die Entwicklung. Interessant wäre 3D, Aquarell und Knetfiguren.“

Auf Rückfrage geklärt:
- **Thema:** PEA = Palmitoylethanolamid.
- **Format:** Erklärvideo wie das Vitamin-D-Schulprojekt, nicht der Faktencheck mit Ampel.

## Format
- Vorlage: `themen/schulprojekt-vitamin-d/erklaervideo/` (`drehbuch_bau.py`, `bilder_bau.py`, `bilder_v2.py`, `LIESMICH.md`).
- Erklärvideo ohne Ampel, Kachel-Einstieg mit Kicker „Erklärvideo“, ein gemeinsamer Ton für alle Stile, nur die Bilder wechseln.
- Länge etwa 5–6 Minuten, rund 720–780 Wörter bei Tempo 1,05. Der Hook nennt zuerst das Thema.
- Abschlusssatz aus der `CLAUDE.md`.
- Stile: I (3D-Trickfilm), G (Aquarell und Tusche), D (Knetfiguren); Stil-Texte in `erklaervideo/bilder_bau.py`.
- Szenenbilder 5:4 (1280×1024) wie in `bilder_v2.py`, Bildwechsel alle 6–12 s; dazu 16:9-Kachelbilder.
- Bildregeln: Knete mit glatter Haut, keine Hautnahaufnahmen, lieber ganze Figuren; sichtbare Gesichter immer mit Augen, Nase, Mund (Profil/Rücken ok); keine englischen Notizen/Schilder, keine anzüglichen Posen; Beschriftungen kurz und deutsch; jedes Bild vor dem Rendern ansehen.

## Inhalt (Kandidaten, jeden mit Primärquelle/DOI prüfen)
- Ursprung: Eigelb-Faktor gegen rheumatisches Fieber (1940er, Coburn); Isolierung aus Eigelb, Erdnussöl, Sojalecithin (1957, Kuehl et al.).
- 1970er: Präparat in der Tschechoslowakei gegen Grippe/Atemwegsinfekte (u. a. Masek), warum es verschwand.
- 1990er: Levi-Montalcini, ALIA (Mastzellen); später PPAR-alpha (Lo Verme 2005), Verwandtschaft mit Anandamid/Endocannabinoid-System.
- Heute: mikronisiert/ultramikronisiert; Rechtsstatus DE/IT; wofür beworben.
- Studienlage: Schmerz-Meta-Analysen, Größe/Qualität, Herstellerfinanzierung (Epitech) offen nennen, Sicherheit, Offenes.
- Ton: neugierig, Entdeckungsgeschichte, nichts verschweigen, keine Heilversprechen, keine Herkunft populärer Behauptungen, keine Dosierungsanleitung über Studien hinaus, Tipps „Sprich mit Arzt oder Ärztin über …“.

## Ablauf
1. Recherche (Subagent, Websuche, DOIs prüfen) → `faktencheck.md` mit Quellenverzeichnis.
2. `drehbuch_bau.py` → `szenen_I.json`, `szenen_G.json`, `szenen_D.json`.
3. Ton einmal (ElevenLabs, Christian), `betonung.py`; Aussprache-Proben für Fachwörter, bis zur Wahl sinnvolle Aussprache, „zur Info“ nennen.
4. Bilder: Kosten vorher schätzen (≈ 3 × 40 × 10–20 Credits), Kontostand beobachten, Fehler je Bild protokollieren.
5. Rendern ohne Rückfrage, alle drei Stile.
6. Vorschau-Seite: je Stil ein Video ≤ 16 MB, 720p, 12 fps, AAC 128k aus der WAV; „passt“/„ändern“; Hörprobe mit Abnahmekasten; YouTube-Beschreibung mit nummerierten Quellen.
7. Abgabe nach Antwortaufbau der `CLAUDE.md`, Push-Nachricht, ElevenLabs-Zeichen und Bild-Credits nennen.
8. Nur in `themen/pea/` arbeiten; vor jedem Push `git pull --rebase origin main`.
