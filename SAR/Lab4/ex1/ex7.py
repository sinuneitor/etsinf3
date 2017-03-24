from nltk.corpus import cess_esp
from nltk.probability import FreqDist

fdist = FreqDist(cess_esp.words(cess_esp.fileids()[0]))

print([k for w,k in fdist.most_common()])
print("Freq aparicion de la preposicion a ", fdist['a'])
