from sentencebank.query.parser import QueryParser, QueryParserError
from sentencebank.query.nodes import (
    AndNode, EndsWithNode, ExactNode,
    NearNode, NotNode, OrNode, PhraseNode,
    PrecedesNode, StartsWithNode, TermNode
)
from sentencebank.query.tokens import QueryToken, QueryTokenKind
from pytest import raises


class TestQueryParser:

    def test_parse_empty_query(self):
        token1 = QueryToken(kind=QueryTokenKind.EOF, value='', start=0, end=0)
        tokens = [token1]

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_term(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='cat', start=0, end=3)
        token2 = QueryToken(kind=QueryTokenKind.EOF,  value='',    start=3, end=3)
        tokens = [token1, token2]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        term = ast
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'cat'

    def test_parse_phrase_with_single_term(self):
        token1 = QueryToken(kind=QueryTokenKind.QUOTE, value='"',     start=0, end=1)
        token2 = QueryToken(kind=QueryTokenKind.TERM,  value='apple', start=0, end=6)
        token3 = QueryToken(kind=QueryTokenKind.QUOTE, value='"',     start=6, end=7)
        token4 = QueryToken(kind=QueryTokenKind.EOF,   value='',      start=7, end=7)
        tokens = [token1, token2, token3, token4]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        phrase = ast
        assert isinstance(phrase, PhraseNode)
        assert len(phrase.children) == 1

        term = phrase.children[0]
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'apple'

    def test_parse_phrase_with_multiple_terms(self):
        token1 = QueryToken(kind=QueryTokenKind.QUOTE, value='"',       start=0,  end=1)
        token2 = QueryToken(kind=QueryTokenKind.TERM,  value='perfect', start=1,  end=8)
        token3 = QueryToken(kind=QueryTokenKind.TERM,  value='apple',   start=9,  end=14)
        token4 = QueryToken(kind=QueryTokenKind.TERM,  value='pie',     start=15, end=18)
        token5 = QueryToken(kind=QueryTokenKind.QUOTE, value='"',       start=19, end=20)
        token6 = QueryToken(kind=QueryTokenKind.EOF,   value='',        start=20, end=20)
        tokens = [token1, token2, token3, token4, token5, token6]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        phrase = ast
        assert isinstance(phrase, PhraseNode)
        assert len(phrase.children) == 3

        term = phrase.children[0]
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'perfect'

        term = phrase.children[1]
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'apple'

        term = phrase.children[2]
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'pie'

    def test_parse_nested_with_single_term(self):
        token1 = QueryToken(kind=QueryTokenKind.LPAREN, value='(',     start=0, end=1)
        token2 = QueryToken(kind=QueryTokenKind.TERM,   value='apple', start=1, end=6)
        token3 = QueryToken(kind=QueryTokenKind.RPAREN, value=')',     start=6, end=7)
        token4 = QueryToken(kind=QueryTokenKind.EOF,    value='',      start=7, end=7)
        tokens = [token1, token2, token3, token4]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        term = ast
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'apple'

    def test_parse_nested_with_multiple_terms(self):
        token1 = QueryToken(kind=QueryTokenKind.LPAREN, value='(',       start=0,  end=1)
        token2 = QueryToken(kind=QueryTokenKind.TERM,   value='perfect', start=1,  end=8)
        token3 = QueryToken(kind=QueryTokenKind.TERM,   value='apple',   start=9,  end=13)
        token4 = QueryToken(kind=QueryTokenKind.TERM,   value='pie',     start=14, end=17)
        token5 = QueryToken(kind=QueryTokenKind.RPAREN, value=')',       start=17, end=18)
        token6 = QueryToken(kind=QueryTokenKind.EOF,    value='',        start=18, end=18)
        tokens = [token1, token2, token3, token4, token5, token6]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        andn = ast
        assert isinstance(andn, AndNode)
        assert len(andn.children) == 3

        term = andn.children[0]
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'perfect'

        term = andn.children[1]
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'apple'

        term = andn.children[2]
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'pie'

    def test_parse_nested_unclosed(self):
        token1 = QueryToken(kind=QueryTokenKind.LPAREN, value='(',    start=0,  end=1)
        token2 = QueryToken(kind=QueryTokenKind.TERM,   value='cat',  start=1,  end=4)
        token3 = QueryToken(kind=QueryTokenKind.TERM,   value='dog',  start=5,  end=8)
        token4 = QueryToken(kind=QueryTokenKind.TERM,   value='fish', start=9,  end=13)
        token5 = QueryToken(kind=QueryTokenKind.EOF,    value='',     start=13, end=13)
        tokens = [token1, token2, token3, token4, token5]

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_nested_unopen_but_closed(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM,   value='cat',  start=0,  end=3)
        token2 = QueryToken(kind=QueryTokenKind.TERM,   value='dog',  start=4,  end=7)
        token3 = QueryToken(kind=QueryTokenKind.TERM,   value='fish', start=8,  end=12)
        token4 = QueryToken(kind=QueryTokenKind.RPAREN, value=')',    start=12, end=13)
        token5 = QueryToken(kind=QueryTokenKind.EOF,    value='',     start=13, end=13)
        tokens = [token1, token2, token3, token4, token5]

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_anchored_starts_with(self):
        token1 = QueryToken(kind=QueryTokenKind.CARET, value='^',   start=0, end=1)
        token2 = QueryToken(kind=QueryTokenKind.TERM,  value='you', start=1, end=4)
        token3 = QueryToken(kind=QueryTokenKind.EOF,   value='',    start=4, end=4)
        tokens = [token1, token2, token3]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        starts = ast
        assert isinstance(starts, StartsWithNode)

        term = starts.child
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'you'

    def test_parse_anchored_ends_with(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM,   value='him', start=0, end=3)
        token2 = QueryToken(kind=QueryTokenKind.DOLLAR, value='$',   start=3, end=4)
        token3 = QueryToken(kind=QueryTokenKind.EOF,    value='',    start=4, end=4)
        tokens = [token1, token2, token3]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        ends = ast
        assert isinstance(ends, EndsWithNode)

        term = ends.child
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'him'

    def test_parse_anchored_leading_ends_with(self):
        token1 = QueryToken(kind=QueryTokenKind.DOLLAR, value='$',   start=0, end=1)
        token2 = QueryToken(kind=QueryTokenKind.TERM,   value='you', start=1, end=4)
        token3 = QueryToken(kind=QueryTokenKind.EOF,    value='',    start=4, end=4)
        tokens = [token1, token2, token3]

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_anchored_trailing_starts_with(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM,  value='him', start=0, end=3)
        token2 = QueryToken(kind=QueryTokenKind.CARET, value='^',   start=3, end=4)
        token3 = QueryToken(kind=QueryTokenKind.EOF,   value='',    start=4, end=4)
        tokens = [token1, token2, token3]

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_anchored_starts_with_and_ends_with(self):
        token1 = QueryToken(kind=QueryTokenKind.CARET,  value='^',   start=0, end=1)
        token2 = QueryToken(kind=QueryTokenKind.TERM,   value='him', start=1, end=4)
        token3 = QueryToken(kind=QueryTokenKind.DOLLAR, value='$',   start=4, end=5)
        token4 = QueryToken(kind=QueryTokenKind.EOF,    value='',    start=5, end=5)
        tokens = [token1, token2, token3, token4]

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_exact(self):
        token1 = QueryToken(kind=QueryTokenKind.EXACT, value='=',   start=0, end=1)
        token2 = QueryToken(kind=QueryTokenKind.TERM,  value='see', start=1, end=4)
        token3 = QueryToken(kind=QueryTokenKind.EOF,   value='',    start=4, end=4)
        tokens = [token1, token2, token3]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        exact = ast
        assert isinstance(exact, ExactNode)

        term = exact.child
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'see'

    def test_parse_not(self):
        token1 = QueryToken(kind=QueryTokenKind.EXACT, value='-',    start=0, end=1)
        token2 = QueryToken(kind=QueryTokenKind.TERM,  value='have', start=1, end=5)
        token3 = QueryToken(kind=QueryTokenKind.EOF,   value='',     start=5, end=5)
        tokens = [token1, token2, token3]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        notn = ast
        assert isinstance(notn, ExactNode)

        term = notn.child
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'have'

    def test_parse_not_exact(self):
        token1 = QueryToken(kind=QueryTokenKind.NOT,   value='-',  start=0, end=1)
        token2 = QueryToken(kind=QueryTokenKind.EXACT, value='=',  start=1, end=2)
        token3 = QueryToken(kind=QueryTokenKind.TERM,  value='be', start=2, end=4)
        token4 = QueryToken(kind=QueryTokenKind.EOF,   value='',   start=4, end=4)
        tokens = [token1, token2, token3, token4]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        notn = ast
        assert isinstance(notn, NotNode)

        exact = notn.child
        assert isinstance(exact, ExactNode)

        term = exact.child
        assert isinstance(term, TermNode)
        assert term.is_wildcard() == False
        assert term.token.kind    == QueryTokenKind.TERM
        assert term.token.value   == 'be'

    def test_parse_not_not(self):
        token1 = QueryToken(kind=QueryTokenKind.NOT,  value='-',  start=0, end=1)
        token2 = QueryToken(kind=QueryTokenKind.NOT,  value='-',  start=1, end=2)
        token3 = QueryToken(kind=QueryTokenKind.TERM, value='be', start=2, end=4)
        token4 = QueryToken(kind=QueryTokenKind.EOF,  value='',   start=4, end=4)
        tokens = [token1, token2, token3, token4]

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_exact_not(self):
        token1 = QueryToken(kind=QueryTokenKind.EXACT, value='=',  start=0, end=1)
        token2 = QueryToken(kind=QueryTokenKind.NOT,   value='-',  start=1, end=2)
        token3 = QueryToken(kind=QueryTokenKind.TERM,  value='be', start=2, end=4)
        token4 = QueryToken(kind=QueryTokenKind.EOF,   value='',   start=4, end=4)
        tokens = [token1, token2, token3, token4]

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_exact_exact(self):
        token1 = QueryToken(kind=QueryTokenKind.EXACT, value='=',  start=0, end=1)
        token2 = QueryToken(kind=QueryTokenKind.EXACT, value='=',  start=1, end=2)
        token3 = QueryToken(kind=QueryTokenKind.TERM,  value='be', start=2, end=4)
        token4 = QueryToken(kind=QueryTokenKind.EOF,   value='',   start=4, end=4)
        tokens = [token1, token2, token3, token4]

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_precedes(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM,     value='cat', start=0,  end=3)
        token2 = QueryToken(kind=QueryTokenKind.PRECEDES, value='<<',  start=4,  end=6)
        token3 = QueryToken(kind=QueryTokenKind.TERM,     value='dog', start=7,  end=10)
        token4 = QueryToken(kind=QueryTokenKind.EOF,      value='',    start=10, end=10)
        tokens = [token1, token2, token3, token4]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        precedes = ast
        assert isinstance(precedes, PrecedesNode)

        term1 = precedes.left
        assert isinstance(term1, TermNode)
        assert term1.is_wildcard() == False
        assert term1.token.kind    == QueryTokenKind.TERM
        assert term1.token.value   == 'cat'

        term2 = precedes.right
        assert isinstance(term2, TermNode)
        assert term2.is_wildcard() == False
        assert term2.token.kind    == QueryTokenKind.TERM
        assert term2.token.value   == 'dog'

    def test_parse_near_with_both_boundaries(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM,        value='cat', start=0,  end=3)
        token2 = QueryToken(kind=QueryTokenKind.ANGLE_OPEN,  value='<',   start=4,  end=5)
        token3 = QueryToken(kind=QueryTokenKind.NUMBER,      value='3',   start=5,  end=6)
        token4 = QueryToken(kind=QueryTokenKind.COLON,       value=':',   start=6,  end=7)
        token5 = QueryToken(kind=QueryTokenKind.NUMBER,      value='6',   start=7,  end=8)
        token6 = QueryToken(kind=QueryTokenKind.ANGLE_CLOSE, value='>',   start=8,  end=9)
        token7 = QueryToken(kind=QueryTokenKind.TERM,        value='dog', start=10, end=13)
        token8 = QueryToken(kind=QueryTokenKind.EOF,         value='',    start=13, end=13)
        tokens = [token1, token2, token3, token4, token5, token6, token7, token8]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        near = ast
        assert isinstance(near, NearNode)
        assert near.min_dist == 3
        assert near.max_dist == 6

        term1 = near.left
        assert isinstance(term1, TermNode)
        assert term1.is_wildcard() == False
        assert term1.token.kind    == QueryTokenKind.TERM
        assert term1.token.value   == 'cat'

        term2 = near.right
        assert isinstance(term2, TermNode)
        assert term2.is_wildcard() == False
        assert term2.token.kind    == QueryTokenKind.TERM
        assert term2.token.value   == 'dog'

    def test_parse_near_with_lower_boundary(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM,        value='cat', start=0,  end=3)
        token2 = QueryToken(kind=QueryTokenKind.ANGLE_OPEN,  value='<',   start=4,  end=5)
        token3 = QueryToken(kind=QueryTokenKind.NUMBER,      value='2',   start=5,  end=6)
        token4 = QueryToken(kind=QueryTokenKind.COLON,       value=':',   start=6,  end=7)
        token5 = QueryToken(kind=QueryTokenKind.ANGLE_CLOSE, value='>',   start=7,  end=8)
        token6 = QueryToken(kind=QueryTokenKind.TERM,        value='dog', start=9,  end=12)
        token7 = QueryToken(kind=QueryTokenKind.EOF,         value='',    start=12, end=12)
        tokens = [token1, token2, token3, token4, token5, token6, token7]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        near = ast
        assert isinstance(near, NearNode)
        assert near.min_dist == 2
        assert near.max_dist is None

        term1 = near.left
        assert isinstance(term1, TermNode)
        assert term1.is_wildcard() == False
        assert term1.token.kind    == QueryTokenKind.TERM
        assert term1.token.value   == 'cat'

        term2 = near.right
        assert isinstance(term2, TermNode)
        assert term2.is_wildcard() == False
        assert term2.token.kind    == QueryTokenKind.TERM
        assert term2.token.value   == 'dog'

    def test_parse_near_with_upper_boundary(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM,        value='cat', start=0,  end=3)
        token2 = QueryToken(kind=QueryTokenKind.ANGLE_OPEN,  value='<',   start=4,  end=5)
        token3 = QueryToken(kind=QueryTokenKind.COLON,       value=':',   start=5,  end=6)
        token4 = QueryToken(kind=QueryTokenKind.NUMBER,      value='5',   start=6,  end=7)
        token5 = QueryToken(kind=QueryTokenKind.ANGLE_CLOSE, value='>',   start=7,  end=8)
        token6 = QueryToken(kind=QueryTokenKind.TERM,        value='dog', start=9,  end=12)
        token7 = QueryToken(kind=QueryTokenKind.EOF,         value='',    start=12, end=12)
        tokens = [token1, token2, token3, token4, token5, token6, token7]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        near = ast
        assert isinstance(near, NearNode)
        assert near.min_dist is None
        assert near.max_dist == 5

        term1 = near.left
        assert isinstance(term1, TermNode)
        assert term1.is_wildcard() == False
        assert term1.token.kind    == QueryTokenKind.TERM
        assert term1.token.value   == 'cat'

        term2 = near.right
        assert isinstance(term2, TermNode)
        assert term2.is_wildcard() == False
        assert term2.token.kind    == QueryTokenKind.TERM
        assert term2.token.value   == 'dog'

    def test_parse_near_with_single_number(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM,        value='cat', start=0,  end=3)
        token2 = QueryToken(kind=QueryTokenKind.ANGLE_OPEN,  value='<',   start=4,  end=5)
        token3 = QueryToken(kind=QueryTokenKind.NUMBER,      value='7',   start=5,  end=6)
        token4 = QueryToken(kind=QueryTokenKind.ANGLE_CLOSE, value='>',   start=6,  end=7)
        token5 = QueryToken(kind=QueryTokenKind.TERM,        value='dog', start=8,  end=11)
        token6 = QueryToken(kind=QueryTokenKind.EOF,         value='',    start=11, end=11)
        tokens = [token1, token2, token3, token4, token5, token6]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        near = ast
        assert isinstance(near, NearNode)
        assert near.min_dist is None
        assert near.max_dist == 7

        term1 = near.left
        assert isinstance(term1, TermNode)
        assert term1.is_wildcard() == False
        assert term1.token.kind    == QueryTokenKind.TERM
        assert term1.token.value   == 'cat'

        term2 = near.right
        assert isinstance(term2, TermNode)
        assert term2.is_wildcard() == False
        assert term2.token.kind    == QueryTokenKind.TERM
        assert term2.token.value   == 'dog'

    def test_parse_exp_and(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='cat', start=0, end=3)
        token2 = QueryToken(kind=QueryTokenKind.AND,  value='&',   start=4, end=5)
        token3 = QueryToken(kind=QueryTokenKind.TERM, value='dog', start=6, end=9)
        token4 = QueryToken(kind=QueryTokenKind.EOF,  value='',    start=9, end=9)
        tokens = [token1, token2, token3, token4]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        andn = ast
        assert isinstance(andn, AndNode)
        assert len(andn.children) == 2

        term1 = andn.children[0]
        assert isinstance(term1, TermNode)
        assert term1.is_wildcard() == False
        assert term1.token.kind    == QueryTokenKind.TERM
        assert term1.token.value   == 'cat'

        term2 = andn.children[1]
        assert isinstance(term2, TermNode)
        assert term2.is_wildcard() == False
        assert term2.token.kind    == QueryTokenKind.TERM
        assert term2.token.value   == 'dog'

    def test_parse_or(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='cat', start=0, end=3)
        token2 = QueryToken(kind=QueryTokenKind.OR,   value='|',   start=4, end=5)
        token3 = QueryToken(kind=QueryTokenKind.TERM, value='dog', start=6, end=9)
        token4 = QueryToken(kind=QueryTokenKind.EOF,  value='',    start=9, end=9)
        tokens = [token1, token2, token3, token4]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        orn = ast
        assert isinstance(orn, OrNode)
        assert len(orn.children) == 2

        term1 = orn.children[0]
        assert isinstance(term1, TermNode)
        assert term1.is_wildcard() == False
        assert term1.token.kind    == QueryTokenKind.TERM
        assert term1.token.value   == 'cat'

        term2 = orn.children[1]
        assert isinstance(term2, TermNode)
        assert term2.is_wildcard() == False
        assert term2.token.kind    == QueryTokenKind.TERM
        assert term2.token.value   == 'dog'

    def test_parse_imp_and(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='cat', start=0, end=3)
        token2 = QueryToken(kind=QueryTokenKind.TERM, value='dog', start=4, end=7)
        token3 = QueryToken(kind=QueryTokenKind.EOF,  value='',    start=7, end=7)
        tokens = [token1, token2, token3]

        parser = QueryParser()
        ast    = parser.parse(tokens)

        andn = ast
        assert isinstance(andn, AndNode)
        assert len(andn.children) == 2

        term1 = andn.children[0]
        assert isinstance(term1, TermNode)
        assert term1.is_wildcard() == False
        assert term1.token.kind    == QueryTokenKind.TERM
        assert term1.token.value   == 'cat'

        term2 = andn.children[1]
        assert isinstance(term2, TermNode)
        assert term2.is_wildcard() == False
        assert term2.token.kind    == QueryTokenKind.TERM
        assert term2.token.value   == 'dog'
