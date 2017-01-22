function [E, k]=final(name = 'OCR_14x14', b = 0.1, a = 1.0)
    load(strcat('data/', name));
    [w, E, k] = perceptron(data, b, a);
    save_precision(4);
    save(strcat('res/', name, '_wfinal'), 'w');
endfunction
