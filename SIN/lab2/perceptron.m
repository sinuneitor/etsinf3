function [w,E,k]=perceptron(data, b, a, K, iw)
    # Init variables
    [N, L] = size(data); # dimensions of
    D      = L - 1;
    labs   = unique(data(:, L)); # unique elements
    C      = numel(labs); # number of elements
    # Fill out empty arguments (nargin = argv.length)
    if (nargin < 5) w = zeros(D + 1, C); else w = iw; end;
    if (nargin < 4) K = 200; end;
    if (nargin < 3) a = 1.0; end;
    if (nargin < 2) b = 0.1; end;
    # Check K times
    for k = 1:K
        E = 0;
        # For each data row
        for n = 1:N
            # Obtain the data vector (without the class)
            xn = [1 data(n, 1:D)]';
            # Obtain the correct class label
            cn = find(labs == data(n, L));
            er = 0;
            # Multiply the weights * data
            g  = w(:, cn)' * xn;
            # Check that no class gets better results
            for c = 1:C;
                # Update the weights of the other class
                if (c != cn && w(:,c)' * xn + b > g)
                    w(:,c) = w(:,c) - a * xn;
                    er = 1;
                end;
            end
            # If any class gets better, update the correct class
            if (er)
                w(:,cn) = w(:,cn) + a * xn;
                E = E + 1;
            end;
        end
        # If there has been no conflict in this iteration, stop
        if (E == 0) break; end;
    end
endfunction
