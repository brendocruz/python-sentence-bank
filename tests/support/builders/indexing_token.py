from sentencebank.indexing.tokens import IndexingToken
from typing import Self


class IndexingTokenTestBuilder:
    _tokens: list[IndexingToken]
    _is_list: bool

    def __init__(self):
        self._tokens  = []
        self._is_list = False

    def term(self, value: str, position: int, start: int, end: int) -> Self:
        token = IndexingToken(value=value, position=position, start=start, end=end)
        self._tokens.append(token)
        return self

    def list_(self) -> Self:
        self._is_list = True
        return self

    def build(self) -> list[IndexingToken] | IndexingToken:
        if not self._is_list:
            return self._tokens.pop(0)
        self._is_list = False

        tokens = self._tokens
        self._tokens = []
        return tokens

