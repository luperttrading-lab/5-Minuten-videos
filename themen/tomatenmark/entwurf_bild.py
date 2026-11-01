"""Szenenentwurf als Bild fürs Handy."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
S = [
 ("0", "Einstieg", "Tomatenmark gilt als Superfood. Sechs Kacheln, Ampel-Legende.", "–"),
 ("1", "Mark oder frische Tomate?", "◐ „20-mal mehr Lykopin“ (eher 11×)\n✓ Hitze und Öl helfen bei der Aufnahme\n◐ „über 80 % mehr mit Olivenöl“ (11 Personen)", "Mark kurz mit etwas Öl anbraten"),
 ("2", "Hilft es dem Gehirn?", "◐ 35 g täglich: bessere Konzentration (42 Pers., Effekt klein)\n◐ steigert BDNF (nur grenzwertig)\n◐ schützt vor Demenz (nur Beobachtung)", "Teil guter Ernährung, kein Ersatz\nfür Bewegung und Schlaf"),
 ("3", "Herz und Schlaganfall", "◐ „55 % weniger Schlaganfälle“ (Gen-Analyse: keine Ursache)\n◐ senkt LDL um 10 % (erst bei 5–6 EL am Tag)\n◐ Blutdruck leicht", "Mittelmeerküche, Medikamente\nnicht ersetzen"),
 ("4", "Kapsel oder Löffel?", "✕ „Synthetisches Lykopin wirkungslos“\n(wird gleich gut aufgenommen; Gegenbeleg vom Hersteller)", "Löffel statt Kapsel: billiger"),
 ("5", "Weitere Versprechen", "◐ Prostatakrebs  ◐ Sonnenschutz\n◐ Knochen nach den Wechseljahren\n✕ mehr Bifidobakterien im Darm", "Sonnencreme und Vorsorge bleiben"),
 ("6", "Beim Kauf", "✓ Schimmelpilzgifte in jedem zweiten Produkt\n✕ „Bio schützt davor“\n◐ viel Histamin", "Marken wechseln, Zutaten:\nnur Tomaten, höchstens Salz"),
 ("7", "Fazit", "Gekocht mit Öl ✓ · Wunderwirkungen ◐ · Kapsel ✕", "In die Soße, mit Öl, Marke wechseln"),
]
fig = plt.figure(figsize=(16, 14.2), dpi=100); fig.patch.set_facecolor("#f8f4ec")
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 16); ax.set_ylim(14.2, 0); ax.axis("off")
ax.text(0.3, 0.55, "Tomatenmark – Szenenentwurf (≈ 6 Minuten)", fontsize=24, weight="bold", color="#1f2a3a")
ax.text(0.3, 1.15, "✓ belegt    ◐ teilweise    ✕ nicht haltbar", fontsize=15, color="#555")
for x, t in [(0.3, "#"), (0.9, "Szene"), (5.0, "Was geprüft wird"), (11.6, "Tipp am Ende")]:
    ax.text(x, 1.85, t, fontsize=15, weight="bold", color="#46597f")
y = 2.2
for i, (n, ti, w, tip) in enumerate(S):
    h = 0.45 + 0.42 * max(w.count("\n"), tip.count("\n")) + 0.35
    if i % 2 == 0: ax.add_patch(plt.Rectangle((0.15, y), 15.7, h, color="#f0e7d8"))
    for x, t, kw in [(0.3, n, dict(weight="bold")), (0.9, ti, dict(weight="bold")), (5.0, w, {}), (11.6, tip, {})]:
        ax.text(x, y + 0.2, t, fontsize=14.5, va="top", color="#1f2a3a", linespacing=1.45, **kw)
    y += h
ax.text(0.3, y + 0.4, "Weggelassen: Abnehmen (nur ein Video, mit Affiliate-Code), Spermien (Herstellerstudie), Markenwarnungen ohne Quelle.",
        fontsize=13, color="#7a3b22", va="top")
fig.savefig("entwurf.png", facecolor=fig.get_facecolor())
