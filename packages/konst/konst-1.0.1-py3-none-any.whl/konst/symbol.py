from ._common import _verify_attr


class Symbol:
    __slots__ = ('name',)
    _cache = dict()

    def __new__(cls, name):
        self = super().__new__(cls)
        self.name = name
        return cls._cache.setdefault(name, self)

    def __repr__(self):
        return self.name

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise TypeError(f'Symbol {self!r} is immutable, cannot set {attr!r}')
        object.__setattr__(self, attr, value)

    def __delattr__(self, attr):
        raise TypeError(f'Symbol {self!r} is immutable, cannot delete {attr!r}')


def __getattr__(attr):
    _verify_attr(attr)
    return Symbol(attr)
