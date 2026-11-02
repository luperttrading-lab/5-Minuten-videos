# Auftrag: Strategie der Videoreihe und Wahl der Sprecherstimme (eigene Sitzung)

Erteilt am 02.11.2026 aus der Guanfacin-Sitzung im Auftrag des Nutzers. Die Guanfacin-Sitzung macht nur noch das
Guanfacin-Video fertig; Strategie und Stimme laufen hier. Zuerst `CLAUDE.md` lesen.

## Teil 1: Strategiepapier als PDF

**Wunsch des Nutzers (sinngemäß, 02.11.):** Du bist seine Beratungsagentur. Prüfe, ob die Struktur der 5–6-Minuten-
Videos geändert werden sollte, damit sie wissenschaftlich exakt bleiben, aber auch innovative Ansätze bringen, die im
Gespräch und nicht widerlegt sind, statt konservativer, altmodischer Informationen (außer sie sind bewährt und Stand der
Wissenschaft). Gefährliche Aussagen weiter klar benennen. Kreative, informative Videos ohne Unsinn. Außerdem: Braucht es
einen Disclaimer, und wo wird er eingeblendet? Ein Abschlusssatz wie in der Fernsehwerbung („Fragen Sie Ihren Arzt oder
Apotheker“)? Ziel: die interessantesten Videos in diesem Bereich auf YouTube. Ergebnis strukturiert als **PDF** (liest er
besser als Chat-Text). Er möchte vorab sehen, wie du vorgehst.

**Was die Guanfacin-Sitzung dem Nutzer schon gesagt hat (Gegenposition, im Papier begründen oder korrigieren):**
- „Im Gespräch und nicht widerlegt“ taugt nicht als Maßstab: Das meiste Gehypte ist nicht widerlegt, weil es niemand
  geprüft hat. Innovation soll aus **neuer Evidenz** kommen (neue Leitlinien, große Meta-Analysen, Studien, die Fachleute
  gerade einordnen) und aus einer ehrlichen vierten Stufe „vielversprechend, aber jung“, nicht aus neuen Behauptungen.
- „Fragen Sie Ihren Arzt oder Apotheker“ ist der Pflichttext des Heilmittelwerbegesetzes für Arzneimittelwerbung;
  wörtlich übernommen klingt das Video wie Werbung. Eigener Satz nötig, Vorschläge ins Papier.

**Bestandsaufnahme der fünf Videos** (Stress, Magnesium, Magnesium 2, Tomatenmark, Guanfacin; Drehbücher unter
`themen/*/szenen.json`):
- Alle gleich gebaut: Einstieg mit sechs Kacheln, sechs Szenen, Fazit „Was bleibt also?“ mit drei Punkten, Schluss „Die
  Quellen stehen in der Beschreibung.“ Länge 5:10–6:04.
- Kein Hook: Alle beginnen mit einer Feststellung; die erste spannende Frage kommt frühestens nach etwa 10 s.
- Gesprochener Hinweis „ersetzt keinen ärztlichen Rat“ nur bei Guanfacin; sonst nur Fußzeile und Beschreibung.
- Tomatenmark: 13 von 20 Markern gelb (wenig Kontrast für Zuschauer).
- Jedes Video verteidigt den Status quo gegen Hype; keins bringt eine Erkenntnis, die neuer ist als die geprüften Behauptungen.
- Neue Nutzerregeln vom 02.11. (stehen im `CLAUDE.md`): Legende nicht sprechen, nur einblenden; „Arzt oder Ärztin“,
  nicht gendern. Beeinflusste Studien (Herstellergeld) weiter nennen; persönliche Seitenhiebe wie die Lizenzgebühren
  einzelner Forscher hat er aus Guanfacin streichen lassen.

**Recherche liegt vor** (zwei Agenten mit Websuche, 02.11.):
- `recherche_B.md`: Evidenzkommunikation (GRADE, Harding-Zentrum, Medizin-transparent, HealthNewsReview, Medien-Doktor),
  Vorschlag vierte Markerstufe „Frühe Hinweise“, Themenradar-Quellen, 12 Themenkandidaten mit Eignung, meistgesehene
  deutsche Gesundheitsvideos. Top-Themen laut Agent: Mikroplastik im Gehirn (Nature Medicine 2025 vs. Matters Arising),
  Kreatin fürs Gehirn, Vitamin D (Telomere vs. Megadosen), Kollagen/Mg-Threonat (Herstellerstudien), zeitlich begrenztes Essen.
- `recherche_A.md`: YouTube-Richtlinien und Health-Features, KI-Kennzeichnung, beste evidenzbasierte Kanäle (Disclaimer,
  Hooks, Abschlussformeln), Zuschauerbindung, Recht in Deutschland (HWG, MStV § 19, Impressum, Haftung), Hinweistexte von
  Quarks/IQWiG. Vollständig seit Commit 4252a9b (76 Quellen). Ungeprüft und vor dem Zitieren
  zu verifizieren: die Urteile „BGH 26.03.2026, I ZR 74/25“ und „OLG Köln 11.09.2025“ sowie Kang 2026 und Wegmann 2026.
- Alle Zahlen und Zitate in den Recherchen vor dem Übernehmen stichprobenartig gegenprüfen (Agenten können sich irren),
  insbesondere Rechtliches.

**Geplanter Inhalt des PDFs (etwa 10–12 Seiten):** Kurzfassung mit den 5 wichtigsten Empfehlungen; Bestandsaufnahme;
Strukturvorlage v2 Sekunde für Sekunde (Hook, Kacheln, Szenen, Fazit, Schluss); Evidenzstufen inkl. vierter Stufe und
Darstellungsregeln (absolute Zahlen, „N von 100“, Evidenz im Verb); Disclaimer-Konzept (wo, wie lang, Wortlaut, rechtlicher
Rahmen); drei Varianten Abschlusssatz; Themen-Scorecard und Themenradar; konkrete Änderungen am Guanfacin-Video (nur als
Empfehlung, die Guanfacin-Sitzung setzt um); Fahrplan nächste Videos. Jede Aussage [Sicher]/[Wahrscheinlich]/[Vermutung].
PDF bauen mit `node pdf_bau.js eingabe.html ausgabe.pdf` (Playwright, A4). PDF dem Nutzer mit SendUserFile schicken,
Push-Nachricht, dann Rückfragen klären. Nicht einchecken, falls groß; HTML-Quelle einchecken.

## Teil 2: Sprecherstimme der Reihe

Der Nutzer will vor vielen weiteren Videos prüfen, ob eine andere Stimme besser passt. Seneca (Hörbuch) nutzt Helmut
Stieglbauer; die Reihe soll eine andere Stimme haben. Aktuell: Christian – Warm and Captivating (`NBqeXKdZHweef6y0B67V`).

- Stimmentest des Seneca-Projekts: Repo `luperttrading-lab/seneca-audio` (öffentlich, klonen), `PROTOKOLL.md` ab
  „Stimmensuche vom 28.10. abends“, Rohdaten `messung/stimmen/`. Ergebnis: Runde 1 (25 Stimmen, Bradley-Terry) Alexander
  81 %, Leo Liest 81 %, Robert 78 %, Gottfried 73 %, Marcus 69 %, Marko 68 %, Helmut 67 %, Christian 59 % (Platz 9);
  Runde 2b: Helmut 72, Alexander 71, Marko 69, Marcus 56, Gottfried 47, Leo 42, Robert 35. In Runde 1 erklärte die
  Tonlage die Wahl (tiefer gewinnt), in Runde 2b nicht.
- **Sprecherprobe ist veröffentlicht:** https://claude.ai/artifact/JN35D98fWimt5w5hSaZiWq — Christian, Alexander, Marko,
  Marcus, Leo Liest mit demselben Absatz (Guanfacin Szene 3, 81 Wörter), gleiche Lautstärke, Blindmodus, Urteil je Stimme
  (Sammlung `stimmwahl`, Feld `urteil` = gut | mittel | nein) und Notiz (Sammlung `stimmnotizen`, geht auch als Kommentar
  an Claude). Quelle `themen/stil/stimmprobe/` (`stimmprobe.py`, `seite/`). Diese Sitzung beobachten:
  `ArtifactComments` mit `action: "watch"` und der URL, dann Urteile mit `ArtifactData list` lesen.
- Zu bedenken: Im Seneca-Duell ging es um ein Hörbuch (ruhig, tief); ein YouTube-Gesundheitsvideo braucht Klarheit bei
  Zahlen und Fachwörtern und Zug. Tempo der Kandidaten: Christian 2,16 W/s, Alexander 2,27, Marko 2,28, Marcus 2,33,
  Leo 2,15. Bei Wechsel: Guanfacin-Ton neu (≈ 2.300 Zeichen), alte Videos nur auf Wunsch.
- Wählt der Nutzer eine Stimme: `CLAUDE.md` (Abschnitt Stimme) anpassen und der Guanfacin-Sitzung Bescheid geben
  (send_message an die Sitzung, aus der dieser Auftrag kam), damit sie vor dem Rendern neu einspricht.

## Zusammenarbeit
- Direkt mit dem Nutzer: Deutsch, Du, kritisch, kurze Antworten, Bilder statt Text, Kostenzeile mit `tools/kosten.py`,
  Push-Nachricht aufs Handy, wenn etwas fertig ist oder er entscheiden soll.
- Arbeiten in `themen/beratung/` und `themen/stil/stimmprobe/`; `CLAUDE.md` nur für beschlossene Regeln.
  Vor jedem Push `git pull --rebase origin main`: Andere Sitzungen arbeiten parallel im selben Repo.
