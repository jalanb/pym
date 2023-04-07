"""Find Python tokens in sources"""


import tokenize

from six import StringIO


def get_comments(string):
    """Hold equivalent tokens for a tree being rendered"""
    stream = StringIO(string)
    tokens = list(tokenize.generate_tokens(stream.readline))
    comments = [
        (start_line, start_column, comment)
        for type_, comment, (start_line, start_column), _, _, in tokens
        if type_ == tokenize.COMMENT
    ]
    return sorted(comments)
