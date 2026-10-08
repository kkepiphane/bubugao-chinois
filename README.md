# Bùbùgāo 步步高 — coach de chinois

**« Monter marche après marche. »** Une appli gratuite pour apprendre le chinois mandarin, pensée pour une ouvrière
francophone d'une usine de chaussures à Lomé qui veut progresser : comprendre son chef, obtenir une promotion,
réussir un entretien, passer le HSK, voyager.

👉 **Appli : https://kkepiphane.github.io/bubugao-chinois/** (ouvrir dans Chrome sur Android, puis « Installer »)

## Ce que fait l'appli

- **Séance du jour (≈ 12 min)** qui s'adapte : nouveaux mots, révisions espacées, duel de tons, prononciation avec
  courbe de voix, caractères, conversation en jeu de rôle, mission à faire pour de vrai à l'usine.
- **Parcours HSK 1** (les 150 mots officiels en 10 chapitres) + branches **Usine et travail** et **Vie quotidienne**.
- **Voix chinoise intégrée** (fichiers audio), qui marche sur tous les téléphones et **sans connexion**.
- **Analyse des tons** de sa voix, sur le téléphone (aucun son n'est envoyé).
- **Motivation** : série de jours avec jokers, test HSK blanc chaque mois, voix avant/après, missions de plus en plus ambitieuses.
- **Hors-ligne**, installable, mise à jour automatique dès qu'il y a du réseau, sauvegarde/restauration de la progression.

## Pour le mainteneur

- **Chaque lundi** : un robot propose le chapitre suivant en Pull Request « 📚 À valider ». *Merge* = publié.
- **Guide pas à pas** (installation, sauvegarde, publication, format des chapitres) : [LISEZMOI.md](LISEZMOI.md).
- **Continuer avec Claude** : ouvrir le dépôt dans Claude Code ; [CLAUDE.md](CLAUDE.md) et les skills de
  `.claude/skills/` (nouveau chapitre, modifier l'appli, voix et tons) lui donnent tout le contexte.

```bash
python3 scripts/test_appli.py      # test complet dans un navigateur
node scripts/banc_tons.js          # justesse de l'analyse des tons
python3 scripts/generer_audio.py   # audio manquant
```

## Structure

```
index.html            l'appli complète (sans dépendance)
sw.js                 hors-ligne et mises à jour
packs/                chapitres publiés (+ packs.json)
a-publier/            chapitres en attente (+ ordre.json)
audio/                un MP3 par texte chinois (+ index.json)
scripts/              génération des chapitres, de l'audio, tests
.github/workflows/    robot du lundi, génération audio
```

## Crédits

Voix : modèle open source [matcha-icefall-zh-baker](https://github.com/k2-fsa/sherpa-onnx) (sherpa-onnx, jeu de données
Baker — usage non commercial). Vocabulaire : liste officielle HSK 1 (ancien format, 150 mots).
