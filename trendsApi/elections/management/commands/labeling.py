from django.core.management.base import BaseCommand, CommandError
from elections.assets.political import persons
from elections.assets.political_party import parties, celebrity_names, ideological_words
from elections.assets.related_people import people, familiar_relationship, biography_words
from elections.assets.medias import medias
from elections.models import Word, Category
from django.db.models import Q
from elections.service import ElectionService
import rows

data = rows.import_from_csv('elections/assets/genero-nomes.csv')
names = [line.first_name.lower() for line in data]


def isPolitical(word):
    all_persons = []
    if word.split(' ')[-1] == '2018':
       word = word[:-5]
    for p in persons:
        all_persons.extend([ElectionService.replace_special_chars(name.lower()) for name in p])
    return ElectionService.pertain(word, all_persons)


def isIdeological(word):
    return ElectionService.pertain(word, parties) \
           or ElectionService.pertain(word, ideological_words)


def isCelebrity(word):
    parts = word.split(' ')
    return parts[0] in names or ElectionService.pertain(word, celebrity_names)


def isBiography(word, slug):
    if ElectionService.pertain(word, familiar_relationship) or ElectionService.pertain(word, biography_words):
        return True
    if people.get(slug.upper()) and word in people[slug.upper()]:
        return True
    return False


def isNews(word):
    return ElectionService.pertain(word, medias)


class Command(BaseCommand):
    help = 'get keywords for candidates'

    def tagging(self):
        words = Word.objects.filter(Q(category__isnull=True) | Q(category_id=2), status=True, candidate__second_round=True)
        print(words.count())
        for word in words:
            if isNews(word.text):
                word.category = Category.objects.get(text='Mídia')
            elif isBiography(word.text, word.candidate.slug):
                word.category = Category.objects.get(text='Biografia')
            elif isIdeological(word.text):
                word.category = Category.objects.get(text='Ideologia')
            elif isPolitical(word.text):
                word.category = Category.objects.get(text='Figuras políticas')
            elif isCelebrity(word.text):
                word.category = Category.objects.get(text='Celebridades')
            else:
                word.category = Category.objects.get(text='Outros')
            print(word.text, word.category, word.candidate)
            word.save()

    def handle(self, *args, **options):
        try:
            self.tagging()
        except CommandError:
            raise
