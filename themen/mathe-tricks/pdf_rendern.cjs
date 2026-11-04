// HTML -> PDF mit dem vorinstallierten Chromium (Playwright). Aufruf: node pdf_rendern.cjs ein.html aus.pdf
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [ein, aus] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(ein));
  await p.waitForTimeout(500);
  await p.pdf({
    path: aus, format: 'A4', printBackground: true,
    margin: { top: '14mm', bottom: '16mm', left: '14mm', right: '14mm' },
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font:8px Inter,sans-serif;color:#888;width:100%;text-align:center">Rechentricks – Sammlung · Seite <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
  });
  await b.close();
})();
