# Architecture du projet OT Metal Plus

## Vue d’ensemble

L’application est une solution Django dédiée à la gestion de devis. Elle permet de remplir un formulaire métier, calculer automatiquement les montants, puis produire un document PDF finalisé à partir d’un template fourni.

## Composants principaux

### 1. Application quotes

La logique métier est centralisée dans l’application `otmetal.quotes`.

- `forms.py` : formulaires de saisie
- `models.py` : modèle `Quote`
- `views.py` : vues de création, historique et génération PDF
- `urls.py` : routes applicatives
- `tests.py` : tests unitaires et fonctionnels

### 2. Services

Le dossier `services/` contient les composants de calcul et d’édition PDF.

- `calculations.py` : calcul du sous-total, discount, TVA et total
- `pdf_generator.py` : fusion du modèle PDF avec les données saisies

### 3. Template PDF

Le fichier dans `templates/Devis_OT_Metal_Plus.pdf` sert de document de référence. Les données sont injectées par overlay sur les zones identifiées dans le PDF.

## Flux métier

1. L’utilisateur remplit le formulaire de devis.
2. Le backend valide les données.
3. Les produits sont analysés et calculés.
4. Le devis est sauvegardé en base SQLite.
5. Le PDF final est généré et renvoyé au navigateur.

## Points d’amélioration

- externalisation de la base dans PostgreSQL
- ajout d’un système d’authentification
- gestion multi-utilisateurs
- API REST pour intégration externe
