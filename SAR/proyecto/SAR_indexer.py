import sys
import re
from os import walk
import pickle
from SAR_utils import *

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

# Basic dict
indiceInvertido = {}
titleIndex = {}
dateIndex = {}
catIndex = {}

doc2file = {}
docid = 0

total = 0
# For each file included in the news folder
while len(news_files) > 0:
    # Read file
    path = news_folder + "/" + news_files.pop(0)
    doc2file[docid] = path
    data = open(path).read()
    # Split into news
    news_list = re.split(delimiter_noticia, data)
    total += len(news_list)
    pos = 0
    # For each news article in the file
    for news_text in news_list:
        # Skip empty strings
        if news_text in ["", "\n"]:
            continue
        # Extract body text
        noticia = re.split(delimiter_text, news_text)[1]
        # Process text
        palabras = procesarNoticia(noticia);
        # For each word of the article
        for word in set(palabras):
            addToIndex(indiceInvertido, word, (docid, pos))
        # Process category
        categoria = re.split(delimiter_cat, news_text)[1]
        for word in set(procesarNoticia(categoria)):
            addToIndex(catIndex, word, (docid, pos))
        # Process date
        date = re.split(delimiter_date, news_text)[1]
        addToIndex(dateIndex, word, (docid, pos))
        # Process title
        title = re.split(delimiter_title, news_text)[1]
        for word in set(procesarNoticia(title)):
            addToIndex(titleIndex, word, (docid, pos))
        pos += 1
    docid += 1

print("Se han leído %d archivos conteniendo %d noticias" % (docid, total))

# Save data to index file

obj = (indiceInvertido, doc2file, titleIndex, catIndex, dateIndex)
with open(index_file, "wb") as f:
    pickle.dump(obj, f)
