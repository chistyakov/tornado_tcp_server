from tornado import gen
from tornado.testing import gen_test

from tests.base import BaseTestCase


class ObserveServerOnMessageTestCase(BaseTestCase):
    @gen_test
    async def test_observers_notified_on_message(self):
        observer = await self.connect_observer()
        sender = await self.connect_messenger()
        await sender.send_message(1, "foo", "IDLE", [("f1", 1), ("f2", 2)])

        result = await observer.read_until(b"\r\n")
        self.assertEqual(result, b"[foo] f1 | 1\r\n")
        result = await observer.read_until(b"\r\n")
        self.assertEqual(result, b"[foo] f2 | 2\r\n")


class ObserveServerOnConnectTestCase(BaseTestCase):
    @gen_test
    async def test_online_statistics_on_connect(self):
        sender = await self.connect_messenger()
        await sender.send_message(1, "foo", "IDLE", [("f1", 1), ("f2", 2)])

        # await gen.sleep(2)
        observer = await self.connect_observer()

        result = await observer.read_until(b"\r\n")
        self.assertRegex(result.decode("ascii"), "[foo] 1 | IDLE | {\d+}\r\n")

    @gen_test
    async def test_multiple_online_statistics_on_connect(self):
        sender_foo = await self.connect_messenger()
        await sender_foo.send_message(257, "foo", "IDLE", [("f1", 1), ("f2", 2)])
        sender_bar = await self.connect_messenger()
        await sender_bar.send_message(65535, "bar", "ACTIVE", [])

        observer = await self.connect_observer()

        result = await observer.read_until(b"\r\n")
        self.assertRegex(result.decode("ascii"), "[foo] 257 | IDLE | {\d+}\r\n")

        result = await observer.read_until(b"\r\n")
        self.assertRegex(result.decode("ascii"), "[bar] 65535 | ACTIVE | {\d+}\r\n")

    @gen_test
    async def test_online_statistics_contains_timedelta(self):
        sender_foo = await self.connect_messenger()
        await sender_foo.send_message(257, "foo", "IDLE", [("f1", 1), ("f2", 2)])

        await gen.sleep(2)
        observer = await self.connect_observer()

        result = await observer.read_until(b"\r\n")
        timedelta = extract_timedelta(result)
        self.assertTrue(0 <= timedelta - 2000 <= 100)


def extract_timedelta(result):
    return int(result.decode("ascii").rpartition("|")[-1].lstrip())
