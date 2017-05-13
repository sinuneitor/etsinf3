#!/usr/bin/octave -qf

if (nargin != 10)
    printf("Usage: pcaldaexp.m <trdata> <trlabels> <tedata> <telabels> <mink> <stepk> <maxk> <mink> <stepk> <maxk>\n");
    exit(1);
end

arg_list = argv();
trdata   = arg_list{1};
trlabels = arg_list{2};
tedata   = arg_list{3};
telabels = arg_list{4};
pmink     = str2num(arg_list{5});
pstepk    = str2num(arg_list{6});
pmaxk     = str2num(arg_list{7});
lmink     = str2num(arg_list{8});
lstepk    = str2num(arg_list{9});
lmaxk     = str2num(arg_list{10});

load(trdata);
load(trlabels);
load(tedata);
load(telabels);

[m, W] = pca(X, maxk);
for k = mink:stepk:maxk
    Xr = W(:, 1:k)' * (X - m);
    Yr = W(:, 1:k)' * (Y - m);
    err = knn(Xr, xl, Yr, yl, 1);
    printf("%d\t%.3f\n", k, err);
end

W = lda(Xr, xl, maxk);
for k = lmink:lstepk:lmaxk
    Xr = W(:, 1:k)' * X;
    Yr = W(:, 1:k)' * Y;
    err = knn(Xr, xl, Yr, yl, 1);
    printf("%d\t%.3f\n", k, err);
end

exit
