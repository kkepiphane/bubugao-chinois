"""Génère les MP3 de Zìzì (caractères, mots, phrases exemples, lectures) à partir de data.json.
Usage (depuis le dossier de l'appli, ex. caracteres/) :  python3 outils/generer_audio_zizi.py
Ne génère que ce qui manque. Voix : sherpa-onnx matcha-icefall-zh-baker (comme Bùbùgāo).
"""
import hashlib, json, os, re, subprocess, sys, tarfile, tempfile, urllib.request

APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(APP, 'audio')
MODELS = os.environ.get('BUBUGAO_TTS_DIR', os.path.join(tempfile.gettempdir(), 'bubugao-tts'))
REL = 'https://github.com/k2-fsa/sherpa-onnx/releases/download'
HAN = re.compile(r'[㐀-鿿]')

def collect():
    d = json.load(open(os.path.join(APP, 'data.json'), encoding='utf-8'))
    t = set()
    for c in d['chars']:
        t.add(c['a'])
        for w in c['w']: t.add(w['h'])
        t.add(c['ex']['h'])
    for l in d['lectures']:
        for s in l['s']: t.add(s['h'])
    return sorted(x for x in t if HAN.search(x))

def key(text): return hashlib.sha1(text.encode('utf-8')).hexdigest()[:12]

def ensure_models():
    d = os.path.join(MODELS, 'matcha-icefall-zh-baker'); voc = os.path.join(MODELS, 'vocos-22khz-univ.onnx')
    os.makedirs(MODELS, exist_ok=True)
    if not os.path.exists(os.path.join(d, 'model-steps-3.onnx')):
        tgz = os.path.join(MODELS, 'matcha.tar.bz2')
        urllib.request.urlretrieve(f'{REL}/tts-models/matcha-icefall-zh-baker.tar.bz2', tgz)
        with tarfile.open(tgz) as tf: tf.extractall(MODELS)
    if not os.path.exists(voc):
        urllib.request.urlretrieve(f'{REL}/vocoder-models/vocos-22khz-univ.onnx', voc)
    return d, voc

def main():
    os.makedirs(AUDIO, exist_ok=True)
    ip = os.path.join(AUDIO, 'index.json')
    index = json.load(open(ip, encoding='utf-8')) if os.path.exists(ip) else {}
    texts = collect()
    todo = [x for x in texts if x not in index or not os.path.exists(os.path.join(AUDIO, index[x]))]
    print(f'{len(texts)} textes, {len(todo)} à générer', flush=True)
    if todo:
        import sherpa_onnx, soundfile as sf
        d, voc = ensure_models()
        tts = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(matcha=sherpa_onnx.OfflineTtsMatchaModelConfig(
                acoustic_model=f'{d}/model-steps-3.onnx', vocoder=voc, lexicon=f'{d}/lexicon.txt',
                tokens=f'{d}/tokens.txt', dict_dir=f'{d}/dict'), num_threads=4),
            rule_fsts=f'{d}/phone.fst,{d}/date.fst,{d}/number.fst', max_num_sentences=1))
        with tempfile.TemporaryDirectory() as tmp:
            for i, x in enumerate(todo, 1):
                # un caractère seul est dit un peu plus lentement
                a = tts.generate(x, sid=0, speed=0.75 if len(x) == 1 else 0.85)
                wav = os.path.join(tmp, 'x.wav'); sf.write(wav, a.samples, a.sample_rate)
                f = key(x) + '.mp3'
                subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav, '-af', 'adelay=150,loudnorm=I=-16:TP=-1.5',
                                '-ac', '1', '-ar', '22050', '-b:a', '40k', os.path.join(AUDIO, f)], check=True)
                index[x] = f
                if i % 25 == 0:
                    print(f'  {i}/{len(todo)}', flush=True)
                    json.dump(index, open(ip, 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    index = {x: index[x] for x in texts if x in index}
    json.dump(index, open(ip, 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    print('audio/index.json :', len(index), 'entrées')

if __name__ == '__main__':
    sys.exit(main())
