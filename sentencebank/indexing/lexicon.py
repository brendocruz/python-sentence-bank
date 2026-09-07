from enum import IntEnum

type LexiconEntry = list[int]


class _EntryAttribute(IntEnum):
    DOCUMENT_FREQUENCY   = 0
    COLLECTION_FREQUENCY = 1


class Lexicon:
    _entries: dict[str, LexiconEntry]

    def __init__(self, entries: dict[str, LexiconEntry] | None = None) -> None:
        self._entries = entries or {}

    def contains(self, term: str) -> bool:
        return term in self._entries

    def get_doc_freq(self, term: str) -> int:
        entry = self._entries.get(term, None)
        if entry is None:
            return 0
        return entry[_EntryAttribute.DOCUMENT_FREQUENCY]

    def get_col_freq(self, term: str) -> int:
        entry = self._entries.get(term, None)
        if entry is None:
            return 0
        return entry[_EntryAttribute.COLLECTION_FREQUENCY]

    def get_terms(self) -> list[str]:
        return list(self._entries.keys())

    def size(self) -> int:
        return len(self._entries)

    def clear(self) -> None:
        self._entries = {}

    def set_entry(self, term: str, doc_freq: int, col_freq: int) -> None:
        self._entries[term] = [doc_freq, col_freq]
        
    def increment_doc_freq(self, term: str) -> None:
        entry = self._entries.get(term, None)
        if entry is None:
            self.set_entry(term, 1, 0)
            return
        entry[_EntryAttribute.DOCUMENT_FREQUENCY] += 1
        
    def decrement_doc_freq(self, term: str) -> None:
        entry = self._entries.get(term, None)
        if entry is None:
            return
        if entry[_EntryAttribute.DOCUMENT_FREQUENCY] == 0:
            return 
        entry[_EntryAttribute.DOCUMENT_FREQUENCY] -= 1

    def increment_col_freq(self, term: str) -> None:
        entry = self._entries.get(term, None)
        if entry is None:
            self.set_entry(term, 0, 1)
            return
        entry[_EntryAttribute.COLLECTION_FREQUENCY] += 1

    def decrement_col_freq(self, term: str) -> None:
        entry = self._entries.get(term, None)
        if entry is None:
            return
        if entry[_EntryAttribute.COLLECTION_FREQUENCY] == 0:
            return 
        entry[_EntryAttribute.COLLECTION_FREQUENCY] -= 1
