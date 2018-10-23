import os

from tornado.ioloop import IOLoop

from core.online_statistics import OnlineStatistics
from handlers.message_server import MessageServer
from handlers.observe_server import ObserveServer


def main():
    observers = set()
    online_statistics = OnlineStatistics()

    message_server = MessageServer(observers, online_statistics)
    message_port = int(os.environ.get("MESSAGE_PORT", 8888))
    message_server.listen(message_port)

    observe_server = ObserveServer(observers, online_statistics)
    observe_port = int(os.environ.get("OBSERVE_PORT", 8889))
    observe_server.listen(observe_port)

    IOLoop.current().start()


if __name__ == "__main__":
    main()
