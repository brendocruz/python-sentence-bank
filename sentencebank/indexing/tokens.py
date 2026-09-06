from dataclasses import dataclass


@dataclass(kw_only=True)
class IndexingToken:
    value:    str
    position: int
    start:    int
    end:      int
