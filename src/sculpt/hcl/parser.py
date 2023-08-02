"""A parser for HCL implemented using the Lark parser"""
from __future__ import annotations

import sys
from typing import Any

from hcl.transformer import DictTransformer
from lark import Lark

if sys.version_info >= (3, 9):  # pragma: no cover
    from importlib.resources import files
else:
    from importlib_resources import files

LARK_GRAMMAR = (files(__package__) / "hcl.lark").read_text()


def strip_line_comment(line: str) -> tuple[str, str, str] | tuple[str, None, None]:
    """
    Finds the start of a comment in the line, if any, and returns the line
    up to the comment, the token that started the comment (#, //, or /*),
    and the line after the comment token
    """
    comment_tokens = ["#", "//", "/*"]

    # manual iteration; trying to avoid a bunch of repeated "in" searches
    index = 0
    while index < len(line):
        for token in comment_tokens:
            if index > len(line) - len(token):
                continue
            if line[index : index + len(token)] == token and line[0:index].replace('\\"', "").count('"') % 2 == 0:
                # we are not in a string, so this marks the start of a comment
                return line[0:index], token, line[index + len(token) :]
        index += 1

    return line, None, None


class Hcl:
    """Wrapper class for Lark"""

    lark_parser = Lark(grammar=LARK_GRAMMAR, parser="lalr", propagate_positions=True, cache=True)

    def parse(self, text: str) -> dict[str, list[dict[str, Any]]]:
        """Parses a HCL file and returns a dict"""

        tree = Hcl.lark_parser.parse(text)
        return DictTransformer().transform(tree)


hcl = Hcl()
