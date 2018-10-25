from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from elections.models import SizeHistory, Candidate
from difflib import SequenceMatcher

import requests

#COM LULA
aggregated_fetchers = 'http://trends-cms.appspot.com/api/fetchers/agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICAreC-CQw/view/ww-BR'
#COM HADDAD

class Command(BaseCommand):
    help = 'get historical fetcher'

    def handle(self, *args, **options):
        try:
            response = requests.get(aggregated_fetchers)
            response = response.json()

            topics = response['result']['aggregated']['topics']
            values = response['result']['aggregated']['result']

            labels = [topic['name'] for topic in topics]

            for result in values:
                parts = [int(part) for part in result['time'].split('-')]
                time = datetime(*parts)
                history = SizeHistory.objects.filter(date=time)
                for l, v in zip(labels, result['value']):
                    c = None
                    cs = Candidate.objects.all()
                    s = [SequenceMatcher(None, candidate.name, l).ratio() for candidate in cs]
                    if l == 'Lula':
                        c = cs.get(id=1)
                    if max(s) > 0.7 or c:
                        if not c:
                            c = cs[s.index(max(s))]
                        history = history.filter(candidate=c, date=time)
                        if history:
                            h = history.first()
                            h.yearly_size = v
                        else:
                            h = SizeHistory(candidate=c, date=time, yearly_size=v)
                        h.save()
                    else:
                        print(l, v)
        except (CommandError, Exception) as e:
            print(e)


