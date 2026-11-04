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
ok(await page.isVisible('#bereit'), 'Nach „Start“: Bereit-Karte, Mikrofon schaltet ein');
await page.waitForFunction(() => window.uebung.sprache.hoert && !document.querySelector('#bereit-los').disabled, null, { timeout: 30000 });
ok(true, `Mikrofon an, Ton kommt an – „Los“ freigegeben: „${(await page.textContent('#bereit-text')).trim()}“`);
// Lautstärke je 10 ms mitschreiben (nur im Test): unabhängiger Vergleich für Anfang und Ende jeder gesprochenen Zahl
await page.evaluate(() => {
  const s = window.uebung.sprache, alt = s.knoten.onaudioprocess; s.energie = [];
  s.knoten.onaudioprocess = ev => {
    alt(ev);
    const d = ev.inputBuffer.getChannelData(0), sr = ev.inputBuffer.sampleRate, n = Math.round(sr / 100), basis = s.proben - d.length;
    for (let k = 0; k + n <= d.length; k += n) { let q = 0; for (let j = k; j < k + n; j++) q += d[j] * d[j]; s.energie.push([(basis + k) / sr, Math.sqrt(q / n)]); }
  };
});
await page.click('#bereit-los');                     // die Aufnahme beginnt mit 2 s Stille: die erste Zahl kommt nach „Los“
await page.waitForTimeout(300);
ok((await page.getAttribute('#mikro', 'class')).includes('an') && (await page.textContent('#mikro')).includes('Mikrofon an'),
  `Anzeige im Spiel: „${(await page.textContent('#mikro')).trim()}“ (grün, mit Pegel)`);
await page.waitForFunction(() => window.uebung.runde.phase === 'ende', null, { timeout: 150000 }).catch(() => {});
const r = await page.evaluate(() => ({ p: window.uebung.sprache.protokoll, e: window.uebung.runde.ergebnisse.map(x => ({ ...x, a: undefined })),
  phase: window.uebung.runde.phase, energie: window.uebung.sprache.energie, zeit: document.querySelector('#e-zeit').textContent }));
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
if (process.env.FOTO) await page.screenshot({ path: path.join(process.env.FOTO, 'sprechen_ende.png') });   // FOTO=ordner: Bild vom Ergebnis
// Wohin gehen die Sekunden? Je gesprochene Zahl: Sprechdauer (erstes bis letztes Wort) und Wartezeit der Erkennung
// (Ende des letzten Wortes bis zur Meldung). Gegenprobe: Anfang und Ende laut Lautstärke statt laut Vosk.
const mittel = l => l.reduce((a, b) => a + b, 0) / l.length, f2 = v => (v / 1000).toFixed(2);
const mit = r.p.filter(x => x.woerter?.length && x.schluss);
const max = Math.max(...r.energie.map(x => x[1])), laut = r.energie.filter(x => x[1] > max * 0.01);   // −40 dB: leise Endungen („-zig“) zählen mit
const segmente = [];                                 // zusammenhängend laut, Lücken unter 0,3 s überbrückt
for (const [t] of laut) { const g = segmente.at(-1); if (g && t - g[1] < 0.3) g[1] = t + 0.01; else segmente.push([t, t + 0.01]); }
const zeilen = mit.map(x => {
  const a = x.woerter[0][1], b = x.woerter.at(-1)[2];
  const g = segmente.find(s => s[1] > a - 0.3 && s[0] < b + 0.3);
  return { text: x.text, sprechen: x.schluss - x.beginn, hundert: x.zweiter !== null ? x.zweiter - x.beginn : null, warten: x.erkannt - x.schluss,
    dA: g ? (a - g[0]) * 1000 : null, dE: g ? (b - g[1]) * 1000 : null };
});
for (const z of zeilen) console.log(`    „${z.text}“: gesprochen ${f2(z.sprechen)} s (davon „…hundert“ ${z.hundert !== null ? f2(z.hundert) : '–'} s) · Erkennung danach ${f2(z.warten)} s`
  + (z.dE !== null ? ` · Vosk gegen Lautstärke: Anfang ${z.dA >= 0 ? '+' : ''}${Math.round(z.dA)} ms, Ende ${z.dE >= 0 ? '+' : ''}${Math.round(z.dE)} ms` : ''));
const w = zeilen.map(z => z.warten);
ok(zeilen.length >= 10 && zeilen.every(z => z.sprechen > 300 && z.sprechen < 2500),
  `Wort-Zeitmarken für jede Zahl: Sprechdauer Ø ${f2(mittel(zeilen.map(z => z.sprechen)))} s`);
ok(w.every(v => v > 0 && v < 2500), `Wartezeit der Erkennung nach dem letzten Wort: Ø ${f2(mittel(w))} s (${f2(Math.min(...w))} … ${f2(Math.max(...w))} s)`);
const dE = zeilen.filter(z => z.dE !== null).map(z => Math.abs(z.dE));
ok(dE.length >= 8 && mittel(dE) < 150, `Vosk-Wortende passt zur Lautstärke: Abweichung Ø ${Math.round(mittel(dE))} ms`);
const ab = r.e.filter(x => x.schluss != null);
ok(ab.length >= 9 && ab.every(x => x.dauer <= x.zweiter && x.zweiter < x.schluss && x.schluss < x.roh),
  `Gezählt wird bis zum ersten Wort: Ø ${f2(mittel(ab.map(x => x.dauer)))} s · bis nach „…hundert“ Ø ${f2(mittel(ab.map(x => x.zweiter)))} s`
  + ` · bis Ende Ø ${f2(mittel(ab.map(x => x.schluss)))} s · bis zur Erkennung Ø ${f2(mittel(ab.map(x => x.roh)))} s`);
ok(/^Ø \d+,\d s je Aufgabe · schnellste \d+,\d s$/.test(r.zeit.trim()), `Ergebnis nur mit der Hauptzahl: „${r.zeit.trim()}“`);
ok(konsole.length === 0, 'Keine Fehler in der Konsole' + (konsole.length ? ': ' + konsole.join(' | ') : ''));
await browser.close(); server.close();
console.log(fehler ? `${fehler} Fehler` : 'Alles grün');
process.exit(fehler ? 1 : 0);
