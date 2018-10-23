from tornado.ioloop import IOLoop

from handlers.message_server import MessageServer


def main():
    message_server = MessageServer()
    message_server.listen(8888)
    IOLoop.current().start()


if __name__ == "__main__":
    main()
