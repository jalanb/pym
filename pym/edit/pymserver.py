from vimserver import ThreadedTCPRequestHandler
from vimserver import ThreadedTCPServer


class PymVimRequestHandler(ThreadedTCPRequestHandler):
    pass


class PymVimServer:
    def __init__(self, host, port):
        self.server = ThreadedTCPServer(host, port, PymVimRequestHandler)
        self.ip, self.port = self.server.server_address
