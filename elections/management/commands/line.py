from django.core.management.base import BaseCommand, CommandError
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from elections.models import Candidate, SizeHistory
import matplotlib.patches as mpatches
from itertools import groupby


class Command(BaseCommand):
    help = 'get keywords for candidates'

    def handle(self, *args, **options):

        """""Filtado por cada candidato"""

        colors = ['b-', 'g-', 'r-', 'c-', 'b-', 'g-', 'r-', 'c-', 'm-', 'y-', 'k-', 'b--', 'g--', 'r--', 'c--', 'm--',
                  'y--', 'k--', ]
        name_colors = {
            'b-': ('blue', 'solid'),
            'g-': ('green', 'solid'),
            'r-': ('red', 'solid'),
            'c-': ('cyan', 'solid'),
            'm-': ('magenta', 'solid'),
            'y-': ('yellow', 'solid'),
            'k-': ('black', 'solid'),
            'b--': ('blue', 'dashed'),
            'g--': ('green', 'dashed'),
            'r--': ('red', 'dashed'),
            'c--': ('cyan', 'dashed'),
            'm--': ('magenta', 'dashed'),
            'y--': ('yellow', 'dashed'),
            'k--': ('black', 'dashed'),
        }
        handles = []

        #######################
        for c in Candidate.objects.all():
            range = datetime.now() - timedelta(days=9)
            shs = SizeHistory.objects.filter(candidate=c, date__gte=range, date__date__lt=datetime.now().date()). \
                values('date', 'weekly_size') \
                .order_by('date') \
                .distinct('date')
            groups = []
            for k, g in groupby(shs, lambda x: x['date'].date()):
                date = g.__next__()['date']
                percent = sum(map(lambda x: 0 if not x['weekly_size'] else x['weekly_size'], g))
                groups.append(percent if percent < 100 else 100)

            t = np.arange(0, len(groups), 1)
            color = colors.pop()
            plt.plot(t, list(groups), color)
            handles.append(mpatches.Patch(color=name_colors[color][0],
                                           linestyle=name_colors[color][1],
                                              label=c.slug))

        plt.legend(handles=handles)
        plt.xlabel('dias')
        plt.ylabel('valor')
        plt.title('Agregado: Mensal (Julho)')
        plt.grid(False)
        plt.savefig("test.png")
        plt.show()
