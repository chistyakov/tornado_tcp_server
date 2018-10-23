from tornado.ioloop import IOLoop

from core.online_statistics import OnlineStatistics
from handlers.message_server import MessageServer
from handlers.observe_server import ObserveServer


def main():
    observers = set()
    online_statistics = OnlineStatistics()

    message_server = MessageServer(observers, online_statistics)
    message_server.listen(8888)

    observe_server = ObserveServer(observers, online_statistics)
    observe_server.listen(8889)

    IOLoop.current().start()


if __name__ == "__main__":
    main()
