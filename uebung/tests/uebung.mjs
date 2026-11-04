// Browser-Test der Übungs-App: node tests/uebung.mjs [bildordner]
// Bildet die Pages-Adresse nach: /5-Minuten-videos/… = dieses Repo, /wuerfel/… = Würfel-Repo (Sprachmodell),
// Pfad zum Würfel-Klon über WUERFEL=… (Standard /home/user/luperttrading-lab/wuerfel).
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

let pw;
try { pw = await import('playwright'); } catch { pw = await import('/opt/node22/lib/node_modules/playwright/index.mjs'); }
const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const wuerfel = process.env.WUERFEL || '/home/user/luperttrading-lab/wuerfel';
const bilder = process.argv[2];
const typen = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.png': 'image/png', '.gz': 'application/gzip',
  '.webmanifest': 'application/manifest+json' };
const server = http.createServer((req, res) => {
  const pfad = decodeURIComponent(new URL(req.url, 'http://x').pathname).replace(/\/$/, '/index.html');
  let p = null;
  if (pfad.startsWith('/5-Minuten-videos/')) p = path.join(repo, pfad.slice('/5-Minuten-videos/'.length));
  else if (pfad.startsWith('/wuerfel/')) p = path.join(wuerfel, pfad.slice('/wuerfel/'.length));
  if (!p || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': typen[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const basis = `http://127.0.0.1:${server.address().port}/5-Minuten-videos/uebung/`;

let fehler = 0;
const ok = (bed, text) => { console.log((bed ? '  ok   ' : '  FEHLER ') + text); if (!bed) fehler++; };
const browser = await pw.chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: bilder ? 2 : 1 });
const page = await ctx.newPage();
const konsole = [];
page.on('pageerror', e => konsole.push(e.message));
page.on('console', m => { if (m.type() === 'error') konsole.push(m.text()); });
const foto = async name => { if (bilder) { fs.mkdirSync(bilder, { recursive: true }); await page.screenshot({ path: path.join(bilder, name + '.png') }); } };

console.log('Zahlwörter (Sprechen)');
const faelle = { 'zweihundert achtundachtzig': 288, 'zweihundertachtundachtzig': 288, 'hundert einundzwanzig': 121,
  'einhundert einundzwanzig': 121, 'dreihundert einundsechzig': 361, 'zweihundert neun': 209, 'zweihundert zehn': 210,
  'dreihundert': 300, '[unk] zweihundert sechzehn': 216, 'zwei hundert vier und zwanzig': 224, 'hundert zwei und achtzig': 182,
  'fünfundzwanzig': 25, 'zwölf': 12, '[unk]': null, 'hallo': null, 'zweihundert fünfundzwanzig': 225 };
await page.goto(basis);
for (const [t, z] of Object.entries(faelle)) {
  const w = await page.evaluate(t => window.uebung.zahlwortZuZahl(t), t);
  ok(w === z, `„${t}“ → ${w}`);
}
const gram = await page.evaluate(() => JSON.parse(GRAMMATIK));
ok(gram.includes('zweihundert') && gram.includes('achtundachtzig') && gram.includes('[unk]'), `Grammatik mit ${gram.length} Wörtern`);

console.log('Runde mit Tippen');
await page.evaluate(() => localStorage.clear());
const folge = '16x18,12x18,13x17,14x16,15x15,11x19,17x13,19x19,11x11,15x14';
await page.goto(basis + '?folge=' + folge);
await foto('1_start');
await page.click('#los');
ok(await page.isVisible('#spiel'), 'Start zeigt die erste Aufgabe');
ok((await page.textContent('#frage')).replace(/\s/g, '') === '16·18', 'Erste Aufgabe 16 · 18');
const loes = folge.split(',').map(p => p.split('x').map(Number)).map(([x, y]) => x * y);
for (let i = 0; i < loes.length; i++) {
  const falsch = i === 2;
  const ziffern = String(falsch ? 999 : loes[i]);
  if (i === 0) await foto('2_aufgabe');
  for (const z of ziffern) { await page.dispatchEvent(`#tasten button[aria-label="${z}"]`, 'pointerdown'); await page.waitForTimeout(120); }
  if (i === 0) { await page.waitForTimeout(100); await foto('3_richtig'); }
  if (falsch) {
    await page.waitForSelector('#weg:not([hidden])', { timeout: 3000 });
    const weg = await page.textContent('#weg');
    ok(weg.includes('13 + 7 = 20') && weg.includes('200') && weg.includes('21') && weg.includes('221'),
      'Nach dem Fehler: Lösungsweg 13 + 7 = 20 → 200 → + 3 · 7 = 21 → 221');
    await foto('4_loesungsweg');
    await page.click('#weiter');
  } else {
    await page.waitForFunction(n => window.uebung.runde.i === n && (window.uebung.runde.phase === 'frage' || window.uebung.runde.phase === 'ende'),
      i + 1, { timeout: 3000 });
  }
}
await page.waitForSelector('#ende:not([hidden])', { timeout: 4000 });
ok((await page.textContent('#e-richtig')).trim() === '9 von 10 richtig', 'Ende: 9 von 10 richtig');
const e = await page.evaluate(() => window.uebung.runde.ergebnisse);
const schnitt = e.reduce((s, x) => s + x.dauer, 0) / e.length / 1000;
ok(/Ø \d+,\d s je Aufgabe/.test(await page.textContent('#e-zeit')), `Durchschnittszeit angezeigt (${(await page.textContent('#e-zeit')).trim()}, gemessen ${schnitt.toFixed(2)} s)`);
ok(e.length === 10 && e.every(x => x.dauer > 0 && x.dauer < 5000), 'Jede Aufgabe hat eine Zeit');
ok((await page.$$('#liste li')).length === 10, 'Liste mit allen 10 Aufgaben');
ok((await page.textContent('#e-spruch')).length > 10, `Motivation: „${(await page.textContent('#e-spruch')).trim()}“`);
await foto('5_ende');
await page.click('#uebersicht');
ok(await page.isVisible('#verlauf'), 'Übersicht zeigt die letzte Runde');
ok((await page.textContent('#bester')).includes('Bester Schnitt'), `Verlauf: ${(await page.textContent('#bester')).trim()}`);
await foto('6_verlauf');

console.log('Aufgaben-Erzeugung');
const z = await page.evaluate(() => {
  const u = UEBUNGEN[0], r = [];
  for (let k = 0; k < 200; k++) r.push(u.erzeuge('alle', 10).map(a => a.frage));
  const zehn = u.erzeuge('zehn', 10);
  return { r, zehn: zehn.map(a => [a.x, a.y]) };
});
ok(z.r.every(l => l.length === 10 && new Set(l.map(f => f.split(' · ').sort().join())).size === 10), '„Alle Zahlen“: 10 verschiedene Paare je Runde (200 Runden)');
ok(z.zehn.every(([x, y]) => (x - 10) + (y - 10) === 10), '„Einer ergeben 10“: nur 11·19, 12·18, 13·17, 14·16, 15·15');
ok(z.r.flat().every(f => { const [x, y] = f.split(' · ').map(Number); return x >= 11 && x <= 19 && y >= 11 && y <= 19; }), 'Alle Faktoren zwischen 11 und 19');

ok(konsole.length === 0, 'Keine Fehler in der Konsole' + (konsole.length ? ': ' + konsole.join(' | ') : ''));
await browser.close(); server.close();
console.log(fehler ? `${fehler} Fehler` : 'Alles grün');
process.exit(fehler ? 1 : 0);
