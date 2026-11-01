"""Behauptungsmatrix: welche Aussage in welchem YouTube-Video, dazu Vorlage und Urteil aus faktencheck.md."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SP = [("Marks", "984 T"), ("Byrne", "90 T"), ("Wood", "52 T"), ("Rege", "38 T"),
      ("Pagnani", "36 T"), ("Jan (DE)", "33 T"), ("Anx. Res.", "23 T"), ("John", "19 T")]
# Zeichen je Video: "x" behauptet, "e" behauptet mit Einschränkung, "d" widerspricht, "." nicht erwähnt
# U = Urteil (stark/mittel/keine/offen), kommt aus urteile.json (Zeilennummer -> Urteil)
ZEILEN = [
    ("Kein Stimulans, kein Suchtpotenzial",            "x x . x x x x .", 0, "offen"),
    ("Nur für Kinder und Jugendliche zugelassen",      "x x . x x x . .", 0, "offen"),
    ("Stärkt das Stirnhirn (präfrontaler Kortex)",     ". e x x . . x x", 0, "offen"),
    ("Hilft, wenn andere ADHS-Mittel versagen",        "x x . x . x x .", 0, "offen"),
    ("Verstärkt Stimulanzien als Zusatz",              "x x . . . . . x", 0, "offen"),
    ("Gute Option für Erwachsene (off-label)",         ". x . . x . . x", 0, "offen"),
    ("Wirkt schon nach wenigen Tagen",                 ". x d . . d x .", 0, "offen"),
    ("Muss nicht täglich genommen werden",             ". x . . . . . .", 0, "offen"),
    ("Macht müde – besser abends nehmen",              ". x e . e . . .", 0, "offen"),
    ("Senkt Blutdruck und Puls, Schwindel",            ". x x d x . x .", 0, "offen"),
    ("Nie abrupt absetzen: Blutdruck steigt",          ". . x . x . . .", 0, "offen"),
    ("Hilft bei Angst",                                ". x x . . . x .", 0, "offen"),
    ("Hilft bei Tics",                                 ". . x x . . . .", 0, "offen"),
    ("Hilft bei PTBS, Schlafproblemen, Wut",           ". . x x . . e .", 0, "offen"),
    ("Löst Aufschieben, macht redefreudiger",          ". . . . . . . x", 0, "offen"),
]
FARBE = {"nu": "#b5382e", "stark": "#2e7d4f", "mittel": "#c9971c", "keine": "#b5382e", "offen": "#888888"}
TEXT = {"nu": "nicht untersucht", "stark": "belegt", "mittel": "teilweise", "keine": "nicht haltbar", "offen": "?"}


def zeichne(urteile, ziel):
    zeilen = [(t, z, v, urteile.get(i, u)) for i, (t, z, v, u) in enumerate(ZEILEN)]
    h = 0.44 * len(zeilen) + 3.4
    fig = plt.figure(figsize=(16.4, h), dpi=100)
    fig.patch.set_facecolor("#f8f4ec")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 16.4); ax.set_ylim(h, 0); ax.axis("off")
    ax.text(0.2, 0.5, "Guanfacin auf YouTube: Was behauptet wird – und was davon hält",
            fontsize=19, weight="bold", color="#1f2a3a", va="center")
    x0, dx = 6.4, 0.98
    for j, (n, a) in enumerate(SP):
        ax.text(x0 + j * dx, 1.25, f"{n}\n{a}", ha="center", va="center", fontsize=10, color="#1f2a3a")
    xu = x0 + len(SP) * dx + 0.75
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
        ax.text(xu, y, TEXT[u], ha="center", va="center", fontsize=12, weight="bold", color=FARBE[u])
    yb = 1.95 + len(zeilen) * 0.44 + 0.25
    ax.text(0.2, yb, "● = behauptet   ○ = nur teilweise oder unsicher behauptet   "
            "dagegen = sagt das Gegenteil.   T = Tausend Aufrufe. Alle englisch außer Jan.", fontsize=11.5, va="top")
    ax.text(0.2, yb + 0.45, "Geschäftsinteressen laut Beschreibung: Byrne (eigene ADHS-Diagnostik „in 48 Stunden“, Beratungstermine), "
            "Marks (Quiz-Trichter), Jan (Videokurse), Rege (Fortbildungs-Akademie),\nWood, Pagnani (eigene Praxen). "
            "Niemand verkauft Guanfacin oder Online-Rezepte. Auf Deutsch gibt es fast keine Videos zu Guanfacin; „Nootropikum“ fand sich in keinem populären Video.",
            fontsize=10, color="#7a3b22", va="top")
    fig.savefig(ziel, facecolor=fig.get_facecolor())


if __name__ == "__main__":
    import json, sys
    import os
    roh = json.load(open("urteile.json")) if os.path.exists("urteile.json") else {}  # Zeilennummer -> Urteil
    urteile = {int(k): v for k, v in roh.items()}
    zeichne(urteile, "behauptungen_youtube.png")
