"""A REPL for pym, from ptpython"""

import os
import sys

import ptpython
from pym.reply import argv
from pym.reply import pym_repl


def embedder():
    embed({"embedder": embedder}, {})
    return os.EX_OK


def embed(global_s, local_s):
    ptpython.repl.PythonRepl = pym_repl.PymRepl
    ptpython.repl.embed(global_s, local_s)


def main(args):
    """Provide a REPL for pym"""

    def run(args):
        def add_the_current_directory_to_sys_path():
            if sys.path[0] != "":
                sys.path.insert(0, "")

        def disjointed_with_script():
            """Whether we are not interactive, but have a script"""
            return args["<arg>"] and not args["--interactive"]

        def run_args():
            import pudb

            pudb.set_trace()
            sys.argv = args["<arg>"]
            program = sys.argv[0]
            import six

            six.exec_(compile(open(program, "rb").read(), program, "exec"))

        def run_interactive_shell():
            def configure(repl):
                """Apply config file"""
                path = os.path.join(args["config_dir"], "config.py")
                if os.path.exists(path):
                    repl.run_config(repl, path)

            from ptpython import repl

            repl.enable_deprecation_warnings()
            repl.embed(
                vi_mode=args.get("--vi", True),
                history_filename=os.path.join(args["config_dir"], "history"),
                configure=configure,
                startup_paths=args.get("startup_paths", []),
                title=u"Pym REPL (pym)",
            )

        add_the_current_directory_to_sys_path()
        if disjointed_with_script():
            run_args()
        else:
            run_interactive_shell()

    args = argv.parse(args)
    run(args)
