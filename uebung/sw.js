// Die App ist am 06.11.2026 nach /mathe-videos/uebung/ umgezogen. Dieser Service Worker räumt den alten Pfad auf und
// meldet sich ab. Er fasst nur Einträge und Fenster unter dem alten Pfad an: Auf luperttrading-lab.github.io teilen
// sich alle Apps (neue Kopfrechnen-App, Würfel …) Cache-Speicher und Fenster-Liste.
const NEU = 'https://luperttrading-lab.github.io/mathe-videos/uebung/';
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    const alt = new URL('./', self.location).href;
    if (await caches.has('kopfrechnen')) {
      const c = await caches.open('kopfrechnen');
      for (const req of await c.keys()) if (req.url.startsWith(alt)) await c.delete(req);
    }
    const fenster = await self.clients.matchAll({ type: 'window' });
    await self.registration.unregister();
    for (const f of fenster) if (f.url.startsWith(alt)) f.navigate(NEU).catch(() => {});
  })());
});
