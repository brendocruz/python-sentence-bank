from sentencebank.query.lexer import QueryLexer
from sentencebank.query.tokens import QueryTokenKind
from pytest import fixture
import string


@fixture
def lexer():
    return QueryLexer(string.ascii_letters)


class TestQueryLexer:

    def test_tokenize_empty(self, lexer: QueryLexer):
        tokens = lexer.tokenize('')

        assert len(tokens)     == 1

        assert tokens[0].kind  == QueryTokenKind.EOF
        assert tokens[0].value == ''
        assert tokens[0].start == 0
        assert tokens[0].end   == 0

    def test_tokenize_dollar(self, lexer: QueryLexer):
        tokens = lexer.tokenize('$')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.DOLLAR
        assert tokens[0].value == '$'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_caret(self, lexer: QueryLexer):
        tokens = lexer.tokenize('^')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.CARET
        assert tokens[0].value == '^'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_not(self, lexer: QueryLexer):
        tokens = lexer.tokenize('~')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.NOT
        assert tokens[0].value == '~'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_exact(self, lexer: QueryLexer):
        tokens = lexer.tokenize('=')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.EXACT
        assert tokens[0].value == '='
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_and(self, lexer: QueryLexer):
        tokens = lexer.tokenize('&')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.AND
        assert tokens[0].value == '&'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_or(self, lexer: QueryLexer):
        tokens = lexer.tokenize('|')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.OR
        assert tokens[0].value == '|'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_lparen(self, lexer: QueryLexer):
        tokens = lexer.tokenize('(')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.LPAREN
        assert tokens[0].value == '('
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_rparen(self, lexer: QueryLexer):
        tokens = lexer.tokenize(')')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.RPAREN
        assert tokens[0].value == ')'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_quote(self, lexer: QueryLexer):
        tokens = lexer.tokenize('"')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.QUOTE
        assert tokens[0].value == '"'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_comma(self, lexer: QueryLexer):
        tokens = lexer.tokenize(',')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.COMMA
        assert tokens[0].value == ','
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_angle_open(self, lexer: QueryLexer):
        tokens = lexer.tokenize('<')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.ANGLE_OPEN
        assert tokens[0].value == '<'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_precedes(self, lexer: QueryLexer):
        tokens = lexer.tokenize('<<')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.PRECEDES
        assert tokens[0].value == '<<'
        assert tokens[0].start == 0
        assert tokens[0].end   == 2

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 2
        assert tokens[1].end   == 2

    def test_tokenize_angle_close(self, lexer: QueryLexer):
        tokens = lexer.tokenize('>')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.ANGLE_CLOSE
        assert tokens[0].value == '>'
        assert tokens[0].start == 0
        assert tokens[0].end   == 1

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 1
        assert tokens[1].end   == 1

    def test_tokenize_term_no_wildcard(self, lexer: QueryLexer):
        tokens = lexer.tokenize('cat')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.TERM
        assert tokens[0].value == 'cat'
        assert tokens[0].start == 0
        assert tokens[0].end   == 3

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 3
        assert tokens[1].end   == 3

    def test_tokenize_wterm_with_asterisk(self, lexer: QueryLexer):
        tokens = lexer.tokenize('c*t')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.WTERM
        assert tokens[0].value == 'c*t'
        assert tokens[0].start == 0
        assert tokens[0].end   == 3

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 3
        assert tokens[1].end   == 3

    def test_tokenize_wterm_question_mark(self, lexer: QueryLexer):
        tokens = lexer.tokenize('c?t')

        assert len(tokens)     == 2

        assert tokens[0].kind  == QueryTokenKind.WTERM
        assert tokens[0].value == 'c?t'
        assert tokens[0].start == 0
        assert tokens[0].end   == 3

        assert tokens[1].kind  == QueryTokenKind.EOF
        assert tokens[1].value == ''
        assert tokens[1].start == 3
        assert tokens[1].end   == 3

    def test_tokenize_term_multiple_words(self, lexer: QueryLexer):
        tokens = lexer.tokenize('cat dog fish')

        assert len(tokens)     == 4

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

    def test_tokenize_handle_whitespace(self, lexer: QueryLexer):
        tokens = lexer.tokenize('|   \t\t\t &   \n\n\n =')

        assert len(tokens)     == 4

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
