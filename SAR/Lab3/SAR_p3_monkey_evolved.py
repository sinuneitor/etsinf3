#! -*- encoding: utf8 -*-
# inspired by Lluís Ulzurrun and Víctor Grau work

"""
3-. El Mono Infinito, parte 2: generador de frases

Alemany Ibor, Sergio
Galindo Jiménez, Carlos Santiago
"""

import sys
import pickle
import random

def load_object(file_name):
    with open(file_name, 'rb') as fh:
        obj = pickle.load(fh)
    return obj

def generate_sentence(file_name):
    aux = load_object(file_name)
    freq = aux[0]
    dic  = aux[1]
    count = 1
    sentence = "$"
    word = "$"
    while (count < 25):
        ran = random.randint(1, freq[word])
        for next_word, next_count in dic[word].items():
            if ran <= next_count:
                word = next_word
                sentence += " " + next_word
                count += 1
                break
            else:
                ran -= next_count
        if word == "$": break
    if count == 25: sentence += " $"
    return sentence


def syntax():
    print ("\n%s indexfilename\n" % sys.argv[0])
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        syntax()
    index = sys.argv[1]
    print(generate_sentence(index))

