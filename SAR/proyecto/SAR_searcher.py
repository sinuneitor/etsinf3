import pickle
import sys

def processQuery2(index, query):
    pLists = []
    for word in query:
        pLists.append(index.get(word, []))

    pLists = sorted(pLists, key=len)
    res = pLists.pop(0)
    while len(pLists) > 0:
        l1 = res
        l2 = pLists.pop(0)
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
    prev = query.pop(0)
    res = index.get(prev, [])
    while len(query) != 0:
        previ = res
        res = []
        word = query.pop(0)
        wordi = index.get(word, [])
        i = j = 0
        while i < len(wordi) and j < len(previ):
            (d1, p1) = wordi[i]
            (d2, p2) = previ[j]
            if d1 > d2:
                j += 1
            elif d1 < d2:
                i += 1
            elif p1 > p2:
                j += 1
            elif p1 < p2:
                i += 1
            else:
                res.append((d1, p1))
                i += 1
                j += 1
    return res


# Process arguments
if len(sys.argv) != 2:
    print("Usage: python SAR_searcher.py index_file")
    exit(-1)
index_file = sys.argv[1]

# Retrieve data from file
with open(index_file, "rb") as f:
    index = pickle.load(f)

# Infinite query loop (end with EOF or '')
while True:
    query = input("Your query > ")
    if query == '':
        break
    wordlist = query.lower().split()
    print(len(processQuery(index, wordlist)))

print("The program will now end.")
