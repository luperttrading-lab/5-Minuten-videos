"""Drehbuch „DMSO: Vom Lösungsmittel zum Kälteschutz“ (Erklärvideo im Schulprojekt-Ton wie themen/pea, keine Ampel),
nur Stil G (Aquarell und Tusche). Nachtrag des Nutzers 10.11.: breite Übersicht, wofür DMSO eingesetzt und untersucht
wird (Einordnung in Worten), und eine Szene zur Selbstanwendung. Keine Dosierungen, keine Konzentrationen, keine
Heilversprechen. Fakten und Quellen: faktencheck.md (10.11.2026). Aufruf: python3 drehbuch_bau.py"""
import json, os

STILE = ['G']

QUELLEN = {
 'saytzeff1867': ['Saytzeff 1867', 'Saytzeff A. Ueber die Einwirkung von Salpetersäure auf Schwefelmethyl und Schwefeläthyl. Annalen der Chemie und Pharmacie 1867;144(2):148–156.', 'https://doi.org/10.1002/jlac.18671440205'],
 'bristol2012': ['May 2012', 'May P. DMSO. Molecule of the Month, University of Bristol, Januar 2012.', 'https://www.chm.bris.ac.uk/motm/DMSO/DMSOh.htm'],
 'capriotti2012': ['Capriotti 2012', 'Capriotti K, Capriotti JA. Dimethyl sulfoxide: history, chemistry, and clinical utility in dermatology. J Clin Aesthet Dermatol 2012;5(9):24–26.', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC3460663/'],
 'lovelock1959': ['Lovelock 1959', 'Lovelock JE, Bishop MWH. Prevention of freezing damage to living cells by dimethyl sulphoxide. Nature 1959;183(4672):1394–1395.', 'https://doi.org/10.1038/1831394a0'],
 'awan2020': ['Awan 2020', 'Awan M, Buriak I, Fleck R et al. Dimethyl sulfoxide: a central player since the dawn of cryobiology, is efficacy balanced by toxicity? Regen Med 2020;15(3):1463–1491.', 'https://doi.org/10.2217/rme-2019-0145'],
 'bennett2024': ['Bennett 2024', 'Bennett B, Hanotaux J, Pasala AR et al. Impact of lower concentrations of dimethyl sulfoxide on cryopreservation of autologous hematopoietic stem cells: a systematic review and meta-analysis. Cytotherapy 2024;26(5):482–489.', 'https://doi.org/10.1016/j.jcyt.2024.02.006'],
 'madsen2019': ['Kollerup Madsen 2019', 'Kollerup Madsen B, Hilscher M, Zetner D, Rosenberg J. Adverse reactions of dimethyl sulfoxide in humans: a systematic review. F1000Research 2019;7:1746.', 'https://doi.org/10.12688/f1000research.16642.2'],
 'jacob1967': ['Jacob 1967', 'Jacob SW, Wood DC. Dimethyl sulfoxide (DMSO): toxicology, pharmacology, and clinical experience. Am J Surg 1967;114(3):414–426.', 'https://doi.org/10.1016/0002-9610(67)90166-3'],
 'rubin1966': ['Rubin 1966', 'Rubin LF, Mattis PA. Dimethyl sulfoxide: lens changes in dogs during oral administration. Science 1966;153(3731):83–84.', 'https://doi.org/10.1126/science.153.3731.83'],
 'time1980': ['TIME 1980', 'TIME. Medicine: DMSO Dustup. 28.04.1980.', 'https://time.com/archive/6857944/medicine-dmso-dustup'],
 'sciencenews2016': ['Science News 2016', 'Science News. 50 years ago, a promising agent pulled. 05.01.2016 (Science News Letter 08.01.1966).', 'https://www.sciencenews.org/article/50-years-ago-promising-agent-pulled'],
 'rimso_fda': ['FDA 1978', 'FDA, Drugs@FDA: RIMSO-50, NDA 017788, Zulassung 04.04.1978.', 'https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo=017788'],
 'perezmarrero1988': ['Perez-Marrero 1988', 'Perez-Marrero R, Emerson LE, Feltis JT. A controlled study of dimethyl sulfoxide in interstitial cystitis. J Urol 1988;140(1):36–39.', 'https://doi.org/10.1016/S0022-5347(17)41478-9'],
 'perezfidalgo2012': ['Pérez Fidalgo 2012', 'Pérez Fidalgo JA, García Fabregat L, Cervantes A et al. Management of chemotherapy extravasation: ESMO–EONS Clinical Practice Guidelines. Ann Oncol 2012;23(Suppl 7):vii167–vii173.', 'https://doi.org/10.1093/annonc/mds294'],
 'dolobene_at': ['Dolobene AT 2019', 'Teva B.V. Gebrauchsinformation Dolobene ratiopharm-Gel, Z.Nr. 1-21937, Stand Mai 2019.', 'https://apps.apoverlag.at/avout/shopindex/FILEs/GI/GIA121937.pdf'],
 'diepta2022': ['Die PTA 2022', 'Brachwitz L. Schwefeliger Schmerzstiller DMSO. DIE PTA IN DER APOTHEKE, 21.06.2022.', 'https://www.diepta.de/news/rezeptur-mischen-possible-schwefeliger-schmerzstiller-dmso'],
 'zostrum_ie': ['Zostrum 2005', 'Irish Medicines Board. Summary of Product Characteristics Zostrum (Idoxuridin in DMSO), 30.09.2005.', 'https://assets.hpra.ie/products/Human/19163/LicenseSPC_PA0590-017-001_30092005144323.pdf'],
 'cfr524660': ['21 CFR 524.660', '21 CFR § 524.660 Dimethyl sulfoxide (Tierarzneimittel, USA).', 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-E/part-524/section-524.660'],
 'zuurmond1996': ['Zuurmond 1996', 'Zuurmond WW, Langendijk PN, Bezemer PD et al. Treatment of acute reflex sympathetic dystrophy with DMSO 50% in a fatty cream. Acta Anaesthesiol Scand 1996;40(3):364–367.', 'https://doi.org/10.1111/j.1399-6576.1996.tb04446.x'],
 'perez2003': ['Perez 2003', 'Perez RSGM, Zuurmond WWA, Bezemer PD et al. The treatment of complex regional pain syndrome type I with free radical scavengers: a randomized controlled study. Pain 2003;102(3):297–307.', 'https://doi.org/10.1016/S0304-3959(02)00414-1'],
 'dgn2018': ['DGN 2018', 'Birklein F et al. Diagnostik und Therapie komplexer regionaler Schmerzsyndrome (CRPS), S1-Leitlinie, DGN 2018, AWMF 030/116.', 'https://register.awmf.org/assets/guidelines/030-116l_S1_Schmerzsyndrome_CRPS_2018-09-abgelaufen.pdf'],
 'brien2011': ['Brien 2011', 'Brien S, Prescott P, Lewith G. Meta-analysis of the related nutritional supplements dimethyl sulfoxide and methylsulfonylmethane in the treatment of osteoarthritis of the knee. Evid Based Complement Alternat Med 2011;2011:528403.', 'https://doi.org/10.1093/ecam/nep045'],
 'brien2008': ['Brien 2008', 'Brien S, Prescott P, Bashir N, Lewith H, Lewith G. Systematic review of the nutritional supplements DMSO and MSM in the treatment of osteoarthritis. Osteoarthritis Cartilage 2008;16(11):1277–1288.', 'https://doi.org/10.1016/j.joca.2008.03.002'],
 'williams1985': ['Williams 1985', 'Williams HJ, Furst DE, Dahl SL et al. Double-blind, multicenter controlled trial comparing topical dimethyl sulfoxide and normal saline for treatment of hand ulcers in patients with systemic sclerosis. Arthritis Rheum 1985;28(3):308–314.', 'https://doi.org/10.1002/art.1780280311'],
 'hall2014': ['Hall 2014', 'Hall MD, Telma KA, Chang KE et al. Say no to DMSO: dimethylsulfoxide inactivates cisplatin, carboplatin, and other platinum complexes. Cancer Res 2014;74(14):3913–3922.', 'https://doi.org/10.1158/0008-5472.CAN-14-0247'],
 'msk_dmso': ['MSK', 'Memorial Sloan Kettering. About Herbs: Dimethylsulfoxide.', 'https://www.mskcc.org/cancer-care/integrative-medicine/herbs/dimethylsulfoxide'],
 'vz_mms': ['Verbraucherzentrale 2025', 'Verbraucherzentrale. Miracle Mineral Supplement (MMS): Erhebliche Gesundheitsgefahr. Stand 24.04.2025.', 'https://www.verbraucherzentrale.de/wissen/lebensmittel/nahrungsergaenzungsmittel/miracle-mineral-supplement-mms-erhebliche-gesundheitsgefahr-11044'],
}
Q = {k: {'kurz': a, 'voll': b, 'url': c} for k, (a, b, c) in QUELLEN.items()}


def S(t, say=None):
    return {'t': t, 'say': say} if say else t


def B(t, at):
    return {'t': t, 'at': at}


SZENEN = [
 {'id': 'd0', 'layout': 'kacheln', 'kapitel': 'Einleitung', 'kicker': 'Erklärvideo', 'headline': 'DMSO: Vom Lösungsmittel zum Kälteschutz',
  'sentences': [S('DMSO: ein Stoff aus der Papierfabrik, der Zellen beim Einfrieren schützt und einmal als Wundermittel gefeiert wurde.',
                  'De-Em-Es-O: ein Stoff aus der Papierfabrik, der Zellen beim Einfrieren schützt und einmal als Wundermittel gefeiert wurde.'),  # klang wie „Der MSO“ (Nutzer 11.11.)
                'Was davon bis heute geblieben ist, ist eine spannende Geschichte.',
                'Du erfährst, wie ein Chemiker den Stoff fand, warum er Zellen vor Kälte schützt, wie es zum großen Hype kam, wofür er zugelassen ist, was Studien zeigen und was bei der Selbstanwendung kritisch ist.'],
  'hervorheben_at': 2,
  'kacheln': [('Ein Stoff aus dem Labor', 'k1', 'Chemiker'), ('Kälteschutz für Zellen', 'k2', 'Kälte'),
              ('Der große Hype', 'k3', 'Hype'), ('Wofür es zugelassen ist', 'k4', 'zugelassen'),
              ('Was Studien zeigen', 'k5', 'Studien'), ('Selbstanwendung: Vorsicht', 'k6', 'Selbstanwendung')]},
 {'id': 'd1', 'kicker': '1860er Jahre', 'headline': 'Ein Stoff aus dem Labor',
  'sentences': ['Unsere Geschichte beginnt in den Achtzehnhundertsechzigerjahren, bei dem russischen Chemiker Alexander Saizew.',
                'Er ließ Salpetersäure auf eine übel riechende Schwefelverbindung wirken und erhielt eine klare Flüssigkeit.',
                S('1867 beschrieb er sie in einer deutschen Chemie-Zeitschrift: Dimethylsulfoxid, kurz DMSO.',
                  'Achtzehnhundertsiebenundsechzig beschrieb er sie in einer deutschen Chemie-Zeitschrift: Dimethylsulfoxid, kurz DMSO.'),
                'Das Molekül ist winzig: ein Schwefelatom, ein Sauerstoffatom und zwei kleine Kohlenstoffgruppen.',
                'Heute fällt DMSO bei der Papierherstellung an, wenn Holz zu Zellstoff verarbeitet wird.',
                'Es löst sehr viele Stoffe, mischt sich mit Wasser und wird schon knapp unter zwanzig Grad fest, also im Kühlschrank.',
                'Fast hundert Jahre lang war es vor allem ein Lösungsmittel für Labor und Industrie.'],
  'bullets': [B('1867: Saizew beschreibt DMSO', 2), B('Schwefel, Sauerstoff, zwei Kohlenstoffgruppen', 3), B('Nebenprodukt der Papierherstellung', 4), B('Lösungsmittel', 6)],
  'quellen': ['saytzeff1867', 'bristol2012', 'capriotti2012'],
  'bilder': [('d1a', None), ('d1b', 1), ('d1c', 2), ('d1d', 3), ('d1e', 4), ('d1f', 5)]},
 {'id': 'd2', 'kicker': '1959', 'headline': 'Kälteschutz für Zellen',
  'sentences': ['1959 machten zwei britische Forscher eine Entdeckung, die bis heute wichtig ist.',
                'Wenn man lebende Zellen einfriert, werden sie durch Eiskristalle und Salz geschädigt.',
                'Mit DMSO überstanden rote Blutkörperchen und Samenzellen von Bullen das Einfrieren viel besser.',
                'Heute werden Blutstammzellen für Transplantationen meist mit DMSO eingefroren, und auch beim Einfrieren von Eizellen und Embryonen kommt es oft zum Einsatz.',
                'Ganz harmlos ist das nicht: Nach der Übertragung riechen Patienten oft nach Knoblauch, und manche bekommen Kreislaufprobleme.',
                'Forscher prüfen deshalb, ob weniger DMSO genügt, und erste Studien sind ermutigend.',
                'Dieser Kälteschutz ist bis heute eine der wichtigsten Anwendungen in der Medizin.'],
  'bullets': [B('1959: Schutz beim Einfrieren', 0), B('Blutstammzellen, Eizellen, Embryonen', 3), B('Nebenwirkung: Knoblauchgeruch', 4), B('Wichtige Anwendung heute', 6)],
  'quellen': ['lovelock1959', 'awan2020', 'bennett2024', 'madsen2019'],
  'bilder': [('d2a', None), ('d2b', 1), ('d2c', 2), ('d2d', 3), ('d2e', 4), ('d2f', 6)]},
 {'id': 'd3', 'kicker': '1960er Jahre', 'headline': 'Der große Hype',
  'sentences': ['Anfang der Sechzigerjahre forschte der Chirurg Stanley Jacob in Oregon zusammen mit Robert Herschler, einem Chemiker eines Papierkonzerns.',
                'Sie bemerkten: DMSO dringt sehr schnell durch die Haut und nimmt dabei andere Stoffe mit.',
                'Bald wurde es als Wundermittel gefeiert, gegen Verstauchungen, Prellungen, Arthritis und vieles mehr.',
                S('Bis 1965 sollen es rund hunderttausend Menschen benutzt haben.', 'Bis neunzehnhundertfünfundsechzig sollen es rund hunderttausend Menschen benutzt haben.'),
                'Dann entdeckten Forscher bei Hunden und anderen Tieren veränderte Augenlinsen.',
                'Ende des Jahres wurden die Studien in den USA gestoppt, und in Westdeutschland verschwand DMSO nach weniger als drei Monaten wieder vom Markt.',
                'Beim Menschen wurden solche Linsenschäden später nicht nachgewiesen. Doch der Ruf als Wundermittel hält sich bis heute.'],
  'bullets': [B('Dringt durch die Haut', 1), B('Gefeiert als Wundermittel', 2), B('Tiere: veränderte Augenlinsen', 4), B('1965: Studien gestoppt', 5)],
  'quellen': ['jacob1967', 'capriotti2012', 'time1980', 'rubin1966', 'sciencenews2016'],
  'bilder': [('d3a', None), ('d3b', 1), ('d3c', 2), ('d3d', 3), ('d3e', 4), ('d3f', 5), ('d3g', 6)]},
 {'id': 'd4', 'kicker': 'Zulassungen', 'headline': 'Wofür es zugelassen ist',
  'sentences': ['Was ist von der großen Hoffnung geblieben? Einiges, nur anders als gedacht.',
                S('In den USA ist DMSO seit 1978 für eine einzige Krankheit beim Menschen zugelassen: eine chronische Blasenentzündung, die interstitielle Zystitis.',
                  'In den USA ist DMSO seit neunzehnhundertachtundsiebzig für eine einzige Krankheit beim Menschen zugelassen: eine chronische Blasenentzündung, die interstitielle Zystitis.'),
                'Dabei füllt Arzt oder Ärztin die Lösung direkt in die Blase. In einer kleinen Studie ging es damit deutlich mehr Menschen besser als mit Kochsalzlösung.',
                'In Kliniken hilft DMSO außerdem, wenn bestimmte Chemotherapie aus Versehen neben die Vene läuft. Leitlinien empfehlen das, obwohl die Studien klein sind.',
                'In Österreich und der Schweiz gibt es ein zugelassenes Gel mit DMSO und zwei weiteren Wirkstoffen, gegen Prellungen, Verstauchungen und Sehnenentzündungen.',
                'In Deutschland ist derzeit wohl kein Fertigarzneimittel mit DMSO im Handel. Es gibt nur Rezepturen aus der Apotheke, auf ärztliche Verordnung.',
                'Früher trug DMSO in einem Mittel gegen Gürtelrose einen Wirkstoff durch die Haut.',
                'Und in der Tiermedizin ist es in den USA für Pferde und Hunde zugelassen, gegen Schwellungen nach Verletzungen.'],
  'bullets': [B('Zugelassen: Blasenspülung (USA)', 1), B('In Leitlinien: Chemo neben der Vene', 3), B('Zugelassen: Gel in AT und CH', 4),
              B('Zugelassen: Pferde und Hunde (USA)', 7)],
  'quellen': ['rimso_fda', 'perezmarrero1988', 'perezfidalgo2012', 'dolobene_at', 'diepta2022', 'zostrum_ie', 'cfr524660'],
  'bilder': [('d4a', None), ('d4b', 1), ('d4c', 2), ('d4d', 3), ('d4e', 4), ('d4f', 5), ('d4g', 6), ('d4h', 7)]},
 {'id': 'd5', 'kicker': 'Studienlage', 'headline': 'Was Studien zeigen',
  'sentences': ['Gegen was soll DMSO noch helfen? Die Liste ist lang. Hier ist, was Studien dazu sagen.',
                'Beim Komplexen Regionalen Schmerzsyndrom, auch Morbus Sudeck genannt, half eine DMSO-Creme in einer kleinen Studie besser als Placebo.',
                'In einer größeren Studie war sie aber nicht besser als ein anderes Mittel. Die deutsche Leitlinie gibt keine klare Empfehlung, in den Niederlanden gehört die Creme zur Standardbehandlung.',
                'Bei Kniearthrose fanden Übersichtsarbeiten keinen spürbaren Nutzen.',
                'Dabei haben solche Studien ein besonderes Problem: Der Knoblauchgeruch verrät, wer DMSO bekommt. Echte Blindstudien sind deshalb schwer.',
                'Bei Sklerodermie half es in einer sorgfältigen Studie nicht, und bei Amyloidose oder Hirnschwellung gibt es nur kleine, alte Untersuchungen.',
                'Für Muskel- und Sportschmerzen gibt es vor allem Erfahrungsberichte, aber kaum Studien mit reinem DMSO.',
                'Und gegen Krebs? Beim Menschen gibt es dafür keine Belege. Im Labor macht DMSO manche Chemotherapie sogar unwirksam.'],
  'bullets': [B('Morbus Sudeck: in Studien untersucht', 1), B('Kniearthrose: kein spürbarer Nutzen', 3), B('Geruch erschwert Blindstudien', 4),
              B('Sportschmerzen: Erfahrungsberichte', 6), B('Krebs: nicht belegt', 7)],
  'quellen': ['zuurmond1996', 'perez2003', 'dgn2018', 'brien2011', 'brien2008', 'williams1985', 'msk_dmso', 'hall2014'],
  'bilder': [('d5a', None), ('d5b', 1), ('d5c', 2), ('d5d', 3), ('d5e', 4), ('d5f', 5), ('d5g', 6), ('d5h', 7)]},
 {'id': 'd6', 'kicker': 'Vorsicht', 'headline': 'Selbstanwendung: was kritisch ist',
  'sentences': ['DMSO lässt sich leicht im Internet kaufen. Wenn du darüber nachdenkst, solltest du einiges wissen.',
                'Erstens: DMSO nimmt andere Stoffe mit durch die Haut, auch Schmutz, Cremes oder Reste von Chemikalien.',
                'Zweitens: DMSO aus dem Chemiehandel ist als Lösungsmittel gedacht, nicht als Arzneimittel, und kann verunreinigt sein.',
                'Drittens: Oft brennt und juckt die Haut, sie wird rot, und der Atem riecht nach Knoblauch.',
                'Viertens: Wechselwirkungen. Zusammen mit dem Schmerzmittel Sulindac kann DMSO zum Beispiel Nerven schädigen.',
                'Zum Trinken oder Einnehmen ist DMSO nicht zugelassen, und dafür fehlen Daten zur Sicherheit.',
                'Und Finger weg von Mischungen mit Chlordioxid, auch MMS genannt. Schon das allein gilt als giftig und ätzend.',
                'Tipp für dich: Sprich mit Arzt oder Ärztin, bevor du DMSO ausprobierst, besonders wenn du Medikamente nimmst.'],
  'bullets': [B('Nimmt andere Stoffe mit', 1), B('Industrie-DMSO: Reinheit unklar', 2), B('Haut, Geruch', 3), B('Wechselwirkungen', 4),
              B('Nicht einnehmen', 5), B('Nie mit Chlordioxid', 6)],
  'quellen': ['dolobene_at', 'zostrum_ie', 'msk_dmso', 'madsen2019', 'vz_mms'],
  'bilder': [('d6a', None), ('d6b', 1), ('d6c', 2), ('d6d', 3), ('d6e', 4), ('d6f', 5), ('d6g', 6), ('d6h', 7)]},
 {'id': 'd7', 'kapitel': 'Fazit', 'kicker': 'Fazit', 'headline': 'Das Wichtigste',
  'sentences': [S('DMSO hat eine erstaunliche Reise hinter sich: vom Lösungsmittel aus der Papierfabrik bis zum Kälteschutz für Stammzellen.',
                  'De-Em-Es-O hat eine erstaunliche Reise hinter sich: vom Lösungsmittel aus der Papierfabrik bis zum Kälteschutz für Stammzellen.'),  # wie oben
                'Zugelassen ist es nur für wenige Anwendungen, etwa für eine chronische Blasenentzündung.',
                'Für vieles andere sind die Studien klein, widersprüchlich oder fehlen ganz.',
                'Die Quellen stehen in der Beschreibung.',
                'Gut, dass du dich informierst. Das Video kann das Gespräch mit Arzt oder Ärztin unterstützen, aber nicht ersetzen. Bis zum nächsten Video!'],
  'bullets': [B('Vom Lösungsmittel zum Kälteschutz', 0), B('Wenige Zulassungen', 1), B('Vieles kaum untersucht', 2)],
  'quellen': ['awan2020', 'rimso_fda'],
  'bilder': [('d7a', None), ('d7b', 1), ('d7c', 2), ('d7d', 4)]},
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
            'titel': 'DMSO: Vom Lösungsmittel zum Kälteschutz', 'stil': stil,
            'untertitel': 'Ein Erklärvideo über Dimethylsulfoxid: wie es entdeckt wurde, wofür es zugelassen ist, was Studien zeigen und was bei der Selbstanwendung kritisch ist.',
            'fuss': 'Sprecherstimme synthetisch (ElevenLabs). Bilder KI-generiert. Das Video ersetzt nicht das Gespräch mit Arzt oder Ärztin.',
            'scenes': szenen, 'quellen': Q}


# Aussprache bis zur Wahl des Nutzers: Fassung 2 (aussprache_wahl/)
AUSSPRACHE = {'Dimethylsulfoxid': 'Di-methyl-sulf-oxid', 'DMSO': 'De Em Es O'}

if __name__ == '__main__':
    for stil in STILE:
        json.dump(bauen(stil), open(f'szenen_{stil}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(bauen('G'), open('szenen.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)  # für Ton und Hörprobe
    w = sum(len((x if isinstance(x, str) else x['t']).split()) for sc in SZENEN for x in sc['sentences'])
    z = sum(len((x if isinstance(x, str) else x.get('say', x['t']))) for sc in SZENEN for x in sc['sentences'])
    print(len(STILE), 'Drehbuch,', w, 'Wörter,', z, 'Zeichen')
