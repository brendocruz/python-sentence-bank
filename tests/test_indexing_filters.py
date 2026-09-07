from sentencebank.indexing.filters import CaseFoldingFilter, ProtectedTermsFilter
from sentencebank.indexing.tokens import IndexingToken


class TestIndexingCaseFoldingFilter:

    def test_process_empty_token_list(self):
        tokens = []
        filter = CaseFoldingFilter()
        result = filter.process(tokens)
        assert len(result) == 0

    def test_process_term_word(self):
        token1 = IndexingToken(value='PaRaDiGm', position=0, start=0, end=8)
        tokens = [token1]

        filter = CaseFoldingFilter()
        result = filter.process(tokens)
        assert len(result) == 1

        assert result[0].value    == 'paradigm'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 8

    def test_process_term_with_digits(self):
        token1 = IndexingToken(value='100', position=0, start=0, end=3)
        tokens = [token1]

        filter = CaseFoldingFilter()
        result = filter.process(tokens)
        assert len(result) == 1

        assert result[0].value    == '100'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 3


class TestIndexingProtectedTermsFilter:

    def test_process_empty_document(self):
        document = ''
        tokens   = []

        terms  = ['Dr.', 'etc.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, document)
        assert len(result) == 0

    def test_process_term_not_in_the_list(self):
        document = 'e.g.'
        token1   = IndexingToken(value='e.g', position=0, start=0, end=3)
        tokens   = [token1]

        terms  = ['etc.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, document)
        assert len(result) == 1

        assert result[0].value    == 'e.g'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 3

    def test_process_term_with_trailing_non_word_char_embedded_in_longer_word(self):
        document = 'L\'hôpital'
        token1   = IndexingToken(value='l\'hôpital', position=0, start=0, end=9)
        tokens   = [token1]

        terms  = ['l\'']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, document)
        assert len(result) == 1
        
        assert result[0].value    == 'l\'hôpital'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 9

    def test_process_term_with_trailing_non_word_char(self):
        document = 'Dr.'
        token1   = IndexingToken(value='dr', position=0, start=0, end=2)
        tokens   = [token1]

        terms  = ['Dr.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, document)
        assert len(result) == 1
        
        assert result[0].value    == 'dr.'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 3

    def test_process_terms_with_trailing_non_word_char(self):
        document = 'Dr. Dra.'
        token1   = IndexingToken(value='dr',  position=0, start=0, end=2)
        token2   = IndexingToken(value='dra', position=1, start=4, end=7)
        tokens   = [token1, token2]

        terms  = ['Dr.', 'Dra.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, document)
        assert len(result) == 2
        
        assert result[0].value    == 'dr.'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 3
        
        assert result[1].value    == 'dra.'
        assert result[1].position == 1
        assert result[1].start    == 4
        assert result[1].end      == 8

    def test_process_term_with_leading_non_word_char(self):
        document = '\'cause'
        token1   = IndexingToken(value='cause', position=0, start=1, end=6)
        tokens   = [token1]

        terms  = ['\'cause']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, document)
        assert len(result) == 1
        
        assert result[0].value    == '\'cause'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 6

    def test_process_term_with_leading_and_trailing_non_word_char(self):
        document = 'rock \'n\' roll'
        token1   = IndexingToken(value='rock', position=0, start=0, end=4)
        token2   = IndexingToken(value='n',    position=1, start=6, end=7)
        token3   = IndexingToken(value='roll', position=2, start=9, end=13)
        tokens   = [token1, token2, token3]

        terms  = ['\'n\'']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, document)
        assert len(result) == 3
        
        assert result[0].value    == 'rock'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 4
        
        assert result[1].value    == '\'n\''
        assert result[1].position == 1
        assert result[1].start    == 5
        assert result[1].end      == 8
        
        assert result[2].value    == 'roll'
        assert result[2].position == 2
        assert result[2].start    == 9
        assert result[2].end      == 13

    def test_process_term_with_multiple_inner_non_word_char(self):
        document = 'rock-\'n\'-roll'
        token1   = IndexingToken(value='rock-\'n\'-roll', position=0, start=0, end=13)
        tokens   = [token1]

        terms  = ['\'n\'']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, document)
        assert len(result) == 1
        
        assert result[0].value    == 'rock-\'n\'-roll'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 13

    def test_process_term_overlapping_matches_longer(self):
        document = 'U.S.A.'
        token1   = IndexingToken(value='u.s.a', position=0, start=0, end=5)
        tokens   = [token1]

        terms  = ['U.S.', 'U.S.A.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, document)
        assert len(result) == 1
        
        assert result[0].value    == 'u.s.a.'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 6

    def test_process_term_overlapping_matches_shorter(self):
        document = 'U.S.'
        token1   = IndexingToken(value='u.s', position=0, start=0, end=3)
        tokens   = [token1]

        terms  = ['U.S.', 'U.S.A.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, document)
        assert len(result) == 1

        assert result[0].value    == 'u.s.'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 4

    def test_process_term_with_inner_whitespace_char(self):
        document = 'et al.'
        token1   = IndexingToken(value='et', position=0, start=0, end=2)
        token2   = IndexingToken(value='al', position=1, start=3, end=5)
        tokens   = [token1, token2]

        terms  = ['et al.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, document)
        assert len(result) == 1
        
        assert result[0].value    == 'et al.'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 6

    def test_process_term_with_repeated_pattern(self):
        query  = 'bye bye'
        token1 = IndexingToken(value='bye', position=0, start=0, end=3)
        token2 = IndexingToken(value='bye', position=1, start=4, end=7)
        tokens = [token1, token2]

        terms  = ['bye bye']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, query)
        assert len(result) == 1
        
        assert result[0].value    == 'bye bye'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 7

    def test_process_term_reajust_token_position(self):
        document = 'bye bye, goodbye, et al. Period.'
        token1   = IndexingToken(value='bye',     position=0, start=0, end=3)
        token2   = IndexingToken(value='bye',     position=1, start=4, end=7)
        token3   = IndexingToken(value='goodbye', position=2, start=9, end=16)
        token4   = IndexingToken(value='et',      position=3, start=18, end=20)
        token5   = IndexingToken(value='al',      position=4, start=21, end=23)
        token6   = IndexingToken(value='period',  position=5, start=25, end=31)
        tokens   = [token1, token2, token3, token4, token5, token6]

        terms  = ['bye bye', 'et al.']
        filter = ProtectedTermsFilter(terms)
        result = filter.process(tokens, document)
        assert len(result) == 4
        
        assert result[0].value    == 'bye bye'
        assert result[0].position == 0
        assert result[0].start    == 0
        assert result[0].end      == 7
        
        assert result[1].value    == 'goodbye'
        assert result[1].position == 1
        assert result[1].start    == 9
        assert result[1].end      == 16
        
        assert result[2].value    == 'et al.'
        assert result[2].position == 2
        assert result[2].start    == 18
        assert result[2].end      == 24
        
        assert result[3].value    == 'period'
        assert result[3].position == 3
        assert result[3].start    == 25
        assert result[3].end      == 31
