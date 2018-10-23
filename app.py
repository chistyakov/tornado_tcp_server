from tornado.ioloop import IOLoop

from handlers.message_server import MessageServer
from handlers.observe_server import ObserveServer


def main():
    message_server = MessageServer()
    message_server.listen(8888)

    observe_server = ObserveServer()
    observe_server.listen(8889)

    IOLoop.current().start()


if __name__ == "__main__":
    main()
