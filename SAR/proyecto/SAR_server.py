import socket
import threading
import re

def getOptions(wordlist):
    no_stopwords = False
    stemming = False
    for arg in wordlist:
        if arg[0] == "-":
            # Option
            if len(arg) > 1 and arg[1] == "-":
                # Long option
                if arg == "--no-stopwords":
                    no_stopwords = True
                elif arg == "--stemming":
                    stemming = True
            else:
                # Short option, check for multiple short options in one arg
                for c in arg:
                    if c == "n":
                        no_stopwords = True
                    elif c == "s":
                        stemming = True
    return (stemming, no_stopwords)


class client_thread(threading.Thread):
    def run(self):
        self.data = self.connection.recv(4096)
        self.query = self.data.decode('utf8').split()
        (self.st, self.sw) = getOptions(list(self.query))
        self.query = " ".join([w for w in self.query if re.match('-', w) == None])
        self.response = responder(self.query, no_stopwords=self.sw, stemming=self.st)
        self.bytessent = self.connection.send(bytes(self.response, "utf8"))
        print(self.query, self.bytessent, self.response.split("\n")[-1])
        self.connection.close()


PORT = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PORT))
s.listen(20)
print("Socket created at localhost:" + str(PORT))

from SAR_searcher_lib import responder

while True:
    (clientsocket, address) = s.accept()
    ct = client_thread()
    ct.connection = clientsocket
    ct.start()

