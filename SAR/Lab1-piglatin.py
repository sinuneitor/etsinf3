#!/usr/bin/env python
#! -*- encoding: utf8 -*-

"""
1.- Pig Latin

Nombre Alumno: Alemany Ibor, Sergio

Nombre Alumno: Galindo Jiménez, Carlos Santiago
"""

import sys


def piglatin_word(word):
    """
    Esta función recibe una palabra en inglés y la traduce a Pig Latin

    :param word: la palabra que se debe pasar a Pig Latin
    :return: la palabra traducida
    """
    if not word[0].isalpha():
        return word

    ending = ''
    if word[len(word) - 1] in (',', '.', '!', '?', ';'):
        ending = word[len(word) - 1]
        word = word[0:len(word) - 1]

    isupper = 'no'
    if word.isupper():
        isupper = 'all'
    elif word[0].isupper():
        isupper = 'first'

    word = word.lower()
    consonante = False
    i = 0

    while i < len(word) and word[i] not in ('a', 'e', 'i', 'o', 'u', 'y'):
        i += 1
        consonante = True

    if not consonante:
        word += 'y'
    else:
        word = word[i:] + word[0:i]

    word += 'ay'

    if isupper == 'all':
        word = word.upper()
    elif isupper == 'first':
        word = word[0].upper() + word[1:]
    return word + ending


def piglatin_sentence(sentence):
    """
    Esta función recibe una frase en inglés i la traduce a Pig Latin

    :param sentence: la frase que se debe pasar a Pig Latin
    :return: la frase traducida
    """
    lista = []
    for word in sentence.split():
        lista.append(piglatin_word(word))
    sentence = " ".join(lista)
    return  sentence


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Usage: python Lab1-piglatin.py -f [filenames]")
        print("\tOr python Lab1-piglatin.py [text]")
        exit()

    if len(sys.argv) > 2 and sys.argv[1] == '-f':
        for filename in sys.argv[2:]:
            print(filename)
            if not filename.endswith('.txt'): continue
            print("processing ", filename)
            infile  = open(filename, 'r').read()
            outfile = open(filename[:-4] + "_piglatin.txt", 'w')
            for line in infile.split('\n'):
                outfile.write(piglatin_sentence(line) + '\n')
            outfile.close()
    elif len(sys.argv) > 1:
        print (piglatin_sentence(sys.argv[1]))
    else:
        for line in sys.stdin:
            print (piglatin_sentence(line))
