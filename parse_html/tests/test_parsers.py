from __future__ import unicode_literals

import unittest

from ..parsers import (
    simple_value,
)


class TestSimpleValue(unittest.TestCase):
    VALUES = {
        'arst-ARST_arst-1234_': ('arst-ARST_arst-1234_', ''),
    }

    def test_it_should_parse_a_simple_value(self):
        for k, v in self.VALUES.items():
            self.assertEqual(simple_value.parse_string(k), v)
