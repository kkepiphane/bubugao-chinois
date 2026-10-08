"""Prépare la publication du prochain chapitre (utilisé par le robot du lundi).
Déplace le premier chapitre de a-publier/ vers packs/, l'ajoute à packs/packs.json,
vérifie son contenu et écrit un résumé pour la demande de validation."""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, 'a-publier')
PACKS = os.path.join(ROOT, 'packs')
HAN = re.compile(r'[㐀-鿿]')

def out(key, val):
    path = os.environ.get('GITHUB_OUTPUT')
    if path:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f'{key}={val}\n')
    print(f'{key}={val}')

order = json.load(open(os.path.join(QUEUE, 'ordre.json'), encoding='utf-8'))['chapitres']
index_path = os.path.join(PACKS, 'packs.json')
index = json.load(open(index_path, encoding='utf-8'))
published = {p['id'] for p in index['packs']}
nxt = next((c for c in order if c['id'] not in published and os.path.exists(os.path.join(QUEUE, c['file']))), None)
if not nxt:
    out('rien', 'oui'); sys.exit(0)

data = json.load(open(os.path.join(QUEUE, nxt['file']), encoding='utf-8'))
errors = []
for it in data.get('items', []):
    han = len(HAN.findall(it['h'])); syl = len(re.split(r'[ -]', it['p']))
    if not (han == syl == len(it['t']) and (('s' not in it) or len(it['s']) == syl)):
        errors.append(f"{it['id']} : {han} caractères, {syl} syllabes, {len(it['t'])} tons")
if errors:
    print('Chapitre invalide :', *errors, sep='\n- '); sys.exit(1)

shutil.move(os.path.join(QUEUE, nxt['file']), os.path.join(PACKS, nxt['file']))
index['packs'].append({'id': nxt['id'], 'v': 1, 'file': nxt['file'], 'title': nxt['title']})
json.dump(index, open(index_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

words = ' · '.join(f"{it['h']} ({it['fr']})" for it in data['items'])
g = data.get('grammar') or {}
convs = ', '.join(c['title'] for c in data.get('convs', []))
reste = sum(1 for c in order if c['id'] not in published) - 1
body = f"""## {nxt['title']}

{data.get('desc','')}

**{len(data['items'])} mots et phrases :** {words}

**Grammaire :** {g.get('title','—')}
**Conversation :** {convs or '—'}
**Caractères :** {' '.join(c['c'] for c in data.get('chars', []))}

---
✅ **Merge** = le chapitre arrive sur son téléphone dès qu'elle a du réseau.
✋ **Close** = on ne publie pas cette semaine (le robot le reproposera lundi prochain).

Chapitres encore en attente après celui-ci : {reste}.
"""
open(os.path.join(ROOT, '.pr-body.md'), 'w', encoding='utf-8').write(body)
out('rien', 'non'); out('id', nxt['id']); out('titre', nxt['title'])
