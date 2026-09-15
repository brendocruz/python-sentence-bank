from sentencebank.indexing.types import TermID
from enum import IntEnum
from typing import TypedDict, cast

type LexiconEntry   = list[TermID | int]
type LexiconTermMap = dict[str, LexiconEntry]
type LexiconIDMap   = dict[TermID, str]


class LexiconData(TypedDict):
    entries: LexiconTermMap
    term_ids: LexiconIDMap
    next_id: int


class _Attribute(IntEnum):
    TERM_ID              = 0
    DOCUMENT_FREQUENCY   = 1
    COLLECTION_FREQUENCY = 2


class Lexicon:
    _data: LexiconData

    def __init__(self) -> None:
        data: LexiconData = {'entries': {}, 'term_ids': {}, 'next_id': 1}
        self._data = data

    def contains(self, term: str) -> bool:
        return term in self._data['entries']

    def get_term(self, term_id: TermID) -> str | None:
        return self._data['term_ids'].get(term_id, None)

    def get_term_id(self, term: str) -> TermID | None:
        entry = self._data['entries'].get(term, None)
        if entry is None:
            return None
        return entry[_Attribute.TERM_ID]

    def get_doc_freq(self, term: str) -> int:
        entry = self._data['entries'].get(term, None)
        if entry is None:
            return 0
        return entry[_Attribute.DOCUMENT_FREQUENCY]

    def get_col_freq(self, term: str) -> int:
        entry = self._data['entries'].get(term, None)
        if entry is None:
            return 0
        return entry[_Attribute.COLLECTION_FREQUENCY]

    def get_terms(self) -> list[str]:
        return list(self._data['entries'].keys())

    def size(self) -> int:
        return len(self._data['entries'])

    def clear(self) -> None:
        self._data['entries'] = {}
        self._data['next_id'] = 1

    def set_entry(self, term: str, doc_freq: int, col_freq: int) -> TermID:
        entry = self._data['entries'].get(term, None)
        if entry is not None:
            term_id = entry[_Attribute.TERM_ID]
            entry[_Attribute.DOCUMENT_FREQUENCY]   = doc_freq
            entry[_Attribute.COLLECTION_FREQUENCY] = col_freq

            self._data['term_ids'][term_id] = term
            return term_id

        term_id = cast(TermID, self._data['next_id'])
        entry   = [term_id, doc_freq, col_freq]
        self._data['entries'][term] = entry
        self._data['term_ids'][term_id] = term
        self._data['next_id'] = term_id + 1
        return term_id
        
    def increment_doc_freq(self, term: str) -> None:
        entry = self._data['entries'].get(term, None)
        if entry is None:
            self.set_entry(term, 1, 0)
            return
        entry[_Attribute.DOCUMENT_FREQUENCY] += 1
        
    def decrement_doc_freq(self, term: str) -> None:
        entry = self._data['entries'].get(term, None)
        if entry is None:
            return
        if entry[_Attribute.DOCUMENT_FREQUENCY] == 0:
            return 
        entry[_Attribute.DOCUMENT_FREQUENCY] -= 1

    def increment_col_freq(self, term: str) -> None:
        entry = self._data['entries'].get(term, None)
        if entry is None:
            self.set_entry(term, 0, 1)
            return
        entry[_Attribute.COLLECTION_FREQUENCY] += 1

    def decrement_col_freq(self, term: str) -> None:
        entry = self._data['entries'].get(term, None)
        if entry is None:
            return
        if entry[_Attribute.COLLECTION_FREQUENCY] == 0:
            return 
        entry[_Attribute.COLLECTION_FREQUENCY] -= 1
