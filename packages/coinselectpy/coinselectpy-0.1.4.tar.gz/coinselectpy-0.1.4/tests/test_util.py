def expand(values, indices=None):
    if indices is not None:
        def f(v, idx):
            if type(v) == dict:
                return dict(i=idx, **v)
            if type(v) == int:
                return {'i': idx, 'value': v}
            y = dict(i=idx, **v)
            return y

        return list(map(f, values, range(len(values))))
    else:
        return list(map(lambda x: {'value': x} if type(x) is not dict else x, values))
