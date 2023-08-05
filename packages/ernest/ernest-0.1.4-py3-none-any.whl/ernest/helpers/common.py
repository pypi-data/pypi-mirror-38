import itertools
from collections import OrderedDict


def nodes_stats(nodes):
    sorted_dict = OrderedDict()
    type_stats = {k: len([i for i in g]) for k, g in
                  itertools.groupby(
                      sorted(nodes, key=lambda x: x.type),
                      key=lambda x: x.type)}
    for k in sorted(type_stats.keys()):
        sorted_dict[k] = type_stats[k]
    sorted_dict.update({
        'total': len(nodes)
        })
    return sorted_dict


def pretty(key, value, depth):
    ki = '\t' * depth if depth > 0 else ''
    vi = '\t' * (depth + 1)
    kp = ki + str(key) + ':'
    if isinstance(value, list):
        vp = '\n'.join([vi + str(v) for v in value])
    elif isinstance(value, dict):
        vp = [pretty(k, v, depth + 1) for k, v in value.items()]
        vp = '\n'.join([item for sublist in vp for item in sublist])
    else:
        vp = vi + str(value)
    return kp, vp


def combine(a, b):
    if a is None:
        return b
    if b is None:
        return a
    thetype = type(a)
    if thetype == dict or thetype == OrderedDict:
        keys = set(list(a.keys()) + list(b.keys()))
        c = {k: combine(a.get(k, None), b.get(k, None)) for k in keys}
    elif thetype == list:
        c = sorted(list(set(a + b)))
    else:
        c = a + b
    return c