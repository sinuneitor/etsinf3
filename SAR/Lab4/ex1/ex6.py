from nltk.corpus import cess_esp
from nltk.probability import FreqDist

fdist=FreqDist(cess_esp.words(cess_esp.fileids()[0]))

print([w for w,k in fdist.items() if k>2 and len(w)>7])
