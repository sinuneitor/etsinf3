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

# Obtencion de los eigenvectores
# NOTA: en vez de llamar a PCA a cada iteración
# se llama con el valor máximo y se va accediendo
# a los k primeros (están ordenados)
[m, W] = pca(X, maxk);
for k = mink:stepk:maxk
    # Proyección de datos de entrenamiento y test
    Xr = W(:, 1:k)' * (X - m);
    Yr = W(:, 1:k)' * (Y - m);
    # Cálculo de error e impresión de resultados
    err = knn(Xr, xl, Yr, yl, 1);
    printf("%d\t%.3f\n", k, err);
end

exit
