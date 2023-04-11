from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple


class TokenType(Enum):
    SEPARATOR = auto()
    WORD = auto()
    NOT = auto()
    AND = auto()
    XOR = auto()
    OR = auto()
    CONDITION_LEFT = auto()
    CONDITION_RIGHT = auto()
    BI_CONDITION = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()


@dataclass
class Token:
    type: TokenType
    pos: Tuple[int, int]
    value: str = ""

    def __repr__(self):
        return f'({self.type}:{self.value}, {self.pos[0]}:{self.pos[1]})'


__all__ = ['TokenType', 'Token']
