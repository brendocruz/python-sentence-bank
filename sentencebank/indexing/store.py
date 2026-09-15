from sentencebank.indexing.types import DocID
from typing import TypedDict

type SentenceMap = dict[DocID, str]


class DocumentStoreData(TypedDict):
    entries: SentenceMap
    next_id: int


class DocumentStore:
    _data: DocumentStoreData

    def __init__(self):
        self._data = {'entries': {}, 'next_id': 1}

    def add_sentence(self, sentence: str) -> DocID:
        doc_id = self._data['next_id']
        self._data['entries'][doc_id] = sentence
        self._data['next_id'] = doc_id + 1
        return doc_id

    def remove_sentence(self, doc_id: DocID) -> bool:
        return self._data['entries'].pop(doc_id, None) is not None

    def get_sentence(self, doc_id: DocID) -> str | None:
        return self._data['entries'].get(doc_id, None);

    def size(self) -> int:
        return len(self._data['entries'])
