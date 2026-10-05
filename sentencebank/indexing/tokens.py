from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class IndexingToken:
    value:    str
    position: int
    start:    int
    end:      int
