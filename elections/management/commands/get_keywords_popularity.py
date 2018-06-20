from django.core.management.base import BaseCommand, CommandError
from pytrends.request import TrendReq
from elections.models import Candidate, Word
import time
from pandas import DataFrame


class Command(BaseCommand):
    help = 'get keywords for candidates'

    def handle(self, *args, **options):
        try:
            pytrends = TrendReq(hl='pt-BR',
                                tz=360,
                                proxies={'https': 'https://66.119.180.104:80'})
            timeframes= ['now 7-d', 'now 1-d', 'today 1-m', 'today 2-m',  'today 1-y', ]
            for candidate in Candidate.objects.all()[7:]:
                for timeframe in timeframes[1]:
                    kw_list = [candidate.name]
                    print(candidate.name)
                    pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo='', gprop='')
                    result = DataFrame(data=pytrends.related_queries())
                    for word, size in zip(result[candidate.name].top['query'], result[candidate.name].top['value']):
                        w = Word(candidate=candidate, text=word, size=size, period=timeframe)
                        w.save()
                    print('-------------------------')
                    time.sleep(120)
        except CommandError:
            raise
