// Hörtest der Spracherkennung ohne Mikrofon: node tests/hoertest.mjs <ordner mit liste.json und wav-Dateien>
// liste.json (oder 2. Argument): [{stimme, zahl, art: produkt|kein_produkt|schlampig, datei}] (16 kHz mono PCM).
// Vergleicht Grammatiken: A freie Zahlwörter (aufgaben.js), B jede Zahl 100–399 als Phrase, C nur die Ergebnisse der Übung.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

let pw;
try { pw = await import('playwright'); } catch { pw = await import('/opt/node22/lib/node_modules/playwright/index.mjs'); }
const ordner = path.resolve(process.argv[2] || '');
const listenname = process.argv[3] || 'liste.json';                // optional andere Liste im selben Ordner
const liste = JSON.parse(fs.readFileSync(path.join(ordner, listenname), 'utf8'));
const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const wuerfel = process.env.WUERFEL || '/home/user/luperttrading-lab/wuerfel';
const seite = `<!doctype html><meta charset="utf-8"><script src="aufgaben.js"></script><script src="../../wuerfel/sprache/vosk.js"></script>`;
const server = http.createServer((req, res) => {
  const pfad = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (pfad === '/5-Minuten-videos/uebung/hoertest.html') { res.writeHead(200, { 'content-type': 'text/html' }); return res.end(seite); }
  let p = null;
  if (pfad.startsWith('/5-Minuten-videos/')) p = path.join(repo, pfad.slice('/5-Minuten-videos/'.length));
  else if (pfad.startsWith('/wuerfel/')) p = path.join(wuerfel, pfad.slice('/wuerfel/'.length));
  else if (pfad.startsWith('/aufnahmen/')) p = path.join(ordner, pfad.slice('/aufnahmen/'.length));
  if (!p || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': p.endsWith('.js') ? 'text/javascript' : 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const basis = `http://127.0.0.1:${server.address().port}`;
const browser = await pw.chromium.launch();
const page = await browser.newPage();
page.on('pageerror', e => console.log('Seitenfehler:', e.message));
await page.goto(basis + '/5-Minuten-videos/uebung/hoertest.html');
const ergebnis = await page.evaluate(async ({ liste, basis }) => {
  const model = await Vosk.createModel(basis + '/wuerfel/sprache/vosk-model-small-de-0.15.tar.gz');
  const P = [...new Set(UEBUNGEN[0].erzeuge('alle', 0).length ? [] : [])];
  const produkte = []; for (let x = 11; x <= 19; x++) for (let y = x; y <= 19; y++) produkte.push(x * y);
  const PHRASEN = typeof zahlPhrasen === 'function' ? zahlPhrasen : null;
  const grammatiken = { A: zahlGrammatik(), B: PHRASEN ? PHRASEN(100, 399) : null, C: PHRASEN ? PHRASEN([...new Set(produkte)]) : null };
  const lade = async datei => {
    const buf = await (await fetch(basis + '/aufnahmen/' + datei)).arrayBuffer();
    const dv = new DataView(buf); let o = 12, start = 0, len = 0;
    while (o < dv.byteLength) { const id = String.fromCharCode(...new Uint8Array(buf, o, 4)), n = dv.getUint32(o + 4, true);
      if (id === 'data') { start = o + 8; len = n; break; } o += 8 + n; }
    const i16 = new Int16Array(buf, start, len / 2), f = new Float32Array(i16.length);
    for (let k = 0; k < i16.length; k++) f[k] = i16[k] / 32768;
    const ab = new AudioBuffer({ length: f.length, sampleRate: 16000, numberOfChannels: 1 }); ab.copyToChannel(f, 0);
    return ab;
  };
  const aus = {};
  for (const [name, g] of Object.entries(grammatiken)) {
    if (!g) continue;
    aus[name] = [];
    for (const e of liste) {
      const rec = new model.KaldiRecognizer(16000, JSON.stringify(g));
      const texte = [];
      let letzt = performance.now();
      rec.on('result', m => { texte.push(m.result.text); letzt = performance.now(); });
      rec.acceptWaveform(await lade(e.datei));
      rec.retrieveFinalResult();
      const t0 = performance.now();
      await new Promise(r => { const iv = setInterval(() => { if (performance.now() - t0 > 300 && performance.now() - letzt > 350 && texte.length) { clearInterval(iv); r(); } if (performance.now() - t0 > 3000) { clearInterval(iv); r(); } }, 50); });
      rec.remove();
      const text = texte.join(' ').trim();
      aus[name].push({ ...e, text, wert: zahlwortZuZahl(text) });
    }
  }
  return aus;
}, { liste, basis });
for (const [name, r] of Object.entries(ergebnis)) {
  console.log(`\nGrammatik ${name}`);
  for (const art of ['produkt', 'schlampig', 'kein_produkt']) {
    const t = r.filter(x => x.art === art);
    if (!t.length) continue;
    const ok = t.filter(x => x.wert === x.zahl);
    console.log(`  ${art.padEnd(13)} ${ok.length}/${t.length} richtig` + (ok.length < t.length ? '   falsch: ' +
      t.filter(x => x.wert !== x.zahl).map(x => `${x.stimme[0]}:${x.zahl}${x.variante && x.variante !== 'std' ? '(' + x.variante + ')' : ''}→${x.wert ?? '–'}`).join(' ') : ''));
  }
}
fs.writeFileSync(path.join(ordner, listenname.replace('liste', 'ergebnis')), JSON.stringify(ergebnis, null, 1));
await browser.close(); server.close();
