// Tests de la série de jours et des jours gelés (streakInfo), dans Bùbùgāo ET dans Zìzì.
// Le code est lu directement dans chaque index.html (entre SERIE:DEBUT et SERIE:FIN) : on teste ce qui tourne
// vraiment sur le téléphone, et on vérifie que les deux applis ont exactement la même règle.
// Usage :  node scripts/test_serie.js      (aussi lancé par TZ=Europe/Paris pour l'heure d'été)
const fs = require('fs'), path = require('path'), assert = require('assert');
const root = path.join(__dirname, '..');
const bloc = f => { const h = fs.readFileSync(path.join(root, f), 'utf8'), a = h.indexOf('/* SERIE:DEBUT'), b = h.indexOf('/* SERIE:FIN */');
  if (a < 0 || b < 0) throw new Error(f + ' : bloc SERIE introuvable'); return h.slice(a, b); };
const apps = { 'Bùbùgāo': bloc('index.html'), 'Zìzì': bloc('caracteres/index.html') };

const jour = (s, k) => { const d = new Date(Date.UTC(+s.slice(0, 4), +s.slice(5, 7) - 1, +s.slice(8, 10) + k)); return d.toISOString().slice(0, 10); };
const suite = (debut, n) => Array.from({ length: n }, (_, i) => jour(debut, i));      // n jours actifs de suite
const le = s => new Date(+s.slice(0, 4), +s.slice(5, 7) - 1, +s.slice(8, 10), 10, 0);  // « maintenant » fixé : ce jour-là, 10 h (heure locale)
const fois = (runs, n) => runs.filter(r => r >= n).length;

const tests = [
  ['série < 7 jours + 1 jour manqué → repart à 1, best garde l’ancienne valeur', f => {
    const r = f([...suite('2026-01-20', 5), '2026-01-26'], le('2026-01-26'));
    assert.strictEqual(r.current, 1); assert.strictEqual(r.best, 5); assert.deepStrictEqual(r.runs, [5, 1]); assert.strictEqual(r.freezesLeft, 0); }],
  ['7 jours, 1 jour manqué → la série continue, le jour manqué est gelé', f => {
    const r = f([...suite('2026-01-01', 7), '2026-01-09'], le('2026-01-09'));
    assert.strictEqual(r.current, 8); assert.deepStrictEqual(r.frozenDays, ['2026-01-08']); assert.strictEqual(r.freezesUsed, 1); assert.strictEqual(r.freezesLeft, 0); }],
  ['7 jours, 2 jours manqués → reset', f => {
    const r = f([...suite('2026-01-01', 7), '2026-01-10'], le('2026-01-10'));
    assert.strictEqual(r.current, 1); assert.strictEqual(r.best, 7); assert.deepStrictEqual(r.frozenDays, []); }],
  ['entre 7 et 29 jours, un 2e jour manqué → reset (le gel est déjà utilisé)', f => {
    const r = f([...suite('2026-01-01', 7), ...suite('2026-01-09', 4), '2026-01-14'], le('2026-01-14'));
    assert.strictEqual(r.current, 1); assert.strictEqual(r.best, 11); assert.strictEqual(r.freezesLeft, 0); }],
  ['après avoir utilisé le gel, 30 jours de série redonnent 1 gel qui couvre un nouveau jour manqué', f => {
    const actifs = [...suite('2026-01-01', 7), ...suite('2026-01-09', 23)];          // 30e jour actif le 31 janvier
    assert.strictEqual(f(actifs, le('2026-01-31')).freezesLeft, 1);
    const r = f([...actifs, '2026-02-02'], le('2026-02-02'));                          // 1er février manqué
    assert.strictEqual(r.current, 31); assert.deepStrictEqual(r.frozenDays, ['2026-01-08', '2026-02-01']); assert.strictEqual(r.freezesUsed, 2); assert.strictEqual(r.freezesLeft, 0); }],
  ['à 50 jours → 3 gels ; 3 jours manqués → la série continue ; 4 → reset', f => {
    const actifs = suite('2026-01-01', 50), d50 = actifs[49];
    assert.strictEqual(f(actifs, le(d50)).freezesLeft, 3);
    const ok = f([...actifs, jour(d50, 4)], le(jour(d50, 4)));
    assert.strictEqual(ok.current, 51); assert.strictEqual(ok.frozenDays.length, 3); assert.strictEqual(ok.freezesLeft, 0);
    const ko = f([...actifs, jour(d50, 5)], le(jour(d50, 5)));
    assert.strictEqual(ko.current, 1); assert.strictEqual(ko.best, 50); }],
  ['à 60 jours sans rien manquer → toujours 3 gels au maximum (plafond)', f => {
    const actifs = suite('2026-01-01', 60);
    const r = f(actifs, le(actifs[59])); assert.strictEqual(r.current, 60); assert.strictEqual(r.freezesLeft, 3); assert.strictEqual(r.freezesUsed, 0); }],
  ['hier manqué, aujourd’hui pas encore fait → série encore vivante si un gel le couvre', f => {
    const r = f(suite('2026-01-01', 7), le('2026-01-09'));
    assert.strictEqual(r.current, 7); assert.deepStrictEqual(r.frozenDays, ['2026-01-08']); assert.strictEqual(r.freezesLeft, 0); assert.strictEqual(r.freezesUsed, 1);
    assert.strictEqual(f(suite('2026-01-01', 5), le('2026-01-07')).current, 0); }],              // sans gel : cassée
  ['aujourd’hui pas encore fait ne casse jamais la série', f => {
    assert.strictEqual(f(suite('2026-01-01', 3), le('2026-01-04')).current, 3); }],
  ['deux séries séparées ayant chacune atteint 7 jours → badge 7 jours ×2', f => {
    const r = f([...suite('2026-01-01', 8), ...suite('2026-01-11', 7)], le('2026-01-17'));
    assert.deepStrictEqual(r.runs, [8, 7]); assert.strictEqual(fois(r.runs, 7), 2); assert.strictEqual(fois(r.runs, 14), 0); }],
  ['badge regagné : une série passée cassée + la série en cours comptent toutes les deux', f => {
    const r = f([...suite('2026-01-01', 3), ...suite('2026-01-06', 3)], le('2026-01-10'));   // série en cours cassée (2 jours manqués)
    assert.strictEqual(r.current, 0); assert.deepStrictEqual(r.runs, [3, 3]); assert.strictEqual(fois(r.runs, 3), 2); }],
  ['doublons, désordre, dates futures et texte invalide sont ignorés', f => {
    const r = f(['2026-01-03', '2026-01-01', '2026-01-02', '2026-01-02', '2026-02-10', 'n’importe quoi'], le('2026-01-03'));
    assert.strictEqual(r.current, 3); assert.deepStrictEqual(r.runs, [3]); }],
  ['passage à l’heure d’été (29 mars 2026) : les jours restent consécutifs', f => {
    const r = f(suite('2026-03-25', 10), le('2026-04-03')); assert.strictEqual(r.current, 10); assert.deepStrictEqual(r.frozenDays, []); }],
  ['aucun jour actif → tout à zéro', f => {
    assert.deepStrictEqual(f([], le('2026-01-01')), { current: 0, best: 0, freezesLeft: 0, freezesUsed: 0, frozenDays: [], runs: [] }); }],
];

let ko = 0;
assert.strictEqual(apps['Bùbùgāo'], apps['Zìzì'], 'Les deux applis doivent avoir exactement le même code de série');
console.log('OK    même code de série dans Bùbùgāo et Zìzì');
for (const [nom, code] of Object.entries(apps)) {
  const f = new Function(code + '\nreturn streakInfo;')();
  for (const [t, fn] of tests) { try { fn(f); console.log(`OK    ${nom} · ${t}`); } catch (e) { ko++; console.log(`ÉCHEC ${nom} · ${t}\n      ${e.message}`); } }
}
console.log(ko ? `\n${ko} test(s) en échec` : '\nTOUT EST BON'); process.exit(ko ? 1 : 0);
