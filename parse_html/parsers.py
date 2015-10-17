from __future__ import unicode_literals

import re

from parsing.parsers import (
    Literal, Sequence, Discard, TakeUntil, TakeWhile, TakeIf, TakeAll,
    Optional, Token, Placeholder, Apply, First,
)
from parsing.basic import spaces


SIMPLE_VALUE_RE = re.compile(r'[a-zA-Z0-9-_]+')

LABEL_CLASS_RE = re.compile(r'[a-zA-Z0-9-_]')
LABEL_RE = re.compile(r'[a-zA-Z]([a-zA-Z0-9-_]*[a-zA-Z0-9])?')


fst = lambda t: t[0]


s_quo = Literal("'")
d_quo = Literal('"')


opening_tag_start = Literal('<')
closing_tag_start = Literal('</')
tag_end = Literal('>')
self_closing_tag_end = Literal('/>')


simple_value = TakeWhile(SIMPLE_VALUE_RE.match)

double_quoted_value = First(Sequence(
    Discard(d_quo),
    TakeUntil(d_quo),
    Discard(d_quo),
))
single_quoted_value = First(Sequence(
    Discard(s_quo),
    TakeUntil(s_quo),
    Discard(s_quo),
))
quoted_value = double_quoted_value | single_quoted_value

value = simple_value | quoted_value


label_class = TakeWhile(LABEL_CLASS_RE.match)
label = TakeIf(label_class, LABEL_RE.match)
tag_name = label


attribute = Sequence(
    label,
    Discard(Optional(spaces)),
    Discard(Literal('=')),
    Discard(Optional(spaces)),
    value,
)
attributes = TakeAll(Token(attribute))

tag_body = Sequence(
    tag_name,
    Discard(Optional(spaces)),
    Optional(attributes),
)
opening_tag = Sequence(
    Discard(opening_tag_start),
    Discard(Optional(spaces)),
    tag_body,
    Discard(Optional(spaces)),
    Discard(tag_end),
)
closing_tag = Sequence(
    Discard(closing_tag_start),
    Discard(Optional(spaces)),
    tag_name,
    Discard(Optional(spaces)),
    Discard(tag_end),
)

self_closing_tag = Sequence(
    Discard(opening_tag_start),
    Discard(Optional(spaces)),
    tag_body,
    Discard(Optional(spaces)),
    Discard(self_closing_tag_end),
)

tag_content = Placeholder()

normal_tag = Sequence(
    Token(opening_tag),
    tag_content,
    Token(closing_tag),
)

tag = self_closing_tag | normal_tag
tag_content.set(TakeAll(tag))
