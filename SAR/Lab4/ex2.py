import nltk
nltk.download('brown')
from nltk.corpus import brown
from nltk.probability import FreqDist

res = []
for i in ["what", "when", "where", "who", "why"]:
    aux = []
    for j in brown.categories():
        aux.append(j)
        aux.append(FreqDist(brown.words(categories=j)).get(j, 0))
    res.append(i)
    res.append(aux)
print(res)
