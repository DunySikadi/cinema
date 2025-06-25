# Projet Cinema - Gestion de films, auteurs et spectateurs

Application Django pour gérer des films, auteurs et spectateurs avec une interface d'administration et une API REST.

## Prérequis

- Docker
- docker-compose
- Clé API TMDb (optionnelle pour l'import de films)

## Installation

1. Clonez le dépôt :
    git clone https://github.com/votre-utilisateur/cinema.git
    cd cinema

2. Créez un fichier `.env` :
    ### Utilisation du package tiers python-decouple pour le Chargement des variables d'environnement
    SECRET_KEY=votre-secret-key
    TMDB_API_KEY=votre-clé-api-tmdb
    POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD= votre-password-postgres
    DB_HOST=db
    DB_PORT=5432

3. Lancez les conteneurs :
    docker-compose up -d --build

4. Arrêtez les containers Docker 
    docker-compose down

5. Appliquez les migrations :
    docker-compose exec web python manage.py migrate

6. Créez un superutilisateur :
    docker-compose exec web python manage.py createsuperuser

7. Importez des films depuis TMDb :
    docker-compose exec web python manage.py import_tmdb --pages=1

## Accès

- Interface d'administration : http://localhost:8000/admin/
- API : http://localhost:8000/api/

## Endpoints API

### Authentification

- POST /api/auth/register/ - S'inscrire
- POST /api/auth/login/ - Se connecter
- POST /api/auth/token/refresh/ - Rafraîchir le token JWT
- POST /api/auth/logout/ - se deconnecter

### Auteurs

- GET /api/auth/authors/ - Lister les auteurs
- GET /api/auth/authors/<id>/ - Détails d'un auteur
- PUT /api/auth/authors/<id>/ - Modifier un auteur
- DELETE /api/auth/authors/<id>/ - Supprimer un auteur sans film

### Films

- GET /api/films/ - Lister tous les films
- POST /api/films/ - Créer un film
- GET /api/films/archived/ - Lister les films archivées
- GET /api/films/<id>/ - Détails d'un film
- PATCH or PUT /api/films/<id>/ - Modifier un film
- DELETE /api/films/<id>/ - Archiver un film

### Spectateur

- POST /api/auth/ratings/film - Noter un film
- POST /api/auth/ratings/author -  Noter un auteur
- GET /api/auth/favorites/ - Lister les films favoris
- POST /api/auth/favorites/ - Ajouter un film aux favoris
- DELETE /api/auth/favorites/<id>/ - Retirer un film des favoris

## Filtres disponibles

### Films
- ?status=RELEASED - Filtrer par statut
- ?is_from_tmdb=true - Filtrer par source (TMDb ou admin)

### Auteurs
Les utilisateurs sont automatiquement filtrés pour ne montrer que ceux ayant le rôle "Auteur".