/* Zìzì — hors-ligne et mises à jour (copie du téléphone d'abord, nouvelle version à l'ouverture suivante). Changer VERSION à chaque nouvelle version de index.html ou data.json.
   Ne supprime que ses propres caches (préfixe « zizi- ») : Bùbùgāo partage la même adresse. */
const VERSION = 'zizi-app-v9';
const KEEP = [VERSION, 'zizi-fonts', 'zizi-audio'];
const SHELL = ['./', 'index.html', 'data.json', 'traits.json', 'hanzi-writer.min.js', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'audio/index.json'];
self.addEventListener('install', e => { e.waitUntil(caches.open(VERSION).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('zizi-') && !KEEP.includes(k)).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request; if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.host === 'fonts.googleapis.com' || url.host === 'fonts.gstatic.com') {
    e.respondWith(caches.open('zizi-fonts').then(async c => { const hit = await c.match(req); if (hit) return hit;
      try { const r = await fetch(req); if (r.ok || r.type === 'opaque') c.put(req, r.clone()); return r; } catch (_) { return new Response('', { status: 504 }); } }));
    return;
  }
  if (url.origin !== location.origin) return;
  if (url.pathname.includes('/audio/') && url.pathname.endsWith('.mp3')) {
    e.respondWith(caches.open('zizi-audio').then(async c => { const hit = await c.match(req, { ignoreSearch: true }); if (hit) return hit;
      try { const r = await fetch(req); if (r.ok) c.put(req, r.clone()); return r; } catch (_) { return new Response('', { status: 504 }); } }));
    return;
  }
  // App et données : la copie du téléphone d'abord (ouverture en ~1 s même avec un réseau faible),
  // et la nouvelle version est téléchargée en arrière-plan pour la prochaine ouverture.
  // Demandes « fraîches » (cache: 'no-cache' / 'no-store', ex. index audio) : réseau d'abord, copie en secours.
  const fresh = req.cache === 'no-cache' || req.cache === 'no-store' || req.cache === 'reload';
  e.respondWith(caches.open(VERSION).then(async c => {
    // no-cache : on redemande au serveur si le fichier a changé (réponse minuscule s'il n'a pas changé)
    const net = fetch(req.url, { cache: 'no-cache', credentials: 'same-origin' }).then(r => { if (r.ok) c.put(req, r.clone()); return r; });
    const hit = await c.match(req, { ignoreSearch: true }) || (req.mode === 'navigate' ? await c.match('index.html') : undefined);
    if (fresh || !hit) return net.catch(() => hit || new Response('', { status: 504 }));
    e.waitUntil(net.catch(() => {}));
    return hit;
  }));
});
