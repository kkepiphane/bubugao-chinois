# Zìzì 字字 — apprendre les caractères

« 字字珠玑 » : chaque caractère est une perle. Appli sœur de Bùbùgāo, dans le même dépôt :
**https://kkepiphane.github.io/bubugao-chinois/caracteres/** (installable, hors-ligne).

## Ce qu'elle apprend

- **214 caractères** : les 174 du HSK 1 + 32 de l'usine (鞋 底 胶 线 质 量 检 查…) + 8 très fréquents (要 给 也 还…).
- **Ordre « briques d'abord »** : les mots utiles en premier (你好, 谢谢, 我是…), et chaque caractère arrive juste après
  ses composants (女 et 子 avant 好, 人 avant 认).
- **Fiche de chaque caractère** : ordre des traits animé (la clé en rouge), pinyin coloré par ton et voix, sens en
  français, **clé** et composition, **petite histoire pour s'en souvenir**, 2–3 mots, une phrase exemple traduite.

## La séance du jour (≈ 10 min)

1. **Découvrir** 5 nouveaux caractères (réglable : 3, 5 ou 8), puis **les tracer au doigt** dans la grille 米字格,
   trait par trait, avec correction automatique.
2. **Réviser** : sens, lecture (pinyin et ton), écoute (quel caractère entends-tu ?), **phrase à trous**,
   et **écrire de mémoire** pour les caractères déjà vus (révisions espacées, 3 compétences par caractère).

## Le reste

- **Mon mur** : les 214 caractères en grille, qui se colorent à mesure qu'ils s'ancrent. Recherche par sens ou pinyin.
- **Les clés** (部首) : 90 familles (氵 eau, 口 bouche, 亻 personne…) avec leurs caractères.
- **Lire** : 13 petits textes de sa vie (usine, famille, magasin, paie…) qui se débloquent quand elle connaît 85 %
  de leurs caractères. Pinyin et traduction seulement si elle les demande.
- Série de jours avec jokers, paliers (10, 25, 50, 100… caractères), sauvegarde/restauration dans les réglages.

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

Ouvrir **https://kkepiphane.github.io/bubugao-chinois/caracteres/** dans Chrome sur Android, une première fois avec
du réseau. Une carte « Installe Zìzì » apparaît sur l'accueil (sinon : menu ⋮ › « Ajouter à l'écran d'accueil »).
Ensuite l'appli marche sans connexion. Le logo se redessine avec `python3 outils/icone.py` (Chrome requis).

Mise en ligne : tout ce qui arrive sur `main` est publié automatiquement par GitHub Pages, comme Bùbùgāo.
Après une modification de `index.html`, passer `zizi-app-vN` à `N+1` dans `sw.js` pour que le téléphone se mette à jour.

## Crédits et licences

- Ordre des traits et correction du tracé : [Hanzi Writer](https://github.com/chanind/hanzi-writer) (MIT).
- Données de traits et décomposition : [Make Me a Hanzi](https://github.com/skishore/makemeahanzi) (Arphic Public License).
- Voix : sherpa-onnx, modèle open source `matcha-icefall-zh-baker` (jeu de données Baker, usage non commercial).
- Les histoires mnémotechniques sont des aides pour retenir, pas toujours l'étymologie exacte.
