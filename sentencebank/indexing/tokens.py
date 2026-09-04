from dataclasses import dataclass


@dataclass(kw_only=True)
class Token:
    text:     str
    position: int
    start:    int
    end:      int
