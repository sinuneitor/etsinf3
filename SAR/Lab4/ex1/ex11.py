from ex10 import wordlists

import nltk
nltk.download('punkt')

for wl in wordlists.fileids():
    print(wl, " ", len(wordlists.words(wl)), " ", len(set(wordlists.words(wl)))," ", len(wordlists.sents(wl)))
