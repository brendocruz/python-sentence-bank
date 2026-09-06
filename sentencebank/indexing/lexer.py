from sentencebank.indexing.tokens import IndexingToken
import unicodedata


class IndexingLexer:
    _separators: str
    _document:   str
    _length:     int
    _cursor:     int
    _position:   int

    def __init__(self, separators: str) -> None:
        self._separators = separators
        self._document   = ''
        self._length     = 0
        self._cursor     = 0
        self._position   = 0

    def _is_word_char(self, char: str) -> bool:
        if char == '':
            return False
        if unicodedata.category(char).startswith('L'):
            return True
        return unicodedata.category(char) == 'Nd'

    def _is_separator(self, char: str) -> bool:
        return char != '' and char in self._separators

    def _at_eof(self) -> bool:
        if self._cursor < self._length:
            return False
        return True

    def _peek(self, offset = 0) -> str:
        if self._cursor + offset < self._length:
            return self._document[self._cursor + offset]
        return ''

    def _advance(self) -> None:
        if self._cursor < self._length:
            self._cursor += 1

    def _reset(self, document: str) -> None:
        self._document = document
        self._length   = len(document)
        self._cursor   = 0
        self._position = 0

    def _should_consume_separators(self, start_index: int) -> bool:
        index = start_index
        while index < self._length:
            char = self._document[index]
            if not self._is_separator(char):
                break
            index += 1

        if index >= self._length:
            return False

        char = self._document[index]
        if self._is_word_char(char):
            return True

        return False

    def _read(self) -> IndexingToken:
        while not self._at_eof():
            char = self._peek()
            if self._is_word_char(char):
                break
            self._advance()

        has_word_char = False

        start = self._cursor
        while not self._at_eof():
            char      = self._peek()
            next_char = self._peek(1)

            is_word_char      = self._is_word_char(char)
            is_separator      = start < self._cursor and self._is_separator(char)
            is_next_word_char = self._is_word_char(next_char)
            is_next_separator = self._is_separator(next_char)

            if not is_word_char and not is_separator:
                break

            if is_separator and not is_next_separator and not is_next_word_char:
                break

            if is_separator and is_next_separator:
                if not self._should_consume_separators(self._cursor):
                    break

            self._advance()

            if is_word_char:
                has_word_char = True
        end = self._cursor

        value    = self._document[start:end] if has_word_char else ''
        start    = end if not has_word_char else start
        position = self._position

        self._position += 1
        return IndexingToken(value=value, position=position, start=start, end=end)

    def tokenize(self, document: str) -> list[IndexingToken]:
        self._reset(document)
        tokens: list[IndexingToken] = []

        if self._document == '':
            return tokens

        while (token := self._read()).value != '':
            tokens.append(token)

        return tokens
