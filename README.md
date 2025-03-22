# website_cuma

Application web pour suivre l'utilisation de matériel prêté par une CUMA.

## CUMA

Coopérative d'Utilisation de Matériel Agricole, une CUMA est une association de personnes qui mettent en commun des moyens pour réaliser des travaux agricoles.
Le besoin principal est de numériser le suivi de l'utilisation du matériel. Les utilisateurs reportent actuellement les heures d'utilisation dans un carnet, qu'il faut reporter dans un tableur pour faire les comptes.

Une personne peut être responsable d'un outil et utilisateur d'autres outils.

## Installation

### Conda

Environnement virtuel avec [miniconda](https://docs.conda.io/projects/miniconda/en/latest/)

Créer l'environnement avec la commande suivante:

```bash
conda env create -f environment.yaml
```

Cela créera un environnement nommé 'cumaweb' avec python 3.11 et avec [poetry](https://python-poetry.org/) qui va nous permettre de gérer les dépendances.
Pour activer l'environnement `conda activate cumaweb`. Puis lancer `poetry install` pour installer les fichiers de dépendances. Pour update les dépendances ajoutées, lancer `poetry update`.

Pour activer les hooks de pre-commit, il faudra (toujours dans l'environnement) lancer la commande suivante `pre-commit install`.
Pour mettre à jour les hooks, lancer la commande suivante `pre-commit autoupdate`.

### env

Vous pouvez aussi créer votre environnement en utilisant env et poetry comme suit :

```bash
TODO
```

### Setup VSCODE

N'oublier pas de spécifier l'environnement dans vscode, taper `ctrl+shift+p` et chercher `Python: Select Interpreter` et choisir l'environnement `cumaweb`.

### A propos de poetry

Organisation des dépendances avec [poetry](https://python-poetry.org/). Avec poetry, nous pouvons organiser les dépendances par groupe. Nous avons définis les groupes suivants doc

- poetry add LIB pour ajouter une dépendance générale
- poetry add LIB --group dev pour ajouter à groupe dev
- poetry add LIB --group doc pour ajouter à groupe doc

Pour l'instant on commit le fichier `poetry.lock` pour que les dépendances soient les mêmes pour tout le monde et pour plus de reproductibilité entre nos machines mais [potentiellement enlevable](https://python-poetry.org/docs/basic-usage/#committing-your-poetrylock-file-to-version-control).

### Django

Références :

- <https://www.youtube.com/watch?v=Bn0k9DDYBZM>

`django-admin startproject cumaweb` pour lancer le projet django et créer le framework
Dans le dossier `cumaweb` crée :

- dans `setting.py` on fixe `DEBUG = True` pour debug
- dans `setting.py` on retrouve les templates
  - si on ajoute une app `blog` à coté du dossier `cumaweb` (vidéo à 1h18)
- dans `urls.py`, ajouter dans la liste `urlspatterns` les paths **relatifs** qui renvoient vers des views (j'ai mis une view index pour page d'accueil)
- dans `views.py`, on peut ajouter des vues qui renvoient vers les templates qui sont dans `templates\cumaweb` (il explique dans la vidéo à 1h39 pourquoi créer un sous-dossier `\cumaweb` dans `templates`), j'ai juste fait un template basique

`python src/manage.py runserver` pour lancer le serveur local (il doit y avoir un moyen de setup le dossier src comme start directory <https://stackoverflow.com/questions/43305050/changing-the-default-path-of-visual-studio-codes-integrated-terminal>)
`CTRL+C` pour arrêter le serveur
`python src/manage.py migrate` sinon y a des warnings (à comprendre mieux)

`python src/manage.py test catalog` pour lancer le fichier de tests unitaires de l'application catalog

### Ecriture de la documentation

Pour écrire la documentation, nous utilisons [mkdocs](https://www.mkdocs.org/).
TODO: comment ca s'utilise ?

## Fonctionnalité et étude du projet

### Role

Admin
Admin d'un outil/ ou de plusieurs outils
Utilisateur

### EN vrac

Répartir une liste d'outil
Faire un menu de recherche pour claim un outil ou pour personnaliser son nombre d'heure.

pouvoir saisir les heures de chacun

Le responsable gere l'agenda de l'outil, ils envoient des sms pour dire que l'outil est disponible.

Utilisable sur téléphone portable est obligatoire.

Mettre des QR code sur l'outil qui mene à la page pour saisir les heures de l'outil.

### Guideline commit

[Conventionnal commit](https://www.conventionalcommits.org/en/v1.0.0/)

- build: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
- ci: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
- docs: Documentation only changes
- feat: A new feature
- fix: A bug fix
- perf: A code change that improves performance
- refactor: A code change that neither fixes a bug nor adds a feature
- style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- test: Adding missing tests or correcting existing tests

## Log avec rich

Pour avoir des beaux logs
<https://rich.readthedocs.io/en/stable/logging.html>
