import itertools
import os
from collections import OrderedDict
from functools import reduce

from ernest.helpers.common import pretty, combine
from .factories import FileFactory


class Directory(object):
    '''
    A directory.
    '''

    def __init__(self, path, config):
        self.path = path
        self.config = config
        self.files = self._getfiles()

    def _getfiles(self):
        factory = FileFactory(self.config)
        return {k: list(v) for k, v in itertools.groupby(sorted(
            [factory(os.path.join(top, f)) for top, sub, files in os.walk(self.path)
             for f in files], key=lambda x: x.meta.ext), key=lambda x: x.meta.ext)}

    @property
    def stats(self):
        stats = {}
        for k, v in self.files.items():
            stats[k] = reduce(combine, [i.stats for i in v])
            stats[k]['items'] = len(v)
            stats[k] = OrderedDict(sorted(stats[k].items()))
        return OrderedDict(sorted(stats.items()))

    def filter(self, exts):
        content = [item for sublist in
                   [pretty(k, v, 0) for k, v in self.stats.items() if k in exts]
                   for item in sublist]
        return '\n'.join([self.path] + content) + '\n'

    def __repr__(self):
        return self.filter(self.files.keys())
