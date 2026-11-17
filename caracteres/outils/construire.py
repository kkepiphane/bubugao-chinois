"""Construit data.json et traits.json de Zìzì à partir de source/.

Sources (à modifier) :
  source/fiches*.txt   une ligne par caractère :
     caractère | pinyin | sens | clé | sens de la clé | composition | histoire | mots (h:fr;h:fr) | phrase (h:fr)
  source/ordre.json    ordre d'apprentissage (liste de caractères)
  source/lectures.txt  titre | phrase:traduction||phrase:traduction…

Le pinyin des mots et des phrases est calculé (outils/pinyin_fr.py) ; corrections au cas par cas dans
outils/pinyin_corrections.json ({"phrase exacte": "Pinyin."}). Les traits d'un nouveau caractère sont
téléchargés depuis le paquet npm hanzi-writer-data (via cdn.jsdelivr.net).

Usage, depuis caracteres/ :  python3 outils/construire.py
"""
import json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'outils'))
from pinyin_fr import sentence_py  # noqa: E402

HAN = re.compile(r'[㐀-鿿]')
TONES = ['āēīōūǖ', 'áéíóúǘ', 'ǎěǐǒǔǚ', 'àèìòùǜ']
# texte prononcé pour « écouter le caractère » quand la lecture seule serait ambiguë
AUDIO_TEXT = {'觉': '睡觉', '了': '好了', '的': '我的', '么': '什么', '吗': '好吗', '呢': '你呢',
              '吧': '好吧', '们': '我们', '子': '儿子', '个': '一个'}
try:
    OVR = json.load(open(os.path.join(ROOT, 'outils', 'pinyin_corrections.json'), encoding='utf-8'))
except FileNotFoundError:
    OVR = {}


def py(text):
    return OVR.get(text) or sentence_py(text)


def tone(p):
    for ch in p:
        for t, g in enumerate(TONES, 1):
            if ch in g:
                return t
    return 0


def main():
    order = json.load(open(os.path.join(ROOT, 'source', 'ordre.json'), encoding='utf-8'))
    F, errors = {}, []
    for name in sorted(os.listdir(os.path.join(ROOT, 'source'))):
        if not (name.startswith('fiches') and name.endswith('.txt')):
            continue
        for n, line in enumerate(open(os.path.join(ROOT, 'source', name), encoding='utf-8'), 1):
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            f = line.split('|')
            if len(f) != 9:
                errors.append(f'{name}:{n} : 9 champs attendus, {len(f)} trouvés'); continue
            c = f[0]
            words = [m.split(':', 1) for m in f[7].split(';')]
            ex = f[8].split(':', 1)
            for w in words:
                if c not in w[0]: errors.append(f'{c} : le mot {w[0]} ne contient pas le caractère')
            if c not in ex[0]: errors.append(f'{c} : la phrase exemple ne contient pas le caractère')
            F[c] = dict(c=c, p=f[1], m=f[2], k=f[3], km=f[4], comp=f[5], st=f[6],
                        w=[{'h': a, 'p': py(a), 'fr': b} for a, b in words],
                        ex={'h': ex[0], 'p': py(ex[0]), 'fr': ex[1]})
    missing = [c for c in order if c not in F]
    if missing: errors.append('caractères dans ordre.json sans fiche : ' + ''.join(missing))
    extra = [c for c in F if c not in order]
    if extra: errors.append('fiches absentes de ordre.json : ' + ''.join(extra))
    if errors:
        print('\n'.join('ERREUR ' + e for e in errors)); sys.exit(1)

    tp = os.path.join(ROOT, 'traits.json')
    traits = json.load(open(tp, encoding='utf-8')) if os.path.exists(tp) else {}
    for c in order:
        if c not in traits:
            url = 'https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0.1/' + urllib.request.quote(c) + '.json'
            print('traits téléchargés pour', c)
            traits[c] = json.load(urllib.request.urlopen(url))
    traits = {c: traits[c] for c in order}

    chars = []
    for i, c in enumerate(order, 1):
        d = F[c]
        d.update(n=i, t=tone(d['p']), a=AUDIO_TEXT.get(c, c), n_strokes=len(traits[c]['strokes']))
        chars.append(d)
    cles = {}
    for d in chars:
        k = cles.setdefault(d['k'], {'k': d['k'], 'm': d['km'], 'c': []}); k['c'].append(d['c'])
    cles = sorted(cles.values(), key=lambda x: -len(x['c']))
    S = set(order); lect = []
    for line in open(os.path.join(ROOT, 'source', 'lectures.txt'), encoding='utf-8'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        title, body = line.split('|', 1)
        sents = [s.split(':', 1) for s in body.split('||')]
        need = sorted({ch for h, _ in sents for ch in h if HAN.match(ch) and ch in S}, key=order.index)
        lect.append({'t': title, 'need': ''.join(need), 'rank': max(order.index(ch) for ch in need) + 1,
                     's': [{'h': h, 'p': py(h), 'fr': fr} for h, fr in sents]})
    lect.sort(key=lambda x: x['rank'])
    json.dump({'v': 1, 'chars': chars, 'cles': cles, 'lectures': lect},
              open(os.path.join(ROOT, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    json.dump(traits, open(tp, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(f'{len(chars)} caractères · {len(cles)} clés · {len(lect)} lectures')
    if '--relire' in sys.argv:
        for d in chars:
            print(d['c'], '|', ' ; '.join(w['h'] + ' ' + w['p'] for w in d['w']), '|', d['ex']['h'], d['ex']['p'])


if __name__ == '__main__':
    main()
