import re

import redbaron

from ernest.helpers.py import PyConstants


class PyCorrector(object):
    def __init__(self, config):
        self.config = config
        self.funcmap = {
            'headers': self._header,
            'literal': self._literal_quotes,
            'docstring': self._docstring_quotes,
            'ascii': self._ascii
            }

    def get(self, methods):
        if methods == [0]:
            return self.funcmap.values()
        else:
            return [self.funcmap.get(m, self._invalid) for m in methods]

    def _header(self, pyfile):
        root = pyfile.tree
        nodes = pyfile.header
        name = self.config['name'] or 'a project'
        for node in nodes:
            node.parent.remove(node)
        header = [redbaron.RedBaron(c.format(name) + '\n')[0] for c in
                  self.config['header']]
        for comment in header:
            comment.parent = root
        for i in range(len(header)):
            root.insert(i, header[i])

    def _literal_quotes(self, pyfile):
        nodes = pyfile.string_literals
        self._correct_quotes(nodes)

    def _docstring_quotes(self, pyfile):
        nodes = pyfile.docstrings
        self._correct_quotes(nodes)

    def _ascii(self, pyfile):
        nodes = pyfile.ascii_literals
        preserve_raw = self.config[
            'preserve_raw_strings'
        ] if 'preserve_raw_strings' in self.config.keys() else True
        for node in nodes:
            prefix = PyConstants.regex.prefix.search(node.value)
            if prefix and preserve_raw and 'r' in prefix.group(1):
                new_prefix = 'ur'
            else:
                new_prefix = 'u'
            content = PyConstants.regex.content.search(node.value)
            if content:
                content = content.groupdict().get('content', '')
            else:
                content = ''
            if re.match('^[/].*', content):
                continue
            node.value = PyConstants.regex.prefix.sub(new_prefix, node.value)

    def _invalid(self, pyfile):
        print('Invalid method.')

    def _correct_quotes(self, nodes):
        for node in nodes:
            quoted = self._replace_quotes(node.value)
            try:
                compile(quoted, filename='<ast>', mode='single')
            except SyntaxError:
                quoted = node.value
            node.value = quoted

    @staticmethod
    def _replace_quotes(string):
        # doing re.sub results in weird characters
        single = PyConstants.regex.single_quote.finditer(string)
        for match in single:
            string = string[:match.span()[0]] + "'" + string[match.span()[1]:]
        triple = PyConstants.regex.triple_quote.finditer(string)
        for match in triple:
            string = string[:match.span()[0]] + "'''" + string[match.span()[1]:]
        return string
