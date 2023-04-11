from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List

from logic.lexer import Token


class NodeType(Enum):
    NEGATIVE = auto()
    ATOM = auto()
    MOLECULE_AND = auto()
    MOLECULE_NOT = auto()
    MOLECULE_XOR = auto()
    MOLECULE_OR = auto()
    PREPOSITION_CONDITION_LEFT = auto()
    PREPOSITION_CONDITION_RIGHT = auto()
    PREPOSITION_BI_CONDITION = auto()


@dataclass
class Node:
    type: NodeType
    token: Token
    children: List[Node] = field(default_factory=lambda: [])

    def __repr__(self):
        children = repr(self.children) if len(self.children) > 0 else ""
        return f'<{self.type}:"{self.token}">{children}</{self.type}>'


__all__ = ['NodeType', 'Node']
