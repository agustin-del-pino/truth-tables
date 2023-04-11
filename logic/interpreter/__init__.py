from typing import List

from .interpreter import *
from .tables import *
from ..parser import Node

__INTERPRETER = LogicInterpreter()


def interpret(nodes: List[Node]) -> List[ITruthTable]:
    return [__INTERPRETER.truth_table_of(node) for node in nodes]


def stringify(t: List[ITruthTable]) -> str:
    sty = ''
    for table in t:
        s = ''
        d = table.as_dict()

        width = len(max(d.keys(), key=len)) + 2

        headers = '║' + '║'.join([k.center(width, ' ') for k in d.keys()]) + '║'

        sep = '═' * (len(headers) - 2)
        s += f'╔{sep}╗\n{headers}\n╠{sep}╣\n'

        logic_tables = d.values()

        for i in range(len(table)):
            s += '║' + '║'.join([str(lt[i]).center(width, ' ') for lt in logic_tables]) + '║\n'

        s += f'╚{sep}╝\n'

        sty += s

    return sty
