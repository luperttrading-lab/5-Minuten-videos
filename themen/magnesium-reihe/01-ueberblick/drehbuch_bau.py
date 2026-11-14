"""Drehbuch Folge 1 „Magnesium: Was du wirklich wissen musst“ (Magnesium-Reihe), Erklärvideo ohne Ampel, Stil G (Aquarell und Tusche).
Fakten und Quellen: faktencheck.md, recherche_A.md, recherche_B.md (14.11.2026). Gliederung: ../konzept.md.
Dosierungen nur als Beschreibung von Behörden und Studien, keine Marken. Aufruf: python3 drehbuch_bau.py"""
import json, os

STILE = ['G']

QUELLEN = {
 'jahnen2012': ['Jahnen-Dechent 2012', 'Jahnen-Dechent W, Ketteler M. Magnesium basics. Clin Kidney J 2012;5(Suppl 1):i3–i14.', 'https://doi.org/10.1093/ndtplus/sfr163'],
 'debaaij2015': ['de Baaij 2015', 'de Baaij JHF, Hoenderop JGJ, Bindels RJM. Magnesium in man: implications for health and disease. Physiol Rev 2015;95(1):1–46.', 'https://doi.org/10.1152/physrev.00012.2014'],
 'fiorentini2021': ['Fiorentini 2021', 'Fiorentini D, Cappadone C, Farruggia G, Prata C. Magnesium: Biochemistry, Nutrition, Detection, and Social Impact of Diseases Linked to Its Deficiency. Nutrients 2021;13(4):1136.', 'https://doi.org/10.3390/nu13041136'],
 'mayer1984': ['Mayer 1984', 'Mayer ML, Westbrook GL, Guthrie PB. Voltage-dependent block by Mg2+ of NMDA responses in spinal cord neurones. Nature 1984;309:261–263.', 'https://doi.org/10.1038/309261a0'],
 'dge_web': ['DGE 2021', 'Deutsche Gesellschaft für Ernährung. Referenzwerte Magnesium (Schätzwerte, Stand Ableitung 2021), abgerufen 14.11.2026.', 'https://www.dge.de/wissenschaft/referenzwerte/magnesium/'],
 'efsa2015': ['EFSA 2015', 'EFSA NDA Panel. Scientific Opinion on Dietary Reference Values for magnesium. EFSA Journal 2015;13(7):4186.', 'https://doi.org/10.2903/j.efsa.2015.4186'],
 'bls2025': ['MRI 2025 (BLS 4.0)', 'Max Rubner-Institut. Bundeslebensmittelschlüssel (BLS), Version 4.0. Karlsruhe 2025, CC BY 4.0.', 'https://doi.org/10.25826/Data20251217-134202-0'],
 'mri2008': ['MRI 2008 (NVS II)', 'Max Rubner-Institut. Nationale Verzehrsstudie II, Ergebnisbericht Teil 2. Karlsruhe 2008.', 'https://www.mri.bund.de/fileadmin/MRI/Institute/EV/NVSII_Abschlussbericht_Teil_2.pdf'],
 'mintafelwv': ['Min/TafelWV', 'Mineral- und Tafelwasser-Verordnung, Anlage 6 (zu § 9 Abs. 3).', 'https://www.gesetze-im-internet.de/min_tafelwv/anlage_6.html'],
 'dge_faq': ['DGE 2022', 'Deutsche Gesellschaft für Ernährung. Ausgewählte Fragen und Antworten zu Magnesium, 2022.', 'https://www.dge.de/fileadmin/dok/gesunde-ernaehrung/faq/DGE-FAQ-Magnesium-2022.pdf'],
 'ahmed2019': ['Ahmed 2019', 'Ahmed F, Mohammed A. Magnesium: The Forgotten Electrolyte – A Review on Hypomagnesemia. Med Sci (Basel) 2019;7(4):56.', 'https://doi.org/10.3390/medsci7040056'],
 'liamis2021': ['Liamis 2021', 'Liamis G, Hoorn EJ, Florentin M, Milionis H. An overview of diagnosis and management of drug-induced hypomagnesemia. Pharmacol Res Perspect 2021;9(4):e00829.', 'https://doi.org/10.1002/prp2.829'],
 'srinutta2019': ['Srinutta 2019', 'Srinutta T, Chewcharat A, Takkavatakarn K et al. Proton pump inhibitors and hypomagnesemia: A meta-analysis of observational studies. Medicine 2019;98(44):e17788.', 'https://doi.org/10.1097/md.0000000000017788'],
 'rosanoff2022': ['Rosanoff 2022', 'Rosanoff A, West C, Elin RJ et al. Recommendation on an updated standardization of serum magnesium reference ranges. Eur J Nutr 2022;61:3697–3706.', 'https://doi.org/10.1007/s00394-022-02916-w'],
 'debaaij2022': ['de Baaij 2022', 'de Baaij JHF et al. Comment to „Recommendation on an updated standardization of serum magnesium reference ranges“. Eur J Nutr 2022;61:4231–4233.', 'https://doi.org/10.1007/s00394-022-03004-9'],
 'kappeler2017': ['Kappeler 2017', 'Kappeler D, Heimbeck I, Herpich C et al. Higher bioavailability of magnesium citrate as compared to magnesium oxide shown by evaluation of urinary excretion and serum levels after single-dose administration in a randomized cross-over study. BMC Nutr 2017;3:7.', 'https://doi.org/10.1186/s40795-016-0121-3'],
 'pardo2021': ['Pardo 2021', 'Pardo MR, Garicano Vilar E, San Mauro Martín I, Camina Martín MA. Bioavailability of magnesium food supplements: A systematic review. Nutrition 2021;89:111294.', 'https://doi.org/10.1016/j.nut.2021.111294'],
 'schuette1994': ['Schuette 1994', 'Schuette SA, Lashner BA, Janghorbani M. Bioavailability of magnesium diglycinate vs magnesium oxide in patients with ileal resection. JPEN 1994;18(5):430–435.', 'https://doi.org/10.1177/0148607194018005430'],
 'pajuelo2024': ['Pajuelo 2024', 'Pajuelo D et al. Comparative Clinical Study on Magnesium Absorption and Side Effects After Oral Intake of Microencapsulated Magnesium Compared to Other Magnesium Sources. Nutrients 2024;16(24):4367.', 'https://doi.org/10.3390/nu16244367'],
 'garrison2020': ['Garrison 2020', 'Garrison SR, Korownyk CS, Kolber MR et al. Magnesium for skeletal muscle cramps. Cochrane Database Syst Rev 2020;9:CD009402.', 'https://doi.org/10.1002/14651858.CD009402.pub3'],
 'efsa_claims2009': ['EFSA 2009', 'EFSA NDA Panel. Scientific Opinion on the substantiation of health claims related to magnesium … EFSA Journal 2009;7(9):1216.', 'https://doi.org/10.2903/j.efsa.2009.1216'],
 'magpie2002': ['Magpie 2002', 'The Magpie Trial Collaborative Group. Do women with pre-eclampsia, and their babies, benefit from magnesium sulphate? Lancet 2002;359:1877–1890.', 'https://doi.org/10.1016/s0140-6736(02)08778-0'],
 'argeros2025': ['Argeros 2025', 'Argeros Z et al. Magnesium Supplementation and Blood Pressure: A Systematic Review and Meta-Analysis of Randomized Controlled Trials. Hypertension 2025;82(11):1844–1856.', 'https://doi.org/10.1161/HYPERTENSIONAHA.125.25129'],
 'dgn2025': ['DGN 2025', 'Diener HC, Kropp P et al. Therapie der Migräneattacke und Prophylaxe der Migräne, S1-Leitlinie (DGN/DMKG), AWMF 030-057, 2025.', 'https://www.dgn.org/cms-content/030057_LL_Migra%CC%88ne_2025_V7_1757058404145.pdf'],
 'mah2021': ['Mah 2021', 'Mah J, Pitre T. Oral magnesium supplementation for insomnia in older adults: a Systematic Review & Meta-Analysis. BMC Complement Med Ther 2021;21:125.', 'https://doi.org/10.1186/s12906-021-03297-z'],
 'schuster2025': ['Schuster 2025', 'Schuster J et al. Magnesium Bisglycinate Supplementation in Healthy Adults Reporting Poor Sleep: A Randomized, Placebo-Controlled Trial. Nat Sci Sleep 2025;17:2027–2040.', 'https://doi.org/10.2147/NSS.S524348'],
 'boyle2017': ['Boyle 2017', 'Boyle NB, Lawton C, Dye L. The Effects of Magnesium Supplementation on Subjective Anxiety and Stress – A Systematic Review. Nutrients 2017;9(5):429.', 'https://doi.org/10.3390/nu9050429'],
 'bfr2021': ['BfR 2021', 'Bundesinstitut für Risikobewertung. Höchstmengenvorschläge für Magnesium in Lebensmitteln inklusive Nahrungsergänzungsmitteln, 2021 (bestätigt in Stellungnahme 006/2024).', 'https://www.bfr.bund.de/cm/343/hoechstmengenvorschlaege-fuer-magnesium-in-lebensmitteln-inklusive-nahrungsergaenzungsmitteln.pdf'],
 'scf2001': ['SCF 2001', 'Scientific Committee on Food. Opinion on the Tolerable Upper Intake Level of Magnesium, 2001.', 'https://ec.europa.eu/food/fs/sc/scf/out105_en.pdf'],
 'fi_jenapharm': ['Fachinformation 2016', 'Fachinformation Magnesium 100 mg JENAPHARM, Tabletten, Stand April 2016 (Abschnitte 4.3–4.5).', 'https://fachinfo.de/pdf/011345'],
 'fine1991': ['Fine 1991', 'Fine KD, Santa Ana CA, Porter JL, Fordtran JS. Intestinal absorption of magnesium from food and supplements. J Clin Invest 1991;88(2):396–402.', 'https://doi.org/10.1172/JCI115317'],
 'pubmed_suche': ['eigene Suche 2026', 'Eigene PubMed-Suche 14.11.2026: Magnesium und Einnahmezeitpunkt (morning/evening/bedtime/time of day), 2015–2026, 13 Treffer, keine Vergleichsstudie.', 'https://pubmed.ncbi.nlm.nih.gov/'],
}
Q = {k: {'kurz': a, 'voll': b, 'url': c} for k, (a, b, c) in QUELLEN.items()}


def S(t, say=None):
    return {'t': t, 'say': say} if say else t


def B(t, at):
    return {'t': t, 'at': at}


ABSCHLUSS = 'Gut, dass du dich informierst. Das Video kann das Gespräch mit Arzt oder Ärztin unterstützen, aber nicht ersetzen. Bis zum nächsten Video!'

SZENEN = [
 {'id': 'm0', 'layout': 'kacheln', 'kapitel': 'Einleitung', 'kicker': 'Erklärvideo', 'headline': 'Magnesium: der Überblick',
  'sentences': ['Magnesium: morgens oder abends? Citrat oder Bisglycinat? Und brauchst du es überhaupt?',
                'Überraschend: Welche Tageszeit besser ist, hat bis heute keine einzige Studie verglichen.',
                'Du erfährst, wozu dein Körper Magnesium braucht, wie viel und woher, wie häufig ein Mangel ist, welche Präparate es gibt, wofür es belegt ist und worauf du bei der Einnahme achtest.'],
  'hervorheben_at': 2,
  'hook_bild': 'thumbnail/bild_G.jpg', 'kacheln_ab': 2, 'hook_titel': 'Magnesium',
  'hook_zeilen': [{'t': 'Morgens oder abends?', 'wort': 'morgens'}, {'t': 'Citrat oder Bisglycinat?', 'wort': 'Zitrat'},  # wort = Sprechtext (Aussprache)
                  {'t': 'Brauchst du es überhaupt?', 'wort': 'überhaupt'},
                  {'t': 'Tageszeit: nie verglichen.', 'wort': 'keine einzige', 'art': 'urteil'}],
  'kacheln': [('Wozu der Körper es braucht', 'k1', 'Körper'), ('Wie viel und woher', 'k2', 'woher'),
              ('Mangel: selten oder häufig?', 'k3', 'Mangel'), ('Präparate und Formen', 'k4', 'Präparate'),
              ('Wofür belegt, wofür nicht', 'k5', 'belegt'), ('Sicher einnehmen', 'k6', 'Einnahme')]},

 {'id': 'm1', 'kicker': 'Im Körper', 'headline': 'Wozu der Körper es braucht',
  'sentences': ['In deinem Körper stecken etwa vierundzwanzig Gramm Magnesium, so schwer wie drei Zwei-Euro-Münzen.',
                'Gut die Hälfte sitzt in den Knochen, ein Viertel in den Muskeln. Im Blut ist weniger als ein Prozent.',
                'Es ist an Hunderten Reaktionen im Stoffwechsel beteiligt. Der Energieträger der Zellen, ATP, arbeitet meist im Paar mit Magnesium.',
                'Im Muskel hilft es beim Entspannen, als Gegenspieler von Calcium. An Nervenzellen sitzt es wie ein Stöpsel in einem Kanal.',
                S('Den Haushalt regeln die Nieren: Sie filtern jeden Tag rund 2,4 Gramm und holen fast alles zurück.',
                  'Den Haushalt regeln die Nieren: Sie filtern jeden Tag rund zweieinhalb Gramm und holen fast alles zurück.')],
  'bullets': [B('Etwa 24 Gramm im Körper', 0), B('Im Blut: unter 1 Prozent', 1), B('Hunderte Reaktionen, Energie', 2),
              B('Muskeln und Nerven', 3), B('Die Nieren regeln', 4)],
  'quellen': ['jahnen2012', 'debaaij2015', 'fiorentini2021', 'mayer1984'],
  'bilder': [('m1a', None), ('m1b', 1), ('m1c', 2), ('m1d', 2), ('m1e', 3), ('m1f', 3), ('m1g', 4)]},

 {'id': 'm2', 'kicker': 'Zufuhr', 'headline': 'Wie viel und woher',
  'sentences': [S('Wie viel brauchst du? Die Deutsche Gesellschaft für Ernährung schätzt: Frauen etwa 300, Männer etwa 350 Milligramm am Tag.',
                  'Wie viel brauchst du? Die Deutsche Gesellschaft für Ernährung schätzt: Frauen etwa dreihundert, Männer etwa dreihundertfünfzig Milligramm am Tag.'),
                'Das sind Schätzwerte, denn einen genauen Bedarf kennt niemand.',
                'Viel Magnesium steckt in Kernen, Nüssen, Haferflocken, Vollkorn und Hülsenfrüchten. Eine Handvoll Sonnenblumenkerne bringt etwa hundert Milligramm.',
                'In Deutschland kommt das meiste aber aus Getränken und Brot.',
                'Mineralwasser darf „magnesiumhaltig“ heißen, wenn ein Liter mehr als fünfzig Milligramm enthält.',
                'Und beim Weißmehl bleibt von sechs Teilen Magnesium nur eines übrig.',
                'Tipp: Vollkorn statt Weißbrot und weißem Reis bringt am Tag etwa so viel wie eine kleine Magnesiumtablette.'],
  'bullets': [B('Frauen 300, Männer 350 mg', 0), B('Kerne, Nüsse, Vollkorn', 2), B('Wasser: über 50 mg pro Liter', 4),
              B('Weißmehl: ein Sechstel', 5), B('Tipp: Vollkorn statt Weiß', 6)],
  'quellen': ['dge_web', 'efsa2015', 'bls2025', 'mri2008', 'mintafelwv'],
  'bilder': [('m2a', None), ('m2b', 1), ('m2c', 2), ('m2d', 3), ('m2e', 4), ('m2f', 5), ('m2g', 6)]},

 {'id': 'm3', 'kicker': 'Mangel', 'headline': 'Selten oder häufig?',
  'sentences': ['Oft heißt es, die meisten Menschen hätten einen Magnesiummangel. Eine Quelle dafür gibt es nicht.',
                'In der letzten großen Verzehrsstudie lag gut jeder Vierte unter der damaligen Empfehlung, bei Mädchen im Teenageralter mehr als die Hälfte.',
                'Das ist aber kein Mangel: Gezählt wurde nur, was auf dem Teller lag, und die Daten sind fast zwanzig Jahre alt.',
                'Einen echten Mangel bekommen vor allem Menschen mit bestimmten Medikamenten oder Krankheiten.',
                'Etwa Magenschutz-Tabletten über Jahre, manche Entwässerungstabletten, Alkoholkrankheit, schlecht eingestellter Diabetes oder anhaltender Durchfall.',
                'Und der Bluttest? Weil kaum Magnesium im Blut ist, schließt ein normaler Wert knappe Vorräte nicht sicher aus. Für einen echten Mangel ist er trotzdem der übliche Test.',
                'Tipp: Gehörst du zu einer dieser Gruppen, lass deinen Wert von Arzt oder Ärztin prüfen.'],
  'bullets': [B('„Die meisten haben Mangel“: keine Quelle', 0), B('Jeder Vierte unter der Empfehlung', 1),
              B('Risiko: Medikamente, Krankheiten', 4), B('Bluttest: begrenzt aussagekräftig', 5)],
  'quellen': ['mri2008', 'dge_faq', 'ahmed2019', 'liamis2021', 'srinutta2019', 'rosanoff2022', 'debaaij2022'],
  'bilder': [('m3a', None), ('m3b', 1), ('m3c', 2), ('m3d', 3), ('m3e', 4), ('m3f', 5), ('m3g', 6)]},

 {'id': 'm4', 'kicker': 'Im Regal', 'headline': 'Präparate und Formen',
  'sentences': ['Im Regal stehen Citrat, Bisglycinat, Oxid und teure Spezialformen.',
                'Gut lösliche Formen wie Citrat werden etwas besser aufgenommen als Oxid.',
                'Der Unterschied ist klein: In einer kleinen Herstellerstudie waren es nach einer Tablette nur etwa vierzehn Milligramm mehr im Urin.',
                'Bisglycinat schnitt in den wenigen Vergleichen nicht besser ab als einfache Formen.',
                'Für Taurat, Malat oder Mischungen aus vielen Formen gibt es keine Vergleichsstudien am Menschen.',
                'Die eigentliche Grenze ist der Darm: Jede Form kann in höherer Dosis Durchfall machen.',
                'Tipp: Ein teurer Name ist kein Beleg. Schau lieber, wie viele Milligramm Magnesium eine Portion enthält.'],
  'bullets': [B('Citrat etwas besser als Oxid', 1), B('Unterschied klein', 2), B('Spezialformen: kaum verglichen', 4),
              B('Grenze: Durchfall', 5)],
  'quellen': ['kappeler2017', 'pardo2021', 'schuette1994', 'pajuelo2024', 'garrison2020'],
  'bilder': [('m4a', None), ('m4b', 1), ('m4c', 2), ('m4d', 3), ('m4e', 4), ('m4f', 5), ('m4g', 6)]},

 {'id': 'm5', 'kicker': 'Studienlage', 'headline': 'Wofür belegt, wofür nicht',
  'sentences': ['Auf Packungen steht oft: trägt zur normalen Muskelfunktion bei. Das heißt nur: Ohne Magnesium arbeiten Muskeln nicht richtig. Es heißt nicht: Mehr hilft mehr.',
                'Zugelassen ist Magnesium in der Klinik: als Infusion gegen Krampfanfälle bei der Schwangerschaftskomplikation Eklampsie.',
                'Blutdruck: gut untersucht. Er sinkt leicht, vor allem bei Menschen mit Bluthochdruck.',
                'Migräne: in kleinen Studien untersucht. Die Leitlinie nennt Magnesium zur Vorbeugung, mit geringer Beweislage.',
                'Schlaf, Stress und Angst: kleine Studien, kleine Effekte, oft von Herstellern bezahlt. Viele berichten, dass sie besser schlafen, belegt ist das kaum.',
                'Und die nächtlichen Wadenkrämpfe älterer Menschen? Gut untersucht, und hier wirkt Magnesium nicht besser als ein Scheinpräparat.'],
  'bullets': [B('Klinik, Eklampsie: zugelassen', 1), B('Blutdruck: gut untersucht, leicht', 2),
              B('Migräne: kleine Studien', 3), B('Schlaf, Stress: kaum belegt', 4), B('Krämpfe im Alter: wirkt nicht', 5)],
  'quellen': ['efsa_claims2009', 'magpie2002', 'argeros2025', 'dgn2025', 'mah2021', 'schuster2025', 'boyle2017', 'garrison2020'],
  'bilder': [('m5a', None), ('m5b', 1), ('m5c', 2), ('m5d', 3), ('m5e', 4), ('m5f', 5)]},

 {'id': 'm6', 'kicker': 'Vorsicht', 'headline': 'Selbstanwendung: was kritisch ist',
  'sentences': [S('Das Bundesinstitut für Risikobewertung rät: aus Präparaten höchstens 250 Milligramm am Tag zusätzlich, verteilt auf mindestens zwei Portionen.',
                  'Das Bundesinstitut für Risikobewertung rät: aus Präparaten höchstens zweihundertfünfzig Milligramm am Tag zusätzlich, verteilt auf mindestens zwei Portionen.'),
                'Darüber droht Durchfall. Gefährlich viel im Blut wird es fast nur bei kranken Nieren, dann nur nach ärztlicher Rücksprache.',
                'Magnesium stört die Aufnahme mancher Medikamente, etwa bestimmter Antibiotika, Osteoporose-Tabletten oder HIV-Mittel. Wie viele Stunden Abstand nötig sind, steht im Beipackzettel des anderen Mittels.',
                'Und morgens oder abends? Das hat keine Studie verglichen. Belegt ist nur: Kleinere Portionen werden anteilig besser aufgenommen.',
                'Tipp: Sprich mit Arzt oder Ärztin, bevor du Magnesium dauerhaft nimmst, besonders wenn du Medikamente nimmst oder deine Nieren schwach sind.'],
  'bullets': [B('Höchstens 250 mg zusätzlich, aufgeteilt', 0), B('Nierenschwäche: nur mit Rücksprache', 1),
              B('Abstand zu manchen Medikamenten', 2), B('Tageszeit: nicht untersucht', 3)],
  'quellen': ['bfr2021', 'scf2001', 'fi_jenapharm', 'liamis2021', 'fine1991', 'pubmed_suche'],
  'bilder': [('m6a', None), ('m6b', 1), ('m6c', 2), ('m6d', 3), ('m6e', 4)]},

 {'id': 'm7', 'kapitel': 'Fazit', 'kicker': 'Fazit', 'headline': 'Kurz gesagt',
  'sentences': ['Also: Morgens oder abends? Das ist offen. Größere Mengen teilst du besser auf.',
                'Citrat oder Bisglycinat? Die Unterschiede zwischen den Formen sind klein.',
                'Und brauchst du es überhaupt? Wer gesund ist und ausgewogen isst, meist nicht. Wer zu einer Risikogruppe gehört, lässt es prüfen.',
                'Belegt: ein leichter Effekt auf den Blutdruck. Unklar: Schlaf, Stress und Migräne. Achte auf Obergrenze, Nieren und Medikamente.'],
  'bullets': [B('Belegt: Blutdruck leicht, Klinik', 3), B('Unklar: Schlaf, Stress, Migräne', 3),
              B('Form: Unterschiede klein', 1), B('Achten: 250 mg, Nieren, Medikamente', 3)],
  'quellen': ['argeros2025', 'kappeler2017', 'bfr2021'],
  'bilder': [('m7a', None), ('m7b', 1), ('m7c', 2), ('m7d', 3)]},

 {'id': 'm8', 'layout': 'kacheln', 'kapitel': 'Die Reihe', 'kicker': 'Erklärvideo', 'headline': 'Alles über Magnesium: die Reihe',
  'sentences': ['In den nächsten Folgen geht es um jede Frage einzeln: morgens oder abends, welche Formen, Mangel erkennen, die Obergrenze, Schlaf und Stress. Danach Krämpfe, Blutdruck, Migräne, Frauen und Lebensmittel.',
                'Als Nächstes: Warum hält sich der Rat, Magnesium abends zu nehmen, so hartnäckig?',
                # Keine Kommentarfrage (Nutzerentscheidung 4c, 14.11.)
                ABSCHLUSS],
  'hervorheben_at': 0,
  'kacheln': [('Morgens oder abends?', 'r2', 'abends'), ('Welche Form?', 'r3', 'Formen'),
              ('Mangel erkennen', 'r4', 'Mangel'), ('Wie viel ist zu viel?', 'r5', 'Obergrenze'),
              ('Schlaf', 'r6', 'Schlaf'), ('Stress und Angst', 'r7', 'Stress')]},
]


def da(stil, b):
    return os.path.exists(f'bilder/{stil}/{b}.jpg')


def bauen(stil):
    szenen = []
    for sc in SZENEN:
        s = {k: v for k, v in sc.items() if k not in ('bilder', 'kacheln')}
        if 'kacheln' in sc:
            s['kacheln'] = [{'t': t, 'bild': f'bilder/{stil}/{b}.jpg', 'wort': w} for t, b, w in sc['kacheln']]
        if 'bilder' in sc:
            liste = [(b, at) for b, at in sc['bilder'] if da(stil, b)] or [(sc['bilder'][0][0], None)]
            liste[0] = (liste[0][0], None)
            s['shots'] = [dict({'bild': f'bilder/{stil}/{b}.jpg'}, **({'at': at} if at is not None else {})) for b, at in liste]
        szenen.append(s)
    return {'tts': 'elevenlabs', 'voice_id': 'NBqeXKdZHweef6y0B67V', 'model': 'eleven_v4', 'tempo': 1.05,
            'aussprache': AUSSPRACHE,
            'titel': 'Magnesium: Was du wirklich wissen musst', 'stil': stil,
            'untertitel': 'Folge 1 der Magnesium-Reihe: wozu der Körper Magnesium braucht, wie viel und woher, wie häufig ein Mangel ist, welche Formen es gibt, wofür es belegt ist und worauf du bei der Einnahme achten solltest.',
            'fuss': 'Sprecherstimme synthetisch (ElevenLabs). Bilder KI-generiert. Das Video ersetzt nicht das Gespräch mit Arzt oder Ärztin.',
            'scenes': szenen, 'quellen': Q}


# Aussprache (vorläufig, Proben folgen): Fachwörter eingedeutscht
AUSSPRACHE = {'Bisglycinat': 'Bisglyzinat', 'Citrat': 'Zitrat', 'ATP': 'A T P', 'Eklampsie': 'Eklampsie'}

if __name__ == '__main__':
    for stil in STILE:
        json.dump(bauen(stil), open(f'szenen_{stil}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(bauen('G'), open('szenen.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    w = sum(len((x if isinstance(x, str) else x['t']).split()) for sc in SZENEN for x in sc['sentences'])
    z = sum(len((x if isinstance(x, str) else x.get('say', x['t']))) for sc in SZENEN for x in sc['sentences'])
    print(len(STILE), 'Drehbuch,', w, 'Wörter,', z, 'Zeichen, ≈', round(w / 2.28 / 60, 1), 'min')
    for sc in SZENEN:
        print(sc['id'], sum(len((x if isinstance(x, str) else x['t']).split()) for x in sc['sentences']))
