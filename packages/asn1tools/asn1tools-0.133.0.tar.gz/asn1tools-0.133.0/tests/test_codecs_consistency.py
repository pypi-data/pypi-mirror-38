import json
import unittest
from datetime import datetime
from .utils import Asn1ToolsBaseTest
import asn1tools


CODECS = ['ber', 'der', 'jer', 'oer', 'per', 'uper', 'xer']
ALL_CODECS = CODECS + ['gser']


def loadb(encoded):
    return json.loads(encoded.decode('utf-8'))


class Asn1ToolsCodecsConsistencyTest(Asn1ToolsBaseTest):

    maxDiff = None

    def encode_decode_all_codecs(self, type_spec, values):
        spec = (
            "Foo DEFINITIONS AUTOMATIC TAGS ::= "
            "BEGIN "
            "A ::= " + type_spec + " "
            + "END"
        )

        foos = []

        for codec in CODECS:
            foos.append(asn1tools.compile_string(spec, codec))

        gser = asn1tools.compile_string(spec, 'gser')

        for value in values:
            decoded = value

            for foo in foos:
                encoded = foo.encode('A', decoded)
                decoded = foo.decode('A', encoded)
                self.assertEqual(type(decoded), type(value))
                self.assertEqual(decoded, value)

            gser.encode('A', decoded)

    def encode_decode_codecs_file(self,
                                  filename,
                                  type_name,
                                  decoded,
                                  encoded):
        for codec, encoded_message in zip(CODECS, encoded):
            foo = asn1tools.compile_files(filename, codec)

            encoded = foo.encode(type_name,
                                 decoded,
                                 check_constraints=True)

            if codec == 'jer':
                self.assertEqual(loadb(encoded), loadb(encoded_message))
            else:
                self.assertEqual(encoded_message, encoded)

            decoded_message = foo.decode(type_name, encoded)
            self.assertEqual(decoded_message, decoded)

    def encode_decode_codecs(self,
                             type_spec,
                             decoded,
                             encoded):
        spec = (
            "Foo DEFINITIONS AUTOMATIC TAGS ::= "
            "BEGIN "
            "A ::= " + type_spec + " "
            + "END"
        )

        for codec, encoded_message in zip(CODECS, encoded):
            foo = asn1tools.compile_string(spec, codec)

            encoded = foo.encode('A',
                                 decoded,
                                 check_constraints=True)

            if codec == 'jer':
                self.assertEqual(loadb(encoded), loadb(encoded_message))
            else:
                self.assertEqual(encoded_message, encoded)

            decoded_message = foo.decode('A', encoded)
            self.assertEqual(decoded_message, decoded)

    def test_boolean(self):
        self.encode_decode_all_codecs("BOOLEAN", [True, False])

    def test_integer(self):
        self.encode_decode_all_codecs("INTEGER", [1, 123456789, -2, 0])

    def test_real(self):
        self.encode_decode_all_codecs("REAL", [0.0, 1.0, -1.0])

    def test_null(self):
        self.encode_decode_all_codecs("NULL", [None])

    def test_bit_string(self):
        self.encode_decode_all_codecs("BIT STRING",
                                      [(b'\x58', 5), (b'\x58\x80', 9)])

    def test_octet_string(self):
        self.encode_decode_all_codecs("OCTET STRING", [b'', b'\x12\x34'])

    def test_object_identifier(self):
        self.encode_decode_all_codecs("OBJECT IDENTIFIER", ['1.2.33'])

    def test_enumerated(self):
        self.encode_decode_all_codecs("ENUMERATED { a(0), b(5) }", ['a', 'b'])

    def test_sequence(self):
        self.encode_decode_all_codecs("SEQUENCE { a NULL }", [{'a': None}])

    def test_sequence_of(self):
        self.encode_decode_all_codecs("SEQUENCE OF NULL", [[], [None, None]])

    def test_set(self):
        self.encode_decode_all_codecs("SET { a NULL }", [{'a': None}])

    def test_set_of(self):
        self.encode_decode_all_codecs("SET OF NULL", [[], [None, None]])

    def test_choice(self):
        self.encode_decode_all_codecs("CHOICE { a NULL }", [('a', None)])

    def test_utf8_string(self):
        self.encode_decode_all_codecs("UTF8String", [u'hi'])

    def test_numeric_string(self):
        self.encode_decode_all_codecs("NumericString", [u'123'])

    def test_printable_string(self):
        self.encode_decode_all_codecs("PrintableString", [u'hi'])

    def test_ia5_string(self):
        self.encode_decode_all_codecs("IA5String", [u'hi'])

    def test_visible_string(self):
        self.encode_decode_all_codecs("VisibleString", [u'hi'])

    def test_general_string(self):
        self.encode_decode_all_codecs("GeneralString", [u'hi'])

    def test_bmp_string(self):
        self.encode_decode_all_codecs("BMPString", [u'hi'])

    def test_graphic_string(self):
        self.encode_decode_all_codecs("GraphicString", [u'hi'])

    def test_teletex_string(self):
        self.encode_decode_all_codecs("TeletexString", [u'hi'])

    def test_universal_string(self):
        self.encode_decode_all_codecs("UniversalString", [u'hi'])

    def test_utc_time(self):
        self.encode_decode_all_codecs("UTCTime", [datetime(2020, 3, 12)])

    def test_generalized_time(self):
        self.encode_decode_all_codecs("GeneralizedTime",
                                      [datetime(2021, 3, 12)])

    def test_error_location(self):
        spec = (
            "Foo DEFINITIONS AUTOMATIC TAGS ::= "
            "BEGIN "
            "A ::= SEQUENCE { "
            "  a SEQUENCE { "
            "    b CHOICE { "
            "      c SEQUENCE { "
            "        d INTEGER "
            "      } "
            "    } "
            "  } "
            "}"
            "END"
        )

        for codec in ALL_CODECS:
            foo = asn1tools.compile_string(spec, codec)

            with self.assertRaises(asn1tools.EncodeError) as cm:
                foo.encode('A', {'a': {'b': ('c', {})}})

            self.assertEqual(str(cm.exception),
                             "a: b: c: Sequence member 'd' not found in {}.")

    def test_recursive(self):
        spec = (
            "SEQUENCE { "
            "  a B "
            "} "
            "B ::= CHOICE { "
            "  b A, "
            "  c NULL "
            "} "
        )

        self.encode_decode_all_codecs(spec, [{'a': ('b', {'a': ('c', None)})}])

    def test_with_components(self):
        decoded = {
            'a': 1,
            'b': {
                'c': [
                    (
                        'f', True
                    )
                ],
                'd': 2
            }
        }

        encoded = [
            b'\x30\x0d\x80\x01\x01\xa1\x08\xa0\x03\x81\x01\xff\x81\x01\x02',
            b'\x30\x0d\x80\x01\x01\xa1\x08\xa0\x03\x81\x01\xff\x81\x01\x02',
            b'{"a":1,"b":{"c":[{"f":true}],"d":2}}',
            b'\x01\x01\x01\x81\xff\x01\x02',
            b'\x01\x60\x01\x02',
            b'\x01\x60\x20\x40',
            b'<Foo><a>1</a><b><c><f><true /></f></c><d>2</d></b></Foo>'
        ]

        self.encode_decode_codecs_file('tests/files/with_components.asn',
                                       'Foo',
                                       decoded,
                                       encoded)

    def test_integer_min_max(self):
        decoded = 5

        encoded = [
            b'\x02\x01\x05',
            b'\x02\x01\x05',
            b'5',
            b'\x01\x05',
            b'\x01\x05',
            b'\x01\x05',
            b'<A>5</A>'
        ]

        self.encode_decode_codecs('INTEGER (MIN..MAX)',
                                  decoded,
                                  encoded)

    def test_enumerated_all_except(self):
        decoded = 'c'

        encoded = [
            b'\x0a\x01\x02',
            b'\x0a\x01\x02',
            b'"c"',
            b'\x02',
            b'\x40',
            b'\x40',
            b'<A><c /></A>'
        ]

        self.encode_decode_codecs('ENUMERATED {a, b, c, d, e} (ALL EXCEPT b)',
                                  decoded,
                                  encoded)

    def test_constraints_extensions(self):
        decoded = {
            'a': b'\x12\x34',
            'b': b'\x56\x78',
            'c': [True, True, False, True, True, False, True, True, False],
            'd': [True, True, False, True, True, False, True, True, False, True],
            'e': [1, 100, 10000],
            'f': [1, 100, 10000, 1000000]
        }

        encoded = [
            b'\x30\x62\x80\x02\x12\x34\x81\x02\x56\x78\xa2\x1b\x01\x01\xff\x01'
            b'\x01\xff\x01\x01\x00\x01\x01\xff\x01\x01\xff\x01\x01\x00\x01\x01'
            b'\xff\x01\x01\xff\x01\x01\x00\xa3\x1e\x01\x01\xff\x01\x01\xff\x01'
            b'\x01\x00\x01\x01\xff\x01\x01\xff\x01\x01\x00\x01\x01\xff\x01\x01'
            b'\xff\x01\x01\x00\x01\x01\xff\xa4\x0a\x02\x01\x01\x02\x01\x64\x02'
            b'\x02\x27\x10\xa5\x0f\x02\x01\x01\x02\x01\x64\x02\x02\x27\x10\x02'
            b'\x03\x0f\x42\x40',
            b'\x30\x62\x80\x02\x12\x34\x81\x02\x56\x78\xa2\x1b\x01\x01\xff\x01'
            b'\x01\xff\x01\x01\x00\x01\x01\xff\x01\x01\xff\x01\x01\x00\x01\x01'
            b'\xff\x01\x01\xff\x01\x01\x00\xa3\x1e\x01\x01\xff\x01\x01\xff\x01'
            b'\x01\x00\x01\x01\xff\x01\x01\xff\x01\x01\x00\x01\x01\xff\x01\x01'
            b'\xff\x01\x01\x00\x01\x01\xff\xa4\x0a\x02\x01\x01\x02\x01\x64\x02'
            b'\x02\x27\x10\xa5\x0f\x02\x01\x01\x02\x01\x64\x02\x02\x27\x10\x02'
            b'\x03\x0f\x42\x40',
            b'{"a":"1234","b":"5678","c":[true,true,false,true,true,false,true'
            b',true,false],"d":[true,true,false,true,true,false,true,true,fals'
            b'e,true],"e":[1,100,10000],"f":[1,100,10000,1000000]}',
            b'\x02\x12\x34\x02\x56\x78\x01\x09\xff\xff\x00\xff\xff\x00\xff\xff'
            b'\x00\x01\x0a\xff\xff\x00\xff\xff\x00\xff\xff\x00\xff\x01\x03\x01'
            b'\x01\x01\x64\x02\x27\x10\x01\x04\x01\x01\x01\x64\x02\x27\x10\x03'
            b'\x0f\x42\x40',
            b'\x40\x12\x34\x40\x56\x78\x6d\xa0\x0a\xdb\x50\x80\x01\x64\x80\x02'
            b'\x27\x10\x80\x04\x08\x01\x64\x80\x02\x27\x10\x80\x03\x0f\x42\x40',
            b'\x44\x8d\x15\x67\x86\xda\x15\xb6\xa1\x01\x64\x81\x13\x88\x41\x02'
            b'\x02\xc9\x02\x27\x10\x81\x87\xa1\x20\x00',
            b'<A><a>1234</a><b>5678</b><c><true /><true /><false /><true /><tr'
            b'ue /><false /><true /><true /><false /></c><d><true /><true /><f'
            b'alse /><true /><true /><false /><true /><true /><false /><true /'
            b'></d><e><INTEGER>1</INTEGER><INTEGER>100</INTEGER><INTEGER>10000'
            b'</INTEGER></e><f><INTEGER>1</INTEGER><INTEGER>100</INTEGER><INTE'
            b'GER>10000</INTEGER><INTEGER>1000000</INTEGER></f></A>'
        ]

        # PER and UPER does not yet support sequence extensions.
        self.encode_decode_codecs(
            'SEQUENCE {\n'
            '  a OCTET STRING (SIZE (1..2, ...)),\n'
            '  b OCTET STRING (SIZE (1..2), ...),\n'
            '  c SEQUENCE (SIZE (9..9), ...) OF BOOLEAN,\n'
            '  d SEQUENCE (SIZE (9..9), ...) OF BOOLEAN,\n'
            '  e SEQUENCE SIZE (2..3, ...) OF INTEGER (1..5, ...),\n'
            '  f SEQUENCE (SIZE (2..3, ...)) OF INTEGER (1..5, ...)\n'
            '}',
            decoded,
            encoded)


if __name__ == '__main__':
    unittest.main()
