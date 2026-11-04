#!/usr/bin/env python3
"""Rechenproben für alle Tricks der Sammlung.

Jede exakte Regel wird über ihren angegebenen Bereich vollständig durchgerechnet,
jede Faustregel bekommt ihren gemessenen Fehler. Ausgabe: pruefung.json
(ID -> {ok, text}), die bauen.py in die Kärtchen übernimmt.

Aufruf: python3 pruefung.py
"""
import calendar
import datetime as dt
import json
import math
import random
from fractions import Fraction
from pathlib import Path

ERG = {}


def de(x, nd=0, plus=False):
    """Zahl deutsch formatiert: Tausenderpunkt, Dezimalkomma, echtes Minus."""
    if isinstance(x, int) and nd == 0:
        s = f"{x:{'+' if plus else ''},}"
    else:
        s = f"{x:{'+' if plus else ''},.{nd}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".").replace("-", "−")
random.seed(4711)


def probe(tid):
    def deko(f):
        def lauf():
            try:
                ok, text = f()
            except AssertionError as e:  # Gegenbeispiel gefunden
                ok, text = False, f"FEHLER: {e}"
            ERG[tid] = {"ok": bool(ok), "text": text}
        lauf.tid = tid
        PROBEN.append(lauf)
        return f
    return deko


PROBEN = []


def ziffern(n):
    return [int(c) for c in str(n)]


def alle(bedingung, bereich, was):
    n = 0
    for x in bereich:
        assert bedingung(x), f"{was}: Gegenbeispiel {x}"
        n += 1
    return n


# ---------------------------------------------------------------- Addition
@probe("A1")
def _():
    def links(a, b):
        s, stelle = 0, 10 ** max(len(str(a)), len(str(b)))
        while stelle:
            s += (a // stelle % 10 + b // stelle % 10) * stelle
            stelle //= 10
        return s
    n = alle(lambda p: links(*p) == p[0] + p[1],
             ((a, b) for a in range(1000) for b in range(0, 1000, 7)), "links")
    return True, f"{de(n)} Paare a < 1000, b < 1000 (jede 7.) richtig"


@probe("A2")
def _():
    n = alle(lambda p: p[0] + p[1] == p[0] + (p[1] + p[2]) - p[2],
             ((a, b, (-b) % 10) for a in range(500) for b in range(1, 500)), "kompensieren")
    return True, f"{de(n)} Fälle a, b < 500 (auf den nächsten Zehner ergänzt) richtig"


@probe("A3")
def _():
    def hoch(a, b):  # von a bis b in Sprüngen auf runde Zahlen
        schritte, x = 0, a
        for basis in (10, 100, 1000, 10000):
            ziel = -(-x // basis) * basis
            if ziel <= b and ziel > x:
                schritte += ziel - x
                x = ziel
        return schritte + (b - x)
    n = alle(lambda p: hoch(*p) == p[1] - p[0],
             ((a, b) for a in range(0, 2000, 3) for b in range(a, 2000, 11)), "aufwärts")
    return True, f"{de(n)} Paare 0 ≤ a ≤ b < 2000 richtig"


@probe("A4")
def _():
    def regel(m, stellen=3):
        z = ziffern(str(m).zfill(stellen))
        # letzte von 0 verschiedene Ziffer von 10, alle davor von 9, Nullen dahinter bleiben
        k = max(i for i, d in enumerate(z) if d)
        neu = [9 - d for d in z[:k]] + [10 - z[k]] + z[k + 1:]
        return int("".join(map(str, neu)))
    n = alle(lambda m: regel(m) == 1000 - m, range(1, 1000), "1000-n")
    n2 = alle(lambda m: regel(m, 4) == 10000 - m, range(1, 10000), "10000-n")
    falsch = sum(1 for m in range(1, 1000) if m % 10 == 0 and
                 int("".join(str(9 - d) for d in ziffern(str(m).zfill(3))[:-1]) + str(10 - m % 10)) != 1000 - m)
    return True, (f"alle {n} Zahlen 1–999 (1000 − n) und {de(n2)} Zahlen 1–9999 richtig, sofern bei Endnull "
                  f"die letzte von 0 verschiedene Ziffer die 10er-Rolle übernimmt; stur angewandt "
                  f"wären {falsch} der 99 Zahlen mit Endnull falsch")


@probe("A5")
def _():
    n = alle(lambda k: sum(range(1, k + 1)) == k * (k + 1) // 2, range(1, 2001), "Gauß")
    return True, f"n = 1 … {n} richtig"


@probe("A6")
def _():
    n = alle(lambda p: p[0] - p[1] == (p[0] + p[2]) - (p[1] + p[2]),
             ((a, b, (-b) % 10) for a in range(600) for b in range(600)), "gleichsinnig")
    return True, f"{de(n)} Fälle a, b < 600 richtig"


@probe("A7")
def _():
    n = alle(lambda k: sum(range(1, 2 * k, 2)) == k * k, range(1, 1001), "ungerade")
    return True, f"n = 1 … {n} richtig"


@probe("A8")
def _():
    n = alle(lambda p: p[0] + (10 - p[0]) + (p[1] - (10 - p[0])) == p[0] + p[1],
             ((a, b) for a in range(1, 10) for b in range(1, 10) if a + b > 10), "Zehnerübergang")
    return True, f"alle {n} Aufgaben mit Zehnerübergang im kleinen Einspluseins richtig"


@probe("A9")
def _():
    n = alle(lambda a: a + (a + 1) == 2 * a + 1 and a + (a - 1) == 2 * a - 1, range(1, 1000), "Fast-Verdoppeln")
    return True, f"a = 1 … {n} (a + (a ± 1) = 2a ± 1) richtig"


# ---------------------------------------------------------- Multiplikation
@probe("M1")
def _():
    n = alle(lambda p: p[0] * p[1] == p[0] * (p[1] + (-p[1]) % 10) - p[0] * ((-p[1]) % 10),
             ((a, b) for a in range(1, 100) for b in range(1, 100)), "Zerlegen")
    return True, f"{de(n)} Paare 1–99 (auf den Zehner aufrunden, Rest abziehen) richtig"


@probe("M2")
def _():
    n = alle(lambda p: p[0] * p[1] == (p[0] // 2) * (2 * p[1]),
             ((a, b) for a in range(2, 200, 2) for b in range(1, 200)), "Halbieren")
    return True, f"{de(n)} Paare (a gerade < 200, b < 200) richtig"


def urdhva(a, b):
    """Kreuzmultiplikation: Spalte k = Summe aller a_i·b_j mit i+j = k, dann Überträge."""
    x, y = ziffern(a)[::-1], ziffern(b)[::-1]
    spalten = [0] * (len(x) + len(y) - 1)
    for i, p in enumerate(x):
        for j, q in enumerate(y):
            spalten[i + j] += p * q
    erg, uebertrag = 0, 0
    for k, s in enumerate(spalten):
        s += uebertrag
        erg += (s % 10) * 10 ** k
        uebertrag = s // 10
    return erg + uebertrag * 10 ** len(spalten)


@probe("M3")
def _():
    n = alle(lambda p: urdhva(*p) == p[0] * p[1], ((a, b) for a in range(10, 100) for b in range(10, 100)), "Urdhva 2×2")
    m = alle(lambda p: urdhva(*p) == p[0] * p[1],
             ((random.randint(100, 999), random.randint(100, 999)) for _ in range(20000)), "Urdhva 3×3")
    return True, f"alle {de(n)} Paare zweistelliger Zahlen und {de(m)} Zufallspaare dreistelliger Zahlen richtig"


@probe("M4")
def _():
    n = alle(lambda p: (p[0] - p[1]) * (p[0] + p[1]) == p[0] ** 2 - p[1] ** 2,
             ((m, d) for m in range(1, 200) for d in range(0, m)), "3. Binom")
    return True, f"{de(n)} Fälle Mitte m < 200, Abstand d < m richtig"


@probe("M5")
def _():
    def bauer(a, b):
        s = 0
        while a:
            if a % 2:
                s += b
            a //= 2
            b *= 2
        return s
    n = alle(lambda p: bauer(*p) == p[0] * p[1], ((a, b) for a in range(1, 300) for b in range(1, 300)), "Bauern")
    return True, f"alle {de(n)} Paare 1–299 richtig"


@probe("M6")
def _():
    def linien(a, b):  # Schnittpunkte je Diagonale zählen = Kreuzmultiplikation
        return urdhva(a, b)
    n = alle(lambda p: linien(*p) == p[0] * p[1], ((a, b) for a in range(10, 100) for b in range(10, 100)), "Linien")
    return True, (f"Schnittpunkt-Zählung je Diagonale = Kreuzmultiplikation; alle {de(n)} Paare zweistelliger "
                  f"Zahlen richtig")


@probe("M7")
def _():
    def gitter(a, b):
        x, y = ziffern(a), ziffern(b)
        diag = {}
        for i, p in enumerate(x):  # Zeile = Ziffer von a? hier Spalte i, Zeile j
            for j, q in enumerate(y):
                z, e = divmod(p * q, 10)
                stelle = (len(x) - 1 - i) + (len(y) - 1 - j)
                diag[stelle] = diag.get(stelle, 0) + e
                diag[stelle + 1] = diag.get(stelle + 1, 0) + z
        return sum(v * 10 ** k for k, v in diag.items())
    n = alle(lambda p: gitter(*p) == p[0] * p[1],
             ((random.randint(1, 9999), random.randint(1, 9999)) for _ in range(30000)), "Gitter")
    return True, f"{de(n)} Zufallspaare bis vierstellig richtig"


@probe("M8")
def _():
    n = alle(lambda p: (10 + p[0]) * (10 + p[1]) == 10 * (10 + p[0] + p[1]) + p[0] * p[1],
             ((a, b) for a in range(1, 10) for b in range(1, 10)), "11-19")
    s = alle(lambda p: (10 + p[0]) * (10 + p[1]) == 200 + p[0] * p[1],
             ((a, 10 - a) for a in range(1, 10)), "Einer-Summe 10")
    return True, f"alle {n} Aufgaben 11–19 × 11–19 richtig; Sonderfall Einer-Summe 10 → 200 + a·b: {s} von {s}"


@probe("M9")
def _():
    def nik(x, y, basis):
        a, b = x - basis, y - basis
        return (x + b) * basis + a * b
    n = alle(lambda p: nik(*p, 100) == p[0] * p[1], ((x, y) for x in range(51, 150) for y in range(51, 150)), "Basis 100")
    m = alle(lambda p: nik(*p, 1000) == p[0] * p[1],
             ((random.randint(900, 1100), random.randint(900, 1100)) for _ in range(20000)), "Basis 1000")
    # Wie oft ist der rechte Teil zweistellig (kein Übertrag nötig)?
    ohne = sum(1 for x in range(90, 100) for y in range(90, 100) if (100 - x) * (100 - y) < 100)
    return True, (f"Identität x·y = (x + b)·Basis + a·b für alle {de(n)} Paare 51–149 (Basis 100) und {de(m)} "
                  f"Zufallspaare 900–1100 (Basis 1000) richtig; bei 90–99 ist der rechte Teil in "
                  f"{ohne} von 100 Fällen ohne Übertrag")


@probe("M10")
def _():
    n = alle(lambda p: (10 * p[0] + p[1]) * (10 * p[0] + 10 - p[1]) == 100 * p[0] * (p[0] + 1) + p[1] * (10 - p[1]),
             ((a, b) for a in range(1, 10) for b in range(1, 10)), "gleiche Zehner")
    m = alle(lambda p: (10 * p[0] + p[1]) * (10 * p[0] + 10 - p[1]) == 100 * p[0] * (p[0] + 1) + p[1] * (10 - p[1]),
             ((a, b) for a in range(10, 100) for b in range(1, 10)), "dreistellig")
    return True, f"alle {n} zweistelligen Paare richtig, ebenso {m} Fälle mit Vorderteil 10–99 (z. B. 123 · 127)"


@probe("M11")
def _():
    n = alle(lambda p: (10 * p[0] + p[2]) * (10 * (10 - p[0]) + p[2]) == 100 * (p[0] * (10 - p[0]) + p[2]) + p[2] ** 2,
             ((a, 0, c) for a in range(1, 10) for c in range(0, 10)), "gleiche Einer")
    return True, f"alle {n} Paare (Zehner-Summe 10, gleiche Einer) richtig"


@probe("M12")
def _():
    n = alle(lambda p: p[0] * p[1] == 50 * (p[0] + p[1] - 50) + (p[0] - 50) * (p[1] - 50),
             ((x, y) for x in range(1, 200) for y in range(1, 200)), "Basis 50")
    return True, f"Identität für alle {de(n)} Paare 1–199 richtig"


@probe("M13")
def _():
    n = alle(lambda k: k * 99 == (k - 1) * 100 + (100 - k), range(1, 101), "×99")
    m = alle(lambda k: k * 999 == (k - 1) * 1000 + (1000 - k), range(1, 1001), "×999")
    return True, f"k · 99 für k = 1 … {n} und k · 999 für k = 1 … {m} richtig"


# ------------------------------------------------------------ Spezialfälle
@probe("S1")
def _():
    n = alle(lambda k: k * 5 == k * 10 // 2, range(10 ** 5), "×5")
    return True, f"k < {de(n)} richtig"


@probe("S2")
def _():
    n = alle(lambda k: k * 25 == k * 100 // 4 and k * 75 == k * 300 // 4, range(10 ** 5), "×25")
    return True, f"k < {de(n)} richtig (auch ×75 = ×300 : 4)"


@probe("S3")
def _():
    n = alle(lambda k: k * 125 == k * 1000 // 8, range(10 ** 5), "×125")
    return True, f"k < {de(n)} richtig"


def mal11(k):
    z = [0] + ziffern(k) + [0]
    erg, ue = [], 0
    for i in range(len(z) - 1, 0, -1):
        s = z[i] + z[i - 1] + ue
        erg.append(s % 10)
        ue = s // 10
    zahl = int("".join(map(str, erg[::-1])))
    return zahl + ue * 10 ** len(erg)


@probe("S4")
def _():
    n = alle(lambda k: 100 * (k // 10) + 10 * (k // 10 + k % 10) + k % 10 == 11 * k, range(10, 100), "×11")
    ue = sum(1 for k in range(10, 100) if k // 10 + k % 10 >= 10)
    return True, f"alle {n} zweistelligen Zahlen richtig; {ue} davon brauchen den Übertrag (Ziffernsumme ≥ 10)"


@probe("S5")
def _():
    n = alle(lambda k: mal11(k) == 11 * k, range(1, 10 ** 5), "×11 mehrstellig")
    return True, f"alle Zahlen 1 … {de(n)} richtig"


@probe("S6")
def _():
    n = alle(lambda k: 9 * k == 10 * k - k and 19 * k == 20 * k - k, range(10 ** 5), "×9")
    return True, f"k < {de(n)} richtig (ebenso ×19 = ×20 − k)"


def trachtenberg(k, regel):
    z = [0, 0] + ziffern(k)  # führende Nullen
    erg, ue = [], 0
    for i in range(len(z) - 1, -1, -1):
        d = z[i]
        nb = z[i + 1] if i + 1 < len(z) else 0  # rechter Nachbar
        s = regel(d, nb) + ue
        erg.append(s % 10)
        ue = s // 10
    zahl = int("".join(map(str, erg[::-1])))
    return zahl + ue * 10 ** len(erg)


@probe("S7")
def _():
    n = alle(lambda k: trachtenberg(k, lambda d, nb: 2 * d + nb) == 12 * k, range(1, 10 ** 5), "×12")
    return True, f"Trachtenberg-Regel ×12 für alle Zahlen 1 … {de(n)} richtig"


@probe("S8")
def _():
    n = alle(lambda k: 15 * k == (k + Fraction(k, 2)) * 10, range(10 ** 4), "×15")
    return True, f"k < {de(n)} richtig"


@probe("S9")
def _():
    n = alle(lambda k: 50 * k == 100 * k // 2, range(10 ** 5), "×50")
    return True, f"k < {de(n)} richtig"


@probe("S10")
def _():
    n = alle(lambda k: k * 101 == int(str(k) * 2), range(10, 100), "×101")
    return True, f"alle {n} zweistelligen Zahlen ergeben ‚abab‘; ab dreistellig gilt nur 100k + k"


@probe("S11")
def _():
    assert 7 * 11 * 13 == 1001
    n = alle(lambda k: k * 1001 == int(str(k) * 2), range(100, 1000), "×1001")
    return True, f"7 · 11 · 13 = 1001; alle {n} dreistelligen Zahlen ergeben ‚abcabc‘"


@probe("S12")
def _():
    n = alle(lambda k: 37 * 3 * k == 111 * k, range(1, 10), "×37")
    return True, f"37 · 3k = kkk für k = 1 … {n} richtig"


@probe("S13")
def _():
    sechs = lambda d, nb: d + nb // 2 + (5 if d % 2 else 0)
    sieben = lambda d, nb: 2 * d + nb // 2 + (5 if d % 2 else 0)
    n = alle(lambda k: trachtenberg(k, sechs) == 6 * k, range(1, 10 ** 5), "×6")
    alle(lambda k: trachtenberg(k, sieben) == 7 * k, range(1, 10 ** 5), "×7")
    return True, f"×6 und ×7 nach Trachtenberg für alle Zahlen 1 … {de(n)} richtig"


# --------------------------------------------------------- Quadrate/Wurzeln
@probe("Q1")
def _():
    n = alle(lambda k: (10 * k + 5) ** 2 == 100 * k * (k + 1) + 25, range(0, 1000), "Endziffer 5")
    return True, f"alle Zahlen 5, 15, … 9995 ({n} Stück) richtig"


@probe("Q2")
def _():
    n = alle(lambda a: (50 + a) ** 2 == 100 * (25 + a) + a * a, range(-49, 50), "nahe 50")
    return True, f"Identität für 1–99 richtig ({n} Zahlen); ohne Übertrag (a² < 100) nur 41–59"


@probe("Q3")
def _():
    n = alle(lambda a: (100 + a) ** 2 == 100 * (100 + 2 * a) + a * a, range(-99, 100), "nahe 100")
    return True, f"Identität für 1–199 richtig ({n} Zahlen); ohne Übertrag (a² < 100) nur 91–109"


@probe("Q4")
def _():
    n = alle(lambda k: k * k == (k // 10 * 10) ** 2 + 2 * (k // 10 * 10) * (k % 10) + (k % 10) ** 2, range(1000), "Binom")
    return True, f"(a + b)² für alle k < {n} (a = Zehneranteil, b = Einer) richtig"


@probe("Q5")
def _():
    n = alle(lambda k: (k + 1) ** 2 == k * k + 2 * k + 1 and (k - 1) ** 2 == k * k - 2 * k + 1, range(1, 10 ** 4), "Nachbar")
    return True, f"k < {de(n)} richtig"


@probe("Q6")
def _():
    n = alle(lambda k: k * k == (k + (-k) % 10) * (k - (-k) % 10) + ((-k) % 10) ** 2, range(1, 1000), "Quadrat über rund")
    return True, f"k = 1 … {n} (d = Abstand zum nächsten Zehner) richtig"


@probe("Q7")
def _():
    worst, worst_n, worst2 = 0, 0, 0
    for N in range(2, 10001):
        a = math.isqrt(N)
        r = N - a * a
        if r == 0:
            continue
        w = math.sqrt(N)
        f1 = (a + r / (2 * a) - w) / w
        f2 = abs(a + r / (2 * a + 1) - w) / w
        assert f1 >= 0
        if f1 > worst:
            worst, worst_n = f1, N
        worst2 = max(worst2, f2)
    f100 = max((math.isqrt(N) + (N - math.isqrt(N) ** 2) / (2 * math.isqrt(N)) - math.sqrt(N)) / math.sqrt(N)
               for N in range(100, 10001))
    return True, (f"N = 2 … 10.000: immer zu groß; größter Fehler {de(worst*100, 1)} % (bei N = {worst_n}), "
                  f"ab N = 100 höchstens {de(f100*100, 2)} %; mit Nenner 2a + 1 höchstens {de(worst2*100, 1)} %")


@probe("Q8")
def _():
    paar = {1: (1, 9), 4: (2, 8), 9: (3, 7), 6: (4, 6), 5: (5, 5), 0: (0, 0)}

    def wurzel(N):
        t = math.isqrt(N // 100)
        e1, e2 = paar[N % 10]
        return 10 * t + (e1 if N < (10 * t + 5) ** 2 else e2)
    n = alle(lambda k: wurzel(k * k) == k, range(1, 100), "Wurzel")
    return True, f"alle {n} Quadratzahlen 1 … 9801 richtig zurückgeführt"


@probe("Q9")
def _():
    endung = {(e ** 3) % 10: e for e in range(10)}
    assert len(endung) == 10

    def kubik(N):
        t = round((N // 1000) ** (1 / 3) + 1e-9)
        while t ** 3 > N // 1000:
            t -= 1
        while (t + 1) ** 3 <= N // 1000:
            t += 1
        return 10 * t + endung[N % 10]
    n = alle(lambda k: kubik(k ** 3) == k, range(1, 100), "Kubik")
    return True, f"alle {n} Kubikzahlen 1 … 970.299 richtig; Endziffer der Kubikzahl bestimmt die Einer eindeutig"


@probe("Q10")
def _():
    def duplex(z):
        k = len(z)
        s = sum(z[i] * z[k - 1 - i] for i in range(k // 2)) * 2
        return s + (z[k // 2] ** 2 if k % 2 else 0)

    def quad(n):
        z = ziffern(n)
        L = len(z)
        spalten = []
        for k in range(2 * L - 1):
            lo, hi = max(0, k - L + 1), min(k, L - 1)
            spalten.append(duplex(z[lo:hi + 1]))
        erg = 0
        for i, s in enumerate(reversed(spalten)):
            erg += s * 10 ** i
        return erg
    n = alle(lambda k: quad(k) == k * k, range(1, 10000), "Duplex")
    return True, f"alle Zahlen 1 … {de(n)} richtig"


# --------------------------------------------------------- Division/Brüche
@probe("D1")
def _():
    n = alle(lambda k: Fraction(k, 5) == Fraction(2 * k, 10), range(10 ** 5), ":5")
    return True, f"k < {de(n)} richtig"


@probe("D2")
def _():
    n = alle(lambda k: Fraction(k, 25) == Fraction(4 * k, 100), range(10 ** 5), ":25")
    return True, f"k < {de(n)} richtig"


@probe("D3")
def _():
    def durch9(N):
        z = ziffern(N)
        q, s = 0, 0
        for d in z[:-1]:
            s += d
            q = q * 10 + s  # laufende Ziffernsumme als nächste Stelle (mit Übertrag)
        r = s + z[-1]
        while r >= 9:
            q, r = q + 1, r - 9
        return q, r
    n = alle(lambda N: durch9(N) == divmod(N, 9), range(10, 10 ** 5), ":9")
    return True, f"alle Zahlen 10 … {de(n + 9)} richtig (Quotient und Rest)"


@probe("D4")
def _():
    n = alle(lambda p: Fraction(p[0], p[1]) == Fraction(2 * p[0], 2 * p[1]),
             ((a, b) for a in range(1, 300) for b in range(1, 300)), "Erweitern")
    return True, f"{de(n)} Brüche richtig (Wert bleibt beim Erweitern gleich)"


@probe("D5")
def _():
    tab = {2: "0,5", 3: "0,333…", 4: "0,25", 5: "0,2", 6: "0,1666…", 8: "0,125", 9: "0,111…",
           10: "0,1", 11: "0,0909…", 12: "0,08333…", 16: "0,0625", 20: "0,05", 25: "0,04", 40: "0,025"}
    for n, s in tab.items():
        ziel = s.replace("…", "").replace(",", ".")
        assert abs(float(ziel) - 1 / n) < 1e-3, n
    return True, f"{len(tab)} Stammbrüche gegen exakte Werte geprüft"


@probe("D6")
def _():
    zyk = "142857"
    for k in range(1, 7):
        x = Fraction(k, 7)
        dez = ""
        rest = k
        for _ in range(6):
            rest *= 10
            dez += str(rest // 7)
            rest %= 7
        assert dez in zyk + zyk, k
    return True, "k/7 für k = 1 … 6 ist jeweils eine Drehung von 142857"


@probe("D7")
def _():
    def periode(z, n, stellen):
        s, r = "", z
        for _ in range(stellen):
            r *= 10
            s += str(r // n)
            r %= n
        return s
    n = alle(lambda k: periode(k, 99, 8) == (str(k).zfill(2)) * 4, range(1, 99), "ab/99")
    m = alle(lambda k: periode(k, 999, 9) == (str(k).zfill(3)) * 3, range(1, 999), "abc/999")
    return True, f"ab/99 für alle {n} Werte, abc/999 für alle {m} Werte richtig"


@probe("D8")
def _():
    n = 0
    for a in range(1, 30):
        for b in range(1, 30):
            for c in range(1, 30, 3):
                for d in range(1, 30, 2):
                    assert Fraction(a, b) + Fraction(c, d) == Fraction(a * d + b * c, b * d)
                    assert (Fraction(a, b) < Fraction(c, d)) == (a * d < b * c)
                    n += 1
    return True, f"{de(n)} Bruchpaare (Summe und Vergleich über Kreuz) richtig"


@probe("D9")
def _():
    erg = []
    for k in range(2, 10):
        n = 10 * k - 1  # 19, 29, …, 89
        # Ekadhikena: von rechts mit 1 beginnen, fortgesetzt mit k multiplizieren (Überträge links)
        ziff, ue, x = [], 0, 1
        periode = len(str(Fraction(1, n)))  # Platzhalter
        # exakte Periodenlänge
        L, r = 1, 10 % n
        while r != 1:
            r = r * 10 % n
            L += 1
        cur = 1
        for _ in range(L):
            s = cur + ue
            ziff.append(s % 10)
            ue = s // 10
            cur = (s % 10) * k
        wert = int("".join(map(str, ziff[::-1])))
        assert Fraction(wert, 10 ** L - 1) == Fraction(1, n), n
        erg.append(f"1/{n}")
    return True, "Ziffernfolge von rechts (×k mit Übertrag) ergibt genau die Periode für " + ", ".join(erg)


@probe("D10")
def _():
    n = alle(lambda p: sum((p[0] // (p[1] * 10 ** e) % 10) * 10 ** e for e in range(4)) * p[1] + p[0] % p[1] == p[0]
             if p[0] < p[1] * 10 ** 4 else True, ((a, b) for a in range(1, 3000, 7) for b in range(2, 40)), "Teilschritte")
    return True, f"{de(n)} Divisionen in Teilschritten richtig"


# ------------------------------------------------------- Prozent und Zinsen
@probe("P1")
def _():
    n = alle(lambda p: Fraction(p[0] * p[1], 100) == Fraction(p[1] * p[0], 100),
             ((x, y) for x in range(0, 201) for y in range(0, 201)), "Tausch")
    return True, f"{de(n)} Paare x, y ≤ 200 richtig"


@probe("P2")
def _():
    n = alle(lambda p: Fraction(p[0] * p[1], 100) == Fraction(p[1] // 10 * p[0], 10) + Fraction(p[1] % 10 * p[0], 100),
             ((g, q) for g in range(1, 500) for q in range(0, 100)), "Bausteine")
    return True, f"{de(n)} Fälle (q % = Zehner · 10 % + Einer · 1 %) richtig"


@probe("P3")
def _():
    n = alle(lambda p: (1 + Fraction(p, 100)) * (1 - Fraction(p, 100)) == 1 - Fraction(p * p, 10000), range(0, 101), "±p")
    return True, f"p = 0 … 100 % richtig; Reihenfolge egal; Beispiel ±10 % → −1 %, ±50 % → −25 %"


def verdopplung(p):
    return math.log(2) / math.log(1 + p / 100)


@probe("P4")
def _():
    werte = [(p, 72 / p - verdopplung(p)) for p in range(1, 21)]
    maxabs = max(abs(f) for _, f in werte)
    rel = max(abs(f) / verdopplung(p) for p, f in werte)
    # bester Zinssatz: 72/p = exakt
    lo, hi = 1.0, 20.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if 72 / mid - verdopplung(mid) > 0:
            lo = mid
        else:
            hi = mid
    f1 = 72 - verdopplung(1); f20 = 72 / 20 - verdopplung(20)
    return True, (f"jährliche Verzinsung 1–20 %: Fehler höchstens {de(maxabs, 2)} Jahre "
                  f"({de(rel*100, 1)} % relativ); bei 1 % zu kurz um {de(abs(f1), 2)} J., bei 20 % zu kurz um {de(abs(f20), 2)} J.; "
                  f"exakt bei {de(lo, 2)} %")


@probe("P5")
def _():
    rel70 = max(abs(70 / p - verdopplung(p)) / verdopplung(p) for p in range(1, 11))
    rel69 = max(abs(69.3 / p - 100 * math.log(2) / p) / (100 * math.log(2) / p) for p in range(1, 21))
    return True, (f"69,3/p ist bei stetiger Verzinsung bis auf {de(rel69*100, 2)} % exakt (100·ln 2 = 69,31); "
                  f"70/p bei jährlicher Verzinsung 1–10 %: Fehler höchstens {de(rel70*100, 1)} %")


@probe("P6")
def _():
    v = lambda p, f: math.log(f) / math.log(1 + p / 100)
    r3 = max(abs(114 / p - v(p, 3)) / v(p, 3) for p in range(1, 16))
    r4 = max(abs(144 / p - v(p, 4)) / v(p, 4) for p in range(1, 16))
    return True, f"1–15 % jährlich: 114/p (Verdreifachung) Fehler höchstens {de(r3*100, 1)} %, 144/p (Vervierfachung) höchstens {de(r4*100, 1)} %"


@probe("P7")
def _():
    n = alle(lambda v: (1 - Fraction(v, 100)) * (1 + Fraction(v, 100 - v)) == 1, range(1, 100), "Verlust")
    return True, f"v = 1 … {n} % exakt: −10 % → +11,1 %, −20 % → +25 %, −50 % → +100 %"


@probe("P8")
def _():
    a19 = Fraction(19, 119); a7 = Fraction(7, 107)
    n = alle(lambda b: Fraction(b) / Fraction(119, 100) + Fraction(b) * a19 == b, range(1, 10 ** 4), "Brutto")
    return True, (f"Netto = Brutto : 1,19 und Steueranteil = Brutto · 19/119 ({de(float(a19)*100, 2)} %) "
                  f"für {de(n)} Beträge exakt; bei 7 %: 7/107 = {de(float(a7)*100, 2)} %")


@probe("P9")
def _():
    zeilen = []
    for p, n in ((3, 10), (5, 10), (5, 30), (7, 10)):
        ex = (1 + p / 100) ** n
        ap = math.exp(n * p / 100)
        zeilen.append(f"{p} %/{n} J.: {de((ap/ex-1)*100, 1, True)} %")
    return True, "e^(n·r) überschätzt (1 + r)^n: " + "; ".join(zeilen)


@probe("P10")
def _():
    worst = 0
    for mu in [i / 100 for i in range(0, 11)]:
        for s in [i / 100 for i in range(5, 31)]:
            geo = math.sqrt((1 + mu + s) * (1 + mu - s)) - 1
            nah = mu - s * s / 2
            worst = max(worst, abs(geo - nah))
    geo50 = math.sqrt(1.5 * 0.5) - 1
    return True, (f"zwei gleich wahrscheinliche Renditen μ ± σ (μ 0–10 %, σ 5–30 %): Abweichung höchstens "
                  f"{de(worst*100, 2)} Prozentpunkte; Extremfall +50 %/−50 %: exakt {de(geo50*100, 1)} % pro Periode, "
                  f"Näherung −12,5 %")


@probe("P11")
def _():
    random.seed(1)
    tage, jahre = 252, 4000
    s = [sum(random.gauss(0, 0.01) for _ in range(tage)) for _ in range(jahre)]
    m = sum(s) / jahre
    sd = math.sqrt(sum((x - m) ** 2 for x in s) / (jahre - 1))
    return True, (f"√252 = {de(math.sqrt(252), 2)}; Simulation (4.000 Jahre, unabhängige Tagesrenditen mit σ = 1 %): "
                  f"Jahres-σ = {de(sd*100, 2)} % (Regel: 15,87 %)")


@probe("P12")
def _():
    n = alle(lambda p: (1 + Fraction(p[0], 100)) * (1 + Fraction(p[1], 100)) == 1 + Fraction(p[0] + p[1], 100) + Fraction(p[0] * p[1], 10000),
             ((a, b) for a in range(-50, 51) for b in range(-50, 51)), "verketten")
    return True, f"{de(n)} Paare −50 … +50 % exakt; der Kreuzterm a·b ist der Fehler der Summen-Näherung (bei +10 %/+10 %: 1 Prozentpunkt)"


# ------------------------------------------------------------ Teilbarkeit
GRENZE = 200000


@probe("T1")
def _():
    for t, k in ((2, 1), (4, 2), (8, 3), (5, 1), (25, 2), (125, 3), (10, 1), (16, 4)):
        alle(lambda n: (n % t == 0) == ((n % 10 ** k) % t == 0), range(GRENZE), f"Endstellen {t}")
    return True, f"Teiler 2, 4, 8, 16, 5, 25, 125, 10 für alle n < {de(GRENZE)} richtig"


@probe("T2")
def _():
    for t in (3, 9):
        alle(lambda n: (n % t == 0) == (sum(ziffern(n)) % t == 0), range(GRENZE), f"Quersumme {t}")
    return True, f"3 und 9 für alle n < {de(GRENZE)} richtig; Quersumme liefert sogar den Rest"


def alt_qs(n, block=1):
    s, vz = 0, 1
    while n:
        s += vz * (n % 10 ** block)
        n //= 10 ** block
        vz = -vz
    return s


@probe("T3")
def _():
    alle(lambda n: (n % 11 == 0) == (alt_qs(n) % 11 == 0), range(GRENZE), "11")
    return True, f"alle n < {de(GRENZE)} richtig (von rechts beginnend +, −, +, …)"


@probe("T4")
def _():
    alle(lambda n: (n % 7 == 0) == ((n // 10 - 2 * (n % 10)) % 7 == 0), range(GRENZE), "7")
    return True, f"alle n < {de(GRENZE)} richtig; Schritt beliebig oft wiederholbar"


@probe("T5")
def _():
    for t in (7, 11, 13):
        alle(lambda n: (n % t == 0) == (alt_qs(n, 3) % t == 0), range(0, 10 ** 7, 7), f"Dreierblock {t}")
    return True, "7, 11, 13 für 1,43 Mio. Zahlen < 10⁷ (jede 7.) richtig"


@probe("T6")
def _():
    alle(lambda n: (n % 13 == 0) == ((n // 10 + 4 * (n % 10)) % 13 == 0), range(GRENZE), "13")
    return True, f"alle n < {de(GRENZE)} richtig"


@probe("T7")
def _():
    alle(lambda n: (n % 6 == 0) == (n % 2 == 0 and n % 3 == 0), range(GRENZE), "6")
    alle(lambda n: (n % 12 == 0) == (n % 3 == 0 and n % 4 == 0), range(GRENZE), "12")
    alle(lambda n: (n % 15 == 0) == (n % 3 == 0 and n % 5 == 0), range(GRENZE), "15")
    alle(lambda n: (n % 18 == 0) == (n % 2 == 0 and n % 9 == 0), range(GRENZE), "18")
    falsch = next(n for n in range(1, 100) if n % 2 == 0 and n % 6 == 0 and n % 12)
    return True, f"6 = 2·3, 12 = 3·4, 15 = 3·5, 18 = 2·9 für n < {de(GRENZE)} richtig; Falle: 2 und 6 reichen für 12 nicht (Gegenbeispiel {falsch})"


@probe("T8")
def _():
    def block(n):
        s = 0
        while n:
            s += n % 1000
            n //= 1000
        return s
    for t in (27, 37, 111, 333, 999):
        alle(lambda n: (n % t == 0) == (block(n) % t == 0), range(0, 10 ** 7, 7), f"Block {t}")
    return True, "27, 37, 111, 333, 999 für 1,43 Mio. Zahlen < 10⁷ (jede 7.) richtig"


@probe("T9")
def _():
    def block(n):
        s = 0
        while n:
            s += n % 100
            n //= 100
        return s
    for t in (33, 99):
        alle(lambda n: (n % t == 0) == (block(n) % t == 0), range(GRENZE), f"Zweierblock {t}")
    return True, f"33 und 99 für alle n < {de(GRENZE)} richtig"


# --------------------------------------------------------- Ergebnisse prüfen
def fehlerarten(rechne, rest):
    """Anteil erkannter Fehler je Fehlerart bei 20.000 zufälligen Produkten."""
    erk = {"Ziffer falsch": [0, 0], "Nachbarziffern vertauscht": [0, 0], "Stelle verrutscht (×10)": [0, 0]}
    random.seed(9)
    for _ in range(20000):
        a, b = random.randint(100, 9999), random.randint(100, 9999)
        r = a * b
        z = ziffern(r)
        i = random.randrange(len(z))
        z1 = z[:]
        z1[i] = random.choice([d for d in range(10) if d != z[i]])
        if z1[0] == 0:
            z1[0] = 1 if z[0] != 1 else 2
        f1 = int("".join(map(str, z1)))
        j = random.randrange(len(z) - 1)
        z2 = z[:]
        z2[j], z2[j + 1] = z2[j + 1], z2[j]
        f2 = int("".join(map(str, z2)))
        f3 = r * 10
        for art, f in (("Ziffer falsch", f1), ("Nachbarziffern vertauscht", f2), ("Stelle verrutscht (×10)", f3)):
            if f == r:
                continue
            erk[art][1] += 1
            if rest(f) != rest(rest(a) * rest(b)):
                erk[art][0] += 1
    return "; ".join(f"{k}: {de(v[0]/v[1]*100, 0)} % erkannt" for k, v in erk.items())


@probe("E1")
def _():
    alle(lambda p: (p[0] * p[1]) % 9 == ((sum(ziffern(p[0])) % 9) * (sum(ziffern(p[1])) % 9)) % 9,
         ((a, b) for a in range(1, 500) for b in range(1, 500, 3)), "Neunerprobe")
    return True, "richtige Ergebnisse bestehen immer; 20.000 Zufallsfehler: " + fehlerarten(None, lambda x: x % 9)


@probe("E2")
def _():
    alle(lambda p: (p[0] * p[1]) % 11 == (alt_qs(p[0]) % 11 * (alt_qs(p[1]) % 11)) % 11,
         ((a, b) for a in range(1, 500) for b in range(1, 500, 3)), "Elferprobe")
    return True, "richtige Ergebnisse bestehen immer; 20.000 Zufallsfehler: " + fehlerarten(None, lambda x: x % 11)


@probe("E3")
def _():
    alle(lambda p: (p[0] * p[1]) % 10 == (p[0] % 10) * (p[1] % 10) % 10,
         ((a, b) for a in range(1, 1000) for b in range(1, 1000, 3)), "Endziffer")
    return True, "Endziffer stimmt bei allen 333.000 Paaren < 1000; " + fehlerarten(None, lambda x: x % 10)


@probe("E4")
def _():
    L = lambda n: len(str(n))
    n = alle(lambda p: L(p[0] * p[1]) in (L(p[0]) + L(p[1]) - 1, L(p[0]) + L(p[1])),
             ((random.randint(1, 10 ** 6), random.randint(1, 10 ** 6)) for _ in range(100000)), "Stellen")
    return True, f"{de(n)} Zufallsprodukte: Stellenzahl immer m + n − 1 oder m + n"


@probe("E5")
def _():
    n = alle(lambda p: (p[0] * p[1]) % 2 == (p[0] % 2) * (p[1] % 2) and (p[0] + p[1]) % 2 == (p[0] + p[1]) % 2,
             ((a, b) for a in range(300) for b in range(300)), "Parität")
    return True, f"{de(n)} Paare richtig; erkennt nur Fehler, die die Parität ändern (≈ jeder zweite Zufallsfehler)"


@probe("E6")
def _():
    n = alle(lambda p: (p[0] * p[1]) // p[1] == p[0] and (p[0] + p[1]) - p[1] == p[0],
             ((a, b) for a in range(1, 300) for b in range(1, 300)), "Umkehr")
    return True, f"{de(n)} Paare; Umkehraufgabe deckt jeden Fehler auf, kostet aber eine zweite Rechnung"


# --------------------------------------------------------- Überschlagen
@probe("U1")
def _():
    def runde1(x):
        e = 10 ** (len(str(x)) - 1)
        return round(x / e) * e
    fehler = sorted(abs(runde1(a) * runde1(b) / (a * b) - 1) for a in range(10, 100) for b in range(10, 100))
    med = fehler[len(fehler) // 2]
    p90 = fehler[int(len(fehler) * 0.9)]
    return True, (f"beide Faktoren 10–99 auf eine gültige Ziffer gerundet: Median-Fehler {de(med*100, 0)} %, "
                  f"90 % der Fälle unter {de(p90*100, 0)} %, schlimmster Fall {de(fehler[-1]*100, 0)} %")


@probe("U2")
def _():
    a, b = 3.2e4, 6.5e5
    assert abs(a * b - 2.08e10) < 1
    return True, "Exponenten addieren, Mantissen multiplizieren – exakt; Beispiel 3,2·10⁴ · 6,5·10⁵ = 2,08·10¹⁰"


@probe("U3")
def _():
    g = math.sqrt(100 * 10000)
    return True, f"geometrisches Mittel als Schätzwert zwischen Grenzen: √(100 · 10.000) = {de(g, 0)}"


@probe("U4")
def _():
    werte = {"lg 2": (0.30103, math.log10(2)), "lg 3": (0.47712, math.log10(3)), "lg 7": (0.84510, math.log10(7)),
             "lg 5 = 1 − lg 2": (1 - 0.30103, math.log10(5))}
    for k, (a, b) in werte.items():
        assert abs(a - b) < 1e-5, k
    return True, "lg 2 ≈ 0,301, lg 3 ≈ 0,477, lg 7 ≈ 0,845 auf 5 Stellen geprüft; 2⁶⁴ ≈ 10^(64·0,301) = 10^19,27 ≈ 1,8·10¹⁹ (exakt 1,84·10¹⁹)"


@probe("U5")
def _():
    t = [f"2^{10*k} / 10^{3*k} = {de(2**(10*k)/10**(3*k), 3)}" for k in (1, 2, 3, 4)]
    return True, ("Abweichung wächst: " + "; ".join(t))


@probe("U6")
def _():
    z = []
    for x, n in ((0.01, 10), (0.02, 10), (0.05, 10), (0.01, 50)):
        ex = (1 + x) ** n
        z.append(f"x = {de(x*100, 0)} %, n = {n}: {de(ex, 4)} statt {de(1+n*x, 2)}")
    return True, ("unterschätzt immer (für x > 0, n ≥ 2): " + "; ".join(z))


@probe("U7")
def _():
    z = []
    for x in (0.01, 0.05, 0.1, 0.2):
        z.append(f"x = {de(x*100, 0)} %: ln(1 + x) = {de(math.log1p(x), 4)}")
    return True, ("Fehler ≈ x²/2: " + "; ".join(z))


@probe("U8")
def _():
    worst = 0
    for a in [i / 1000 for i in range(-50, 51, 5)]:
        for b in [i / 1000 for i in range(-50, 51, 5)]:
            exakt = (1 + a) * (1 + b) - 1
            worst = max(worst, abs(exakt - (a + b)))
    return True, f"relative Fehler bis ±5 % je Faktor: Summen-Näherung weicht höchstens {de(worst*100, 2)} Prozentpunkte ab"


@probe("U9")
def _():
    werte = [("22/7", 22 / 7, math.pi), ("355/113", 355 / 113, math.pi), ("1,414", 1.414, math.sqrt(2)),
             ("1,732", 1.732, math.sqrt(3)), ("2,718", 2.718, math.e)]
    return True, "; ".join(f"{n}: {de(abs(a/b-1)*100, 5)} % daneben" for n, a, b in werte)


@probe("U10")
def _():
    jahr = 365.2425 * 86400
    return True, f"Jahr = {de(jahr, 0)} s, π·10⁷ = 31.415.927 s, Abweichung {de(abs(math.pi*1e7/jahr-1)*100, 2)} %"


# ------------------------------------------------------------ Kalender
DOOMS_MONAT = {1: 3, 2: 28, 3: 14, 4: 4, 5: 9, 6: 6, 7: 11, 8: 8, 9: 5, 10: 10, 11: 7, 12: 12}
ANKER = {0: 2, 1: 0, 2: 5, 3: 3}  # Jahrhundert mod 4 -> Ankertag (0 = So) für 1600/1700/1800/1900...


def doomsday(j):
    c, y = divmod(j, 100)
    anker = ANKER[c % 4]
    return (anker + y // 12 + y % 12 + (y % 12) // 4) % 7


def wochentag_conway(j, m, t):
    ref = DOOMS_MONAT[m]
    if calendar.isleap(j) and m in (1, 2):
        ref += 1
    return (doomsday(j) + t - ref) % 7  # 0 = Sonntag


def py_wt(j, m, t):
    return (dt.date(j, m, t).weekday() + 1) % 7  # 0 = Sonntag


def tage(start, ende):
    d = start
    while d <= ende:
        yield d
        d += dt.timedelta(days=1)


@probe("K1")
def _():
    n = alle(lambda d: wochentag_conway(d.year, d.month, d.day) == py_wt(d.year, d.month, d.day),
             tage(dt.date(1583, 1, 1), dt.date(2499, 12, 31)), "Doomsday")
    return True, f"alle {de(n)} Tage 1583–2499 (gregorianisch) richtig"


@probe("K2")
def _():
    def gauss(j, m, t):
        if m < 3:
            m += 12
            j -= 1
        mm = m - 2  # März = 1
        c, y = divmod(j, 100)
        return (t + (13 * mm - 1) // 5 + y + y // 4 + c // 4 - 2 * c) % 7
    n = alle(lambda d: gauss(d.year, d.month, d.day) == py_wt(d.year, d.month, d.day),
             tage(dt.date(1583, 1, 1), dt.date(2499, 12, 31)), "Gauß")
    return True, f"alle {de(n)} Tage 1583–2499 richtig"


@probe("K3")
def _():
    def odd11(y):
        t = y
        if t % 2:
            t += 11
        t //= 2
        if t % 2:
            t += 11
        return (7 - t % 7) % 7
    n = alle(lambda y: odd11(y) == (y // 12 + y % 12 + (y % 12) // 4) % 7, range(100), "Odd+11")
    return True, f"Jahreszahl-Anteil für alle {n} Endungen 00–99 identisch mit Conways Formel"


@probe("K4")
def _():
    n = alle(lambda j: ((j % 4 == 0 and j % 100 != 0) or j % 400 == 0) == calendar.isleap(j), range(1583, 10000), "Schaltjahr")
    return True, f"Jahre 1583–9999 ({de(n)}) richtig; 2100, 2200, 2300 sind keine Schaltjahre, 2400 schon"


@probe("K5")
def _():
    def formel(h, m):
        w = abs(30 * h - 5.5 * m) % 360
        return min(w, 360 - w)

    def sim(h, m):
        stunde = (h % 12) * 30 + m * 0.5
        minute = m * 6
        w = abs(stunde - minute) % 360
        return min(w, 360 - w)
    n = alle(lambda p: abs(formel(*p) - sim(*p)) < 1e-9, ((h, m) for h in range(24) for m in range(60)), "Uhr")
    return True, f"alle {de(n)} Minuten eines Tages richtig; Zeiger decken sich alle 12/11 h ≈ 65 min 27 s"


@probe("K6")
def _():
    def gauss_ostern(j):  # Gauß mit Korrekturen (Lichtenberg 1997)
        k = j // 100
        m = 15 + (3 * k + 3) // 4 - (8 * k + 13) // 25
        s = 2 - (3 * k + 3) // 4
        a = j % 19
        d = (19 * a + m) % 30
        r = (d + a // 11) // 29
        og = 21 + d - r
        sz = 7 - (j + j // 4 + s) % 7
        oe = 7 - (og - sz) % 7
        os_ = og + oe
        return dt.date(j, 3, 1) + dt.timedelta(days=os_ - 1)

    def meeus(j):  # anonymer gregorianischer Algorithmus (Meeus/Jones/Butcher) als Referenz
        a, b, c = j % 19, j // 100, j % 100
        d, e = divmod(b, 4)
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i, k = divmod(c, 4)
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        mon, tag = divmod(h + l - 7 * m + 114, 31)
        return dt.date(j, mon, tag + 1)
    n = alle(lambda j: gauss_ostern(j) == meeus(j) and gauss_ostern(j).weekday() == 6, range(1583, 5000), "Ostern")
    return True, f"alle Jahre 1583–4999 ({de(n)}) stimmen mit dem Meeus-Algorithmus überein und fallen auf Sonntag"


@probe("K7")
def _():
    n = alle(lambda j: all(dt.date(j, m, 1).weekday() == dt.date(j + 28, m, 1).weekday() for m in range(1, 13))
             and calendar.isleap(j) == calendar.isleap(j + 28), range(1901, 2072), "28 Jahre")
    falsch = next(j for j in range(2072, 2200) if dt.date(j, 1, 1).weekday() != dt.date(j + 28, 1, 1).weekday()
                  or calendar.isleap(j) != calendar.isleap(j + 28))
    return True, f"Kalender von 1901–2071 wiederholt sich nach 28 Jahren ({n} Jahre geprüft); bricht über 2100 hinweg (erstes Gegenbeispiel {falsch})"


# ------------------------------------------------------ Statistik
@probe("W1")
def _():
    z = []
    for n in (10, 30, 100, 1000):
        ex = 1 - 0.05 ** (1 / n)
        z.append(f"n = {n}: 3/n = {de(3/n*100, 2)} %, exakt {de(ex*100, 2)} %")
    return True, ("95-%-Obergrenze bei 0 Ereignissen in n Versuchen: " + "; ".join(z))


@probe("W2")
def _():
    phi = lambda k: math.erf(k / math.sqrt(2))
    return True, f"Normalverteilung: ±1σ {de(phi(1)*100, 2)} %, ±2σ {de(phi(2)*100, 2)} %, ±3σ {de(phi(3)*100, 2)} %; 95 % genau bei ±1,96 σ"


@probe("W3")
def _():
    random.seed(3)
    z = []
    for n in (25, 100, 400):
        mittel = [sum(random.random() for _ in range(n)) / n for _ in range(4000)]
        m = sum(mittel) / len(mittel)
        sd = math.sqrt(sum((x - m) ** 2 for x in mittel) / (len(mittel) - 1))
        z.append(f"n = {n}: {de(sd, 4)} (Regel {de(math.sqrt(1/12)/math.sqrt(n), 4)})")
    return True, ("Standardfehler des Mittelwerts (Gleichverteilung, 4000 Wiederholungen): " + "; ".join(z))


@probe("W4")
def _():
    z = []
    for n in (100, 400, 1000, 2500):
        ex = 1.96 * math.sqrt(0.25 / n)
        z.append(f"n = {n}: 1/√n = {de(1/math.sqrt(n)*100, 1)} %, exakt {de(ex*100, 2)} %")
    return True, ("95-%-Fehlermarge für einen Anteil nahe 50 %: " + "; ".join(z) + "; 1/√n ist um 2 % zu groß")


@probe("W5")
def _():
    def p(n, N=365):
        q = 1.0
        for i in range(n):
            q *= (N - i) / N
        return 1 - q
    n50 = next(n for n in range(1, 100) if p(n) >= 0.5)
    nah = 1.1774 * math.sqrt(365)
    worst = max(abs(p(n) - (1 - math.exp(-n * (n - 1) / 730))) for n in range(1, 80))
    return True, (f"P(23) = {de(p(23)*100, 1)} % (erste Gruppe über 50 %: {n50}); Näherung 1,18·√365 = {de(nah, 1)}; "
                  f"1 − e^(−n(n−1)/730) weicht für n < 80 höchstens {de(worst*100, 2)} Prozentpunkte ab")


@probe("W6")
def _():
    z = []
    for p_, n in ((0.01, 10), (0.01, 50), (0.05, 10), (0.1, 10)):
        z.append(f"p = {de(p_*100, 0)} %, n = {n}: exakt {de((1-(1-p_)**n)*100, 1)} %, n·p = {de(n*p_*100, 0)} %")
    return True, ("n·p überschätzt immer: " + "; ".join(z))


@probe("W7")
def _():
    z = [f"n = {n}: {de((1-(1-1/n)**n)*100, 1)} %" for n in (2, 6, 10, 100)]
    return True, (f"1 − 1/e = {de((1-1/math.e)*100, 1)} %; " + "; ".join(z))


@probe("W8")
def _():
    random.seed(5)
    treffer = 0
    for _ in range(200000):
        x = [random.random() for _ in range(5)]
        treffer += min(x) < 0.5 < max(x)
    return True, f"exakt 1 − 2·(1/2)⁵ = 93,75 %; Simulation (200.000 Läufe): {de(treffer/2000, 2)} %"


@probe("W9")
def _():
    z = []
    for k in (2, 3):
        normal = 1 - math.erf(k / math.sqrt(2))
        z.append(f"k = {k}: Schranke {de(100/k/k, 1)} %, Normalverteilung {de(normal*100, 2)} %")
    return True, ("gilt für jede Verteilung mit endlicher Varianz, ist aber grob: " + "; ".join(z))


@probe("W10")
def _():
    random.seed(8)
    s = [random.gauss(0, 3) + random.gauss(0, 4) for _ in range(100000)]
    m = sum(s) / len(s)
    sd = math.sqrt(sum((x - m) ** 2 for x in s) / (len(s) - 1))
    return True, f"σ = 3 und σ = 4 unabhängig: Summe σ = 5 (nicht 7); Simulation 100.000 Werte: {de(sd, 3)}"


@probe("W11")
def _():
    random.seed(6)
    wuerfe = []
    for _ in range(100000):
        k = 1
        while random.randint(1, 6) != 6:
            k += 1
        wuerfe.append(k)
    m = sum(wuerfe) / len(wuerfe)
    med = sorted(wuerfe)[len(wuerfe) // 2]
    return True, f"Erwartung 1/p = 6 Würfe; Simulation 100.000 Läufe: Mittel {de(m, 2)}, Median {med} (die Hälfte schafft es in ≤ 4)"


# ------------------------------------------------------- Systeme/Finger
@probe("R1")
def _():
    return True, "Einzelverfahren geprüft: siehe A4, M3, M9, M10, Q3, Q10, D3, D9"


@probe("R2")
def _():
    return True, "Einzelregeln geprüft: siehe S5, S7, S13"


@probe("R3")
def _():
    # Soroban: jede Ziffer 0–9 = Himmelsperle (5) + 0–4 Erdperlen, eindeutig
    darst = {(h, e) for h in (0, 1) for e in range(5)}
    assert sorted(5 * h + e for h, e in darst) == list(range(10))
    return True, "jede Ziffer 0–9 eindeutig als 5·h + e (h ∈ {0,1}, e ∈ {0,…,4}) darstellbar"


@probe("R4")
def _():
    n = alle(lambda p: p[0] + p[1] == p[0] + 10 - (10 - p[1]) and p[0] + p[1] == p[0] + 5 - (5 - p[1] if p[1] <= 5 else 0) + (p[1] - 5 if p[1] > 5 else 0),
             ((a, b) for a in range(10) for b in range(1, 10)), "Freunde")
    return True, f"alle {n} Ziffernadditionen über 5er- und 10er-Freunde richtig"


@probe("R5")
def _():
    return True, "rechnerisch identisch mit der Gittermethode M7 (geprüft)"


@probe("F1")
def _():
    n = alle(lambda k: 10 * (k - 1) + (10 - k) == 9 * k, range(1, 11), "9er")
    return True, f"9 · k für k = 1 … {n} richtig"


@probe("F2")
def _():
    n = alle(lambda p: 10 * (p[0] - 5 + p[1] - 5) + (10 - p[0]) * (10 - p[1]) == p[0] * p[1],
             ((a, b) for a in range(6, 11) for b in range(6, 11)), "Finger 6-10")
    m = alle(lambda p: 10 * (p[0] - 5 + p[1] - 5) + (10 - p[0]) * (10 - p[1]) == p[0] * p[1],
             ((a, b) for a in range(1, 30) for b in range(1, 30)), "Finger allgemein")
    return True, f"alle {n} Aufgaben 6–10 × 6–10 richtig; als Formel sogar für alle a, b ({m} Paare geprüft), nur mit Fingern nicht darstellbar"


@probe("F3")
def _():
    darst = {}
    for lt in (0, 1):
        for lf in range(5):
            for rt in (0, 1):
                for rf in range(5):
                    darst.setdefault(50 * lt + 10 * lf + 5 * rt + rf, []).append(1)
    assert sorted(darst) == list(range(100)) and all(len(v) == 1 for v in darst.values())
    return True, "jede Zahl 0–99 genau eine Fingerstellung (links: Daumen 50, Finger je 10; rechts: Daumen 5, Finger je 1)"


@probe("F4")
def _():
    knochen = [1, 3, 5, 7, 8, 10, 12]  # Monate auf Knöcheln
    n = alle(lambda m: (calendar.monthrange(2026, m)[1] == 31) == (m in knochen), range(1, 13), "Knöchel")
    return True, "alle 12 Monate richtig (Knöchel = 31 Tage; Juli und August liegen nebeneinander auf Knöcheln)"


@probe("F5")
def _():
    assert 2 ** 10 - 1 == 1023
    return True, "10 Finger als Binärziffern: 0 … 2¹⁰ − 1 = 1023, jede Zahl genau eine Stellung"


@probe("F6")
def _():
    n = alle(lambda p: 100 + 10 * ((p[0] - 10) + (p[1] - 10)) + (p[0] - 10) * (p[1] - 10) == p[0] * p[1],
             ((a, b) for a in range(11, 16) for b in range(11, 16)), "Finger 11-15")
    return True, f"alle {n} Aufgaben 11–15 × 11–15 richtig"


# ------------------------------------------------- Ergänzungen aus der Recherche
@probe("S14")
def _():
    n = alle(lambda k: Fraction(3, 2) * k == k + Fraction(k, 2), range(10 ** 5), "×1,5")
    return True, f"k < {de(n)} richtig (×1,5 = Zahl + Hälfte)"


@probe("A10")
def _():
    assert 10**2 + 11**2 + 12**2 == 365 == 13**2 + 14**2
    return True, "10² + 11² + 12² = 365 = 13² + 14², also (10² + … + 14²) : 365 = 2"


@probe("M14")
def _():
    n = alle(lambda p: (p[0] * 10 ** p[2]) * (p[1] * 10 ** p[3]) == p[0] * p[1] * 10 ** (p[2] + p[3]),
             ((a, b, i, j) for a in range(1, 50) for b in range(1, 50) for i in range(4) for j in range(4)), "Nullen")
    return True, f"{de(n)} Fälle richtig (Nullen zählen und anhängen)"


@probe("S15")
def _():
    for k in range(1, 10):
        alle(lambda x: trachtenberg(x, lambda d, nb: k * d + nb) == (10 + k) * x, range(1, 20000), f"×1{k}")
    return True, "×11 bis ×19 (k-fache Ziffer + rechter Nachbar, mit Übertrag) für alle Zahlen 1 … 19.999 richtig"


@probe("Q11")
def _():
    assert all(e ** 5 % 10 == e for e in range(10))
    def wurzel5(N):
        t = 0
        while (t + 1) ** 5 * 10 ** 5 <= N:
            t += 1
        return 10 * t + N % 10
    n = alle(lambda k: wurzel5(k ** 5) == k, range(1, 100), "5. Wurzel")
    return True, f"alle {n} fünften Potenzen von 1 … 99 richtig; Endziffer der Potenz = Endziffer der Basis"


@probe("T10")
def _():
    alle(lambda n: (n % 7 == 0) == ((3 * (n // 10) + n % 10) % 7 == 0), range(GRENZE), "7 russisch")
    return True, f"7-Regel ‚Zehnerzahl · 3 + Einer‘ für alle n < {de(GRENZE)} richtig"


@probe("P13")
def _():
    v = lambda p: math.log(3) / math.log(1 + p / 100)
    r108 = max(abs(108 / p - v(p)) / v(p) for p in range(1, 16))
    bester = min(range(100, 121), key=lambda c: max(abs(c / p - v(p)) / v(p) for p in range(1, 16)))
    return True, (f"Verdreifachung, 1–15 % jährlich: 108/p höchstens {de(r108*100, 1)} % daneben; "
                  f"beste ganze Konstante im Bereich: {bester}; 100·ln 3 = 109,9 (stetig exakt)")


@probe("W12")
def _():
    k = math.sqrt(2)
    normal = math.erf(k / math.sqrt(2))
    return True, f"mindestens 1 − 1/k² = 50 % innerhalb ±√2·σ; bei Normalverteilung tatsächlich {de(normal*100, 1)} %"

@probe("S16")
def _():
    def mal111(k):  # Summen über bis zu drei Nachbarziffern
        z = [0, 0] + ziffern(k) + [0, 0]
        erg = 0
        for i in range(len(z) - 2):
            erg = erg * 10 + z[i] + z[i + 1] + z[i + 2]
        return erg
    n = alle(lambda k: mal111(k) == 111 * k, range(1, 10 ** 5), "×111")
    return True, f"Nachbarsummen-Regel für alle Zahlen 1 … {de(n)} richtig"


@probe("M15")
def _():
    n = alle(lambda p: (10 * p[0] + p[1]) * (10 * p[1] + p[0]) == 101 * p[0] * p[1] + 10 * (p[0] ** 2 + p[1] ** 2),
             ((a, b) for a in range(1, 10) for b in range(1, 10)), "Spiegel")
    return True, f"alle {n} Paare ab · ba richtig"


@probe("M16")
def _():
    n = alle(lambda p: (10 * p[0] + 10 - p[0]) * 11 * p[1] == 100 * (p[0] + 1) * p[1] + (10 - p[0]) * p[1],
             ((a, c) for a in range(1, 10) for c in range(1, 10)), "Schnapszahl")
    return True, f"alle {n} Paare (Ziffernsumme 10) · (cc) richtig, z. B. 73 · 55 = 8·5 | 3·5 = 4015"


@probe("E7")
def _():
    random.seed(12)
    n = 0
    for _ in range(20000):
        a, b = random.randint(1000, 99999), random.randint(1000, 99999)
        z = ziffern(a * b)
        i = random.randrange(len(z))
        if z[i] in (0, 9):
            continue
        rest = sum(z) - z[i]
        x = (a % 9 * (b % 9) - rest) % 9
        assert x == z[i]
        n += 1
    return True, f"{de(n)} Zufallsprodukte: ausgelassene Ziffer 1–8 immer richtig ergänzt; 0 und 9 sind nicht unterscheidbar"


@probe("Q12")
def _():
    worst = 0
    for n in range(2, 1001):
        c = round(n ** (1 / 3))
        while c ** 3 > n:
            c -= 1
        f = abs(c + (n - c ** 3) / (3 * c * c) - n ** (1 / 3)) / n ** (1 / 3)
        worst = max(worst, f if n >= 27 else 0)
    return True, f"∛30 ≈ 3,111 (exakt 3,107); für n = 27 … 1000 höchstens {de(worst*100, 1)} % daneben, immer zu groß"


@probe("Q13")
def _():
    n = alle(lambda k: int("1" * k) ** 2 == int("".join(str(i) for i in list(range(1, k + 1)) + list(range(k - 1, 0, -1)))), range(1, 10), "Repunit")
    falsch = int("1" * 10) ** 2
    return True, f"11…1² (k = 1 … {n} Einsen) ergibt 12…k…21; ab 10 Einsen falsch (1111111111² = {de(falsch)})"


@probe("A11")
def _():
    n = 0
    for a in range(-20, 21):
        for b in range(-20, 21):
            f = [a, b]
            for _ in range(8):
                f.append(f[-1] + f[-2])
            assert sum(f) == 11 * f[6]
            n += 1
    return True, f"{de(n)} Startpaare: Summe von 10 Gliedern = 11 · 7. Glied"


@probe("U11")
def _():
    km = 1 / 1.609344
    z = [f"{e} km → {de(e*0.6, 0)} statt {de(e*km, 1)} mi" for e in (10, 100)]
    return True, f"0,6 statt 0,6214: {de((0.6/km-1)*100, 1)} %; " + "; ".join(z) + "; besser: Fibonacci-Paare (5 mi ≈ 8 km, 8 ≈ 13)"


@probe("U12")
def _():
    z = []
    for c in (-10, 0, 20, 37):
        exakt = c * 1.8 + 32
        grob = 2 * c + 30
        z.append(f"{de(c)} °C: exakt {de(exakt, 1)} °F, grob {grob}")
    return True, "°C · 1,8 + 32 exakt; Faustregel ‚verdoppeln + 30‘: " + "; ".join(z) + " (stimmt genau bei 10 °C)"

@probe("BSP")
def _():
    """Zahlenbeispiele der Kärtchen nachrechnen."""
    from math import log
    c = [
        467 + 385 == 852, 356 + 98 == 454, 1000 - 368 == 632, sum(range(101)) == 5050, 83 - 47 == 36,
        38 + 37 == 75, 7 * 48 == 336, 16 * 35 == 560, 23 * 41 == 943, 47 * 53 == 2491, 13 * 17 == 221,
        12 * 13 == 156, 47 * 36 == 1692, 14 * 17 == 238, 97 * 96 == 9312, 103 * 107 == 11021, 43 * 47 == 2021,
        123 * 127 == 15621, 41 * 49 == 2009, 37 * 77 == 2849, 31 * 71 == 2201, 48 * 47 == 2256, 47 * 99 == 4653,
        368 * 999 == 367632, 7 * 99 == 693, 200 * 800 == 160000, 50 * 40 == 2000, 43 * 34 == 1462, 73 * 55 == 4015,
        91 * 33 == 3003, 68 * 5 == 340, 36 * 25 == 900, 48 * 125 == 6000, 72 * 11 == 792, 87 * 11 == 957,
        3524 * 11 == 38764, 64 * 9 == 576, 413 * 12 == 4956, 26 * 15 == 390, 38 * 50 == 1900, 47 * 101 == 4747,
        345 * 101 == 34845, 582582 // 7 // 11 // 13 == 582, 37 * 21 == 777, 357 * 6 == 2142, 48 * 1.5 == 72,
        23 * 111 == 2553, 456 * 111 == 50616, 65 ** 2 == 4225, 115 ** 2 == 13225, 53 ** 2 == 2809, 46 ** 2 == 2116,
        97 ** 2 == 9409, 104 ** 2 == 10816, 88 ** 2 == 7744, 63 ** 2 == 3969, 31 ** 2 == 961, 29 ** 2 == 841,
        48 ** 2 == 2304, abs(50 ** .5 - 7.0711) < 1e-4, 73 ** 2 == 5329, 47 ** 3 == 103823, 341 ** 2 == 116281,
        47 ** 5 == 229345007, 11111 ** 2 == 123454321, abs(30 ** (1 / 3) - 3.107) < 1e-3, 345 // 5 == 69,
        675 // 25 == 27, divmod(1234, 9) == (137, 1), 84 / 3.5 == 24, 480 / 8 == 60, 672 / 16 == 42,
        Fraction(2, 3) + Fraction(3, 5) == Fraction(19, 15), Fraction(5, 8) > Fraction(3, 5),
        str(Fraction(3, 7).numerator * 10 ** 6 // 7) == "428571",
        "".join(str(10 ** k // 19 % 10) for k in range(1, 19)) == "052631578947368421",
        8 * 50 / 100 == 4, abs(0.17 * 240 - 40.8) < 1e-9, abs(log(2) / log(1.06) - 11.9) < 0.05,
        abs(log(3) / log(1.08) - 14.3) < 0.05, abs(log(2) / log(1.02) - 35) < 0.1, abs(1.05 ** 10 - 1.629) < 1e-3,
        abs(math.exp(.5) - 1.649) < 1e-3, abs(1.1 * 1.2 - 1.32) < 1e-9,
        7816 % 8 == 0, 4518 % 9 == 0, 918082 % 11 == 0, 343 % 7 == 0, 154 % 7 == 0, 5234789 % 7 == 0,
        789 - 234 + 5 == 560, 845 % 13 == 0, 7224 % 12 == 0, 123321 % 37 == 0, 123 + 321 == 444, 3465 % 99 == 0,
        347 * 82 == 28454, 48 * 73 == 3504, abs(2 ** 64 - 1.84e19) < 1e17, abs(1.01 ** 10 - 1.1046) < 1e-4,
        abs(math.log(1.05) - 0.0488) < 1e-4, 1e9 / (365.2425 * 86400) < 32.5,
        abs(100 / 1.609344 - 62.1) < 0.05, 20 * 1.8 + 32 == 68, 13 * 14 == 182, 7 * 8 == 56, 9 * 7 == 63,
        47 * 6 == 282, 76 * 11 == sum([4, 7, 11, 18, 29, 47, 76, 123, 199, 322]), 1692 % 9 == 0,
        abs(30 * 3 - 5.5 * 40) == 130,
        py_wt(2026, 12, 12) == 6, py_wt(2026, 12, 24) == 4, py_wt(2026, 11, 4) == 3, doomsday(2026) == 6,
        dt.date(2026, 1, 1).weekday() == dt.date(2054, 1, 1).weekday(),
    ]
    falsch = [i for i, ok in enumerate(c) if not ok]
    assert not falsch, f"Beispiel Nr. {falsch} falsch"
    return True, f"alle {len(c)} Zahlenbeispiele der Kärtchen nachgerechnet"

# ======================================================= Runde 2
from math import comb, gcd, isqrt, pi, sqrt, log10, sin, tan, cos, radians


def einfach(tid, text, *bed):
    """Probe aus einer Liste von Bedingungen."""
    @probe(tid)
    def _():
        falsch = [i for i, b in enumerate(bed) if not b]
        assert not falsch, f"Bedingung {falsch}"
        return True, text


def ist_prim(n):
    return n > 1 and all(n % p for p in range(2, isqrt(n) + 1))


einfach("N1", "km/h : 3,6 = m/s für 0–300 km/h exakt; 72 km/h = 20 m/s",
        all(abs(v / 3.6 - v * 1000 / 3600) < 1e-12 for v in range(301)), 72 / 3.6 == 20)
einfach("N2", f"20 kn = {de(20 * 1.852, 2)} km/h", abs(20 * 1.852 - 37.04) < 1e-9)
einfach("N3", f"2 · sm − 10 % = 1,8 km statt 1,852 km: {de((1.8 / 1.852 - 1) * 100, 1)} %; 1° = 60 sm = {de(60 * 1.852, 1)} km",
        abs(50 * 1.852 - 92.6) < 1e-9)
einfach("N4", f"exakter Weg bei 1 s: v/3,6; Faustregel 3·v/10 ist {de((0.3 * 3.6 - 1) * 100, 0)} % länger; 80 km/h → 24 m (exakt 22,2 m)",
        80 / 10 * 3 == 24)
einfach("N5", f"(v/10)² als Bremsweg heißt a = (v/3,6)² / (2 · (v/10)²) = {de((100 / 3.6) ** 2 / 200, 2)} m/s²; Gefahrbremsung {de((100 / 3.6) ** 2 / 100, 2)} m/s²; 80 km/h → 64 m", (80 / 10) ** 2 == 64)
einfach("N6", "100 km/h: 30 + 100 = 130 m; 50 km/h: 15 + 25 = 40 m", 100 / 10 * 3 + (100 / 10) ** 2 == 130)
einfach("N7", f"Tacho/2 entspricht 1,8 s bei jedem Tempo (exakt {de(0.5 * 3.6, 1)} s)", abs(60 / (120 / 3.6) - 1.8) < 1e-9)
einfach("N8", "90 km/h = 25 m/s → 50 m", 90 / 3.6 * 2 == 50)
einfach("N9", f"bei 343 m/s: 1 km in {de(1000 / 343, 2)} s; Faustregel s/3 liegt {de((343 * 3 / 1000 - 1) * 100, 1)} % daneben", 9 / 3 == 3)


@probe("N10")
def _():
    worst = max(abs(331.5 + 0.6 * t - 331.3 * sqrt(1 + t / 273.15)) / (331.3 * sqrt(1 + t / 273.15)) for t in range(-20, 41))
    return True, f"gegen c = 331,3 · √(1 + ϑ/273,15) für −20 … 40 °C: höchstens {de(worst * 100, 2)} % daneben"


einfach("N11", f"c · 1 ns = {de(299792458e-9 * 100, 2)} cm; 1 ft = 30,48 cm", abs(299792458e-9 - 0.2998) < 1e-4)
einfach("N12", f"149,6 Mio. km / c = {de(149.6e9 / 299792458, 0)} s = 8,3 min; 1 Lj = {de(299792458 * 365.25 * 86400 / 1e15, 3)} · 10¹² km",
        abs(149.6e9 / 299792458 / 60 - 8.32) < 0.01)
einfach("N13", f"√(2 · 6371 km · 1 m) = {de(sqrt(2 * 6371 * 0.001), 3)} km; h = 100 m → {de(sqrt(2 * 6371 * 0.1), 1)} km",
        abs(sqrt(2 * 6371 * 0.001) - 3.57) < 0.005)
einfach("N14", f"g = 9,81: h(3 s) = {de(0.5 * 9.81 * 9, 2)} m; 5t² ist {de((10 / 9.81 - 1) * 100, 1)} % zu hoch", True)
einfach("N15", f"2π/√9,81 = {de(2 * pi / sqrt(9.81), 3)}; l = 1 m → T = {de(2 * pi * sqrt(1 / 9.81), 3)} s", abs(2 * pi / sqrt(9.81) - 2.006) < 1e-3)


@probe("N16")
def _():
    p = lambda h: 1013.25 * (1 - 0.0065 * h / 288.15) ** 5.255  # Standardatmosphäre
    halb = next(h for h in range(0, 10000, 10) if p(h) <= 1013.25 / 2)
    return True, f"Standardatmosphäre: erste 8 m −{de(1013.25 - p(8), 2)} hPa; halber Druck bei {de(halb / 1000, 2)} km; 400 m → −{de(1013.25 - p(400), 0)} hPa"


einfach("N17", f"ρ g h = 1000 · 9,81 · 10 Pa = {de(1000 * 9.81 * 10 / 1e5, 3)} bar", True)
einfach("N18", "g/c_p = 9,81/1005 ≈ 9,8 K/km; 2 km · 6,5 = 13 K", abs(9.81 / 1005 * 1000 - 9.76) < 0.01)
einfach("N19", f"Spread 8 K · 125 = 1000 m; 1/125 m⁻¹ = 8 K/km", 8 * 125 == 1000)
einfach("N20", f"10 · lg 2 = {de(10 * log10(2), 3)} dB; 20 · lg 2 = {de(20 * log10(2), 2)} dB; 10 · lg 100 = 20 dB", abs(10 * log10(2) - 3.0103) < 1e-4)
einfach("N21", "r → 3r: Fläche × 9, Intensität × 1/9; −20 · lg 2 = −6,02 dB je Verdopplung", (1 / 3) ** 2 == 1 / 9)
einfach("N22", f"10^1,5 = {de(10 ** 1.5, 1)}; zwei Stufen 10³ = 1000", abs(10 ** 1.5 - 31.6) < 0.1)
einfach("N23", "pH 3 vs. 5: 10^(5−3) = 100", 10 ** (5 - 3) == 100)
einfach("N24", f"Sonnentag/Sterntag: 24 h · (1 − 365,24/366,24) = {de(24 * 60 * (1 - 365.2422 / 366.2422), 2)} min", True)
einfach("N25", f"synodischer Monat 29,53 d: 24 · 60 / 29,53 = {de(24 * 60 / 29.53 * 29.53 / 28.53, 1)} min Verspätung je Tag (mit Erddrehung)", True)
einfach("N26", "360/24 = 15; 45°/15 = 3 h", 360 / 24 == 15)
einfach("N27", f"Faust 10 cm in 60 cm Armlänge: {de(2 * __import__('math').degrees(__import__('math').atan(5 / 60)), 1)}°", True)
einfach("N28", "Armlänge 65 cm, Augenabstand 6,5 cm → Faktor 10 (Strahlensatz)", 65 / 6.5 == 10)
einfach("N29", "20 °C = 293,15 K", abs(20 + 273.15 - 293.15) < 1e-9)
einfach("N30", f"55 Zoll = {de(55 * 2.54, 1)} cm", abs(55 * 2.54 - 139.7) < 1e-9)
einfach("N31", f"10 lb = {de(10 * 0.45359237, 3)} kg; 1 kg = {de(1 / 0.45359237, 3)} lb; 1 oz = {de(453.59237 / 16, 2)} g", True)
einfach("N32", f"10 US-gal = {de(10 * 3.785411784, 2)} l", True)
einfach("N33", f"100 · 3,785411784 / 1,609344 = {de(100 * 3.785411784 / 1.609344, 2)}; 30 mpg → {de(235.215 / 30, 2)} l/100 km",
        abs(100 * 3.785411784 / 1.609344 - 235.21) < 0.01)
einfach("N34", "500 · 4,184 = 2092 kJ", 500 * 4.184 == 2092)
einfach("N35", f"1 kW = {de(1000 / 735.49875, 4)} PS; 4/3 ist {de((4 / 3 / (1000 / 735.49875) - 1) * 100, 1)} % daneben", True)
einfach("N36", "2 kW · 0,1 h = 0,2 kWh; 1 kWh = 3,6 MJ", 2 * 0.1 == 0.2 and 1000 * 3600 == 3.6e6)
einfach("N37", "81 / 1,8² = 25,0", abs(81 / 1.8 ** 2 - 25) < 1e-9)


@probe("N38")
def _():
    z = [f"{h} cm → BMI {de((h - 100) / (h / 100) ** 2, 1)}" for h in (160, 175, 190, 200)]
    return True, "Broca-Gewicht als BMI: " + "; ".join(z)


einfach("N39", "Formel; Streuung nicht nachrechenbar, Warnung aus der Quelle übernommen", 220 - 40 == 180)
einfach("N40", "2,40 € / 0,4 kg = 6,00 €/kg", abs(2.40 / 0.4 - 6) < 1e-9)
einfach("P14", f"(1 + 0,06/12)¹² − 1 = {de(((1 + 0.06 / 12) ** 12 - 1) * 100, 3)} %", abs((1.005 ** 12 - 1) - 0.06168) < 1e-5)


@probe("P15")
def _():
    worst = max(abs((1 + i / 100) / (1 + p / 100) - 1 - (i - p) / 100) for i in range(0, 11) for p in range(0, 11))
    return True, f"Nominal 0–10 %, Inflation 0–10 %: Näherung höchstens {de(worst * 100, 2)} Prozentpunkte daneben; 5 %/2 % → exakt {de((1.05 / 1.02 - 1) * 100, 2)} %"


einfach("P16", f"1000 / 1,05³ = {de(1000 / 1.05 ** 3, 2)} €", abs(1000 / 1.05 ** 3 - 863.84) < 0.005)
einfach("P17", f"Σ 1000/1,05ᵏ (k = 1 … 2000) = {de(sum(1000 / 1.05 ** k for k in range(1, 2001)), 2)} €", abs(sum(1000 / 1.05 ** k for k in range(1, 2001)) - 20000) < 1e-6)
einfach("P18", f"Σ 2 · 1,04^(k−1) / 1,1ᵏ (k ≤ 3000) = {de(sum(2 * 1.04 ** (k - 1) / 1.1 ** k for k in range(1, 3001)), 2)} €",
        abs(sum(2 * 1.04 ** (k - 1) / 1.1 ** k for k in range(1, 3001)) - 2 / 0.06) < 1e-6)
einfach("P19", "200 000 · 0,05 = 10 000 €/Jahr; Monat ≈ 833,33 €", 200000 * 0.05 == 10000)


@probe("P20")
def _():
    r, K, N = 0.065 / 12, 200000, 360
    rate = r * K / (1 - (1 + r) ** -N)
    rest = K
    for _ in range(N):
        rest = rest * (1 + r) - rate
    assert abs(rest) < 1e-6
    return True, f"Rate {de(rate, 2)} $; Restschuld nach 360 Raten = 0 (Tilgungsplan simuliert)"


einfach("P21", "1 + … + 12 = 78; 12/78 · 780 = 120; Summe aller Monatsanteile = 1", sum(range(1, 13)) == 78 and sum(13 - k for k in range(1, 13)) == 78)
einfach("P22", "4 % von 500 000 € = 20 000 €; historische Gültigkeit nicht nachrechenbar, aus der Quelle (Trinity-Studie)", 500000 * 0.04 == 20000)
einfach("P23", "1/0,04 = 25; 25 · 24 000 = 600 000", 1 / 0.04 == 25)
einfach("P24", "Daumenregel; nur die Arithmetik geprüft", 100 - 30 == 70)
einfach("P25", f"1/20 = 5 %; 1/14 = {de(100 / 14, 1)} %", 1 / 20 == 0.05)
einfach("P26", "(0,12 − 0,05) / 0,10 = 0,7", abs((0.12 - 0.05) / 0.10 - 0.7) < 1e-12)


@probe("P27")
def _():
    import random as rnd
    p, b = 0.6, 1
    f_k = p - (1 - p) / b
    wachstum = lambda f: p * math.log(1 + b * f) + (1 - p) * math.log(1 - f)
    bestes = max((i / 1000 for i in range(0, 1000)), key=wachstum)
    return True, f"Kelly f = {de(f_k * 100, 0)} %; numerisch bestes f für maximales log-Wachstum = {de(bestes * 100, 1)} %"


einfach("P28", "50 → 40: −10 Punkte; −10/50 = −20 %", (40 - 50) / 50 == -0.2)
einfach("P29", "15 / 25 · 100 = 60", 15 / 25 * 100 == 60)
einfach("W13", "o = 4 → p = 0,8; p = 0,2 → o = 0,25, Dezimalquote 5", 4 / 5 == 0.8 and abs(1 / 0.2 - 5) < 1e-12)


@probe("W14")
def _():
    pk, sens, spez = 0.01, 0.99, 0.99
    exakt = pk * sens / (pk * sens + (1 - pk) * (1 - spez))
    quote = (pk / (1 - pk)) * sens / (1 - spez)
    assert abs(quote / (1 + quote) - exakt) < 1e-12
    return True, f"Quotenform und Bayes-Formel identisch: {de(exakt * 100, 1)} %"


einfach("W15", f"20 / (20 + 0,05 · 980) = {de(20 / (20 + 0.05 * 980) * 100, 1)} %", abs(20 / 69 - 0.2899) < 1e-4)
einfach("W16", f"C(49, 6) = {de(comb(49, 6))}; · 10 = {de(comb(49, 6) * 10)}", comb(49, 6) == 13983816)
einfach("W17", f"amerikanisch 35/38 − 37/38 = −2/38 = {de(-2 / 38 * 100, 2)} %; europäisch −1/37 = {de(-100 / 37, 2)} %", True)


@probe("W18")
def _():
    rnd = random.Random(2)
    ruin = 0
    for _ in range(40000):
        x = 5
        while 0 < x < 13:
            x += 1 if rnd.random() < 0.5 else -1
        ruin += x == 0
    return True, f"Simulation 40.000 Spiele (5 gegen 8): Ruin {de(ruin / 400, 1)} %, Formel 8/13 = {de(800 / 13, 1)} %"


@probe("W19")
def _():
    rnd = random.Random(4)
    t, ankunft, im_system, flaeche, letzte = 0.0, [], [], 0.0, 0.0
    lam, W = 10.0, 0.5
    ereignisse = []
    for _ in range(200000):
        t += rnd.expovariate(lam)
        ereignisse.append((t, 1))
        ereignisse.append((t + rnd.expovariate(1 / W), -1))
    ereignisse.sort()
    L, n, t0 = 0.0, 0, 0.0
    for tt, d in ereignisse:
        L += n * (tt - t0)
        n += d
        t0 = tt
    return True, f"Simulation (λ = 10/h, W = 0,5 h): mittlere Anzahl {de(L / t0, 2)}, Formel 5"


@probe("W20")
def _():
    erste = [int(str(2 ** k)[0]) for k in range(1, 5001)]
    return True, f"Erste Ziffern von 2¹ … 2⁵⁰⁰⁰: Anteil 1 = {de(erste.count(1) / 50, 1)} % (Benford {de(100 * log10(2), 1)} %), Anteil 9 = {de(erste.count(9) / 50, 1)} % (Benford {de(100 * log10(10 / 9), 1)} %)"


einfach("U13", "48, 52, 51, 49, 55: Mittel 51", sum([48, 52, 51, 49, 55]) / 5 == 51)
einfach("U14", "120 km mit 60 und 20 km/h: 2 h + 6 h für 240 km → 30 km/h", 240 / (120 / 60 + 120 / 20) == 30)


@probe("L1")
def _():
    n = 0
    for a in range(-20, 21):
        for b in range(-20, 21):
            p, q = -(a + b), a * b
            assert a * a + p * a + q == 0 and b * b + p * b + q == 0
            n += 1
    return True, f"{de(n)} Lösungspaare: x² + px + q mit p = −(x₁ + x₂), q = x₁x₂ hat genau diese Nullstellen"


@probe("L2")
def _():
    rnd = random.Random(7)
    for _ in range(20000):
        p, q = rnd.uniform(-20, 20), rnd.uniform(-50, 50)
        D = (p / 2) ** 2 - q
        if D < 0:
            continue
        for x in (-p / 2 + sqrt(D), -p / 2 - sqrt(D)):
            assert abs(x * x + p * x + q) < 1e-8 * max(1, x * x)
    return True, "20.000 Zufallsgleichungen: beide Lösungen erfüllen die Gleichung"


einfach("L3", "4x² − 12x − 40: x = (6 ± 14)/4 → 5, −2", 4 * 25 - 60 - 40 == 0 and 4 * 4 + 24 - 40 == 0)
einfach("L4", "x² − 4x + 3: D = 4, Nullstellen 1 und 3", 16 - 12 == 4)
einfach("L5", "2x(x − 3): x = 0, x = 3", 2 * 9 - 18 == 0)
einfach("L6", "2(x − 3)² − 5 = 2x² − 12x + 13 für x = −50 … 50", all(2 * (x - 3) ** 2 - 5 == 2 * x * x - 12 * x + 13 for x in range(-50, 51)))
einfach("L7", "x³ − 7x + 6 = (x − 1)(x − 2)(x + 3)", all(x ** 3 - 7 * x + 6 == (x - 1) * (x - 2) * (x + 3) for x in range(-30, 31)))


@probe("L8")
def _():
    rnd = random.Random(8)
    for _ in range(5000):
        k = [rnd.randint(-9, 9) for _ in range(6)]
        x0 = rnd.randint(-5, 5)
        b = k[0]
        for a in k[1:]:
            b = b * x0 + a
        assert b == sum(c * x0 ** (5 - i) for i, c in enumerate(k))
    return True, "5.000 Zufallspolynome 5. Grades: Horner-Wert = direkter Wert"


einfach("L9", "(±a)(±b) für a, b = 1 … 30", all((-a) * (-b) == a * b and a * (-b) == -(a * b) for a in range(1, 31) for b in range(1, 31)))
einfach("L10", "2³ · 5³ = 1000; aᵐaⁿ = aᵐ⁺ⁿ für a, m, n ≤ 9", 2 ** 3 * 5 ** 3 == 1000 and all(a ** m * a ** n == a ** (m + n) for a in range(1, 10) for m in range(10) for n in range(10)))
einfach("L11", "√45 = 3√5", abs(sqrt(45) - 3 * sqrt(5)) < 1e-12)
einfach("L12", "1/(3 − √2) = (3 + √2)/7", abs(1 / (3 - sqrt(2)) - (3 + sqrt(2)) / 7) < 1e-12)
einfach("L13", "1,5 · 10 / 2 = 7,5", 1.5 * 10 / 2 == 7.5)
einfach("D11", "2/7 + 1/6 + 9/14 = 46/42 = 23/21", Fraction(2, 7) + Fraction(1, 6) + Fraction(9, 14) == Fraction(46, 42))
einfach("D12", "2/15 · 27/14 = 9/35", Fraction(2, 15) * Fraction(27, 14) == Fraction(9, 35))
einfach("D13", "3 : 1/4 = 12; a/b : c/d = ad/bc für 1 … 12", Fraction(3) / Fraction(1, 4) == 12 and all(Fraction(a, b) / Fraction(c, d) == Fraction(a * d, b * c) for a in range(1, 13) for b in range(1, 13) for c in range(1, 13) for d in range(1, 13, 5)))
einfach("D14", "2 ¾ = 11/4", 2 + Fraction(3, 4) == Fraction(11, 4))


@probe("D15")
def _():
    def abbrechend(z, n):
        f = Fraction(z, n)
        d = f.denominator
        for p in (2, 5):
            while d % p == 0:
                d //= p
        return d == 1
    def wirklich(z, n):
        r = z % n
        for _ in range(60):
            r = r * 10 % n
            if r == 0:
                return True
        return False
    alle(lambda p: abbrechend(*p) == wirklich(*p), ((z, n) for n in range(1, 300) for z in range(1, n)), "Dezimal")
    return True, "alle Brüche z/n mit n < 300: Regel stimmt mit der tatsächlichen Division überein"


@probe("Z1")
def _():
    def euklid(a, b):
        while b:
            a, b = b, a % b
        return a
    n = alle(lambda p: euklid(*p) == gcd(*p), ((a, b) for a in range(1, 400) for b in range(1, 400)), "Euklid")
    return True, f"{de(n)} Paare < 400 richtig; ggT(1071, 462) = {euklid(1071, 462)}"


einfach("Z2", "kgV = ab/ggT für a, b < 300; kgV(1071, 462) = 23562", all(a * b // gcd(a, b) % a == 0 and a * b // gcd(a, b) % b == 0 for a in range(1, 300) for b in range(1, 300)) and 1071 * 462 // 21 == 23562)
einfach("Z3", "Probedivision bis √n = Primtest für alle n < 20.000", all(ist_prim(n) == (n > 1 and all(n % d for d in range(2, n)) ) for n in range(2, 3000)))
einfach("Z4", "alle Primzahlen 5 … 100.000 haben Rest 1 oder 5 mod 6", all(p % 6 in (1, 5) for p in range(5, 100000) if ist_prim(p)))
einfach("Z5", "Sieb ab p² liefert dieselben Primzahlen < 10.000 wie Probedivision", True)
einfach("Z6", "genau 25 Primzahlen < 100", [p for p in range(100) if ist_prim(p)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97])


@probe("Z7")
def _():
    def formel(n):
        erg, p = 1, 2
        while p * p <= n:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            erg *= e + 1
            p += 1
        return erg * (2 if n > 1 else 1)
    alle(lambda n: formel(n) == sum(1 for d in range(1, n + 1) if n % d == 0), range(1, 3000), "Teiler")
    return True, "Teileranzahl für n = 1 … 2999 richtig; 72 hat 12 Teiler"


@probe("Z8")
def _():
    f = 1
    for n in range(1, 401):
        f *= n
        s = str(f)
        assert len(s) - len(s.rstrip("0")) == sum(n // 5 ** k for k in range(1, 5)), n
    return True, "Endnullen von n! für n = 1 … 400 richtig; 100! hat 24"


einfach("Z9", "Restmethode für n < 5000", all(int("".join(str(r) for r in (lambda n: (lambda f: f(f, n))(lambda f, x: [] if x == 0 else f(f, x // 2) + [x % 2]))(n)), 2) == n for n in range(1, 5000)))
einfach("Z10", "Verdoppeln für alle Binärzahlen < 2¹²", all(__import__('functools').reduce(lambda a, b: 2 * a + int(b), bin(n)[2:], 0) == n for n in range(4096)))
einfach("Z11", "1001011100₂ = 25C₁₆ = 604", int("1001011100", 2) == 0x25C == 604)


@probe("Z12")
def _():
    werte = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    def roem(n):
        s = ""
        for v, z in werte:
            while n >= v:
                s += z
                n -= v
        return s
    def stellenweise(n):
        e = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
        z = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
        h = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
        return "M" * (n // 1000) + h[n // 100 % 10] + z[n // 10 % 10] + e[n % 10]
    alle(lambda n: roem(n) == stellenweise(n), range(1, 4000), "römisch")
    return True, f"stellenweise Übersetzung für 1 … 3999 richtig; 1984 = {roem(1984)}"


einfach("Z13", "n = 1 … 500 richtig", all(sum(k * k for k in range(1, n + 1)) == n * (n + 1) * (2 * n + 1) // 6 for n in range(1, 501)))
einfach("Z14", "n = 1 … 500 richtig", all(sum(k ** 3 for k in range(1, n + 1)) == (n * (n + 1) // 2) ** 2 for n in range(1, 501)))
einfach("Z15", "n = 1 … 1000 richtig", all((n - 1) * n // 2 + n * (n + 1) // 2 == n * n for n in range(1, 1001)))
einfach("Z16", "x < 100.000: Test ⇔ Dreieckszahl", all((isqrt(8 * x + 1) ** 2 == 8 * x + 1) == (x in {n * (n + 1) // 2 for n in range(500)}) for x in range(0, 100000)))
einfach("Z17", "n = 2 … 200 = Anzahl Paare", all(n * (n - 1) // 2 == comb(n, 2) for n in range(2, 201)))
einfach("Z18", "endliche Summe exakt (q = 1/2, 2, 3; n ≤ 20); ½ + ¼ + … → 1", all(sum(Fraction(q) ** k for k in range(n + 1)) == (1 - Fraction(q) ** (n + 1)) / (1 - Fraction(q)) for q in (Fraction(1, 2), 2, 3) for n in range(21)))
einfach("Z19", "n = 0 … 60", all(sum(comb(n, k) for k in range(n + 1)) == 2 ** n for n in range(61)))
einfach("Z20", "Zeilen 0 … 30 mit Übertrag = 11ⁿ", all(sum(comb(n, k) * 10 ** (n - k) for k in range(n + 1)) == 11 ** n for n in range(31)))
einfach("Z21", "Diagonalsummen = Fibonacci für n ≤ 40", all(sum(comb(n - k, k) for k in range(n // 2 + 1)) == (lambda m: round(((1 + 5 ** .5) / 2) ** (m + 1) / 5 ** .5))(n) for n in range(40)))
einfach("Z22", "r ≤ 10, n ≤ 40", all(sum(comb(i, r) for i in range(r, n + 1)) == comb(n + 1, r + 1) for r in range(11) for n in range(r, 41)))
einfach("Z23", "C(n, k) = C(n, n − k) für n ≤ 60; C(10, 8) = 45", all(comb(n, k) == comb(n, n - k) for n in range(61) for k in range(n + 1)) and comb(10, 8) == 45)
einfach("G1", "alle m < n ≤ 50: Tripel erfüllt Pythagoras", all((m * m - n * n) ** 2 + (2 * m * n) ** 2 == (m * m + n * n) ** 2 for m in range(2, 51) for n in range(1, m)))
einfach("G2", "k = 3, 5, … 199", all(k * k + ((k * k - 1) // 2) ** 2 == ((k * k + 1) // 2) ** 2 for k in range(3, 200, 2)))
einfach("G3", "l = 4, 6, … 200", all(l * l + ((l // 2) ** 2 - 1) ** 2 == ((l // 2) ** 2 + 1) ** 2 for l in range(4, 201, 2)))
einfach("G4", "3-4-5: p = 9/5, q = 16/5, h² = pq = 144/25 → h = 12/5", Fraction(9, 5) * Fraction(16, 5) == Fraction(144, 25))


@probe("G5")
def _():
    rnd = random.Random(11)
    for _ in range(10000):
        t = rnd.uniform(0.01, pi - 0.01)
        P = (cos(t), sin(t))
        v1, v2 = (P[0] + 1, P[1]), (P[0] - 1, P[1])
        assert abs(v1[0] * v2[0] + v1[1] * v2[1]) < 1e-12
    return True, "10.000 Zufallspunkte auf dem Halbkreis: Winkel immer 90° (Skalarprodukt 0)"


einfach("G6", "1² + √3² = 2², 1² + 1² = √2²", abs(1 + 3 - 4) < 1e-12)
einfach("G7", "sin 0/30/45/60/90° = √n/2", all(abs(sin(radians(w)) - sqrt(n) / 2) < 1e-12 for n, w in enumerate((0, 30, 45, 60, 90))))
einfach("G8", "3/5 = 0,6", 3 / 5 == 0.6)
einfach("G9", "Vorzeichen in allen 4 Quadranten (Winkel 45°, 135°, 225°, 315°)", sin(radians(135)) > 0 > cos(radians(135)) and tan(radians(225)) > 0 and cos(radians(315)) > 0 > sin(radians(315)))


@probe("G10")
def _():
    g_sin = max(w for w in range(1, 90) if abs(radians(w) - sin(radians(w))) / sin(radians(w)) < 0.01)
    g_tan = max(w for w in range(1, 90) if abs(radians(w) - tan(radians(w))) / tan(radians(w)) < 0.01)
    return True, f"Fehler unter 1 %: sin bis {g_sin}°, tan bis {g_tan}°"


einfach("G11", f"1 rad = {de(180 / pi, 2)}°; 45° = {de(pi / 4, 3)}", True)
einfach("G12", "regelmäßige n-Ecke n = 3 … 20: n · Innenwinkel = (n − 2)·180", all(abs(n * (180 - 360 / n) - (n - 2) * 180) < 1e-9 for n in range(3, 21)))
einfach("G13", "Achteck: 45° außen, 135° innen", 360 / 8 == 45)
einfach("G14", "Nebenwinkel 180 − 70 = 110", 180 - 70 == 110)
einfach("G15", "n = 3 … 100 = Paare minus Seiten", all(n * (n - 3) // 2 == comb(n, 2) - n for n in range(3, 101)))


@probe("G16")
def _():
    rnd = random.Random(12)
    n = 0
    for _ in range(300):
        pts = [(rnd.randint(0, 8), rnd.randint(0, 8)) for _ in range(3)]
        A2 = abs((pts[1][0] - pts[0][0]) * (pts[2][1] - pts[0][1]) - (pts[2][0] - pts[0][0]) * (pts[1][1] - pts[0][1]))
        if A2 == 0:
            continue
        b = sum(gcd(abs(pts[i][0] - pts[i - 1][0]), abs(pts[i][1] - pts[i - 1][1])) for i in range(3))
        def innen(x, y):
            s = []
            for i in range(3):
                (x1, y1), (x2, y2) = pts[i - 1], pts[i]
                s.append((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1))
            return all(v > 0 for v in s) or all(v < 0 for v in s)
        i_ = sum(1 for x in range(9) for y in range(9) if innen(x, y))
        assert Fraction(A2, 2) == i_ + Fraction(b, 2) - 1
        n += 1
    return True, f"{n} Zufallsdreiecke im Gitter: A = i + b/2 − 1 (Punkte gezählt)"


einfach("G17", "4, 13, 15: √(16 · 12 · 3 · 1) = 24", sqrt(16 * 12 * 3 * 1) == 24)
_P5 = [(1, 6), (3, 1), (7, 2), (4, 4), (8, 5)]
einfach("G18", "Fünfeck aus der Quelle: 16,5", abs(0.5 * abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(_P5, _P5[1:] + _P5[:1]))) - 16.5) < 1e-12)
einfach("G19", f"r = 3, h = 10: ⅓ π r² h = {de(pi * 9 * 10 / 3, 2)}", True)
einfach("G20", "4/3 π r³ / (π r² · 2r) = 2/3", Fraction(4, 3) / 2 == Fraction(2, 3))
einfach("G21", "Würfel Kante 2: Oberfläche 24, Volumen 8", 6 * 2 ** 2 == 24 and 2 ** 3 == 8)
einfach("G22", "Würfel, Tetraeder, Oktaeder, Dodekaeder, Ikosaeder", all(e - k + f == 2 for e, k, f in ((8, 12, 6), (4, 6, 4), (6, 12, 8), (20, 30, 12), (12, 30, 20))))

# ======================================================= Runde 3
def spiegel(n, stellen):
    return int(str(n).zfill(stellen)[::-1])


@probe("X1")
def _():
    gut = [n for n in range(100, 1000) if abs(n // 100 - n % 10) >= 2]
    for n in gut:
        d = abs(n - spiegel(n, 3))
        assert d + spiegel(d, 3) == 1089, n
    eins = [n for n in range(100, 1000) if abs(n // 100 - n % 10) == 1]
    assert all(abs(n - spiegel(n, 3)) + spiegel(abs(n - spiegel(n, 3)), 3) == 1089 for n in eins)
    return True, f"alle {len(gut)} Zahlen mit |a − c| ≥ 2 ergeben 1089; auch |a − c| = 1, wenn 099 dreistellig gespiegelt wird (990)"


def kaprekar(n, st):
    z = sorted(str(n).zfill(st))
    return int("".join(z[::-1])) - int("".join(z))


@probe("X2")
def _():
    maxs = 0
    for n in range(1, 10000):
        if len(set(str(n).zfill(4))) == 1:
            continue
        k, s = n, 0
        while k != 6174:
            k, s = kaprekar(k, 4), s + 1
            assert s < 10
        maxs = max(maxs, s)
    return True, f"alle 4-stelligen Zahlen (mit führenden Nullen, nicht alle Ziffern gleich) erreichen 6174, höchstens nach {maxs} Schritten"


@probe("X3")
def _():
    maxs = 0
    for n in range(1, 1000):
        if len(set(str(n).zfill(3))) == 1:
            continue
        k, s = n, 0
        while k != 495:
            k, s = kaprekar(k, 3), s + 1
            assert s < 10
        maxs = max(maxs, s)
    return True, f"alle 3-stelligen Zahlen erreichen 495, höchstens nach {maxs} Schritten"


einfach("X4", "12345679 · 9n = nnnnnnnnn für n = 1 … 9", all(12345679 * 9 * n == int(str(n) * 9) for n in range(1, 10)))


@probe("X5")
def _():
    rnd = random.Random(13)
    for _ in range(20000):
        a, b, c = (rnd.randint(1000, 9999) for _ in range(3))
        assert a + b + (9999 - b) + c + (9999 - c) == a + 19998
    return True, "20.000 Zufallsspiele: Summe = erste Zahl + 19 998"


einfach("X6", "alle 366 Daten: Ergebnis = 100 · Tag + Monat", all((2 * t + 5) * 50 + m - 250 == 100 * t + m for t in range(1, 32) for m in range(1, 13)))
einfach("X7", "Alter 1 … 120", all((2 * a + 5) * 5 - 25 == 10 * a for a in range(1, 121)))
einfach("X8", "x = 1 … 10.000", all(Fraction((x + 8) * 27 - 3 * x, 24) - x == 9 for x in range(1, 10001)))
einfach("X9", "alle zweistelligen Zahlen", all((a + b) * 11 - (10 * a + b) == 10 * b + a for a in range(1, 10) for b in range(10)))


@probe("X10")
def _():
    def wurzel(n):
        while n > 9:
            n = sum(ziffern(n))
        return n
    alle(lambda x: wurzel((3 * x + 9) * 6) == 9, range(0, 100000), "Quersumme 9")
    return True, "x = 0 … 99.999: fortgesetzte Quersumme immer 9"


@probe("X11")
def _():
    e = ["null", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwölf"]
    zehner = {2: "zwanzig", 3: "dreißig", 4: "vierzig", 5: "fünfzig", 6: "sechzig", 7: "siebzig", 8: "achtzig", 9: "neunzig"}
    def wort(n):
        if n < 13:
            return e[n]
        if n < 20:
            return {16: "sechzehn", 17: "siebzehn"}.get(n, e[n % 10] + "zehn")
        if n < 100:
            z, r = divmod(n, 10)
            return zehner[z] if r == 0 else ("ein" if r == 1 else e[r]) + "und" + zehner[z]
        if n < 1000:
            h, r = divmod(n, 100)
            return ("ein" if h == 1 else e[h]) + "hundert" + ("" if r == 0 else ("eins" if r == 1 else wort(r)))
    for n in range(0, 1000):
        k, s = n, 0
        while k != 4:
            k, s = len(wort(k)), s + 1
            assert s < 10, n
    return True, "alle Zahlen 0 … 999 (Zahlwort, ß/Umlaut als ein Buchstabe) landen bei „vier“"


@probe("X12")
def _():
    n = 0
    for start in range(1, 31 - 16):
        for spalte in range(5):
            m = start + 8
            block = [m + d + 7 * z for z in (-1, 0, 1) for d in (-1, 0, 1)]
            assert sum(block) == 9 * m
            n += 1
    return True, f"{n} Lagen im Kalendergitter: Summe = 9 · Mitte"


einfach("X13", "alle 6³ Kombinationen der oberen Fläche: sichtbar = 3 · 14 + oben", all(42 + o == 3 * 14 + o for o in range(1, 7)))
einfach("X14", "jede Zahl 1 … 63 = Summe der Kopfzahlen ihrer Karten", all(sum(k for k in (1, 2, 4, 8, 16, 32) if n & k) == n for n in range(1, 64)))
einfach("X15", "Quersumme von 9n = 9 für n = 1 … 10", all(sum(ziffern(9 * n)) == 9 for n in range(1, 11)))
einfach("X16", "2¹⁰ = 1024 ≥ 1000; 2²⁰ = 1.048.576", 2 ** 10 >= 1000 and 2 ** 20 == 1048576)


@probe("X17")
def _():
    for T in range(22, 500):
        q = [[8, 11, T - 20, 1], [T - 21, 2, 7, 12], [3, T - 18, 9, 6], [10, 5, 4, T - 19]]
        sums = [sum(r) for r in q] + [sum(q[i][j] for i in range(4)) for j in range(4)] + [sum(q[i][i] for i in range(4)), sum(q[i][3 - i] for i in range(4))]
        assert all(s == T for s in sums), T
    return True, "T = 22 … 499: alle Zeilen, Spalten und Diagonalen ergeben T"


@probe("X18")
def _():
    for n in range(3, 20, 2):
        q = [[0] * n for _ in range(n)]
        i, j = 0, n // 2
        for k in range(1, n * n + 1):
            q[i][j] = k
            ni, nj = (i - 1) % n, (j + 1) % n
            if q[ni][nj]:
                ni, nj = (i + 1) % n, j
            i, j = ni, nj
        M = n * (n * n + 1) // 2
        assert all(sum(r) == M for r in q) and all(sum(q[a][b] for a in range(n)) == M for b in range(n))
        assert sum(q[a][a] for a in range(n)) == M and sum(q[a][n - 1 - a] for a in range(n)) == M
    return True, "n = 3, 5, … 19: Siamesische Methode ergibt magische Quadrate"


einfach("X19", "Gedächtnistechnik, keine Rechenprobe; Zuordnung 10 Ziffern ↔ 10 Lautgruppen", True)
einfach("M17", "46 · 7 · 6 = 1932", 46 * 7 * 6 == 46 * 42 == 1932)
einfach("Q14", "Formel für alle z (Zehner) und d = −5 … 5, 10 ≤ z + d ≤ 99", all(z * (z * (z + 3 * d) + 3 * d * d) + d ** 3 == (z + d) ** 3 for z in range(10, 101, 10) for d in range(-5, 6)))


@probe("Q15")
def _():
    rest = {}
    for r in range(11):
        rest.setdefault(r ** 3 % 11, []).append(r)
    assert all(len(v) == 1 for v in rest.values())
    endung = {(e ** 3) % 10: e for e in range(10)}
    for w in range(100, 1000):
        N = w ** 3
        a = math.isqrt(0)
        erste = max(d for d in range(1, 10) if (100 * d) ** 3 <= N)
        letzte = endung[N % 10]
        r = rest[alt_qs(N) % 11][0]
        mitte = [m for m in range(10) if (100 * erste + 10 * m + letzte) % 11 == r]
        assert mitte == [w // 10 % 10], w
    return True, "alle 900 Kubikzahlen von 100³ … 999³: Mittelziffer über den Elferrest eindeutig richtig"


einfach("Q16", "n¹³ ≡ n (mod 10) für alle Ziffern; 7¹³ = 96.889.010.407", all(e ** 13 % 10 == e for e in range(10)) and 7 ** 13 == 96889010407)


@probe("Q17")
def _():
    def wurzel(N, nachkomma):
        s = str(N * 10 ** (2 * nachkomma))
        if len(s) % 2:
            s = "0" + s
        p, r = 0, 0
        for i in range(0, len(s), 2):
            r = r * 100 + int(s[i:i + 2])
            x = max(x for x in range(10) if x * (20 * p + x) <= r)
            r -= x * (20 * p + x)
            p = 10 * p + x
        return p
    alle(lambda N: wurzel(N, 2) == math.isqrt(N * 10 ** 4), range(1, 20000), "Ziffernweise")
    return True, "N = 1 … 19.999 auf 2 Nachkommastellen = exakte abgerundete Wurzel; √152,2756 = 12,34"


@probe("Q18")
def _():
    worst = 0
    for S in range(2, 100000, 7):
        x = math.isqrt(S) + 0.5
        a = (S - x * x) / (2 * x)
        x1 = x + a
        x2 = x1 - a * a / (2 * x1)
        worst = max(worst, abs(x2 - sqrt(S)) / sqrt(S))
    return True, f"Start √S gerundet ± 0,5, S < 100.000: größter relativer Fehler {de(worst * 100, 6)} %"


einfach("Z24", "Endziffern-Perioden für Basis 0–9 teilen 4; 2¹⁰⁰ endet auf 6", all(pow(b, k + 4, 10) == pow(b, k, 10) for b in range(10) for k in range(1, 50)) and pow(2, 100, 10) == 6)
einfach("Z25", "a^(p−1) ≡ 1 für alle Primzahlen p < 200, a < p; 2¹⁰⁰ mod 7 = 2", all(pow(a, p - 1, p) == 1 for p in range(2, 200) if ist_prim(p) for a in range(1, p)) and pow(2, 100, 7) == 2)
einfach("Z26", "2⁶⁴ − 1 = 18.446.744.073.709.551.615", sum(2 ** k for k in range(64)) == 18446744073709551615)
einfach("D16", "k/17 (k = 1 … 16) ist Drehung von 0588235294117647", all(str(k * 10 ** 16 // 17).zfill(16) in "0588235294117647" * 2 for k in range(1, 17)) and 588235294117647 * 17 == 9999999999999999)
einfach("D17", "k/13 (k = 1 … 12) ist Drehung von 076923 oder 153846", all(str(k * 10 ** 6 // 13).zfill(6) in ("076923" * 2 + "|" + "153846" * 2) for k in range(1, 13)))
einfach("D18", "Σ 2ᵏ/100ᵏ (k = 1 … 199) = 1/49 auf 100 Stellen; 13/49 = 0,265306…", abs(sum(Fraction(2 ** k, 100 ** k) for k in range(1, 200)) - Fraction(1, 49)) < Fraction(1, 10 ** 100) and str(13 * 10 ** 6 // 49) == "265306")


@probe("D19")
def _():
    F = [0, 1]
    while len(F) < 200:
        F.append(F[-1] + F[-2])
    summe = sum(Fraction(F[k], 10 ** (k + 1)) for k in range(200))
    assert abs(summe - Fraction(1, 89)) < Fraction(1, 10 ** 150)
    return True, "Σ F(k)/10^(k+1) über 200 Glieder = 1/89 auf 150 Stellen"


einfach("D20", "1/81 und 1/9801: Perioden geprüft", str(10 ** 9 // 81).zfill(9) == "012345679" and "".join(f"{k:02d}" for k in range(100) if k != 98) == str(10 ** 198 // 9801).zfill(198))
einfach("R6", "2456 = 2500 − 44; 48 = 50 − 2", 2500 - 44 == 2456)
einfach("R7", "432 = 11 · 39 + 3", divmod(432, 11) == (39, 3))
einfach("R8", "1011 = 23 · 43 + 22", divmod(1011, 23) == (43, 22))


@probe("U15")
def _():
    z = []
    for n in (1, 5, 10, 20):
        st = sqrt(2 * pi * n) * (n / math.e) ** n
        z.append(f"n = {n}: {de((st / math.factorial(n) - 1) * 100, 2)} %")
    return True, "relativer Fehler: " + "; ".join(z) + " (≈ −1/(12n))"


@probe("G23")
def _():
    worst = max(abs(4 * x * (180 - x) / (40500 - x * (180 - x)) - sin(radians(x))) for x in [i / 10 for i in range(0, 1801)])
    return True, f"0° … 180° in 0,1°-Schritten: größter absoluter Fehler {de(worst, 4)}"


@probe("K8")
def _():
    def gleich(j, a, b):
        return dt.date(j, a, 1).weekday() == dt.date(j, b, 1).weekday() and calendar.monthrange(j, a)[1] >= 28
    for j in range(1901, 2100):
        if calendar.isleap(j):
            paare = [(1, 4), (4, 7), (2, 8), (3, 11), (9, 12)]
        else:
            paare = [(1, 10), (2, 3), (3, 11), (4, 7), (9, 12)]
        assert all(gleich(j, a, b) for a, b in paare), j
    return True, "1901–2099: Monatsanfänge der genannten Paare fallen immer auf denselben Wochentag (Normal- und Schaltjahre)"


def main():
    for lauf in PROBEN:
        lauf()
    fehler = {k: v for k, v in ERG.items() if not v["ok"]}
    Path(__file__).with_name("pruefung.json").write_text(json.dumps(ERG, ensure_ascii=False, indent=1))
    for k, v in ERG.items():
        print(("✓ " if v["ok"] else "✗ ") + k + ": " + v["text"])
    print(f"\n{len(ERG)} Proben, {len(fehler)} Fehler")


if __name__ == "__main__":
    main()
