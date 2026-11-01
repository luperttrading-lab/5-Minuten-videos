# Bildleitfaden

**Festgelegt am 31.10.2026:** Modell GPT Image 2, Stil wie `themen/magnesium2/bildbogen.png` (14 Bilder): Motiv mittig
auf warmem Papier, Tusche und Aquarell, warm und kräftig genug fürs Handy. Erklärbilder (Abläufe im Körper) im selben Stil
wie m3b, ohne Schrift; Zoom von Station zu Station. Nano-Banana-Fassung nur als Archiv (`themen/stil/nanobanana_magnesium2/`). Der Stiltext steht als `STIL` in `werkzeug/bilder.py` und wird nicht
für einzelne Bilder geändert. Stilvergleich A/B/C nur als Archiv.

## Menge und Takt
- Ziel: alle 10–12 s ein neues Bild oder ein neuer Ausschnitt, also ≈ 30 Einstellungen in 6 Minuten.
- Pro Szene 2 eigene Bilder: **Bild 1 = Situation/Behauptung**, **Bild 2 = Antwort/Tipp**. Jedes Bild trägt 1–2 Einstellungen
  (Gesamtbild, dann Zoom auf ein Detail). Für 7 Szenen ≈ 14 Bilder ≈ 100 Credits ≈ 7 ct.
- Kein Motiv mehr als zweimal im Video. Die Einstiegskacheln nutzen Ausschnitte der Szenenbilder.

## Stil
- Technik: Tusche und Aquarell auf warmem, leicht strukturiertem Papier.
- Palette: Taubenblau, Terrakotta, Ocker, Salbei; Papier warmes Off-White. Keine Neonfarben, kein Schwarz als Fläche.
- Licht: weich, warm, freundlich. Stimmung ruhig, nicht dramatisch.

## Komposition
- **Fürs Handy gebaut:** Hauptmotiv groß, füllt das Bild fast ganz aus, nur ein schmaler Papierrand (der Renderer stellt
  das Motiv ohnehin frei). Wenige, große Elemente; Beschriftungen groß genug, dass man sie auf dem Handy liest
  (Beispiel: `themen/magnesium2/bilder/m3b_Q7b.png`).
- Nichts Wichtiges am Bildrand. Hauptmotiv leicht links oder mittig.
- 2–3 erkennbare Details, auf die man zoomen kann (z. B. Kapseln, Kerne, Glas).
- Gut lesbar auch klein (Handy): klare Silhouetten, wenig Kleinkram.

## Menschen
- Erwachsene verschiedenen Alters und Aussehens, ruhige Haltung, einfache Gesichter.
- Keine Hände, die Tabletten halten, keine Finger in Nahaufnahme (häufige KI-Fehler).

## Verboten
- Schrift jeder Art: keine Buchstaben, Zahlen, Etiketten, Uhren mit Ziffern, Logos, Markenpackungen, Bildschirme mit Text.
- Fotorealismus, Comic-Übertreibung, Blut, Spritzen, Kliniksituationen.
- Inhaltlich Falsches: nur echte Lebensmittelquellen zeigen (z. B. keine Banane für Magnesium).

## Prompt-Vorlage
`Generate an image. {STIL} Absolutely no text, no letters, no numbers, no labels anywhere. Aspect ratio 16:9 landscape.
Composition: one clear main motif, 30-40 percent empty paper around it, nothing important near the edges. Motif: {MOTIV}`

## Prüfen vor dem Rendern
Schrift? Hände/Finger? Anzahl und Art der Objekte richtig? Passt es zur Aussage? Wiederholt es ein anderes Motiv?
