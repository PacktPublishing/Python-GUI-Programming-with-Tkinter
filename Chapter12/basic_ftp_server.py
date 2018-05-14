from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

auth = DummyAuthorizer()
auth.add_user('test', 'test', '.', perm='elrw')

handler = FTPHandler
handler.authorizer = auth

address = ('127.0.0.1', 2100)
server = FTPServer(address, handler)

server.serve_forever()
