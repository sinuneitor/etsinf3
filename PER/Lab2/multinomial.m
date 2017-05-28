#!/usr/bin/octave -qf

e = 0;
# Parameter processing
if (nargin < 1)
    printf("Usage: multinomial.m <data_filename> [<epsilon>]");
    exit(1)
end
if (nargin > 1)
#    disp(argv(){2})
    e = double(argv(){2});
end
#disp(argv(){1})
load(argv(){1});

# Split data: 90% training, 10% test
[nrows, ncols] = size(data);
rand("seed", 23);
perm = randperm(nrows);
pdata = data(perm,:);
trper = 0.9;
ntr = floor(nrows * trper);
nte = nrows - ntr;

# Split training and test into labels and data
trlabels = pdata(1:ntr,ncols);
trdata = pdata(1:ntr,1:ncols-1);
telabels = pdata(ntr+1:nrows,ncols);
tedata = pdata(ntr+1:nrows,1:ncols-1);

# Numbers of rows for each class
hrows = find(trlabels==0);
srows = find(trlabels==1);

# Probability of encountering a spam or ham mail
ph = size(hrows)(1,1) / ntr;
ps = size(srows)(1,1) / ntr;

# Vectors of probability of ham and spam
Ph = sum(trdata(hrows,:)) / sum(sum(trdata(hrows,:)));
Ps = sum(trdata(srows,:)) / sum(sum(trdata(srows,:)));

# Laplace smoothening
if (e != 0)
    e = 0.0001;
    Ph = (Ph + e) / sum(Ph + e);
    Ps = (Ps + e) / sum(Ps + e);
end

# Parameters for the linear clasifier
wh = log(Ph);
ws = log(Ps);
wh0 = log(ph);
ws0 = log(ps);

# Probability vectors for each class (vector for each mail/row in te)
gh = tedata * wh' + wh0;
gs = tedata * ws' + ws0;

# Vector with the experimental class compared with the real class
# In this vector, 0 means misclassification and 1 correct class
aux = telabels == (gs > gh);
# Number of errors
errors = size(find(aux==0))(1,1);

# Display percentage of errors
disp(errors / nte);
exit(0);
