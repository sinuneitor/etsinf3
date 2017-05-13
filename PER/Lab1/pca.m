function [m, W]=pca(X, k=256)
    # Número de columnas de X es el número de muestras
    n = columns(X);
    # Valor medio para cada dimensión (vector columna)
    m = sum(X')' / n;

    # Cálculo de la matriz de covarianzas
    aux = X - m;
    cova = 1/n * aux * aux';
    # Obtención de los eigenvalues y eigenvectors ordenados según eigenvalue ascendente
    [V, lambda]=eig(cova);
    [eigval, order]=sort(-diag(lambda)');
    # Se devuelven los primeros k eigenvectors
    W = V(:,order)(:,1:k);
endfunction
