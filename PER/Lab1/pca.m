function [m, W]=pca(X, k=256)
    n = columns(X);
    m = sum(X')' / n;

    aux = X - m;
    cova = 1/n * aux * aux';
    [V, lambda]=eig(cova);
    [eigval, order]=sort(-diag(lambda)');
    W = V(:,order)(:,1:k);
endfunction
