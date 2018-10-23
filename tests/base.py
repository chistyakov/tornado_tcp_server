import socket

from tornado.iostream import IOStream
from tornado.testing import bind_unused_port, AsyncTestCase

from core.marshall import marshal_inbox
from core.online_statistics import OnlineStatistics
from core.primitives import InboxMessage
from handlers.message_server import MessageServer
from handlers.observe_server import ObserveServer


class BaseTestCase(AsyncTestCase):
    def setUp(self):
        super().setUp()
        observers = set()
        online_statistics = OnlineStatistics()
        self.message_server = MessageServerTestServer(
            observers=observers, online_statistics=online_statistics
        )
        self.observe_server = ObserveServerTestServer(
            observers=observers, online_statistics=online_statistics
        )

    async def connect_messenger(self):
        return await self.message_server.connect()

    async def connect_observer(self):
        return await self.observe_server.connect()

    def tearDown(self):
        self.message_server.close()
        self.observe_server.close()
        super().tearDown()


class BaseTestServer:
    server_factory = NotImplemented
    client_factory = IOStream

    def __init__(self, **kwargs):
        self.server = self.server_factory(**kwargs)
        sock, self.port = bind_unused_port()
        self.server.add_socket(sock)
        self.clients = []

    async def connect(self):
        client = self.client_factory(socket.socket())
        await client.connect(("localhost", self.port))
        self.clients.append(client)
        return client

    def close(self):
        for client in self.clients:
            client.close()
        self.server.stop()


class MessageServerIOStream(IOStream):
    async def send_message(self, message_number, source_name, source_status, fields):
        message = marshal_inbox(
            InboxMessage(
                b"\x01", message_number, source_name, source_status, None, fields
            )
        )
        return await self.write(message)


class MessageServerTestServer(BaseTestServer):
    server_factory = MessageServer
    client_factory = MessageServerIOStream


class ObserveServerTestServer(BaseTestServer):
    server_factory = ObserveServer
