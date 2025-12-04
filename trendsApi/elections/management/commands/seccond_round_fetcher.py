from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from elections.models import SizeHistorySecondRound, Candidate
from difflib import SequenceMatcher
import requests

fetcher = 'http://trends-cms.appspot.com/api/fetchers/agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICo-e3KCgw/view/ww-BR'

"""""MARINA E BOULOS FETCHER:
fetcher = 'http://trends-cms.appspot.com/api/fetchers/agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICo6cTtCww/view/ww-BR'
"""

class Command(BaseCommand):
    help = '2 round'

    def weekly_fetcher(self):
        try:
            response = requests.get(fetcher)
            response = response.json()
            labels = [topic['label'] for topic in response['topics']]
            for result in response['result']:
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
                            sh, created = SizeHistorySecondRound.objects.update_or_create(candidate=c,
                                                                            date=date,
                                                                            size=value)
                            print(sh.id, c.name, date, value)
                        else:
                            print('Não encontrou o candidato', label, value)
                    except (CommandError, Exception) as e:
                        print(e)
                        pass
        except (CommandError, Exception) as e:
            print(e)
            pass

    def handle(self, *args, **options):
        self.weekly_fetcher()



