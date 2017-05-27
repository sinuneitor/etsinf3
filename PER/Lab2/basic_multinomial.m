#!/usr/bin/octave -qf

# Parameter processing
if (nargin != 1)
    printf("Usage: multinomial.m <data_filename>");
    exit(1)
end
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
p_h = size(hrows)(1,1) / ntr;
p_s = size(srows)(1,1) / ntr;

# Vectors of probability of ham and spam
P_h = sum(trdata(hrows,:)) / sum(sum(trdata(hrows,:)));
P_s = sum(trdata(srows,:)) / sum(sum(trdata(srows,:)));


# Parameters for the linear clasifier
w_h = log(P_h);
w_s = log(P_s);
w_h0 = log(p_h);
w_s0 = log(p_s);

# Probability vectors for each class (vector for each mail/row in te)
gh = tedata * w_h' + w_h0;
gs = tedata * w_s' + w_s0;

# Vector with the experimental class compared with the real class
# In this vector, 0 means misclassification and 1 correct class
aux = telabels == (gs > gh);
# Number of errors
errors = size(find(aux==0))(1,1);

# Display percentage of errors
disp(errors / size(tedata)(1,1));
