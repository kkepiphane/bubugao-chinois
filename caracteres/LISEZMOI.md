# Zìzì 字字 — apprendre les caractères

« 字字珠玑 » : chaque caractère est une perle. Appli sœur de Bùbùgāo, dans le même dépôt :
**https://kkepiphane.github.io/bubugao-chinois/caracteres/** (installable, hors-ligne).

## Ce qu'elle apprend

- **214 caractères** : les 174 du HSK 1 + 32 de l'usine (鞋 底 胶 线 质 量 检 查…) + 8 très fréquents (要 给 也 还…).
- **Ordre « briques d'abord »** : les mots utiles en premier (你好, 谢谢, 我是…), et chaque caractère arrive juste après
  ses composants (女 et 子 avant 好, 人 avant 认).
- **Fiche de chaque caractère** : ordre des traits animé (la clé en rouge), pinyin coloré par ton et voix, sens en
  français, **clé** et composition, **petite histoire pour s'en souvenir**, 2–3 mots, une phrase exemple traduite.

## La séance du jour : on choisit le temps, Zìzì choisit le contenu

- **5, 10 ou 15 minutes** (sur l'accueil). Environ 2, 4 ou 6 nouveaux caractères : un de moins si la réussite récente
  est sous 75 %, moitié moins s'il y a plus de 25 révisions en retard, un de plus si tout va bien (plus de 90 %).
- Quatre temps : **échauffement** (3 révisions) → **nouveaux** (fiche, tracé au doigt dans la grille 米字格, vérification)
  → **pratique** (sens, lecture, écoute, mot entier, phrase à trous) → **écrire de mémoire** et phrases des nouveaux.
- Les séries de bonnes réponses (连 ×3, ×4…) rapportent des points en plus.

## Niveaux, défis, quêtes, médailles

- **8 niveaux** : les titres des examens impériaux, de 童生 (la candidate) à 状元 (la première de l'empire),
  affichés comme un sceau rouge. Fichier `source/rangs.txt` (pinyin vérifié à la main, points nécessaires).
- **Défi du jour** (un différent chaque jour, les autres rejouables) : 字谜 le caractère mystère (il apparaît trait par
  trait), 部首 la chasse aux clés (25 s par clé), 快 l'éclair (60 s). Débloqués à 5 caractères appris.
- **3 quêtes du jour** tirées au sort selon la date (+20 chacune, +50 et un sceau sur le calendrier pour les 3).
- **17 médailles** dans l'onglet Progrès, avec le calendrier des 12 dernières semaines et la date prévue de fin du mur.

## Mon rouleau 卷 (la progression sur l'accueil)

- Les 214 caractères forment un rouleau de **11 pages de 20**, écrites en colonnes de droite à gauche comme un texte
  classique. Appris = à l'encre ; le prochain = case rouge en pointillés ; à venir = en filigrane.
- **L'encre pâlit** quand un caractère n'est plus révisé (rétention moyenne sous 70 %) : la séance le repasse à l'encre.
- Un petit sceau 读 marque le caractère qui débloque une lecture. Page finie = sceau 完成 et +50 points.
- Au retour de séance, les nouveaux caractères s'écrivent à l'encre sous ses yeux. On peut feuilleter les pages.

## Préparer le HSK (onglet 考 HSK)

- Les **174 caractères du HSK 1** (150 mots, `source/hsk1.txt`) sont repérés : jauge « vus / bien ancrés ».
- **Examen blanc · lecture** : 20 questions, 4 parties comme le vrai HSK 1 (vrai/faux, phrase, question-réponse,
  phrase à compléter), 17 minutes, note sur 100, réussi à 60, avec ou sans pinyin, correction à la fin.
  Questions-réponses dans `source/hsk_qr.txt`. Entraînement partie par partie (5 questions, correction immédiate).

## Ajouter des caractères ou corriger une fiche

1. Écrire une ligne dans `source/fiches*.txt` :
   `caractère|pinyin|sens|clé|sens de la clé|composition|histoire|mot:sens;mot:sens|phrase exemple:traduction`
2. Ajouter le caractère dans `source/ordre.json` à la place voulue.
3. Pousser sur `main` : le robot **Zìzì — données et audio** reconstruit `data.json`, télécharge l'ordre des traits,
   génère les voix et passe la version du service worker. Ou à la main, depuis `caracteres/` :
   ```bash
   pip install pypinyin sherpa-onnx soundfile        # + ffmpeg
   python3 outils/construire.py --relire              # vérifie et affiche tout le pinyin à relire
   python3 outils/generer_audio_zizi.py
   python3 outils/test_zizi.py                        # pip install playwright && playwright install chromium
   ```
4. Si un pinyin calculé est faux : ajouter la phrase exacte dans `outils/pinyin_corrections.json`
   ou le mot dans le dictionnaire `FIXED` de `outils/pinyin_fr.py`.

**Ne jamais renommer ni retirer un caractère déjà appris** : sa progression est enregistrée sous ce caractère.

## Installer sur le téléphone

Ouvrir **https://kkepiphane.github.io/bubugao-chinois/caracteres/** dans **Chrome** sur Android (pas dans Bùbùgāo ni
dans WhatsApp), une première fois avec du réseau. Une carte « Installe Zìzì » apparaît sur l'accueil ; si Chrome ne
propose rien, une aide explique où est « Installer » dans le menu ⋮. Ensuite l'appli marche sans connexion.

Piège : Zìzì est sous l'adresse de Bùbùgāo. Si Bùbùgāo est installée, Android ouvre Zìzì dans la fenêtre de Bùbùgāo,
où on ne peut pas l'installer. C'est pourquoi le lien 字 de Bùbùgāo ouvre Zìzì dans Chrome, et Zìzì affiche
« Ouvrir dans Chrome » si elle se retrouve quand même dans la fenêtre de Bùbùgāo. L'appli Zìzì installée démarre
avec `?app=zizi` (manifeste) : c'est ainsi qu'elle se reconnaît. Le logo se redessine avec `python3 outils/icone.py` (Chrome requis).

Mise en ligne : tout ce qui arrive sur `main` est publié automatiquement par GitHub Pages, comme Bùbùgāo.
Après une modification de `index.html`, passer `zizi-app-vN` à `N+1` dans `sw.js` pour que le téléphone se mette à jour.

## Crédits et licences

- Ordre des traits et correction du tracé : [Hanzi Writer](https://github.com/chanind/hanzi-writer) (MIT).
- Données de traits et décomposition : [Make Me a Hanzi](https://github.com/skishore/makemeahanzi) (Arphic Public License).
- Voix : sherpa-onnx, modèle open source `matcha-icefall-zh-baker` (jeu de données Baker, usage non commercial).
- Les histoires mnémotechniques sont des aides pour retenir, pas toujours l'étymologie exacte.
