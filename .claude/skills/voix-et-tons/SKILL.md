---
name: voix-et-tons
description: Tout ce qui touche au son dans Bùbùgāo — fichiers audio pré-générés, voix de secours du téléphone, problèmes de voix signalés, analyse et score des tons (YIN + modèle), banc d'essai. À utiliser quand la voix « ne marche pas », sonne mal, ou quand les scores de prononciation semblent faux.
---

# Voix et tons

## Comment l'appli parle

1. `say(texte)` cherche `texte` dans `AUDIO` (= `audio/index.json`). S'il existe : lecture du MP3 (`new Audio`),
   vitesse 0,7 pour « Lent ». Le service worker garde chaque MP3 en cache permanent ; `prefetchAudio()` télécharge
   tous les sons quand il y a du réseau (sauf mode économie de données).
2. Sinon (texte avec `{name}`, contenu sans audio) : `ttsSay()` = voix du téléphone (`speechSynthesis`, `zh-CN`),
   avec les contournements Chrome Android (attendre 150 ms après `cancel()`, garder une référence à l'énoncé).

**Si la voix ne marche pas**, vérifier dans cet ordre :
- le texte prononcé est-il exactement une clé de `audio/index.json` ? (ponctuation chinoise comprise : `，` `。` `？` `！`)
  Sinon lancer `python3 scripts/generer_audio.py` (et `node scripts/exporter_base.js` si c'est du contenu de base) ;
- le workflow **Audio des chapitres** a-t-il tourné et commité après le dernier ajout de chapitre ?
- `sw.js` : la règle `/audio/*.mp3` (cache d'abord) est-elle intacte ? `VERSION` a-t-elle été incrémentée ?
- sur le téléphone : son du média activé, appli ouverte au moins une fois avec réseau après la mise à jour.

## Générer l'audio

`scripts/generer_audio.py` collecte tous les textes chinois (mots, morceaux de phrases pour l'exercice « construis la
phrase », conversations, exemples de grammaire, duels, bonus) dans `audio/base-contenu.json`, `packs/` et `a-publier/`,
et ne génère que les manquants. Voix : `matcha-icefall-zh-baker` (sherpa-onnx, open source, mandarin standard féminin ;
jeu de données Baker, usage non commercial). Nom de fichier = 12 premiers caractères du SHA-1 du texte.
Vitesse de synthèse 0,85, 150 ms de silence au début, volume normalisé, MP3 mono 40 kb/s.

## Analyse des tons

Chaîne : `pitchTrack` (YIN, 10 ms, filtre des sauts > 4 demi-tons) → `segment` (coupe aux creux d'énergie) →
`feats` (début, fin, min, max, montée, chute, creux, niveau moyen, en demi-tons par rapport à la voix) →
`toneProbs` (régression logistique `TONE_MODEL`, deux variantes : `ref` quand la hauteur moyenne de sa voix
`S.pitchRef` est connue ou que la phrase a ≥ 3 syllabes, `noref` sinon) → score par syllabe
(juste : 70 + 30 × probabilité ; faux : 70 × p(attendu)/p(max)). Les conseils ne s'affichent que si le modèle est sûr.
`S.pitchRef` est appris sur ses phrases de 3 syllabes ou plus (le test de départ en fait enregistrer une de 5).

**Banc d'essai obligatoire** après toute modification : `node scripts/banc_tons.js`.
Repère : ≈ 78,7 % de syllabes justes avec référence, ≈ 72,7 % sans, sur 545 syllabes natives.
Une modification qui fait baisser ces chiffres ne doit pas être livrée.

Pour ré-entraîner `TONE_MODEL` : extraire les traits de chaque syllabe des MP3 natifs (tons attendus = `s` sinon `t`),
entraîner une régression logistique (scikit-learn, normalisation standard, C=1), valider par `GroupKFold` sur les mots,
puis replier la normalisation dans les poids (`W/écart-type`, biais corrigé) avant de remplacer la constante.
Idéalement, ajouter aussi de vrais enregistrements (collègues chinois, avec leur accord) pour sortir de la seule voix de synthèse.
