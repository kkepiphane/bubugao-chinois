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
| `sw.js` | Service worker : hors-ligne ; ouvre depuis la copie du téléphone (rapide même sur réseau faible) et télécharge la mise à jour en arrière-plan pour l'ouverture suivante ; demandes `cache: 'no-store'`/`'no-cache'` (chapitres, index audio) : réseau d'abord ; sons en cache permanent. |
| `manifest.webmanifest`, `icon-*.png` | Installation sur l'écran d'accueil. |
| `packs/` | Chapitres **publiés** + `packs.json` (liste lue par l'appli à chaque connexion). |
| `a-publier/` | Chapitres **en attente** + `ordre.json` (file du robot). |
| `audio/` | Un MP3 par texte chinois + `index.json` (`{"texte": "fichier.mp3"}`) + `base-contenu.json`. |
| `scripts/make_packs.py` | Source lisible de tous les chapitres HSK 1 et thématiques ; régénère les JSON. |
| `scripts/publier_chapitre.py` | Utilisé par le robot : passe le chapitre suivant de `a-publier/` à `packs/`. |
| `scripts/generer_audio.py` | Génère les MP3 manquants (voix open source sherpa-onnx `matcha-icefall-zh-baker`). |
| `scripts/exporter_base.js` | Exporte le contenu de base de `index.html` vers `audio/base-contenu.json`. |
| `scripts/banc_tons.js` | Mesure la justesse de l'analyseur de tons sur les MP3 natifs. |
| `scripts/test_appli.py` | Test de bout en bout dans Chromium (séances, audio, analyse, test HSK, hors-ligne). |
| `.github/workflows/chapitre-du-lundi.yml` | Lundi, mercredi, vendredi 7 h : ouvre une PR « 📚 À valider » avec le chapitre suivant (une seule à la fois). |
| `.github/workflows/audio.yml` | À chaque push touchant `packs/`, `a-publier/` ou `audio/base-contenu.json` : génère l'audio manquant. |
| `caracteres/` | **Zìzì 字字**, l'appli sœur pour lire et écrire les caractères (voir `caracteres/LISEZMOI.md`). |
| `.github/workflows/zizi.yml` | À chaque push touchant `caracteres/source/` : reconstruit les données de Zìzì et son audio. |
| `LISEZMOI.md` | Guide pas à pas pour Epiphane (non technique). |

## Zìzì (caracteres/)

Appli séparée sous la même adresse : `caracteres/index.html` + `data.json` (généré) + `traits.json` (ordre des traits,
Hanzi Writer) + `audio/`. Clé de stockage `zizi.v1` (règle absolue n° 1 valable aussi). Contenu source dans
`caracteres/source/`, outils dans `caracteres/outils/` (logo : `outils/icone.py`). Les deux service workers ne suppriment
**que leurs propres caches** (préfixes `bubugao-` et `zizi-`) : ne jamais casser cette règle. Après une modification de
`caracteres/index.html`, incrémenter `zizi-app-vN` dans `caracteres/sw.js`. Skill : `.claude/skills/nouveaux-caracteres/`.
Zìzì a aussi : séance en minutes (5/10/15), 8 niveaux (`source/rangs.txt`), défi et quêtes du jour, défi de la semaine, carnet de 53 sceaux (badges partageables, `SEALS` dans `caracteres/index.html`),
examen blanc HSK 1 lecture (`source/hsk1.txt`, `source/hsk_qr.txt`). Tout texte chinois prononcé doit être dans `data.json`
(le robot `zizi.yml` génère son MP3).

## Fonctionnement de l'appli (résumé)

- **Moteur de révision** : chaque mot a 4 compétences (`reco`, `oreille`, `ton`, `prod`) avec stabilité `S` (jours) ;
  rétention `R=(1+dt/(9S))^-1` (R=0,9 quand dt=S) ; priorité = oubli·0,5 + faiblesse du profil·0,3 + utilité·0,2.
  Réussite (note 1 difficile / 2 bien / 3 facile) : `S×=min(cap, a+b·max(0,1-R))` avec a,b,cap = 1,6,2.5 / 1.2,13,4 / 1.5,20,5,
  soit ×1,6 / ×2,5 / ×3,5 à R=0,9 et presque rien si on révise trop tôt. Échec : `S×0,4` (min 0,3).
  Caractères (`gradeChar`) : comme la note 2 (×2,5 à R=0,9, plafond ×4), comme dans Zìzì.
  Ne pas revenir à l'ancienne formule `1+(mult-1)·max(.25,1-R)` : elle ne multipliait l'intervalle que par ≈1,1–1,5,
  les révisions s'accumulaient et freinaient les nouveaux mots.
- **Séance du jour** : échauffement, nouveaux mots (60 % parcours HSK, 40 % branche choisie), règle de grammaire,
  duel de tons, prononciation, caractères, révisions, conversation, mission terrain. Difficulté visée 80–85 % de réussite.
  Frein des nouveaux mots (`nNewFor`) : retard > 30f compétences → 2f mots max, > 60f → f mots max.
  La place des mots retenus par le frein sert à réviser (`revCap` : +3 révisions par mot retenu, au plus 2 × 8f) :
  la séance garde sa durée. L'échauffement prend les mots à réviser les plus faciles (pas ceux déjà sus, qui ne gagnent rien).
- **Branches** : `hsk` (parcours principal), `travail` (usine, carrière : étapes Usine → Promotion → Entretien → Ailleurs), `quotidien`.
- **Voix** : `say(texte)` joue `audio/<fichier>.mp3` si le texte est dans `audio/index.json`, sinon la voix du téléphone (secours).
  **Tout texte chinois prononcé par l'appli doit donc avoir son MP3** (le workflow audio s'en charge).
- **Analyse des tons** : YIN → découpage par creux d'énergie → traits en demi-tons par rapport à la voix (`S.pitchRef`)
  → régression logistique `TONE_MODEL` (4 tons). Repère : ≈ 79 % de syllabes justes avec référence, ≈ 73 % sans.
- **Sauvegarde** : Progrès › Sauvegarde exporte/importe un fichier JSON.

## Commandes

```bash
python3 scripts/test_appli.py          # test complet (pip install playwright && playwright install chromium)
node scripts/banc_tons.js              # justesse de l'analyseur de tons
cd caracteres && python3 outils/test_zizi.py   # test complet de Zìzì (ffmpeg requis)
python3 scripts/generer_audio.py       # audio manquant (pip install sherpa-onnx soundfile ; ffmpeg)
node scripts/exporter_base.js          # après modification du contenu de base dans index.html
cd scripts && python3 make_packs.py    # régénère les chapitres depuis la source lisible
```

## Skills du projet

- `.claude/skills/nouveau-chapitre/` : écrire un chapitre (HSK ou thématique), le vérifier, l'audio, la file du robot.
- `.claude/skills/modifier-appli/` : changer `index.html` sans casser la progression ni le hors-ligne.
- `.claude/skills/voix-et-tons/` : audio, voix de secours, analyseur de tons et son banc d'essai.
- `.claude/skills/nouveaux-caracteres/` : ajouter ou corriger des caractères, histoires, phrases et lectures de Zìzì.

## Feuille de route (idées validées en discussion)

- Branche « Vie quotidienne » : restaurant, transport, santé, téléphone/WeChat, famille.
- Après le HSK 1 : parcours HSK 2 (300 mots, ancien format) au même rythme (jusqu'à 3 chapitres par semaine).
- ✅ Bouton « J'ai entendu une phrase » (onglet Parler) : elle enregistre et note des phrases réelles, puis les partage (WhatsApp…). Epiphane les transmet à Claude pour les intégrer aux chapitres (skill `nouveau-chapitre`).
