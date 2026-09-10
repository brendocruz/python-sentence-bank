from dataclasses import dataclass
from enum import IntEnum

type TermID = int
type DocID  = int

type PostingEntry = list[int]
type PostingList  = list[PostingEntry]
type PostingMap   = dict[TermID, PostingList]


class _EntryAttribute(IntEnum):
    DOCUMENT_ID  = 0
    POSITION     = 1
    START_OFFSET = 2
    END_OFFSET   = 3


@dataclass(slots=True)
class Posting:
    doc_id: DocID
    position: int
    start: int
    end: int


class InvertedIndex:
    _entries: PostingMap

    def __init__(self, index: PostingMap | None = None) -> None:
        self._entries = index or {}

    def term_count(self) -> int:
        return len(self._entries)

    def clear(self) -> None:
        self._entries.clear()

    def get_posting(self, term_id: TermID, doc_id: DocID, position: int) -> Posting | None:
        posting_list = self._entries.get(term_id, None)
        if posting_list is None:
            return None

        for posting_entry in posting_list:
            if posting_entry[_EntryAttribute.DOCUMENT_ID] != doc_id:
                continue
            if posting_entry[_EntryAttribute.POSITION] != position:
                continue

            return Posting(doc_id=posting_entry[_EntryAttribute.DOCUMENT_ID],
                           position=posting_entry[_EntryAttribute.POSITION],
                           start=posting_entry[_EntryAttribute.START_OFFSET],
                           end=posting_entry[_EntryAttribute.END_OFFSET])
        return None

    def get_postings(self, term_id: TermID) -> list[Posting]:
        posting_list = self._entries.get(term_id, None)
        if posting_list is None:
            return []

        postings: list[Posting] = []
        for posting_entry in posting_list:
            posting = Posting(doc_id=posting_entry[_EntryAttribute.DOCUMENT_ID],
                              position=posting_entry[_EntryAttribute.POSITION],
                              start=posting_entry[_EntryAttribute.START_OFFSET],
                              end=posting_entry[_EntryAttribute.END_OFFSET])
            postings.append(posting)
        return postings

    def remove_posting(self, term_id: TermID, doc_id: DocID, position: int) -> None:
        posting_list = self._entries.get(term_id, None)
        if posting_list is None:
            return

        if len(posting_list) == 1:
            self._entries.pop(term_id)
            return

        for posting_entry in posting_list:
            if posting_entry[_EntryAttribute.DOCUMENT_ID] != doc_id:
                continue
            if posting_entry[_EntryAttribute.POSITION] != position:
                continue
            posting_list.remove(posting_entry)
            break

    def add_posting(self, term_id: TermID, posting: Posting) -> None:
        posting_list = self._entries.get(term_id, None)
        if posting_list is None:
            posting_list = []
            self._entries[term_id] = posting_list

        for posting_entry in posting_list:
            if posting_entry[_EntryAttribute.DOCUMENT_ID] != posting.doc_id:
                continue
            if posting_entry[_EntryAttribute.POSITION] == posting.position:
                return

        posting_entry = [posting.doc_id, posting.position, posting.start, posting.end]
        posting_list.append(posting_entry)

    def contains_posting(self, term_id: TermID, doc_id: DocID, position: int) -> bool:
        posting_list = self._entries.get(term_id, None)
        if posting_list is None:
            return False

        for posting_entry in posting_list:
            if posting_entry[_EntryAttribute.DOCUMENT_ID] != doc_id:
                continue
            if posting_entry[_EntryAttribute.POSITION] != position:
                continue
            return True
        return False

    def contains_term(self, term_id: TermID) -> bool:
        return term_id in self._entries
