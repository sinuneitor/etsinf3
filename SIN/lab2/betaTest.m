function betaTest(name = 'OCR_14x14', a = 1.0, initial = 0.1, step = 10, final = 1000000, k = 500)
    load(strcat('data/', name));
    [N, L] = size(data);
    D = L - 1;
    ll = unique(data(:, L));
    C = numel(ll);
    rand('seed', 23);
    data = data(randperm(N), :);
    NTr = round(.7 * N);
    M = N - NTr;
    te = data(NTr +  1 : N, :);
    printf('#      b   E   k Ete\n');
    printf('#------- --- --- ---\n');
    b = initial;
    while (b < final)
        [w, E, k] = perceptron(data(1:NTr, :), b, a, k);
        rl = zeros(M, 1);
        for n = 1:M
            rl(n) = ll(linmach(w, [1 te(n, 1:D)]'));
        end;
        [nerr m] = confus(te(:, L), rl);
        printf('%8.1f %3d %3d %3d\n', b, E, k, nerr);
        b = b * step;
    endwhile
endfunction
