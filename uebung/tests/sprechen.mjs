// Sprechen mit Ersatz-Mikrofon: node tests/sprechen.mjs folge.wav
// folge.wav: 2 s Stille, dann die Ergebnisse von FOLGE gesprochen („zweihundertachtundachtzig“ …), je 3 s Pause,
// 16 kHz mono. Chromium spielt die Datei in Schleife als Mikrofon ab. Die Aufnahme liegt nicht im Repo.
// Braucht den Würfel-Klon (Sprachmodell), Pfad über WUERFEL=… (Standard /home/user/luperttrading-lab/wuerfel).
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

let pw;
try { pw = await import('playwright'); } catch { pw = await import('/opt/node22/lib/node_modules/playwright/index.mjs'); }
const wav = path.resolve(process.argv[2] || '');
if (!fs.existsSync(wav)) { console.log('Aufruf: node tests/sprechen.mjs folge.wav'); process.exit(2); }
const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const wuerfel = process.env.WUERFEL || '/home/user/luperttrading-lab/wuerfel';
const typen = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.png': 'image/png', '.gz': 'application/gzip' };
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

const FOLGE = '16x18,12x18,13x17,14x16,15x15,11x19,17x14,19x19,11x11,15x14';   // 17 · 14 = 238, gesagt wird 221: ein Fehler
const GESAGT = [288, 216, 221, 224, 225, 209, 221, 361, 121, 210];   // so steht es in folge.wav (15 · 14 = 210)
let fehler = 0;
const ok = (bed, text) => { console.log((bed ? '  ok   ' : '  FEHLER ') + text); if (!bed) fehler++; };
const browser = await pw.chromium.launch({ args: ['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream',
  `--use-file-for-fake-audio-capture=${wav}`, '--autoplay-policy=no-user-gesture-required'] });
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, permissions: ['microphone'] });
const page = await ctx.newPage();
const konsole = [];
page.on('pageerror', e => konsole.push(e.message));

console.log('Sprechen: Ergebnisse laut sagen (Ersatz-Mikrofon)');
await page.goto(basis);
await page.evaluate(() => localStorage.setItem('kopfrechnen.stand', JSON.stringify({ eingabe: 'sprechen', ton: false })));
await page.goto(basis + '?folge=' + FOLGE);
const t0 = Date.now();
// „Sprechen“ war zuletzt gewählt: die App lädt das Modell schon auf der Startseite (sonst liefe die Aufnahme beim Laden)
await page.waitForFunction(() => window.uebung.sprache.modell, null, { timeout: 180000 });
ok(true, `Sprachmodell auf der Startseite vorgeladen in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
ok((await page.textContent('#sprachstatus')).includes('Sprache bereit'), `Startseite: „${(await page.textContent('#sprachstatus')).trim()}“`);
await page.click('#los');
await page.waitForFunction(() => window.uebung.sprache.hoert, null, { timeout: 180000 });
ok(true, 'Mikrofon an, Ton kommt an');
await page.waitForTimeout(300);
ok((await page.getAttribute('#mikro', 'class')).includes('an') && (await page.textContent('#mikro')).includes('Mikrofon an'),
  `Anzeige im Spiel: „${(await page.textContent('#mikro')).trim()}“ (grün, mit Pegel)`);
await page.waitForFunction(() => window.uebung.runde.phase === 'ende', null, { timeout: 150000 }).catch(() => {});
const r = await page.evaluate(() => ({ p: window.uebung.sprache.protokoll, e: window.uebung.runde.ergebnisse, phase: window.uebung.runde.phase }));
const werte = r.p.map(x => x.wert).filter(x => x !== null);
console.log('  gehört: ' + r.p.map(x => `„${x.text}“→${x.wert}`).join('  '));
// Wie viele gesprochene Zahlen kamen richtig an? Die Aufnahme läuft in Schleife; gezählt wird die erste Runde.
// Die Erkennung kann mitten in der Schleife einsetzen: Versatz suchen, bei dem die meisten Zahlen passen
let treffer = 0;
for (let v = 0; v < GESAGT.length; v++) {
  const t = werte.filter((w, i) => w === GESAGT[(v + i) % GESAGT.length]).length;
  treffer = Math.max(treffer, t);
}
ok(werte.length >= 10 && treffer >= werte.length - 1, `${treffer} von ${werte.length} erkannten Zahlen stimmen mit dem Gesprochenen`);
ok(r.phase === 'ende' && r.e.length === 10 && r.e.filter(x => x.ok).length === 9,
  `Runde nur mit Sprechen zu Ende gespielt (${r.e.filter(x => x.ok).length} von 10 richtig, der eingebaute Fehler zählt)`);
const knopf = await page.$('.hoerfehler');
ok(!!knopf && (await knopf.textContent()).includes('238'), `Gesprochener Fehler: Knopf „${knopf ? (await knopf.textContent()).trim() : '–'}“`);
if (knopf) { await knopf.click(); ok((await page.textContent('#e-richtig')).trim() === '10 von 10 richtig', 'Nach „Hörfehler“: 10 von 10 richtig'); }
ok((await page.getAttribute('#mikro', 'class')).includes('aus'), 'Am Ende ist das Mikrofon aus');
const z = r.e.map(x => x.dauer / 1000);
if (z.length) ok(true, `Antwortzeit gesprochen: Ø ${(z.reduce((a, b) => a + b, 0) / z.length).toFixed(2)} s (inkl. 3 s Pause der Aufnahme)`);
ok(konsole.length === 0, 'Keine Fehler in der Konsole' + (konsole.length ? ': ' + konsole.join(' | ') : ''));
await browser.close(); server.close();
console.log(fehler ? `${fehler} Fehler` : 'Alles grün');
process.exit(fehler ? 1 : 0);
