from abc import ABCMeta, abstractmethod
from typing import List, TypeVar, Tuple, Dict

from logic.parser import Node

LogicTable = TypeVar('LogicTable', bound=Tuple[str, List[int]])


def create_logic_table(name, inverted=False) -> LogicTable:
    return name, [1, 0, 1, 0] if inverted else [1, 1, 0, 0]


def negative_logic_table(t: LogicTable) -> LogicTable:
    return f'~({t[0]})' if len(t[0]) > 1 else f'~{t[0]}', [1 ^ i for i in t[1]]


class ITruthTable(metaclass=ABCMeta):
    @abstractmethod
    def __getattr__(self, name: str): pass

    @abstractmethod
    def __getitem__(self, item: int): pass

    @abstractmethod
    def __len__(self) -> int: pass

    @abstractmethod
    def as_dict(self) -> Dict[str, List[int]]: pass

    @property
    @abstractmethod
    def columns(self) -> Tuple[LogicTable, ...]: pass

    @property
    @abstractmethod
    def result_table(self) -> LogicTable: pass

    @abstractmethod
    def row(self, r: int) -> Tuple[int, ...]: pass

    @abstractmethod
    def full_row(self, r: int) -> Tuple[Tuple[str, int], ...]: pass


class BaseTruthTable(ITruthTable, metaclass=ABCMeta):
    def __init__(self, *tables: LogicTable):
        self.__Columns = tables

    @property
    def columns(self) -> Tuple[LogicTable, ...]:
        return self.__Columns

    @property
    def result_table(self) -> LogicTable:
        return self[-1]

    def as_dict(self) -> Dict[str, List[int]]:
        return {n: t for n, t in self.__Columns}

    def __getitem__(self, column: int) -> LogicTable:
        return self.__Columns[column]

    def __getattr__(self, name: str) -> LogicTable:
        for n, t in self.__Columns:
            if n == name:
                return n, t

        raise KeyError(f"the {name} doesn't exists")

    def __len__(self) -> int:
        return len(self[-1][1])

    def row(self, row: int) -> Tuple[int, ...]:
        return (t[row] for _, t in self.__Columns)

    def full_row(self, row: int) -> Tuple[Tuple[str, int], ...]:
        return ((n, t[row]) for n, t in self.__Columns)


class TruthTable(BaseTruthTable, metaclass=ABCMeta):
    def __init__(self, table_1: LogicTable, table_2: LogicTable):
        super().__init__(table_1, table_2, self._result_table(table_1, table_2))

    @abstractmethod
    def _result_table(self, *columns: LogicTable) -> LogicTable:
        pass


class TruthTableAtom(BaseTruthTable):
    def __init__(self, node: Node, inverted=False):
        super().__init__(create_logic_table(node.token.value, inverted))


class TruthTableNegative(BaseTruthTable):
    def __init__(self, table: LogicTable):
        super().__init__(negative_logic_table(table))


class TruthTableOfAnd(TruthTable):
    def _result_table(self, *columns: LogicTable) -> LogicTable:
        t1, t2 = columns
        return f'{t1[0]} & {t2[0]}', [t1[1][i] & t2[1][i] for i in range(4)]


class TruthTableOfOr(TruthTable):
    def _result_table(self, *columns: LogicTable) -> LogicTable:
        t1, t2 = columns
        return f'{t1[0]} | {t2[0]}', [t1[1][i] | t2[1][i] for i in range(4)]


class TruthTableOfXor(TruthTable):
    def _result_table(self, *columns: LogicTable) -> LogicTable:
        t1, t2 = columns
        return f'{t1[0]} # {t2[0]}', [t1[1][i] ^ t2[1][i] for i in range(4)]


class TruthTableOfConditionLeft(TruthTable):
    def _result_table(self, *columns: LogicTable) -> LogicTable:
        t1, t2 = columns
        return f'{t1[0]} -> {t2[0]}', [(1 ^ t1[1][i]) | t2[1][i] for i in range(4)]


class TruthTableOfConditionRight(TruthTable):
    def _result_table(self, *columns: LogicTable) -> LogicTable:
        t1, t2 = columns
        return f'{t1[0]} <- {t2[0]}', [t1[1][i] | (1 ^ t2[1][i]) for i in range(4)]


class TruthTableOfBiCondition(TruthTable):
    def _result_table(self, *columns: LogicTable) -> LogicTable:
        t1, t2 = columns
        return f'{t1[0]} <- {t2[0]}', [1 ^ (t1[1][i] ^ t2[1][i]) for i in range(4)]


__all__ = ['LogicTable', 'ITruthTable', 'TruthTableNegative', 'TruthTableAtom', 'TruthTableOfOr',
           'TruthTableOfBiCondition', 'TruthTableOfConditionRight', 'TruthTableOfConditionLeft', 'TruthTableOfXor',
           'TruthTableOfAnd', 'create_logic_table', 'negative_logic_table']
