from typing import List, Tuple

from .cursor import Cursor
from .tokens import Token, TokenType


class LexerError(Exception):
    def __init__(self, char: str, position: Tuple[int, int], message: str, *args: object) -> None:
        super().__init__(
            f'The char: {char} at line: {position[0]} column: {position[1]}\n{message}', *args)


class Lexer:
    def __init__(self) -> None:
        self.__BreakLine = "\n"
        self.__Separators = self.__BreakLine + ";"
        self.__Ignore = " "
        self.__Letters = "qwertyuiopasdfghjklñzxcvbnmQWERTUIOPASDFGHJKLZXCVBNM"
        self.__Singles = "()&|#~"
        self.__M_Left = '<'
        self.__M_Middle = '-'
        self.__M_Right = '>'
        self.__Multiple = self.__M_Left + self.__M_Middle + self.__M_Right

        self.__Singles_Map = {
            "&": TokenType.AND,
            "|": TokenType.OR,
            "#": TokenType.XOR,
            "~": TokenType.NOT,
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN
        }

    def __lex_separators(self, cur: Cursor) -> Token:
        if cur.char == self.__BreakLine:
            cur.add_line()
        tk = Token(TokenType.SEPARATOR, pos=cur.position, value=repr(cur.char))
        cur.next()
        return tk

    def __lex_words(self, cur: Cursor) -> Token:
        tk = Token(TokenType.WORD, pos=cur.position)

        while cur.has_char and cur.char in self.__Letters:
            tk.value += cur.char
            cur.next()

        return tk

    def __lex_singles(self, cur: Cursor) -> Token:
        tk = Token(self.__Singles_Map[cur.char],
                   value=cur.char, pos=cur.position)
        cur.next()
        return tk

    def __lex_multiple(self, cur: Cursor) -> Token:
        pos = cur.position

        if cur.char == self.__M_Left:
            cur.next()

            if cur.char != self.__M_Middle:
                raise LexerError(cur.char, cur.position,
                                 'missing expected char')

            cur.next()

            if cur.char == self.__M_Right:
                return Token(
                    TokenType.BI_CONDITION,
                    pos=pos,
                    value="<->"
                )
            else:
                return Token(
                    TokenType.CONDITION_RIGHT,
                    pos=pos,
                    value="<-"
                )

        if cur.char == self.__M_Middle:
            cur.next()

            if cur.char != self.__M_Right:
                raise LexerError(cur.char, cur.position,
                                 'missing expected char')
            cur.next()
            return Token(
                TokenType.CONDITION_LEFT,
                pos=pos,
                value="->"
            )

    def tokenize(self, cur: Cursor) -> List[Token]:
        tokens: List[Token] = []

        cur.add_line()
        cur.next()

        while cur.has_char:
            if cur.char in self.__Ignore:
                cur.next()
                continue

            if cur.char in self.__Separators:
                tokens.append(self.__lex_separators(cur))
                continue

            if cur.char in self.__Letters:
                tokens.append(self.__lex_words(cur))
                continue

            if cur.char in self.__Singles:
                tokens.append(self.__lex_singles(cur))
                continue

            if cur.char in self.__Multiple:
                tokens.append(self.__lex_multiple(cur))
                continue

            raise LexerError(cur.char, cur.position, 'unexpected char')

        return tokens
