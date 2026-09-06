from sentencebank.query.lexer import QueryLexer
from sentencebank.query.tokens import QueryTokenKind


class TestQueryLexer:
    lexer: QueryLexer

    def setup_method(self):
        separators = '-,.\''
        self.lexer = QueryLexer(separators)

    def test_tokenize_empty(self):
        tokens = self.lexer.tokenize('')
        assert len(tokens) == 1

        assert tokens[0].kind  == QueryTokenKind.EOF
        assert tokens[0].value == ''
        assert tokens[0].start == 0
        assert tokens[0].end   == 0

    def test_tokenize_dollar(self):
        tokens = self.lexer.tokenize('$')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.DOLLAR
        assert tokens[0].value == '$'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_caret(self):
        tokens = self.lexer.tokenize('^')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.CARET
        assert tokens[0].value == '^'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_not(self):
        tokens = self.lexer.tokenize('~')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.NOT
        assert tokens[0].value == '~'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_exact(self):
        tokens = self.lexer.tokenize('=')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.EXACT
        assert tokens[0].value == '='
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_and(self):
        tokens = self.lexer.tokenize('&')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.AND
        assert tokens[0].value == '&'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_or(self):
        tokens = self.lexer.tokenize('|')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.OR
        assert tokens[0].value == '|'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_lparen(self):
        tokens = self.lexer.tokenize('(')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.LPAREN
        assert tokens[0].value == '('
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_rparen(self):
        tokens = self.lexer.tokenize(')')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.RPAREN
        assert tokens[0].value == ')'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_quote(self):
        tokens = self.lexer.tokenize('"')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.QUOTE
        assert tokens[0].value == '"'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_colon(self):
        tokens = self.lexer.tokenize(':')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.COLON
        assert tokens[0].value == ':'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_angle_open(self):
        tokens = self.lexer.tokenize('<')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.ANGLE_OPEN
        assert tokens[0].value == '<'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_precedes(self):
        tokens = self.lexer.tokenize('<<')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.PRECEDES
        assert tokens[0].value == '<<'
        assert tokens[0].start == 0
        assert tokens[0].end   == 2

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 2
        assert tokens[1].end   == 2

    def test_tokenize_angle_close(self):
        tokens = self.lexer.tokenize('>')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.ANGLE_CLOSE
        assert tokens[0].value == '>'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_number(self):
        tokens = self.lexer.tokenize('67')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.NUMBER
        assert tokens[0].value == '67'
        assert tokens[0].start == 0
        assert tokens[0].end   == 2

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 2
        assert tokens[1].end   == 2

    def test_tokenize_term_with_digit_in_the_end(self):
        tokens = self.lexer.tokenize('Web3')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == 'Web3'
        assert tokens[0].start == 0
        assert tokens[0].end   == 4

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 4
        assert tokens[1].end   == 4

    def test_tokenize_term_with_digit_in_the_beginning(self):
        tokens = self.lexer.tokenize('5G')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == '5G'
        assert tokens[0].start == 0
        assert tokens[0].end   == 2

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 2
        assert tokens[1].end   == 2

    def test_tokenize_term_with_digit_in_the_middle(self):
        tokens = self.lexer.tokenize('Y2K')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == 'Y2K'
        assert tokens[0].start == 0
        assert tokens[0].end   == 3

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 3
        assert tokens[1].end   == 3

    def test_tokenize_term_no_wildcard(self):
        tokens = self.lexer.tokenize('cat')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == 'cat'
        assert tokens[0].start == 0
        assert tokens[0].end   == 3

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 3
        assert tokens[1].end   == 3

    def test_tokenize_wterm_with_asterisk(self):
        tokens = self.lexer.tokenize('c*t')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.WTERM
        assert tokens[0].value == 'c*t'
        assert tokens[0].start == 0
        assert tokens[0].end   == 3

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 3
        assert tokens[1].end   == 3

    def test_tokenize_wterm_question_mark(self):
        tokens = self.lexer.tokenize('c?t')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.WTERM
        assert tokens[0].value == 'c?t'
        assert tokens[0].start == 0
        assert tokens[0].end   == 3

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 3
        assert tokens[1].end   == 3

    def test_tokenize_term_with_wildcard_and_digit(self):
        tokens = self.lexer.tokenize('?2K')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.WTERM
        assert tokens[0].value == '?2K'
        assert tokens[0].start == 0
        assert tokens[0].end   == 3

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 3
        assert tokens[1].end   == 3

    def test_tokenize_term_multiple_words(self):
        tokens = self.lexer.tokenize('cat dog fish')
        assert len(tokens) == 4

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == 'cat'
        assert tokens[0].start == 0
        assert tokens[0].end   == 3

        assert tokens[1].kind  == QueryTokenKind.TERM
        assert tokens[1].value == 'dog'
        assert tokens[1].start == 4
        assert tokens[1].end   == 7

        assert tokens[2].kind  == QueryTokenKind.TERM
        assert tokens[2].value == 'fish'
        assert tokens[2].start == 8
        assert tokens[2].end   == 12

        assert tokens[3].kind  == QueryTokenKind.EOF
        assert tokens[3].value == ''
        assert tokens[3].start == 12
        assert tokens[3].end   == 12

    def test_tokenize_handle_whitespace(self):
        tokens = self.lexer.tokenize('|   \t\t\t &   \n\n\n =')
        assert len(tokens) == 4

        assert tokens[0].kind  == QueryTokenKind.OR
        assert tokens[0].value == '|'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.AND
        assert tokens[1].value == '&'
        assert tokens[1].start == 8
        assert tokens[1].end   == 9

        assert tokens[2].kind  == QueryTokenKind.EXACT
        assert tokens[2].value == '='
        assert tokens[2].start == 16
        assert tokens[2].end   == 17

        assert tokens[3].kind  == QueryTokenKind.EOF
        assert tokens[3].value == ''
        assert tokens[3].start == 17
        assert tokens[3].end   == 17

    def test_tokenize_term_number_with_separators(self):
        tokens = self.lexer.tokenize('100.000.000')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == '100.000.000'
        assert tokens[0].start == 0
        assert tokens[0].end   == 11

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 11
        assert tokens[1].end   == 11

    def test_tokenize_term_number_start_with_separator(self):
        tokens = self.lexer.tokenize('.5')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.NUMBER
        assert tokens[0].value == '5'
        assert tokens[0].start == 1
        assert tokens[0].end   == 2

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 2
        assert tokens[1].end   == 2
    
    def test_tokenize_term_with_separator(self):
        tokens = self.lexer.tokenize('self-esteem')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == 'self-esteem'
        assert tokens[0].start == 0
        assert tokens[0].end   == 11

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 11
        assert tokens[1].end   == 11

    def test_tokenize_term_with_single_trailing_separator(self):
        tokens = self.lexer.tokenize('Dr.')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == 'Dr'
        assert tokens[0].start == 0
        assert tokens[0].end   == 2

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 3
        assert tokens[1].end   == 3

    def test_tokenize_term_with_multiple_trailing_separators(self):
        tokens = self.lexer.tokenize('Hello...')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == 'Hello'
        assert tokens[0].start == 0
        assert tokens[0].end   == 5

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 8
        assert tokens[1].end   == 8

    def test_tokenize_term_with_single_leading_separator(self):
        tokens = self.lexer.tokenize('\'n')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == 'n'
        assert tokens[0].start == 1
        assert tokens[0].end   == 2

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 2
        assert tokens[1].end   == 2

    def test_tokenize_term_with_multiple_leading_separator(self):
        tokens = self.lexer.tokenize('...World')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == 'World'
        assert tokens[0].start == 3
        assert tokens[0].end   == 8

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 8
        assert tokens[1].end   == 8

    def test_tokenize_term_with_multiple_separators(self):
        tokens = self.lexer.tokenize('rock-\'n\'-roll')
        assert len(tokens) == 2

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == 'rock-\'n\'-roll'
        assert tokens[0].start == 0
        assert tokens[0].end   == 13

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 13
        assert tokens[1].end   == 13
