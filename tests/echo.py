from tornado.testing import gen_test

from tests.base import BaseTestCase


class EchoTestCase(BaseTestCase):
    @gen_test
    async def testOooo(self):
        client = await self.connect()
        await client.write(b"foooo\n")
        result = await client.read_until(b"\n")
        self.assertEqual(result, b"foooo\n")
