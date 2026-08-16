# SoftDesk API

Projet réalisé dans le cadre de la formation Développeur d'application Python d'OpenClassrooms.

## Description

SoftDesk API est une API REST développée avec Django Rest Framework permettant de gérer des projets, leurs contributeurs, les problèmes (issues) et les commentaires associés.

L'API utilise une authentification JWT et applique des permissions afin de sécuriser l'accès aux différentes ressources.

---

## Technologies

- Python 3.14
- Django
- Django REST Framework
- Simple JWT
- Pipenv

---

## Installation

### Cloner le dépôt

```bash
git clone <url_du_repo>
```

Puis :

```bash
cd Project10
```

### Installer les dépendances

```bash
pipenv install
```

### Activer l'environnement virtuel

```bash
pipenv shell
```

### Effectuer les migrations

```bash
python manage.py migrate
```

### Lancer le serveur

```bash
python manage.py runserver
```

Le serveur est alors disponible à l'adresse :

```
http://127.0.0.1:8000/
```

---

## Qualité du code

Exécuter Flake8 :

```bash
flake8
```

---

## Auteur

Projet réalisé par Damien Ladoux dans le cadre de la formation OpenClassrooms.