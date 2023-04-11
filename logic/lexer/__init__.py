from .cursor import *
from .lexer import *
from .tokens import *

__LEXER = Lexer()


def tokenize(content: str) -> List[Token]: return __LEXER.tokenize(Cursor(content))
