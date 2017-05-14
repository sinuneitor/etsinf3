import sys
import re
from os import walk
import pickle


# Funciones
def procesarTexto(texto):
    texto = "".join([c if c.isalpha() else " " for c in texto])
    return [w.lower() for w in re.split(delimiter_word, texto)]

def addToIndex(index, key, element):
    aux = index.get(key, [])
    aux.append(element)
    index[key] = aux


# Process arguments
if len(sys.argv) != 3:
    print("Usage: python SAR_indexer.py news_folder index_file")
    exit(-1)
news_folder = sys.argv[1]
index_file = sys.argv[2]

# Scan folder for files
_, _, news_files = next(walk(news_folder), (None, None, []))

# Create regex delimiters
delimiter_word = re.compile("[\n\t ]")  # tab, newline or space
delimiter_text = re.compile("</?TEXT>")  # <TEXT> or </TEXT>
delimiter_cat  = re.compile("</?CATEGORY>")
delimiter_title = re.compile("</?TITLE>")
delimiter_date = re.compile("</?DATE>")
delimiter_noticia = re.compile("</?DOC>")

# Basic dict
indiceInvertido = {}
titleIndex = {}
dateIndex = {}
catIndex = {}

doc2file = {}
docid = 0

# For each file included in the news folder
while len(news_files) > 0:
    # Read file
    path = news_folder + "/" + news_files.pop(0)
    doc2file[docid] = path
    data = open(path).read()
    # Split into news
    news_list = re.split(delimiter_noticia, data)
    pos = 0
    # For each news article in the file
    for news_text in news_list:
        # Skip empty strings
        if news_text in ["", "\n"]:
            continue
        # Extract body text
        noticia = re.split(delimiter_text, news_text)[1]
        # Process text
        palabras = procesarTexto(noticia);
        # For each word of the article
        for word in set(palabras):
            addToIndex(indiceInvertido, word, (docid, pos))
        # Process category
        categoria = re.split(delimiter_cat, news_text)[1]
        for word in set(procesarTexto(categoria)):
            addToIndex(catIndex, word, (docid, pos))
        # Process date
        date = re.split(delimiter_date, news_text)[1]
        addToIndex(dateIndex, word, (docid, pos))
        # Process title
        title = re.split(delimiter_title, news_text)[1]
        for word in set(procesarTexto(title)):
            addToIndex(titleIndex, word, (docid, pos))
        pos += 1
    docid += 1

# Save data to index file

obj = (indiceInvertido, doc2file, titleIndex, catIndex, dateIndex)
with open(index_file, "wb") as f:
    pickle.dump(obj, f)
