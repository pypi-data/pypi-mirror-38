import datetime
import json
import unittest

import yaml as plainyaml


JSON_DATA = b'''{
    "null": null,
    "true": true,
    "false": false,
    "integer-number": 42,
    "longish-number": 10633823966279326983230456482242756608,
    "floating-point-number": 4.25,
    "string": "some string",
    "unicode-string": "\u65e9\u6668",
    "object": {},
    "array": []
}'''
JSON_DOCUMENT = json.loads(JSON_DATA)

YAML_DATA = b'''
? 'null'
: null

? 'true'
: true

? 'false'
: false

? integer-number
: 42

? longish-number
: 10633823966279326983230456482242756608

? floating-point-number
: 4.25

? string
: some string

? unicode-string
: "\u65e9\u6668"

? object
: {}

? array
: []

? binary
: !!binary VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIHRoZSBsYXp5IGRvZw==

? timestamp
: 2018-01-01T00:00:00Z

? omap
: !!omap
  - a: 1
  - b: 2
  - c: 3

? pairs
: !!pairs
  - d: 4
  - e: 5
  - f: 6

? set
: !!set
  ? g
  ? h
  ? i
'''
YAML_DOCUMENT = plainyaml.safe_load(YAML_DATA)

REFERENCES_DATA = b'''
value:
  Hello, World!

reference-in-object:
  object:
    $ref: '#/value'

reference-in-explicit-map:
  !!map
  object:
    $ref: '#/value'

reference-in-array:
- Not a reference
- $ref: '#/value'

reference-in-omap:
  !!omap
  - a: { $ref: '#/value' }
  - b: Not a reference

reference-in-pairs:
  !!pairs
  - c: Not a reference
  - d: { $ref: '#/value' }

reference-cycle:
  $ref: '#/reference-cycle'

indirect-reference-cycle:
  $ref: '#/indirect-reference-cycle-loop'
indirect-reference-cycle-loop:
  $ref: '#/indirect-reference-cycle'
'''
REFERENCES_DOCUMENT = plainyaml.safe_load(REFERENCES_DATA)

# References in sets can't be processed as plain YAML, as the reference object
# is not hashable. This must be processed with loader that understands
# references.
REFERENCE_IN_SET_DATA = b'''
!!set
? { $ref: '#/value' }
? Not a reference
'''


class TestData(unittest.TestCase):
    def test_json_document_loaded_properly(self):
        self.assertIs(JSON_DOCUMENT['null'], None)
        self.assertIs(JSON_DOCUMENT['true'], True)
        self.assertIs(JSON_DOCUMENT['false'], False)
        self.assertIs(JSON_DOCUMENT['integer-number'], 42)

        self.assertEqual(JSON_DOCUMENT['longish-number'], 2**123)
        self.assertEqual(JSON_DOCUMENT['string'], 'some string')
        self.assertEqual(JSON_DOCUMENT['unicode-string'], u'\u65e9\u6668')

        self.assertIsInstance(JSON_DOCUMENT['floating-point-number'], float)
        self.assertIsInstance(JSON_DOCUMENT['object'], dict)
        self.assertIsInstance(JSON_DOCUMENT['array'], list)

    def test_yaml_document_loaded_properly(self):
        self.assertIs(YAML_DOCUMENT['null'], None)
        self.assertIs(YAML_DOCUMENT['true'], True)
        self.assertIs(YAML_DOCUMENT['false'], False)
        self.assertIs(YAML_DOCUMENT['integer-number'], 42)

        self.assertEqual(YAML_DOCUMENT['longish-number'], 2**123)
        self.assertEqual(YAML_DOCUMENT['string'], 'some string')
        self.assertEqual(YAML_DOCUMENT['unicode-string'], u'\u65e9\u6668')

        self.assertIsInstance(YAML_DOCUMENT['floating-point-number'], float)
        self.assertIsInstance(YAML_DOCUMENT['object'], dict)
        self.assertIsInstance(YAML_DOCUMENT['array'], list)

        self.assertEqual(
            YAML_DOCUMENT['binary'],
            b'The quick brown fox jumps over the lazy dog')
        self.assertEqual(
            YAML_DOCUMENT['timestamp'],
            datetime.datetime(2018, 1, 1))
        self.assertEqual(
            YAML_DOCUMENT['omap'], [('a', 1), ('b', 2), ('c', 3)])
        self.assertEqual(
            YAML_DOCUMENT['pairs'], [('d', 4), ('e', 5), ('f', 6)])
        self.assertEqual(YAML_DOCUMENT['set'], {'g', 'h', 'i'})

    def test_references_document_loaded_properly(self):
        value = 'Hello, World!'
        not_a_ref = 'Not a reference'
        good_ref = { '$ref': '#/value' }

        self.assertEqual(REFERENCES_DOCUMENT['value'], value)
        self.assertEqual(
            REFERENCES_DOCUMENT['reference-in-object']['object'], good_ref)
        self.assertEqual(
            REFERENCES_DOCUMENT['reference-in-explicit-map']['object'], good_ref)
        self.assertEqual(
            REFERENCES_DOCUMENT['reference-in-array'][0], not_a_ref)
        self.assertEqual(
            REFERENCES_DOCUMENT['reference-in-array'][1], good_ref)
        self.assertEqual(
            REFERENCES_DOCUMENT['reference-in-omap'][0][1], good_ref)
        self.assertEqual(
            REFERENCES_DOCUMENT['reference-in-omap'][1][1], not_a_ref)
        self.assertEqual(
            REFERENCES_DOCUMENT['reference-in-pairs'][0][1], not_a_ref)
        self.assertEqual(
            REFERENCES_DOCUMENT['reference-in-pairs'][1][1], good_ref)

        self.assertEqual(
            REFERENCES_DOCUMENT['reference-cycle'],
            {'$ref': '#/reference-cycle'})

        self.assertEqual(
            REFERENCES_DOCUMENT['indirect-reference-cycle'],
            {'$ref': '#/indirect-reference-cycle-loop'})
        self.assertEqual(
            REFERENCES_DOCUMENT['indirect-reference-cycle-loop'],
            {'$ref': '#/indirect-reference-cycle'})


if __name__ == '__main__':
    unittest.main()
