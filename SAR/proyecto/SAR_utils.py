import re

delimiter_noticia = re.compile("<DOC>")
delimiter_text = re.compile("</?TEXT>")
delimiter_title = re.compile("</?TITLE>")
delimiter_word = re.compile("[\n\t ]")
delimiter_cat = re.compile("</?CATEGORY>")
delimiter_date = re.compile("</?DATE>")

class color:
    PURPLE    = "\033[95m"
    CYAN      = "\033[96m"
    DARKCYAN  = "\033[36m"
    BLUE      = "\033[94m"
    GREEN     = "\033[92m"
    YELLOW    = "\033[93m"
    RED       = "\033[91m"
    BOLD      = "\033[1m"
    UNDERLINE = "\033[4m"
    END       = "\033[0m"

class Trie:

    def __init__(self, toAdd=None):
        self.isWord = False
        self.children = {}
        if toAdd != None:
            self.add(toAdd)

    def add(self, word):
        if len(word) == 0:
            self.isWord = True
        else:
            c = word.pop(0)
            if c in self.children:
                self.children[c].add(word)
            else:
                aux = Trie(word)
                self.children[c] = aux

    def find(self, word, ww=None, wildcard="*"):
        if ww == None:
            ww = "".join(word)
        if len(word) == 0:
            return self.allTrue(ww, justOne=wildcard == "?")
        else:
            c = word.pop(0)
            if c in self.children:
                return self.children[c].find(word, ww=ww, wildcard=wildcard)
            else:
                return []

    def allTrue(self, word, justOne=False):
        res = [word] if self.isWord else []
        for c in self.children:
            if justOne and self.children[c].isWord:
                res.append(word + c)
            elif not justOne:
                res.extend(self.children[c].allTrue(word + c))
        return res



def procesarNoticia(texto):
    texto = "".join([c if c.isalpha() or c.isdigit() else " " for c in texto])
    return [w.lower() for w in re.split(delimiter_word, texto)]
