"""Module to perceive the contents of python scripts"""

import os
import re
import sys
import token
from fnmatch import fnmatch
from cStringIO import StringIO
from collections import Counter
from tokenize import generate_tokens
from keyword import iskeyword


from stemming.porter2 import stem


def is_lib_module(word):
    if not hasattr(is_lib_module, 'modules'):
        path_to_lib = os.path.join(
            sys.exec_prefix,
            'lib', 'python%s' % sys.version[:3])
        is_lib_module.modules = [
            os.path.splitext(f)[0]
            for f in os.listdir(path_to_lib)
            if fnmatch(f, '*.py')]
    modules = is_lib_module.modules + ['sys']
    return word in modules


def is_python_stem(string):
    """Not a python keyword, but usually used as python"""
    return string in [
        'all',
        'any',
        'argparser',
        'arg',
        'bool',
        'classmethod',
        'cls',
        'cmp',
        'dict',
        'dir',
        'getattr',
        'iter',
        'len',
        'metavar',
        'narg',
        'none',
        'read',
        'self',
        'str',
        'super',
    ]


def is_python_call(string):
    """Common python methods"""
    return string in [
        'basename',
        'dirname',
        'isdir',
        'isfile',
        'islower',
        'ispunct',
        'isspace',
        'isupper',
        'join',
        'list',
        'lower',
        'lstrip',
        'main',
        'next',
        'readline',
        'replace',
        'rstrip',
        'setattr',
        'sort',
        'startswith',
        'strip',
        'trim',
        'var',
        'write',
    ]


def is_programming_stem(string):
    """Words commonly used by programmers"""
    return string in [
        'add',
        'append',
        'arg',
        'argv',
        'ascii',
        'character',
        'diff',
        'file',
        'filename',
        'key',
        'name',
        'one',
        'path',
        'string',
        'two',
        'usage',
        'value',
    ]


def interesting(string):
    if is_lib_module(string):
        return False
    if is_python_stem(string):
        return False
    if is_python_call(string):
        return False
    if is_programming_stem(string):
        return False
    return string not in [
        'the',
        'we',
        'they',
        'to',
        'split',
        'set',
        'sep',
        'result',
        'pop',
    ]


def as_words(string):
    words = []
    for word in string.split('_'):
        if len(word) < 2:
            continue
        elif iskeyword(word):
            continue
        elif word.islower():
            words.append(word)
        elif word[1:].islower():
            words.append(word.lower())
        else:
            strings = re.findall('[A-Z][a-z]+', word)
            lowers = [s.lower() for s in strings]
            words.extend(lowers)
    return words


def interesting_stems(string):
    words = as_words(string)
    stems = [stem(word) for word in words]
    return [word for word in stems if interesting(word)]


def read_text(path):
    with open(path) as stream:
        text = stream.read()
        readline = StringIO(text).readline
        words = []
        for number, value, _, _, _ in generate_tokens(readline):
            if number == token.NAME:
                words.extend(interesting_stems(value))
        return words


def perceive_file(f):
    words = read_text(f)
    return Counter(words)


def directory_scripts(scripts, directory, files):
    scripts.extend([
        os.path.join(directory, f)
        for f in files
        if fnmatch(f, '*.py')])


def collect_scripts(path):
    scripts = []
    os.path.walk(path, directory_scripts, scripts)
    return scripts


def pyrceive_dir(path):
    dir_counter = Counter()
    for script in collect_scripts(path):
        script_counter = perceive_file(script)
        dir_counter.update(script_counter)
    return dir_counter
