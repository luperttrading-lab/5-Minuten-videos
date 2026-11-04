#!/usr/bin/env python3
"""Motivierende Sätze für Erklärvideos, die von Video zu Video wechseln (Nutzerwunsch 04.11.: „nicht immer der
gleiche Spruch“). Ein Thema behält seinen Spruch (sonst ändert sich der Sprechtext bei jedem Neu-Rendern und kostet
neuen Ton); ein neues Thema bekommt den am seltensten benutzten. Vergabe in motivation_benutzt.json.

    from motivation import spruch
    spruch('mathe-einmaleins', 'schluss')   # → 'Das ist kein Hexenwerk.'
"""
import json, os

SPRUECHE = {
    # am Schluss, nach „Mit ein bisschen Übung schaffst du das auch“
    'schluss': [
        'Das ist kein Hexenwerk.',
        'Das ist keine Raketenwissenschaft.',
        'Übung macht den Meister.',
        'Das kann jeder lernen.',
        'Nach ein paar Runden geht das wie von selbst.',
        'Dein Kopf ist schneller, als du denkst.',
        'Dranbleiben lohnt sich.',   # „Jeder fängt mal langsam an“ raus (Nutzer 04.11.: klingt herablassend)
        'Mit jeder Aufgabe wird es leichter.',
        'Dafür musst du kein Mathe-Genie sein.',
        'Ein paar Minuten am Tag reichen schon.',
    ],
    # Brücke vor der Erklärung („Warum klappt das?“)
    'bruecke': [
        'Klingt nach Zauberei? Ist es nicht.',
        'Klingt komplizierter, als es ist.',
        'Kein Trick ohne Grund.',
        'Das sieht man sogar im Bild.',
        'Dahinter steckt ganz einfache Mathematik.',
    ],
}

PFAD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'motivation_benutzt.json')


def spruch(thema, art='schluss'):
    try:
        benutzt = json.load(open(PFAD, encoding='utf-8'))
    except FileNotFoundError:
        benutzt = {}
    fach = benutzt.setdefault(art, {})
    if thema in fach:
        return fach[thema]
    zaehler = {s: 0 for s in SPRUECHE[art]}
    for s in fach.values():
        if s in zaehler:
            zaehler[s] += 1
    wahl = min(SPRUECHE[art], key=lambda s: zaehler[s])     # am seltensten benutzt, bei Gleichstand der erste
    fach[thema] = wahl
    with open(PFAD, 'w', encoding='utf-8') as f:
        json.dump(benutzt, f, ensure_ascii=False, indent=1)
    return wahl


if __name__ == '__main__':
    print(json.dumps(json.load(open(PFAD, encoding='utf-8')) if os.path.exists(PFAD) else {}, ensure_ascii=False,
                     indent=1))
