from sentencebank.db.database import init_db
from sentencebank.indexing.lexicon import Lexicon
from sqlite3 import IntegrityError, connect
from pytest import fixture, raises


class TestLexicon:
    lexicon: Lexicon

    @fixture(autouse=True)
    def setup(self):
        conn = connect(':memory:')

        init_db(conn)
        self.lexicon = Lexicon(conn)

        yield

        conn.close()

    def test_contains_true(self):
        term_id = self.lexicon.add_term('hello')
        self.lexicon.increment_doc_freq(term_id, 1)
        self.lexicon.increment_col_freq(term_id, 2)

        assert self.lexicon.contains('hello') == True

    def test_contains_false(self):
        term_id = self.lexicon.add_term('hello')
        self.lexicon.increment_doc_freq(term_id, 1)
        self.lexicon.increment_col_freq(term_id, 2)

        assert self.lexicon.contains('world') == False

    def test_get_term_present_id(self):
        term_id = self.lexicon.add_term('language')
        self.lexicon.increment_doc_freq(term_id, 6)
        self.lexicon.increment_col_freq(term_id, 7)

        assert self.lexicon.get_term(term_id) == 'language'

    def test_get_term_absent_id(self):
        term_id = self.lexicon.add_term('language')
        self.lexicon.increment_doc_freq(term_id, 6)
        self.lexicon.increment_col_freq(term_id, 7)

        absent_term_id = term_id + 1
        assert self.lexicon.get_term(absent_term_id) is None

    def test_get_term_invalid_id(self):
        term_id = self.lexicon.add_term('language')
        self.lexicon.increment_doc_freq(term_id, 6)
        self.lexicon.increment_col_freq(term_id, 7)

        assert self.lexicon.get_term(-1) is None

    def test_get_term_id_present_term(self):
        term_id = self.lexicon.add_term('language')
        self.lexicon.increment_doc_freq(term_id, 6)
        self.lexicon.increment_col_freq(term_id, 7)

        assert self.lexicon.get_term_id('language') == term_id

    def test_get_term_id_absent_term(self):
        term_id = self.lexicon.add_term('language')
        self.lexicon.increment_doc_freq(term_id, 6)
        self.lexicon.increment_col_freq(term_id, 7)

        assert self.lexicon.get_term_id('learning') is None

    def test_get_term_id_empty_string(self):
        term_id = self.lexicon.add_term('language')
        self.lexicon.increment_doc_freq(term_id, 6)
        self.lexicon.increment_col_freq(term_id, 7)

        assert self.lexicon.get_term_id('') is None

    def test_get_doc_freq_absent_term(self):
        term_id = self.lexicon.add_term('language')
        self.lexicon.increment_doc_freq(term_id, 6)
        self.lexicon.increment_col_freq(term_id, 7)

        assert self.lexicon.get_doc_freq(term_id) == 6

    def test_get_doc_freq_present_term(self):
        term_id = self.lexicon.add_term('language')
        self.lexicon.increment_doc_freq(term_id, 6)
        self.lexicon.increment_col_freq(term_id, 7)

        assert self.lexicon.get_doc_freq(term_id) == 6

    def test_get_col_freq_absent_term(self):
        term_id = self.lexicon.add_term('language')
        self.lexicon.increment_doc_freq(term_id, 6)
        self.lexicon.increment_col_freq(term_id, 7)

        assert self.lexicon.get_col_freq(term_id) == 7

    def test_get_col_freq_present_term(self):
        term_id = self.lexicon.add_term('language')
        self.lexicon.increment_doc_freq(term_id, 6)
        self.lexicon.increment_col_freq(term_id, 7)

        assert self.lexicon.get_col_freq(term_id) == 7

    def test_get_all_terms_non_empty_lexicon(self):
        self.lexicon.add_term('cat')
        self.lexicon.add_term('dog')
        self.lexicon.add_term('bird')

        terms = self.lexicon.get_all_terms()

        assert len(terms) == 3
        assert 'cat'  in terms
        assert 'dog'  in terms
        assert 'bird' in terms

    def test_get_all_terms_empty_lexicon(self):
        terms = self.lexicon.get_all_terms()

        assert len(terms) == 0

    def test_get_all_protected_terms_non_empty_lexicon(self):
        self.lexicon.add_term('\'bout',    is_protected=True)
        self.lexicon.add_term('friends\'', is_protected=True)
        self.lexicon.add_term('\'cause',   is_protected=True)

        terms = self.lexicon.get_all_protected_terms()

        assert len(terms) == 3
        assert '\'bout'    in terms
        assert 'friends\'' in terms
        assert '\'cause'   in terms

    def test_get_all_protected_terms_empty_lexicon(self):
        terms = self.lexicon.get_all_protected_terms()

        assert len(terms) == 0

    def test_size_empty_lexicon(self):
        assert self.lexicon.size() == 0

    def test_size_non_empty_lexicon(self):
        self.lexicon.add_term('hello')
        self.lexicon.add_term('word')

        assert self.lexicon.size() == 2

    def test_add_term_absent_term(self):
        term_id = self.lexicon.add_term('bird')

        assert self.lexicon.contains('bird')      == True
        assert self.lexicon.get_term(term_id)     == 'bird'
        assert self.lexicon.get_term_id('bird')   == term_id
        assert self.lexicon.get_doc_freq(term_id) == 0
        assert self.lexicon.get_col_freq(term_id) == 0

    def test_add_term_present_term_raises_error(self):
        self.lexicon.add_term('bird')

        with raises(IntegrityError):
            self.lexicon.add_term('bird')

    def test_add_term_absent_protected_term(self):
        term    = '\'bout'
        term_id = self.lexicon.add_term(term, True)

        assert self.lexicon.contains(term)             == True
        assert self.lexicon.get_term(term_id)          == term
        assert self.lexicon.get_term_id(term)          == term_id
        assert self.lexicon.get_doc_freq(term_id)      == 0
        assert self.lexicon.get_col_freq(term_id)      == 0
        assert self.lexicon.is_protected_term(term_id) == True

    def test_increment_doc_freq_present_term(self):
        term_id = self.lexicon.add_term('bird')
        self.lexicon.increment_doc_freq(term_id, 2)
        self.lexicon.increment_col_freq(term_id, 6)

        self.lexicon.increment_doc_freq(term_id, 3)

        assert self.lexicon.get_doc_freq(term_id) == 5

    def test_increment_doc_freq_absent_term(self):
        term_id = self.lexicon.add_term('bird')
        self.lexicon.increment_doc_freq(term_id, 2)
        self.lexicon.increment_col_freq(term_id, 6)

        absent_term_id = term_id + 1
        self.lexicon.increment_doc_freq(absent_term_id, 3)

        assert self.lexicon.get_doc_freq(absent_term_id) == 0

    def test_decrement_doc_freq_present_term_and_greater_than_zero(self):
        term_id = self.lexicon.add_term('bird')
        self.lexicon.increment_doc_freq(term_id, 2)
        self.lexicon.increment_col_freq(term_id, 6)

        self.lexicon.decrement_doc_freq(term_id, 1)

        assert self.lexicon.get_doc_freq(term_id) == 1

    def test_decrement_doc_freq_present_term_and_equal_zero(self):
        term_id = self.lexicon.add_term('bird')
        self.lexicon.increment_doc_freq(term_id, 0)
        self.lexicon.increment_col_freq(term_id, 0)

        self.lexicon.decrement_doc_freq(term_id, 3)

        assert self.lexicon.get_doc_freq(term_id) == 0

    def test_decrement_doc_freq_absent_term(self):
        term_id = self.lexicon.add_term('bird')
        self.lexicon.increment_doc_freq(term_id, 2)
        self.lexicon.increment_col_freq(term_id, 6)

        absent_term_id = term_id + 1
        self.lexicon.decrement_doc_freq(absent_term_id, 3)

        assert self.lexicon.get_doc_freq(absent_term_id) == 0

    def test_increment_col_freq_present_term(self):
        term_id = self.lexicon.add_term('horse')
        self.lexicon.increment_doc_freq(term_id, 3)
        self.lexicon.increment_col_freq(term_id, 5)

        self.lexicon.increment_col_freq(term_id, 3)

        assert self.lexicon.get_col_freq(term_id) == 8

    def test_increment_col_freq_absent_term(self):
        term_id = self.lexicon.add_term('horse')
        self.lexicon.increment_doc_freq(term_id, 3)
        self.lexicon.increment_col_freq(term_id, 5)

        absent_term_id = term_id + 1
        self.lexicon.increment_col_freq(term_id, 3)

        assert self.lexicon.get_col_freq(absent_term_id) == 0

    def test_decrement_col_freq_present_term_and_greater_than_zero(self):
        term_id = self.lexicon.add_term('horse')
        self.lexicon.increment_doc_freq(term_id, 3)
        self.lexicon.increment_col_freq(term_id, 5)

        self.lexicon.decrement_col_freq(term_id, 3)

        assert self.lexicon.get_col_freq(term_id) == 2

    def test_decrement_col_freq_present_term_and_equal_zero(self):
        term_id = self.lexicon.add_term('horse')
        self.lexicon.increment_doc_freq(term_id, 0)
        self.lexicon.increment_col_freq(term_id, 0)

        self.lexicon.decrement_col_freq(term_id, 1)

        assert self.lexicon.get_col_freq(term_id) == 0

    def test_decrement_col_freq_absent_term(self):
        term_id = self.lexicon.add_term('horse')
        self.lexicon.increment_doc_freq(term_id, 3)
        self.lexicon.increment_col_freq(term_id, 5)

        absent_term_id = term_id + 1
        self.lexicon.decrement_col_freq(absent_term_id, 3)

        assert self.lexicon.get_col_freq(absent_term_id) == 0

    def test_is_protected_term_present_term_true(self):
        term_id = self.lexicon.add_term('\'cause', is_protected=True)

        is_protected = self.lexicon.is_protected_term(term_id)
        assert is_protected == True

    def test_is_protected_term_present_term_false(self):
        term_id = self.lexicon.add_term('dog', is_protected=False)

        is_protected = self.lexicon.is_protected_term(term_id)
        assert is_protected == False

    def test_is_protected_term_absent_term(self):
        term_id = self.lexicon.add_term('dog', is_protected=False)

        absent_term_id = term_id + 1
        is_protected = self.lexicon.is_protected_term(absent_term_id)
        assert is_protected == False
