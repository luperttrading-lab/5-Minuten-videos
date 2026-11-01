"""Behauptungsmatrix: welche Aussage in welchem YouTube-Video, dazu Vorlage und Urteil aus faktencheck.md."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SP = [("Weigl", "711 T"), ("Timo G.", "245 T"), ("Selz", "83 T"), ("Selz", "34 T"),
      ("EssEnth.", "97 T"), ("Natur T.", "7 T"), ("Adler", "22 T")]
# Zeichen je Video: "x" behauptet, "e" behauptet mit Einschränkung, "d" widerspricht, "" nicht erwähnt
# Spalte V = in der Gemini-Vorlage; U = Urteil (stark/mittel/keine/offen)
ZEILEN = [
    ("Erhitzen + Öl macht Lykopin verfügbarer",      "x x x x . x .", 1, "offen"),
    ("Mark hat viel mehr Lykopin als Tomaten (20×)", "x . x x . x .", 1, "offen"),
    ("1 EL täglich wirkt messbar",                          "x x x x . x .", 0, "offen"),
    ("Kapseln/synthetisch wirken nicht",             "x . x x . . .", 1, "offen"),
    ("Besseres Gedächtnis (35 g, 40–55 J.)",         ". . e . . . .", 1, "offen"),
    ("Schützt vor Demenz, steigert BDNF",            ". x e e . . .", 1, "offen"),
    ("Weniger Schlaganfälle (−55 %)",                "x x e . . . .", 1, "offen"),
    ("Senkt LDL (≈ −10 %) und Blutdruck",            ". x x x . . .", 1, "offen"),
    ("Senkt Prostatakrebs-Risiko",                   ". x e x . . .", 1, "offen"),
    ("Senkt Krebsrisiko allgemein",                  "e x e e . x .", 0, "offen"),
    ("Schützt die Haut vor Sonne",                   ". x . x . . x", 0, "offen"),
    ("Schützt Leber (Fettleber)",                    ". . e . . . .", 1, "offen"),
    ("Mehr Bifidobakterien im Darm",                 ". . e e . . .", 1, "offen"),
    ("Schützt Knochen nach den Wechseljahren",       ". . x x . . .", 1, "offen"),
    ("Gesündere Spermien",                           ". x x . . . .", 0, "offen"),
    ("Hilft beim Abnehmen (Leptin)",                 ". x . . . . .", 0, "offen"),
    ("Viel Histamin, Zucker, Salz",                  "x . . x x x .", 0, "offen"),
    ("Schimmelpilzgifte in vielen Marken",           "x x . . x . .", 0, "offen"),
    ("Bio schützt vor Schimmelpilzgiften",           "x x . . x . .", 0, "offen"),
]
FARBE = {"stark": "#2e7d4f", "mittel": "#c9971c", "keine": "#b5382e", "offen": "#888888"}
TEXT = {"stark": "belegt", "mittel": "teilweise", "keine": "nicht haltbar", "offen": "?"}


def zeichne(urteile, ziel):
    zeilen = [(t, z, v, urteile.get(i, u)) for i, (t, z, v, u) in enumerate(ZEILEN)]
    h = 0.44 * len(zeilen) + 3.4
    fig = plt.figure(figsize=(16.4, h), dpi=100)
    fig.patch.set_facecolor("#f8f4ec")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 16.4); ax.set_ylim(h, 0); ax.axis("off")
    ax.text(0.2, 0.5, "Tomatenmark auf YouTube: Was behauptet wird – und was davon hält",
            fontsize=19, weight="bold", color="#1f2a3a", va="center")
    x0, dx = 6.6, 0.98
    for j, (n, a) in enumerate(SP):
        ax.text(x0 + j * dx, 1.25, f"{n}\n{a}", ha="center", va="center", fontsize=10, color="#1f2a3a")
    xv, xu = x0 + len(SP) * dx + 0.2, x0 + len(SP) * dx + 1.55
    ax.text(xv, 1.25, "Gemini-\nVorlage", ha="center", va="center", fontsize=10, weight="bold")
    ax.add_patch(plt.Rectangle((xu - 0.85, 0.85), 1.7, 0.44 * len(zeilen) + 0.85, color="#e8eef6"))
    ax.text(xu, 1.25, "Urteil", ha="center", va="center", fontsize=13, weight="bold", color="#1f2a3a")
    for i, (t, z, v, u) in enumerate(zeilen):
        y = 1.95 + i * 0.44
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((0.1, y - 0.22), xu - 0.95, 0.44, color="#f2ebdf"))
        ax.text(0.2, y, t, va="center", fontsize=12.5, color="#1f2a3a")
        for j, c in enumerate(z.split()):
            if c == "x":
                ax.plot(x0 + j * dx, y, "o", ms=13, color="#46597f")
            elif c == "e":
                ax.plot(x0 + j * dx, y, "o", ms=13, mfc="none", mec="#46597f", mew=2.2)
            elif c == "d":
                ax.text(x0 + j * dx, y, "dagegen", ha="center", va="center", fontsize=9, color="#b5382e")
        if v:
            ax.plot(xv, y, "s", ms=11, color="#c0543a")
        ax.text(xu, y, TEXT[u], ha="center", va="center", fontsize=12, weight="bold", color=FARBE[u])
    yb = 1.95 + len(zeilen) * 0.44 + 0.25
    ax.text(0.2, yb, "● = behauptet   ○ = behauptet, aber selbst eingeschränkt („nur Beobachtung“, „nicht bewiesen“)"
            "   ■ (rot) = steht in der Gemini-Grafik", fontsize=11.5, va="top")
    ax.text(0.2, yb + 0.45, "Geschäftsinteressen laut Beschreibung: Timo G. (Affiliate-Code für Olivenöl und Präparate), "
            "Selz (eigenes Buch, Kurs, pauschal „Affiliatelinks“),\nWeigl (eigene Ratgeber), Natur Total (eigener Shop). "
            "EssEnthüllt: Markenwarnungen ohne prüfbare Quellen, wirkt KI-generiert.",
            fontsize=10, color="#7a3b22", va="top")
    fig.savefig(ziel, facecolor=fig.get_facecolor())


if __name__ == "__main__":
    import json, sys
    import os
    roh = json.load(open("urteile.json")) if os.path.exists("urteile.json") else {}  # Zeilennummer -> Urteil
    urteile = {int(k): v for k, v in roh.items()}
    zeichne(urteile, "behauptungen_youtube.png")
