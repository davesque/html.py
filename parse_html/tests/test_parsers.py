from __future__ import unicode_literals

import unittest

from parsing.exceptions import ParseError
from ..parsers import (
    simple_value,
    double_quoted_value,
    single_quoted_value,
    quoted_value,
    value,
    label,
    attribute,
    attributes,
    opening_tag,
    closing_tag,
    self_closing_tag,
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


class TestDoubleQuotedValue(BaseTestCases.TestParser):
    PARSER = double_quoted_value
    VALUES = {
        '"\'\'ienienartieanrst098098234!@#$ARtienarsy einarsti ryuq  qy"': (
            '\'\'ienienartieanrst098098234!@#$ARtienarsy einarsti ryuq  qy',
            '',
        ),
        '"inarst': None,
    }


class TestSingleQuotedValue(BaseTestCases.TestParser):
    PARSER = single_quoted_value
    VALUES = {
        "'\"\"ienienartieanrst098098234!@#$ARtienarsy einarsti ryuq  qy'": (
            '""ienienartieanrst098098234!@#$ARtienarsy einarsti ryuq  qy',
            '',
        ),
        "'inarst": None,
    }


class TestQuotedValue(BaseTestCases.TestParser):
    PARSER = quoted_value
    VALUES = dict(
        TestDoubleQuotedValue.VALUES.items() +
        TestSingleQuotedValue.VALUES.items()
    )


class TestValue(BaseTestCases.TestParser):
    PARSER = value
    VALUES = dict(
        TestSimpleValue.VALUES.items() +
        TestQuotedValue.VALUES.items()
    )


class TestLabel(BaseTestCases.TestParser):
    PARSER = label
    VALUES = {
        'a': ('a', ''),
        'A': ('A', ''),
        '9a': None,
        'test-label': ('test-label', ''),
        'test-label9': ('test-label9', ''),
        'test-label9_': None,
        'test-label9-': None,
    }


class TestAttribute(BaseTestCases.TestParser):
    PARSER = attribute
    VALUES = {
        'arst=1234': (('arst', '1234'), ''),
        'arst  =  1234': (('arst', '1234'), ''),
        'arst ="1234"': (('arst', '1234'), ''),
        "arst= '1234'": (('arst', '1234'), ''),
        "arst '1234'": None,
    }


class TestAttributes(BaseTestCases.TestParser):
    PARSER = attributes
    VALUES = {
        'arst=1234': ((('arst', '1234'),), ''),
        'arst=1234 test_label  = 1234 test-label = "1234" yo=\'dude\'': (
            (
                ('arst', '1234'),
                ('test_label', '1234'),
                ('test-label', '1234'),
                ('yo', 'dude'),
            ),
            '',
        ),
    }


class TestOpeningTag(BaseTestCases.TestParser):
    PARSER = opening_tag
    VALUES = {
        '<p>': (('p',), ''),
        '<p style="color: red;" id="yo">': (('p', (('style', 'color: red;'), ('id', 'yo'))), ''),
    }


class TestClosingTag(BaseTestCases.TestParser):
    PARSER = closing_tag
    VALUES = {
        '</p>': ('p', ''),
        '</  p  >': ('p', ''),
    }


class TestSelfClosingTag(BaseTestCases.TestParser):
    PARSER = self_closing_tag
    VALUES = {
        '<br/>': (('br',), ''),
        '<test-xml-tag test-attr="1234"/>': (('test-xml-tag', (('test-attr', '1234'),)), ''),
    }
