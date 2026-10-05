from dataclasses import dataclass, field

from sentencebank.indexing.types import TermID


@dataclass
class QueryNode:
    pass


@dataclass(slots=True)
class TermNode(QueryNode):
    value:             str
    is_exact:          bool        = False
    resolved_term_ids: set[TermID] = field(default_factory=set)

 
@dataclass(slots=True)
class PatternNode(QueryNode):
    value:             str
    resolved_term_ids: set[TermID] = field(default_factory=set)


@dataclass
class PhraseNode(QueryNode):
    children: list[QueryNode]


@dataclass
class StartsWithNode(QueryNode):
    child: QueryNode


@dataclass
class EndsWithNode(QueryNode):
    child: QueryNode


@dataclass
class NotNode(QueryNode):
    child: QueryNode


@dataclass
class NearNode(QueryNode):
    left:  QueryNode
    right: QueryNode
    min_dist: int | None
    max_dist: int | None


@dataclass
class PrecedesNode(QueryNode):
    left: QueryNode
    right: QueryNode


@dataclass
class AndNode(QueryNode):
    children: list[QueryNode]


@dataclass
class OrNode(QueryNode):
    children: list[QueryNode]
