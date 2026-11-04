# Rechentricks – Sammlung

Themenvorrat für eine Mathe-Videoreihe: 302 Tricks in 18 Kategorien, 127 Folgen in 14 Staffeln, 331 Quellen in 10 Sprachen.

- `tricks.py`, `tricks2.py`, `tricks3.py` – Inhalt (Runde 1–3; Top 15, Kategorien)
- `folgen.py` – Folgenplan: jede Folge = Haupttrick + verwandte Tricks, jeder Trick genau einmal
- `pruefung.py` – Rechenproben: exakte Regeln über ganze Bereiche durchgerechnet, Faustregeln mit gemessenem Fehler,
  alle Zahlenbeispiele nachgerechnet → `pruefung.json`
- `quellen.txt` – Quellen (`IDs | Sprache | Titel | URL`), alle bei der Recherche am 04.11.2026 abgerufen;
  `linktest.json` = HTTP-Code des späteren automatischen Linktests
- `bauen.py` + `stil.css` + `pdf_rendern.cjs` – erzeugt `rechentricks.html` und `rechentricks.pdf`

Neu bauen:

    python3 pruefung.py && NODE_PATH=$(npm root -g) python3 bauen.py --bilder /tmp/seiten
