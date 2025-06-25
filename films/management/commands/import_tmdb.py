import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from films.models import Film
from users.models import User

class Command(BaseCommand):
    """
    Commande personnalisée pour importer des films et leurs réalisateurs depuis l'API TMDb.
    Usage : python manage.py import_tmdb --pages=1
    """
    
    help = 'Import movies and authors from TMDb API'
    
    def add_arguments(self, parser):
        """Définit les arguments optionnels de la commande"""
        parser.add_argument(
            '--pages', 
            type=int, 
            default=1, 
            help='Number of pages to import (20 movies per page)'
        )
    
    def handle(self, *args, **options):
        """Point d'entrée principal de la commande"""
        
        # Vérification de la clé API
        api_key = settings.TMDB_API_KEY
        if not api_key:
            self.stdout.write(self.style.ERROR('TMDB_API_KEY is not set in settings'))
            return

        pages = options['pages']
        base_url = 'https://api.themoviedb.org/3'
        
        # Traitement page par page
        for page in range(1, pages + 1):
            self._process_page(page, api_key, base_url)
    
    def _process_page(self, page, api_key, base_url):
        """Traite une page de résultats de l'API TMDb"""
        try:
            # Récupération des films populaires
            response = requests.get(
                f'{base_url}/movie/popular',
                params={
                    'api_key': api_key,
                    'page': page,
                    'language': 'fr-FR'
                },
                timeout=10  # Ajout d'un timeout pour la requête
            )
            response.raise_for_status()  # Lève une exception pour les codes 4XX/5XX
            movies = response.json().get('results', [])
            for movie_data in movies:
                self._import_movie(movie_data, api_key, base_url)
                
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error fetching page {page}: {str(e)}'))

    def _import_movie(self, movie_data, api_key, base_url):
        """Importe un film spécifique dans la base de données"""
        tmdb_id = movie_data.get('id')
        
        # Vérification des doublons
        if Film.objects.filter(tmdb_id=tmdb_id).exists():
            self.stdout.write(self.style.WARNING(f'Movie {tmdb_id} already exists'))
            return

        try:
            # Récupération des détails complets du film
            details = self._get_movie_details(tmdb_id, api_key, base_url)
            if not details:
                return

            # Récupération des crédits (réalisateurs)
            credits = self._get_movie_credits(tmdb_id, api_key, base_url)
            if not credits:
                return

            # Création des auteurs (réalisateurs)
            authors = self._create_authors(credits)
            
            # Création du film
            self._create_film_record(details, authors, tmdb_id)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing movie {tmdb_id}: {str(e)}'))

    def _get_movie_details(self, tmdb_id, api_key, base_url):
        """Récupère les détails d'un film spécifique"""
        response = requests.get(
            f'{base_url}/movie/{tmdb_id}',
            params={
                'api_key': api_key,
                'language': 'fr-FR'
            },
            timeout=10
        )
        
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'Error fetching details for movie {tmdb_id}'))
            return None
            
        return response.json()

    def _get_movie_credits(self, tmdb_id, api_key, base_url):
        """Récupère les crédits (équipe technique) d'un film"""
        response = requests.get(
            f'{base_url}/movie/{tmdb_id}/credits',
            params={'api_key': api_key},
            timeout=10
        )
        
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'Error fetching credits for movie {tmdb_id}'))
            return None
            
        return response.json()

    def _create_authors(self, credits):
        """Crée ou récupère les auteurs (réalisateurs)"""
        authors = []
        directors = [
            crew for crew in credits.get('crew', []) 
            if crew.get('job') == 'Director'
        ]
        
        for director in directors:
            author, created = User.objects.get_or_create(
                username=f"{director.get('name').replace(" ","_")}",
                defaults={
                    'email': f"{director.get('name').lower().replace(" ","_")}@example.com",
                    'role': User.Role.AUTHOR,
                    'birth_date': None,
                }
            )
            authors.append(author)
        return authors

    def _create_film_record(self, details, authors, tmdb_id):
        """Crée l'enregistrement du film dans la base de données"""        
        # Création du film
        film = Film.objects.create(
            title=details.get('title', 'Sans titre'),
            description=details.get('overview', ''),
            release_date=details.get('release_date'),
            status=details.get('status').replace(' ','_').upper(),
            tmdb_id=tmdb_id,
            is_from_tmdb=True,
        )
        # Association des auteurs
        film.authors.set(authors)
        self.stdout.write(self.style.SUCCESS(f'Imported movie: {film.title}'))