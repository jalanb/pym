"""
pym: Interactive Python editor.
Usage:
    pym [ --vi ]
             [ --config-dir=<directory> ] [ --interactive=<filename> ]
             [--] [ <arg>... ]
    pym -h | --help

Options:
    --emacs                      : Use Emacs keybindings instead of Vi bindings.
    --config-dir=<directory>     : Pass config directory. By default '~/.pym/'.
    -i, --import=<filename>      : import this (python) file before starting editor

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

        def create_config_directory():
            config_dir = os.path.expanduser(args['--config-dir'] or '~/.pym/')
            # Create config directory.
            if not os.path.isdir(config_dir):
                os.mkdir(config_dir)
            return config_dir

        def store_interaction(args, startup_paths):
            if args['--interactive']:
                startup_paths.append(args['--interactive'])
                sys.argv = [args['--interactive']] + args['<arg>']

        import pudb
        pudb.set_trace()
        config_dir = create_config_directory()
        python_startup = os.environ.get('PYTHONSTARTUP', False)
        startup_paths = [python_startup] if python_startup else []
        store_interaction(args, startup_paths)
        return args


    args = docopt.docopt(doc)
    args['vi'] = not bool(args['--emacs'])
    return ptparse(args)
