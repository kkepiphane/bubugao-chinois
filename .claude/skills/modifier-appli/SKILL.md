---
name: modifier-appli
description: Modifier l'appli Bùbùgāo (index.html, sw.js) — nouvelle fonction, correction de bug, changement d'écran — sans casser la progression enregistrée, le hors-ligne ni les mises à jour. À utiliser pour toute modification de code de l'appli.
---

# Modifier l'appli

L'appli tourne sur un Android d'entrée de gamme, souvent hors-ligne, avec des mois de progression stockés dans le navigateur.
Une erreur JavaScript au démarrage = elle ne peut plus apprendre. Prudence d'abord.

## Ce qu'il ne faut jamais casser

- **État** : `S` (clé `bubugao.v1`), chapitres `PS` (`bubugao.packs.v1`), index audio (`bubugao.audio`).
  Pour un nouveau champ : l'ajouter dans `fresh()` ; `load()` fusionne avec `Object.assign(fresh(), ancien)`, donc les
  anciennes sauvegardes restent valides. Ne jamais renommer ni supprimer un champ existant ; ne jamais changer `v:1`
  sans écrire une migration.
- **Identifiants** de mots, chapitres, conversations, caractères (les clés de `S.items`, `S.chars`, `S.convDone`…).
- **Fonctions utilisées par les chapitres JSON** : `installPack`, `validItem`, `prep`. Un ancien chapitre doit toujours se charger.
- **Hors-ligne** : rien de bloquant au démarrage ne doit dépendre du réseau. Polices Google = facultatives (repli système).
- **Sauvegarde/restauration** : `backupData()` / `applyRestore()` doivent relire les anciennes sauvegardes.

## Méthode

1. Lire la zone concernée de `index.html` (gros fichier : chercher par `grep -n`). Les écrans sont des fonctions
   `renderHome`, `renderParler`, `renderProgres`, `renderCarriere`, `renderSession` + les vues d'exercices `v*` ;
   les actions passent par l'objet `ACT` et l'attribut `data-act`.
2. Modifier en gardant le style existant (fonctions courtes, gabarits HTML en chaînes, jetons CSS `--…` du `:root`,
   clair et sombre). Textes en français simple, tutoiement.
3. Si le contenu de base (entre `BEGIN_DATA` et `END_DATA`) change : `node scripts/exporter_base.js` puis
   `python3 scripts/generer_audio.py`.
4. **Incrémenter `VERSION` dans `sw.js`** (`bubugao-app-vN` → `vN+1`), sinon les téléphones gardent l'ancienne version plus longtemps.
5. Vérifier :
   - `python3 scripts/test_appli.py` → « TOUT EST BON » ;
   - si l'analyse des tons a été touchée : `node scripts/banc_tons.js` (ne pas descendre sous ≈ 79 % / 73 %) ;
   - regarder l'écran modifié à 390 px de large, en clair et en sombre (capture Playwright).
6. Pull Request vers `main` avec, en français, ce qui change pour l'utilisatrice et comment Epiphane peut le vérifier sur son téléphone.

## Rappels techniques

- `localStorage` est la seule persistance ; toujours dans `try/catch`.
- Le son ne peut démarrer qu'après un geste (toucher) : appeler `say()` dans un gestionnaire de clic ou juste après.
- Micro : `getUserMedia` + `MediaRecorder` ; repli « enregistreur du téléphone » (`<input type=file accept=audio/* capture>`).
- Les chemins sont **relatifs** (le site est servi depuis `/bubugao-chinois/`).
