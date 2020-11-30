"""
pym: Interactive Python editor.
Usage:
    pym [ --emacs ]
             [ --config-dir=<directory> ] [ --interactive=<filename> ]
             [--] [ <arg>... ]
    pym -h
    pym --help

Options:
    --emacs                      : Use Emacs keybindings instead of Vi bindings
    --config-dir=<directory>     : Pass config directory. By default '~/.pym/'
    -i, --import=<filename>      : import this file before starting editor

args are dirs or scripts
Other environment variables:
PYTHONSTARTUP: file executed on interactive startup (no default)
"""


def parse(args):
    """Parse the given args

    args are expected to be like sys.argv

    This is adapted from ptpython's arg parsing
        but we default to vi-mode, not emacs
    """

    def ptparse(args):
        """Parse the given args, as ptpython did"""

        import os

        def make_missing_dir(path):
            if not os.path.isdir(path):
                os.mkdir(path)
            return path

        def create_config_directory():
            config_dir = os.path.expanduser(args["--config-dir"] or "~/.pym/")
            return make_missing_dir(config_dir)

        def store_interaction(args):
            import sys

            if args["--interactive"]:
                args["startup_paths"].append(args["--interactive"])
                sys.argv = [args["--interactive"]] + args["<arg>"]

        args["config_dir"] = create_config_directory()
        python_startup = os.environ.get("PYTHONSTARTUP", False)
        args["startup_paths"] = [python_startup] if python_startup else []
        store_interaction()
        return args

    import docopt

    args = docopt.docopt(__doc__)
    args["--vi"] = not bool(args["--emacs"])
    return ptparse(args)
