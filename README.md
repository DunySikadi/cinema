# Projet Cinema - Gestion de films, auteurs et spectateurs

Application Django pour gérer des films, auteurs et spectateurs avec une interface d'administration et une API REST.

## 📋 Table des matières
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Accès](#-accès)
- [Endpoints API](#-endpoints-api)
  - [Authentification](#authentification)
  - [Auteurs](#auteurs)
  - [Films](#films)
  - [Spectateurs](#spectateurs)
- [Filtres disponibles](#-filtres-disponibles)

## ⚙️ Prérequis

- Docker
- docker-compose
- Authentification JWT
- Clé API TMDb (optionnelle pour l'import de films)

## 🛠️ Installation

1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/DunySikadi/cinema.git
   cd cinema
   ```

2. **Créez un fichier `.env`** :
   ```ini
   # Configuration de base
   SECRET_KEY=votre-secret-key
   TMDB_API_KEY=votre-clé-api-tmdb

   # Configuration PostgreSQL
   POSTGRES_DB=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=votre-password-postgres
   DB_HOST=db
   DB_PORT=5432
   ```

3. **Lancez les conteneurs** :
   ```bash
   docker-compose up -d --build
   ```

4. **Arrêtez les containers Docker** :
   ```bash
   docker-compose down
   ```

5. **Appliquez les migrations** :
   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. **Créez un superutilisateur** :
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

7. **Importez des films depuis TMDb** (optionnel) :
   ```bash
   docker-compose exec web python manage.py import_tmdb --pages=1
   ```

## 🌐 Accès

- **Interface d'administration** : [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **API** : [http://localhost:8000/api/](http://localhost:8000/api/)

## 🔌 Endpoints API

### Authentification

| Méthode | Endpoint                     | Description               |
|---------|------------------------------|---------------------------|
| POST    | `/api/auth/register/`        | S'inscrire               |
| POST    | `/api/auth/login/`           | Se connecter             |
| POST    | `/api/auth/token/refresh/`   | Rafraîchir le token JWT  |
| POST    | `/api/auth/logout/`          | Se déconnecter           |

### Auteurs

| Méthode | Endpoint                     | Description                          |
|---------|------------------------------|--------------------------------------|
| GET     | `/api/auth/authors/`         | Lister les auteurs                  |
| GET     | `/api/auth/authors/<id>/`    | Détails d'un auteur                 |
| PUT     | `/api/auth/authors/<id>/`    | Modifier un auteur                  |
| DELETE  | `/api/auth/authors/<id>/`    | Supprimer un auteur (sans film)     |

### Films

| Méthode | Endpoint                     | Description                          |
|---------|------------------------------|--------------------------------------|
| GET     | `/api/films/`                | Lister tous les films               |
| POST    | `/api/films/`                | Créer un film                      |
| GET     | `/api/films/archived/`       | Lister les films archivés          |
| GET     | `/api/films/<id>/`           | Détails d'un film                  |
| PATCH   | `/api/films/<id>/`           | Modifier un film                   |
| PUT     | `/api/films/<id>/`           | Modifier un film                   |
| DELETE  | `/api/films/<id>/`           | Archiver un film                   |

### Spectateurs

| Méthode | Endpoint                          | Description                          |
|---------|-----------------------------------|--------------------------------------|
| POST    | `/api/auth/ratings/film/`         | Noter un film                       |
| POST    | `/api/auth/ratings/author/`       | Noter un auteur                     |
| GET     | `/api/auth/favorites/`            | Lister les films favoris            |
| POST    | `/api/auth/favorites/`            | Ajouter un film aux favoris         |
| DELETE  | `/api/auth/favorites/<id>/`       | Retirer un film des favoris         |

## 🔍 Filtres disponibles

### Films
- `?status=RELEASED` - Filtrer par statut
- `?is_from_tmdb=true` - Filtrer par source (TMDb ou admin)

### Auteurs
Les utilisateurs sont automatiquement filtrés pour ne montrer que ceux ayant le rôle "Auteur".