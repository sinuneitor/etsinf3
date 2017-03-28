#! -*- encoding: utf8 -*-
# inspired by Lluís Ulzurrun and Víctor Grau work

"""
3-. El Mono Infinito, parte 1: creador del indice

Alemany Ibor, Sergio
Galindo Jiménez, Carlos Santiago
"""

from operator import itemgetter
import re
import sys
import pickle

clean_re = re.compile('\W+')
def clean_text(text):
    return clean_re.sub(' ', text)

def save_object(object, file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)

def sort_dic(d):
    for key, value in sorted(sorted(d.items()), key=itemgetter(1), reverse=True):
        yield key, value

def generate_index(infilename, outfilename):
    doc = open(infilename, 'r', encoding='utf8')
    text = doc.read()
    text = text.replace("\n\n",".")
    dic = {}
    freq = {}

    # Analyze the text
    for sentence in text.split('.'):
        sentence = clean_text(sentence.lower())
        if sentence == "": continue
        sentence = "$ " + sentence + " $"
        prev = ""
        for word in sentence.split():
            if prev != "":
                dic[prev] = dic.get(prev,{})
                dic[prev][word] = dic[prev].get(word, 0) + 1
                if word == "$": break
            prev = word
            freq[word] = freq.get(word, 0) + 1

    # Print the results to stdout
    for word, count in sorted(freq.items()):
        print("%s\t%d\t[" % (word, count), end="")
        tmp = count
        for nextword, nextcount in sort_dic(dic[word]):
            print("(%d, '%s')" % (nextcount, nextword), end="")
            tmp -= nextcount
            if tmp != 0: print(", ", end="")
        print("]")

    # Save data to a file
    save_object((freq, dic), outfilename)


def syntax():
    print ("\n%s filename.txt indexfilename\n" % sys.argv[0])
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        syntax()
    name  = sys.argv[1]
    index = sys.argv[2]
    generate_index(name, index)

