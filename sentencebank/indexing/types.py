from dataclasses import dataclass

type TermID   = int
type DocID    = int


@dataclass(slots=True, frozen=True)
class Posting:
    doc_id: DocID
    position: int
    start: int
    end: int


@dataclass(slots=True, frozen=True)
class TermCount:
    term_id: TermID
    count:   int


@dataclass(slots=True, frozen=True, order=True)
class TermPosition:
    term_id:  TermID
    position: int


@dataclass(slots=True, frozen=True, order=True)
class TermPosting:
    term_id:  TermID
    posting:  Posting


type TermPositionMap = dict[DocID, list[TermPosition]]
