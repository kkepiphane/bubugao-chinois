---
name: nouveaux-caracteres
description: Ajouter ou corriger des caractères, histoires, mots, phrases ou lectures dans Zìzì (caracteres/), l'appli d'écriture des caractères. À utiliser pour tout contenu de Zìzì : nouveau lot de caractères (ex. HSK 2), fiche à corriger, nouvelle lecture.
---

# Nouveaux caractères pour Zìzì

Tout le contenu vit dans `caracteres/source/` ; `data.json`, `traits.json` et `audio/` sont **générés**
(ne jamais les éditer à la main).

## Une fiche = une ligne de `source/fiches*.txt`

```
好|hǎo|bien, bon|女|femme|女 femme + 子 enfant|Une femme avec son enfant : c’est bien, c’est bon.|你好:bonjour;好的:d’accord|今天天气很好。:Il fait beau aujourd’hui.
```
9 champs séparés par `|` : caractère, pinyin (avec accents, lecture principale ; noter l'autre lecture dans le sens,
ex. « (se lit aussi cháng : long) »), sens court en français, clé (forme réduite : 亻 氵 讠 扌 忄 钅 饣 纟 犭 礻 衤…),
sens de la clé, composition (« 女 femme + 子 enfant », signaler les composants qui donnent le son), histoire,
2–3 mots `mot:sens` séparés par `;` (chacun contient le caractère), une phrase exemple `phrase:traduction`
(contient le caractère, ≤ 12 caractères, vocabulaire simple, de préférence des caractères déjà dans la liste).

Règles de qualité :
- **Chinois simplifié exact**, phrases naturelles du mandarin parlé ; utiliser la vie de l'utilisatrice
  (usine de chaussures à Lomé, collègues chinois, famille, marché).
- **Histoire** : une phrase concrète et visuelle qui relie la forme (les composants) au sens. Vérifier la
  décomposition réelle (Make Me a Hanzi : `dictionary.txt` du dépôt skishore/makemeahanzi). Une aide mnémotechnique
  peut s'écarter de l'étymologie, mais ne doit jamais affirmer une fausse étymologie comme un fait.
- Français simple, tutoiement dans les histoires.

## Ordre

`source/ordre.json` est la liste d'apprentissage. Placer un caractère **après ses composants** déjà présents dans la
liste, et les caractères très fréquents tôt. Ajouter à la fin pour un nouveau lot (ex. HSK 2) : un caractère déjà
appris par l'utilisatrice ne doit jamais changer de nom ; changer sa position est sans risque.

## Lectures

`source/lectures.txt` : `titre|phrase:traduction||phrase:traduction…`. 4 à 6 phrases courtes, au moins 85 % de
caractères de la liste (les autres apparaissent soulignés et restent cliquables). La lecture s'ouvre
automatiquement quand elle connaît 85 % de ses caractères.

## Construire et vérifier (depuis `caracteres/`)

```bash
python3 outils/construire.py --relire     # erreurs de format + tout le pinyin calculé, à relire ligne par ligne
python3 outils/generer_audio_zizi.py      # voix manquantes
python3 outils/test_zizi.py               # « TOUT EST BON » obligatoire
```
Relire le pinyin affiché : tons neutres (名字 míngzi), 一/不, mots collés, lectures multiples (长, 觉, 还, 只, 得…).
Corriger dans `outils/pinyin_fr.py` (`FIXED` pour un mot, `WORDS` pour garder un mot entier) ou dans
`outils/pinyin_corrections.json` pour une phrase entière.

Après un changement de `index.html` ou `data.json` publié à la main : incrémenter `VERSION` dans `caracteres/sw.js`
(le robot `zizi.yml` le fait tout seul quand il reconstruit). Livrer par Pull Request, avec la liste des
caractères ajoutés et leur histoire dans la description.
