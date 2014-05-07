"""Find Python tokens in sources"""


from cStringIO import StringIO
import tokenize


def get_comments(string):
    """Hold equivalent tokens for a tree being rendered"""
    stream = StringIO(string)
    tokens = list(tokenize.generate_tokens(stream.readline))
    comments = [
        (start_line, start_column, string)
        for type_, string, (start_line, start_column), _, _,
        in tokens
        if type_ == tokenize.COMMENT
    ]
    return sorted(comments)