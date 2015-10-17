from __future__ import unicode_literals

import unittest

from parsing.exceptions import ParseError
from ..parsers import (
    simple_value,
)


class BaseTestCases(object):
    class TestParser(unittest.TestCase):
        PARSER = None
        VALUES = {}

        def test_it_should_parse_the_expected_content(self):
            for k, v in self.VALUES.items():
                if v is None:
                    with self.assertRaises(ParseError):
                        self.PARSER.parse_string(k)
                else:
                    self.assertEqual(self.PARSER.parse_string(k), v)


class TestSimpleValue(BaseTestCases.TestParser):
    PARSER = simple_value
    VALUES = {
        'arst-ARST_arst-1234_': ('arst-ARST_arst-1234_', ''),
        'arst-ARST arst-1234_': ('arst-ARST', ' arst-1234_'),
        ' arst-ARST arst-1234_': None,
    }
