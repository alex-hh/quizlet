import os
import re
import argparse

from unicodedata import normalize

from quizlet_interface import QuizletUpdater

# based on scripts at https://github.com/tdomhan/pyquizlet
filename = '/Users/alexhooker/Dropbox/Public/notes/french words dictionary.txt'

# 236321717 constructions
# 282610606
#282610676
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument("text_file", help="Name of the file where definitions are stored",)
    # parser.add_argument("username")
    parser.add_argument("--full_set", default=5219389) # 
    parser.add_argument("--keep_text", action="store_false")
    parser.add_argument("--split_quizlet", help="save to separate quizlet sets by word type", action="store_true")
    # parser.add_argument("--words_set", help="quizlet id of words set", default=None)
    # parser.add_argument("--phrases_set", help="quizlet id of phrases set", default=None)
    # parser.add_argument("--const_set", help="quizlet id of construction set", default=None)
    parser.add_argument("--translator", help="which translation api to use: google, linguee", default=None)
    parser.add_argument("--split_txt", help="save text files split by phrase type", action="store_true")
    args = parser.parse_args()
    if args.split_quizlet:
        words_set = 282610676
        constructions_set = 236321717
        phrases_set = 282610606
    updater = QuizletUpdater(filename, args.full_set,
                             words_set_id=words_set,
                             phrases_set_id=phrases_set,
                             const_set_id=constructions_set,
                             translator=args.translator,
                             split_txt=args.split_txt) # split_txt will only be True if the arg --split_txt is passed
    updater.update()

    # new_defs = []
    # with open(filename, 'r') as f:
    #     for line in f:
    #         defs = line.rstrip('\n').split(': ')
    #         if len(defs) > 1:
    #             phrase, meaning = defs
    #             vocab[add_accents(phrase.lower())] = meaning
    #         else:
    #             phrase = add_accents(re.sub(':', '', defs[0])).lower()
    #             meaning = translate(phrase)
    #             new_defs.append((phrase, meaning))
    #             print(phrase, meaning)
    #             vocab[phrase] = meaning
    # sorted_vocab = sorted([w for w in vocab], 
    #                       key=lambda w: normalize('NFD', w).encode('ascii', 'ignore').decode())
    # with open(filename, 'w') as f:
    #     for v in sorted_vocab:
    #         f.write('{}: {}\n'.format(v, vocab[v]))

    # print('New definitions:', new_defs)

    # quizlet_phrs, quizlet_ids, quizlet_defs = get_quizlet_list()
    # start_id = max(quizlet_ids) + 1
    # new_phrs = [phr for phr in vocab.keys() if phr not in quizlet_phrs]
    # token = os.environ['QUIZLET_ACCESS']
    # for phr in new_phrs:
    #     headers = {'Authorization': 'Bearer {}'.format(token)}
    #     params = {'term': phr,
    #               'definition':vocab[phr]}
    #     r = requests.post('https://api.quizlet.com/2.0/sets/5219389/terms',
    #                       headers=headers, params=params)


