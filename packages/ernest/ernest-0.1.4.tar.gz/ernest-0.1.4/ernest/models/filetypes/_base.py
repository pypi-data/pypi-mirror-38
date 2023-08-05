from ernest.helpers.common import pretty


class FileItem(object):
    '''
    A generic file type.
    '''
    ext_ = None

    def __init__(self, meta):
        self.meta = meta

    def read(self):
        with open(self.meta.path, 'r') as f:
            return f.read()

    def correct(self, *methods):
        raise NotImplementedError('corrections not implemented for this filetype')

    @property
    def stats(self):
        return {}

    def __repr__(self):
        content = [item for sublist in [pretty(k, v, 0) for k, v in self.stats.items()]
                   for item in sublist]
        return '\n'.join([self.meta.path] + content) + '\n'