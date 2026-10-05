from pytest import fixture

from sentencebank.query.filters import CaseFoldingFilter, ProtectedTermsFilter
from sentencebank.query.tokens import QueryTokenKind
from tests.support.builders.query_token import QueryTokenTestBuilder


class TestQueryCaseFoldingFilter:
    _builder: QueryTokenTestBuilder

    @fixture(autouse=True)
    def setup(self):
        self._builder = QueryTokenTestBuilder()

    def test_process_when_token_list_is_empty(self):
        tokens = []
        filter = CaseFoldingFilter()
        result = filter.process(tokens)
        assert len(result) == 0

    def test_process_when_token_is_eof(self):
        tokens = self._builder.many().eof(0).build()

        filter = CaseFoldingFilter()
        result = filter.process(tokens)
        assert len(result) == 1

        assert result[0].value == ''
        assert result[0].kind  == QueryTokenKind.EOF
        assert result[0].start == 0
        assert result[0].end   == 0

    def test_process_when_token_is_a_term(self):
        tokens = self._builder.many().term('PaRaDiGm', 0, 8).eof(8).build()

        filter = CaseFoldingFilter()
        result = filter.process(tokens)
        assert len(result) == 2

        assert result[0].value == 'paradigm'
        assert result[0].kind  == QueryTokenKind.TERM
        assert result[0].start == 0
        assert result[0].end   == 8

        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 8
        assert result[1].end   == 8

    def test_process_when_token_is_a_pattern(self):
        tokens = self._builder.many().pattern('T??En', 0, 5).eof(5).build()

        filter = CaseFoldingFilter()
        result = filter.process(tokens)
        assert len(result) == 2

        assert result[0].value == 't??en'
        assert result[0].kind  == QueryTokenKind.PATTERN
        assert result[0].start == 0
        assert result[0].end   == 5

        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 5
        assert result[1].end   == 5

    def test_process_when_token_is_a_number(self):
        tokens = self._builder.many().number('100', 0, 3).eof(3).build()

        filter = CaseFoldingFilter()
        result = filter.process(tokens)
        assert len(result) == 2

        assert result[0].value == '100'
        assert result[0].kind  == QueryTokenKind.NUMBER
        assert result[0].start == 0
        assert result[0].end   == 3

        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 3
        assert result[1].end   == 3

    def test_process_when_token_is_a_symbol(self):
        tokens = self._builder.many().precedes(0).eof(2).build()

        filter = CaseFoldingFilter()
        result = filter.process(tokens)
        assert len(result) == 2

        assert result[0].value == '<<'
        assert result[0].kind  == QueryTokenKind.PRECEDES
        assert result[0].start == 0
        assert result[0].end   == 2

        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 2
        assert result[1].end   == 2


class TestQueryProtectedTermsFilter:
    builder: QueryTokenTestBuilder

    @fixture(autouse=True)
    def setup(self):
        self.builder = QueryTokenTestBuilder()

    def test_process_when_token_list_is_empty(self):
        query  = ''
        tokens = []

        terms  = ['Dr.', 'etc.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 0

    def test_process_when_query_is_empty(self):
        query  = ''
        tokens = self.builder.many().eof(0).build()

        terms  = ['Dr.', 'etc.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 1

        assert result[0].value == ''
        assert result[0].kind  == QueryTokenKind.EOF
        assert result[0].start == 0
        assert result[0].end   == 0

    def test_process_when_token_is_a_pattern(self):
        query  = 'd?g'
        tokens = self.builder.many().pattern('d?g', 0, 3).eof(3).build()

        terms  = ['etc.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 2

        assert result[0].value == 'd?g'
        assert result[0].kind  == QueryTokenKind.PATTERN
        assert result[0].start == 0
        assert result[0].end   == 3

        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 3
        assert result[1].end   == 3

    def test_process_when_term_is_not_in_the_list(self):
        query  = 'e.g.'
        tokens = self.builder.many().term('e.g', 0, 3).eof(3).build()

        terms  = ['etc.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 2

        assert result[0].value == 'e.g'
        assert result[0].kind  == QueryTokenKind.TERM
        assert result[0].start == 0
        assert result[0].end   == 3

        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 3
        assert result[1].end   == 3

    def test_process_with_term_embedded_in_longer_word(self):
        query  = 'L\'hôpital'
        tokens = self.builder.many().term('l\'hôpital', 0, 9).eof(9).build()

        terms  = ['l\'']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 2
        
        assert result[0].value == 'l\'hôpital'
        assert result[0].kind  == QueryTokenKind.TERM
        assert result[0].start == 0
        assert result[0].end   == 9
        
        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 9
        assert result[1].end   == 9

    def test_process_with_term_with_trailing_non_word_char(self):
        query  = 'Dr.'
        tokens = self.builder.many().term('dr', 0, 2).eof(3).build()

        terms  = ['Dr.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 2
        
        assert result[0].value == 'dr.'
        assert result[0].kind  == QueryTokenKind.TERM
        assert result[0].start == 0
        assert result[0].end   == 3

        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 3
        assert result[1].end   == 3

    def test_process_with_terms_with_trailing_non_word_char(self):
        query  = 'Dr. Dra.'
        tokens = (self.builder.many()
                  .term('dr', 0, 2)
                  .term('dra', 4, 7)
                  .eof(8).build())

        terms  = ['Dr.', 'Dra.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 3
        
        assert result[0].value == 'dr.'
        assert result[0].kind  == QueryTokenKind.TERM
        assert result[0].start == 0
        assert result[0].end   == 3
        
        assert result[1].value == 'dra.'
        assert result[1].kind  == QueryTokenKind.TERM
        assert result[1].start == 4
        assert result[1].end   == 8

        assert result[2].value == ''
        assert result[2].kind  == QueryTokenKind.EOF
        assert result[2].start == 8
        assert result[2].end   == 8

    def test_process_with_term_with_leading_non_word_char(self):
        query  = '\'cause'
        tokens = self.builder.many().term('cause', 1, 6).eof(6).build()

        terms  = ['\'cause']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 2
        
        assert result[0].value == '\'cause'
        assert result[0].kind  == QueryTokenKind.TERM
        assert result[0].start == 0
        assert result[0].end   == 6
        
        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 6
        assert result[1].end   == 6

    def test_process_with_term_with_leading_and_trailing_non_word_char(self):
        query  = 'rock \'n\' roll'
        tokens = (self.builder.many()
                  .term('rock', 0, 4)
                  .term('n', 6, 7)
                  .term('roll', 9, 13)
                  .eof(13).build())

        terms  = ['\'n\'']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 4
        
        assert result[0].value == 'rock'
        assert result[0].kind  == QueryTokenKind.TERM
        assert result[0].start == 0
        assert result[0].end   == 4
        
        assert result[1].value == '\'n\''
        assert result[1].kind  == QueryTokenKind.TERM
        assert result[1].start == 5
        assert result[1].end   == 8
        
        assert result[2].value == 'roll'
        assert result[2].kind  == QueryTokenKind.TERM
        assert result[2].start == 9
        assert result[2].end   == 13
        
        assert result[3].value == ''
        assert result[3].kind  == QueryTokenKind.EOF
        assert result[3].start == 13
        assert result[3].end   == 13

    def test_process_with_term_with_multiple_inner_non_word_char(self):
        query  = 'rock-\'n\'-roll'
        tokens = self.builder.many().term('rock-\'n\'-roll', 0, 13).eof(13).build()

        terms  = ['\'n\'']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 2
        
        assert result[0].value == 'rock-\'n\'-roll'
        assert result[0].kind  == QueryTokenKind.TERM
        assert result[0].start == 0
        assert result[0].end   == 13
        
        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 13
        assert result[1].end   == 13

    def test_process_with_terms_overlapping_targeting_the_longer_term(self):
        query  = 'U.S.A.'
        tokens = self.builder.many().term('u.s.a', 0, 5).eof(6).build()

        terms  = ['U.S.', 'U.S.A.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 2
        
        assert result[0].value == 'u.s.a.'
        assert result[0].kind  == QueryTokenKind.TERM
        assert result[0].start == 0
        assert result[0].end   == 6

        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 6
        assert result[1].end   == 6

    def test_process_with_terms_overlapping_targeting_the_shorter_term(self):
        query  = 'U.S.'
        tokens = self.builder.many().term('u.s', 0, 3).eof(4).build()

        terms  = ['U.S.', 'U.S.A.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 2

        assert result[0].value == 'u.s.'
        assert result[0].kind  == QueryTokenKind.TERM
        assert result[0].start == 0
        assert result[0].end   == 4

        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 4
        assert result[1].end   == 4

    def test_process_with_term_with_inner_whitespace_char(self):
        query  = 'et al.'
        tokens = (self.builder.many()
                  .term('et', 0, 2)
                  .term('al', 3, 5)
                  .eof(6).build())

        terms  = ['et al.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 2
        
        assert result[0].value == 'et al.'
        assert result[0].kind  == QueryTokenKind.TERM
        assert result[0].start == 0
        assert result[0].end   == 6
        
        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 6
        assert result[1].end   == 6

    def test_process_with_term_with_repeated_pattern(self):
        query  = 'bye bye'
        tokens = (self.builder.many()
                  .term('bye', 0, 3)
                  .term('bye', 4, 7)
                  .eof(7).build())

        terms  = ['bye bye']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 2
        
        assert result[0].value == 'bye bye'
        assert result[0].kind  == QueryTokenKind.TERM
        assert result[0].start == 0
        assert result[0].end   == 7
        
        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 7
        assert result[1].end   == 7
