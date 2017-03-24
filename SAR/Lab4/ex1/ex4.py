from nltk.corpus import cess_esp
from nltk.probability import *

firstfile = cess_esp.words(cess_esp.fileids()[0])
fdist = FreqDist(firstfile)
print(fdist.most_common(20))
