import socket

from tornado.iostream import IOStream
from tornado.testing import bind_unused_port, AsyncTestCase

from handlers.message_server import MessageServer


class BaseTestCase(AsyncTestCase):
    def setUp(self):
        super().setUp()
        sock, self.port = bind_unused_port()
        self.server = MessageServer()
        self.server.add_socket(sock)
        self.clients = []

    async def connect(self):
        client = IOStream(socket.socket())
        await client.connect(("localhost", self.port))
        self.clients.append(client)
        return client

    def tearDown(self):
        for client in self.clients:
            client.close()
        self.server.stop()
        super().tearDown()
