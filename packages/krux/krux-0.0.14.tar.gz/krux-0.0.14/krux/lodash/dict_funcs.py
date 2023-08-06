# -*- coding:utf-8 -*-

import six

__all__ = ['pick', 'defaults']


def pick(d, keys):
    result = {k: d[k] for k in keys if k in d}
    return result


def defaults(d1, d2, inplace=True):
    result = d1 if inplace else d1.copy()
    for k, v in six.iteritems(d2):
        result.setdefault(k, v)
    return result

