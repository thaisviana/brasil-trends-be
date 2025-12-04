from django.core.management.base import BaseCommand
from elections.models import Candidate
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with initial candidates'

    def handle(self, *args, **options):
        candidates_2022 = [
            {"name": "Simone Tebet", "color": "#1F77B4", "election_year": 2022},
            {"name": "Ciro Gomes", "color": "#FF7F0E", "election_year": 2022},
            {"name": "Soraya Thronicke", "color": "#2CA02C", "election_year": 2022},
            {"name": "Felipe D'Avila", "color": "#D62728", "election_year": 2022},
            {"name": "Padre Kelmon", "color": "#9467BD", "election_year": 2022},
            {"name": "Léo Péricles", "color": "#8C564B", "election_year": 2022},
            {"name": "Sofia Manzano", "color": "#E377C2", "election_year": 2022},
            {"name": "Vera", "color": "#7F7F7F", "election_year": 2022},
            {"name": "Constituinte Eymael", "color": "#BCBD22", "election_year": 2022},
            {"name": "Lula", "color": "#FF0000", "election_year": 2022, "second_round": True},
            {"name": "Jair Bolsonaro", "color": "#800000", "election_year": 2022, "second_round": True}
        ]

        for data in candidates_2022:
            candidate, created = Candidate.objects.get_or_create(
                name=data["name"],
                defaults={
                    "slug": slugify(data["name"]),
                    "color": data["color"],
                    "active": True,
                    "election_year": data["election_year"],
                    "second_round": data.get("second_round", False)
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created candidate: {candidate.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Candidate already exists: {candidate.name}'))
