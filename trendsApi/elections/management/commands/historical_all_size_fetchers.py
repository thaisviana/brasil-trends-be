from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from elections.models import SizeHistory, Candidate
from difflib import SequenceMatcher

import requests

aggregated_fetchers = 'http://trends-cms.appspot.com/api/fetchers/agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgIDQl5zXCAw/view/ww-BR'

class Command(BaseCommand):
    help = 'historical_all_size_fetchers'

    def weekly_fetcher(self):
        return

    def handle(self, *args, **options):
        try:
            response = requests.get(aggregated_fetchers)
            response = response.json()
            labels = [topic['name'] for topic in response['result']['aggregated']['topics']]
            for result in response['result']['aggregated']['result']:
                parts = result['time'].split('-')
                date = datetime(*[int(part) for part in parts])
                if date > datetime(2018, 6, 9):
                    for label, value in zip(labels, result['value']):
                        try:
                            c = None
                            cs = Candidate.objects.all()
                            s = [SequenceMatcher(None, candidate.name, label).ratio() for candidate in cs]
                            if label == 'Lula':
                                c = cs.get(id=1)
                            if max(s) > 0.7 or c:
                                if not c:
                                    c = cs[s.index(max(s))]
                                c.size = value
                                c.save()
                                sh, created = SizeHistory.objects.update_or_create(candidate=c,
                                                                                date=date,
                                                                                weekly_size=value)
                                print(created, c.name, date, value)
                            else:
                                print('Não encontrou o candidato', label, value)
                        except (CommandError, Exception) as e:
                            print(e)
                            pass
        except (CommandError, Exception) as e:
            print(e)
            pass


