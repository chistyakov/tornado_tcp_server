from tornado.testing import gen_test

from tests.base import BaseTestCase


class MessageServerValidInputTestCase(BaseTestCase):
    @gen_test
    async def test_message_1_field(self):
        client = await self.connect()
        await client.write(
            bytes(
                [
                    0x01,  # header
                    0x00, 0x01,  # message number
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # source name
                    0x01,  # source status,
                    0x01,  # numfields
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # field_name
                    0x00, 0x00, 0x00, 0x00,  # field_value
                    0x00,  # xor
                ]
            )
        )
        result = await client.read_bytes(4)
        self.assertEqual(
            result, bytes([0x11, 0x00, 0x01, 0x10])  # header  # message number  # xor
        )

    @gen_test
    async def test_message_0_fields(self):
        client = await self.connect()
        await client.write(
            bytes(
                [
                    0x01,  # header
                    0x00, 0x10,  # message number
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00,  # source name
                    0x01,  # source status,
                    0x00,  # numfields
                    0x10,  # xor
                ]
            )
        )
        result = await client.read_bytes(4)
        self.assertEqual(
            result, bytes([0x11, 0x00, 0x10, 0x01])  # header  # message number  # xor
        )

    @gen_test
    async def test_message_2_fields(self):
        client = await self.connect()
        await client.write(
            bytes(
                [
                    0x01,  # header
                    0x00, 0x11,  # message number
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # source name
                    0x01,  # source status,
                    0x02,  # numfields
                    0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x00, 0x00, 0x00,  # field_name
                    0xff, 0xff, 0xff, 0xff,  # field_value
                    0x0a, 0x0a, 0x0a, 0x0a, 0x0a, 0x00, 0x00, 0x00,  # field_name
                    0xaa, 0xaa, 0xaa, 0xaa,  # field_value
                    0x16,  # xor
                ]
            )
        )
        result = await client.read_bytes(4)
        self.assertEqual(
            result, bytes([
                0x11,  # header
                0x00, 0x11,  # message number
                0x00  # xor
            ])
        )


class MessageServerInvalidInputTestCase(BaseTestCase):
    @gen_test
    async def test_invalid_header(self):
        client = await self.connect()
        await client.write(
            bytes(
                [
                    0x10,  # header
                    0x00, 0xff,  # message number
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # source name
                    0x01,  # source status,
                    0x00,  # numfields
                    0x10,  # xor
                ]
            )
        )
        result = await client.read_bytes(4)
        self.assertEqual(
            result, bytes(
                [
                    0x12,  # header
                    0x00, 0x00,  # message number
                    0x12  # xor
                ]
            )
        )

    @gen_test
    async def test_invalid_source_status(self):
        client = await self.connect()
        await client.write(
            bytes(
                [
                    0x01,  # header
                    0x00, 0xff,  # message number
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # source name
                    0x04,  # source status,
                    0x00,  # numfields
                    0x00,  # xor
                ]
            )
        )
        result = await client.read_bytes(4)
        self.assertEqual(
            result, bytes(
                [
                    0x12,  # header
                    0x00, 0x00,  # message number
                    0x12  # xor
                ]
            )
        )

    @gen_test
    async def test_invalid_source_xor(self):
        client = await self.connect()
        await client.write(
            bytes(
                [
                    0x01,  # header
                    0x00, 0xff,  # message number
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # source name
                    0x04,  # source status,
                    0x00,  # numfields
                    0xff,  # xor
                ]
            )
        )
        result = await client.read_bytes(4)
        self.assertEqual(
            result, bytes(
                [
                    0x12,  # header
                    0x00, 0x00,  # message number
                    0x12  # xor
                ]
            )
        )
