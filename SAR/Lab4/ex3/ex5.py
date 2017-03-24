from ex3 import texto
from nltk.tokenize import word_tokenize
tk = word_tokenize(texto)
print(len(tk), len(set(tk)))
print(sorted(set(tk))[:10])
print(sorted(set(tk))[-10:])
