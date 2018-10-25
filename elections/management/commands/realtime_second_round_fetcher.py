from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from elections.models import Candidate
from difflib import SequenceMatcher
import requests

real_time = 'http://trends-cms.appspot.com/api/fetchers/agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgIColdLCCQw/view/ww-BR'


class Command(BaseCommand):
    help = 'realtime_size_fetchers'

    def real_time_fetcher(self):
        try:
            response = requests.get(real_time)
            response = response.json()
            labels = [topic['label'] for topic in response['topics']]
            result = response['result'][-1]
            time = int(result['time'])
            date = datetime.fromtimestamp(time).date()
            for label, value in zip(labels, result['value']):
                try:
                    c = None
                    cs = Candidate.objects.all()
                    s = [SequenceMatcher(None, candidate.name, label).ratio() for candidate in cs]
                    if max(s) > 0.7 or c:
                        if not c:
                            c = cs[s.index(max(s))]
                        c.size = value
                        c.save()
                        print(c.name, date, value)
                    else:
                        print('Não encontrou o candidato', label, value)
                except (CommandError, Exception) as e:
                    print(e)
                    pass
        except (CommandError, Exception) as e:
            print(e)
            pass

    def handle(self, *args, **options):
        self.real_time_fetcher()



