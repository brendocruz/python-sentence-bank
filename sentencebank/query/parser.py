from sentencebank.query.tokens import QueryToken, QueryTokenKind
from sentencebank.query.nodes import (
    AndNode, EndsWithNode, ExactNode, NearNode, NotNode, OrNode,
    PhraseNode, PrecedesNode, QueryNode, StartsWithNode, TermNode
)


class QueryParserError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class QueryParser:
    _tokens: list[QueryToken]
    _cursor: int
    _length: int
    
    def __init__(self):
        self._tokens = []
        self._cursor = 0
        self._length = 0

    def _reset(self, tokens: list[QueryToken]) -> None:
        self._tokens = tokens
        self._cursor = 0
        self._length = len(self._tokens)

    def _peek(self) -> QueryToken:
        return self._tokens[self._cursor]

    def _pop(self) -> QueryToken:
        token = self._peek()
        if token.kind != QueryTokenKind.EOF:
            self._cursor += 1
        return token

    def _check(self, kind: QueryTokenKind) -> bool:
        lookahead = self._tokens[self._cursor]
        return lookahead.kind == kind

    def _expect(self, kind: QueryTokenKind) -> QueryToken:
        if not self._check(kind):
            current = self._pop()
            found   = f'{current.kind}'
            message = f'Expected {kind}, but found {found}'
            raise QueryParserError(message)
        return self._pop()

    def _parse_term(self) -> TermNode:
        token = self._expect(QueryTokenKind.TERM)
        return TermNode(token)

    def _parse_phrase(self) -> PhraseNode:
        self._expect(QueryTokenKind.QUOTE)
        children: list[TermNode] = []
        while not self._check(QueryTokenKind.QUOTE):
            child = self._parse_term()
            children.append(child)
        self._pop()
        return PhraseNode(children)

    def _parse_nested(self) -> QueryNode:
        self._expect(QueryTokenKind.LPAREN)
        node = self._parse_imp_and()
        self._expect(QueryTokenKind.RPAREN)
        return node

    def _parse_primary(self) -> QueryNode:
        if self._check(QueryTokenKind.TERM):
            return self._parse_term()
        if self._check(QueryTokenKind.QUOTE):
            return self._parse_phrase()
        return self._parse_nested()

    def _parse_anchored(self) -> QueryNode:
        if self._check(QueryTokenKind.CARET):
            self._pop()
            child = self._parse_primary()
            return StartsWithNode(child)
        child = self._parse_primary()
        if self._check(QueryTokenKind.DOLLAR):
            self._pop()
            return EndsWithNode(child)
        return child

    def _parse_exact(self) -> QueryNode:
        if self._check(QueryTokenKind.EXACT):
            self._pop()
            child = self._parse_anchored()
            return ExactNode(child)
        return self._parse_anchored()

    def _parse_not(self) -> QueryNode:
        if self._check(QueryTokenKind.NOT):
            self._pop()
            child = self._parse_exact()
            return NotNode(child)
        return self._parse_exact()

    def _parse_near_range(self) -> tuple[int | None, int | None]:
        if self._check(QueryTokenKind.COLON):
            self._pop()
            second = self._expect(QueryTokenKind.NUMBER)
            return None, int(second.value)

        first = self._expect(QueryTokenKind.NUMBER)
        if self._check(QueryTokenKind.ANGLE_CLOSE):
            return None, int(first.value)

        self._expect(QueryTokenKind.COLON)

        if self._check(QueryTokenKind.ANGLE_CLOSE):
            return int(first.value), None

        second = self._expect(QueryTokenKind.NUMBER)
        return int(first.value), int(second.value)

    def _parse_positional(self) -> QueryNode:
        lhs = self._parse_not()
        if self._check(QueryTokenKind.PRECEDES):
            self._pop()
            rhs = self._parse_not()
            return PrecedesNode(lhs, rhs)
        if self._check(QueryTokenKind.ANGLE_OPEN):
            self._pop()
            min_dist, max_dist = self._parse_near_range()
            self._expect(QueryTokenKind.ANGLE_CLOSE)
            rhs = self._parse_not()
            return NearNode(lhs, rhs, min_dist, max_dist)
        return lhs

    def _parse_exp_and(self) -> QueryNode:
        lhs = self._parse_positional()
        if not self._check(QueryTokenKind.AND):
            return lhs

        children: list[QueryNode] = [lhs]
        while self._check(QueryTokenKind.AND):
            self._pop()
            rhs = self._parse_positional()
            children.append(rhs)
        return AndNode(children)

    def _parse_or(self) -> QueryNode:
        lhs = self._parse_exp_and()
        if not self._check(QueryTokenKind.OR):
            return lhs
        
        children: list[QueryNode] = [lhs]
        while self._check(QueryTokenKind.OR):
            self._pop()
            rhs = self._parse_exp_and()
            children.append(rhs)
        return OrNode(children)

    def _parse_imp_and(self) -> QueryNode:
        lhs = self._parse_or()
        if self._check(QueryTokenKind.EOF):
            return lhs
        if self._check(QueryTokenKind.RPAREN):
            return lhs

        children: list[QueryNode] = [lhs]
        while not self._check(QueryTokenKind.EOF):
            if self._check(QueryTokenKind.RPAREN):
                break
            rhs = self._parse_or()
            children.append(rhs)
        return AndNode(children)

    def parse(self, tokens: list[QueryToken]) -> QueryNode:
        self._reset(tokens)
        if self._check(QueryTokenKind.EOF):
            raise QueryParserError('Empty query')

        root = self._parse_imp_and()
        if not self._check(QueryTokenKind.EOF):
            token   = self._pop()
            message = f'Unexpected token {token.kind} with value {token.value}'
            raise QueryParserError(message)

        return root
