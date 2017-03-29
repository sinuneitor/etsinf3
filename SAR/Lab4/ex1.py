# Exercise 1

# 1
from nltk.corpus import cess_esp
# 2
print("2.", len(cess_esp.words()))
# 3
print("3.", len(cess_esp.sents()))
# 4
from nltk.probability import FreqDist
first_file = cess_esp.fileids()[0]
cess_freq0 = FreqDist(cess_esp.words(first_file))
print("4.", cess_freq0.most_common(20))
# 5
print("5.", [w for w,k in cess_freq0.most_common()])
# 6
print("6.", [w for w,k in cess_freq0.items() if len(w) > 7 and k > 2])
# 7
print("7.", [k for w,k in cess_freq0.most_common()])
print("7b. Freq de aparición de la preposición a", cess_freq0.get("a", 0))
# 8
print("8. No de palabras que aparecen una sola vez:", len([w for w,k in cess_freq0.items() if k == 1]))
# 9
print("9. La palabra más frecuente es", cess_freq0.max())
# 10
from nltk.corpus import PlaintextCorpusReader
mycorpus = PlaintextCorpusReader("../res/", ".*")
# 11
print("11.")
for doc in mycorpus.fileids():
    print(doc, len(mycorpus.words(doc)), len(set(mycorpus.words(doc))), len(mycorpus.sents(doc)))
