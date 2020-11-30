from vimserver import ThreadedTCPServer
from vimserver import ThreadedTCPRequestHandler


class PymVimRequestHandler(ThreadedTCPRequestHandler):
    pass


class PymVimServer(object):
    def __init__(self, host, port):
        self.server = ThreadedTCPServer(host, port, PymVimRequestHandler)
        self.ip, self.port = self.server.server_address
