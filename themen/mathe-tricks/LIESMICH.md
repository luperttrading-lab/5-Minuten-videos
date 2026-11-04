# Rechentricks – Sammlung

Themenvorrat für Mathe-Videos und Übungen: 134 Tricks in 13 Kategorien, 189 Quellen in 10 Sprachen.

- `tricks.py` – Inhalt (ein Eintrag je Trick, Top 15, Kategorien)
- `pruefung.py` – Rechenproben: exakte Regeln über ganze Bereiche durchgerechnet, Faustregeln mit gemessenem Fehler,
  alle Zahlenbeispiele nachgerechnet → `pruefung.json`
- `quellen.txt` – Quellen (`IDs | Sprache | Titel | URL`), alle bei der Recherche am 04.11.2026 abgerufen;
  `linktest.json` = HTTP-Code des späteren automatischen Linktests
- `bauen.py` + `stil.css` + `pdf_rendern.cjs` – erzeugt `rechentricks.html` und `rechentricks.pdf`

Neu bauen:

    python3 pruefung.py && NODE_PATH=$(npm root -g) python3 bauen.py --bilder /tmp/seiten
