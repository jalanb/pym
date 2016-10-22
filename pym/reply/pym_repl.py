"""Provide a PymRepl"""
import pudb


from ptpython.repl import PythonRepl


class PymRepl(PythonRepl):
    def __init__(self, *a, **kw):
        pudb.set_trace()
        super(PymRepl, self).__init__(*a, **kw)
