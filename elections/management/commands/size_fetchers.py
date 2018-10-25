from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from elections.models import SizeHistory

import requests

APP_SPOT_URL = 'https://trends-cms.appspot.com/api/fetchers/'

weekly_fetchers = [
    {'id': 1, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICA9eL3CAw/view/ww-BR'},
    {'id': 2, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICAzuHSCww/view/ww-BR'},
    {'id': 3, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICAoNKACAw/view/ww-BR'},
    {'id': 4, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICA4O-LCQw/view/ww-BR'},
    {'id': 5, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICA4IuSCgw/view/ww-BR'},
    {'id': 8, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICAiOi0CQw/view/ww-BR'},
    {'id': 9, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICAoNKACgw/view/ww-BR'},
    {'id': 12, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICA0M_9Cww/view/ww-BR'},
    {'id': 14, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICAwN-PCAw/view/ww-BR'},
    {'id': 19, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICA5t2YCgw/view/ww-BR'},
    {'id': 20, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICQk8-wCQw/view/ww-BR'},
    {'id': 21, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICQs4rrCQw/view/ww-BR'},
    {'id': 22, 'url': 'agxzfnRyZW5kcy1jbXNyKwsSCkdyb3VwRXZlbnQYgICAgMCInQoMCxIHRmV0Y2hlchiAgICQk8-wCgw/view/ww-BR'},
]


class Command(BaseCommand):
    help = 'get keywords for candidates'

    def weekly_fetcher(self):
        for fetcher in weekly_fetchers:
            url = APP_SPOT_URL+fetcher['url']
            try:
                response = requests.get(url)
                response = response.json()
                for r in response['result']:
                    if r['value']:
                        date = datetime.fromtimestamp(int(r['time'])).date()

                        sh, created = SizeHistory.objects.update_or_create(date=date,
                                                                    candidate_id=fetcher['id'],
                                                                    weekly_real_size = r['value'][0])
                        print(created, fetcher['id'], date, r['value'][0])
            except (CommandError, Exception) as e:
                print(e)

    def handle(self, *args, **options):
        self.weekly_fetcher()
