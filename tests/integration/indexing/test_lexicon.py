from sqlite3 import Connection

from pytest import fixture, raises

from sentencebank.indexing.lexicon import Lexicon
from tests.support.seeders import seed_term


class TestLexicon:
    _conn:    Connection
    _lexicon: Lexicon

    @fixture(autouse=True)
    def setup(self, db_connection: Connection):
        self._conn    = db_connection
        self._lexicon = Lexicon(self._conn)

    def test_contains_when_term_is_present(self):
        seed_term(self._conn, 'hello', doc_freq=1, col_freq=2)

        assert self._lexicon.contains('hello') == True

    def test_contains_when_term_is_absent(self):
        seed_term(self._conn, 'hello', doc_freq=1, col_freq=2)

        assert self._lexicon.contains('world') == False

    def test_contains_when_term_is_empty(self):
        seed_term(self._conn, 'hello', doc_freq=1, col_freq=2)

        assert self._lexicon.contains('') == False

    def test_get_term_when_term_is_present(self):
        term_id = seed_term(self._conn, 'language', doc_freq=6, col_freq=7)

        assert self._lexicon.get_term(term_id) == 'language'

    def test_get_term_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'language', doc_freq=6, col_freq=7)

        absent_term_id = term_id + 1
        assert self._lexicon.get_term(absent_term_id) is None

    def test_get_term_id_when_term_is_present(self):
        term_id = seed_term(self._conn, 'language', doc_freq=6, col_freq=7)

        assert self._lexicon.get_term_id('language') == term_id

    def test_get_term_id_when_term_is_absent(self):
        seed_term(self._conn, 'language', doc_freq=6, col_freq=7)

        assert self._lexicon.get_term_id('learning') is None

    def test_get_term_id_when_term_is_empty(self):
        seed_term(self._conn, 'language', doc_freq=6, col_freq=7)

        assert self._lexicon.get_term_id('') is None

    def test_get_doc_freq_when_term_is_present(self):
        term_id = seed_term(self._conn, 'language', doc_freq=6, col_freq=7)

        assert self._lexicon.get_doc_freq(term_id) == 6

    def test_get_doc_freq_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'language', doc_freq=6, col_freq=7)

        absent_term_id = term_id + 1
        assert self._lexicon.get_doc_freq(absent_term_id) == 0

    def test_get_col_freq_when_term_is_present(self):
        term_id = seed_term(self._conn, 'language', doc_freq=6, col_freq=7)

        assert self._lexicon.get_col_freq(term_id) == 7

    def test_get_col_freq_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'language', doc_freq=6, col_freq=7)

        absent_term_id = term_id + 1
        assert self._lexicon.get_col_freq(absent_term_id) == 0

    def test_get_all_terms_when_lexicon_is_not_empty(self):
        seed_term(self._conn, 'cat',       is_protected=False)
        seed_term(self._conn, '\'bout',    is_protected=True)
        seed_term(self._conn, 'dog',       is_protected=False)
        seed_term(self._conn, 'friends\'', is_protected=True)
        seed_term(self._conn, 'bird',      is_protected=False)

        terms = self._lexicon.get_all_terms()
        assert len(terms) == 5

        assert 'cat'       in terms
        assert 'dog'       in terms
        assert 'bird'      in terms
        assert 'friends\'' in terms
        assert '\'bout'    in terms

    def test_get_all_terms_when_lexicon_is_empty(self):
        terms = self._lexicon.get_all_terms()

        assert len(terms) == 0

    def test_get_all_protected_terms_when_lexicon_is_not_empty(self):
        seed_term(self._conn, '\'bout',    is_protected=True)
        seed_term(self._conn, 'day',       is_protected=False)
        seed_term(self._conn, 'friends\'', is_protected=True)
        seed_term(self._conn, 'night',     is_protected=False)
        seed_term(self._conn, '\'cause',   is_protected=True)

        terms = self._lexicon.get_all_protected_terms()

        assert len(terms) == 3
        assert '\'bout'    in terms
        assert 'friends\'' in terms
        assert '\'cause'   in terms
        assert 'day'       not in terms
        assert 'night'     not in terms

    def test_get_all_protected_terms_when_lexicon_is_empty(self):
        terms = self._lexicon.get_all_protected_terms()

        assert len(terms) == 0

    def test_size_when_lexicon_is_empty(self):
        assert self._lexicon.size() == 0

    def test_size_when_lexicon_is_not_empty(self):
        seed_term(self._conn, 'hello')
        seed_term(self._conn, 'world')

        assert self._lexicon.size() == 2

    def test_add_term_when_term_is_absent_and_is_not_empty(self):
        term_id = self._lexicon.add_term('bird')

        assert self._lexicon.contains('bird')      == True
        assert self._lexicon.get_term(term_id)     == 'bird'
        assert self._lexicon.get_term_id('bird')   == term_id
        assert self._lexicon.get_doc_freq(term_id) == 0
        assert self._lexicon.get_col_freq(term_id) == 0

    def test_add_term_when_term_is_absent_and_is_empty(self):
        with raises(Exception):
            self._lexicon.add_term('')

    def test_add_term_returns_existing_id_when_term_is_present(self):
        term_id_1 = seed_term(self._conn, 'bird')

        term_id_2 = self._lexicon.add_term('bird')
        assert term_id_1 == term_id_2

        assert self._lexicon.contains('bird')        == True
        assert self._lexicon.get_term(term_id_2)     == 'bird'
        assert self._lexicon.get_term_id('bird')     == term_id_2
        assert self._lexicon.get_doc_freq(term_id_2) == 0
        assert self._lexicon.get_col_freq(term_id_2) == 0

    def test_add_term_when_term_is_protected_and_absent(self):
        term_id = self._lexicon.add_term('\'bout', True)

        assert self._lexicon.contains('\'bout')         == True
        assert self._lexicon.get_term(term_id)          == '\'bout'
        assert self._lexicon.get_term_id('\'bout')      == term_id
        assert self._lexicon.get_doc_freq(term_id)      == 0
        assert self._lexicon.get_col_freq(term_id)      == 0
        assert self._lexicon.is_protected_term(term_id) == True

    def test_increment_doc_freq_when_term_is_present(self):
        term_id = seed_term(self._conn, 'bird', doc_freq=2, col_freq=6)

        self._lexicon.increment_doc_freq(term_id, 3)

        assert self._lexicon.get_doc_freq(term_id) == 5

    def test_increment_doc_freq_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'bird', doc_freq=2, col_freq=6)

        absent_term_id = term_id + 1
        self._lexicon.increment_doc_freq(absent_term_id, 3)

        assert self._lexicon.get_doc_freq(absent_term_id) == 0

    def test_decrement_doc_freq_when_term_is_present_and_greater_than_zero(self):
        term_id = seed_term(self._conn, 'bird', doc_freq=2, col_freq=6)

        self._lexicon.decrement_doc_freq(term_id, 1)

        assert self._lexicon.get_doc_freq(term_id) == 1

    def test_decrement_doc_freq_when_term_is_present_and_equals_zero(self):
        term_id = seed_term(self._conn, 'bird', doc_freq=0, col_freq=0)

        self._lexicon.decrement_doc_freq(term_id, 3)

        assert self._lexicon.get_doc_freq(term_id) == 0

    def test_decrement_doc_freq_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'bird', doc_freq=0, col_freq=0)

        absent_term_id = term_id + 1
        self._lexicon.decrement_doc_freq(absent_term_id, 3)

        assert self._lexicon.get_doc_freq(absent_term_id) == 0

    def test_increment_col_freq_when_term_is_present(self):
        term_id = seed_term(self._conn, 'horse', doc_freq=3, col_freq=5)

        self._lexicon.increment_col_freq(term_id, 3)

        assert self._lexicon.get_col_freq(term_id) == 8

    def test_increment_col_freq_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'horse', doc_freq=3, col_freq=5)

        absent_term_id = term_id + 1
        self._lexicon.increment_col_freq(term_id, 3)

        assert self._lexicon.get_col_freq(absent_term_id) == 0

    def test_decrement_col_freq_when_term_is_present_and_greater_than_zero(self):
        term_id = seed_term(self._conn, 'horse', doc_freq=3, col_freq=5)

        self._lexicon.decrement_col_freq(term_id, 3)

        assert self._lexicon.get_col_freq(term_id) == 2

    def test_decrement_col_freq_when_term_is_present_and_equals_zero(self):
        term_id = seed_term(self._conn, 'horse', doc_freq=0, col_freq=0)

        self._lexicon.decrement_col_freq(term_id, 1)

        assert self._lexicon.get_col_freq(term_id) == 0

    def test_decrement_col_freq_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'horse', doc_freq=3, col_freq=5)

        absent_term_id = term_id + 1
        self._lexicon.decrement_col_freq(absent_term_id, 3)

        assert self._lexicon.get_col_freq(absent_term_id) == 0

    def test_is_protected_term_when_term_is_present_and_is_protected(self):
        term_id = seed_term(self._conn, '\'cause', is_protected=True)

        is_protected = self._lexicon.is_protected_term(term_id)
        assert is_protected == True

    def test_is_protected_term_when_term_is_present_and_is_not_protected(self):
        term_id = seed_term(self._conn, 'dog', is_protected=False)

        is_protected = self._lexicon.is_protected_term(term_id)
        assert is_protected == False

    def test_is_protected_term_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'dog', is_protected=False)

        absent_term_id = term_id + 1
        is_protected = self._lexicon.is_protected_term(absent_term_id)
        assert is_protected == False

    def test_purge_unused_terms_when_lexicon_has_unused_terms(self):
        term_id_1 = seed_term(self._conn, 'cat',   doc_freq=3, col_freq=5)
        term_id_2 = seed_term(self._conn, 'day',   doc_freq=0, col_freq=0)
        term_id_3 = seed_term(self._conn, 'dog',   doc_freq=2, col_freq=2)
        term_id_4 = seed_term(self._conn, 'night', doc_freq=0, col_freq=0)
        term_id_5 = seed_term(self._conn, 'bird',  doc_freq=1, col_freq=1)

        purged_terms = self._lexicon.purge_unused_terms()
        assert len(purged_terms) == 2
        
        assert 'day'   in purged_terms
        assert 'night' in purged_terms

        assert self._lexicon.get_term(term_id_1) == 'cat'
        assert self._lexicon.get_term(term_id_2) == None
        assert self._lexicon.get_term(term_id_3) == 'dog'
        assert self._lexicon.get_term(term_id_4) == None
        assert self._lexicon.get_term(term_id_5) == 'bird'

    def test_purge_unused_terms_when_lexicon_has_no_unused_terms(self):
        term_id_1 = seed_term(self._conn, 'cat',  doc_freq=3, col_freq=5)
        term_id_2 = seed_term(self._conn, 'dog',  doc_freq=2, col_freq=3)
        term_id_3 = seed_term(self._conn, 'bird', doc_freq=1, col_freq=1)

        purged_terms = self._lexicon.purge_unused_terms()
        assert len(purged_terms) == 0

        assert self._lexicon.get_term(term_id_1) == 'cat'
        assert self._lexicon.get_term(term_id_2) == 'dog'
        assert self._lexicon.get_term(term_id_3) == 'bird'

    def test_purge_unused_terms_when_lexicon_is_empty(self):
        purged_terms = self._lexicon.purge_unused_terms()

        assert len(purged_terms) == 0

    def test_purge_unused_terms_preseves_protected_terms(self):
        term_id_1 = seed_term(self._conn, '\'cause', is_protected=True,  doc_freq=1, col_freq=2)
        term_id_2 = seed_term(self._conn, '\'bout',  is_protected=True,  doc_freq=0, col_freq=0)

        purged_terms = self._lexicon.purge_unused_terms()
        assert len(purged_terms) == 0

        assert self._lexicon.get_term(term_id_1) == '\'cause'
        assert self._lexicon.get_term(term_id_2) == '\'bout'

    def test_get_term_ids_when_terms_is_present(self):
        term_id_1 = seed_term(self._conn, 'dog')
        term_id_2 = seed_term(self._conn, 'day')
        term_id_3 = seed_term(self._conn, 'cat')
        term_id_4 = seed_term(self._conn, 'night')
        term_id_5 = seed_term(self._conn, 'bird')

        terms    = ['dog', 'cat', 'bird']
        term_ids = self._lexicon.get_term_ids(terms)
        assert len(term_ids) == 3

        assert term_id_1 in term_ids
        assert term_id_3 in term_ids
        assert term_id_5 in term_ids
        assert term_id_2 not in term_ids
        assert term_id_4 not in term_ids

    def test_get_term_ids_when_terms_is_absent(self):
        seed_term(self._conn, 'dog')
        seed_term(self._conn, 'cat')
        seed_term(self._conn, 'bird')

        terms    = ['day', 'night']
        term_ids = self._lexicon.get_term_ids(terms)
        assert len(term_ids) == 0

    def test_get_term_ids_when_terms_is_empty(self):
        seed_term(self._conn, 'dog')
        seed_term(self._conn, 'cat')
        seed_term(self._conn, 'bird')

        terms    = []
        term_ids = self._lexicon.get_term_ids(terms)
        assert len(term_ids) == 0
