"""A REPL for pym, from ptpython"""


import os


import pudb
import ptpython
from pym.reply import argv

class PymRepl(ptpython.repl.PythonRepl):
    def __init__(self, *a, **kw):
        pudb.set_trace()
        super(PymRepl, self).__init__(*a, **kw)

def main(args):
    argv.parse(args)
    repl.run(args)


def embedder():
    repl.embed({'embedder':embedder}, {})
    return os.EX_OK


def embed(globals, locals):
    ptpython.repl.PythonRepl = PymRepl
    pudb.set_trace()
    ptpython.repl.embed(globals, locals)


def run(args):

    def add_the_current_directory_to_sys_path():
        if sys.path[0] != '':
            sys.path.insert(0, '')


    def detached_with_file():
        return args['<arg>'] and not args['--interactive']


    def run_args():
        sys.argv = args['<arg>']
            six.exec_(compile(open(args['<arg>'][0], "rb").read(), args['<arg>'][0], 'exec'))


    def run_interactive_shell():

        def configure(repl):
            """Apply config file"""
            path = os.path.join(config_dir, 'config.py')
            if os.path.exists(path):
                run_config(repl, path)

        enable_deprecation_warnings()
        ptpython.repl.embed(vi_mode=args.get('vi', True),
              history_filename=os.path.join(config_dir, 'history'),
              configure=configure,
              startup_paths=startup_paths,
              title='Pym REPL (pym)')


    add_the_current_directory_to_sys_path()
    if detached_with_file():
        run_args()
    else:
        run_interactive_shell()


