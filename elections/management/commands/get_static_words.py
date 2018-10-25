from django.core.management.base import BaseCommand
from rows import import_from_csv
import os
from elections.service import ElectionService


class Command(BaseCommand):
    help = 'get_static_words'

    def handle(self, *args, **options):
        for file in os.listdir('elections/assets/words/'):
            data = import_from_csv('elections/assets/words/' + file)
            name = file.split(' - ')[-1]
            name = name.replace('.csv', '')
            c = ElectionService.get_candidate_by_name(name)
            if c and c.id in [4, 22, 9, 20, 19, 8, 14, 21]:
                print(c)
                for line in data:
                    try:
                        # if line.size_ano > 0:
                        #     ElectionService.process_and_save_word(c, line.ano, line.size_ano, 'today 1-y')
                        if line.size_mes > 0 and line.size_mes > 2:
                            ElectionService.process_and_save_word(c, line.mes, line.size_mes, 'today 1-m')
                    except TypeError:
                        pass


