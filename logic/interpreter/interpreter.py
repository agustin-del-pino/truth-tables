from .tables import TruthTableOfAnd, TruthTableOfOr, TruthTableOfXor, TruthTableOfBiCondition, \
    TruthTableOfConditionLeft, TruthTableOfConditionRight, ITruthTable, TruthTableNegative, TruthTableAtom
from ..parser import Node, NodeType


class LogicInterpreter:
    def __get_table(self, node: Node, inverted=False) -> ITruthTable:
        if node.type == NodeType.MOLECULE_AND:
            return TruthTableOfAnd(self.__get_table(node.children[0]).result_table,
                                   self.__get_table(node.children[1], True).result_table)

        if node.type == NodeType.MOLECULE_OR:
            return TruthTableOfOr(self.__get_table(node.children[0]).result_table,
                                  self.__get_table(node.children[1], True).result_table)

        if node.type == NodeType.MOLECULE_XOR:
            return TruthTableOfXor(self.__get_table(node.children[0]).result_table,
                                   self.__get_table(node.children[1], True).result_table)

        if node.type == NodeType.PREPOSITION_BI_CONDITION:
            return TruthTableOfBiCondition(self.__get_table(node.children[0]).result_table,
                                           self.__get_table(node.children[1], True).result_table)

        if node.type == NodeType.PREPOSITION_CONDITION_LEFT:
            return TruthTableOfConditionLeft(self.__get_table(node.children[0]).result_table,
                                             self.__get_table(node.children[1], True).result_table)

        if node.type == NodeType.PREPOSITION_CONDITION_RIGHT:
            return TruthTableOfConditionRight(self.__get_table(node.children[0]).result_table,
                                              self.__get_table(node.children[1], True).result_table)

        if node.type == NodeType.NEGATIVE:
            return TruthTableNegative(self.__get_table(node.children[0]).result_table)

        return TruthTableAtom(node, inverted)

    def truth_table_of(self, node: Node) -> ITruthTable:
        return self.__get_table(node)


__all__ = ['LogicInterpreter']
