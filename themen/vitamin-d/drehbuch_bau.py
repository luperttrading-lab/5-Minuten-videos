"""Baut szenen.json für das Vitamin-D-Probevideo aus Texten hier und dem Quellenverzeichnis in faktencheck.md."""
import json, re
fc = open('faktencheck.md', encoding='utf-8').read().split('## Quellenverzeichnis')[1]
Q = {}
for z in fc.splitlines():
    m = re.match(r'\| (\w+) \| (.+?) \| (.+) \| (\S+) \|', z)
    if m and m.group(1) != 'ID':
        Q[m.group(1)] = {'kurz': m.group(2), 'voll': m.group(3), 'url': m.group(4)}
PROMPTS = {b['datei']: b['prompt'] for s in json.load(open('bilder_prompts.json'))['scenes'] for b in s['bilder']}


def S(t, say=None):
    return {'t': t, 'say': say} if say else t


def B(t, at, ev, **kw):
    return dict({'t': t, 'at': at, 'ev': ev}, **kw)


GANZ = {'d1a', 'd3a', 'd4b', 'd5a', 'd6a', 'd6b'}            # Erklärbilder: ganz zeigen, nicht freistellen


def shots(sid, folge):
    out = []
    for x, n in folge:
        s = {'bild': f'bilder/{sid}{x}.png', 'zoom': 0.18}
        if sid + x in GANZ:
            s.update({'a': [0, 0, 2048, 1152], 'zoom': 'none'})
        if n:
            s['at'] = n
        out.append(s)
    return out


def bilder(sid):
    return [{'datei': f'bilder/{sid}{x}.png', 'prompt': PROMPTS[f'bilder/{sid}{x}.png']} for x in 'ab']


ABSCHLUSS = 'Gut, dass du dich informierst. Das Video kann das Gespräch mit Arzt oder Ärztin unterstützen, aber nicht ersetzen. Bis zum nächsten Video!'

scenes = [
 {'id': 'd0', 'layout': 'kacheln', 'kapitel': 'Einleitung', 'kicker': 'Faktencheck',
  'headline': 'Vitamin D: Was stimmt wirklich?',
  'sentences': [
   S('Vitamin D: Viele raten zu 10.000 Einheiten am Tag, gegen Krebs, Infekte und sogar gegen das Altern. Was davon hält?',
     'Vitamin D: Viele raten zu zehntausend Einheiten am Tag, gegen Krebs, Infekte und sogar gegen das Altern. Was davon hält?'),
   'Wir prüfen sechs Fragen: Sonne oder Essen, wie häufig Mangel ist, Testen, die großen Studien, Infekte und Altern, und Megadosen.'],
  'hervorheben_at': 1, 'legende_at': 1, 'kacheln_ab': 1, 'hook_bild': 'bilder/d0_hook.png', 'hook_titel': 'Vitamin D',
  'hook_zeilen': [{'t': '10.000 Einheiten am Tag?', 'wort': 'zehntausend'},
                  {'t': 'Gegen Krebs und Infekte?', 'wort': 'Krebs'},
                  {'t': 'Bremst es das Altern?', 'wort': 'Altern'},
                  {'t': 'Was davon hält?', 'wort': 'Was', 'art': 'urteil'}],
  'bilder': [{'datei': 'bilder/d0_hook.png', 'prompt': PROMPTS['bilder/d0_hook.png']}],
  'kacheln': [{'t': 'Sonne oder Essen?', 'bild': 'bilder/d1b.png', 'wort': 'Essen'},
              {'t': 'Wie verbreitet ist Mangel?', 'bild': 'bilder/d2a.png', 'wort': 'Mangel'},
              {'t': 'Testen lassen?', 'bild': 'bilder/d3a.png', 'wort': 'Testen'},
              {'t': 'Die großen Studien', 'bild': 'bilder/d4a.png', 'wort': 'Studien'},
              {'t': 'Infekte und Altern', 'bild': 'bilder/d5a.png', 'wort': 'Altern, und'},
              {'t': 'Megadosen', 'bild': 'bilder/d6a.png', 'wort': 'Megadosen'}]},

 {'id': 'd1', 'kapitel': 'Sonne oder Essen?', 'kicker': 'Herkunft', 'headline': 'Woher kommt Vitamin D?',
  'sentences': [
   'Den größten Teil seines Vitamin D bildet dein Körper selbst: in der Haut, mit dem UV-Licht der Sonne.',
   'Aus dem Essen kommt nur ein kleiner Teil, viel steckt nur in fettem Fisch wie Hering, etwas in Eiern und Pilzen.',
   'Von Oktober bis März steht die Sonne in Deutschland zu tief. Dann bildet die Haut kaum Vitamin D.',
   'Faustregel: Ist dein Schatten länger als du, bildet die Haut wenig. Geprüft ist das aber nicht.',
   'Im Alter, mit dunkler Haut und mit Sonnencreme bildet die Haut weniger.',
   'Gesicht und Arme allein sind wenig Fläche. In einem Versuch mit T-Shirt und kurzer Hose erreichten fast alle die Untergrenze, aber nur jeder Vierte höhere Werte.',
   S('Tipp für dich: Geh von Frühling bis Herbst mittags kurz raus, mit möglichst viel freier Haut. Je nach Hauttyp reichen 5 bis 25 Minuten, aber nie bis zum Sonnenbrand.',
     'Tipp für dich: Geh von Frühling bis Herbst mittags kurz raus, mit möglichst viel freier Haut. Je nach Hauttyp reichen fünf bis fünfundzwanzig Minuten, aber nie bis zum Sonnenbrand.')],
  'bullets': [B('Haut bildet den Großteil', 0, 'stark'), B('Essen allein reicht', 1, 'keine'),
              B('Oktober bis März kaum Bildung', 2, 'stark'), B('Gesicht und Arme reichen', 5, 'mittel')],
  'evidence': {'level': 'stark', 'label': 'gut belegt'},
  'quellen': ['bfr2025', 'rabenberg2015', 'rhodes2010'],
  'shots': shots('d1', [('b', 0), ('a', 2)]) + [{'bild': 'bilder/d2b.png', 'zoom': 0.18, 'at': 5}], 'bilder': bilder('d1')},

 {'id': 'd2', 'kapitel': 'Wie verbreitet ist Mangel?', 'kicker': 'Verbreitung', 'headline': 'Wie verbreitet ist ein Mangel?',
  'sentences': [
   'Oft heißt es, fast alle Deutschen hätten einen Mangel.',
   S('Die große Messung des Robert Koch-Instituts zeigt: Etwa jeder Siebte liegt im echten Mangel, unter 30 Nanomol pro Liter.',
     'Die große Messung des Robert Koch-Instituts zeigt: Etwa jeder Siebte liegt im echten Mangel, unter dreißig Nanomol pro Liter.'),
   'Gut vier von zehn liegen in einem Graubereich darüber, knapp die Hälfte ist gut versorgt.',
   'Diese Zahlen sind Jahresmittel: Im Winter und Frühjahr ist der Anteil im Mangel deutlich höher.',
   S('Die hohen Mangel-Zahlen entstehen mit einer Grenze von 75, die nicht einmal jeder Zehnte erreicht.',
     'Die hohen Mangel-Zahlen entstehen mit einer Grenze von fünfundsiebzig, die nicht einmal jeder Zehnte erreicht.'),
   S('Doch diese Grenze ist umstritten: Laut den großen Fachgremien reichen 50 für fast alle.',
     'Doch diese Grenze ist umstritten: Laut den großen Fachgremien reichen fünfzig für fast alle.'),
   'Tipp für dich: Ein Wert im Graubereich ist kein Notfall. Frag nach, welche Grenze dein Labor verwendet.'],
  'bullets': [B('Fast alle haben einen Mangel', 1, 'keine'), B('Im Winter mehr Mangel', 3, 'stark'),
              B('Ziel: mindestens 75 nmol/l', 5, 'mittel')],
  'evidence': {'level': 'mittel', 'label': 'Mangel seltener als behauptet'},
  'quellen': ['rabenberg2018', 'rabenberg2015', 'ross2011', 'demay2024'],
  'shots': shots('d2', [('a', 0), ('b', 6)]), 'bilder': bilder('d2')},

 {'id': 'd3', 'kapitel': 'Testen lassen?', 'kicker': 'Test', 'headline': 'Solltest du testen lassen?',
  'sentences': [
   'Viele raten, den Vitamin-D-Wert regelmäßig messen zu lassen.',
   S('Eine große Fachgesellschaft für Hormonmedizin rät seit 2024 davon ab, Gesunde routinemäßig zu testen.', 'Eine große Fachgesellschaft für Hormonmedizin rät seit zweitausendvierundzwanzig davon ab, Gesunde routinemäßig zu testen.'),
   'Denn der richtige Zielwert ist unklar, und Studien zum Nutzen solcher Tests fehlen.',
   'Die Kasse zahlt ihn nur bei begründetem Verdacht, sonst kostet er meist rund dreißig Euro.',
   'Achte auf die Einheit: Nanogramm pro Milliliter mal zweieinhalb ergibt Nanomol pro Liter. Zwanzig sind also fünfzig.',
   'Tipp für dich: Lass testen, wenn Arzt oder Ärztin einen Grund sehen, etwa bei Knochenschwund.'],
  'bullets': [B('Alle sollten regelmäßig testen', 1, 'keine', unbelegt=True), B('ng/ml mal 2,5 = nmol/l', 4, 'stark')],
  'evidence': {'level': 'keine', 'label': 'Routinetest: Nutzen unbelegt'},
  'quellen': ['demay2024', 'kvb2026'],
  'shots': shots('d3', [('a', 0), ('b', 3)]), 'bilder': bilder('d3')},

 {'id': 'd4', 'kapitel': 'Die großen Studien', 'kicker': 'Studien', 'headline': 'Was zeigen die großen Studien?',
  'sentences': [
   'Vitamin D soll vor Krebs, Herzinfarkt und Knochenbrüchen schützen.',
   'Zwar sind Menschen mit wenig Vitamin D öfter krank, doch Krankheit kann den Wert auch senken.',
   'Deshalb zählen Studien, in denen das Los entscheidet, wer Vitamin D bekommt und wer ein Scheinmittel.',
   S('Die größte lief in den USA, mit über 25.000 Menschen, fünf Jahre lang.',
     'Die größte lief in den USA, mit über fünfundzwanzigtausend Menschen, fünf Jahre lang.'),
   'Ergebnis: nicht weniger Krebs, nicht weniger Herzinfarkte und Schlaganfälle, nicht weniger Brüche. Ähnlich in Australien, Neuseeland und Europa.',
   'Ein Lichtblick: Bei täglicher Einnahme starben etwas weniger Menschen an Krebs. Gesichert ist das aber nicht.',
   'Wichtig: Fast alle Teilnehmer waren gut versorgt. Eine große Genanalyse deutet an: Unter fünfzig Nanomol steigt das Sterberisiko, darüber kaum noch.',
   'Tipp für dich: Nimm Vitamin D nicht als Krebs- oder Herzschutz. Bewegung und Nichtrauchen sind dafür viel besser belegt.'],
  'bullets': [B('Schützt vor Krebs', 4, 'keine'), B('Schützt Herz und Gefäße', 4, 'keine'),
              B('Schützt Gesunde vor Brüchen', 4, 'keine'), B('Weniger Krebstodesfälle', 5, 'mittel')],
  'evidence': {'level': 'keine', 'label': 'kein Schutz bei guter Versorgung'},
  'quellen': ['autier2014', 'manson2019', 'leboff2022', 'neale2022', 'scragg2017', 'bischoff2020', 'bolland2018',
              'keum2019', 'kuznia2023', 'sutherland2022'],
  'shots': shots('d4', [('a', 0), ('b', 4), ('a', 6)]), 'bilder': bilder('d4')},

 {'id': 'd5', 'kapitel': 'Infekte und Altern', 'kicker': 'Weitere Versprechen', 'headline': 'Infekte, Corona, Altern',
  'sentences': [
   'Gegen Erkältungen gibt es einen kleinen Schutz: Von hundert Menschen bleibt etwa einer mehr gesund.',
   'Bei Corona sahen frühe kleine Studien einen Nutzen, größere bestätigten das nicht. Depressionen verhinderte Vitamin D auch nicht.',
   'Und das Altern? In einer Studie verkürzten sich mit Vitamin D die Telomere etwas langsamer, die Schutzkappen der Chromosomen.',
   'Daraus wurde: Vitamin D bremse das Altern um fast drei Jahre.',
   'Doch das ist hochgerechnet, knapp an der Grenze zum Zufall. Und Telomere sind ein Laborwert, keine Krankheit.',
   'Tipp für dich: Bei Versprechen gegen das Altern frag nach: Wurden weniger Krankheiten gemessen oder nur ein Laborwert?'],
  'bullets': [B('Weniger Atemwegsinfekte', 0, 'mittel'), B('Schützt vor Corona und Depression', 1, 'keine'),
              B('Bremst das Altern um 3 Jahre', 3, 'mittel', neu='erst eine Studie')],
  'evidence': {'level': 'mittel', 'label': 'kleine Effekte'},
  'quellen': ['jolliffe2021', 'entrenas2020', 'murai2021', 'jolliffe2022', 'okereke2020', 'zhu2025'],
  'shots': shots('d5', [('b', 0), ('a', 2)]), 'bilder': bilder('d5')},

 {'id': 'd6', 'kapitel': 'Megadosen', 'kicker': 'Dosis', 'headline': 'Wie riskant sind Megadosen?',
  'sentences': [
   S('Manche raten zu 10.000 Einheiten am Tag oder mehr.',
     'Manche raten zu zehntausend Einheiten am Tag oder mehr.'),
   S('Wer selbst kaum Vitamin D bildet, braucht laut Fachgesellschaft für Ernährung etwa 800 Einheiten.',
     'Wer selbst kaum Vitamin D bildet, braucht laut Fachgesellschaft für Ernährung etwa achthundert Einheiten.'),
   S('Als sichere Obergrenze für Erwachsene nennt die europäische Lebensmittelbehörde 4.000. Normale Tagesmengen sind also kein Problem, erst bei 10.000 täglich sah sie erste Schäden.',
     'Als sichere Obergrenze für Erwachsene nennt die europäische Lebensmittelbehörde viertausend. Normale Tagesmengen sind also kein Problem, erst bei zehntausend täglich sah sie erste Schäden.'),
   'Zu viel treibt das Kalzium im Blut hoch. Das kann Nierensteine machen und die Nieren bleibend schädigen.',
   'Das Bundesinstitut für Risikobewertung meldet Vergiftungen, auch bei Säuglingen mit Mitteln für Erwachsene.',
   'Auch riesige Einzeldosen sind riskant: Ältere Frauen mit einer Megadosis pro Jahr stürzten und brachen sich öfter etwas.',
   'Die Stiftung Warentest fand die meisten Präparate überdosiert. Und Vitamin K2 dazu? Ein Nutzen ist nicht belegt.',
   S('Tipp für dich: 800 Einheiten am Tag decken laut Fachgesellschaft den Bedarf, bis 4.000 gelten als sicher. Mehr nur, wenn Arzt oder Ärztin das verordnen.',
     'Tipp für dich: Achthundert Einheiten am Tag decken laut Fachgesellschaft den Bedarf, bis viertausend gelten als sicher. Mehr nur, wenn Arzt oder Ärztin das verordnen.')],
  'bullets': [B('10.000 Einheiten täglich sind sicher', 2, 'keine', gefahr=True),
              B('Hohe Einzeldosen sind unbedenklich', 5, 'keine', gefahr=True),
              B('Vitamin K2 gehört dazu', 6, 'keine', unbelegt=True)],
  'evidence': {'level': 'keine', 'label': 'Megadosen schaden eher'},
  'quellen': ['efsa2023', 'bfr2025', 'burt2019', 'bfr045_2026', 'sanders2010', 'bfr031_2025', 'warentest2025', 'vz2026'],
  'shots': shots('d6', [('a', 0), ('b', 3), ('a', 5)]), 'bilder': bilder('d6')},

 {'id': 'd7', 'kapitel': 'Fazit', 'kicker': 'Fazit', 'headline': 'Wann Vitamin D sinnvoll ist',
  'sentences': [
   'Wann ist Vitamin D also klar sinnvoll?',
   'Bei Säuglingen: Sie bekommen es gegen Rachitis, bis zu ihrem zweiten Frühsommer.',
   'Bei Menschen im Pflegeheim, die kaum nach draußen kommen. Zusammen mit Kalzium senkt es dort Hüftbrüche.',
   'Und bei nachgewiesenem Mangel. Schwangere mit wenig Sonne sollten es ansprechen.',
   'Für alle anderen: Sommersonne hilft viel, im Winter kann eine kleine Tagesdosis sinnvoll sein, Megadosen schaden eher.',
   'Die Quellen stehen in der Beschreibung.',
   ABSCHLUSS],
  'bullets': [B('Säuglinge: Schutz vor Rachitis', 1, 'stark'), B('Pflegeheim: weniger Hüftbrüche', 2, 'stark'),
              B('Viel hilft viel', 4, 'keine')],
  'evidence': {'level': 'stark', 'label': 'sinnvoll für Risikogruppen'},
  'quellen': ['bfr2025', 'chapuy1992', 'avenell2014', 'koletzko2018'],
  'shots': shots('d7', [('a', 0), ('b', 2)]), 'bilder': bilder('d7')},
]

genutzt = []
for s in scenes:
    for q in s.get('quellen', []):
        if q not in genutzt:
            genutzt.append(q)
cfg = {'tts': 'elevenlabs', 'voice_id': 'NBqeXKdZHweef6y0B67V', 'voice_name': 'Christian - Warm and Captivating',
       'model': 'eleven_v4', 'tempo': 1.05, 'aussprache': {},
       'titel': 'Vitamin D: Was stimmt wirklich?',
       'untertitel': 'Ein Faktencheck zu Sonne, Mangel, Test, großen Studien, Altern und Megadosen. Jeder Punkt ist gegen Studien und Behörden geprüft; die Marker zeigen, wie gut er belegt ist.',
       'fuss': 'Sprecherstimme synthetisch (ElevenLabs). Illustrationen KI-generiert. Kein Ersatz für ärztlichen Rat: Das Video kann das Gespräch mit Arzt oder Ärztin unterstützen, aber nicht ersetzen.',
       'quellen': {q: Q[q] for q in genutzt}, 'scenes': scenes}
json.dump(cfg, open('szenen.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
w = sum(len((x['say'] if isinstance(x, dict) else x).split()) for s in scenes for x in s['sentences'])
print('Wörter (gesprochen):', w, '| Quellen:', len(genutzt))
