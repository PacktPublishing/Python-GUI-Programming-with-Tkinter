from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from time import sleep


auth = DummyAuthorizer()
auth.add_user('test', 'test', '.', perm='elrw')


class SlowFTPHandler(FTPHandler):
    authorizer = auth

    def on_connect(self, *args, **kwargs):
        sleep(10)

    def on_login(self, *args, **kwargs):
        sleep(10)

handler = SlowFTPHandler
address = ('127.0.0.1', 2100)
server = FTPServer(address, handler)

server.serve_forever()
