from sentencebank.indexing.lexer import IndexingLexer


class TestIndexingLexer:
    lexer: IndexingLexer

    def setup_method(self):
        separators = '-,.\''
        self.lexer = IndexingLexer(separators)

    def test_tokenize_empty(self):
        tokens = self.lexer.tokenize('')
        assert len(tokens) == 0

    def test_tokenize_sigle_token(self):
        tokens = self.lexer.tokenize('World')
        assert len(tokens) == 1

        assert tokens[0].value    == 'World'
        assert tokens[0].position == 0
        assert tokens[0].start    == 0
        assert tokens[0].end      == 5

    def test_tokenize_multiple_words(self):
        tokens = self.lexer.tokenize('cat dog fish')
        assert len(tokens) == 3

        assert tokens[0].value    == 'cat'
        assert tokens[0].position == 0
        assert tokens[0].start    == 0
        assert tokens[0].end      == 3

        assert tokens[1].value    == 'dog'
        assert tokens[1].position == 1
        assert tokens[1].start    == 4
        assert tokens[1].end      == 7

        assert tokens[2].value    == 'fish'
        assert tokens[2].position == 2
        assert tokens[2].start    == 8
        assert tokens[2].end      == 12

    def test_tokenize_handle_no_word_chars(self):
        tokens = self.lexer.tokenize('\n\n  Hello  ,,, \t\t  World!!!!   ')
        assert len(tokens) == 2

        assert tokens[0].value    == "Hello"
        assert tokens[0].position == 0
        assert tokens[0].start    == 4
        assert tokens[0].end      == 9

        assert tokens[1].value    == "World"
        assert tokens[1].position == 1
        assert tokens[1].start    == 19
        assert tokens[1].end      == 24

    def test_tokenize_number(self):
        tokens = self.lexer.tokenize('67')
        assert len(tokens) == 1

        assert tokens[0].value    == '67'
        assert tokens[0].position == 0
        assert tokens[0].start    == 0
        assert tokens[0].end      == 2

    def test_tokenize_term_with_digit_in_the_end(self):
        tokens = self.lexer.tokenize('Web3')
        assert len(tokens) == 1

        assert tokens[0].value    == 'Web3'
        assert tokens[0].position == 0
        assert tokens[0].start    == 0
        assert tokens[0].end      == 4

    def test_tokenize_term_with_digit_in_the_beginning(self):
        tokens = self.lexer.tokenize('5G')
        assert len(tokens) == 1

        assert tokens[0].value    == '5G'
        assert tokens[0].position == 0
        assert tokens[0].start    == 0
        assert tokens[0].end      == 2

    def test_tokenize_term_with_digit_in_the_middle(self):
        tokens = self.lexer.tokenize('Y2K')
        assert len(tokens) == 1

        assert tokens[0].value    == 'Y2K'
        assert tokens[0].position == 0
        assert tokens[0].start    == 0
        assert tokens[0].end      == 3
    
    def test_tokenize_term_with_separator(self):
        tokens = self.lexer.tokenize('self-esteem')
        assert len(tokens) == 1

        assert tokens[0].value    == 'self-esteem'
        assert tokens[0].position == 0
        assert tokens[0].start    == 0
        assert tokens[0].end      == 11

    def test_tokenize_term_number_with_separators(self):
        tokens = self.lexer.tokenize('100.000.000')
        assert len(tokens) == 1

        assert tokens[0].value    == '100.000.000'
        assert tokens[0].position == 0
        assert tokens[0].start    == 0
        assert tokens[0].end      == 11

    def test_tokenize_term_with_single_trailing_separator(self):
        tokens = self.lexer.tokenize('Dr.')
        assert len(tokens) == 1

        assert tokens[0].value    == 'Dr'
        assert tokens[0].position == 0
        assert tokens[0].start    == 0
        assert tokens[0].end      == 2

    def test_tokenize_term_with_multiple_trailing_separators(self):
        tokens = self.lexer.tokenize('Hello...')
        assert len(tokens) == 1

        assert tokens[0].value    == 'Hello'
        assert tokens[0].position == 0
        assert tokens[0].start    == 0
        assert tokens[0].end      == 5

    def test_tokenize_term_with_single_leading_separator(self):
        tokens = self.lexer.tokenize('\'n')
        assert len(tokens) == 1

        assert tokens[0].value    == 'n'
        assert tokens[0].position == 0
        assert tokens[0].start    == 1
        assert tokens[0].end      == 2

    def test_tokenize_term_with_multiple_leading_separator(self):
        tokens = self.lexer.tokenize('...World')
        assert len(tokens) == 1

        assert tokens[0].value    == 'World'
        assert tokens[0].position == 0
        assert tokens[0].start    == 3
        assert tokens[0].end      == 8

    def test_tokenize_term_number_with_leading_separator(self):
        tokens = self.lexer.tokenize('.5')
        assert len(tokens) == 1

        assert tokens[0].value    == '5'
        assert tokens[0].position == 0
        assert tokens[0].start    == 1
        assert tokens[0].end      == 2

    def test_tokenize_term_with_multiple_separators(self):
        tokens = self.lexer.tokenize('rock-\'n\'-roll')
        assert len(tokens) == 1

        assert tokens[0].value    == 'rock-\'n\'-roll'
        assert tokens[0].position == 0
        assert tokens[0].start    == 0
        assert tokens[0].end      == 13
