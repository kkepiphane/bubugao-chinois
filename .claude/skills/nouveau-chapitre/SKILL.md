---
name: nouveau-chapitre
description: Écrire un nouveau chapitre de Bùbùgāo (parcours HSK ou branche thématique usine/vie quotidienne), le vérifier, générer son audio et le mettre dans la file du robot du lundi. À utiliser dès qu'on demande d'ajouter du contenu, des mots, un chapitre, une conversation ou une leçon.
---

# Nouveau chapitre

Un chapitre = un fichier JSON. Il entre dans la file `a-publier/` ; le robot du lundi le propose ensuite à Epiphane
en Pull Request, et il n'arrive sur le téléphone qu'après validation.

## 1. Choisir le contenu

- **Parcours HSK** (`"branch": "hsk"`, `"level": 1|2…`) : ~15 mots de la liste officielle (ancien HSK : 150 mots en HSK 1,
  300 en HSK 2), regroupés par thème, + 2 ou 3 phrases utiles qui les emploient. Ne pas reprendre un mot déjà présent
  (chercher son caractère dans `packs/`, `a-publier/` et `audio/base-contenu.json`).
- **Branche thématique** (`"travail"` ou `"quotidien"`) : 8 à 12 mots/phrases de la vraie vie de l'utilisatrice
  (usine de chaussures à Lomé, marché, transport, santé, téléphone, collègues chinois).
- Toujours : **une** règle de grammaire simple, **une** conversation, 1 ou 2 duels de tons, 6 à 8 caractères avec leur clé.

## 2. Écrire le chapitre

Ajouter le chapitre dans `scripts/make_packs.py` (même style que les autres : `PACKS.append(dict(...))`, `publish=False`),
puis `cd scripts && python3 make_packs.py`. Le script vérifie caractères / syllabes / tons et écrit le JSON.
Ou écrire directement le JSON sur le modèle de `packs/hsk1-01-presenter.json`.

Champs d'un mot :
```json
{"id": "q_tomate", "h": "西红柿", "p": "xi-hong-shi", "t": [1, 2, 4], "fr": "Tomate", "st": 0, "m": "Mission (facultatif)"}
```
- `id` unique et définitif, préfixé par chapitre (`k11_`, `q2_`, `w3_`…). Ne jamais réutiliser ni renommer.
- `p` : pinyin sans accents ; espace entre les mots, `-` entre les syllabes d'un mot ; `v` pour ü (`nv` = nǚ) ;
  le 儿 d'un mot rétroflexe est une syllabe `r` de ton 0 (`哪儿` → `na-r`, `[3,0]`).
- `t` : tons écrits (0 = neutre). `s` : tons prononcés si différents (sandhi 3+3 → 2+3, suite de trois 3e tons…).
- `fr` : sens court, en français. `st` : 0 sauf pour la branche travail (0 Usine, 1 Promotion, 2 Entretien, 3 Ailleurs).
- `m` : mission terrain concrète, faisable à l'usine ou en ville, avec la phrase en caractères.

Conversation : nœuds `a`, `b`, … `end` ; chaque option a `ok:1` + `n` (nœud suivant) ou `fix` (correction bienveillante
en français qui donne la bonne phrase). Le prénom de l'utilisatrice s'écrit `{name}`. Au moins une option juste par nœud.

## 3. Vérifier (obligatoire)

1. Relire chaque ligne de chinois : sens, caractères simplifiés, pinyin, tons, sandhi. Préférer le chinois parlé courant.
2. `cd scripts && python3 make_packs.py` → aucune erreur d'assertion.
3. Ajouter le chapitre à la fin de `a-publier/ordre.json` (`id`, `file`, `title`).
4. Audio : `python3 scripts/generer_audio.py` (ou laisser le workflow `audio.yml` le faire après le push).
   Écouter 2 ou 3 MP3 générés si possible.
5. `python3 scripts/test_appli.py` → « TOUT EST BON ».

## 4. Livrer

Commit sur une branche, Pull Request vers `main` avec, dans la description, la liste des mots (caractères + sens),
la règle de grammaire et le titre de la conversation, pour qu'Epiphane puisse relire depuis son téléphone.
Le chapitre restera dans `a-publier/` jusqu'au lundi où le robot le proposera.

Pour publier **tout de suite** (correction urgente d'un chapitre déjà publié) : modifier le fichier dans `packs/`,
incrémenter son `"v"` dans `packs/packs.json`, garder les mêmes `id`.
