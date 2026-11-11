"""Drehbuch „L-Theanin: Was der Stoff aus dem Tee kann“ (Erklärvideo im Schulprojekt-Ton wie themen/dmso, keine Ampel),
nur Stil G (Aquarell und Tusche). Fakten und Quellen: faktencheck.md, recherche_A.md, recherche_B.md (11.11.2026).
Dosierungen nur als Beschreibung der Studien, keine Empfehlung, keine Marken. Aufruf: python3 drehbuch_bau.py"""
import json, os

STILE = ['G']

QUELLEN = {
 'sakato1950': ['Sakato 1950', 'Sakato Y. Studies on the Chemical Constituents of Tea. Part III. On a New Amide Theanine. Nippon Nōgeikagaku Kaishi 1950;23(6):262–267.', 'https://doi.org/10.1271/nogeikagaku1924.23.262'],
 'ashihara2015': ['Ashihara 2015', 'Ashihara H. Occurrence, Biosynthesis and Metabolism of Theanine in Plants: A Comprehensive Review. Nat Prod Commun 2015;10(5):803–810.', 'https://doi.org/10.1177/1934578X1501000525'],
 'casimir1960': ['Casimir 1960', 'Casimir J, Jadot J, Renard M. Séparation et caractérisation de la N-éthyl-γ-glutamine à partir de Xerocomus badius. Biochim Biophys Acta 1960;39:462–468.', 'https://doi.org/10.1016/0006-3002(60)90199-2'],
 'kaneko2006': ['Kaneko 2006', 'Kaneko S, Kumazawa K, Masuda H, Henze A, Hofmann T. Molecular and Sensory Studies on the Umami Taste of Japanese Green Tea. J Agric Food Chem 2006;54:2688–2694.', 'https://doi.org/10.1021/jf0525232'],
 'keenan2011': ['Keenan 2011', 'Keenan EK, Finnie MDA, Jones PS, Rogers PJ, Priestley CM. How much theanine in a cup of tea? Food Chem 2011;125:588–594.', 'https://doi.org/10.1016/j.foodchem.2010.08.071'],
 'boros2016': ['Boros 2016', 'Boros K, Jedlinszki N, Csupor D. Theanine and Caffeine content of infusions prepared from commercial tea samples. Pharmacogn Mag 2016;12(45):75–79.', 'https://doi.org/10.4103/0973-1296.176061'],
 'mu2015': ['Mu 2015', 'Mu W, Zhang T, Jiang B. An overview of biological production of L-theanine. Biotechnol Adv 2015;33:335–342.', 'https://doi.org/10.1016/j.biotechadv.2015.04.004'],
 'fda_grn209': ['FDA 2007', 'FDA. Agency Response Letter GRAS Notice No. GRN 000209 (L-theanine), 05.02.2007.', 'https://www.hfpappexternal.fda.gov/scripts/fdcc/index.cfm?set=GRASNotices&id=209'],
 'scheid2012': ['Scheid 2012', 'Scheid L, Ellinger S, Alteheld B et al. Kinetics of L-theanine uptake and metabolism in healthy participants are comparable after ingestion of L-theanine via capsules and green tea. J Nutr 2012;142:2091–2096.', 'https://doi.org/10.3945/jn.112.166371'],
 'yokogoshi1998': ['Yokogoshi 1998', 'Yokogoshi H, Kobayashi M, Mochizuki M, Terashima T. Effect of theanine on brain monoamines and striatal dopamine release in conscious rats. Neurochem Res 1998;23:667–673.', 'https://doi.org/10.1023/a:1022490806093'],
 'kakuda2002': ['Kakuda 2002', 'Kakuda T, Nozawa A, Sugimoto A, Niino H. Inhibition by theanine of binding of [3H]AMPA, [3H]kainate, and [3H]MDL 105,519 to glutamate receptors. Biosci Biotechnol Biochem 2002;66:2683–2686.', 'https://doi.org/10.1271/bbb.66.2683'],
 'kobayashi1998': ['Kobayashi 1998', 'Kobayashi K, Nagato Y, Aoi N, Juneja LR et al. Effects of L-theanine on the release of α-brain waves in human volunteers. Nippon Nōgeikagaku Kaishi 1998;72:153–157.', 'https://doi.org/10.1271/nogeikagaku1924.72.153'],
 'gomez2009': ['Gomez-Ramirez 2009', 'Gomez-Ramirez M, Kelly SP, Montesi JL, Foxe JJ. The effects of L-theanine on alpha-band oscillatory brain activity during a visuo-spatial attention task. Brain Topogr 2009;22:44–51.', 'https://doi.org/10.1007/s10548-008-0068-z'],
 'white2016': ['White 2016', 'White DJ, de Klerk S, Woods W et al. Anti-stress, behavioural and magnetoencephalography effects of an L-theanine-based nutrient drink. Nutrients 2016;8:53.', 'https://doi.org/10.3390/nu8010053'],
 'gerolymos2026': ['Gerolymos 2026', 'Gerolymos C, Saddier E, Boyer L, Fond G. Cognitive and affective effects of L-theanine: a systematic review and meta-analysis of 31 randomized trials. Mol Psychiatry 2026;31:6592–6602.', 'https://doi.org/10.1038/s41380-026-03727-9'],
 'hidese2019': ['Hidese 2019', 'Hidese S, Ogawa S, Ota M et al. Effects of L-theanine administration on stress-related symptoms and cognitive functions in healthy adults: a randomized controlled trial. Nutrients 2019;11:2362.', 'https://doi.org/10.3390/nu11102362'],
 'moulin2024': ['Moulin 2024', 'Moulin M, Crowley DC, Xiong L et al. Safety and efficacy of AlphaWave L-theanine supplementation for 28 days in healthy adults with moderate stress. Neurol Ther 2024;13:1135–1153.', 'https://doi.org/10.1007/s40120-024-00624-7'],
 'bulman2025': ['Bulman 2025', "Bulman A, D'Cunha NM, Marx W et al. The effects of L-theanine consumption on sleep outcomes: a systematic review and meta-analysis. Sleep Med Rev 2025;81:102076.", 'https://doi.org/10.1016/j.smrv.2025.102076'],
 'sarris2019': ['Sarris 2019', 'Sarris J, Byrne GJ, Cribb L et al. L-theanine in the adjunctive treatment of generalized anxiety disorder: a double-blind, randomised, placebo-controlled trial. J Psychiatr Res 2019;110:31–37.', 'https://doi.org/10.1016/j.jpsychires.2018.12.014'],
 'camfield2014': ['Camfield 2014', 'Camfield DA, Stough C, Farrimond J, Scholey AB. Acute effects of tea constituents L-theanine, caffeine, and epigallocatechin gallate on cognitive function and mood: a systematic review and meta-analysis. Nutr Rev 2014;72:507–522.', 'https://doi.org/10.1111/nure.12120'],
 'payne2025': ['Payne 2025', 'Payne ER, Aceves-Martins M, Dubost J, Greyling A, de Roos B. Effects of tea or its bioactive compounds L-theanine or L-theanine plus caffeine on cognition, sleep, and mood in healthy participants. Nutr Rev 2025;83:1873–1891.', 'https://doi.org/10.1093/nutrit/nuaf054'],
 'rogers2008': ['Rogers 2008', 'Rogers PJ, Smith JE, Heatherley SV, Pleydell-Pearce CW. Time for tea: mood, blood pressure and cognitive performance effects of caffeine and theanine administered alone and together. Psychopharmacology 2008;195:569–577.', 'https://doi.org/10.1007/s00213-007-0938-1'],
 'kahathuduwa2020': ['Kahathuduwa 2020', 'Kahathuduwa CN, Wakefield S, West BD et al. Effects of L-theanine–caffeine combination on sustained attention and inhibitory control among children with ADHD: a proof-of-concept neuroimaging RCT. Sci Rep 2020;10:13072.', 'https://doi.org/10.1038/s41598-020-70037-7'],
 'shamabadi2023': ['Shamabadi 2023', 'Shamabadi A, Kafi F, Arab Bafrani M et al. L-theanine adjunct to sertraline for major depressive disorder. J Affect Disord 2023;333:38–43.', 'https://doi.org/10.1016/j.jad.2023.04.029'],
 'shojaei2021': ['Shojaei-Zarghani 2021', 'Shojaei-Zarghani S, Rafraf M, Yari-Khosroushahi A. Theanine and cancer: a systematic review of the literature. Phytother Res 2021;35:4782–4794.', 'https://doi.org/10.1002/ptr.7110'],
 'baba2021': ['Baba 2021', 'Baba Y, Inagaki S, Nakagawa S et al. Effects of L-theanine on cognitive function in middle-aged and older subjects. J Med Food 2021;24:333–341.', 'https://doi.org/10.1089/jmf.2020.4803'],
 'efsa2011': ['EFSA 2011', 'EFSA NDA Panel. Scientific Opinion on the substantiation of health claims related to L-theanine from Camellia sinensis (tea). EFSA Journal 2011;9(6):2238.', 'https://doi.org/10.2903/j.efsa.2011.2238'],
 'bfr2003': ['BfR 2003', 'Bundesinstitut für Risikobewertung. Getränke mit isoliertem L-Theanin. Aktualisierte Stellungnahme, August 2003.', 'https://www.bfr.bund.de/cm/343/getraenke_mit_isoliertem_l_theanin.pdf'],
 'hc_mono': ['Health Canada 2026', 'Health Canada. Natural Health Products Ingredients Database, Monograph: Theanine, L-. Stand 30.01.2026.', 'https://webprod.hc-sc.gc.ca/nhpid-bdipsn/atReq?atid=l.theanine2&lang=eng'],
 'lactmed': ['LactMed 2025', 'Drugs and Lactation Database (LactMed): Theanine. NICHD, Stand 15.05.2025.', 'https://www.ncbi.nlm.nih.gov/books/NBK501922/'],
 'msk': ['MSK 2026', 'Memorial Sloan Kettering Cancer Center. About Herbs: L-Theanine. Stand 14.07.2026.', 'https://www.mskcc.org/cancer-care/integrative-medicine/herbs/l-theanine'],
 'yu2016': ['Yu 2016', 'Yu X-C, Wu B-L, Gao J-C, Yang W. Theanine enhanced both the toxicity of strychnine and anticonvulsion of pentobarbital sodium. Drug Chem Toxicol 2016;39:217–223.', 'https://doi.org/10.3109/01480545.2015.1080264'],
 'desai2004': ['Desai 2004', 'Desai MJ, Armstrong DW. Analysis of derivatized and underivatized theanine enantiomers by HPLC/API-MS. Rapid Commun Mass Spectrom 2004;18:251–256.', 'https://doi.org/10.1002/rcm.1319'],
}
Q = {k: {'kurz': a, 'voll': b, 'url': c} for k, (a, b, c) in QUELLEN.items()}


def S(t, say=None):
    return {'t': t, 'say': say} if say else t


def B(t, at):
    return {'t': t, 'at': at}


SZENEN = [
 {'id': 't0', 'layout': 'kacheln', 'kapitel': 'Einleitung', 'kicker': 'Erklärvideo', 'headline': 'L-Theanin: Was der Stoff aus dem Tee kann',
  'sentences': ['L-Theanin: ein Stoff aus grünem Tee, der entspannen soll, ohne müde zu machen.',
                'Was davon belegt ist und was nur Werbung, schauen wir uns an.',
                'Du erfährst, wie ein japanischer Forscher den Stoff fand, wie er aus dem Blatt in die Kapsel kam, was er im Gehirn tun soll, was Studien zeigen, was Behörden dazu sagen und was bei der Selbstanwendung kritisch ist.'],
  'hervorheben_at': 2,
  'kacheln': [('Entdeckt im Tee', 'k1', 'Forscher'), ('Vom Blatt zur Kapsel', 'k2', 'Kapsel'),
              ('Wie es wirken soll', 'k3', 'Gehirn'), ('Was Studien zeigen', 'k4', 'Studien'),
              ('Was Behörden sagen', 'k5', 'Behörden'), ('Selbstanwendung: Vorsicht', 'k6', 'Selbstanwendung')]},
 {'id': 't1', 'kicker': 'Um 1950', 'headline': 'Entdeckt im Tee',
  'sentences': ['Unsere Geschichte beginnt in Japan, in der Teestadt Uji bei Kyoto.',
                'Dort untersuchte der Forscher Yajiro Sakato, was in grünem Tee steckt.',
                S('1949 fand er einen neuen Stoff und nannte ihn Theanin.',
                  'Neunzehnhundertneunundvierzig fand er einen neuen Stoff und nannte ihn Theanin.'),
                'Besonders viel davon steckte im edlen Schattentee Gyokuro.',
                'Theanin ist eine Aminosäure, aber kein Baustein von Eiweißen. Es ähnelt dem Botenstoff Glutamat.',
                'Die Teepflanze bildet es vor allem in den Wurzeln und schickt es in die jungen Blätter.',
                'Außerhalb des Tees ist es selten: Spuren gibt es etwa in einem Pilz, dem Maronenröhrling.',
                'Im Tee verstärkt es den herzhaften Geschmack, den man Umami nennt.'],
  'bullets': [B('1949: Sakato findet Theanin', 2), B('Aminosäure, ähnelt Glutamat', 4), B('Entsteht in den Wurzeln', 5), B('Geschmack: Umami', 7)],
  'quellen': ['sakato1950', 'ashihara2015', 'casimir1960', 'kaneko2006'],
  'bilder': [('t1a', None), ('t1b', 1), ('t1c', 2), ('t1d', 3), ('t1e', 4), ('t1f', 5), ('t1g', 6), ('t1h', 7)]},
 {'id': 't2', 'kicker': 'Tasse und Kapsel', 'headline': 'Vom Blatt zur Kapsel',
  'sentences': ['Werden Teesträucher vor der Ernte beschattet, wie bei Gyokuro und Matcha, enthalten die Blätter mehr Theanin.',
                'In einer Tasse Tee stecken grob zehn bis fünfundzwanzig Milligramm, je nachdem, wie lange er zieht.',
                'In Japan ist Theanin seit Jahrzehnten als Zusatz für Lebensmittel erlaubt. Heute wird es weltweit als Kapsel verkauft.',
                'Studien nutzen meist zweihundert Milligramm auf einmal. Das ist so viel wie in zehn bis zwanzig Tassen Tee.',
                'Überraschend: Das Theanin in Kapseln stammt oft gar nicht aus Teeblättern.',
                'Der bekannteste Rohstoff entsteht in der Fabrik, mit einem Enzym aus Bakterien.'],
  'bullets': [B('Beschattung: mehr Theanin', 0), B('Tasse: 10 bis 25 Milligramm', 1), B('Studien: meist 200 Milligramm', 3), B('Oft nicht aus Teeblättern', 4)],
  'quellen': ['keenan2011', 'boros2016', 'mu2015', 'fda_grn209'],
  'bilder': [('t2a', None), ('t2b', 1), ('t2d', 2), ('t2e', 3), ('t2f', 4), ('t2g', 5)]},
 {'id': 't3', 'kicker': 'Im Körper', 'headline': 'Wie es wirken soll',
  'sentences': ['Nach dem Schlucken geht Theanin schnell ins Blut. Nach knapp einer Stunde ist der Höchstwert erreicht, eine Stunde später ist schon die Hälfte wieder abgebaut.',
                'Bei Ratten gelangt es ins Gehirn. Beim Menschen wurde das noch nie direkt gemessen.',
                'Im Labor besetzt Theanin Andockstellen für den Botenstoff Glutamat, allerdings viel schwächer als Glutamat selbst.',
                'Am bekanntesten sind die Alpha-Wellen: Hirnströme, die typisch sind für entspanntes Wachsein.',
                'In kleinen Studien zeigten sich nach Theanin in Ruhe mehr Alpha-Wellen, bei Konzentrationsaufgaben aber weniger.',
                'Die Studien hatten nur acht bis fünfunddreißig Teilnehmer, und fast alle kamen von Herstellern oder Teekonzernen.',
                'Und mehr Alpha-Wellen sind nur ein Messwert. Ob man sich dadurch besser fühlt, zeigen sie nicht.'],
  'bullets': [B('Schnell im Blut, schnell abgebaut', 0), B('Gehirn: nur bei Ratten gezeigt', 1), B('Alpha-Wellen: kleine Studien', 4), B('Messwert, kein Nutzenbeweis', 6)],
  'quellen': ['scheid2012', 'yokogoshi1998', 'kakuda2002', 'kobayashi1998', 'gomez2009', 'white2016'],
  'bilder': [('t3a', None), ('t3b', 1), ('t3c', 2), ('t3e', 3), ('t3f', 4), ('t3g', 5), ('t3h', 6)]},
 {'id': 't4', 'kicker': 'Studienlage', 'headline': 'Stress, Schlaf und Angst',
  'sentences': ['Beworben wird L-Theanin vor allem für Entspannung, Schlaf und Konzentration.',
                S('Zum Stress hat eine große Auswertung von 2026 einunddreißig Studien zusammengefasst.', 'Zum Stress hat eine große Auswertung von zweitausendsechsundzwanzig einunddreißig Studien zusammengefasst.'),
                'Ergebnis: Eine einzelne Dosis dämpft akuten Stress ein wenig. Der Effekt ist klein und stützt sich vor allem auf Studien mit Schwächen.',
                'Über mehrere Wochen ist das Bild gemischt. Eine kleine Studie fand eine Besserung, eine andere keinen Unterschied zum Scheinpräparat, auch nicht beim Stresshormon Cortisol. Beide bezahlten Hersteller.',
                'Zum Schlaf gibt es neunzehn Studien. Im Schnitt empfanden die Teilnehmer ihren Schlaf als etwas besser.',
                'Messungen waren aber uneinheitlich, und oft wurden Mischpräparate getestet.',
                'Und bei einer Angststörung? In der einzigen guten Studie, mit sechsundvierzig Menschen, half Theanin nicht besser als ein Scheinpräparat.'],
  'bullets': [B('Akuter Stress: kleiner Effekt', 2), B('Über Wochen: widersprüchlich', 3), B('Schlaf: gefühlt etwas besser', 4), B('Angststörung: nicht belegt', 6)],
  'quellen': ['gerolymos2026', 'hidese2019', 'moulin2024', 'bulman2025', 'sarris2019'],
  'bilder': [('t4a', None), ('t4b', 1), ('t4c', 2), ('t4d', 3), ('t4e', 4), ('t4f', 5), ('t4g', 6)]},
 {'id': 't5', 'kicker': 'Studienlage', 'headline': 'Konzentration, Koffein und mehr',
  'sentences': ['Am besten untersucht ist Theanin zusammen mit Koffein, so wie beide im Tee vorkommen.',
                'In vielen kleinen Studien waren die Teilnehmer in den ersten zwei Stunden etwas wacher und aufmerksamer.',
                'Viele davon bezahlte ein Teekonzern, und vermutlich leistet das Koffein den größeren Teil.',
                'Theanin allein machte die Reaktion in manchen Tests etwas schneller, in anderen aber langsamer.',
                'Oft heißt es, Theanin nehme dem Koffein die Nebenwirkungen. In einer Studie dämpfte es aber nur den Anstieg des Blutdrucks, nicht die Zittrigkeit.',
                'Bei ADHS gibt es nur winzige Studien, eine davon mit fünf Kindern.',
                'Bei Depression und Schizophrenie gab es in einzelnen kleinen Studien ermutigende Ergebnisse, aber nur zusätzlich zu Medikamenten.',
                'Für Blutdruck, Immunsystem, Abnehmen, Demenz oder Krebs fehlen überzeugende Belege beim Menschen.',
                'Und ob schon eine normale Tasse Tee solche Wirkungen hat, ist nicht belegt.'],
  'bullets': [B('Mit Koffein: gut untersucht, Effekt klein', 1), B('Allein: widersprüchlich', 3), B('ADHS: kaum Studien', 5),
              B('Depression: kleine Studien, als Zusatz', 6), B('Krebs, Demenz, Abnehmen: nicht belegt', 7)],
  'quellen': ['camfield2014', 'payne2025', 'gerolymos2026', 'rogers2008', 'kahathuduwa2020', 'shamabadi2023', 'shojaei2021', 'baba2021'],
  'bilder': [('t5a', None), ('t5b', 1), ('t5c', 2), ('t5d', 3), ('t5e', 4), ('t5f', 5), ('t5g', 6), ('t5h', 7), ('t5i', 8)]},
 {'id': 't6', 'kicker': 'Rechtsstatus', 'headline': 'Was Behörden sagen',
  'sentences': ['Derselbe Stoff, und je nach Land eine andere Antwort.',
                S('In der EU prüfte die Lebensmittelbehörde 2011 Werbeaussagen zu Konzentration, Stress und Schlaf. Sie hielt keine davon für belegt.',
                  'In der EU prüfte die Lebensmittelbehörde zweitausendelf Werbeaussagen zu Konzentration, Stress und Schlaf. Sie hielt keine davon für belegt.'),
                'Deshalb darf hier niemand damit werben.',
                S('In Deutschland lehnte das Bundesinstitut für Risikobewertung 2003 Theanin als Zusatz in Getränken ab, weil Daten zur Sicherheit fehlten.',
                  'In Deutschland lehnte das Bundesinstitut für Risikobewertung zweitausenddrei Theanin als Zusatz in Getränken ab, weil Daten zur Sicherheit fehlten.'),
                'In den USA gilt Theanin als sicher für Lebensmittel. Eingestuft hat das aber der Hersteller selbst. Die Behörde hatte dazu nur keine Fragen, und die Wirkung hat sie nicht geprüft.',
                'Kanada erlaubt dagegen die Aussage, Theanin fördere vorübergehend die Entspannung.',
                'Keine dieser Einstufungen beweist, dass Theanin wirkt.'],
  'bullets': [B('EU: Werbeaussagen abgelehnt', 1), B('Deutschland 2003: nicht in Getränke', 3), B('USA: vom Hersteller als sicher erklärt', 4), B('Kanada: „fördert Entspannung“ erlaubt', 5)],
  'quellen': ['efsa2011', 'bfr2003', 'fda_grn209', 'hc_mono'],
  'bilder': [('t6a', None), ('t6b', 1), ('t6c', 2), ('t6d', 3), ('t6e', 4), ('t6f', 5), ('t6g', 6)]},
 {'id': 't7', 'kicker': 'Vorsicht', 'headline': 'Selbstanwendung: was kritisch ist',
  'sentences': ['L-Theanin gibt es frei zu kaufen. Vorher solltest du einiges wissen.',
                'Zuerst das Gute: In Studien wurden keine schweren Nebenwirkungen berichtet.',
                'Aber die längsten Studien liefen nur wenige Monate. Eine Einnahme über Jahre hat niemand untersucht.',
                'Zweitens: Im Tierversuch verstärkte Theanin ein Schlafmittel. Fachleute raten deshalb, es nicht mit Schlaf- oder Beruhigungsmitteln zu kombinieren.',
                'Drittens: Für Schwangerschaft und Stillzeit gibt es keine Daten, für Kinder nur wenige kleine Studien.',
                'Viertens, die Qualität: In einer älteren Analyse enthielten fünf von sechs Präparaten auch eine spiegelbildliche Form des Moleküls. Neuere unabhängige Prüfungen fehlen.',
                'Und Theanin ersetzt keine Behandlung, wenn Angst oder Schlafprobleme dich belasten.',
                'Tipp für dich: Sprich mit Arzt oder Ärztin, bevor du L-Theanin nimmst, besonders wenn du Medikamente nimmst, schwanger bist oder stillst.'],
  'bullets': [B('Kurzfristig gut vertragen', 1), B('Langzeitdaten fehlen', 2), B('Nicht mit Schlafmitteln', 3), B('Schwangerschaft, Stillzeit: keine Daten', 4),
              B('Qualität der Präparate unklar', 5)],
  'quellen': ['gerolymos2026', 'yu2016', 'msk', 'lactmed', 'desai2004'],
  'bilder': [('t7a', None), ('t7b', 1), ('t7c', 2), ('t7d', 3), ('t7e', 4), ('t7f', 5), ('t7g', 6), ('t7h', 7)]},
 {'id': 't8', 'kapitel': 'Fazit', 'kicker': 'Fazit', 'headline': 'Das Wichtigste',
  'sentences': ['L-Theanin hat eine schöne Geschichte: vom Schattentee aus Uji bis in die Kapsel.',
                'Am besten belegt sind kleine, kurzfristige Effekte: etwas weniger Stress und, zusammen mit Koffein, etwas mehr Aufmerksamkeit.',
                'Vieles andere ist kaum untersucht, und viele Studien haben Hersteller bezahlt.',
                'Die Quellen stehen in der Beschreibung.',
                'Gut, dass du dich informierst. Das Video kann das Gespräch mit Arzt oder Ärztin unterstützen, aber nicht ersetzen. Bis zum nächsten Video!'],
  'bullets': [B('Vom Schattentee zur Kapsel', 0), B('Kleine, kurzfristige Effekte', 1), B('Vieles kaum untersucht', 2)],
  'quellen': ['sakato1950', 'gerolymos2026'],
  'bilder': [('t8a', None), ('t8b', 1), ('t8c', 2), ('t8d', 4)]},
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
            'titel': 'L-Theanin: Was der Stoff aus dem Tee kann', 'stil': stil,
            'untertitel': 'Ein Erklärvideo über L-Theanin: wie es im grünen Tee entdeckt wurde, wie es wirken soll, was Studien zeigen, was Behörden sagen und was bei der Selbstanwendung kritisch ist.',
            'fuss': 'Sprecherstimme synthetisch (ElevenLabs). Bilder KI-generiert. Das Video ersetzt nicht das Gespräch mit Arzt oder Ärztin.',
            'scenes': szenen, 'quellen': Q}


# Aussprache: vorläufig, bis der Nutzer auf der Auswahl-Seite gewählt hat (aussprache_wahl/)
AUSSPRACHE = {}

if __name__ == '__main__':
    for stil in STILE:
        json.dump(bauen(stil), open(f'szenen_{stil}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(bauen('G'), open('szenen.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)  # für Ton und Hörprobe
    w = sum(len((x if isinstance(x, str) else x['t']).split()) for sc in SZENEN for x in sc['sentences'])
    z = sum(len((x if isinstance(x, str) else x.get('say', x['t']))) for sc in SZENEN for x in sc['sentences'])
    print(len(STILE), 'Drehbuch,', w, 'Wörter,', z, 'Zeichen')
    for sc in SZENEN:
        print(sc['id'], sum(len((x if isinstance(x, str) else x['t']).split()) for x in sc['sentences']))
