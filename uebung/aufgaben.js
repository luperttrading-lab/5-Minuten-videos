// Übungen zu den Mathe-Videos. Jede Übung erzeugt Aufgaben {frage, loesung, weg} und kann Stufen haben.
// Neue Übung: hier ein Objekt in UEBUNGEN ergänzen (id, titel, video, stufen[], erzeuge(stufe, n), weg(aufgabe)).
// Danach APP_VERSION in index.html hochzählen und sw.js ASSETS prüfen.

const zufallInt = n => {                           // gleichverteilt 0 … n−1 (Verwerfungsmethode wie im Würfel)
  const max = Math.floor(0x100000000 / n) * n, a = new Uint32Array(1);
  do crypto.getRandomValues(a); while (a[0] >= max);
  return a[0] % n;
};
const mischen = liste => { for (let i = liste.length - 1; i > 0; i--) { const j = zufallInt(i + 1); [liste[i], liste[j]] = [liste[j], liste[i]]; } return liste; };

const UEBUNGEN = [
  {
    id: 'einmaleins-1119',
    titel: '11 bis 19 mal 11 bis 19',
    video: 'Einer rüber · mal 10 · Einer · Einer dazu',
    auto: true,                                    // alle Ergebnisse dreistellig (121 … 361): nach 3 Ziffern prüfen
    antworten: [100, 399],                         // Grammatik der Spracherkennung: jede Zahl 100 … 399 (auch falsche)
    stufen: [
      { id: 'alle', name: 'Alle Zahlen', info: 'z. B. 16 · 18' },
      { id: 'zehn', name: 'Einer ergeben 10', info: 'z. B. 12 · 18 = 200 + 16' },
    ],
    erzeuge(stufe, anzahl) {
      const paare = [];                            // ohne Reihenfolge: [12, 18] steht für 12 · 18 und 18 · 12
      for (let x = 11; x <= 19; x++) for (let y = x; y <= 19; y++)
        if (stufe !== 'zehn' || (x - 10) + (y - 10) === 10) paare.push([x, y]);
      let ziehe;
      if (stufe === 'zehn') {
        // Nutzerwunsch 04.11.: so wenig Doppelte wie möglich. Mit beiden Reihenfolgen gibt es hier 9 Aufgaben
        // (11·19, 19·11 … 16·14, dazu 15·15 nur einmal) – bei 10 Aufgaben ist genau EINE Wiederholung nötig, nie 15 · 15.
        const varianten = paare.flatMap(([x, y]) => (x === y ? [[x, y]] : [[x, y], [y, x]]));
        ziehe = () => {
          const l = [];
          while (l.length < anzahl) {
            const runde = mischen(varianten.slice()), rest = anzahl - l.length;
            l.push(...(rest >= runde.length ? runde : runde.filter(([x, y]) => x !== y).slice(0, rest)));
          }
          return mischen(l);
        };
      } else {
        // 10 verschiedene Paare, jedes zufällig gedreht: keine Aufgabe doppelt, auch nicht verdreht
        ziehe = () => mischen(paare.slice()).slice(0, anzahl).map(([x, y]) => (zufallInt(2) ? [x, y] : [y, x]));
      }
      const gleichesPaar = (a, b) => Math.min(...a) === Math.min(...b) && Math.max(...a) === Math.max(...b);
      const passt = l => l.every((a, i) =>
        (i === 0 || !gleichesPaar(a, l[i - 1])) &&                                   // nie 12·18 und dann 18·12 (oder 12·18)
        l.every((b, j) => j <= i || !(a[0] === b[0] && a[1] === b[1]) || j - i >= 4)); // Wiederholung frühestens 4 später
      let liste = ziehe();
      for (let k = 0; k < 2000 && !passt(liste); k++) liste = ziehe();
      return liste.map(([x, y]) => this.aufgabe(x, y));
    },
    aufgabe(x, y) {
      return { x, y, frage: `${x} · ${y}`, loesung: x * y };
    },
    weg({ x, y }) {                                // Lösungsweg mit den drei Schritten aus dem Video
      const a = x - 10, b = y - 10, s = x + b;
      return [
        { nr: 1, titel: 'Einer rüber', text: `${x} + <b class="c2">${b}</b> = ${s}` },
        { nr: 2, titel: 'mal 10', text: `${s} · 10 = <b class="c10">${s * 10}</b>` },
        { nr: 3, titel: 'Einer · Einer dazu', text: `+ <b class="c1">${a}</b> · <b class="c2">${b}</b> = <b class="c3">${a * b}</b>` },
        { nr: '=', titel: '', text: `${s * 10} + ${a * b} = <b class="cok">${x * y}</b>` },
      ];
    },
  },
];

// Motivationssätze für das Ende einer Runde (wie werkzeug/motivation.py, beim Ergänzen beide pflegen)
const SPRUECHE = [
  'Das ist kein Hexenwerk.', 'Das ist keine Raketenwissenschaft.', 'Übung macht den Meister.', 'Das kann jeder lernen.',
  'Nach ein paar Runden geht das wie von selbst.', 'Dein Kopf ist schneller, als du denkst.', 'Jeder fängt mal langsam an.',
  'Mit jeder Aufgabe wird es leichter.', 'Dafür musst du kein Mathe-Genie sein.', 'Ein paar Minuten am Tag reichen schon.',
];

// Gesprochene Zahl (Vosk liefert Wörter) → Zahl 0 … 999. Die Wörter werden zusammengezogen, weil das Modell
// „zweihundertachtundachtzig“ als „zweihundert achtundachtzig“ oder „zweihundert acht und achtzig“ liefern kann.
const EINER = { null: 0, eins: 1, ein: 1, eine: 1, zwei: 2, zwo: 2, drei: 3, vier: 4, 'fünf': 5, sechs: 6, sieben: 7, acht: 8, neun: 9 };
const ZEHNER = { zehn: 10, elf: 11, 'zwölf': 12, dreizehn: 13, vierzehn: 14, 'fünfzehn': 15, sechzehn: 16, siebzehn: 17,
  achtzehn: 18, neunzehn: 19, zwanzig: 20, 'dreißig': 30, vierzig: 40, 'fünfzig': 50, sechzig: 60, siebzig: 70, achtzig: 80,
  neunzig: 90 };
function zahlwortZuZahl(text) {
  const s = text.toLowerCase().replace(/\[unk\]/g, ' ').replace(/[^a-zäöüß]/g, '');
  if (!s) return null;
  const m = s.match(/^(?:(ein|eins|zwei|zwo|drei|vier|fünf|sechs|sieben|acht|neun)?(hundert))?(.*)$/);
  let wert = 0;
  if (m[2]) wert = 100 * (m[1] ? EINER[m[1]] : 1);
  let rest = m[3].replace(/^und/, '');
  if (!rest) return m[2] ? wert : null;
  if (rest in ZEHNER) return wert + ZEHNER[rest];
  if (rest in EINER) return wert + EINER[rest];
  const k = rest.match(/^(ein|zwei|drei|vier|fünf|sechs|sieben|acht|neun)und(zwanzig|dreißig|vierzig|fünfzig|sechzig|siebzig|achtzig|neunzig)$/);
  if (k) return wert + EINER[k[1]] + ZEHNER[k[2]];
  return null;
}
// Grammatik aus ganzen Zahlen statt freier Wörter: jede erlaubte Zahl als Phrase in mehreren Schreibweisen
// („zweihundert einundzwanzig“, „zweihundert und einundzwanzig“, „zwohundert ein und zwanzig“ …).
// zahlen: Liste oder (von, bis). Wörter, die das Modell nicht kennt, ignoriert Vosk mit einer Warnung.
function zahlPhrasen(zahlen, bis) {
  if (!Array.isArray(zahlen)) { const v = zahlen; zahlen = []; for (let n = v; n <= bis; n++) zahlen.push(n); }
  const E = ['', 'ein', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun'];
  const T = ['', '', 'zwanzig', 'dreißig', 'vierzig', 'fünfzig', 'sechzig', 'siebzig', 'achtzig', 'neunzig'];
  const TEEN = ['zehn', 'elf', 'zwölf', 'dreizehn', 'vierzehn', 'fünfzehn', 'sechzehn', 'siebzehn', 'achtzehn', 'neunzehn'];
  const HUNDERT = { 1: ['hundert', 'einhundert'], 2: ['zweihundert', 'zwohundert'], 3: ['dreihundert'], 4: ['vierhundert'],
    5: ['fünfhundert'], 6: ['sechshundert'], 7: ['siebenhundert'], 8: ['achthundert'], 9: ['neunhundert'] };
  const rest = r => r === 0 ? [''] : r === 1 ? ['eins'] : r < 10 ? [E[r]] : r < 20 ? [TEEN[r - 10]]
    : r % 10 === 0 ? [T[r / 10]] : [`${E[r % 10]}und${T[Math.floor(r / 10)]}`, `${E[r % 10]} und ${T[Math.floor(r / 10)]}`];
  const aus = new Set();
  for (const n of zahlen) {
    const h = Math.floor(n / 100), r = n % 100;
    const hs = h ? HUNDERT[h] : [''];
    for (const hw of hs) for (const rw of rest(r)) {
      aus.add(`${hw} ${rw}`.trim());
      if (hw && rw) aus.add(`${hw} und ${rw}`);
    }
  }
  return [...aus, '[unk]'];
}
// Wörter, die die Erkennung überhaupt kennen darf (Grammatik): alles, woraus 0 … 999 gebaut wird
function zahlGrammatik() {
  const w = new Set([...Object.keys(EINER), ...Object.keys(ZEHNER), 'und', 'hundert']);
  for (const e of ['ein', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun']) {
    w.add(e + 'hundert');
    for (const z of ['zwanzig', 'dreißig', 'vierzig', 'fünfzig', 'sechzig', 'siebzig', 'achtzig', 'neunzig']) w.add(e + 'und' + z);
  }
  return [...w, '[unk]'];
}
