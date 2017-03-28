function [W]=lda(X, xl, k=256)
    D = rows(X);
    n = columns(X);
    m = sum(X')' / columns(X);

    # Compute Sb and Sw
    Sb = zeros(D, D);
    Sw = zeros(D, D);
    for c=unique(xl)
        indc = find(xl == c);
        nc = columns(indc);
        xc = sum(X(:,indc)')' / nc;
        cova = zeros(size(Sb));
        for i=indc
            cova += (X(:,i) - xc) * (X(:,i) - xc)';
        endfor
        Sw += cova / nc;
        Sb += nc * (xc - m) * (xc - m)';
    endfor

    # Encontrar eigenvalues Sb y Sw y devolver los primeros k eigenvectors
    [V, lambda] = eig(Sb, Sw);
    [eigval, order] = sort(-diag(lambda)');
    W = V(:,order)(:,1:k);
endfunction
