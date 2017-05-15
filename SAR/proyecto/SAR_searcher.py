import pickle
import sys
import re
import time
from SAR_utils import *
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


def getPList(word, i=None):
    if i != None:
        return i.get(word, [])

    if "*" in word or "?" in word:
        if "*" in word:
            symbol = "*"
        elif "?" in word:
            symbol = "?"
        (prefix, suffix) = word.split(symbol)
        words = permuterm.find(list(suffix + "$" + prefix), wildcard=symbol)
        aux = []
        for e in words:
            s, p = e.split("$")
            aux.append(p + s)
        words = aux
        return ORpostinglist([getPList(x, i=index) for x in words])

    if ":" in word:
        [where, word] = word.split(":")
        if where == "headline":
            i = titleIndex
        elif where == "date":
            i = dateIndex
        elif where == "category":
            i = catIndex
        else:
            return []
    else:
        i = index

    if no_stopwords and word in stopwords.words('spanish'):
        return []
    if stemming:
        aux = [getPList(w, i=i) for w in stems.get(stemmer.stem(word), [])]
        return ORpostinglist(aux)
    else:
        return getPList(word, i=i)

def ANDpostinglist(posting_lists):
    if (len(posting_lists) == 0): return []
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

def ORpostinglist(posting_lists):
    res = []
    for l2 in posting_lists:
        l1 = res
        res = []
        x = y = 0
        while x < len(l1) and y < len(l2):
            (d1, p1) = l1[x]
            (d2, p2) = l2[y]
            if d1 == d2:
                if p1 == p2:
                    res.append(l1[x])
                    x += 1
                    y += 1
                elif p1 > p2:
                    res.append(l2[y])
                    y += 1
                else:
                    res.append(l1[x])
                    x += 1
            elif d1 > d2:
                res.append(l2[y])
                y += 1
            else:
                res.append(l1[x])
                x += 1
        res.extend(l1[x:])
        res.extend(l2[y:])
    return res

def NANDpostinglist(l1, l2):
    res = []
    x = y = 0
    while x < len(l1) and y < len(l2):
        (d1, p1) = l1[x]
        (d2, p2) = l2[y]
        if d1 > d2:
            y += 1
        elif d1 < d2:
            res.append(l1[x])
            x += 1
        elif p1 > p2:
            y += 1
        elif p1 < p2:
            res.append(l1[x])
            x += 1
        else:
            x += 1
            y += 1
    res.extend(l1[x:])
    return res



def processQuery(query):
    pLists = [getPList(word) for word in query]
    pLists = sorted(pLists, key=len)
    return ANDpostinglist(pLists)

def performBinaryOP(list1, list2, op):
    if op == None:
        return list2
    elif op == "AND":
        return ANDpostinglist([list1, list2])
    elif op == "OR":
        return ORpostinglist([list1, list2])
    elif op == "NAND":
        return NANDpostinglist(list1, list2)
    elif op == "NOR":
        return ORpostinglist([list1, NANDpostinglist(universe, list2)])
    elif op == "NOT":
        return NANDpostinglist(universe, list2)

def processBinaryQuery(query):
    res = []
    words = []
    op = None
    for w in query:
        if w == "NOT":
            if len(words) != 0:
                processed_words = processQuery(words)
                words = []
                res = performBinaryOP(res, processed_words, op if op != None else "OR")
                op = "NAND"
            elif op == None:
                op = "NOT"
            elif op == "AND" or op == "NOT":
                op = "NAND"
            elif op == "OR":
                op = "NOR"
        elif w == "OR" or w == "AND":
            processed_words = processQuery(words)
            words = []
            res = performBinaryOP(res, processed_words, op)
            op = w
        else:
            words.append(w.lower())
    processed_words = processQuery(words)
    return performBinaryOP(res, processed_words, op)


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

no_stopwords = False
stemming = False

# Process arguments
if len(sys.argv) < 2:
    print("Usage: python SAR_searcher.py [OPTIONS] index_file")
    print("Options:\n\t--no-stopwords OR -n\tRemove all stopwords\n" +
          "\t--stemming OR -s\tLeave only the stem of the words")
    exit(-1)
for arg in sys.argv:
    if arg[0] == "-":
        if len(arg) > 1 and arg[1] == "-":
            # It's a long parameter
            if arg == "--no-stopwords":
                no_stopwords = True
            elif arg == "--stemming":
                stemming = True
        else:
            # It's a single letter option, scan all letters
            for c in arg:
                if c == "n":
                    no_stopwords = True
                elif c == "s":
                    stemming = True
    else:
        # Not an option, the last nonoption must be the filename
        index_file = arg

print("Iniciando búsqueda interactiva en", index_file, "sin" if no_stopwords else "con", "stopwords y ",
      "con" if stemming else "sin", "stemming")

# Retrieve data from file
with open(index_file, "rb") as f:
    (index, docIndex, titleIndex, catIndex, dateIndex, universe, stems, permuterm) = pickle.load(f)
    f.close()

# Infinite query loop (end with '')
print("Puedes emplear operadores binarios (AND, OR y NOT), búsqueda en campos (headline:, date: y category:).",
      "También puedes emplear comodines ('*' para múltiples caracteres y '?' para uno solo) para buscar con tolerancia.",
      "Por último, puedes emplear !! para denotar tu búsqueda anterior")
prev = ""
stemmer = SnowballStemmer('spanish')
query = input("Your query > ")
while query != '':
    start_time = time.time()
    query = query.replace("!!", prev)
    prev = query
    wordlist = query.split()
    res = processBinaryQuery(wordlist)
    wordlist = [w.lower() for w in wordlist if w not in ["AND", "OR", "NOT"]]
    if stemming:
        aux = []
        for word in wordlist:
            if ":" in word:
                (header, term) = word.split(":")
                aux.extend([header + ":" + x for x in stems.get(stemmer.stem(term), [])])
            else:
                aux.extend(stems.get(stemmer.stem(word), []))
        wordlist = aux

    if no_stopwords:
        aux = []
        for word in wordlist:
            term = word
            if ":" in word:
                (_, term) = word.split(":")
            if term not in stopwords.words('spanish'):
                aux.append(word)
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

    query = input("Tu búsqueda > ")

print("El programa se está cerrando...")
