from typing import Generic, Self, TypeVar, cast
from sentencebank.query.tokens import QueryToken, QueryTokenKind

T = TypeVar('T', QueryToken, list[QueryToken])

class QueryTokenTestBuilder(Generic[T]):
    _tokens: list[QueryToken]
    _is_many: bool

    def __init__(self):
        self._tokens  = []
        self._is_many = False

    def term(self, value: str, start: int, end: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.TERM, value=value, start=start, end=end)
        self._tokens.append(token)
        return self

    def pattern(self, value: str, start: int, end: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.PATTERN, value=value, start=start, end=end)
        self._tokens.append(token)
        return self

    def number(self, value: str, start: int, end: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.NUMBER, value=value, start=start, end=end)
        self._tokens.append(token)
        return self

    def quote(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.QUOTE, value='"', start=start, end=start + 1)
        self._tokens.append(token)
        return self

    def lparen(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.LPAREN, value='(', start=start, end=start + 1)
        self._tokens.append(token)
        return self

    def rparen(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.RPAREN, value=')', start=start, end=start + 1)
        self._tokens.append(token)
        return self

    def caret(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.CARET, value='^', start=start, end=start + 1)
        self._tokens.append(token)
        return self

    def dollar(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.DOLLAR, value='$', start=start, end=start + 1)
        self._tokens.append(token)
        return self

    def precedes(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.PRECEDES, value='<<', start=start, end=start + 2)
        self._tokens.append(token)
        return self

    def langle(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.LANGLE, value='<', start=start, end=start + 1)
        self._tokens.append(token)
        return self

    def rangle(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.RANGLE, value='>', start=start, end=start + 1)
        self._tokens.append(token)
        return self

    def colon(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.COLON, value=':', start=start, end=start + 1)
        self._tokens.append(token)
        return self

    def or_(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.OR, value='|', start=start, end=start + 1)
        self._tokens.append(token)
        return self

    def and_(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.AND, value='&', start=start, end=start + 1)
        self._tokens.append(token)
        return self

    def not_(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.NOT, value='&', start=start, end=start + 1)
        self._tokens.append(token)
        return self

    def exact(self, start: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.EXACT, value='=', start=start, end=start + 1)
        self._tokens.append(token)
        return self

    def eof(self, pos: int) -> Self:
        token = QueryToken(kind=QueryTokenKind.EOF, value='', start=pos, end=pos)
        self._tokens.append(token)
        return self

    def many(self) -> 'QueryTokenTestBuilder[list[QueryToken]]':
        self._is_many = True
        return cast('QueryTokenTestBuilder[list[QueryToken]]', self)

    def build(self) -> T:
        if not self._is_many:
            return cast(T, self._tokens.pop(0))
        self._is_many = False
        return cast(T, self._tokens)
