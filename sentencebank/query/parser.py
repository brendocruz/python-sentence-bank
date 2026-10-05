from sentencebank.query.tokens import QueryToken, QueryTokenKind
from sentencebank.query import nodes as n

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

    def _parse_term(self) -> n.QueryNode:
        token = self._expect(QueryTokenKind.TERM)
        return n.TermNode(token.value)

    def _parse_pattern(self) -> n.QueryNode:
        token = self._expect(QueryTokenKind.PATTERN)
        return n.PatternNode(token.value)

    def _parse_phrase(self) -> n.QueryNode:
        self._expect(QueryTokenKind.QUOTE)
        children: list[n.QueryNode] = []
        while not self._check(QueryTokenKind.QUOTE):
            if self._check(QueryTokenKind.PATTERN):
                child = self._parse_exact()
                children.append(child)
                continue
            child = self._parse_exact()
            children.append(child)
        self._pop()
        return n.PhraseNode(children)

    def _parse_nested(self) -> n.QueryNode:
        self._expect(QueryTokenKind.LPAREN)
        node = self._parse_imp_and()
        self._expect(QueryTokenKind.RPAREN)
        return node

    def _parse_primary(self) -> n.QueryNode:
        if self._check(QueryTokenKind.TERM):
            return self._parse_term()
        if self._check(QueryTokenKind.PATTERN):
            return self._parse_pattern()
        if self._check(QueryTokenKind.QUOTE):
            return self._parse_phrase()
        return self._parse_nested()

    def _parse_anchored(self) -> n.QueryNode:
        if self._check(QueryTokenKind.CARET):
            self._pop()
            child = self._parse_exact()
            return n.StartsWithNode(child)
        child = self._parse_exact()
        if self._check(QueryTokenKind.DOLLAR):
            self._pop()
            return n.EndsWithNode(child)
        return child

    def _mark_exact(self, node: n.QueryNode) -> n.QueryNode:
        match node:
            case n.TermNode():
                node.is_exact = True
            case n.AndNode() | n.OrNode() | n.PhraseNode():
                for child in node.children:
                    self._mark_exact(child)
            case n.StartsWithNode() | n.EndsWithNode() | n.NotNode():
                self._mark_exact(node.child)
            case n.NearNode() | n.PrecedesNode():
                self._mark_exact(node.left)
                self._mark_exact(node.right)
        return node

    def _parse_exact(self) -> n.QueryNode:
        if not self._check(QueryTokenKind.EXACT):
            return self._parse_primary()
        self._pop()
        child = self._parse_primary()
        return self._mark_exact(child)

    def _parse_not(self) -> n.QueryNode:
        if self._check(QueryTokenKind.NOT):
            self._pop()
            child = self._parse_anchored()
            return n.NotNode(child)
        return self._parse_anchored()

    def _parse_near_range(self) -> tuple[int | None, int | None]:
        if self._check(QueryTokenKind.COLON):
            self._pop()
            second = self._expect(QueryTokenKind.NUMBER)
            return None, int(second.value)

        first = self._expect(QueryTokenKind.NUMBER)
        if self._check(QueryTokenKind.RANGLE):
            return None, int(first.value)

        self._expect(QueryTokenKind.COLON)

        if self._check(QueryTokenKind.RANGLE):
            return int(first.value), None

        second = self._expect(QueryTokenKind.NUMBER)
        return int(first.value), int(second.value)

    def _parse_positional(self) -> n.QueryNode:
        lhs = self._parse_not()
        if self._check(QueryTokenKind.PRECEDES):
            self._pop()
            rhs = self._parse_not()
            return n.PrecedesNode(lhs, rhs)
        if self._check(QueryTokenKind.LANGLE):
            self._pop()
            min_dist, max_dist = self._parse_near_range()
            self._expect(QueryTokenKind.RANGLE)
            rhs = self._parse_not()
            return n.NearNode(lhs, rhs, min_dist, max_dist)
        return lhs

    def _parse_exp_and(self) -> n.QueryNode:
        lhs = self._parse_positional()
        if not self._check(QueryTokenKind.AND):
            return lhs

        children: list[n.QueryNode] = [lhs]
        while self._check(QueryTokenKind.AND):
            self._pop()
            rhs = self._parse_positional()
            children.append(rhs)
        return n.AndNode(children)

    def _parse_or(self) -> n.QueryNode:
        lhs = self._parse_exp_and()
        if not self._check(QueryTokenKind.OR):
            return lhs
        
        children: list[n.QueryNode] = [lhs]
        while self._check(QueryTokenKind.OR):
            self._pop()
            rhs = self._parse_exp_and()
            children.append(rhs)
        return n.OrNode(children)

    def _parse_imp_and(self) -> n.QueryNode:
        lhs = self._parse_or()
        if self._check(QueryTokenKind.EOF):
            return lhs
        if self._check(QueryTokenKind.RPAREN):
            return lhs

        children: list[n.QueryNode] = [lhs]
        while not self._check(QueryTokenKind.EOF):
            if self._check(QueryTokenKind.RPAREN):
                break
            rhs = self._parse_or()
            children.append(rhs)
        return n.OrNode(children)

    def parse(self, tokens: list[QueryToken]) -> n.QueryNode:
        self._reset(tokens)
        if self._check(QueryTokenKind.EOF):
            raise QueryParserError('Empty query')

        root = self._parse_imp_and()
        if not self._check(QueryTokenKind.EOF):
            token   = self._pop()
            message = f'Unexpected token {token.kind} with value {token.value}'
            raise QueryParserError(message)

        return root
