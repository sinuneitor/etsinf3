from ex10 import palabras
from nltk.probability import FreqDist
print(FreqDist(palabras).most_common(20))
