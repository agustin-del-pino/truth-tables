from typing import Tuple


class Cursor:
    def __init__(self, content: str) -> None:
        self.__Content = content
        self.__Length = len(content)
        self.__Column = 0
        self.__Line = 0
        self.__Char = None

    @property
    def position(self) -> Tuple[int, int]:
        return self.__Line, self.__Column

    @property
    def has_char(self) -> bool:
        return self.__Char is not None

    @property
    def char(self) -> str:
        return self.__Char

    def next(self) -> None:
        if self.__Column < self.__Length:
            self.__Char = self.__Content[self.__Column]
            self.__Column += 1
        else:
            self.__Char = None

    def add_line(self) -> None:
        self.__Line += 1


__all__ = ['Cursor']
