from nltk.corpus import cess_esp
from nltk.probability import FreqDist

fdist = FreqDist(cess_esp.words(cess_esp.fileids()[0]))
print("La palabra mas frecuente es ", fdist.max())
