from ex7 import tk as palabras
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("spanish")
palabras = [stemmer.stem(w) for w in palabras]
