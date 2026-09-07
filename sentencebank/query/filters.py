from sentencebank.query.tokens import QueryToken, QueryTokenKind
import unicodedata


class CaseFoldingFilter:

    def process(self, tokens: list[QueryToken]) -> list[QueryToken]:
        for token in tokens:
            if token.kind != QueryTokenKind.TERM and token.kind != QueryTokenKind.WTERM:
                continue
            normalized  = unicodedata.normalize('NFC', token.value).casefold()
            token.value = normalized
        return tokens


class ProtectedTermsFilter:
    _terms:     list[str]
    _tokens:    list[QueryToken]
    _query:     str
    _query_len: int
    _cursor:    int
    _length:    int

    def _is_word_char(self, char: str) -> bool:
        category = unicodedata.category(char)
        return category.startswith('L') or category == 'Nd'

    def __init__(self, terms: list[str]) -> None:
        # The terms are reversed ordered to prevent terms that start with
        # the same sequence of characters from being incorrectly replaced.
        term_set        = { term.casefold() for term in terms }
        self._terms     = sorted(term_set, key=len, reverse=True)
        self._tokens    = []
        self._query     = ''
        self._query_len = 0
        self._cursor    = 0
        self._length    = 0

    def _reset(self, tokens: list[QueryToken], query: str) -> None:
        self._tokens    = tokens
        self._query     = query
        self._query_len = len(query)
        self._cursor    = 0
        self._length    = len(tokens)

    def _find_protected_term(self, token: QueryToken) -> tuple[str, int, int]:
        for term in self._terms:
            term_length = len(term)

            match_start = term.find(token.value)
            if match_start == -1:
                continue

            term_start = token.start - match_start
            term_end   = term_start + term_length

            if term_start < 0 or term_end > self._query_len:
                continue

            slice_text = self._query[term_start:term_end].casefold()
            if slice_text != term:
                continue

            # Check if the character before the matched term is word boundary.
            lower_boundary = term_start - 1
            if lower_boundary >= 0:
                lower_boundary_str = self._query[lower_boundary]
                if self._is_word_char(lower_boundary_str):
                    continue

            # Check if the character after the matched term is word boundary.
            upper_boundary = term_end
            if upper_boundary < self._query_len:
                upper_boundary_str = self._query[upper_boundary]
                if self._is_word_char(upper_boundary_str):
                    continue

            return term, term_start, term_end

        return '', 0, 0

    def process(self, tokens: list[QueryToken], query: str) -> list[QueryToken]:
        self._reset(tokens, query)
        result: list[QueryToken] = []

        while self._cursor < self._length:
            token = self._tokens[self._cursor]

            if token.kind != QueryTokenKind.TERM:
                result.append(token)
                self._cursor += 1
                continue

            term, term_start, term_end = self._find_protected_term(token)
            if term == '':
                result.append(token)
                self._cursor += 1
                continue

            protected_term = QueryToken(kind=token.kind, value=term,
                                        start=term_start, end=term_end)
            result.append(protected_term)
            self._cursor += 1

            while self._cursor < self._length:
                next_token = self._tokens[self._cursor]
                if next_token.start >= term_end:
                    break
                self._cursor += 1

        return result
