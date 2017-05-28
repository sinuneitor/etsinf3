#!/usr/bin/octave -qf

# Parameter processing
if (nargin < 1)
    printf("Usage: multinomial.m <data_filename> [<epsilon>]");
    exit(1)
end
load(argv(){1});

N_EXPERIMENTS = 30

values = zeros(20, N_EXPERIMENTS);

# Split data: 90% training, 10% test
[nrows, ncols] = size(data);
rand("seed", 23);
trper = 0.9;
ntr = floor(nrows * trper);
nte = nrows - ntr;
a = 1;
while a <= N_EXPERIMENTS
    perm = randperm(nrows);
    pdata = data(perm,:);

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

    # Vectors of probability of ham and spam for each word
    Ph = sum(trdata(hrows,:)) / sum(sum(trdata(hrows,:)));
    Ps = sum(trdata(srows,:)) / sum(sum(trdata(srows,:)));

    i = -20;
    # Laplace smoothening
    while i < 0
        e = 10 ** i;
        wh = log((Ph + e) / sum(Ph + e));
        ws = log((Ps + e) / sum(Ps + e));
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

        values(abs(i), a) = errors / nte;
        i++;
    end
    a++;
end

avg = sum(values, 2) / N_EXPERIMENTS;
dev = sqrt(sum((values - avg) .^ 2, 2) / N_EXPERIMENTS);

for a=1:20
    x = 10 ** (-1 * a);
    e95 = 1.96 * dev(a);
    printf("%e\t%f\t%f\n", x, avg(a), e95);
end
exit(0);
