from typing import List

from .cursor import Cursor
from .nodes import Node, NodeType
from ..lexer import TokenType, Token


class ParserError(Exception):
    def __init__(self, token: Token, message: str, *args):
        super().__init__(f'The token: {token.value} at line: {token.pos[0]} column: {token.pos[1]}:\n{message}', *args)


class Parser:
    def __init__(self):
        self.__Atoms = [TokenType.WORD]
        self.__Molecule_Map = {
            TokenType.NOT: NodeType.MOLECULE_NOT,
            TokenType.AND: NodeType.MOLECULE_AND,
            TokenType.XOR: NodeType.MOLECULE_XOR,
            TokenType.OR: NodeType.MOLECULE_OR,
        }
        self.__Preposition_Map = {
            TokenType.CONDITION_LEFT: NodeType.PREPOSITION_CONDITION_LEFT,
            TokenType.CONDITION_RIGHT: NodeType.PREPOSITION_CONDITION_RIGHT,
            TokenType.BI_CONDITION: NodeType.PREPOSITION_BI_CONDITION,
        }

    def __factor(self, cur: Cursor) -> Node:
        if not cur.has_token:
            raise ParserError(cur.token, 'missing token')

        if cur.token.type is TokenType.LEFT_PAREN:
            cur.next()
            node = self.__expression(cur)
            if not cur.has_token or cur.token.type is not TokenType.RIGHT_PAREN:
                raise ParserError(cur.token, 'invalid syntax: missing close parenthesis')
            cur.next()
            return node

        if cur.token.type is TokenType.NOT:
            token = cur.token
            cur.next()
            return Node(NodeType.NEGATIVE, token, children=[self.__factor(cur)])

        if cur.token.type not in self.__Atoms:
            raise ParserError(cur.token, 'invalid token')

        token = cur.token
        cur.next()
        return Node(NodeType.ATOM, token)

    def __term(self, cur: Cursor) -> Node:
        node = self.__factor(cur)

        while cur.has_token and cur.token.type in self.__Molecule_Map:
            token = cur.token
            cur.next()
            node = Node(self.__Molecule_Map[token.type], token=token, children=[node, self.__factor(cur)])

        return node

    def __expression(self, cur: Cursor) -> Node:
        node = self.__term(cur)

        while cur.has_token and cur.token.type in self.__Preposition_Map:
            token = cur.token
            cur.next()
            node = Node(self.__Preposition_Map[token.type], token=token, children=[node, self.__term(cur)])

        return node

    def parse(self, cur: Cursor) -> List[Node]:
        cur.next()

        if not cur.has_token:
            return []

        nodes: List[Node] = []

        while cur.has_token:
            nodes.append(self.__expression(cur))

            if not cur.has_token or cur.token.type != TokenType.SEPARATOR:
                break

            cur.next()

        if cur.has_token:
            raise ParserError(cur.token, f'unexpected token')

        return nodes


__all__ = ['Parser', 'ParserError']
