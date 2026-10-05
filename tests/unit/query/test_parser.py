from pytest import raises, fixture

from sentencebank.query import nodes as n
from sentencebank.query.parser import QueryParser, QueryParserError
from tests.support.builders.query_token import QueryTokenTestBuilder


class TestQueryParser:
    builder: QueryTokenTestBuilder

    @fixture(autouse=True)
    def setup(self):
        self.builder = QueryTokenTestBuilder()

    def test_parse_raises_error_when_query_is_empty(self):
        tokens = self.builder.many().eof(0).build()
        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_with_term(self):
        tokens = self.builder.many().term('cat', 0, 3).eof(3).build()

        parser = QueryParser()
        ast    = parser.parse(tokens)

        term   = ast
        assert isinstance(term, n.TermNode)
        assert term.value             == 'cat'
        assert term.is_exact          == False
        assert term.resolved_term_ids == set()

    def test_parse_with_pattern(self):
        tokens = self.builder.many().pattern('c?t', 0, 3).eof(3).build()

        parser = QueryParser()
        ast    = parser.parse(tokens)

        pattern = ast
        assert isinstance(pattern, n.PatternNode)
        assert pattern.value             == 'c?t'
        assert pattern.resolved_term_ids == set()

    def test_parse_with_phrase_with_a_single_term(self):
        tokens = (self.builder.many()
                  .quote(0)
                  .term('apple', 1, 6)
                  .quote(6)
                  .eof(7).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        phrase = ast
        assert isinstance(phrase, n.PhraseNode)
        assert len(phrase.children) == 1

        term = phrase.children[0]
        assert isinstance(term, n.TermNode)
        assert term.value             == 'apple'
        assert term.is_exact          == False
        assert term.resolved_term_ids == set()

    def test_parse_with_phrase_with_a_single_pattern(self):
        tokens = (self.builder.many()
                  .quote(0)
                  .pattern('a*e', 1, 4)
                  .quote(4)
                  .eof(5).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        phrase = ast
        assert isinstance(phrase, n.PhraseNode)
        assert len(phrase.children) == 1

        pattern = phrase.children[0]
        assert isinstance(pattern, n.PatternNode)
        assert pattern.value             == 'a*e'
        assert pattern.resolved_term_ids == set()

    def test_parse_with_phrase_with_single_exact_term(self):
        tokens = (self.builder.many()
                  .quote(0)
                  .exact(1)
                  .term('have', 2, 6)
                  .quote(6)
                  .eof(7).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        phrase = ast
        assert isinstance(phrase, n.PhraseNode)
        assert len(phrase.children) == 1

        term = phrase.children[0]
        assert isinstance(term, n.TermNode)
        assert term.value             == 'have'
        assert term.is_exact          == True
        assert term.resolved_term_ids == set()

    def test_parse_with_phrase_with_multiple_children(self):
        tokens = (self.builder.many()
                  .quote(0)
                  .term('perfect', 1, 8)
                  .pattern('a*e', 9, 12)
                  .exact(13)
                  .term('have', 14, 18)
                  .quote(18)
                  .eof(19).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        phrase = ast
        assert isinstance(phrase, n.PhraseNode)
        assert len(phrase.children) == 3

        term1 = phrase.children[0]
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'perfect'
        assert term1.is_exact          == False
        assert term1.resolved_term_ids == set()

        pattern = phrase.children[1]
        assert isinstance(pattern, n.PatternNode)
        assert pattern.value             == 'a*e'
        assert pattern.resolved_term_ids == set()

        term2 = phrase.children[2]
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'have'
        assert term2.is_exact          == True
        assert term2.resolved_term_ids == set()

    def test_parse_with_nested_with_single_term(self):
        tokens = (self.builder.many()
                  .lparen(0)
                  .term('apple', 1, 6)
                  .rparen(6)
                  .eof(7).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        term = ast
        assert isinstance(term, n.TermNode)
        assert term.value             == 'apple'
        assert term.is_exact          == False
        assert term.resolved_term_ids == set()

    def test_parse_with_nested_with_multiple_terms(self):
        tokens = (self.builder.many()
                  .lparen(0)
                  .term('perfect', 1,   8)
                  .term('apple',   9,  14)
                  .term('pie',     15, 18)
                  .rparen(18)
                  .eof(19).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        andn = ast
        assert isinstance(andn, n.OrNode)
        assert len(andn.children) == 3

        term1 = andn.children[0]
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'perfect'
        assert term1.is_exact          == False
        assert term1.resolved_term_ids == set()

        term2 = andn.children[1]
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'apple'
        assert term2.is_exact          == False
        assert term2.resolved_term_ids == set()

        term3 = andn.children[2]
        assert isinstance(term3, n.TermNode)
        assert term3.value             == 'pie'
        assert term3.is_exact          == False
        assert term3.resolved_term_ids == set()

    def test_parse_raises_error_when_nested_is_unclosed(self):
        tokens = (self.builder.many()
                  .lparen(0)
                  .term('cat', 1, 4)
                  .eof(4).build())

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_raises_error_when_nested_is_closed(self):
        tokens = (self.builder.many()
                  .term('cat', 0, 3)
                  .rparen(3)
                  .eof(4).build())

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_with_starts_with(self):
        tokens = (self.builder.many()
                  .caret(0)
                  .term('you', 1, 4)
                  .eof(4).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        starts = ast
        assert isinstance(starts, n.StartsWithNode)

        term = starts.child
        assert isinstance(term, n.TermNode)
        assert term.value             == 'you'
        assert term.is_exact          == False
        assert term.resolved_term_ids == set()

    def test_parse_with_ends_with(self):
        tokens = (self.builder.many()
                  .term('him', 0, 3)
                  .dollar(3)
                  .eof(4).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        ends = ast
        assert isinstance(ends, n.EndsWithNode)

        term = ends.child
        assert isinstance(term, n.TermNode)
        assert term.value             == 'him'
        assert term.is_exact          == False
        assert term.resolved_term_ids == set()

    def test_parse_raises_error_when_ends_with_is_leading(self):
        tokens = (self.builder.many()
                  .dollar(0)
                  .term('you', 1, 4)
                  .eof(4).build())

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_raises_error_when_starts_with_is_trailing(self):
        tokens = (self.builder.many()
                  .term('him', 0, 3)
                  .caret(3)
                  .eof(4).build())

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_raises_error_when_anchored_with_starts_and_ends_with(self):
        tokens = (self.builder.many()
                  .caret(0)
                  .term('him', 1, 4)
                  .dollar(4)
                  .eof(5).build())

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_with_exact_term(self):
        tokens = (self.builder.many()
                  .exact(0)
                  .term('see', 1, 4)
                  .eof(4).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        term = ast
        assert isinstance(term, n.TermNode)
        assert term.value             == 'see'
        assert term.is_exact          == True
        assert term.resolved_term_ids == set()

    def test_parse_with_exact_pattern(self):
        tokens = (self.builder.many()
                  .exact(0)
                  .pattern('s*e', 1, 4)
                  .eof(4).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        pattern = ast
        assert isinstance(pattern, n.PatternNode)
        assert pattern.value             == 's*e'
        assert pattern.resolved_term_ids == set()

    def test_parse_with_exact_phrase(self):
        tokens = (self.builder.many()
                  .exact(0)
                  .quote(1)
                  .term('be', 2, 4)
                  .term('have', 5, 9)
                  .quote(9)
                  .eof(10).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        phrase = ast
        assert isinstance(phrase, n.PhraseNode)
        assert len(phrase.children) == 2

        term1 = phrase.children[0]
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'be'
        assert term1.is_exact          == True
        assert term1.resolved_term_ids == set()

        term2 = phrase.children[1]
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'have'
        assert term2.is_exact          == True
        assert term2.resolved_term_ids == set()

    def test_parse_with_exact_nested_with_and(self):
        tokens = (self.builder.many()
                  .exact(0)
                  .lparen(1)
                  .term('be', 2, 4)
                  .and_(5)
                  .term('have', 7, 11)
                  .rparen(11)
                  .eof(12).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        andn = ast
        assert isinstance(andn, n.AndNode)
        assert len(andn.children) == 2

        term1 = andn.children[0]
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'be'
        assert term1.is_exact          == True
        assert term1.resolved_term_ids == set()

        term2 = andn.children[1]
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'have'
        assert term2.is_exact          == True
        assert term2.resolved_term_ids == set()

    def test_parse_with_exact_nested_with_or(self):
        tokens = (self.builder.many()
                  .exact(0)
                  .lparen(1)
                  .term('be', 2, 4)
                  .or_(5)
                  .term('have', 7, 11)
                  .rparen(11)
                  .eof(12).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        orn = ast
        assert isinstance(orn, n.OrNode)
        assert len(orn.children) == 2

        term1 = orn.children[0]
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'be'
        assert term1.is_exact          == True
        assert term1.resolved_term_ids == set()

        term2 = orn.children[1]
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'have'
        assert term2.is_exact          == True
        assert term2.resolved_term_ids == set()

    def test_parse_with_exact_nested_with_starts_with(self):
        tokens = (self.builder.many()
                  .exact(0)
                  .lparen(1)
                  .caret(2)
                  .term('be', 3, 5)
                  .rparen(5)
                  .eof(6).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        starts = ast
        assert isinstance(starts, n.StartsWithNode)

        term = starts.child
        assert isinstance(term, n.TermNode)
        assert term.value             == 'be'
        assert term.is_exact          == True
        assert term.resolved_term_ids == set()

    def test_parse_with_exact_nested_with_ends_with(self):
        tokens = (self.builder.many()
                  .exact(0)
                  .lparen(1)
                  .term('be', 2, 4)
                  .dollar(4)
                  .rparen(5)
                  .eof(6).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        ends = ast
        assert isinstance(ends, n.EndsWithNode)

        term = ends.child
        assert isinstance(term, n.TermNode)
        assert term.value             == 'be'
        assert term.is_exact          == True
        assert term.resolved_term_ids == set()

    def test_parse_with_exact_nested_with_precedes(self):
        tokens = (self.builder.many()
                  .exact(0)
                  .lparen(1)
                  .term('be', 2, 4)
                  .precedes(5)
                  .term('you', 8, 11)
                  .rparen(11)
                  .eof(12).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        precedes = ast
        assert isinstance(precedes, n.PrecedesNode)

        term = precedes.left
        assert isinstance(term, n.TermNode)
        assert term.value             == 'be'
        assert term.is_exact          == True
        assert term.resolved_term_ids == set()

        term = precedes.right
        assert isinstance(term, n.TermNode)
        assert term.value             == 'you'
        assert term.is_exact          == True
        assert term.resolved_term_ids == set()

    def test_parse_with_exact_nested_with_near(self):
        tokens = (self.builder.many()
                  .exact(0)
                  .lparen(1)
                  .term('be', 2, 4)
                  .langle(5)
                  .number('2', 6, 7)
                  .colon(7)
                  .number('4', 8, 9)
                  .rangle(9)
                  .term('you', 10, 13)
                  .rparen(13)
                  .eof(14).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        near = ast
        assert isinstance(near, n.NearNode)
        assert near.min_dist == 2
        assert near.max_dist == 4

        term = near.left
        assert isinstance(term, n.TermNode)
        assert term.value             == 'be'
        assert term.is_exact          == True
        assert term.resolved_term_ids == set()

        term = near.right
        assert isinstance(term, n.TermNode)
        assert term.value             == 'you'
        assert term.is_exact          == True
        assert term.resolved_term_ids == set()

    def test_parse_with_exact_nested_with_not(self):
        tokens = (self.builder.many()
                  .exact(0)
                  .lparen(1)
                  .not_(2)
                  .term('be', 3, 5)
                  .rparen(5)
                  .eof(6).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        notn = ast
        assert isinstance(notn, n.NotNode)

        term = notn.child
        assert isinstance(term, n.TermNode)
        assert term.value             == 'be'
        assert term.is_exact          == True
        assert term.resolved_term_ids == set()

    def test_parse_with_not(self):
        tokens = (self.builder.many()
                  .not_(0)
                  .term('have', 1, 5)
                  .eof(5).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        notn = ast
        assert isinstance(notn, n.NotNode)

        term = notn.child
        assert isinstance(term, n.TermNode)
        assert term.value             == 'have'
        assert term.is_exact          == False
        assert term.resolved_term_ids == set()

    def test_parse_with_not_with_exact_term(self):
        tokens = (self.builder.many()
                  .not_(0)
                  .exact(1)
                  .term('be', 2, 4)
                  .eof(4).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        notn = ast
        assert isinstance(notn, n.NotNode)

        term = notn.child
        assert isinstance(term, n.TermNode)
        assert term.value             == 'be'
        assert term.is_exact          == True
        assert term.resolved_term_ids == set()

    def test_parse_raises_error_when_not_precedes_another_not(self):
        tokens = (self.builder.many()
                  .not_(0)
                  .not_(1)
                  .term('be', 2, 4)
                  .eof(4).build())

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_raises_error_when_exact_precedes_not(self):
        tokens = (self.builder.many()
                  .exact(0)
                  .not_(1)
                  .term('be', 2, 4)
                  .eof(4).build())

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_raises_error_when_exact_precedes_another_exact(self):
        tokens = (self.builder.many()
                  .exact(0)
                  .exact(1)
                  .term('be', 2, 4)
                  .eof(4).build())

        parser = QueryParser()

        with raises(QueryParserError):
            parser.parse(tokens)

    def test_parse_with_precedes(self):
        tokens = (self.builder.many()
                  .term('cat', 0, 3)
                  .precedes(4)
                  .term('dog', 7, 10)
                  .eof(10).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        precedes = ast
        assert isinstance(precedes, n.PrecedesNode)

        term1 = precedes.left
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'cat'
        assert term1.is_exact          == False
        assert term1.resolved_term_ids == set()

        term2 = precedes.right
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'dog'
        assert term2.is_exact          == False
        assert term2.resolved_term_ids == set()

    def test_parse_with_near_with_both_boundaries(self):
        tokens = (self.builder.many()
                  .term('cat', 0, 3)
                  .langle(4)
                  .number('3', 5, 6)
                  .colon(6)
                  .number('6', 7, 8)
                  .rangle(8)
                  .term('dog', 10, 13)
                  .eof(13).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        near = ast
        assert isinstance(near, n.NearNode)
        assert near.min_dist == 3
        assert near.max_dist == 6

        term1 = near.left
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'cat'
        assert term1.is_exact          == False
        assert term1.resolved_term_ids == set()

        term2 = near.right
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'dog'
        assert term2.is_exact          == False
        assert term2.resolved_term_ids == set()

    def test_parse_with_near_with_lower_boundary(self):
        tokens = (self.builder.many()
                  .term('cat', 0, 3)
                  .langle(4)
                  .number('2', 5, 6)
                  .colon(6)
                  .rangle(7)
                  .term('dog', 9, 12)
                  .eof(12).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        near = ast
        assert isinstance(near, n.NearNode)
        assert near.min_dist == 2
        assert near.max_dist is None

        term1 = near.left
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'cat'
        assert term1.is_exact          == False
        assert term1.resolved_term_ids == set()

        term2 = near.right
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'dog'
        assert term2.is_exact          == False
        assert term2.resolved_term_ids == set()

    def test_parse_with_near_with_upper_boundary(self):
        tokens = (self.builder.many()
                  .term('cat', 0, 3)
                  .langle(4)
                  .colon(5)
                  .number('5', 6, 7)
                  .rangle(7)
                  .term('dog', 9, 12)
                  .eof(12).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        near = ast
        assert isinstance(near, n.NearNode)
        assert near.min_dist is None
        assert near.max_dist == 5

        term1 = near.left
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'cat'
        assert term1.is_exact          == False
        assert term1.resolved_term_ids == set()

        term2 = near.right
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'dog'
        assert term2.is_exact          == False
        assert term2.resolved_term_ids == set()

    def test_parse_with_near_with_single_number(self):
        tokens = (self.builder.many()
                  .term('cat', 0, 3)
                  .langle(4)
                  .number('7', 5, 6)
                  .rangle(7)
                  .term('dog', 9, 11)
                  .eof(11).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        near = ast
        assert isinstance(near, n.NearNode)
        assert near.min_dist is None
        assert near.max_dist == 7

        term1 = near.left
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'cat'
        assert term1.is_exact          == False
        assert term1.resolved_term_ids == set()

        term2 = near.right
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'dog'
        assert term2.is_exact          == False
        assert term2.resolved_term_ids == set()

    def test_parse_with_exp_and(self):
        tokens = (self.builder.many()
                  .term('cat', 0, 3)
                  .and_(4)
                  .term('dog', 6, 9)
                  .eof(9).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        andn = ast
        assert isinstance(andn, n.AndNode)
        assert len(andn.children) == 2

        term1 = andn.children[0]
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'cat'
        assert term1.is_exact          == False
        assert term1.resolved_term_ids == set()

        term2 = andn.children[1]
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'dog'
        assert term2.is_exact          == False
        assert term2.resolved_term_ids == set()

    def test_parse_with_imp_and(self):
        tokens = (self.builder.many()
                  .term('cat', 0, 3)
                  .term('dog', 4, 7)
                  .eof(7).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        andn = ast
        assert isinstance(andn, n.OrNode)
        assert len(andn.children) == 2

        term1 = andn.children[0]
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'cat'
        assert term1.is_exact          == False
        assert term1.resolved_term_ids == set()

        term2 = andn.children[1]
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'dog'
        assert term2.is_exact          == False
        assert term2.resolved_term_ids == set()

    def test_parse_with_or(self):
        tokens = (self.builder.many()
                  .term('cat', 0, 3)
                  .or_(4)
                  .term('dog', 6, 9)
                  .eof(9).build())

        parser = QueryParser()
        ast    = parser.parse(tokens)

        orn = ast
        assert isinstance(orn, n.OrNode)
        assert len(orn.children) == 2

        term1 = orn.children[0]
        assert isinstance(term1, n.TermNode)
        assert term1.value             == 'cat'
        assert term1.is_exact          == False
        assert term1.resolved_term_ids == set()

        term2 = orn.children[1]
        assert isinstance(term2, n.TermNode)
        assert term2.value             == 'dog'
        assert term2.is_exact          == False
        assert term2.resolved_term_ids == set()
