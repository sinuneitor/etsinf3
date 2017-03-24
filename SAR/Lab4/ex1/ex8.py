from nltk.corpus import cess_esp
from nltk.probability import FreqDist

fdist = FreqDist(cess_esp.words(cess_esp.fileids()[0]))
print("No de palabras que aparecen una sola vez: ", len([w for w,k in fdist.items() if k==1]))
