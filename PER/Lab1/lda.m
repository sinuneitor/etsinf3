function [W]=lda(X, xl, k=256)
    D = rows(X); # dimensiones
    n = columns(X); # número de muestras
    m = sum(X')' / columns(X); # valor medio para cada dimensión

    # Cálculo de Sb y Sw
    Sb = zeros(D, D);
    Sw = zeros(D, D);
    for c=unique(xl)
        indc = find(xl == c);
        nc = columns(indc);
        xc = sum(X(:,indc)')' / nc;
        Sw += (X(:,indc) - xc) * (X(:,indc) - xc)' / nc;
        Sb += nc * (xc - m) * (xc - m)';
    endfor

    # Encontrar eigenvalues Sb y Sw y devolver los primeros k eigenvectors
    # ordenados por eigenvalue ascendente
    [V, lambda] = eig(Sb, Sw);
    [eigval, order] = sort(-diag(lambda)');
    W = V(:,order)(:,1:k);
endfunction
