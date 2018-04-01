import os
import re
from unicodedata import normalize

import requests

from utils import add_accents, checka, filter_phrases
from translators import GoogleTranslator

class QuizletUpdater:

  def __init__(self, base_txt_file,
               full_set_id,
               username=None,
               words_set_id=None,
               phrases_set_id=None,
               const_set_id=None,
               split_txt=False,
               translator=None,
               source_lang='fr',
               dest_lang='en',
               verbose=True):
    """
    Args:
     split_txt: Bool, whether to separate vocab into separate quizlet lists by type (word/phrase/construction)
     full_set_id: quizlet id of undifferentiated (base) list
    """
    # TODO choose dictionary based on source_lang
    self.split_txt = split_txt
    self.base_txt_file = base_txt_file
    self.username = username
    self.full_set_id = full_set_id
    self.vocab = {}
    assert translator in [None, 'google', 'linguee'], 'Must specify recognized translator'
    self.translator = translator
    if translator == 'google':
      self.translator = GoogleTranslator(source_lang=source_lang,
                                         dest_lang=dest_lang)
    self.words_set_id = words_set_id
    self.phrases_set_id = phrases_set_id
    self.const_set_id = const_set_id
    self.verbose = verbose
    self.source_lang = source_lang
    self.dest_lang = dest_lang

  def get_user_sets(self):
    api_key = os.environ['QUIZLET_API']
    params = {'client_id': api_key}
    api_base = 'https://api.quizlet.com/2.0/'
    r = requests.get(api_base + 'users/{}/sets'.format(self.username))
    return r

  def get_set_defs(self, set_id):
    api_key = os.environ['QUIZLET_API']
    params = {'client_id': api_key}
    api_base = 'https://api.quizlet.com/2.0/'
    r = requests.get(api_base + 'sets/' + str(set_id), params=params)
    term_dicts = r.json()['terms']
    phrs = [re.sub(':','',d['term']).lower() for d in term_dicts]
    ids = [int(d['id']) for d in term_dicts]
    defs = [d['definition'] for d in term_dicts]
    return phrs, ids, defs

  @staticmethod
  def format_def_list(def_list):
    return '\n'.join(['{}:\t{}'.format(phr, d) for phr,d in def_list])

  def get_vocab(self, write_txt=True):
    self.vocab = {}
    new_defs = []
    untranslated = []
    with open(self.base_txt_file, 'r') as f:
      for line in f:
        # blank space is taken as starting a definition
        defs = line.rstrip('\n').split(': ')
        if len(defs)>2:
          print('Skipping', line)
          continue
        elif len(defs) > 1:
          phrase, meaning = defs
          self.vocab[add_accents(phrase.lower(), self.source_lang)] = meaning
        else:
          phrase = add_accents(re.sub(':', '', defs[0]), self.source_lang).lower()
          if self.translator is not None:
            meaning = self.translator.translate(phrase)
            new_defs.append((phrase, meaning))
            # print(phrase, meaning)
            self.vocab[phrase] = meaning
          else:
            untranslated.append((phrase, ''))
    sorted_vocab = sorted([w for w in self.vocab], 
                          key=lambda w: normalize('NFD', w).encode('ascii', 'ignore').decode())
    print(untranslated)
    if self.verbose:
      print('Newly translated phrases: ', self.format_def_list(new_defs))
      print('Untranslated phrases: ', self.format_def_list(untranslated))
    if write_txt:
      with open(self.base_txt_file, 'w') as f:
        for v in sorted([p for p, d in untranslated], key=lambda w: normalize('NFD', w).encode('ascii', 'ignore').decode()):
          print(v)
          f.write('{}:\n'.format(v))
        for v in sorted_vocab:
          f.write('{}: {}\n'.format(v, self.vocab[v]))

  def update_set(self, set_id, filt=None):
    quizlet_phrs, quizlet_ids, quizlet_defs = self.get_set_defs(set_id)
    start_id = max(quizlet_ids) + 1
    new_phrs = [phr for phr in filter_phrases(self.vocab.keys(), filt) if phr not in quizlet_phrs]
    print('Set {} ({}): {} new definitions added'.format(set_id, filt, len(new_phrs)))
    token = os.environ['QUIZLET_ACCESS']
    for phr in new_phrs:
      headers = {'Authorization': 'Bearer {}'.format(token)}
      params = {'term': phr,
                'definition': self.vocab[phr]}
      r = requests.post('https://api.quizlet.com/2.0/sets/{}/terms'.format(set_id),
                        headers=headers, params=params)

  def update(self, write_txt=True):
    self.get_vocab(write_txt=write_txt)
    set_ids = [self.full_set_id, self.words_set_id, self.phrases_set_id, self.const_set_id]
    set_filters = [None, 'words', 'phrases', 'constructions']
    for sid, filt in zip(set_ids, set_filters):
      if sid is not None:
        self.update_set(sid, filt=filt)
        
    

    