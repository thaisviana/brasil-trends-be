from difflib import SequenceMatcher
from elections.models import Word, Candidate
from elections.assets.blacklist import blacklist

qs = ['/m/0dsyzf', '/g/11b7r5bgrp', '/g/12215271', '/g/11g65h1pms', '/m/0bcdmp', '/m/0h_sx', '/g/11gb3ncsl_', '/m/04gc4vp', '/g/120wl4mm', '/m/05ghl4', '/m/047dbx9', '/m/04g5q20', '/m/0b4fnb', '/m/0pc9q']

class ElectionService:

    @classmethod
    def get_candidate_by_name(cls, name):
        cs = Candidate.objects.filter(active=True)
        s = [SequenceMatcher(None, candidate.name.lower(), name).ratio() for candidate in cs]
        s_slug = [SequenceMatcher(None, candidate.slug, name).ratio() for candidate in cs]
        c = None
        if max(s) > 0.7 or c or max(s_slug) > 0.7:
            if not c:
                c = cs[s.index(max(s))]
        return c

    @classmethod
    def replace_special_chars(cls,text):
        text = text.replace('`', '').replace("'", '')
        text = text.replace('ã', 'a').replace('â', 'a').replace('á', 'a')
        text = text.replace('ê', 'e').replace('é', 'e')
        text = text.replace('í', 'i').replace('ú', 'u')
        text = text.replace('õ', 'o').replace('ô', 'o').replace('ó', 'o')
        text = text.replace('.', ' ')
        return text

    def pertain(term, list):
        term = term.lower()
        term = ElectionService.replace_special_chars(term)
        s = [SequenceMatcher(None, item, term).ratio() for item in list]
        if max(s) > 0.85:
            return True
        return False

    @classmethod
    def process_and_save_word(cls, candidate, word, size, timeframe):
        names = []
        for name in candidate.name.split():
            name = ElectionService.replace_special_chars(name)
            names.append(name.lower())
        names.extend(candidate.slug)
        
        diff_ratio = SequenceMatcher(None, candidate.name, word).ratio()
        diff_slug_ratio = SequenceMatcher(None, candidate.slug, word).ratio()

        word = ElectionService.replace_special_chars(word)
        words = list(filter(lambda x: not ElectionService.pertain(x, blacklist)
                                      and not ElectionService.pertain(x, names), word.split(' ')))
        if words and (diff_ratio < 0.85 or diff_slug_ratio < 0.85):
            text = ' '.join(words)
            if len(text.split(' ')) > 1 and not len(text.split(' ')) == 2 \
                    and text.split(' ')[1] not in ['de', 'da', 'do', 'das', 'dos'] \
                    and text in ['de mello', 'de melo', 'de', 'da', 'do', 'das', 'dos']:
                text = text.split(' ')[0]
            original = Word.objects.filter(text=text, candidate=candidate, period=timeframe)
            if original:
                w = original.first()
                w.status = True
                w.size += 5
                w.save()
            else:
                w = Word(candidate=candidate,
                         text=text,
                         query_text=word,
                         size=size,
                         period=timeframe)
                w.save()
                print(word, size)