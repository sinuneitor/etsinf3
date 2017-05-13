import pickle
import sys

# Process arguments
if len(sys.argv) != 2:
    print("Usage: python SAR_searcher.py index_file")
    exit(-1)
index_file = sys.argv[1]

# Retrieve data from file
with open(index_file, "rb") as f:
    [index, newid2docid] = pickle.load(f)

# Infinite query loop (end with EOF)
while True:
    try:
        query = input("Your query > ")
        if query == '': break

        res = []
        wordlist = query.lower().split()
        prev = wordlist.pop(0)
        res = index[prev]
        while len(wordlist) != 0:
            previ = res
            res = []
            word = wordlist.pop(0)
            wordi = index[word]
            i = j = 0
            while i < len(wordi) and j < len(previ):
                (d1,p1) = wordi[i]
                (d2,p2) = previ[j]
                if d1 > d2:
                    j+=1
                elif d1 < d2:
                    i+=1
                elif p1 > p2:
                    j+=1
                elif p1 < p2:
                    i+=1
                else: res.append((d1, p1))

        print("There are %d news articles with your query" % len(res))
    except EOFError:
        print("The program will now end...")
        break

