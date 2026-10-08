# Bùbùgāo 步步高 — mise en ligne et mises à jour

## 1. Mettre en ligne gratuitement (une seule fois)

**GitHub Pages** : gratuit, sans date d'expiration, HTTPS inclus.

1. Créer un dépôt **public** sur GitHub, par ex. `bubugao`.
2. Y déposer **tout le contenu du zip**, y compris le dossier caché `.github/` (le robot du lundi), `scripts/` et `a-publier/`.
   Le plus simple : *Add file › Upload files* et glisser le dossier décompressé.
3. **Settings › Pages** › *Deploy from a branch* › `main` › `/ (root)`.
4. **Settings › Actions › General** › *Workflow permissions* : cocher **Read and write permissions**
   et **Allow GitHub Actions to create and approve pull requests**, puis *Save*.
5. **Adresse définitive (très important)** : chez ton fournisseur de domaine, créer un CNAME `chinois` → `ton-pseudo.github.io`,
   puis dans **Settings › Pages › Custom domain** entrer `chinois.doole.cloud` et cocher *Enforce HTTPS*.

La progression est liée à l'adresse : **ne jamais changer l'adresse**. Pour changer d'hébergeur (Cloudflare Pages, Netlify…),
déplacer les fichiers et modifier seulement le CNAME.

## 2. Installer sur le téléphone de ton amie

1. Ouvrir l'adresse dans **Chrome** (Android), avec du réseau.
2. Toucher **Installer** sur l'accueil de l'appli, ou menu ⋮ › **Ajouter à l'écran d'accueil**.
3. Une fois : Réglages Android › Synthèse vocale › moteur Google › installer la langue **Chinois (Mandarin)**, pour que la voix marche sans réseau.

Ensuite l'appli s'ouvre depuis son icône, même en mode avion.

## 3. Sauvegarde de sa progression

Sa progression vit dans son téléphone. Onglet **Progrès › Sauvegarde** :
- **Sauvegarder ma progression** crée un petit fichier `.json` (partage direct vers WhatsApp, Drive ou e-mail sur Android).
- **Restaurer** sur un nouveau téléphone : installer l'appli, puis choisir ce fichier.

L'appli lui rappelle de sauvegarder une fois par mois. Elle demande aussi au navigateur de protéger ses données
(accordé en général quand l'appli est installée sur l'écran d'accueil).

## 4. Le programme

- **Parcours HSK 1** (liste officielle, ancien format, 150 mots) : 10 chapitres `hsk1-01` à `hsk1-10`.
  Les 3 premiers sont publiés. Les 7 suivants sont prêts dans le dossier `a-publier/`.
  **Rythme conseillé : 1 chapitre HSK par semaine.** Elle aura vu tout le HSK 1 en environ 2 mois et demi.
- **Branches thématiques** (elle choisit la sienne sur l’accueil) : « Usine et travail » et « Vie quotidienne ».
  Chaque séance mélange environ 6 mots du parcours HSK et 4 mots de sa branche.
- Chaque chapitre apporte : des mots, une règle de grammaire, une conversation, un duel de tons et 6 à 8 caractères avec leur clé.
- **Test HSK blanc** : proposé automatiquement tous les 28 jours, dès qu’elle a vu 20 mots HSK.
- **Missions terrain** : niveau 1 (une phrase), 2 dès 5 missions réussies (une question), 3 dès 12 (2 minutes de conversation).

## 5. Publier un nouveau chapitre : le robot du lundi

Chaque **lundi à 7 h** (heure de Lomé), un robot GitHub prépare le chapitre suivant de `a-publier/`
(dans l'ordre de `a-publier/ordre.json`) et ouvre une **Pull Request** intitulée « 📚 À valider : … ».
Tu reçois un e-mail / une notification GitHub avec la liste des mots, la règle de grammaire et la conversation.

- **Merge pull request** → le chapitre est publié. Il arrive sur son téléphone dès qu'elle a du réseau.
- **Close pull request** → rien n'est publié ; le robot reproposera le même chapitre le lundi suivant.
- Le robot ne propose rien tant qu'une demande est encore ouverte, et s'arrête quand `a-publier/` est vide.
- Pour avancer sans attendre lundi : onglet **Actions › Chapitre du lundi › Run workflow**.

Avant de publier, le robot vérifie que chaque mot a autant de caractères que de syllabes et de tons. Sinon, il s'arrête et rien n'est publié.

**Ajouter de nouveaux chapitres à la file** : déposer le fichier dans `a-publier/` et ajouter une ligne dans `a-publier/ordre.json`.

**À savoir** : GitHub met en pause les robots planifiés d'un dépôt public sans activité pendant 60 jours.
Chaque validation compte comme activité. Après une longue pause, il suffit de cliquer **Enable workflow** dans l'onglet Actions.

**Publier à la main** (sans robot) : déplacer le fichier de `a-publier/` vers `packs/` et ajouter une ligne à la fin de `packs/packs.json` :
```json
{"id": "hsk1-04", "v": 1, "file": "hsk1-04-temps.json", "title": "HSK 1 · 4 — L’heure et la date"}
```

Dès que son téléphone a du réseau (à l'ouverture, au retour de la connexion, ou après 6 h), l'appli télécharge le chapitre,
le garde pour le hors-ligne et affiche « Nouveau chapitre ». Sa progression n'est jamais effacée.

**Corriger un chapitre déjà publié** : modifier le fichier, puis passer `"v": 1` à `"v": 2` dans `packs.json`.
Garder les mêmes `id` de mots : la progression sur ces mots est conservée.

## 6. Format d'un mot

```json
{"id": "m_tomate", "h": "西红柿", "p": "xi-hong-shi", "t": [1, 2, 4], "fr": "Tomate", "st": 0, "m": "Mission facultative"}
```

- `id` : unique pour toujours (préfixe par chapitre conseillé : `m_`, `n_`, `h_`…)
- `h` : caractères · `p` : pinyin sans accents, mots séparés par un espace, syllabes par `-`
- `t` : tons écrits (1 à 4, 0 = neutre), un par syllabe · `s` (facultatif) : tons réellement prononcés (ex. 你好 → `[2,3]`)
- `fr` : sens · `st` : étape (0 Usine/bases, 1 Promotion, 2 Entretien, 3 Ailleurs) · `m` : mission terrain (facultatif)

Un mot dont le nombre de caractères, de syllabes et de tons ne correspond pas est ignoré automatiquement.

Un chapitre peut aussi contenir `grammar` (une règle avec exemples), `pairs` (duels de tons), `convs` (conversations) et `bonus`.
Ajoute aussi `"branch"` : `"hsk"`, `"travail"` ou `"quotidien"`. Voir `hsk1-01-presenter.json` pour un exemple complet.
Le script `scripts/make_packs.py` contient tout le contenu en clair : il régénère les chapitres et vérifie que caractères, pinyin et tons concordent.

## 7. Mettre à jour l'appli elle-même

Remplacer `index.html`, et changer `VERSION` dans `sw.js` (ex. `bubugao-app-v5`).
