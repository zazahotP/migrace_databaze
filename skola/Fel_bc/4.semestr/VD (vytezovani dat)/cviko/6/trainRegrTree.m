function tree = trainRegrTree( inputs, outputs, splitmin, varargin )
% TRAINREGRTREE Trains a regression tree using the classregtree of
% statistics toolbox. The tree pruning is off.

    tree = classregtree( inputs, outputs, ...
        varargin{:}, ...
        'method', 'regression', ...
        'prune', 'off', ...
        'splitmin', splitmin );

end