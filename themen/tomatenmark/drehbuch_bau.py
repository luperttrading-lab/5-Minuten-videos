import json, re
fc = open('faktencheck.md', encoding='utf-8').read().split('## Quellenverzeichnis')[1]
Q = {}
for z in fc.splitlines():
    m = re.match(r'\| (\w+) \| (.+?) \| (.+) \| (\S+)', z)
    if m and m.group(1) not in ('ID',):
        Q[m.group(1)] = {'kurz': m.group(2), 'voll': m.group(3), 'url': m.group(4)}

def S(t, say=None):
    return {'t': t, 'say': say} if say else t
def B(t, at, ev): return {'t': t, 'at': at, 'ev': ev}
def shots(sid, at): return [{'bild': f'bilder/{sid}a.png', 'zoom': 0.18}, {'bild': f'bilder/{sid}b.png', 'zoom': 0.18, 'at': at}]

scenes = [
 {'id': 't0', 'layout': 'kacheln', 'kapitel': 'Einleitung', 'kicker': 'Info-Video · Faktencheck',
  'headline': 'Tomatenmark: Was steckt wirklich im Löffel?',
  'sentences': [
   'Tomatenmark gilt als Superfood aus der Tube: gut fürs Gehirn, fürs Herz und gegen Krebs.',
   'Wir prüfen sechs Fragen: Mark oder frische Tomate, was es dem Gehirn bringt und dem Herzen, ob eine Kapsel reicht, welche Versprechen halten und worauf du beim Kauf achtest.',
   'Jede Aussage haben wir gegen die Studienlage geprüft.',
   'Grün heißt belegt, gelb teilweise, rot nicht haltbar.'],
  'hervorheben_at': 1, 'legende_at': 3,
  'kacheln': [{'t': 'Mark oder Tomate?', 'bild': 'bilder/t1b.png', 'wort': 'frische Tomate'},
              {'t': 'Hilft es dem Gehirn?', 'bild': 'bilder/t2a.png', 'wort': 'Gehirn bringt'},
              {'t': 'Herz und Schlaganfall', 'bild': 'bilder/t3a.png', 'wort': 'Herzen'},
              {'t': 'Kapsel oder Löffel?', 'bild': 'bilder/t4a.png', 'wort': 'Kapsel'},
              {'t': 'Weitere Versprechen', 'bild': 'bilder/t5a.png', 'wort': 'Versprechen'},
              {'t': 'Beim Kauf', 'bild': 'bilder/t6a.png', 'wort': 'Kauf'}]},
 {'id': 't1', 'kapitel': 'Mark oder Tomate?', 'kicker': 'Aufnahme', 'headline': 'Mark oder frische Tomate?',
  'sentences': [
   'Der Stoff, um den es geht, heißt Lykopin. Er macht Tomaten rot.',
   S('Oft heißt es, Tomatenmark liefere 20-mal so viel davon wie frische Tomaten.', 'Oft heißt es, Tomatenmark liefere zwanzigmal so viel davon wie frische Tomaten.'),
   S('Gemessen ist etwas anderes: Pro Gramm enthält Mark etwa 11-mal so viel, weil das Wasser fehlt.', 'Gemessen ist etwas anderes: Pro Gramm enthält Mark etwa elfmal so viel, weil das Wasser fehlt.'),
   'Dazu kommt: Aus gekochtem Mark mit etwas Fett nimmt der Körper Lykopin deutlich besser auf als aus roher Tomate.',
   'Denn Lykopin löst sich in Fett, nicht in Wasser.',
   S('Oft heißt es auch, mit Olivenöl steige das Lykopin im Blut um über 80 %, doch diese Zahl stammt aus einem einzigen kleinen Versuch.', 'Oft heißt es auch, mit Olivenöl steige das Lykopin im Blut um über achtzig Prozent, doch diese Zahl stammt aus einem einzigen kleinen Versuch.'),
   'Ein Esslöffel Mark enthält etwa so viel Lykopin wie anderthalb frische Tomaten.',
   'Tipp für dich: Brate das Mark kurz in etwas Öl an, bevor die anderen Zutaten in den Topf kommen.'],
  'bullets': [B('Mark: 20-mal mehr Lykopin', 1, 'mittel'), B('Hitze und Öl verbessern die Aufnahme', 3, 'stark'),
              B('Mit Olivenöl über 80 % mehr', 5, 'mittel')],
  'evidence': {'level': 'mittel', 'label': 'Richtung stimmt, Zahlen übertrieben'},
  'quellen': ['usda_fdc', 'gaertner1997', 'stahl1992', 'unlu2007', 'fielding2005'],
  'shots': shots('t1', 6),
  'bilder': [
   {'datei': 'bilder/t1a.png', 'prompt': 'explanatory picture in four big steps from left to right connected by large hand-drawn arrows: ripe red tomatoes, a small pan where a spoon of tomato paste sizzles in golden olive oil, a simple stylized human gut, a red blood vessel with small red droplets flowing inside'},
   {'datei': 'bilder/t1b.png', 'prompt': 'on a wooden board: one heaped tablespoon of deep red tomato paste lying next to one whole fresh red tomato and one half tomato, seen slightly from above, the spoon and the tomatoes large in the frame'}]},
 {'id': 't2', 'kapitel': 'Hilft es dem Gehirn?', 'kicker': 'Gehirn', 'headline': 'Hilft es dem Gehirn?',
  'sentences': [
   'Das größte Versprechen: Tomatenmark stärke Gehirn und Gedächtnis.',
   'Dazu gibt es tatsächlich eine neue Studie aus Spanien.',
   S('Gut 40 Erwachsene aßen dafür täglich zwei Esslöffel Tomatenmark.', 'Gut vierzig Erwachsene aßen dafür täglich zwei Esslöffel Tomatenmark.'),
   'Nach drei Monaten konzentrierten sie sich etwas besser und ordneten Namen etwas leichter Gesichtern zu.',
   'Aber: Alle wussten, was sie aßen, und die Unterschiede waren klein.',
   'Der Wachstumsstoff für Nervenzellen stieg nur knapp, schwächer als die Forscher erwartet hatten.',
   'Der Schutz vor Demenz ist bisher nur beobachtet: Menschen mit Demenz haben weniger Lykopin im Blut, vielleicht aber, weil sie anders essen.',
   'Tipp für dich: Sieh Tomatenmark als Teil guter Ernährung. Für Bewegung und Schlaf ist die Wirkung aufs Gehirn viel besser belegt.'],
  'bullets': [B('35 g täglich: bessere Konzentration', 3, 'mittel'), B('Steigert den Nervenwachstumsfaktor BDNF', 5, 'mittel'),
              B('Schützt vor Demenz', 6, 'mittel')],
  'evidence': {'level': 'mittel', 'label': 'erste Hinweise, kein Beweis'},
  'quellen': ['lopezsolis2026', 'wang2023', 'crowewhite2019'],
  'shots': shots('t2', 7),
  'bilder': [
   {'datei': 'bilder/t2a.png', 'prompt': 'a woman in her mid forties sitting at a kitchen table, thoughtfully looking at a few blank picture cards with simple portrait sketches spread on the table, a bowl of pasta with red tomato sauce beside her, the scene fills the whole frame edge to edge, no empty paper border'},
   {'datei': 'bilder/t2b.png', 'prompt': 'a man and a woman in their fifties walking briskly side by side along a tree-lined path in a park in soft morning light, relaxed and happy'}]},
 {'id': 't3', 'kapitel': 'Herz und Schlaganfall', 'kicker': 'Herz und Gefäße', 'headline': 'Herz und Schlaganfall',
  'sentences': [
   'Fürs Herz heißt es: Lykopin senke das Risiko für einen Schlaganfall um mehr als die Hälfte.',
   'Die Zahl stammt aus Finnland, aus einer Beobachtung von gut tausend Männern.',
   S('Wer viel Lykopin im Blut hatte, bekam seltener einen Schlaganfall, insgesamt waren es aber nur 67 Fälle.', 'Wer viel Lykopin im Blut hatte, bekam seltener einen Schlaganfall, insgesamt waren es aber nur siebenundsechzig Fälle.'),
   'Eine Gen-Analyse an über einer Million Menschen fand dagegen keinen ursächlichen Schutz.',
   'Viel Lykopin zeigt also eher eine gesunde Ernährung an.',
   'Auch das schlechte LDL-Cholesterin sank nur bei großen Mengen, umgerechnet fünf, sechs Esslöffeln Mark am Tag.',
   'Der Blutdruck sank in manchen Studien leicht, meist mit Extrakten statt mit Mark.',
   'Tipp für dich: Tomaten gehören in eine Mittelmeerküche. Tabletten gegen Blutdruck oder Cholesterin ersetzen sie nicht.'],
  'bullets': [B('55 % weniger Schlaganfälle', 0, 'mittel'), B('Senkt LDL um etwa 10 %', 5, 'mittel'),
              B('Senkt den Blutdruck', 6, 'mittel')],
  'evidence': {'level': 'mittel', 'label': 'Zusammenhang ja, Ursache unklar'},
  'quellen': ['karppi2012', 'martens2021', 'ried2011', 'tierney2020', 'li2013'],
  'shots': shots('t3', 7),
  'bilder': [
   {'datei': 'bilder/t3a.png', 'prompt': 'a large softly drawn human heart with its main blood vessels in terracotta and dove blue, simple friendly anatomical illustration, filling most of the frame'},
   {'datei': 'bilder/t3b.png', 'prompt': 'a Mediterranean dinner table seen from above: a pan of tomato sauce with chickpeas, a bowl of salad with vegetables, a small bottle of olive oil, bread, fresh tomatoes'}]},
 {'id': 't4', 'kapitel': 'Kapsel oder Löffel?', 'kicker': 'Präparate', 'headline': 'Kapsel oder Löffel?',
  'sentences': [
   'Und wenn du keine Tomaten magst, reicht dann eine Kapsel?',
   'Oft heißt es: Künstliches Lykopin sei wirkungslos, nur der natürliche Komplex aus der Tomate zähle.',
   'Dahinter steht vor allem eine Studie, bezahlt von einer Firma, die genau diesen Tomatenextrakt verkauft.',
   'Pro Gruppe waren es nur etwa ein Dutzend Teilnehmer, der Unterschied war knapp.',
   'Ins Blut gelangt künstliches Lykopin genauso gut, auch das hat allerdings ein Hersteller gemessen.',
   'Klar ist also nur: Eine Kapsel bringt dir nichts, was ein Löffel Mark nicht auch bringt.',
   'Tipp für dich: Spar dir das Geld für die Kapsel und nimm den Löffel.'],
  'bullets': [B('Synthetisches Lykopin ist wirkungslos', 1, 'keine')],
  'evidence': {'level': 'keine', 'label': 'Herstellerstudie, nicht haltbar'},
  'quellen': ['wolak2019', 'hoppe2003'],
  'shots': shots('t4', 6),
  'bilder': [
   {'datei': 'bilder/t4a.png', 'prompt': 'an old brass balance scale in perfect balance: on one pan a single red softgel pill, on the other pan a tablespoon of deep red tomato paste, large in the frame'},
   {'datei': 'bilder/t4b.png', 'prompt': 'a hand stirring a spoonful of tomato paste into a simmering pot of sauce on a stove, a closed pill bottle pushed to the edge of the counter'}]},
 {'id': 't5', 'kapitel': 'Weitere Versprechen', 'kicker': 'Weitere Versprechen', 'headline': 'Prostata, Haut, Leber, Darm',
  'sentences': [
   'Dazu kommen weitere Versprechen.',
   'Prostatakrebs: Männer, die oft gekochte Tomatenprodukte essen, erkranken in Beobachtungsstudien etwas seltener, bei rohen Tomaten zeigt sich das nicht.',
   'Für einen Beweis reichen die wenigen Versuche nicht.',
   'Haut: Nach zehn Wochen mit Tomatenmark wurde die Haut in der Sonne etwas weniger rot, eine Sonnencreme ersetzt das nicht.',
   'Leber: Wer viel Lykopin isst, hat seltener eine Fettleber, auch das ist vor allem beobachtet.',
   'Zu den Knochen nach den Wechseljahren gibt es nur einen kleinen Versuch, ohne Messung der Knochendichte.',
   'Und mehr gute Darmbakterien? Das stammt aus einer winzigen Studie mit Lykopin-Präparaten, mit Tomatenmark wurde es nie untersucht.',
   'Tipp für dich: Vorsorge und Sonnencreme bleiben, Tomatenmark kommt obendrauf.'],
  'bullets': [B('Senkt Prostatakrebs-Risiko', 1, 'mittel'), B('Schützt die Haut vor Sonne', 3, 'mittel'),
              B('Schützt vor Fettleber', 4, 'mittel'), B('Mehr Bifidobakterien im Darm', 6, 'keine')],
  'evidence': {'level': 'mittel', 'label': 'vor allem Beobachtungen'},
  'quellen': ['rowles2018', 'ilic2011', 'stahl2001', 'donghia2024', 'tatoli2026', 'mackinnon2011', 'wiese2019'],
  'shots': shots('t5', 3),
  'bilder': [
   {'datei': 'bilder/t5a.png', 'prompt': 'a friendly doctor and a man in his sixties talking calmly at a wooden desk in a bright consulting room, a bowl of red tomatoes on the windowsill'},
   {'datei': 'bilder/t5b.png', 'prompt': 'a woman under a beach umbrella on a sunny terrace rubbing sunscreen on her arm, a plate of pasta with tomato sauce on the small table beside her'}]},
 {'id': 't6', 'kapitel': 'Beim Kauf', 'kicker': 'Einkauf', 'headline': 'Worauf du beim Kauf achtest',
  'sentences': [
   'Bleibt der Einkauf.',
   'In Tests fanden sich in etwa jedem zweiten Tomatenmark Schimmelpilzgifte.',
   'Für diese Gifte gibt es in der EU bisher nur Richtwerte, keine Grenzwerte.',
   'Oft heißt es, Bio schütze davor, doch unter den am stärksten belasteten Produkten waren mehrere Bio-Marken.',
   'Der Zucker auf dem Etikett stammt meist aus der Tomate selbst, nicht aus der Zuckerdose.',
   'Und wer Histamin schlecht verträgt, probiert vorsichtig aus, wie viel er verträgt.',
   'Tipp für dich: Schau in aktuelle Testergebnisse, wechsle ab und zu die Marke und lies die Zutatenliste: Tomaten, höchstens Salz.'],
  'bullets': [B('Schimmelpilzgifte in jedem zweiten Produkt', 1, 'stark'), B('Bio schützt davor', 3, 'keine'),
              B('Viel Histamin', 5, 'mittel')],
  'evidence': {'level': 'stark', 'label': 'Belastung belegt'},
  'quellen': ['oekotest2021', 'saldo2025', 'eu2022_553', 'sanchezperez2018'],
  'shots': shots('t6', 6),
  'bilder': [
   {'datei': 'bilder/t6a.png', 'prompt': 'a hand holding a big magnifying glass over a row of plain unlabeled tubes and small jars of tomato paste on a supermarket shelf'},
   {'datei': 'bilder/t6b.png', 'prompt': 'an open glass jar of tomato paste next to a heap of ripe red tomatoes and a small dish of coarse salt on a wooden kitchen counter'}]},
 {'id': 't7', 'kapitel': 'Fazit', 'kicker': 'Fazit', 'headline': 'Was wirklich bleibt',
  'sentences': [
   'Was bleibt also?',
   'Erstens: Tomatenmark ist ein günstiger, guter Lykopin-Lieferant, am besten gekocht und mit etwas Öl.',
   'Zweitens: Die großen Versprechen beruhen vor allem auf Beobachtungen und kleinen Studien.',
   'Drittens: Kapseln bringen nichts extra, ab und zu die Marke zu wechseln schon eher.',
   'Ob es jeden Tag ein Esslöffel sein muss, hat übrigens niemand untersucht. Ein paar Mal pro Woche in der Soße ist ein guter Anfang.',
   'Die Quellen stehen in der Beschreibung.'],
  'bullets': [B('Gekocht mit Öl besser aufgenommen', 1, 'stark'), B('Schützt Gehirn, Herz, vor Krebs', 2, 'mittel'),
              B('Nur natürliches Lykopin wirkt', 3, 'keine')],
  'evidence': {'level': 'mittel', 'label': 'gutes Lebensmittel, kein Wundermittel'},
  'quellen': ['usda_fdc'],
  'shots': shots('t7', 4),
  'bilder': [
   {'datei': 'bilder/t7a.png', 'prompt': 'close-up of a frying pan where a spoonful of deep red tomato paste sizzles in golden olive oil with a wooden spoon, warm kitchen light'},
   {'datei': 'bilder/t7b.png', 'prompt': 'a family of three at a kitchen table sharing a big bowl of pasta with red tomato sauce, warm and cheerful, the scene fills the whole frame edge to edge, no empty paper border'}]},
]
genutzt = []
for sc in scenes:
    for q in sc.get('quellen', []):
        assert q in Q, q
        if q not in genutzt: genutzt.append(q)
cfg = {'tts': 'elevenlabs', 'voice_id': 'NBqeXKdZHweef6y0B67V', 'voice_name': 'Christian - Warm and Captivating',
       'model': 'eleven_v4', 'tempo': 1.0, 'titel': 'Tomatenmark: Was steckt wirklich im Löffel?',
       'untertitel': 'Ein Faktencheck zu Lykopin, Gehirn, Herz, Kapseln und Einkauf. Jeder Punkt ist gegen Studien geprüft; die Marker zeigen, wie gut er belegt ist.',
       'fuss': 'Sprecherstimme synthetisch (ElevenLabs). Illustrationen KI-generiert. Kein Ersatz für ärztlichen Rat.',
       'quellen': {q: Q[q] for q in genutzt}, 'scenes': scenes}
json.dump(cfg, open('szenen.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tot = 0
for sc in scenes:
    n = sum(len(re.findall(r'\w+', s['say'] if isinstance(s, dict) else s)) for s in sc['sentences'])
    tot += n; print(sc['id'], n)
print('Summe', tot, '≈', round(tot / 2.2), 's')
