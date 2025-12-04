from django.core.management.base import BaseCommand
from elections.models import Candidate
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with initial candidates'

    def handle(self, *args, **options):
        candidates_data = [
            {"name": "Vera Lúcia", "color": "#FF0000"},
            {"name": "Aldo Rebelo", "color": "#00FF00"},
            {"name": "Ciro Gomes", "color": "#0000FF"},
            {"name": "Fernando Collor", "color": "#FFFF00"},
            {"name": "José Maria Eymael", "color": "#00FFFF"},
            {"name": "Geraldo Alckmin", "color": "#FF00FF"},
            {"name": "Guilherme Boulos", "color": "#C0C0C0"},
            {"name": "Henrique Meirelles", "color": "#808080"},
            {"name": "Jair Bolsonaro", "color": "#800000"},
            {"name": "João Amoêdo", "color": "#808000"},
            {"name": "Levy Fidelix", "color": "#008000"},
            {"name": "Manuela D’Ávila", "color": "#800080"},
            {"name": "Marina Silva", "color": "#008080"},
            {"name": "Paulo Rabello de Castro", "color": "#000080"},
            {"name": "Rodrigo Maia", "color": "#FFA500"},
            {"name": "Álvaro Dias", "color": "#A52A2A"},
            {"name": "Lula", "color": "#FF0000"}, # Added based on service.py logic
            {"name": "Fernando Haddad", "color": "#FF0000"} # Likely needed
        ]

        for data in candidates_data:
            candidate, created = Candidate.objects.get_or_create(
                name=data["name"],
                defaults={
                    "slug": slugify(data["name"]),
                    "color": data["color"],
                    "active": True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created candidate: {candidate.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Candidate already exists: {candidate.name}'))
