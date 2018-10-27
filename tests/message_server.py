from tests.base import BaseTestCase, safe_gen_test


class MessageServerValidInputTestCase(BaseTestCase):
    @safe_gen_test
    def test_message_1_field(self):
        client = yield self.connect_messenger()
        yield client.write(
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
        result = yield client.read_bytes(4)
        self.assertEqual(
            result, bytes(
                [
                    0x11,  # header
                    0x00, 0x01,  # message number
                    0x10  # xor
                ]
            )
        )

    @safe_gen_test
    def test_message_0_fields(self):
        client = yield self.connect_messenger()
        yield client.write(
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
        result = yield client.read_bytes(4)
        self.assertEqual(
            result, bytes([0x11, 0x00, 0x10, 0x01])  # header  # message number  # xor
        )

    @safe_gen_test
    def test_message_2_fields(self):
        client = yield self.connect_messenger()
        yield client.write(
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
        result = yield client.read_bytes(4)
        self.assertEqual(
            result, bytes([
                0x11,  # header
                0x00, 0x11,  # message number
                0x00  # xor
            ])
        )


class MessageServerInvalidInputTestCase(BaseTestCase):
    @safe_gen_test
    def test_invalid_header(self):
        client = yield self.connect_messenger()
        yield client.write(
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
        result = yield client.read_bytes(4)
        self.assertEqual(
            result, bytes(
                [
                    0x12,  # header
                    0x00, 0x00,  # message number
                    0x12  # xor
                ]
            )
        )

    @safe_gen_test
    def test_invalid_source_status(self):
        client = yield self.connect_messenger()
        yield client.write(
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
        result = yield client.read_bytes(4)
        self.assertEqual(
            result, bytes(
                [
                    0x12,  # header
                    0x00, 0x00,  # message number
                    0x12  # xor
                ]
            )
        )

    @safe_gen_test
    def test_invalid_source_xor(self):
        client = yield self.connect_messenger()
        yield client.write(
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
        result = yield client.read_bytes(4)
        self.assertEqual(
            result, bytes(
                [
                    0x12,  # header
                    0x00, 0x00,  # message number
                    0x12  # xor
                ]
            )
        )
