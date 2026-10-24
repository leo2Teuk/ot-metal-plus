# O.T METAL PLUS — Application de gestion de devis

## Présentation

Application Django server-rendered pour saisir, calculer, enregistrer et produire des devis commerciaux au format PDF. L’interface regroupe les coordonnées du client, les lignes de produits, les conditions du devis et le récapitulatif financier.

## Objectif métier

Le projet vise à remplacer la préparation manuelle répétitive des devis par un formulaire unique et des règles de calcul cohérentes. Les devis sont enregistrés localement et peuvent être consultés dans un historique.

## Fonctionnalités

- Création d’un devis avec numéro, date, ville et coordonnées client.
- Saisie de jusqu’à 15 lignes de produits, avec quantité, prix unitaire et calcul des montants.
- Calcul du sous-total, d’une remise en FCFA ou en pourcentage, de la TVA fixe de 19,25 % et du total.
- Enregistrement du devis dans SQLite et génération du document PDF.
- Consultation de l’historique, ouverture du PDF, duplication et suppression d’un devis.
- Validation de dates au format formulaire ISO et au format localisé `jour/mois/année`.

L’application ne comporte actuellement ni authentification utilisateur ni API REST.

## Technologies

- Python 3 et Django (`Django>=5.0,<6.0`)
- SQLite et migrations Django
- ReportLab pour le calque PDF et pypdf pour la lecture/fusion du modèle
- Templates Django, CSS et JavaScript côté navigateur

## Architecture

```text
manage.py                         Entrée des commandes Django
otmetal/settings.py               Configuration, base et environnement
otmetal/urls.py                   Routage racine et templates
otmetal/quotes/                    Application métier des devis
otmetal/quotes/models.py          Modèle Quote
otmetal/quotes/forms.py           Validation des champs du devis
otmetal/quotes/views.py           Création, historique et opérations sur devis
otmetal/quotes/services/          Calculs et production PDF
otmetal/quotes/migrations/        Historique de schéma conservé
otmetal/quotes/templates/         Formulaire et historique HTML
otmetal/quotes/static/            CSS et JavaScript de l’interface
templates/                        Modèle PDF de démonstration
docs/                              Documentation complémentaire
```

Le modèle `Quote` conserve les informations de l’en-tête, les produits sérialisés en JSON et les montants calculés. La base de développement est SQLite ; elle n’est pas incluse dans Git.

## Flux de génération PDF

```text
Formulaire Django
	→ validation des champs et lignes produits
	→ calcul des montants et de la TVA
	→ enregistrement SQLite (sauf aperçu)
	→ superposition des données sur le modèle PDF de deux pages
	→ réponse PDF dans le navigateur
```

Le générateur utilise `templates/Devis_OT_Metal_Plus_demo.pdf`. Le document commercial original n’est pas versionné.

## Installation et lancement

Prérequis : Python compatible avec Django 5 et `pip`.

```powershell
git clone https://github.com/leo2Teuk/ot-metal-plus.git
cd ot-metal-plus
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Éditer ensuite `.env` et remplacer le placeholder de clé par une clé locale. Puis :

```powershell
py manage.py migrate
py manage.py runserver
```

Ouvrir `http://127.0.0.1:8000/`. Le projet ne fournit pas de compte utilisateur : l’écran de création de devis est directement accessible en développement.

## Configuration et sécurité

Variables lues depuis `.env` ou l’environnement du processus :

```env
DJANGO_SECRET_KEY=replace-with-local-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=
```

Le placeholder est réservé au développement avec `DEBUG=True`. Avec `DEBUG=False`, une `DJANGO_SECRET_KEY` explicite est obligatoire. Configurer également `ALLOWED_HOSTS` et, si nécessaire, les origines CSRF pour l’environnement de déploiement. Ne jamais versionner `.env` ni `db.sqlite3`.

## Tests

```powershell
py manage.py check
py manage.py test
```

Les tests couvrent les calculs de remise/TVA, la limite de lignes et la soumission de devis.

## Boutique en ligne TLveta

Le dépôt contient également la boutique e-commerce Flutter Web et son API
Strapi 5 dans [`flutter_ecommerce/`](./flutter_ecommerce/) et
[`strapi-cms/`](./strapi-cms/). Le catalogue public affiche les tarifs, tandis
que l’ouverture d’une fiche produit, le panier et les commandes nécessitent un
compte client. Le paiement est une simulation locale de 10 secondes : aucune
transaction Stripe réelle ni donnée de carte n’est utilisée.

Les instructions pour démarrer les deux applications, accéder à
l’administration Strapi, recréer les produits et tester les routes avec Postman
sont détaillées dans le [guide de l’API Strapi](./strapi-cms/README.md). Le
[README Flutter](./flutter_ecommerce/README.md) décrit le fonctionnement de la
boutique.

## Limitations

- SQLite est prévu pour le développement local ; aucun déploiement de production n’est documenté.
- La TVA est fixe dans le service de calcul.
- Le rendu PDF dépend du modèle de démonstration fourni.
- Les routes sont des vues Django HTML/PDF, pas une API REST.
- Aucune licence n’a encore été choisie.

## Auteur

`leo2Teuk`
