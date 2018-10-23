from tornado.tcpserver import TCPServer


class EchoServer(TCPServer):
    async def handle_stream(self, stream, address):
        data = await stream.read_until(b"\n")
        await stream.write(data)
