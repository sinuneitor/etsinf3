import sys
import re
from os import walk

# Funciones
def procesarNoticia(texto):
	texto = [w.lower() for w in re.split(delimiter_word, texto)]
	aux = []
	for w in texto:
		aux.append("".join([c for c in w if c.isalpha()]))
	return aux


# Treat input and prepare variables
if (len(sys.argv) != 3):
    print("Usage: python SAR_indexer.py news_folder index_file")
    exit(-1)

news_folder = sys.argv[1]
index_file = sys.argv[2]

_, _, news_files = next(walk(news_folder), (None, None, []))

delimiter_word = re.compile("[\n\t ]")
delimiter_text = re.compile("</?TEXT>")
delimiter_noticia = re.compile("</?DOC>")
delimiter_docid = re.compile("</?DOCID>")

indiceInvertido = {}
newtodocmap = {}
docid = 0

# For each file included in the news folder
while len(news_files) > 0:
	# Read file
	data = open(news_folder + "/" + news_files.pop(0)).read()
	# Split into news
	news_list = re.split(delimiter_noticia, data)[1:-2]
	pos = 0
	for news_text in news_list:
		if news_text in ["", "\n"]: continue
		noticia = re.split(delimiter_text, news_text)[1]
		newid = re.split(delimiter_docid, news_text)[1]
		newtodocmap[newid] = (docid, pos)
		for word in procesarNoticia(noticia):
			if word in indiceInvertido:
				indiceInvertido[word].append(newid)
			else:
				indiceInvertido[word] = [newid]
		pos += 1
	docid += 1


# Save data to index file
import pickle
obj = [indiceInvertido, newtodocmap]
with open(index_file, "wb") as f:
	pickle.dump(obj, f)