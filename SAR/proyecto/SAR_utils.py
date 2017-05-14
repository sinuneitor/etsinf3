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

def procesarNoticia(texto):
    texto = "".join([c if c.isalpha() else " " for c in texto])
    return [w.lower() for w in re.split(delimiter_word, texto)]
