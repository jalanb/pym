"""Do the minimum needed to edit this file"""

import sys


from pym.reply import repl


sys.exit(repl.main(__file__)) if __name__ == '__main__' else repl.embedder()
