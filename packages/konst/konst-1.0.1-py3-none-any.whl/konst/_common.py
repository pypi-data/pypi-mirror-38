def _verify_attr(name):
    if name.startswith('_'):
        raise AttributeError(f'konst does not support leading underscores: {name!r}')
