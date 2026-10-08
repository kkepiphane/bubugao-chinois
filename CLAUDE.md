# Bùbùgāo 步步高 — instructions pour Claude

Appli web installable (PWA, hors-ligne) pour apprendre le chinois mandarin.
Utilisatrice : une jeune femme togolaise francophone qui travaille dans une usine de chaussures tenue par des Chinois
et veut progresser (HSK, promotion, entretien, voyage). Elle utilise un téléphone Android, souvent sans réseau.
Mainteneur : Epiphane (développeur, Lomé). En ligne : https://kkepiphane.github.io/bubugao-chinois/

## Règles absolues

1. **Ne jamais changer l'adresse du site ni les clés de stockage** (`bubugao.v1`, `bubugao.packs.v1`, `bubugao.audio`) :
   sa progression vit dans le navigateur, liée à l'adresse. Un changement = elle perd tout (sauf restauration d'une sauvegarde).
2. **Ne jamais changer l'`id` d'un mot, d'un chapitre ou d'une conversation déjà publiés** : la progression y est rattachée.
3. **Tout le texte visible est en français simple**, tutoiement, ton encourageant, phrases courtes, sans jargon technique.
4. **Chinois exact** : caractères simplifiés, pinyin et tons vérifiés. Le nombre de caractères = nombre de syllabes = nombre de tons.
   Le sandhi va dans `s` (tons prononcés) : 3+3 → 2+3 (你好 `t:[3,3] s:[2,3]`), 不 devant un 4e ton → bú, 一 → yí/yì.
   Dans `t`, on écrit déjà 不/一 avec leur ton modifié quand c'est l'usage des manuels (不是 `[2,4]`, 一个 `[2,0]`).
5. Après toute modification de `index.html` : incrémenter `VERSION` dans `sw.js`, puis lancer les tests (ci-dessous).
6. Rien n'est publié sur son téléphone sans validation d'Epiphane (Pull Request).

## Carte du dépôt

| Chemin | Rôle |
|---|---|
| `index.html` | Toute l'appli (HTML + CSS + JS, sans dépendance). Contenu de base entre `BEGIN_DATA` et `END_DATA`. |
| `sw.js` | Service worker : hors-ligne, mises à jour (réseau d'abord), sons en cache permanent. |
| `manifest.webmanifest`, `icon-*.png` | Installation sur l'écran d'accueil. |
| `packs/` | Chapitres **publiés** + `packs.json` (liste lue par l'appli à chaque connexion). |
| `a-publier/` | Chapitres **en attente** + `ordre.json` (file du robot du lundi). |
| `audio/` | Un MP3 par texte chinois + `index.json` (`{"texte": "fichier.mp3"}`) + `base-contenu.json`. |
| `scripts/make_packs.py` | Source lisible de tous les chapitres HSK 1 et thématiques ; régénère les JSON. |
| `scripts/publier_chapitre.py` | Utilisé par le robot : passe le chapitre suivant de `a-publier/` à `packs/`. |
| `scripts/generer_audio.py` | Génère les MP3 manquants (voix open source sherpa-onnx `matcha-icefall-zh-baker`). |
| `scripts/exporter_base.js` | Exporte le contenu de base de `index.html` vers `audio/base-contenu.json`. |
| `scripts/banc_tons.js` | Mesure la justesse de l'analyseur de tons sur les MP3 natifs. |
| `scripts/test_appli.py` | Test de bout en bout dans Chromium (séances, audio, analyse, test HSK, hors-ligne). |
| `.github/workflows/chapitre-du-lundi.yml` | Chaque lundi 7 h : ouvre une PR « 📚 À valider » avec le chapitre suivant. |
| `.github/workflows/audio.yml` | À chaque push touchant `packs/`, `a-publier/` ou `audio/base-contenu.json` : génère l'audio manquant. |
| `LISEZMOI.md` | Guide pas à pas pour Epiphane (non technique). |

## Fonctionnement de l'appli (résumé)

- **Moteur de révision** : chaque mot a 4 compétences (`reco`, `oreille`, `ton`, `prod`) avec stabilité `S` (jours) ;
  rétention `R=(1+dt/(9S))^-1` ; priorité = oubli·0,5 + faiblesse du profil·0,3 + utilité·0,2.
- **Séance du jour** : échauffement, nouveaux mots (60 % parcours HSK, 40 % branche choisie), règle de grammaire,
  duel de tons, prononciation, caractères, révisions, conversation, mission terrain. Difficulté visée 80–85 % de réussite.
- **Branches** : `hsk` (parcours principal), `travail` (usine, carrière : étapes Usine → Promotion → Entretien → Ailleurs), `quotidien`.
- **Voix** : `say(texte)` joue `audio/<fichier>.mp3` si le texte est dans `audio/index.json`, sinon la voix du téléphone (secours).
  **Tout texte chinois prononcé par l'appli doit donc avoir son MP3** (le workflow audio s'en charge).
- **Analyse des tons** : YIN → découpage par creux d'énergie → traits en demi-tons par rapport à la voix (`S.pitchRef`)
  → régression logistique `TONE_MODEL` (4 tons). Repère : ≈ 79 % de syllabes justes avec référence, ≈ 73 % sans.
- **Sauvegarde** : Progrès › Sauvegarde exporte/importe un fichier JSON.

## Commandes

```bash
python3 scripts/test_appli.py          # test complet (pip install playwright && playwright install chromium)
node scripts/banc_tons.js              # justesse de l'analyseur de tons (ffmpeg requis)
python3 scripts/generer_audio.py       # audio manquant (pip install sherpa-onnx soundfile ; ffmpeg)
node scripts/exporter_base.js          # après modification du contenu de base dans index.html
cd scripts && python3 make_packs.py    # régénère les chapitres depuis la source lisible
```

## Skills du projet

- `.claude/skills/nouveau-chapitre/` : écrire un chapitre (HSK ou thématique), le vérifier, l'audio, la file du lundi.
- `.claude/skills/modifier-appli/` : changer `index.html` sans casser la progression ni le hors-ligne.
- `.claude/skills/voix-et-tons/` : audio, voix de secours, analyseur de tons et son banc d'essai.

## Feuille de route (idées validées en discussion)

- Branche « Vie quotidienne » : restaurant, transport, santé, téléphone/WeChat, famille.
- Après le HSK 1 : parcours HSK 2 (300 mots, ancien format) au même rythme d'un chapitre par semaine.
- Bouton « J'ai entendu une phrase » pour qu'elle envoie les phrases réelles de l'usine à intégrer dans les chapitres.
