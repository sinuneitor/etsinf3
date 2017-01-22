function alfaTest(name = 'OCR_14x14', initial = 0.1, step = 10, final = 1000000, k = 200)
    load(strcat('data/', name));
    [N, L] = size(data);
    D = L - 1;
    ll = unique(data(:, L));
    C = numel(ll);
    rand('seed', 23);
    data = data(randperm(N), :);
    NTr = round(.7 * N);
    M = N - NTr;
    te = data(NTr + 1 : N, :);
    printf('#      a   E   k Ete\n');
    printf('#------- --- --- ---\n');
    a = initial;
    while (a < final)
        [w,E,k]=perceptron(data(1:NTr, :), 0.1, a, k);
        rl = zeros(M, 1);
        for n=1:M
            rl(n) = ll(linmach(w, [1 te(n, 1:D)]'));
        end;
        [nerr m] = confus(te(:, L), rl);
        printf('%8.1f %3d %3d %3d\n', a, E, k, nerr);
        a = a * step;
    endwhile
endfunction
