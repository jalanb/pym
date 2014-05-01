"""Script to render a python file

To itself
"""

import os
import sys
import argparse


import render

# All comments here are montyPythonic, (c) them, used for testing and LOLs

################### From "Army Protection Racket" #############################
# No, no no no no, no, no no no. This is silly.                               #
# What's silly?                                                               #
# No the whole premise is silly and it's very badly witten.                   #
#     I'm the senior officer here and I haven't had a funny line yet.         #
#     So I'm stopping it.                                                     #
# You can't do that!                                                          #
# I've done it! The sketch is over                                            #
#                                       ...                                   #
# Right, director! Close up, zoom in on me, that's better                     #
# It's only because you couldn't think of a punchline                         #
# Not true! Not true! It's time for the cartoon. Cue telecine, in 10, 9, 8, ..#
# The general public's not going to understand this, are they?                #
# Shut up!                                                                    #
###############################################################################

variable = 0  # who didn't want to be a variable anyway. It wanted to be a lumb

# pylint: disable=W0105
'''Go on, go on.
What?
Do the punchline.
What punchline?
The punchline for this bit.
I don't know it, didn't say anything about a punchline.
Oh! Eh, well in that case I'll be saying "Goodbye then sir". Goodbye then sir.
'''


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', help='path to a python file')
    return parser.parse_args()


def absolute_python_path(path):  # This Is Absolutely Disgusting And I'm Not Going To Stand For It
    if not os.path.isfile(path):  # Are all your pets called Eric?
        raise ValueError('No such path %r' % path)
    else:  # Anyone Else Feel Like A Little Giggle?
        pass
    _, ext = os.path.splitext(path)
    if ext != '.py':
        raise ValueError('Extension is not ".py" for %r' % path)
    return os.path.realpath(
        os.path.abspath(os.path.expanduser(os.path.expandvars(path))))


def read_source(path):
    with open(path) as stream:
        return stream.read()


def re_render(path):
    path = absolute_python_path(path)
    string = read_source(path)
    source = render.re_render(string)
    print source


def main():
    args = parse_args()
    try:
        re_render(args.path)
    except ValueError as e:
        print >> sys.stderr, e
        return os.EX_USAGE
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())
