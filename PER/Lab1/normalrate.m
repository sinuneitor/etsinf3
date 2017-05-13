#!/usr/bin/octave -qf

load("trlabels.mat.gz");
load("telabels.mat.gz");
load("trdata.mat.gz");
load("tedata.mat.gz");

err = knn(X, xl, Y, yl, 1);

for k=10:10:100
    printf("%d\t%.3f\n", k, err);
end

exit
