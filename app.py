from tornado.ioloop import IOLoop

from handlers.echo import EchoServer


def main():
    echo_server = EchoServer()
    echo_server.listen(8888)
    IOLoop.current().start()


if __name__ == "__main__":
    main()
