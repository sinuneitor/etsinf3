#!/usr/bin/octave -qf

if (nargin != 7)
    printf("Usage: pcaexp.m <trdata> <trlabels> <tedata> <telabels> <mink> <stepk> <maxk>\n");
    exit(1);
end

# Procesamiento de argumentos
arg_list = argv();
trdata   = arg_list{1};
trlabels = arg_list{2};
tedata   = arg_list{3};
telabels = arg_list{4};
mink     = str2num(arg_list{5});
stepk    = str2num(arg_list{6});
maxk     = str2num(arg_list{7});

# Carga de datos
load(trdata);
load(trlabels);
load(tedata);
load(telabels);

# Cálculo de la matriz de proyección con LDA
# NOTA: al igual que con PCA, se llama una sóla vez
# a LDA y se van empleando las primeras k columnas
# o eigenvectores para la proyección
W = lda(X, xl, maxk);
for k = mink:stepk:maxk
    # Proyección de los datos de entrenamiento y test
    Xr = W(:, 1:k)' * X;
    Yr = W(:, 1:k)' * Y;
    # Cálculo del error e impresión de resultados
    err = knn(Xr, xl, Yr, yl, 1);
    printf("%d\t%.3f\n", k, err);
end
exit
