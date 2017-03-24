from ex5 import tk
from nltk.corpus import stopwords
sw = stopwords.words("spanish")
tk = [w for w in tk if w.lower() not in sw]

