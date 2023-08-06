from ._common import _verify_attr


def __getattr__(attr):

    _verify_attr(attr)
    return attr
