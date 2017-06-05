#!/usr/bin/octave -qf

# Parameter processing
if (nargin < 1)
    printf("Usage: multinomial.m <data_filename> [<epsilon-exponent>]");
    exit(1);
end
load(argv(){1});
exponent = -1;
if (nargin > 1)
    exponent = str2num(argv(){2});
end

# Split data: 90% training, 10% test
[ntr, ncols] = size(tr);
[nte, ncols] = size(te);

# Split training and test into labels and data
trlabels = tr(:,ncols);
trdata = tr(:,1:ncols-1);
telabels = te(:,ncols);
tedata = te(:,1:ncols-1);

# Numbers of rows for each class
hrows = find(trlabels==0);
srows = find(trlabels==1);

# Probability of encountering a spam or ham mail
ph = size(hrows)(1,1) / ntr;
ps = size(srows)(1,1) / ntr;

# Vectors of probability of ham and spam for each word
Ph = sum(trdata(hrows,:)) / sum(sum(trdata(hrows,:)));
Ps = sum(trdata(srows,:)) / sum(sum(trdata(srows,:)));

i = -100;
# Laplace smoothening
while exponent != -1 & i < 0
    if (exponent != -1)
        e = 10 ** (-exponent);
        exponent = -1;
    else
        e = 10 ** i;
    end
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

    printf("%.0e\t%f\n", e, errors / nte);
    i++;
end

exit(0);
