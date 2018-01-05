import os
import re
from unicodedata import normalize

import requests
import enchant
from googletrans import Translator

# based on scripts at https://github.com/tdomhan/pyquizlet
filename = '/Users/alexhooker/Dropbox/Public/notes/french words dictionary.txt'

d = enchant.Dict('fr_FR')

vocab = {}

def checka(prev_w):
    preceders = ['qui', 'il', 'on', 'y', 'en', 'm', 't']
    if prev_w in preceders:
        return 'a'
    return 'à'

def add_accents(phr):
    output = []
    words = normalize('NFKD',phr).split(' ')
    for i, w in enumerate(words):
        if w:
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

def translate(text):
    translator = Translator()
    if type(text)==str:
        return translator.translate(text, src='fr', dest='en').text
    elif type(text)==list:
        return [w.text for w in translator.translate(text, src='fr', dest='en')]

def get_quizlet_list():
    api_key = os.environ['QUIZLET_API']
    params = {'client_id': api_key}
    api_base = 'https://api.quizlet.com/2.0/'
    r = requests.get(api_base + 'sets/5219389', params=params)
    term_dicts = r.json()['terms']
    phrs = [re.sub(':','',d['term']).lower() for d in term_dicts]
    ids = [int(d['id']) for d in term_dicts]
    defs = [d['definition'] for d in term_dicts]
    return phrs, ids, defs

if __name__ == '__main__':
    new_defs = []
    with open(filename, 'r') as f:
        for line in f:
            defs = line.rstrip('\n').split(': ')
            if len(defs) > 1:
                phrase, meaning = defs
                vocab[add_accents(phrase.lower())] = meaning
            else:
                phrase = add_accents(re.sub(':', '', defs[0])).lower()
                meaning = translate(phrase)
                new_defs.append((phrase, meaning))
                print(phrase, meaning)
                vocab[phrase] = meaning
    sorted_vocab = sorted([w for w in vocab], 
                          key=lambda w: normalize('NFD', w).encode('ascii', 'ignore').decode())
    with open(filename, 'w') as f:
        for v in sorted_vocab:
            f.write('{}: {}\n'.format(v, vocab[v]))

    print('New definitions:', new_defs)

    quizlet_phrs, quizlet_ids, quizlet_defs = get_quizlet_list()
    start_id = max(quizlet_ids) + 1
    new_phrs = [phr for phr in vocab.keys() if phr not in quizlet_phrs]
    token = os.environ['QUIZLET_ACCESS']
    for phr in new_phrs:
        headers = {'Authorization': 'Bearer {}'.format(token)}
        params = {'term': phr,
                  'definition':vocab[phr]}
        r = requests.post('https://api.quizlet.com/2.0/sets/5219389/terms',
                          headers=headers, params=params)


