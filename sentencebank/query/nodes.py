from sentencebank.query.tokens import QueryToken, QueryTokenKind
from dataclasses import dataclass


@dataclass
class QueryNode:
    pass


@dataclass
class TermNode(QueryNode):
    token: QueryToken

    def is_wildcard(self) -> bool:
        return self.token.kind == QueryTokenKind.WTERM


@dataclass
class PhraseNode(QueryNode):
    children: list[TermNode]


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
class ExactNode(QueryNode):
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
