from sentencebank.query.tokens import QueryToken, QueryTokenKind


class QueryLexer:
    alphabet: str
    _text:    str
    _length:  int
    _cursor:  int

    def __init__(self, alphabet: str) -> None:
        self.alphabet = alphabet
        self._text    = ''
        self._length  = 0
        self._cursor  = 0

    def _peek(self) -> str:
        if self._cursor < self._length:
            return self._text[self._cursor]
        return ''

    def _pop(self) -> str:
        if self._cursor < self._length:
            char = self._text[self._cursor]
            self._cursor += 1
            return char
        return ''

    def _reset(self, text: str) -> None:
        self._text   = text
        self._length = len(text)
        self._cursor = 0

    def _skip_whitespace(self) -> None:
        while self._peek().isspace():
            self._pop()

    def _read_term(self) -> QueryToken:
        chars: list[str] = []
        has_wildcard     = False

        start = self._cursor
        while (char := self._peek()) != '':
            if char in self.alphabet:
                self._pop()
                chars.append(char)
                continue
            if char == '*':
                has_wildcard = True
                self._pop()
                chars.append(char)
                continue
            if char == '?':
                has_wildcard = True
                self._pop()
                chars.append(char)
                continue
            break
        end = self._cursor

        term  = ''.join(chars)
        kind  = QueryTokenKind.WTERM if has_wildcard else QueryTokenKind.TERM
        token = QueryToken(kind=kind, value=term, start=start, end=end)
        return token

    def _read_angle(self) -> QueryToken:
        start = self._cursor
        self._pop()
        if self._peek() == '<':
            self._pop()
            end = self._cursor
            return QueryToken(kind=QueryTokenKind.PRECEDES, value='<<', start=start, end=end)
        end = self._cursor
        return QueryToken(kind=QueryTokenKind.ANGLE_OPEN, value='<', start=start, end=end)

    def _read(self):
        char = self._peek()
        if char == '':
            start = self._cursor
            end   = self._cursor
            return QueryToken(kind=QueryTokenKind.EOF, value='', start=start, end=end)
        if char == '&':
            start = self._cursor
            self._pop()
            end   = self._cursor
            return QueryToken(kind=QueryTokenKind.AND, value='&', start=start, end=end)
        if char == '|':
            start = self._cursor
            self._pop()
            end   = self._cursor
            return QueryToken(kind=QueryTokenKind.OR, value='|', start=start, end=end)
        if char == '~':
            start = self._cursor
            self._pop()
            end   = self._cursor
            return QueryToken(kind=QueryTokenKind.NOT, value='~', start=start, end=end)
        if char == '=':
            start = self._cursor
            self._pop()
            end   = self._cursor
            return QueryToken(kind=QueryTokenKind.EXACT, value='=', start=start, end=end)
        if char == '(':
            start = self._cursor
            self._pop()
            end   = self._cursor
            return QueryToken(kind=QueryTokenKind.LPAREN, value='(', start=start, end=end)
        if char == ')':
            start = self._cursor
            self._pop()
            end   = self._cursor
            return QueryToken(kind=QueryTokenKind.RPAREN, value=')', start=start, end=end)
        if char == '"':
            start = self._cursor
            self._pop()
            end   = self._cursor
            return QueryToken(kind=QueryTokenKind.QUOTE, value='"', start=start, end=end)
        if char == ',':
            start = self._cursor
            self._pop()
            end   = self._cursor
            return QueryToken(kind=QueryTokenKind.COMMA, value=',', start=start, end=end)
        if char == '<':
            return self._read_angle()
        if char == '>':
            start = self._cursor
            self._pop()
            end   = self._cursor
            return QueryToken(kind=QueryTokenKind.ANGLE_CLOSE, value='>', start=start, end=end)
        if char == '^':
            start = self._cursor
            self._pop()
            end   = self._cursor
            return QueryToken(kind=QueryTokenKind.CARET, value='^', start=start, end=end)
        if char == '$':
            start = self._cursor
            self._pop()
            end   = self._cursor
            return QueryToken(kind=QueryTokenKind.DOLLAR, value='$', start=start, end=end)
        if char.isspace():
            self._skip_whitespace()
            return self._read()

        return self._read_term()

    def tokenize(self, text: str) -> list[QueryToken]:
        self._reset(text)
        tokens: list[QueryToken] = []

        while (token := self._read()).kind != QueryTokenKind.EOF:
            tokens.append(token)

        self._pop()
        start = self._cursor
        end   = self._cursor
        token = QueryToken(kind=QueryTokenKind.EOF, value='', start=start, end=end)
        tokens.append(token)

        return tokens
