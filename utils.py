import re
import enchant
from unicodedata import normalize

def checka(prev_w):
    preceders = ['qui', 'il', 'on', 'y', 'en', 'm', 't']
    if prev_w in preceders:
        return 'a'
    return 'à'

def add_accents(phr, lang='fr'):
    if lang=='fr':
        dict_lang = 'fr_FR'
    elif lang=='es':
        dict_lang = 'es_ES'
    d = enchant.Dict(dict_lang)
    output = []
    words = normalize('NFKD',phr).split(' ')
    for i, w in enumerate(words):
        if w:
            if lang=='fr':
                if w == 'a':
                    output.append(checka(words[i-1]))
            elif d.check(w):
                output.append(w)
            else:
                wout = w
                suggestions = d.suggest(w)
                unaccented_suggestions = [normalize('NFD', s).encode('ascii', 'ignore').decode() for s in suggestions]
                for sugg, poss_match in zip(suggestions, unaccented_suggestions):
                    if poss_match == w:
                        wout = sugg
                        break
                output.append(wout)
    return ' '.join(output)

def is_word(string):
    word_list = string.split(' ')
    if len(word_list) <= 1:
      return True
    if len(word_list) == 2 and word_list[0] in ['se', 'un', 'une', 'le', 'la', 'les']:
      return True
    return False

def is_construction(string):
    return bool(re.search('\.\.\.|\.\.|\+', string))

def filter_phrases(phrase_list, filt):
    if filt is None:
      return phrase_list
    elif filt == 'constructions':
      return [phr for phr in phrase_list if is_construction(phr)]
    elif filt == 'phrases':
      phrases = []
      for phr in phrase_list:
        if not (is_construction(phr) or is_word(phr)):
          phrases.append(phr)
      return phrases
    elif filt == 'words':
      return [phr for phr in phrase_list if\
              is_word(phr) and (not is_construction(phr))]