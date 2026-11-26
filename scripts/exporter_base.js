// Exporte le contenu intégré à index.html (ITEMS, PAIRS, CONVS, BONUS, PROVERBES, SOS) vers audio/base-contenu.json,
// pour que scripts/generer_audio.py puisse en produire l'audio.
// À relancer si on modifie le contenu de base dans index.html :  node scripts/exporter_base.js
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const js = html.slice(html.indexOf('<script>') + 8, html.indexOf('/* END_DATA */'));
const box = {};
// Textes à prononcer pendant la partie Écoute des examens blancs.
const examTexts = E => Object.values(E).flatMap(B => B.plan.filter(([part]) => part[0] === 'L').flatMap(([, type, key]) =>
  type === 'tfword' ? Object.keys(B.pics) : B[key].flatMap(x => [x.h, x.q, ...(x.l || []).map(y => y[0])]))).filter(Boolean).map(h => ({ h }));
new Function('box', js.replace(/const (STAGES|ITEMS|PAIRS|BONUS|CONVS|PROVERBES|SOS|EXAMENS)=/g, 'box.$1=') )(box);
fs.writeFileSync(path.join(root, 'audio', 'base-contenu.json'),
  JSON.stringify({ items: box.ITEMS, pairs: box.PAIRS, convs: box.CONVS, bonus: [...box.BONUS, ...(box.PROVERBES || []), ...(box.SOS || []), ...examTexts(box.EXAMENS || {})] }));
console.log('audio/base-contenu.json :', box.ITEMS.length, 'mots,', box.CONVS.length, 'conversations');
