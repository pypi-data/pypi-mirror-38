import json
import pkg_resources


class Metadata(object):
    '''
    File metadata.
    '''

    def __init__(self, path, config):
        self.path = path
        self.filename = path.split('/')[-1]
        self.ext = self.filename.split('.')[-1] if '.' in self.filename else ''
        self.config = config


def get_config(path=None, name_override=None):
    if path is None:
        content = json.loads(pkg_resources.resource_string('ernest', 'data/ernest.json'))
    else:
        with open(path, 'r') as f:
            content = json.load(f)
    if name_override:
        content['name'] = name_override
    return content