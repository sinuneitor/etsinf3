import pickle
import re
import time
from SAR_utils import *
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk import downloader

downloader.download('stopwords')

def compareT(a, b):
    (d1, p1) = a
    (d2, p2) = b
    if d1 == d2:
        return p1 - p2
    else:
        return d1 - d2


# Obtain posting list of a word
# If an index i is not specified it will match : patterns and develop stemming
def getPList(word, i=None, stemming=False):
    if i != None:
        return i.get(word, [])


    if ":" in word:
        [where, word] = word.split(":")
        if where == "headline" or where == "h":
            i = titleIndex
        elif where == "date" or where == "d":
            i = dateIndex
        elif where == "category" or where == "c":
            i = catIndex
        else:
            return []
    else:
        i = index

    if "*" in word or "?" in word:
        if "*" in word:
            symbol = "*"
        elif "?" in word:
            symbol = "?"
        else:
            return []
        count = len([x for x, ltr in enumerate(word) if ltr == symbol])
        if count == 1:
            (prefix, suffix) = word.split(symbol)
            pSearch = list(suffix + "$" + prefix)
        elif count == 2:
            (_, pSearch, _) = word.split(symbol)
            pSearch = list(pSearch)
        else:
            return []
        words = permuterm.find(pSearch, wildcard=symbol)
        aux = []
        for e in words:
            s, p = e.split("$")
            aux.append(p + s)
        words = aux
        return ORpostinglist([getPList(x, i=i) for x in words])
    elif stemming:
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
            diff = compareT(l1[x], l2[y])
            if diff > 0:
                y += 1
            elif diff < 0:
                x += 1
            else:
                res.append(l1[x])
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
            diff = compareT(l1[x], l2[y])
            if diff == 0:
                res.append(l1[x])
                x += 1
                y += 1
            elif diff > 0:
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
        diff = compareT(l1[x], l2[y])
        if diff > 0:
            y += 1
        elif diff < 0:
            res.append(l1[x])
            x += 1
        else:
            x += 1
            y += 1
    res.extend(l1[x:])
    return res


# Get posting list for each word in query
def processQuery(query, stemming=False):
    pLists = [getPList(word, stemming=stemming) for word in query]
    # Before ANDing the lists, sort them by ascending length
    return ANDpostinglist(sorted(pLists, key=len))


# Perform a binary operation between two posting lists
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


# Process query that includes OR, AND or NOT operators
def processBinaryQuery(query, stemming=False):
    res = []   # Posting list
    words = [] # Words processed but not queried
    op = None  # Operation processed but not queried

    for w in query:
        if w == "NOT":
            if len(words) != 0:
                processed_words = processQuery(words, stemming=stemming)
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
            processed_words = processQuery(words, stemming=stemming)
            words = []
            res = performBinaryOP(res, processed_words, op)
            op = w
        else:
            words.append(w.lower())
    return performBinaryOP(res, processQuery(words, stemming=stemming), op)


def snippet(text, query):
    words = procesarNoticia(text)
    snippet = ""
    # Check each word of the article
    for i in range(0, len(words)):
        if words[i] in query:
            # Add that word and some context if the word is in the query
            snippet += "..." + " ".join(words[max(0, i - 3):min(len(words), i + 4)]) + "...\n"
    return snippet

def responder(query, no_stopwords=False, stemming=False):
    start_time = time.time()

    # Treat query and obtain posting list of the result
    wordlist = query.split()
    if no_stopwords: # Remove spanish stopwords including *:stopword
        aux = []
        for word in wordlist:
            term = word
            if ":" in word:
                _, term = word.split(":")
            if term.lower() not in stopwords.words('spanish'):
                aux.append(word)
        wordlist = aux
    res = processBinaryQuery(wordlist, stemming=stemming)

    # The query will be used to underline the words in the full text results
    # Stem query words, remove boolean operators and *:* operators
    wordlist = [w.lower() for w in wordlist if w not in ["AND", "OR", "NOT"] and ":" not in w]
    if stemming:
        aux = []
        for word in wordlist:
            aux.extend(stems.get(stemmer.stem(word), []))
        wordlist = aux


    printall = ""
    # Print results
    #     1-2: print the whole article
    #     3-5: snippets
    #     5+ : print first 10 headlines
    dant = -1 # Previous document id
    cont = 0  # Amount of articles printed
    for (d,p) in res:
        # Print only the first 10 results
        if(cont>9):
            break
        # If the docid changes, load the new file
        if dant != d:
            data = open(docIndex.get(d)).read()
            dant = d
        # Print the file in which the article is located
        printall += "Fichero " + docIndex.get(d) + "\n"
        # Obtain article and print title
        article = re.split(delimiter_noticia, data)[p + 1]
        printall += re.split(delimiter_title, article)[1] + "\n"
        cont += 1
        if len(res) <= 2:
            # Print whole article
            text = re.split(delimiter_text, article)[1]
            printall += text + "\n"
        elif len(res) <= 5:
            # Print snippets
            toprint = snippet(re.split(delimiter_text, article)[1], wordlist)
            printall += toprint + "\n"

    # Print number of results and timing
    total_time = time.time() - start_time
    printall += "%d resultados obtenidos en %.9f segundos\n" % (len(res), total_time)
    return printall

print("Loading mini_enero.data...")
# Retrieve data from file
with open("mini_enero.data", "rb") as f:
    (index, docIndex, titleIndex, catIndex, dateIndex, universe, stems, permuterm) = pickle.load(f)
    f.close()
print("Loaded!")
# Prepare variables
stemmer = SnowballStemmer('spanish')
