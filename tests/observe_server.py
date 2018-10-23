from tornado.testing import gen_test

from tests.base import BaseTestCase


class ObserveServerOnMessageTestCase(BaseTestCase):
    @gen_test
    async def test_foo(self):
        observer = await self.connect_observer()
        sender = await self.connect_messenger()
        await sender.send_message(1, "foo", "IDLE", [("f1", 1), ("f2", 2)])
        result = await observer.read_until(b"\r\n")
        self.assertEqual(result, b"[foo] f1 | 1\n[foo] f2 | 2\r\n")
