from dataclasses import dataclass
from enum import Enum, auto


class QueryTokenKind(Enum):
    TERM        = auto() # `cat`, `dog`, `apple`.
    WTERM       = auto() # `*tion`, `post*`, `post*tion`
    NUMBER      = auto() # 6, 7, 12.

    PRECEDES    = auto() # `<<`.
    ANGLE_OPEN  = auto() # `<`.
    ANGLE_CLOSE = auto() # `>`.
    COLON       = auto() # `:`.

    AND         = auto() # `&`.
    OR          = auto() # `|`.
    NOT         = auto() # `-`.
    EXACT       = auto() # `=`.
    CARET       = auto() # `^`.
    DOLLAR      = auto() # `$`.

    LPAREN      = auto() # `(`.
    RPAREN      = auto() # `)`.
    QUOTE       = auto() # `"`.

    EOF         = auto() # End of the query string.


@dataclass(kw_only=True)
class QueryToken:
    kind:     QueryTokenKind
    value:    str
    start:    int
    end:      int
