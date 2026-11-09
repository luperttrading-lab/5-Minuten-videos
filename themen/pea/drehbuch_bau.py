"""Drehbuch „PEA: Vom Eigelb zur Schmerzforschung“ (Erklärvideo im Ton des Schulprojekts, kein Faktencheck,
Nutzerwunsch 09.11.: „etwas anders und etwas softer“; keine Ampel) für drei Bildstile I, G, D.
Ein Sprechtext für alle Stile (gemeinsamer Ton-Cache), nur die Bilder wechseln. Vorlage:
themen/schulprojekt-vitamin-d/erklaervideo/drehbuch_bau.py. Fakten und Quellen: faktencheck.md (09.11.2026).
Aufruf: python3 drehbuch_bau.py"""
import json, os

STILE = ['I', 'G', 'D']

QUELLEN = {
 'coburn1954': ['Coburn 1954', 'Coburn AF, Graham CE, Haninger J. The effect of egg yolk in diets on anaphylactic arthritis (passive Arthus phenomenon) in the guinea pig. J Exp Med 1954;100(5):425–435.', 'https://doi.org/10.1084/jem.100.5.425'],
 'coburn1960': ['Coburn 1960', 'Coburn AF. The concept of egg yolk as a dietary inhibitor to rheumatic susceptibility. Lancet 1960;275(7129):867–870.', 'https://doi.org/10.1016/s0140-6736(60)90750-9'],
 'keppel2013': ['Keppel Hesselink 2013', 'Keppel Hesselink JM, de Boer T, Witkamp RF. Palmitoylethanolamide: a natural body-own anti-inflammatory agent, effective and safe against influenza and common cold. Int J Inflam 2013:151028.', 'https://doi.org/10.1155/2013/151028'],
 'kuehl1957': ['Kuehl 1957', 'Kuehl FA Jr, Jacob TA, Ganley OH, Ormond RE, Meisinger MAP. The identification of N-(2-hydroxyethyl)-palmitamide as a naturally occurring anti-inflammatory agent. J Am Chem Soc 1957;79(20):5577–5578.', 'https://doi.org/10.1021/ja01577a066'],
 'masek1974': ['Mašek 1974', 'Mašek K, Perlík F, Klíma J, Kahlich R. Prophylactic efficacy of N-2-hydroxyethyl palmitamide (Impulsin) in acute respiratory tract infections. Eur J Clin Pharmacol 1974;7(6):415–419.', 'https://doi.org/10.1007/BF00560353'],
 'kahlich1979': ['Kahlich 1979', 'Kahlich R, Klíma J, Cihla F et al. Studies on prophylactic efficacy of N-2-hydroxyethyl palmitamide (Impulsin) in acute respiratory infections. Serologically controlled field trials. J Hyg Epidemiol Microbiol Immunol 1979;23(1):11–24.', 'https://pubmed.ncbi.nlm.nih.gov/392005/'],
 'bortoletto2025': ['Bortoletto 2025', 'Bortoletto R et al. Palmitoylethanolamide supplementation for human health: a state-of-the-art systematic review of RCTs in patient populations. Brain Behav Immun Health 2025;43:100927.', 'https://doi.org/10.1016/j.bbih.2024.100927'],
 'nobel1986': ['Nobelpreis 1986', 'The Nobel Prize in Physiology or Medicine 1986: Stanley Cohen, Rita Levi-Montalcini.', 'https://www.nobelprize.org/prizes/medicine/1986/summary/'],
 'aloe1993': ['Aloe 1993', 'Aloe L, Leon A, Levi-Montalcini R. A proposed autacoid mechanism controlling mastocyte behaviour. Agents Actions 1993;39:C145–C147.', 'https://doi.org/10.1007/BF01972748'],
 'facci1995': ['Facci 1995', 'Facci L, Dal Toso R, Romanello S, Buriani A, Skaper SD, Leon A. Mast cells express a peripheral cannabinoid receptor with differential sensitivity to anandamide and palmitoylethanolamide. PNAS 1995;92(8):3376–3380.', 'https://doi.org/10.1073/pnas.92.8.3376'],
 'lambert2002': ['Lambert 2002', 'Lambert DM, Vandevoorde S, Jonsson KO, Fowler CJ. The palmitoylethanolamide family: a new class of anti-inflammatory agents? Curr Med Chem 2002;9(6):663–674.', 'https://doi.org/10.2174/0929867023370707'],
 'loverme2005': ['Lo Verme 2005', 'Lo Verme J, Fu J, Astarita G et al. The nuclear receptor PPAR-α mediates the anti-inflammatory actions of palmitoylethanolamide. Mol Pharmacol 2005;67(1):15–19.', 'https://doi.org/10.1124/mol.104.006353'],
 'devane1992': ['Devane 1992', 'Devane WA, Hanuš L, Breuer A et al. Isolation and structure of a brain constituent that binds to the cannabinoid receptor. Science 1992;258:1946–1949.', 'https://doi.org/10.1126/science.1470919'],
 'jonsson2001': ['Jonsson 2001', 'Jonsson KO, Vandevoorde S, Lambert DM, Tiger G, Fowler CJ. Effects of homologues and analogues of palmitoylethanolamide upon the inactivation of the endocannabinoid anandamide. Br J Pharmacol 2001;133:1263–1275.', 'https://doi.org/10.1038/sj.bjp.0704199'],
 'ho2008': ['Ho 2008', "Ho WSV, Barrett DA, Randall MD. 'Entourage' effects of N-palmitoylethanolamide and N-oleoylethanolamide on vasorelaxation to anandamide occur through TRPV1 receptors. Br J Pharmacol 2008;155:837–846.", 'https://doi.org/10.1038/bjp.2008.324'],
 'gabrielsson2016': ['Gabrielsson 2016', 'Gabrielsson L, Mattsson S, Fowler CJ. Palmitoylethanolamide for the treatment of pain: pharmacokinetics, safety and efficacy. Br J Clin Pharmacol 2016;82(4):932–942.', 'https://doi.org/10.1111/bcp.13020'],
 'langilli2023': ['Lang-Illievich 2023', 'Lang-Illievich K, Klivinyi C, Lasser C, Brenna CTA, Szilagyi IS, Bornemann-Cimenti H. Palmitoylethanolamide in the treatment of chronic pain: a systematic review and meta-analysis of double-blind randomized controlled trials. Nutrients 2023;15(6):1350.', 'https://doi.org/10.3390/nu15061350'],
 'artukoglu2017': ['Artukoglu 2017', 'Artukoglu BB, Beyer C, Zuloff-Shani A, Brener E, Bloch MH. Efficacy of palmitoylethanolamide for pain: a meta-analysis. Pain Physician 2017;20(5):353–362.', 'https://pubmed.ncbi.nlm.nih.gov/28727699/'],
 'andresen2016': ['Andresen 2016', 'Andresen SR, Bing J, Hansen RM et al. Ultramicronized palmitoylethanolamide in spinal cord injury neuropathic pain: a randomized, double-blind, placebo-controlled trial. Pain 2016;157(9):2097–2103.', 'https://doi.org/10.1097/j.pain.0000000000000623'],
}
Q = {k: {'kurz': a, 'voll': b, 'url': c} for k, (a, b, c) in QUELLEN.items()}


def S(t, say=None):
    return {'t': t, 'say': say} if say else t


def B(t, at):
    return {'t': t, 'at': at}


SZENEN = [
 {'id': 'p0', 'layout': 'kacheln', 'kapitel': 'Einleitung', 'kicker': 'Erklärvideo', 'headline': 'PEA: Vom Eigelb zur Schmerzforschung',
  'sentences': ['PEA: ein Stoff, den dein Körper selbst herstellt, und der zuerst im Eigelb entdeckt wurde.',
                'Seine Geschichte ist eine echte Entdeckungsreise, über fast achtzig Jahre.',
                'Du erfährst, wie ein Arzt auf das Eigelb kam, wie Chemiker den Stoff fanden, warum es eine Grippetablette gab, was eine Nobelpreisträgerin vermutete, wie PEA wirken könnte und was Studien heute zeigen.'],
  'hervorheben_at': 2,
  'kacheln': [('Das Eigelb-Rätsel', 'k1', 'Arzt'), ('Der Stoff wird gefunden', 'k2', 'Chemiker'),
              ('Eine Grippetablette', 'k3', 'Grippetablette'), ('Die Nobelpreisträgerin', 'k4', 'Nobelpreisträgerin'),
              ('Wie PEA wirken könnte', 'k5', 'wirken'), ('Was Studien heute zeigen', 'k6', 'Studien heute')]},
 {'id': 'p1', 'kicker': '1940er Jahre', 'headline': 'Das Eigelb-Rätsel',
  'sentences': ['Unsere Geschichte beginnt in den Vierzigerjahren in New York, bei Kindern mit rheumatischem Fieber.',
                'Diese Entzündung folgte auf eine Halsentzündung durch Streptokokken und schädigte damals oft das Herz.',
                'Der Arzt Alvin Coburn vermutete, dass etwas in der Ernährung die Kinder schützt, und kam auf das Eigelb.',
                'Ohne Eigelb erkrankte in seinen Beobachtungen etwa jedes dritte Kind erneut.',
                'Mit Eigelbpulver war es nur eines von fünfundzwanzig.',
                'Auch bei Meerschweinchen dämpfte Eigelb im Futter eine Gelenkentzündung.',
                'Streng ausgelost waren diese Versuche noch nicht. Aber sie stellten eine spannende Frage: Welcher Stoff im Eigelb wirkt da?'],
  'bullets': [B('Rheumatisches Fieber bei Kindern', 0), B('Idee: Eigelb schützt', 2), B('Weniger Rückfälle', 4), B('Auch bei Meerschweinchen', 5)],
  'quellen': ['coburn1960', 'coburn1954', 'keppel2013'],
  'bilder': [('p1a', None), ('p1b', 1), ('p1c', 2), ('p1d', 3), ('p1e', 5), ('p1f', 6)]},
 {'id': 'p2', 'kicker': '1957', 'headline': 'Der Stoff wird gefunden',
  'sentences': ['Die Spur nahmen Chemiker eines amerikanischen Pharmakonzerns auf.',
                'Sie suchten den Stoff im Eigelb, in Sojalecithin und in Erdnussmehl, und fanden ihn überall.',
                S('1957 stellten sie ihn vor: Palmitoylethanolamid, kurz PEA.', '1957 stellten sie ihn vor: Palmitoylethanolamid, kurz Pe E A.'),  # Aussprache-Wahl 9 (Nutzer 10.11., 0:42, endgültig)
                'Der Name klingt kompliziert, das Molekül ist einfach: eine Fettsäure, wie sie auch in Palmöl steckt, verbunden mit einem kleinen Baustein.',
                'Das Besondere: Dein Körper bildet PEA selbst, in vielen Geweben.',
                'Und bei Meerschweinchen wirkte der reine Stoff gegen die Gelenkentzündung, genau wie das Eigelb.'],
  'bullets': [B('Eigelb, Soja, Erdnuss', 1), B('1957: Palmitoylethanolamid', 2), B('Fettsäure plus Baustein', 3), B('Körpereigen', 4)],
  'quellen': ['kuehl1957', 'keppel2013'],
  'bilder': [('p2a', None), ('p2b', 1), ('p2c', 2), ('p2d', 3), ('p2e', 4), ('p2f', 5)]},
 {'id': 'p3', 'kicker': '1970er Jahre', 'headline': 'Eine Grippetablette',
  'sentences': ['In der Tschechoslowakei wurde aus PEA um 1970 eine Tablette, gegen Grippe und Erkältung.',
                'Getestet wurde sie sorgfältig, doppelblind, an Fabrikarbeitern und an jungen Soldaten.',
                'Mit PEA bekamen deutlich weniger einen Atemwegsinfekt, in einem Winter nur etwa halb so viele.',
                'Eine neuere kleine Studie konnte diesen Schutz allerdings nicht klar bestätigen.',
                'Trotzdem verschwand die Tablette damals vom Markt. Warum, ist nicht genau überliefert.',
                'Vermutlich lag es auch daran, dass niemand wusste, wie PEA wirkt. Die Forschung schlief für viele Jahre ein.',
                'Tipp für dich: Gegen Grippe sind Impfung und Schonung die bewährten Mittel. Ob PEA dazu passt, besprich mit Arzt oder Ärztin.'],
  'bullets': [B('Tablette gegen Grippe', 0), B('Doppelblind getestet', 1), B('Weniger Infekte', 2), B('Verschwand vom Markt', 4)],
  'quellen': ['masek1974', 'kahlich1979', 'bortoletto2025', 'keppel2013'],
  'bilder': [('p3a', None), ('p3b', 1), ('p3c', 2), ('p3d', 4), ('p3e', 5), ('p3f', 6)]},
 {'id': 'p4', 'kicker': '1990er Jahre', 'headline': 'Die Nobelpreisträgerin',
  'sentences': ['Anfang der Neunziger weckte eine berühmte Forscherin PEA wieder auf: Rita Levi-Montalcini, Nobelpreis für die Entdeckung des Nervenwachstumsfaktors.',
                'Ihr Team untersuchte Mastzellen. Das sind Wächterzellen im Gewebe, die bei Reizung Entzündungsstoffe ausschütten.',
                'Die Idee: Wo Gewebe verletzt wird, bildet der Körper selbst Stoffe wie PEA, die diese Wächter beruhigen.',
                'Eine körpereigene Entzündungsbremse, direkt vor Ort.',
                S('Eine Weile dachte man sogar, PEA docke an dieselben Rezeptoren an wie Wirkstoffe aus Hanf.',
                  'Eine Weile dachte man sogar, Pe E A docke an dieselben Rezeptoren an wie Wirkstoffe aus Hanf.'),  # „Pe-E-A“ klang hier wie „PEEA“ (Nutzer 10.11.)
                'Das ließ sich nicht bestätigen. Aber die Idee der Entzündungsbremse gab der Forschung neuen Schwung.'],
  'bullets': [B('Mastzellen: Wächter im Gewebe', 1), B('Körpereigene Entzündungsbremse', 3), B('Hanf-Rezeptor? Nicht bestätigt', 5)],
  'quellen': ['nobel1986', 'aloe1993', 'facci1995', 'lambert2002'],
  'bilder': [('p4a', None), ('p4b', 1), ('p4c', 2), ('p4d', 3), ('p4e', 4), ('p4f', 5)]},
 {'id': 'p5', 'kicker': 'Wirkung', 'headline': 'Wie PEA wirken könnte',
  'sentences': ['2005 fand eine Gruppe in Kalifornien einen Schalter: PEA aktiviert einen Rezeptor im Zellkern, der Entzündung drosselt.',
                'Mäuse ohne diesen Schalter sprachen auf PEA nicht mehr an.',
                'Außerdem ist PEA ein Verwandter von Anandamid, einem körpereigenen Botenstoff.',
                'Sein Name kommt vom Sanskrit-Wort für Glückseligkeit.',
                'Beide werden von denselben Enzymen abgebaut, und PEA kann den Abbau von Anandamid bremsen. Man nennt das den Entourage-Effekt, den Effekt des Gefolges.',
                'Das alles stammt aus Zell- und Tierversuchen. Wie genau PEA im Menschen wirkt, erforschen Wissenschaftler noch.'],
  'bullets': [B('Schalter im Zellkern', 0), B('Verwandt mit Anandamid', 2), B('Bremst dessen Abbau', 4), B('Beim Menschen: noch offen', 5)],
  'quellen': ['loverme2005', 'devane1992', 'jonsson2001', 'ho2008'],
  'bilder': [('p5a', None), ('p5b', 1), ('p5c', 2), ('p5d', 3), ('p5e', 4), ('p5f', 5)]},
 {'id': 'p6', 'kicker': 'Heute', 'headline': 'Was Studien heute zeigen',
  'sentences': ['Heute gibt es PEA als Kapseln, oft sehr fein gemahlen, damit der Körper mehr davon aufnehmen kann.',
                'In Deutschland wird es meist als Nahrungsergänzung verkauft, nicht als Arzneimittel.',
                'Untersucht wird es vor allem bei chronischen Schmerzen, zum Beispiel bei Nervenschmerzen.',
                'Eine unabhängige Auswertung von elf doppelblinden Studien fand weniger Schmerz, im Mittel gut eineinhalb Punkte auf einer Skala bis zehn.',
                'Die Studien waren allerdings klein, und viele nutzten Präparate desselben Herstellers.',
                'Nicht jede fand einen Unterschied zu Placebo.',
                'Gut verträglich war PEA in den Studien, schwere Nebenwirkungen traten nicht auf.',
                'Offen ist, wie es bei langer Einnahme aussieht, und für Schwangere fehlen Daten.',
                'Tipp für dich: Wenn du PEA gegen Schmerzen ausprobieren möchtest, sprich vorher mit Arzt oder Ärztin, und setz verordnete Mittel nicht eigenmächtig ab.'],
  'bullets': [B('Kapseln, Nahrungsergänzung', 1), B('Weniger Schmerz, im Mittel gut 1,5 von 10 Punkten', 3),
              B('Kleine Studien', 4), B('Gut verträglich', 6)],
  'quellen': ['langilli2023', 'gabrielsson2016', 'artukoglu2017', 'andresen2016'],
  'bilder': [('p6a', None), ('p6b', 1), ('p6c', 2), ('p6d', 3), ('p6e', 4), ('p6f', 6), ('p6g', 7), ('p6h', 8)]},
 {'id': 'p7', 'kapitel': 'Fazit', 'kicker': 'Fazit', 'headline': 'Das Wichtigste',
  'sentences': ['PEA hat eine erstaunliche Reise hinter sich: vom Eigelb über eine Grippetablette bis in die Schmerzforschung.',
                'Dein Körper bildet es selbst, als eine Art Entzündungsbremse.',
                'Bei Schmerzen sind die ersten Studien ermutigend.',
                'Jetzt braucht es große, unabhängige Studien. Vielleicht schreiben sie das nächste Kapitel dieser Geschichte.',
                'Die Quellen stehen in der Beschreibung.',
                'Gut, dass du dich informierst. Das Video kann das Gespräch mit Arzt oder Ärztin unterstützen, aber nicht ersetzen. Bis zum nächsten Video!'],
  'bullets': [B('Vom Eigelb zur Kapsel', 0), B('Körpereigene Entzündungsbremse', 1), B('Schmerz: erste Studien ermutigend', 2), B('Große Studien fehlen noch', 3)],
  'quellen': ['langilli2023', 'gabrielsson2016'],
  'bilder': [('p7a', None), ('p7b', 1), ('p7c', 2), ('p7d', 3), ('p7e', 5)]},
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
            'aussprache': {'Palmitoylethanolamid': 'Palmitoül-ethanolamid', 'PEA': 'Pe-E-A'},
            'titel': 'PEA: Vom Eigelb zur Schmerzforschung', 'stil': stil,
            'untertitel': 'Ein Erklärvideo über Palmitoylethanolamid: wie es entdeckt wurde, wie es wirken könnte und was Studien heute zeigen.',
            'fuss': 'Sprecherstimme synthetisch (ElevenLabs). Bilder KI-generiert. Das Video ersetzt nicht das Gespräch mit Arzt oder Ärztin.',
            'scenes': szenen, 'quellen': Q}


if __name__ == '__main__':
    for stil in STILE:
        json.dump(bauen(stil), open(f'szenen_{stil}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(bauen('I'), open('szenen.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)  # für Ton und Hörprobe
    w = sum(len((x if isinstance(x, str) else x['t']).split()) for sc in SZENEN for x in sc['sentences'])
    print(len(STILE), 'Drehbücher,', w, 'Wörter')
