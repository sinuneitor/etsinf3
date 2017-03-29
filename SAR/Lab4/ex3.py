# Ejercicio 3

# 1 Cargar quijote.txt en una variable en utf8
elquijote = open("../res/quijote.txt", mode="r", encoding="utf8").read()
# 2 Mostrar todos los caracteres empleados
print("2.", sorted(set(list(elquijote))))
# 3 Eliminar simbolos
simbolos = "¡!\"'(),-.:;¿?]" + u"\u00AB" + u"\u00BB"
elquijote = "".join([x for x in elquijote if x not in simbolos])
# 4 Mostrar todos los caracteres empleados
print("4.", sorted(set(list(elquijote))))
# 5 Tokenize y mostrar stats
from nltk.tokenize import word_tokenize
elquijote = word_tokenize
print("5.")
print(len(elquijote), len(set(elquijote)))
print(sorted(set(elquijote))[:10])
print(sorted(set(elquijote))[-10:])
# 6 Mostrar los 20 tokens mas comunes
from nltk.probability import FreqDist
fquijote = FreqDist(elquijote)
print("6.", fquijote.most_common(20))
# 7 Quitar stopwords
from nltk.corpus import stopwords
elquijote = [w for w in elquijote if w.lower() not in stopwords.words("spanish")]
# 8 Mostrar stats
print("8.")
print(len(elquijote), len(set(elquijote)))
print(sorted(set(elquijote))[:10])
print(sorted(set(elquijote))[-10:])
# 9 Mostrar los 20 tokens mas comunes
fquijote = FreqDist(elquijote)
print("9.", fquijote.most_common(20))
# 10 Aplicar snowball stemming
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("spanish")
elquijote = [stemmer.stem(w) for w in elquijote]
# 11 Mostrar stats
print("10.")
print(len(elquijote), len(set(elquijote)))
print(sorted(set(elquijote))[:10])
print(sorted(set(elquijote))[-10:])
# 12 Mostrar los 20 stems mas comunes
fquijote = FreqDist(elquijote)
print("12.", fquijote.most_common(20))

