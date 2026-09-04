from sentencebank.indexing.lexer import IndexingLexer
from pytest import fixture
import string


@fixture
def lexer():
    return IndexingLexer(string.ascii_letters)


class TestIndexingLexer:

    def test_tokenize_sigle_token(self, lexer: IndexingLexer):
        tokens = lexer.tokenize('World')
        assert len(tokens)     == 1

        token0 = tokens[0]
        assert token0.text     == 'World'
        assert token0.position == 0
        assert token0.start    == 0
        assert token0.end      == 5

    def test_tokenize_handle_no_alphabet_chars(self, lexer: IndexingLexer):
        tokens = lexer.tokenize("\n\n  Hello,,, \t\t  World!!!!   ")
        assert len(tokens)     == 2

        token0 = tokens[0]
        assert token0.text     == "Hello"
        assert token0.position == 0
        assert token0.start    == 4
        assert token0.end      == 9

        token1 = tokens[1]
        assert token1.text     == "World"
        assert token1.position == 1
        assert token1.start    == 17
        assert token1.end      == 22
