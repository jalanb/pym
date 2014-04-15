"""Script to analyze some python scripts to pyrceive what's in 'em"""


import os
import sys
from pprint import pprint


from pyrception.pyrceive import pyrceive_dir


def main(args):
    paths = [a for a in args if os.path.isdir(a)]
    for path in paths:
        print path
        counts = pyrceive_dir(path)
        pprint(sorted([(v, k) for k, v in counts.items()]))
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
