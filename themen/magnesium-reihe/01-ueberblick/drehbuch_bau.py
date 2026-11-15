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
 'fuller1662': ['Fuller 1662', 'Fuller T. The History of the Worthies of England, Surrey: „Medicinal Waters. Ebsham.“ London 1662.', 'https://distantreader.org/stacks/earlyprint/txt/A40672.txt'],
 'black1756': ['Black 1756', 'Black J. Experiments upon Magnesia Alba, Quick-lime, and other Alcaline Substances. Essays and Observations, Physical and Literary 1756;2:157–225.', 'https://www.gutenberg.org/ebooks/24591'],
 'davy1808': ['Davy 1808', 'Davy H. Electro-chemical researches, on the decomposition of the earths. Phil Trans R Soc Lond 1808;98:333–370.', 'https://doi.org/10.1098/rstl.1808.0023'],
 'gi_bittersalz': ['Gebrauchsinformation Bittersalz 2025', 'Gebrauchsinformation Bittersalz, Zul.-Nr. 1199.99.99, überarbeitet 01/2025.', 'https://cdn.shop-apotheke.com/PDF/D01/569/860/D01569860-bp.pdf'],
 'dgvs2022': ['DGVS 2022', 'Andresen V et al. Aktualisierte S2k-Leitlinie chronische Obstipation (DGVS/DGNM). Z Gastroenterol 2022;60:1528–1572.', 'https://doi.org/10.1055/a-1880-1928'],
 'gi_verla': ['Gebrauchsinformation Magnesium Verla 2022', 'Gebrauchsinformation Magnesium Verla N Dragées, Anwendungsgebiet nachgewiesener Magnesiummangel, überarbeitet 07/2022.', 'https://patienteninfo-service.de/gi/7130/pdf'],
}
Q = {k: {'kurz': a, 'voll': b, 'url': c} for k, (a, b, c) in QUELLEN.items()}


def S(t, say=None):
    return {'t': t, 'say': say} if say else t


def B(t, at):
    return {'t': t, 'at': at}


ABSCHLUSS = 'Gut, dass du dich informierst. Das Video kann das Gespräch mit Arzt oder Ärztin unterstützen, aber nicht ersetzen. Bis zum nächsten Video!'

SZENEN = [
 # Umbau 15.11. (Nutzer: „Folge 1 umbauen“): kein Inhaltsverzeichnis, Reihenfolge nach Nachfrage, Belegtes vor den
 # Grenzen, Wende in der Mitte (Wadenkrämpfe), Geschichte (Bittersalz) bei den Formen, Karte als offene Fragen.
 {'id': 'm0', 'layout': 'kacheln', 'kapitel': 'Einleitung', 'kicker': 'Erklärvideo', 'headline': 'Magnesium: der Überblick',
  'sentences': ['Magnesium: Was du wirklich wissen musst.',  # Nutzer 15.11.: Titel des Vorschaubilds gesprochen
                'Morgens oder abends? Citrat oder Bisglycinat? Und brauchst du es überhaupt?',
                'Überraschend: Welche Tageszeit besser ist, hat bis heute keine einzige Studie verglichen.',
                'Wem hilft Magnesium wirklich, und wem nicht? Wir klären, ob du es überhaupt brauchst, wem es hilft, wo es nicht hilft, welche Form taugt, wie du es sicher einnimmst und was im Essen steckt.'],  # Nutzer 15.11.: Startvariante A
  'hervorheben_at': 3,
  'hook_bild': 'thumbnail/bild_G.jpg', 'kacheln_ab': 3, 'hook_titel': 'Magnesium',
  'hook_stil': 'vorschaubild', 'hook_untertitel': ['Was du wirklich', 'wissen musst'],  # Nutzer 15.11.: erstes Bild = Vorschaubild, ohne Zierstrich
  'hook_zeilen': [{'t': 'Morgens oder abends?', 'wort': 'Morgens'}, {'t': 'Citrat oder Bisglycinat?', 'wort': 'Zitrat'},  # wort = Sprechtext (Aussprache)
                  {'t': 'Brauchst du es überhaupt?', 'wort': 'überhaupt'},
                  {'t': 'Tageszeit: nie verglichen.', 'wort': 'keine einzige', 'art': 'urteil'}],
  # Startvariante A (Nutzer 15.11.): Übersicht gesprochen, jede Kachel leuchtet beim Wort
  'kacheln': [('Brauchst du es überhaupt?', 'k3', 'Wir klären'), ('Wem es hilft', 'k7', 'wem es hilft'),
              ('Wo es nicht hilft', 'k8', 'wo es nicht'), ('Welche Form?', 'k4', 'welche Form'),
              ('Sicher einnehmen', 'k6', 'sicher'), ('Aus dem Essen', 'k2', 'Essen')]},

 {'id': 'm1', 'kapitel_nr': 1, 'kicker': 'Kapitel 1 · Mangel', 'headline': 'Brauchst du es überhaupt?',
  'sentences': ['Oft heißt es, die meisten Menschen hätten zu wenig Magnesium. Eine Quelle dafür gibt es nicht.',
                'In der letzten großen Verzehrsstudie lag gut jeder Vierte unter der damaligen Empfehlung. Das ist aber kein Mangel: Gezählt wurde nur, was auf dem Teller lag, und die Daten sind fast zwanzig Jahre alt.',
                S('Die Deutsche Gesellschaft für Ernährung schätzt den Bedarf auf etwa 300 Milligramm für Frauen und 350 für Männer.',
                  'Die Deutsche Gesellschaft für Ernährung schätzt den Bedarf auf etwa dreihundert Milligramm für Frauen und dreihundertfünfzig für Männer.'),
                'Einen echten Mangel bekommen vor allem Menschen mit bestimmten Medikamenten oder Krankheiten: Magenschutz-Tabletten über Jahre, manche Entwässerungstabletten, Alkoholkrankheit, schlecht eingestellter Diabetes oder anhaltender Durchfall.',
                'Und der Bluttest? In deinem Körper stecken etwa vierundzwanzig Gramm Magnesium, so schwer wie drei Zwei-Euro-Münzen. Im Blut ist davon weniger als ein Prozent.',
                'Ein niedriger Wert zeigt einen echten Mangel an. Ein normaler Wert schließt knappe Vorräte aber nicht aus. Einen besseren Test gibt es bisher nicht.',
                'Tipp: Gehörst du zu einer dieser Gruppen, sprich mit Arzt oder Ärztin darüber, nicht nur über den Blutwert.'],
  'bullets': [B('„Die meisten haben Mangel“: keine Quelle', 0), B('Bedarf: Frauen 300, Männer 350 mg', 2),
              B('Risiko: Medikamente, Krankheiten', 3), B('Im Blut: unter 1 Prozent', 4), B('Bluttest: findet Mangel, schließt ihn nicht aus', 5)],
  'quellen': ['mri2008', 'dge_faq', 'dge_web', 'ahmed2019', 'liamis2021', 'srinutta2019', 'jahnen2012', 'rosanoff2022', 'debaaij2022'],
  'bilder': [('m3a', None), ('m3c', 1), ('m2b', 2), ('m3e', 3), ('m1a', 4), ('m3f', 5), ('m3g', 6)]},

 {'id': 'm2', 'kapitel_nr': 2, 'kicker': 'Kapitel 2 · Studienlage', 'headline': 'Wem es hilft',
  'sentences': ['Wem hilft Magnesium also wirklich?',
                'Zuerst Menschen mit nachgewiesenem Mangel. Dafür gibt es zugelassene Arzneimittel, etwa wenn der Mangel die Muskeln stört.',
                'Denn Magnesium ist an Hunderten Reaktionen im Körper beteiligt. Im Muskel hilft es beim Entspannen, als Gegenspieler von Calcium.',
                'Bei Bluthochdruck ist es gut untersucht: Der Druck sinkt leicht. Bei normalem Blutdruck zeigte sich kein klarer Effekt.',
                'Bei Migräne nennt die Leitlinie Magnesium zur Vorbeugung, mit geringer Beweislage.',
                'Und in der Klinik ist es ein zugelassenes Mittel: als Infusion gegen Krampfanfälle bei der Schwangerschaftskomplikation Eklampsie.',
                'Tipp: Bei Bluthochdruck oder Migräne ersetzt Magnesium keine Behandlung. Sprich mit Arzt oder Ärztin, ob es für dich passt.'],
  'bullets': [B('Nachgewiesener Mangel: zugelassen', 1), B('Bluthochdruck: gut untersucht, leicht', 3),
              B('Migräne: geringe Beweislage', 4), B('Eklampsie: Infusion, zugelassen', 5)],
  'quellen': ['gi_verla', 'debaaij2015', 'jahnen2012', 'argeros2025', 'dgn2025', 'magpie2002'],
  'bilder': [('m2x', None), ('m3g', 1), ('m1e', 2), ('m5c', 3), ('m5d', 4), ('m5b', 5), ('m6e', 6)]},

 {'id': 'm3', 'kapitel_nr': 3, 'kicker': 'Kapitel 3 · Die Wende', 'headline': 'Wo es nicht hilft',
  'sentences': ['Und wofür nehmen es die meisten? Gegen Wadenkrämpfe. Viele berichten, dass es ihnen hilft.',
                'Doch genau das ist gut untersucht. Bei den nächtlichen Krämpfen älterer Menschen wirkt Magnesium nicht besser als ein Scheinpräparat.',
                'In der Schwangerschaft sind die Studien widersprüchlich.',
                'Auch für Schlaf, Stress und Angst gibt es nur kleine Studien mit kleinen Effekten, oft von Herstellern bezahlt. Viele berichten, dass sie besser schlafen, belegt ist das kaum.',
                'Auf Packungen steht oft: trägt zur normalen Muskelfunktion bei. Das heißt nur: Ohne Magnesium arbeiten Muskeln nicht richtig. Es heißt nicht: Mehr hilft mehr.',
                'Tipp: Kommen Krämpfe oft wieder, lass die Ursache abklären, statt nur Tabletten zu nehmen.'],
  'bullets': [B('Krämpfe im Alter: wirkt nicht', 1), B('Schwangerschaft: widersprüchlich', 2),
              B('Schlaf, Stress: kaum belegt', 3), B('„Muskelfunktion“: kein Mehr-hilft-mehr', 4)],
  'quellen': ['garrison2020', 'mah2021', 'schuster2025', 'boyle2017', 'efsa_claims2009'],
  'bilder': [('m5f', None), ('m4c', 1), ('m3y', 2), ('m5e', 3), ('m5a', 4), ('m3g', 5)]},

 {'id': 'm4', 'kapitel_nr': 4, 'kicker': 'Kapitel 4 · Im Regal', 'headline': 'Welche Form?',
  'sentences': ['Die älteste Magnesium-Arznei ist ein Abführmittel.',
                S('Der Überlieferung nach fand ein Mann namens Henry Wicker 1618 im englischen Epsom eine Wasserstelle, aus der das durstige Vieh nicht trinken wollte. Das Wasser schmeckte bitter.',
                  'Der Überlieferung nach fand ein Mann namens Henry Wicker sechzehnhundertachtzehn im englischen Epsom eine Wasserstelle, aus der das durstige Vieh nicht trinken wollte. Das Wasser schmeckte bitter.'),
                'Daraus wurde Bittersalz. Aus ihm gewannen Forscher später auch das Metall selbst, und bis heute ist es als Abführmittel zugelassen.',
                'Damit kennst du die Grenze jeder Form: In höherer Dosis macht Magnesium Durchfall.',
                'Gut lösliche Formen wie Citrat werden etwas besser aufgenommen als Oxid. In einer kleinen Herstellerstudie waren es nach einer Tablette aber nur etwa vierzehn Milligramm mehr im Urin.',
                'Bisglycinat schnitt in den wenigen Vergleichen nicht besser ab als einfache Formen. Für Taurat, Malat oder Mischungen gibt es keine Vergleichsstudien am Menschen.',
                'Tipp: Ein teurer Name ist kein Beleg. Schau lieber, wie viele Milligramm Magnesium eine Portion enthält.'],
  'bullets': [B('Bittersalz: Epsom, überliefert 1618', 1), B('Grenze: Durchfall', 3), B('Citrat etwas besser als Oxid', 4),
              B('Spezialformen: kaum verglichen', 5)],
  'quellen': ['fuller1662', 'black1756', 'davy1808', 'gi_bittersalz', 'kappeler2017', 'pardo2021', 'schuette1994', 'pajuelo2024'],
  'bilder': [('m4x', None), ('m4y', 1), ('m4z', 2), ('m4f', 3), ('m4b', 4), ('m4e', 5), ('m4g', 6)]},

 {'id': 'm5', 'kapitel_nr': 5, 'kicker': 'Kapitel 5 · Vorsicht', 'headline': 'Sicher einnehmen',
  'sentences': [S('Das Bundesinstitut für Risikobewertung rät: aus Präparaten höchstens 250 Milligramm am Tag zusätzlich, verteilt auf mindestens zwei Portionen.',
                  'Das Bundesinstitut für Risikobewertung rät: aus Präparaten höchstens zweihundertfünfzig Milligramm am Tag zusätzlich, verteilt auf mindestens zwei Portionen.'),
                'Gefährlich viel im Blut wird es fast nur bei kranken Nieren, dann nur nach ärztlicher Rücksprache.',
                'Magnesium stört die Aufnahme mancher Medikamente, etwa bestimmter Antibiotika, Osteoporose-Tabletten oder HIV-Mittel. Wie viele Stunden Abstand nötig sind, steht im Beipackzettel des anderen Mittels.',
                'Und morgens oder abends? Das hat keine Studie verglichen. Belegt ist nur: Kleinere Portionen werden anteilig besser aufgenommen.',
                'Tipp: Sprich mit Arzt oder Ärztin, bevor du Magnesium dauerhaft nimmst, besonders wenn du Medikamente nimmst oder deine Nieren schwach sind.'],
  'bullets': [B('Höchstens 250 mg zusätzlich, aufgeteilt', 0), B('Nierenschwäche: nur mit Rücksprache', 1),
              B('Abstand zu manchen Medikamenten', 2), B('Tageszeit: nicht untersucht', 3)],
  'quellen': ['bfr2021', 'scf2001', 'fi_jenapharm', 'liamis2021', 'fine1991', 'pubmed_suche'],
  'bilder': [('m6a', None), ('m6b', 1), ('m6c', 2), ('m6d', 3), ('m6e', 4)]},

 {'id': 'm6', 'kapitel_nr': 6, 'kicker': 'Kapitel 6 · Zufuhr', 'headline': 'Aus dem Essen',
  'sentences': ['Viel Magnesium steckt in Kernen, Nüssen, Haferflocken, Vollkorn und Hülsenfrüchten. Eine Handvoll Sonnenblumenkerne bringt etwa hundert Milligramm.',
                'In Deutschland kommt das meiste aber aus Getränken und Brot.',
                'Mineralwasser darf „magnesiumhaltig“ heißen, wenn ein Liter mehr als fünfzig Milligramm enthält.',
                'Und beim Weißmehl bleibt von sechs Teilen Magnesium nur eines übrig.',
                'Tipp: Vollkorn statt Weißbrot und weißem Reis bringt am Tag etwa so viel wie eine kleine Magnesiumtablette.'],
  'bullets': [B('Kerne, Nüsse, Vollkorn', 0), B('Wasser: über 50 mg pro Liter', 2), B('Weißmehl: ein Sechstel', 3),
              B('Tipp: Vollkorn statt Weiß', 4)],
  'quellen': ['bls2025', 'mri2008', 'mintafelwv'],
  'bilder': [('m2c', None), ('m2d', 1), ('m2e', 2), ('m2f', 3), ('m2g', 4)]},

 {'id': 'm7', 'kapitel_nr': 'fazit', 'kapitel': 'Fazit', 'kicker': 'Fazit', 'headline': 'Kurz gesagt',
  'sentences': ['Also: Brauchst du Magnesium? Es hilft vor allem bei echtem Mangel, und es senkt hohen Blutdruck leicht. Für alle anderen reicht meist das Essen.',
                'Citrat oder Bisglycinat? Die Unterschiede zwischen den Formen sind klein.',
                'Morgens oder abends? Das ist offen. Größere Mengen teilst du besser auf.',
                'Und achte auf die Obergrenze, deine Nieren und deine Medikamente.'],
  'bullets': [B('Hilft: echter Mangel, Blutdruck leicht', 0), B('Form: Unterschiede klein', 1),
              B('Tageszeit offen, aufteilen', 2), B('Achten: 250 mg, Nieren, Medikamente', 3)],
  'quellen': ['gi_verla', 'argeros2025', 'kappeler2017', 'bfr2021'],
  'bilder': [('m7c', None), ('m7b', 1), ('m7a', 2), ('m7d', 3)]},

 {'id': 'm8', 'layout': 'kacheln', 'kapitel': 'Die Reihe', 'kicker': 'Erklärvideo', 'headline': 'Alles über Magnesium: die Reihe',
  'sentences': ['Als Nächstes: Warum hält sich der Rat, Magnesium abends zu nehmen, so hartnäckig?',
                'Danach: Welche Form passt wozu? Woran erkennst du einen Mangel? Ab wann ist es zu viel? Und was zeigen die Studien zu Schlaf und Stress?',
                'Es folgen Krämpfe, Blutdruck, Migräne, Frauen und Lebensmittel.',
                # Keine Kommentarfrage (Nutzerentscheidung 4c, 14.11.)
                ABSCHLUSS],
  'hervorheben_at': 0,
  'kacheln': [('Warum abends?', 'r2', 'abends'), ('Welche Form wozu?', 'r3', 'Form'),
              ('Mangel erkennen?', 'r4', 'Mangel'), ('Wann zu viel?', 'r5', 'zu viel'),
              ('Hilft es beim Schlaf?', 'r6', 'Schlaf'), ('Hilft es bei Stress?', 'r7', 'Stress')]},
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
            'untertitel': 'Folge 1 der Magnesium-Reihe: ob du Magnesium überhaupt brauchst, wem es hilft und wem nicht, welche Form taugt, wie du es sicher einnimmst und was im Essen steckt.',
            'fuss': 'Unabhängig: keine Sponsoren, keine Affiliate-Links, keine eigenen Produkte. Recherche-Stand: November 2026. Sprecherstimme synthetisch (ElevenLabs). Bilder KI-generiert. Das Video ersetzt nicht das Gespräch mit Arzt oder Ärztin.',
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
