import re
from collections import namedtuple

import redbaron


def get_dotproxy_names(node):
    if isinstance(node, redbaron.DotProxyList):
        return [n.value for n in node.node_list.data if
                isinstance(n, redbaron.NameNode)]
    elif hasattr(node, 'value'):
        return get_dotproxy_names(node.value)
    else:
        return get_dotproxy_names(node.data[0][0])


class PyConstants:
    _typenames = namedtuple('TypeNames', 'strings ascii comment documentable imports')
    typenames = _typenames(**{
        'strings': ['string', 'unicodestring', 'rawstring', 'binarystring',
                    'unicoderawstring', 'binaryrawstring'],
        'ascii': ['string'],
        'comment': ['comment'],
        'documentable': ['def', 'class'],
        'imports': ['import', 'fromimport']
        })
    _regexes = namedtuple('Regexes', 'single_quote triple_quote prefix content')
    regex = _regexes(**{
        'single_quote': re.compile('(?:^([A-Za-z]+)?(\")(?!\"{2}))|((?<!\"{2})\"$)'),
        'triple_quote': re.compile('(?:^([A-Za-z]+)?(\"){3})|(\"{3}$)'),
        'prefix': re.compile('(?:^([A-Za-z]*)(?=[\"\']))'),
        'content': re.compile(
            '(?:^[A-Za-z]*([\'\"]{1,3}))(?P<content>.*?)([\'\"]{1,3})$')
        })


class PyBools:
    @classmethod
    def isdocumentable(cls, node):
        return isinstance(node, (
            redbaron.DefNode, redbaron.ClassNode, redbaron.RedBaron))

    @classmethod
    def isroot(cls, node):
        return isinstance(node, redbaron.RedBaron)

    @classmethod
    def isforbidden(cls, import_name, config):
        exclude = config['imports']['exclude']
        conditional_exclude = config['imports']['conditional_exclude']
        conditional_include = config['imports']['conditional_include']
        if any([x in import_name for x in exclude]):
            return True
        parts = import_name.split('.', 1)
        if len(parts) > 1 and parts[0] in conditional_exclude.keys():
            if any([x == parts[1] for x in conditional_exclude.get(parts[0])]):
                return True
        if len(parts) > 1 and parts[0] in conditional_include.keys():
            if all([x != parts[1] for x in conditional_include.get(parts[0])]):
                return True
        return False
