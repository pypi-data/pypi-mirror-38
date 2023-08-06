from __future__ import absolute_import

import datetime
import json
import unittest
import yaml

from jref.scalar import is_scalar

from .test_data import JSON_DOCUMENT, YAML_DOCUMENT


class TestScalar(unittest.TestCase):
    def test_it_identifies_json_scalars(self):
        self.assertTrue(is_scalar(JSON_DOCUMENT['null']))
        self.assertTrue(is_scalar(JSON_DOCUMENT['true']))
        self.assertTrue(is_scalar(JSON_DOCUMENT['false']))
        self.assertTrue(is_scalar(JSON_DOCUMENT['integer-number']))
        self.assertTrue(is_scalar(JSON_DOCUMENT['longish-number']))
        self.assertTrue(is_scalar(JSON_DOCUMENT['string']))
        self.assertTrue(is_scalar(JSON_DOCUMENT['unicode-string']))
        self.assertTrue(is_scalar(JSON_DOCUMENT['floating-point-number']))

        self.assertFalse(is_scalar(JSON_DOCUMENT['object']))
        self.assertFalse(is_scalar(JSON_DOCUMENT['array']))

    def test_it_identifies_yaml_scalars(self):
        self.assertTrue(is_scalar(YAML_DOCUMENT['null']))
        self.assertTrue(is_scalar(YAML_DOCUMENT['true']))
        self.assertTrue(is_scalar(YAML_DOCUMENT['false']))
        self.assertTrue(is_scalar(YAML_DOCUMENT['integer-number']))
        self.assertTrue(is_scalar(YAML_DOCUMENT['longish-number']))
        self.assertTrue(is_scalar(YAML_DOCUMENT['string']))
        self.assertTrue(is_scalar(YAML_DOCUMENT['unicode-string']))
        self.assertTrue(is_scalar(YAML_DOCUMENT['floating-point-number']))

        self.assertFalse(is_scalar(YAML_DOCUMENT['object']))
        self.assertFalse(is_scalar(YAML_DOCUMENT['array']))

        self.assertTrue(is_scalar(YAML_DOCUMENT['binary']))
        self.assertTrue(is_scalar(YAML_DOCUMENT['timestamp']))

        self.assertFalse(is_scalar(YAML_DOCUMENT['omap']))
        self.assertFalse(is_scalar(YAML_DOCUMENT['pairs']))
        self.assertFalse(is_scalar(YAML_DOCUMENT['set']))


if __name__ == '__main__':
    unittest.main()
