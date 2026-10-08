// Banc d'essai de l'analyseur de tons : passe les fichiers audio natifs (audio/*.mp3)
// dans l'analyseur de index.html et compte les syllabes bien reconnues.
// Usage : node scripts/banc_tons.js      (nécessite ffmpeg)
// Repère actuel : ≈ 79 % avec référence de voix, ≈ 73 % sans. Ne pas livrer une modification qui fait baisser ces chiffres.
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const js = html.slice(html.indexOf('<script>') + 8, html.lastIndexOf('</script>'));
const grab = n => { const i = js.indexOf('function ' + n + '('); let d = 0; for (let k = js.indexOf('{', i); k < js.length; k++) { if (js[k] === '{') d++; else if (js[k] === '}' && !--d) return js.slice(i, k + 1); } };
const cst = n => { const i = js.indexOf('const ' + n + '='); return js.slice(i, js.indexOf(';\n', i) + 1); };
const avg = a => a.reduce((x, y) => x + y, 0) / (a.length || 1);
eval([cst('TONE_MODEL'), ...['median', 'resample', 'yinAt', 'pitchTrack', 'segment', 'feats', 'toneProbs', 'analyzeTones'].map(grab)].join('\n'));
const index = JSON.parse(fs.readFileSync(path.join(root, 'audio/index.json'), 'utf8'));
let items = JSON.parse(fs.readFileSync(path.join(root, 'audio/base-contenu.json'), 'utf8')).items;
for (const dir of ['packs', 'a-publier']) for (const f of fs.readdirSync(path.join(root, dir)))
  if (f.endsWith('.json') && !['packs.json', 'ordre.json'].includes(f)) items = items.concat(JSON.parse(fs.readFileSync(path.join(root, dir, f), 'utf8')).items || []);
const load = file => { const raw = execFileSync('ffmpeg', ['-loglevel', 'error', '-i', file, '-f', 'f32le', '-ac', '1', '-ar', '22050', '-']); const d = new Float32Array(raw.buffer, raw.byteOffset, raw.length / 4); return { numberOfChannels: 1, length: d.length, sampleRate: 22050, getChannelData: () => d }; };
const L = items.filter(it => index[it.h]).map(it => ({ h: it.h, t: it.s || it.t, b: load(path.join(root, 'audio', index[it.h])) }));
const ref = median(L.filter(x => x.t.length >= 3).map(x => pitchTrack(x.b).med).filter(Boolean));
for (const [nom, R] of [['sans référence', 0], ['avec référence', ref]]) {
  let tot = 0, ok = 0; const err = {};
  for (const x of L) { const r = analyzeTones(x.b, x.t, R); if (!r.ok) { tot += x.t.filter(Boolean).length; continue; }
    r.segs.forEach(s => { if (!s.tone) return; tot++; if (s.got === s.tone) ok++; else err[s.tone + '→' + s.got] = (err[s.tone + '→' + s.got] || 0) + 1; }); }
  console.log(`${nom} : ${ok}/${tot} syllabes justes (${(100 * ok / tot).toFixed(1)} %) · erreurs fréquentes : ${Object.entries(err).sort((a, b) => b[1] - a[1]).slice(0, 4).map(([k, v]) => k + ' ×' + v).join(', ')}`);
}
