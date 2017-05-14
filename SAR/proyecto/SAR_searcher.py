import pickle
import sys
import re
import time
from SAR_utils import *

def ANDpostinglist(posting_lists):
    res = posting_lists.pop(0)
    while len(posting_lists) > 0:
        l1 = res
        l2 = posting_lists.pop(0)
        res = []
        x = y = 0
        while x < len(l1) and y < len(l2):
            (d1, p1) = l1[x]
            (d2, p2) = l2[y]
            if d1 > d2:
                y += 1
            elif d1 < d2:
                x += 1
            elif p1 > p2:
                y += 1
            elif p1 < p2:
                x += 1
            else:
                res.append((d1, p1))
                x += 1
                y += 1
    return res

def processQuery(index, query):
    # Get all posting lists for each word of the query
    pLists = [index.get(word, []) for word in query]
    # Sort posting lists by size (smallest first)
    pLists = sorted(pLists, key=len)
    # Compare all lists, 2 by 2 from smallest to largest
    # using the basic algorithm from theory
    return ANDpostinglist(pLists)

#def processBinaryQuery(index, query):


def snippet(text, wordlist):
    words = procesarNoticia(text);
    #words = re.split(delimiter_word,text)
    snippet = ""
    for i in range(0,len(words)):
        word = words[i]
        if word in wordlist:
            snippet = snippet + "..."
            for j in range(max(0,i-3),min(len(words),i+4)):
                snippet = snippet + words[j] + " "
            snippet = snippet + "...\n"
    return snippet

# Process arguments
if len(sys.argv) < 2:
    print("Usage: python SAR_searcher.py index_file")
    exit(-1)
index_file = sys.argv[1]

# Retrieve data from file
with open(index_file, "rb") as f:
    (index, docIndex, titleIndex, catIndex, dateIndex) = pickle.load(f)

# Infinite query loop (end with '')
print("TIP: you can write " + color.BOLD + "!!" + color.END + " to insert your previous query")
prev = ""
query = input("Your query > ")
while query != '':
    start_time = time.time()
    query = query.replace("!!", prev)
    prev = query
    wordlist = query.lower().split()
    res = processQuery(index, wordlist)
    dant = -1
#    print(res)
    cont = 0
    for (d,p) in res:
        if(cont>9):
            continue
        if dant != d:
            data = open(docIndex.get(d)).read()
            dant = d
        print("Fichero " + docIndex.get(d))
        news_list = re.split(delimiter_noticia, data)
        new = news_list[p+1]
        title = re.split(delimiter_title,new)
        #print(title)
        if len(title)>1:
            print(title[1])
            cont+=1
        if len(res)<3:
            text = re.split(delimiter_text,new)[1]
            for word in wordlist:
                text = re.sub(word, color.UNDERLINE + word + color.END, text, flags=re.IGNORECASE)
            if len (title)>1:
                print(text)
        elif len(res)<6:
            text = re.split(delimiter_text,new)
            toprint = snippet(text[1], wordlist)
            for word in wordlist:
                toprint = re.sub(word, color.UNDERLINE + word + color.END, toprint, flags=re.IGNORECASE)
            print(snippet(text[1], wordlist))

    total_time = time.time() - start_time
    print((color.BOLD + "%d resultados" + color.END + " obtenidos en %.9f segundos") % (len(res), total_time))

    query = input("Your query > ")

print("The program will now end.")
