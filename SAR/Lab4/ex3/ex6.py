from ex5 import tk
from nltk.probability import FreqDist

fd = FreqDist(tk)
print(fd.most_common(20))
