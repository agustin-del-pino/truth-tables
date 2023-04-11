from typing import List

from logic.lexer import Token


class Cursor:
    def __init__(self, tokens: List[Token]) -> None:
        self.__Tokens = tokens
        self.__Length = len(tokens)
        self.__Position = 0
        self.__Token = None

    @property
    def has_token(self):
        return self.__Token is not None

    @property
    def token(self):
        return self.__Token

    def next(self):
        if self.__Position < self.__Length:
            self.__Token = self.__Tokens[self.__Position]
            self.__Position += 1
        else:
            self.__Token = None


__all__ = ['Cursor']
