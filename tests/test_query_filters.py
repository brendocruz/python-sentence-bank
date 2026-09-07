from sentencebank.query.filters import CaseFoldingFilter, ProtectedTermsFilter
from sentencebank.query.tokens import QueryToken, QueryTokenKind


class TestQueryCaseFoldingFilter:

    def test_process_empty_token_list(self):
        tokens = []
        filter = CaseFoldingFilter()
        result = filter.process(tokens)
        assert len(result) == 0

    def test_process_eof(self):
        token1 = QueryToken(kind=QueryTokenKind.EOF,  value='', start=0, end=0)
        tokens = [token1]

        filter = CaseFoldingFilter()
        result = filter.process(tokens)
        assert len(result) == 1

        assert result[0].value == ''
        assert result[0].kind  == QueryTokenKind.EOF
        assert result[0].start == 0
        assert result[0].end   == 0

    def test_process_term(self):
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='PaRaDiGm', start=0, end=8)
        token2 = QueryToken(kind=QueryTokenKind.EOF,  value='',         start=8, end=8)
        tokens = [token1, token2]

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

    def test_process_wterm(self):
        token1 = QueryToken(kind=QueryTokenKind.WTERM, value='T??En', start=0, end=5)
        token2 = QueryToken(kind=QueryTokenKind.EOF,   value='',      start=5, end=5)
        tokens = [token1, token2]

        filter = CaseFoldingFilter()
        result = filter.process(tokens)
        assert len(result) == 2

        assert result[0].value == 't??en'
        assert result[0].kind  == QueryTokenKind.WTERM
        assert result[0].start == 0
        assert result[0].end   == 5

        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 5
        assert result[1].end   == 5

    def test_process_number(self):
        token1 = QueryToken(kind=QueryTokenKind.NUMBER, value='100', start=0, end=3)
        token2 = QueryToken(kind=QueryTokenKind.EOF,    value='',    start=3, end=3)
        tokens = [token1, token2]

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

    def test_process_symbol(self):
        token1 = QueryToken(kind=QueryTokenKind.PRECEDES, value='<<', start=0, end=2)
        token2 = QueryToken(kind=QueryTokenKind.EOF,      value='',   start=2, end=2)
        tokens = [token1, token2]

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

    def test_process_empty_token_list(self):
        query  = ''
        tokens = []

        terms  = ['Dr.', 'etc.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 0

    def test_process_empty_query(self):
        query  = ''
        token1 = QueryToken(kind=QueryTokenKind.EOF, value='', start=1, end=1)
        tokens = [token1]

        terms  = ['Dr.', 'etc.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 1

        assert result[0].value == ''
        assert result[0].kind  == QueryTokenKind.EOF
        assert result[0].start == 1
        assert result[0].end   == 1

    def test_process_wterm(self):
        query  = 'd?g'
        token1 = QueryToken(kind=QueryTokenKind.WTERM, value='d?g', start=0, end=3)
        token2 = QueryToken(kind=QueryTokenKind.EOF,   value='',    start=3, end=3)
        tokens = [token1, token2]

        terms  = ['etc.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 2

        assert result[0].value == 'd?g'
        assert result[0].kind  == QueryTokenKind.WTERM
        assert result[0].start == 0
        assert result[0].end   == 3

        assert result[1].value == ''
        assert result[1].kind  == QueryTokenKind.EOF
        assert result[1].start == 3
        assert result[1].end   == 3

    def test_process_term_not_in_the_list(self):
        query  = 'e.g.'
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='e.g', start=0, end=3)
        token2 = QueryToken(kind=QueryTokenKind.EOF,  value='',    start=4, end=4)
        tokens = [token1, token2]

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
        assert result[1].start == 4
        assert result[1].end   == 4

    def test_process_term_embedded_in_longer_word(self):
        query  = 'L\'hôpital'
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='l\'hôpital', start=0, end=9)
        token2 = QueryToken(kind=QueryTokenKind.EOF,  value='',           start=9, end=9)
        tokens = [token1, token2]

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

    def test_process_term_with_trailing_non_word_char(self):
        query  = 'Dr.'
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='dr', start=0, end=2)
        token2 = QueryToken(kind=QueryTokenKind.EOF,  value='',   start=3, end=3)
        tokens = [token1, token2]

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

    def test_process_terms_with_trailing_non_word_char(self):
        query  = 'Dr. Dra.'
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='dr',  start=0, end=2)
        token2 = QueryToken(kind=QueryTokenKind.TERM, value='dra', start=4, end=7)
        token3 = QueryToken(kind=QueryTokenKind.EOF,  value='',    start=8, end=8)
        tokens = [token1, token2, token3]

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

    def test_process_term_with_leading_non_word_char(self):
        query  = '\'cause'
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='cause', start=1, end=6)
        token2 = QueryToken(kind=QueryTokenKind.EOF,  value='',      start=6, end=6)
        tokens = [token1, token2]

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

    def test_process_term_with_leading_and_trailing_non_word_char(self):
        query  = 'rock \'n\' roll'
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='rock', start=0, end=4)
        token2 = QueryToken(kind=QueryTokenKind.TERM, value='n',    start=6, end=7)
        token3 = QueryToken(kind=QueryTokenKind.TERM, value='roll', start=9, end=13)
        token4 = QueryToken(kind=QueryTokenKind.EOF,  value='',     start=13, end=13)
        tokens = [token1, token2, token3, token4]

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

    def test_process_term_with_multiple_inner_non_word_char(self):
        query  = 'rock-\'n\'-roll'
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='rock-\'n\'-roll',
                            start=0, end=13)
        token2 = QueryToken(kind=QueryTokenKind.EOF,  value='', start=13, end=13)
        tokens = [token1, token2]

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

    def test_process_term_overlapping_matches_longer(self):
        query  = 'U.S.A.'
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='u.s.a', start=0, end=5)
        token2 = QueryToken(kind=QueryTokenKind.EOF,  value='',      start=6, end=6)
        tokens = [token1, token2]

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

    def test_process_term_overlapping_matches_shorter(self):
        query  = 'U.S.'
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='u.s', start=0, end=3)
        token2 = QueryToken(kind=QueryTokenKind.EOF,  value='',    start=4, end=4)
        tokens = [token1, token2]

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

    def test_process_term_with_inner_whitespace_char(self):
        query  = 'et al.'
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='et', start=0, end=2)
        token2 = QueryToken(kind=QueryTokenKind.TERM, value='al', start=3, end=5)
        token3 = QueryToken(kind=QueryTokenKind.EOF,  value='',   start=6, end=6)
        tokens = [token1, token2, token3]

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

    def test_process_term_with_repeated_pattern(self):
        query  = 'bye bye'
        token1 = QueryToken(kind=QueryTokenKind.TERM, value='bye', start=0, end=3)
        token2 = QueryToken(kind=QueryTokenKind.TERM, value='bye', start=4, end=7)
        token3 = QueryToken(kind=QueryTokenKind.EOF,  value='',    start=7, end=7)
        tokens = [token1, token2, token3]

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
