function [E k]=training(name = 'OCR_14x14', b = 0.1, a = 1.0, K = 1000)
    load(strcat('data/', name));
    [N, L] = size(data);
    D = L - 1;
    ll = unique(data(:,L));
    C  = numel(ll);
    rand("seed", 23);
    data = data(randperm(N), :);
    [w, E, k] = perceptron(data(1:round(.7 * N), :), b, a, K);
    save_precision(4);
    save(strcat('res/', name, '_w'), 'w');
    output_precision(2);
endfunction
