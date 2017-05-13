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


# Process arguments
if len(sys.argv) != 3:
    print("Usage: python SAR_indexer.py news_folder index_file")
    exit(-1)
news_folder = sys.argv[1]
index_file = sys.argv[2]

# Scan folder for files
_, _, news_files = next(walk(news_folder), (None, None, []))

# Create regex delimiters
delimiter_word = re.compile("[\n\t ]") # tab, newline or space
delimiter_text = re.compile("</?TEXT>") # <TEXT> or </TEXT>
delimiter_noticia = re.compile("</?DOC>")

# Basic dict
indiceInvertido = {}
newid2docid = {}
docid = 0

# For each file included in the news folder
while len(news_files) > 0:
	# Read file
	data = open(news_folder + "/" + news_files.pop(0)).read()
	# Split into news
	news_list = re.split(delimiter_noticia, data)
	pos = 0
	# For each news article in the file
	for news_text in news_list:
		# Skip empty strings
		if news_text in ["", "\n"]: continue
		# Extract body text
		noticia = re.split(delimiter_text, news_text)[1]		
		# For each word of the article
		for word in set(procesarNoticia(noticia)):
			if word in indiceInvertido:
				indiceInvertido[word].append((docid, pos))
			else:
				indiceInvertido[word] = [(docid, pos)]
		pos += 1
	docid += 1


# Save data to index file
import pickle
obj = [indiceInvertido, newid2docid]
with open(index_file, "wb") as f:
	pickle.dump(obj, f)