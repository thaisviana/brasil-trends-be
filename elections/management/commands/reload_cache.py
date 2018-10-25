import threading

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand
from elections.api.category_radar import get_candidate_categories_percents_weekly, \
    get_candidate_categories_percents_monthly, get_candidate_categories_percents_yearly
from elections.api.category_bar import get_bar_chart_weekly, get_bar_chart_monthly, get_bar_chart_yearly
from elections.api.new_category_radar import get_new_candidate_categories_percents_monthly, \
    get_new_candidate_categories_percents_yearly, \
    get_new_candidate_categories_percents_weekly
APIS_BY_CACHE_KEY = [
    ('yearly_radar', get_candidate_categories_percents_yearly),
    ('monthly_radar', get_candidate_categories_percents_monthly),
    ('weekly_radar', get_candidate_categories_percents_weekly),
    ('new_yearly_radar', get_new_candidate_categories_percents_yearly),
    ('new_monthly_radar', get_new_candidate_categories_percents_monthly),
    ('new_weekly_radar', get_new_candidate_categories_percents_weekly),
    ('yearly_bar', get_bar_chart_yearly),
    ('monthly_bar', get_bar_chart_monthly),
    ('weekly_bar', get_bar_chart_weekly),
]


def _reload_cache(key, function):
    cache.set(key, function(), settings.CACHE_TIME)
    print(key + u" - OK")


def reload_cache():
    # Update cache entries
    print(u"Atualizando %d caches..." % len(APIS_BY_CACHE_KEY))

    for key, function in APIS_BY_CACHE_KEY:
        threading.Thread(target=_reload_cache, kwargs={'key': key, 'function': function}).start()


class Command(BaseCommand):
    """
    Reload all caches to prevent users from missing the cache.
    """
    help = "Reload all caches."

    def handle(self, *args, **options):
        reload_cache()