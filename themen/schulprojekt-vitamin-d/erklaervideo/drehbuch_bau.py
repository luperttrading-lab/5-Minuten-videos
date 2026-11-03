"""Drehbuch „Vitamin D: Das Sonnenhormon“ (Erklärvideo, kein Faktencheck, keine Ampel) für acht Bildstile.
Ein Sprechtext für alle Stile (gemeinsamer Ton-Cache), nur die Bilder wechseln. Quellen aus themen/vitamin-d/ übernommen
(dort geprüft), neue per Crossref geprüft (03.11.). Aufruf: python3 drehbuch_bau.py"""
import json, os

STILE = ['C', 'D', 'E', 'G', 'H', 'I', 'J', 'L']
alt = json.load(open('../../vitamin-d/szenen.json', encoding='utf-8'))['quellen']
UEBERNEHMEN = ['bfr2025', 'rhodes2010', 'rabenberg2018', 'ross2011', 'demay2024', 'manson2019', 'kuznia2023',
               'jolliffe2021', 'zhu2025', 'efsa2023', 'sanders2010', 'chapuy1992', 'koletzko2018']
Q = {k: alt[k] for k in UEBERNEHMEN}
NEU = {
 'holick2007': ['Holick 2007', 'Holick MF. Vitamin D Deficiency. N Engl J Med 2007;357:266–281.', 'https://doi.org/10.1056/NEJMra070553'],
 'holick2011': ['Holick et al. 2011', 'Holick MF et al. Evaluation, Treatment, and Prevention of Vitamin D Deficiency: an Endocrine Society Clinical Practice Guideline. J Clin Endocrinol Metab 2011;96(7):1911–1930.', 'https://doi.org/10.1210/jc.2011-0385'],
 'ekwaru2014': ['Ekwaru et al. 2014', 'Ekwaru JP et al. The Importance of Body Weight for the Dose Response Relationship of Oral Vitamin D Supplementation and Serum 25-Hydroxyvitamin D in Healthy Volunteers. PLoS One 2014;9(11):e111265.', 'https://doi.org/10.1371/journal.pone.0111265'],
 'veugelers2014': ['Veugelers & Ekwaru 2014', 'Veugelers PJ, Ekwaru JP. A Statistical Error in the Estimation of the Recommended Dietary Allowance for Vitamin D. Nutrients 2014;6(10):4472–4475.', 'https://doi.org/10.3390/nu6104472'],
 'dawson2015': ['Dawson-Hughes et al. 2015', 'Dawson-Hughes B et al. Dietary Fat Increases Vitamin D-3 Absorption. J Acad Nutr Diet 2015;115(2):225–230.', 'https://doi.org/10.1016/j.jand.2014.09.014'],
 'pittas2023': ['Pittas et al. 2023', 'Pittas AG et al. Vitamin D and Risk for Type 2 Diabetes in People With Prediabetes: Meta-analysis of Individual Participant Data From 3 Randomized Clinical Trials. Ann Intern Med 2023;176(3):355–363.', 'https://doi.org/10.7326/M22-3018'],
 'hahn2022': ['Hahn et al. 2022', 'Hahn J et al. Vitamin D and marine omega 3 fatty acid supplementation and incident autoimmune disease: VITAL randomized controlled trial. BMJ 2022;376:e066452.', 'https://doi.org/10.1136/bmj-2021-066452'],
}
for k, (kurz, voll, url) in NEU.items():
    Q[k] = {'kurz': kurz, 'voll': voll, 'url': url}

def S(t, say=None):
    return {'t': t, 'say': say} if say else t

def B(t, at):
    return {'t': t, 'at': at}

SZENEN = [
 {'id': 'v0', 'layout': 'kacheln', 'kapitel': 'Einleitung', 'kicker': 'Erklärvideo', 'headline': 'Vitamin D: Das Sonnenhormon',
  'sentences': ['Vitamin D: Dein Körper macht es selbst, aus Sonnenlicht. Doch im Winter fehlt es vielen.',
                'Du erfährst, was es eigentlich ist, wie du die Sonne richtig nutzt, wie du deinen Wert liest, wie viel du brauchst, was Studien zeigen und wer besonders profitiert.'],
  'hervorheben_at': 1,
  'kacheln': [('Ein Hormon aus Licht', 'e1', 'eigentlich'), ('Sonne richtig nutzen', 'e2a', 'Sonne richtig'),
              ('Dein Wert in ng/ml', 'e3', 'Wert'), ('Wie viel du brauchst', 'e4', 'wie viel'),
              ('Was Studien zeigen', 'e5', 'Studien'), ('Wer profitiert', 'e6', 'profitiert')]},
 {'id': 'v1', 'kicker': 'Grundlagen', 'headline': 'Ein Hormon aus Licht',
  'sentences': ['Vitamin D ist eigentlich kein klassisches Vitamin, sondern die Vorstufe eines Hormons.',
                'Den größten Teil bildet dein Körper selbst: in der Haut, mit dem UV-Licht der Sonne.',
                'Leber und Niere machen daraus die aktive Form, und Andockstellen dafür gibt es in fast allen Geweben.',
                'Am bekanntesten ist seine Aufgabe für Knochen und Muskeln: Es hilft dem Darm, Kalzium aufzunehmen.',
                'Aus dem Essen kommt nur wenig, am meisten steckt in fettem Fisch wie Hering.',
                'Tipp für dich: Fetter Fisch ein- bis zweimal pro Woche hilft etwas, die wichtigste Quelle bleibt aber die Sonne.'],
  'bullets': [B('Vorstufe eines Hormons', 0), B('Gebildet in der Haut', 1), B('Hilft, Kalzium aufzunehmen', 3), B('Wenig im Essen, viel im Hering', 4)],
  'quellen': ['holick2007', 'bfr2025'], 'bilder': [('e1', None)]},
 {'id': 'v2', 'kicker': 'Sonne', 'headline': 'Sonne richtig nutzen',
  'sentences': ['Im Sommer ist die Sonne die beste Quelle, und es kommt auf die Fläche an.',
                'Gesicht und Arme allein sind wenig Haut.',
                'In einem Versuch mit T-Shirt und kurzer Hose erreichten fast alle die Untergrenze, aber nur jeder Vierte höhere Werte.',
                'Mittags im Hochsommer, in Badehose oder Bikini, bildet die Haut nach einer bekannten Schätzung in wenigen Minuten mehrere tausend Einheiten, lange bevor sie rot wird.',
                'Von Oktober bis März steht die Sonne in Deutschland zu tief, dann bildet die Haut kaum Vitamin D.',
                'Im Alter, mit dunkler Haut und mit Sonnencreme bildet sie weniger.',
                S('Tipp für dich: Geh von Frühling bis Herbst mittags kurz raus, mit möglichst viel freier Haut. Je nach Hauttyp reichen 5 bis 25 Minuten, aber nie bis zum Sonnenbrand.',
                  'Tipp für dich: Geh von Frühling bis Herbst mittags kurz raus, mit möglichst viel freier Haut. Je nach Hauttyp reichen fünf bis fünfundzwanzig Minuten, aber nie bis zum Sonnenbrand.')],
  'bullets': [B('Viel freie Haut zählt', 1), B('Wenige Minuten im Hochsommer', 3), B('Oktober bis März: zu wenig Sonne', 4)],
  'quellen': ['rhodes2010', 'holick2007', 'bfr2025'], 'bilder': [('e2a', None), ('e2b', 4)]},
 {'id': 'v3', 'kicker': 'Laborwert', 'headline': 'Dein Wert in ng/ml',
  'sentences': [S('Gemessen wird die Speicherform im Blut, das 25-OH-Vitamin D.', 'Gemessen wird die Speicherform im Blut, das fünfundzwanzig-O-H-Vitamin D.'),
                'Wir rechnen in Nanogramm pro Milliliter.',
                'Manche Labore schreiben Nanomol pro Liter, das ist das Zweieinhalbfache: Zwanzig Nanogramm sind fünfzig Nanomol.',
                'Schau deshalb immer auf die Einheit, sonst hältst du einen guten Wert womöglich für einen Mangel.',
                'Unter zwölf gilt als Mangel.',
                'Ab zwanzig reicht es laut großen Fachgremien.',
                'Eine Fachgesellschaft für Hormonmedizin nannte lange dreißig als Ziel, das Optimum ist bis heute umstritten.',
                'In Deutschland liegt im Jahresmittel etwa jeder Siebte unter zwölf, im Winter sind es deutlich mehr.',
                'Tipp für dich: Lässt du deinen Wert messen, frag nach der Einheit und nach der Grenze, die dein Labor verwendet.'],
  'bullets': [B('Messgröße: 25-OH-Vitamin D', 0), B('20 ng/ml = 50 nmol/l', 2), B('Mangel: unter 12 ng/ml', 4), B('Ziel 20 oder 30? Umstritten', 6)],
  'quellen': ['ross2011', 'holick2011', 'demay2024', 'rabenberg2018'], 'bilder': [('e3', None)]},
 {'id': 'v4', 'kicker': 'Dosis', 'headline': 'Wie viel du brauchst',
  'sentences': [S('Ohne Sonne braucht ein Erwachsener laut Fachgesellschaft für Ernährung etwa 800 Einheiten am Tag.', 'Ohne Sonne braucht ein Erwachsener laut Fachgesellschaft für Ernährung etwa achthundert Einheiten am Tag.'),
                S('Als sichere Obergrenze für Erwachsene nennt die europäische Lebensmittelbehörde 4.000 Einheiten täglich.', 'Als sichere Obergrenze für Erwachsene nennt die europäische Lebensmittelbehörde viertausend Einheiten täglich.'),
                'Wer mehr wiegt, braucht mehr: bei Übergewicht etwa anderthalbmal so viel, bei starkem Übergewicht zwei- bis dreimal so viel für denselben Wert.',
                'Für die amerikanische Empfehlung fanden Statistiker sogar einen Rechenfehler, danach läge der Bedarf deutlich höher. Das ist allerdings umstritten.',
                'Am besten nimmst du es täglich statt als riesige Einzeldosis, und zu einer Mahlzeit mit etwas Fett, dann wird es besser aufgenommen.',
                S('Tipp für dich: 800 Einheiten decken den Grundbedarf. Mehr als 4.000 nur, wenn Arzt oder Ärztin es mit Laborkontrolle festlegen.', 'Tipp für dich: Achthundert Einheiten decken den Grundbedarf. Mehr als viertausend nur, wenn Arzt oder Ärztin es mit Laborkontrolle festlegen.')],
  'bullets': [B('Grundbedarf: 800 IE', 0), B('Obergrenze: 4.000 IE', 1), B('Mehr Gewicht, mehr Bedarf', 2), B('Täglich und mit etwas Fett', 4)],
  'quellen': ['bfr2025', 'efsa2023', 'ekwaru2014', 'veugelers2014', 'sanders2010', 'dawson2015'], 'bilder': [('e4', None)]},
 {'id': 'v5', 'kicker': 'Forschung', 'headline': 'Was Studien zeigen',
  'sentences': ['Was bringt die Einnahme? Am meisten bei Menschen mit niedrigem Wert.',
                'Bei täglicher Einnahme starben in einer Auswertung großer Studien etwa ein Achtel weniger Menschen an Krebs.',
                'Bei einer Diabetes-Vorstufe erkrankten weniger Menschen an Typ-2-Diabetes, etwa jeder siebte Fall weniger.',
                'In der großen amerikanischen Studie traten Autoimmunerkrankungen wie Rheuma oder Schuppenflechte um etwa ein Fünftel seltener auf.',
                'Gegen Atemwegsinfekte gibt es einen kleinen Schutz, vor allem bei täglicher Einnahme.',
                'Und die Telomere, die Schutzkappen der Chromosomen, verkürzten sich langsamer.',
                'Bei gut versorgten Gesunden fanden große Studien dagegen wenig. Die Chance liegt vor allem darin, einen Mangel auszugleichen.',
                'Tipp für dich: Vitamin D lohnt sich besonders, wenn dein Wert niedrig ist, und das ist im Winter häufig.'],
  'bullets': [B('Weniger Krebstodesfälle bei täglicher Einnahme', 1), B('Seltener Typ-2-Diabetes bei Vorstufe', 2), B('Seltener Autoimmunerkrankungen', 3), B('Etwas weniger Atemwegsinfekte', 4)],
  'quellen': ['kuznia2023', 'pittas2023', 'hahn2022', 'jolliffe2021', 'zhu2025', 'manson2019'], 'bilder': [('e5', None)]},
 {'id': 'v6', 'kicker': 'Für wen', 'headline': 'Wer besonders profitiert',
  'sentences': ['Wer profitiert besonders?',
                'Säuglinge: Sie bekommen Vitamin D gegen Rachitis, bis zu ihrem zweiten Frühsommer.',
                'Ältere Menschen bilden in der Haut weniger. Im Pflegeheim senkte Vitamin D zusammen mit Kalzium die Hüftbrüche.',
                'Auch Menschen mit dunkler Haut, mit starkem Übergewicht oder die fast nur drinnen arbeiten, haben öfter niedrige Werte.',
                'Schwangere mit wenig Sonne sollten es in der Praxis ansprechen.',
                'Tipp für dich: Gehörst du zu einer dieser Gruppen, sprich Arzt oder Ärztin auf Vitamin D an.'],
  'bullets': [B('Säuglinge', 1), B('Ältere, Pflegeheim', 2), B('Dunkle Haut, Übergewicht, Innenarbeit', 3), B('Schwangere mit wenig Sonne', 4)],
  'quellen': ['bfr2025', 'chapuy1992', 'holick2007', 'koletzko2018'], 'bilder': [('e6', None)]},
 {'id': 'v7', 'kapitel': 'Fazit', 'kicker': 'Fazit', 'headline': 'Das Wichtigste',
  'sentences': ['Vitamin D ist ein Sonnenhormon, das dein Körper selbst macht, wenn du ihn lässt.',
                'Im Sommer heißt das: mittags kurz raus, viel freie Haut, nie bis zum Sonnenbrand.',
                S('Im Winter hilft eine tägliche Dosis von etwa 800 Einheiten.', 'Im Winter hilft eine tägliche Dosis von etwa achthundert Einheiten.'),
                S('Mehr als 4.000 nur mit ärztlicher Begleitung.', 'Mehr als viertausend nur mit ärztlicher Begleitung.'),
                'Und wenn du deinen Wert misst, achte auf die Einheit.',
                'Die Quellen stehen in der Beschreibung.',
                'Gut, dass du dich informierst. Das Video kann das Gespräch mit Arzt oder Ärztin unterstützen, aber nicht ersetzen. Bis zum nächsten Video!'],
  'bullets': [B('Sommer: Sonne auf viel Haut', 1), B('Winter: tägliche kleine Dosis', 2), B('Auf die Einheit achten', 4)],
  'quellen': ['bfr2025', 'efsa2023'], 'bilder': [('e7', None)]},
]

def bauen(stil):
    szenen = []
    for sc in SZENEN:
        s = {k: v for k, v in sc.items() if k not in ('bilder', 'kacheln')}
        if 'kacheln' in sc:
            s['kacheln'] = [{'t': t, 'bild': f'bilder/{stil}/{b}.jpg', 'wort': w} for t, b, w in sc['kacheln']]
        if 'bilder' in sc:
            s['shots'] = [dict({'bild': f'bilder/{stil}/{b}.jpg'}, **({'at': at} if at is not None else {})) for b, at in sc['bilder']]
        szenen.append(s)
    return {'tts': 'elevenlabs', 'voice_id': 'NBqeXKdZHweef6y0B67V', 'model': 'eleven_v4', 'tempo': 1.05,
            'titel': 'Vitamin D: Das Sonnenhormon', 'stil': stil,
            'untertitel': 'Ein Erklärvideo: was Vitamin D ist, wie du die Sonne richtig nutzt, deinen Wert liest und wie viel du brauchst.',
            'fuss': 'Sprecherstimme synthetisch (ElevenLabs). Bilder KI-generiert. Das Video ersetzt nicht das Gespräch mit Arzt oder Ärztin.',
            'scenes': szenen, 'quellen': Q}

if __name__ == '__main__':
    for stil in STILE:
        json.dump(bauen(stil), open(f'szenen_{stil}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    w = sum(len((x if isinstance(x, str) else x['t']).split()) for sc in SZENEN for x in sc['sentences'])
    print(len(STILE), 'Drehbücher,', w, 'Wörter')
