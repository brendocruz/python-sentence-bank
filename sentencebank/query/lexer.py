from sentencebank.query.tokens import QueryToken, QueryTokenKind
import unicodedata


class QueryLexer:
    _separators: str
    _query:      str
    _length:     int
    _cursor:     int

    WILDCARDS = '*?'
    SYMBOLS   = '&|~=<>:()"^$'

    def __init__(self, separators: str = '') -> None:
        self._separators = separators
        self._query      = ''
        self._length     = 0
        self._cursor     = 0

    def _is_word_char(self, char: str) -> bool:
        return char != '' and unicodedata.category(char).startswith('L')

    def _is_digit_char(self, char: str) -> bool:
        return char != '' and unicodedata.category(char) == 'Nd'

    def _is_wildcard(self, char: str) -> bool:
        return char != '' and char in self.WILDCARDS

    def _is_separator(self, char: str) -> bool:
        return char != '' and char in self._separators

    def _at_eof(self) -> bool:
        if self._cursor < self._length:
            return False
        return True

    def _peek(self, offset = 0) -> str:
        if self._cursor + offset < self._length:
            return self._query[self._cursor + offset]
        return ''

    def _advance(self) -> None:
        if self._cursor < self._length:
            self._cursor += 1

    def _reset(self, query: str) -> None:
        self._query   = query
        self._length = len(query)
        self._cursor = 0

    def _should_consume_separators(self, start_index: int) -> bool:
        index = start_index
        while index < self._length:
            char = self._query[index]
            if not self._is_separator(char):
                break
            index += 1

        if index >= self._length:
            return False

        char = self._query[index]
        if self._is_wildcard(char) or self._is_word_char(char) or self._is_digit_char(char):
            return True

        return False

    def _read_term_or_number(self) -> QueryToken:
        has_wildcard  = False
        has_non_digit = False
        has_separator = False

        start = self._cursor
        while not self._at_eof():
            char = self._peek()

            is_digit     = self._is_digit_char(char)
            is_wildcard  = self._is_wildcard(char)
            is_word_char = self._is_word_char(char)
            is_term_char = is_word_char or is_wildcard
            is_separator = start < self._cursor and self._is_separator(char)

            # Breaks if the current character is not consumable by this method.
            if not is_digit and not is_term_char and not is_separator:
                break

            next_char = self._peek(1)

            is_next_digit     = self._is_digit_char(next_char)
            is_next_wildcard  = self._is_wildcard(next_char)
            is_next_word_char = self._is_word_char(next_char)
            is_next_term_char = is_next_word_char or is_next_wildcard
            is_next_separator = self._is_separator(next_char)

            # Breaks if the current character is a separator candidate and the
            # next one is not another separator nor a valid character in a term.
            if is_separator and not is_next_separator:
                if not is_next_term_char and not is_next_digit:
                    break

            if is_separator and is_next_separator:
                if not self._should_consume_separators(self._cursor):
                    break

            self._advance()

            if is_wildcard:
                has_wildcard = True

            if not is_digit:
                has_non_digit = True

            if is_separator:
                has_separator = True
        end = self._cursor

        value = self._query[start:end]

        kind: QueryTokenKind
        if has_wildcard:
            kind = QueryTokenKind.WTERM
        elif has_separator:
            kind = QueryTokenKind.TERM
        elif not has_non_digit:
            kind = QueryTokenKind.NUMBER
        else:
            kind = QueryTokenKind.TERM

        return QueryToken(kind=kind, value=value, start=start, end=end)

    def _read_angle(self) -> QueryToken:
        start = self._cursor
        self._advance()
        if self._peek() == '<':
            self._advance()
            end = self._cursor
            return QueryToken(kind=QueryTokenKind.PRECEDES, value='<<', start=start, end=end)
        end = self._cursor
        return QueryToken(kind=QueryTokenKind.ANGLE_OPEN, value='<', start=start, end=end)

    def _read_symbol(self) -> QueryToken:
        char = self._peek()

        if char == '<':
            return self._read_angle()

        start = self._cursor

        kind: QueryTokenKind
        if char == '&':
            kind = QueryTokenKind.AND
        elif char == '|':
            kind = QueryTokenKind.OR
        elif char == '~':
            kind = QueryTokenKind.NOT
        elif char == '=':
            kind = QueryTokenKind.EXACT
        elif char == '(':
            kind = QueryTokenKind.LPAREN
        elif char == ')':
            kind = QueryTokenKind.RPAREN
        elif char == '"':
            kind = QueryTokenKind.QUOTE
        elif char == ':':
            kind = QueryTokenKind.COLON
        elif char == '>':
            kind = QueryTokenKind.ANGLE_CLOSE
        elif char == '^':
            kind = QueryTokenKind.CARET
        else:
            kind = QueryTokenKind.DOLLAR

        self._advance()
        end = self._cursor

        return QueryToken(kind=kind, value=char, start=start, end=end)

    def _read(self) -> QueryToken:
        while not self._at_eof():
            char = self._peek()

            if char in self.SYMBOLS:
                return self._read_symbol()
            if char in self.WILDCARDS:
                return self._read_term_or_number()
            if self._is_digit_char(char):
                return self._read_term_or_number()
            if self._is_word_char(char):
                return self._read_term_or_number()

            self._advance()

        start = end = self._cursor
        return QueryToken(kind=QueryTokenKind.EOF, value='', start=start, end=end)

    def tokenize(self, text: str) -> list[QueryToken]:
        self._reset(text)
        tokens: list[QueryToken] = []

        while (token := self._read()).kind != QueryTokenKind.EOF:
            tokens.append(token)

        self._advance()
        start = self._cursor
        end   = self._cursor
        token = QueryToken(kind=QueryTokenKind.EOF, value='', start=start, end=end)
        tokens.append(token)

        return tokens
