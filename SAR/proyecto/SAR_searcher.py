import pickle
import sys

def processQuery(index, query):
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


# Process arguments
if len(sys.argv) != 2:
    print("Usage: python SAR_searcher.py index_file")
    exit(-1)
index_file = sys.argv[1]

# Retrieve data from file
with open(index_file, "rb") as f:
    (index, docIndex) = pickle.load(f)

# Infinite query loop (end with '')
query = input("Your query > ")
while query != '':
    wordlist = query.lower().split()
    print(len(processQuery(index, wordlist)))
    query = input("Your query > ")

print("The program will now end.")
