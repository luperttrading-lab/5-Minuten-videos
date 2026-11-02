// HTML -> PDF mit Playwright (Chromium ist vorinstalliert). Aufruf: node pdf_bau.js eingabe.html ausgabe.pdf
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, pdf] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await p.pdf({ path: pdf, format: 'A4', printBackground: true,
    margin: { top: '18mm', bottom: '18mm', left: '18mm', right: '18mm' },
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font-size:8px;color:#888;padding:0 18mm;display:flex;justify-content:space-between;font-family:sans-serif"><span>Videoreihe Gesundheits-Faktencheck · Strategiepapier · 02.11.2026</span><span class="pageNumber"></span></div>' });
  await b.close(); console.log('ok', pdf);
})();
