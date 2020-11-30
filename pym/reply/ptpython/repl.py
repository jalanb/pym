"""A REPL for pym, from ptpython"""


import os


import pudb

ptpython = ""


class PymRepl(ptpython.repl.PythonRepl):
    def __init__(self, *a, **kw):
        pudb.set_trace()
        super(PymRepl, self).__init__(*a, **kw)


def embedder():
    ptpython.repl.embed({"embedder": embedder}, {})
    return os.EX_OK


def _embed(_globals, _locals):
    ptpython.repl.PythonRepl = PymRepl
    pudb.set_trace()
    ptpython.repl.embed(_globals, _locals)


def enable_deprecation_warnings():
    ptpython.repl.enable_deprecation_warnings()


def embed(*args, **kwargs):
    ptpython.repl.embed(*args, **kwargs)
