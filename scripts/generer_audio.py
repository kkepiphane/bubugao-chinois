"""Génère les fichiers audio (MP3) de tout le contenu chinois de Bùbùgāo.

- Lit : audio/base-contenu.json (contenu intégré à index.html), packs/*.json et a-publier/*.json
- Écrit : audio/<clé>.mp3 et audio/index.json  ({"texte chinois": "fichier.mp3"})
- Ne régénère que ce qui manque : relancer le script est sans risque.

Voix : modèle open source « matcha-icefall-zh-baker » (sherpa-onnx), mandarin standard, voix féminine.
Le modèle (≈130 Mo) est téléchargé une seule fois depuis les releases GitHub de k2-fsa/sherpa-onnx.

Usage :  python3 scripts/generer_audio.py            (depuis la racine du dépôt)
Prérequis : pip install sherpa-onnx soundfile  +  ffmpeg
"""
import glob, hashlib, json, os, re, subprocess, sys, tarfile, tempfile, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(ROOT, 'audio')
MODELS = os.environ.get('BUBUGAO_TTS_DIR', os.path.join(tempfile.gettempdir(), 'bubugao-tts'))
REL = 'https://github.com/k2-fsa/sherpa-onnx/releases/download'
HAN = re.compile(r'[㐀-鿿]')
SPEED = 0.85  # un peu plus lent que la normale : c'est pour apprendre


def collect():
    """Tous les textes chinois que l'appli peut prononcer."""
    sources = [os.path.join(AUDIO, 'base-contenu.json')]
    sources += sorted(glob.glob(os.path.join(ROOT, 'packs', '*.json')))
    sources += sorted(glob.glob(os.path.join(ROOT, 'a-publier', '*.json')))
    texts = set()

    def add(t):
        if t and HAN.search(t) and '{name}' not in t:
            texts.add(t.strip())

    for path in sources:
        name = os.path.basename(path)
        if name in ('packs.json', 'ordre.json'):
            continue
        d = json.load(open(path, encoding='utf-8'))
        for it in d.get('items', []):
            add(it['h'])
            # morceaux utilisés par l'exercice « construis la phrase »
            han = HAN.findall(it['h']); k = 0
            for w in it['p'].split(' '):
                n = len(w.split('-')); add(''.join(han[k:k + n])); k += n
        for pair in d.get('pairs', []):
            for x in pair:
                add(x['h'])
        for c in d.get('convs', []):
            for node in c['nodes'].values():
                add(node['h'])
                for o in node.get('o', []):
                    if not o.get('fr_only'):
                        add(o['h'])
        g = d.get('grammar') or {}
        for e in g.get('examples', []):
            add(e['h'])
        for b in d.get('bonus', []):
            add(b['h'])
    return sorted(texts)


def key(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()[:12]


def ensure_models():
    d = os.path.join(MODELS, 'matcha-icefall-zh-baker')
    voc = os.path.join(MODELS, 'vocos-22khz-univ.onnx')
    os.makedirs(MODELS, exist_ok=True)
    if not os.path.exists(os.path.join(d, 'model-steps-3.onnx')):
        tgz = os.path.join(MODELS, 'matcha.tar.bz2')
        print('Téléchargement du modèle de voix…')
        urllib.request.urlretrieve(f'{REL}/tts-models/matcha-icefall-zh-baker.tar.bz2', tgz)
        with tarfile.open(tgz) as t:
            t.extractall(MODELS)
    if not os.path.exists(voc):
        urllib.request.urlretrieve(f'{REL}/vocoder-models/vocos-22khz-univ.onnx', voc)
    return d, voc


def main():
    os.makedirs(AUDIO, exist_ok=True)
    idx_path = os.path.join(AUDIO, 'index.json')
    index = json.load(open(idx_path, encoding='utf-8')) if os.path.exists(idx_path) else {}
    texts = collect()
    todo = [t for t in texts if t not in index or not os.path.exists(os.path.join(AUDIO, index[t]))]
    print(f'{len(texts)} textes, {len(todo)} à générer')
    if todo:
        import sherpa_onnx, soundfile as sf
        d, voc = ensure_models()
        cfg = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                matcha=sherpa_onnx.OfflineTtsMatchaModelConfig(
                    acoustic_model=f'{d}/model-steps-3.onnx', vocoder=voc,
                    lexicon=f'{d}/lexicon.txt', tokens=f'{d}/tokens.txt', dict_dir=f'{d}/dict'),
                num_threads=4),
            rule_fsts=f'{d}/phone.fst,{d}/date.fst,{d}/number.fst', max_num_sentences=1)
        tts = sherpa_onnx.OfflineTts(cfg)
        with tempfile.TemporaryDirectory() as tmp:
            for i, t in enumerate(todo, 1):
                a = tts.generate(t, sid=0, speed=SPEED)
                wav = os.path.join(tmp, 'x.wav'); sf.write(wav, a.samples, a.sample_rate)
                f = key(t) + '.mp3'
                # 0,15 s de silence au début : certains téléphones coupent le tout début du son
                subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav,
                                '-af', 'adelay=150,loudnorm=I=-16:TP=-1.5', '-ac', '1', '-ar', '22050',
                                '-b:a', '40k', os.path.join(AUDIO, f)], check=True)
                index[t] = f
                if i % 25 == 0:
                    print(f'  {i}/{len(todo)}', flush=True)
                    json.dump(index, open(idx_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    # on retire de l'index ce qui n'existe plus dans le contenu (les fichiers restent, sans danger)
    index = {t: index[t] for t in texts if t in index}
    json.dump(index, open(idx_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    print('audio/index.json :', len(index), 'entrées')


if __name__ == '__main__':
    sys.exit(main())
