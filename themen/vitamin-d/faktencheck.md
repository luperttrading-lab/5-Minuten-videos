# Faktencheck Vitamin D (03.11.2026)

Geprüft von zwei Recherche-Agenten mit Websuche, alle DOIs per `curl -sI https://doi.org/…` aufgelöst (302), Abstracts
über PubMed, Behördentexte selbst geladen. Urteil = Ampel im Video: **stark** (belegt) · **mittel** (teilweise) ·
**keine** (nicht haltbar; „ist falsch“ bei Gegenbeleg, „ist nicht belegt“ ohne Belege).

## Behauptungen sammeln: was ging, was nicht
- YouTube-Suche ging (yt-dlp `ytsearch`). Meistgesehene deutsche Treffer: DoktorWeigl (443 T, 316 T, 155 T Aufrufe),
  „Schmerz beiseite“ (775 T: „No doctor has ever explained vitamin D so clearly“; 256 T: „60.000 IE täglich? Diese Klinik
  zeigt erstaunliche Ergebnisse“), Pommes Män (107 T: „50.000 Einheiten täglich für Wochen“), Christian Lainé
  (458 T: „10.000 Einheiten jeden Tag“), BRAINEFFECT (307 T, Hersteller mit eigenen Präparaten), AMM/Spitz („Vitamin-D-Mangel
  als Ursache für Diabetes“), MAITHINK X (2,1 Mio., wissenschaftlich, kein Behauptungsvideo).
- **Transkripte und Beschreibungen: nicht abrufbar.** YouTube antwortete mit HTTP 429 und „Sign in to confirm you’re not a
  bot“, auch mit `player_client=web_embedded`. Ein weiteres Umgehen der Bot-Sperre wurde nicht versucht. Affiliate-Links und
  Rabattcodes konnten deshalb nicht geprüft werden. Behauptungen stammen aus Titeln und Presse/Websuche.
- Herkunft wird im Video nicht genannt („Viele raten …“, „Oft heißt es …“).

## A. Herkunft
| Aussage | Urteil | Beleg |
|---|---|---|
| Haut bildet bei Sonne 80–90 % | stark | BfR-FAQ 2025 wörtlich; Ernährung liefert in D nur 2–4 µg/Tag |
| Essen allein reicht | keine (falsch) | 2–4 µg aus Nahrung vs. DGE-Schätzwert 20 µg ohne Eigenbildung |
| Fettfisch, Ei, Pilze | stark | BfR-Tabelle: Hering gesalzen 25,6; Lachs geräuchert 4,2; Ei 2,9; Champignons 1,9 µg/100 g |
| Okt.–März reicht die Sonne in D nicht | stark | BfR-FAQ wörtlich; Körper speichert in Fett und Muskeln |
| 5–25 min Gesicht, Hände, Arme, mehrmals pro Woche | stark | BfR-FAQ |
| Alter, dunkle Haut, Sonnencreme, Übergewicht | stark | BfR-FAQ; Rabenberg 2015 (BMI) |
| Schattenregel als Vitamin-D-Regel | mittel | stammt aus dem Sonnenschutz (45° ≈ UV-Index 4), physikalisch plausibel, für Vitamin D nicht geprüft → im Video nur als Faustregel, kein Stichpunkt |

## B. Verbreitung (DEGS1, 6.995 Erwachsene)
- Standardisiert (Rabenberg 2018, so zitiert BfR heute): < 30 nmol/l 15 %, 30–< 50 nmol/l 41 %, ≥ 50 nmol/l 44 %;
  > 75 nmol/l nur 9 %. Originalmessung 2015: 30,2 / 31,4 / 38,4 %. Video nutzt die standardisierten Werte.
- „Fast alle Deutschen haben Mangel“ (88 % bei Grenze 30 ng/ml = 75 nmol/l): **keine (falsch)**, hängt an der Grenze.
- Winter deutlich niedriger: **stark** (Rabenberg 2015).
- Einheiten ng/ml × 2,5 = nmol/l: **stark**. Zielwert: IOM 2011 50 nmol/l für 97,5 %; Endocrine Society 2011 ≥ 75;
  Endocrine Society 2024: kein belegter Zielwert. „≥ 75 nötig“: **mittel** (umstritten). „100+ ng/ml optimal“: keine
  (BfR: > 100 nmol/l mit negativen Effekten verbunden) – nicht im Video, um Zahlen zu sparen.

## C. Testen
- Endocrine Society 2024 (Demay): rät von Routinetests ab, auch bei Übergewicht und dunkler Haut; empirische Einnahme ohne
  Test für 1–18 J., ≥ 75 J., Schwangere, Hochrisiko-Prädiabetes; schwache Empfehlungen.
- Deutschland: Kassenleistung bei hinreichendem Verdacht (z. B. Niereninsuffizienz), sonst IGeL, GOÄ 4138 27,98 € (Faktor 1,0)
  plus Blutentnahme/Beratung (KVB 2026). IGeL-Monitor: Screening „unklar“, keine Studien zu Nutzen oder Schaden.
- „Alle sollten regelmäßig testen“: **keine (nicht belegt)**.

## D. Große Studien (Teilnehmer meist gut versorgt: VITAL 30,8 ng/ml, D2d 27,7, ViDA 26,5, DO-HEALTH 22,4)
- VITAL (Manson 2019): 25.871, 2000 IE/Tag, 5,3 J. Krebs HR 0,96 (0,88–1,06); Herz-Kreislauf 0,97 (0,85–1,12);
  Sterblichkeit 0,99. Pharmavite spendete Präparate. → „Schützt vor Krebs / Herz“: **keine (falsch)**.
- D-Health (Neale 2022): 21.315, 60.000 IE/Monat, 5 J., Sterblichkeit HR 1,04 (0,93–1,18). Herzinfarkt sekundär 0,81 (Thompson 2023).
- ViDA (Scragg 2017): 5.110, 100.000 IE/Monat, Herz-Kreislauf HR 1,02 (0,87–1,20).
- DO-HEALTH (Bischoff-Ferrari 2020): 2.157 ab 70, 2000 IE/Tag, 3 J.: kein Effekt auf Brüche, Infekte, Blutdruck. Industrie-Mitfinanzierung (DSM u. a.).
- Brüche bei Normalversorgten: VITAL (LeBoff 2022) HR 0,98 (0,89–1,08); Bolland 2018 (81 RCTs) RR 1,00 → **keine (falsch)**.
- Krebstod: Keum 2019 RR 0,87 (0,79–0,96); Zhang 2019 0,84; Kuznia 2023 (IPD, 104.727) gesamt 0,94 (0,86–1,02) n. s., täglich 0,88 (0,78–0,98), Bolus 1,07 → **mittel**, Untergruppe.
- Muster: Autier 2014 (290 Kohorten, 172 RCTs): niedriger Spiegel eher Marker als Ursache von Krankheit.

## E. Weitere Versprechen
- Atemwegsinfekte (Jolliffe 2021, 46 RCTs): OR 0,92 (0,86–0,99), 61,3 % vs. 62,3 % → **mittel**, kleiner Effekt; täglich 0,78. Autoren mit Industriegeldern (DSM, Pharma Nord).
- COVID (CORONAVIT, Jolliffe 2022, 6.200): OR 1,39 (0,98–1,97) bzw. 1,13 → „schützt vor Corona“ **keine (falsch)**.
- Depression (VITAL-DEP, Okereke 2020, 18.353): HR 0,97 (0,87–1,09) → **keine (falsch)**.
- Diabetes: D2d HR 0,88 (0,75–1,04) n. s.; Meta-Analyse Pittas 2023 (3 RCTs) HR 0,85 (0,75–0,96) nur bei Prädiabetes → **mittel**.
- Autoimmun (Hahn 2022) HR 0,78 (0,61–0,99), nach Absetzen verschwunden (Costenbader 2024) – nicht im Video (Platz).
- Telomere (Zhu 2025, VITAL, n = 1.009 in der Analyse): 140 Basenpaare weniger Verkürzung in 4 J. (KI 7–270), p = 0,039,
  nach 2 J. n. s., keine Korrektur für mehrfaches Testen. „3 Jahre weniger Altern“ steht im Paper selbst, hochgerechnet aus
  ≈ 46 bp/Jahr einer anderen Kohorte. Surrogat, keine klinischen Endpunkte → **mittel**, Zusatz „erst eine Studie“.

## F. Megadosen und Grenzwerte
- DGE-Schätzwert 20 µg (800 IE) bei fehlender Eigenbildung; BfR-Empfehlung höchstens 20 µg/Tag in Nahrungsergänzung (keine gesetzliche Höchstmenge); EFSA-UL 100 µg (4.000 IE), 2023 bestätigt, abgeleitet von LOAEL 250 µg = **10.000 IE** (Hyperkalziurie). 1 µg = 40 IE.
- „10.000 IE täglich über Jahre sind sicher“: **keine (falsch)** – genau die Dosis mit ersten Nebenwirkungen; Burt 2019: Knochendichte bei 10.000 IE stärker gesunken.
- Risiken: Hyperkalzämie → Nierensteine, Nierenverkalkung, bleibende Abnahme der Nierenfunktion (BfR). Fälle: BfR-Mitteilung 045/2026, Säuglingsvergiftung mit Erwachsenen-Präparat, „mehrere Fälle“; Coimbra-Fallberichte mit Nierenversagen (nur Suchtreffer, nicht im Video).
- Bolus: Sanders 2010 (2.256 Frauen ≥ 70, 500.000 IE/Jahr): Stürze RR 1,15 (1,02–1,30), Brüche 1,26 (1,00–1,59). Bischoff-Ferrari 2016: 60.000 IE/Monat mehr Stürze (klein, n = 200). BfR 031/2025 rät von Einzeldosen im Abstand von Tagen/Wochen ab → „hohe Einzeldosen unbedenklich“ **keine (falsch)**.
- Stiftung Warentest (test 01/2026, 25 Mittel): „Die meisten Mittel im Test sind überdosiert“; Kombis mit K, Mg, Zink durchgefallen → **stark**.
- K2 dazu: Verbraucherzentrale 2026 „keine verlässliche Empfehlung“, DVO 2023 gegen K2 bei Osteoporose → **keine (nicht belegt)**.
- Magnesium (Dai 2018, 180 Teilnehmende): regulierend, nicht einseitig steigernd; ohne klinische Endpunkte → **mittel**, nicht im Video (Platz).

## G. Wo es klar sinnvoll ist
- Säuglinge: 400–500 IE täglich bis zum zweiten erlebten Frühsommer (BfR) → **stark**.
- Pflegeheim: BfR rät, bis 20 µg/Tag zu erwägen. Chapuy 1992 (3.270 Frauen, 84 J., D + Calcium): 43 % weniger Hüftbrüche; Cochrane Avenell 2014: D + Calcium Hüfte RR 0,84 (0,74–0,96), D allein kein Effekt → **stark** (mit Calcium).
- Schwangere: Netzwerk Gesund ins Leben 2018 für Schwangere mit wenig Sonne oder dunkler Haut → **mittel**, im Video als Hinweis.

## H. Nachträge 03.11. (zweite Fassung, Nutzerwunsch: fairer gegenüber Vitamin D)
- Sonne: Rhodes 2010 (120 Erwachsene, Manchester, simulierte Sommersonne 1,3 SED 3×/Woche, 6 Wochen, T-Shirt und kurze Hose ≈ 35 % Haut): 90 % erreichten ≥ 20 ng/ml, nur 26,2 % ≥ 32 ng/ml. Gesicht und Arme sind höchstens ≈ 25 % der Haut → „Gesicht und Arme reichen“ **mittel** (reicht für die Untergrenze eher knapp, für höhere Werte kaum).
- Winter: Rabenberg 2015 (Originalmessung): im Sommer hatte die Hälfte ≥ 50 nmol/l, im Winter lag ein Viertel unter 30 nmol/l. Standardisierte Werte nach Jahreszeit sind nicht veröffentlicht; das Video sagt deshalb nur „Jahresmittel, im Winter und Frühjahr deutlich höher“, ohne Mischung der beiden Datenstände.
- Echter Mangel: Sutherland 2022 (Mendelsche Randomisierung, 307.601 UK-Biobank-Teilnehmer): L-förmig, OR 1,25 (1,16–1,35) für 25 gegen 50 nmol/l, darüber flach. Methode später kritisiert → im Video „deutet an“.
- Corona-Behandlung: Entrenas Castillo 2020 (Córdoba, 76 Patienten, offen, Calcifediol): Intensivstation 1/50 gegen 13/26; Zuteilungsliste für Personal einsehbar, Spiegel nicht gemessen. Murai 2021 (JAMA, 240 Klinikpatienten, doppelblind, 200.000 IE einmalig): kein Unterschied bei Liegedauer (Hauptendpunkt), Intensivstation, Beatmung, Sterblichkeit. → „frühe kleine Studien sahen Nutzen, größere bestätigten das nicht“.
- Dosis: EFSA-UL 4.000 IE als sichere Obergrenze ist eine Behördenangabe, keine Empfehlung; Tipp nennt DGE-Bedarf 800 IE und UL 4.000 IE, mehr nur ärztlich.
- Ton: Rauschunterdrückung und De-Esser laufen im Renderer (AUFBEREITUNG); gemessen: Pegel in Sprechpausen −58 bis −75 dB (5.–1. Perzentil der nicht stummen 50-ms-Fenster).

## Quellenverzeichnis
| ID | Kurz | Voll | URL |
|---|---|---|---|
| bfr2025 | BfR 2025 | Bundesinstitut für Risikobewertung: Ausgewählte Fragen und Antworten zu Vitamin D, Stand 30.12.2025. | https://www.bfr.bund.de/cm/343/ausgewaehlte-fragen-und-antworten-zu-vitamin-d.pdf |
| rabenberg2015 | Rabenberg et al. 2015 | Rabenberg M et al. Vitamin D status among adults in Germany – results from DEGS1. BMC Public Health 2015;15:641. | https://doi.org/10.1186/s12889-015-2016-7 |
| rabenberg2018 | Rabenberg et al. 2018 | Rabenberg M et al. Implications of standardization of serum 25-hydroxyvitamin D data for the evaluation of vitamin D status in Germany. BMC Public Health 2018;18:845. | https://doi.org/10.1186/s12889-018-5769-y |
| ross2011 | Ross et al. 2011 | Ross AC et al. The 2011 Report on Dietary Reference Intakes for Calcium and Vitamin D from the Institute of Medicine. J Clin Endocrinol Metab 2011;96(1):53–58. | https://doi.org/10.1210/jc.2010-2704 |
| demay2024 | Demay et al. 2024 | Demay MB et al. Vitamin D for the Prevention of Disease: An Endocrine Society Clinical Practice Guideline. J Clin Endocrinol Metab 2024;109(8):1907–1947. | https://doi.org/10.1210/clinem/dgae290 |
| kvb2026 | KVB 2026 | Kassenärztliche Vereinigung Bayerns: Vitamin D zwischen Verordnungsfähigkeit und Patientenwunsch. Verordnung aktuell, 26.02.2026. | https://www.kvb.de/fileadmin/kvb/Mitglieder/Verordnungen/VO-aktuell/2026-DS/KVB-VA-260226-WIS-Vitamin-D.pdf |
| autier2014 | Autier et al. 2014 | Autier P et al. Vitamin D status and ill health: a systematic review. Lancet Diabetes Endocrinol 2014;2(1):76–89. | https://doi.org/10.1016/S2213-8587(13)70165-7 |
| manson2019 | Manson et al. 2019 | Manson JE et al. Vitamin D Supplements and Prevention of Cancer and Cardiovascular Disease (VITAL). N Engl J Med 2019;380:33–44. (Präparate von Pharmavite gespendet) | https://doi.org/10.1056/NEJMoa1809944 |
| neale2022 | Neale et al. 2022 | Neale RE et al. The D-Health Trial: a randomised controlled trial of the effect of vitamin D on mortality. Lancet Diabetes Endocrinol 2022;10(2):120–128. | https://doi.org/10.1016/S2213-8587(21)00345-4 |
| scragg2017 | Scragg et al. 2017 | Scragg R et al. Effect of Monthly High-Dose Vitamin D Supplementation on Cardiovascular Disease in the Vitamin D Assessment Study. JAMA Cardiol 2017;2(6):608–616. | https://doi.org/10.1001/jamacardio.2017.0175 |
| bischoff2020 | Bischoff-Ferrari et al. 2020 | Bischoff-Ferrari HA et al. Effect of Vitamin D Supplementation, Omega-3 Fatty Acids, and a Strength-Training Exercise Program on Clinical Outcomes in Older Adults: The DO-HEALTH Randomized Clinical Trial. JAMA 2020;324(18):1855–1868. (Industrie-Mitfinanzierung) | https://doi.org/10.1001/jama.2020.16909 |
| leboff2022 | LeBoff et al. 2022 | LeBoff MS et al. Supplemental Vitamin D and Incident Fractures in Midlife and Older Adults. N Engl J Med 2022;387:299–309. | https://doi.org/10.1056/NEJMoa2202106 |
| bolland2018 | Bolland et al. 2018 | Bolland MJ et al. Effects of vitamin D supplementation on musculoskeletal health: a systematic review, meta-analysis, and trial sequential analysis. Lancet Diabetes Endocrinol 2018;6(11):847–858. | https://doi.org/10.1016/S2213-8587(18)30265-1 |
| kuznia2023 | Kuznia et al. 2023 | Kuznia S et al. Efficacy of vitamin D3 supplementation on cancer mortality: Systematic review and individual patient data meta-analysis of randomised controlled trials. Ageing Res Rev 2023;87:101923. | https://doi.org/10.1016/j.arr.2023.101923 |
| keum2019 | Keum et al. 2019 | Keum N et al. Vitamin D supplementation and total cancer incidence and mortality: a meta-analysis of randomized controlled trials. Ann Oncol 2019;30(5):733–743. | https://doi.org/10.1093/annonc/mdz059 |
| jolliffe2021 | Jolliffe et al. 2021 | Jolliffe DA et al. Vitamin D supplementation to prevent acute respiratory infections: a systematic review and meta-analysis of aggregate data from randomised controlled trials. Lancet Diabetes Endocrinol 2021;9(5):276–292. | https://doi.org/10.1016/S2213-8587(21)00051-6 |
| jolliffe2022 | Jolliffe et al. 2022 | Jolliffe DA et al. Effect of a test-and-treat approach to vitamin D supplementation on risk of all cause acute respiratory tract infection and covid-19 (CORONAVIT). BMJ 2022;378:e071230. (Hersteller-Mitfinanzierung) | https://doi.org/10.1136/bmj-2022-071230 |
| okereke2020 | Okereke et al. 2020 | Okereke OI et al. Effect of Long-term Vitamin D3 Supplementation vs Placebo on Risk of Depression or Clinically Relevant Depressive Symptoms (VITAL-DEP). JAMA 2020;324(5):471–480. | https://doi.org/10.1001/jama.2020.10224 |
| pittas2023 | Pittas et al. 2023 | Pittas AG et al. Vitamin D and Risk for Type 2 Diabetes in People With Prediabetes: A Systematic Review and Meta-analysis of Individual Participant Data From 3 Randomized Clinical Trials. Ann Intern Med 2023;176(3):355–363. | https://doi.org/10.7326/M22-3018 |
| zhu2025 | Zhu et al. 2025 | Zhu H et al. Vitamin D3 and marine ω-3 fatty acids supplementation and leukocyte telomere length: 4-year findings from VITAL. Am J Clin Nutr 2025. | https://doi.org/10.1016/j.ajcnut.2025.05.003 |
| efsa2023 | EFSA 2023 | EFSA NDA Panel. Scientific opinion on the tolerable upper intake level for vitamin D, including the derivation of a conversion factor for calcidiol monohydrate. EFSA J 2023;21(8):e08145. | https://doi.org/10.2903/j.efsa.2023.8145 |
| burt2019 | Burt et al. 2019 | Burt LA et al. Effect of High-Dose Vitamin D Supplementation on Volumetric Bone Density and Bone Strength: A Randomized Clinical Trial. JAMA 2019;322(8):736–745. | https://doi.org/10.1001/jama.2019.11889 |
| bfr045_2026 | BfR 2026 | BfR-Mitteilung 045/2026: Vitamin-D-Vergiftung bei Säuglingen, 07.08.2026. | https://www.bfr.bund.de/mitteilung/vitamin-d-vergiftung-bei-saeuglingen/ |
| sanders2010 | Sanders et al. 2010 | Sanders KM et al. Annual high-dose oral vitamin D and falls and fractures in older women: a randomized controlled trial. JAMA 2010;303(18):1815–1822. | https://doi.org/10.1001/jama.2010.594 |
| bfr031_2025 | BfR 2025b | BfR-Stellungnahme 031/2025: Einnahme hoher Einzeldosen Vitamin D über Nahrungsergänzungsmittel im Abstand von Tagen oder Wochen birgt gesundheitliche Risiken. | https://doi.org/10.17590/20250903-104032-0 |
| warentest2025 | Stiftung Warentest 2025 | Stiftung Warentest: Vitamin-D-Präparate – Für viele überflüssig. Pressemitteilung 15.12.2025 (test 01/2026). | https://www.test.de/presse/pressemitteilungen/Vitamin-D-Praeparate-Fuer-viele-ueberfluessig-6259497-0/ |
| vz2026 | Verbraucherzentrale 2026 | Verbraucherzentrale: Vitamin D besser mit Vitamin K2? Stand 15.07.2026. | https://www.verbraucherzentrale.de/faq/lebensmittel/vitamin-d-besser-mit-vitamin-k2-39144 |
| chapuy1992 | Chapuy et al. 1992 | Chapuy MC et al. Vitamin D3 and calcium to prevent hip fractures in elderly women. N Engl J Med 1992;327:1637–1642. | https://doi.org/10.1056/NEJM199212033272305 |
| avenell2014 | Avenell et al. 2014 | Avenell A et al. Vitamin D and vitamin D analogues for preventing fractures in post-menopausal women and older men. Cochrane Database Syst Rev 2014;CD000227. | https://doi.org/10.1002/14651858.CD000227.pub4 |
| koletzko2018 | Koletzko et al. 2018 | Koletzko B et al. Ernährung und Lebensstil vor und während der Schwangerschaft – Handlungsempfehlungen des bundesweiten Netzwerks Gesund ins Leben. Geburtsh Frauenheilk 2018;78:1262–1282. | https://www.gesund-ins-leben.de/fileadmin/resources/import/pdf/3589_empfehlungen_vor_und_in_schwangerschaft_2018_gebfra.pdf |
| rhodes2010 | Rhodes et al. 2010 | Rhodes LE, Webb AR et al. Recommended summer sunlight exposure levels can produce sufficient (≥20 ng/ml) but not the proposed optimal (≥32 ng/ml) 25(OH)D levels at UK latitudes. J Invest Dermatol 2010;130(5):1411–1418. | https://doi.org/10.1038/jid.2009.417 |
| sutherland2022 | Sutherland et al. 2022 | Sutherland JP, Zhou A, Hyppönen E. Vitamin D Deficiency Increases Mortality Risk in the UK Biobank: A Nonlinear Mendelian Randomization Study. Ann Intern Med 2022;175(11):1552–1559. | https://doi.org/10.7326/M21-3324 |
| entrenas2020 | Entrenas Castillo et al. 2020 | Entrenas Castillo M et al. Effect of calcifediol treatment and best available therapy versus best available therapy on intensive care unit admission and mortality among patients hospitalized for COVID-19: A pilot randomized clinical study. J Steroid Biochem Mol Biol 2020;203:105751. (offen, 76 Patienten) | https://doi.org/10.1016/j.jsbmb.2020.105751 |
| murai2021 | Murai et al. 2021 | Murai IH et al. Effect of a Single High Dose of Vitamin D3 on Hospital Length of Stay in Patients With Moderate to Severe COVID-19: A Randomized Clinical Trial. JAMA 2021;325(11):1053–1060. | https://doi.org/10.1001/jama.2020.26848 |
