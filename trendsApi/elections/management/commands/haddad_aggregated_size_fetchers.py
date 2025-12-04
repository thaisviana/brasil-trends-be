from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from elections.models import SizeHistory, Candidate
from difflib import SequenceMatcher
import requests
#SEM HADDAD
old_aggregated_fetchers = 'http://trends-cms.appspot.com/api/fetchers/agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICA7fztCAw/view/ww-BR'

#COM_HADDAD
aggregated_fetchers = 'http://trends-cms.appspot.com/api/fetchers/agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICIy9f4Cww/view/ww-BR'
#'http://trends-cms.appspot.com/api/fetchers/agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICA1ruRCww/view/ww-BR'
#'http://trends-cms.appspot.com/api/fetchers/agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICIy9f4Cww/view/ww-BR'
#'http://trends-cms.appspot.com/api/fetchers/agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICIy9f4Cww/view/ww-BR'

class Command(BaseCommand):
    help = 'haddad_aggregated_size_fetchers'

    def weekly_fetcher(self):
        try:
            response = requests.get(aggregated_fetchers)
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
                            if label == 'Fernando Haddad ':
                                c = cs.filter(id=53).first()
                            # c.size = value
                            # c.save()
                            sh, created = SizeHistory.objects.update_or_create(candidate=c,
                                                                            date=date,
                                                                            haddad_weekly_size=value)
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



