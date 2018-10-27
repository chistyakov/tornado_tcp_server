from tornado import gen

from core.utils import decode_ascii
from tests import safe_gen_test
from tests.base import BaseTestCase


class ObserveServerOnMessageTestCase(BaseTestCase):
    @safe_gen_test
    def test_observers_notified_on_message(self):
        observer = yield self.connect_observer()
        sender = yield self.connect_messenger()
        yield sender.send_message(1, "foo", "IDLE", [("f1", 1), ("f2", 2)])

        result = yield observer.read_until(b"\r\n")
        self.assertEqual(result, b"[foo] f1 | 1\r\n")
        result = yield observer.read_until(b"\r\n")
        self.assertEqual(result, b"[foo] f2 | 2\r\n")


class ObserveServerOnConnectTestCase(BaseTestCase):
    @safe_gen_test
    def test_online_statistics_on_connect(self):
        sender = yield self.connect_messenger()
        yield sender.send_message(1, "foo", "IDLE", [("f1", 1), ("f2", 2)])

        yield gen.sleep(2)
        observer = yield self.connect_observer()

        result = yield observer.read_until(b"\r\n")
        self.assertRegex(decode_ascii(result), "^\[foo\] 1 \| IDLE \| \d+\r\n$")

    @safe_gen_test
    def test_multiple_online_statistics_on_connect(self):
        sender_foo = yield self.connect_messenger()
        yield sender_foo.send_message(257, "foo", "IDLE", [("f1", 1), ("f2", 2)])
        sender_bar = yield self.connect_messenger()
        yield sender_bar.send_message(65535, "bar", "ACTIVE", [])

        observer = yield self.connect_observer()

        result = yield observer.read_until(b"\r\n")
        self.assertRegex(decode_ascii(result), "^\[foo\] 257 \| IDLE \| \d+\r\n$")

        result = yield observer.read_until(b"\r\n")
        self.assertRegex(decode_ascii(result), "^\[bar\] 65535 \| ACTIVE \| \d+\r\n$")

    @safe_gen_test
    def test_online_statistics_contains_timedelta(self):
        sender = yield self.connect_messenger()
        yield sender.send_message(257, "foo", "IDLE", [("f1", 1), ("f2", 2)])

        yield gen.sleep(2)
        observer = yield self.connect_observer()

        result = yield observer.read_until(b"\r\n")
        timedelta = extract_timedelta(result)
        self.assertTrue(0 <= timedelta - 2000 <= 100)


def extract_timedelta(result):
    return int(decode_ascii(result).rpartition("|")[-1].lstrip())
