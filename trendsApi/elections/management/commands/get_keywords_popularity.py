from django.core.management.base import BaseCommand, CommandError
from pytrends.request import TrendReq
from elections.models import Candidate, Word
import time
from pandas import DataFrame
from elections.service import ElectionService


class Command(BaseCommand):
    help = 'get keywords for candidates'

    def get_keywords(self):
        try:
            pytrends = TrendReq(hl='pt-BR', tz=360)
            timeframes = ['now 7-d', 'now 1-d']
            for timeframe in timeframes:
                print('------------------------', timeframe, '--------------------')
                for candidate in Candidate.objects.filter(second_round=True).order_by('?'):
                    Word.objects.filter(candidate=candidate, period=timeframe).update(status=False)
                    kw_list = [candidate.name]
                    print(candidate.name)
                    try:
                        pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo='BR', gprop='')
                        result = DataFrame(data=pytrends.related_queries())
                        if result[candidate.name].top is not None and not result[candidate.name].top.empty:
                            for word, size in zip(result[candidate.name].top['query'], result[candidate.name].top['value']):
                                ElectionService.process_and_save_word(candidate, word, size, timeframe)
                            print('-------------------------')
                            time.sleep(120)
                    except:
                        print('error')
        except CommandError:
            raise

    def handle(self, *args, **options):
        self.get_keywords()
