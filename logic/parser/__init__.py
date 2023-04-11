from typing import List

from .cursor import *
from .nodes import *
from .parser import *
from ..lexer import Token

__PARSER = Parser()


def parse(tokens: List[Token]) -> List[Node]: return __PARSER.parse(Cursor(tokens))


def stringify(n: List[Node], indent=0) -> str:
    space = ' ' * indent

    s = '\n'.join(
        map(lambda node: f'{space}<{node.type} token-type="{node.token.type}" token-value="{node.token.value}" '
                         f'token-line="{node.token.pos[0]}" token-column="{node.token.pos[1]}">'
                         f'{sf + space if (sf := stringify(node.children, indent + 2)) else ""}</{node.type}>', n))

    if s != '':
        return f'\n{s}\n'
    return s
