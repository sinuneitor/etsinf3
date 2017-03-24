from nltk.corpus import PlaintextCorpusReader

corpus_root='/media/windows/Dropbox/ETSINF/3/git/SAR/res/'
wordlists = PlaintextCorpusReader(corpus_root, '.*')
print("Archivos importados: ", wordlists.fileids())
