from nltk.corpus import cess_esp
from nltk.probability import *

fdist = FreqDist(cess_esp.words(cess_esp.fileids()[0]))
print([w for w,f in fdist.most_common()])
