from sqlite3 import Connection

from pytest import fixture

from sentencebank.indexing.lemmatizer import Lemmatizer
from tests.support.seeders import seed_lemma, seed_term


class TestLemmatizer:
    _conn:       Connection
    _lemmatizer: Lemmatizer

    @fixture(autouse=True)
    def setup(self, db_connection: Connection):
        self._conn       = db_connection
        self._lemmatizer = Lemmatizer(self._conn)

    def test_term_count_when_lemmatizer_is_empty(self):
        assert self._lemmatizer.term_count() == 0

    def test_term_count_when_lemmatizer_is_not_empty(self):
        term_id_1 = seed_term(self._conn, 'put')
        term_id_2 = seed_term(self._conn, 'puts')
        term_id_3 = seed_term(self._conn, 'putting')

        seed_lemma(self._conn, term_id_1, term_id_1)
        seed_lemma(self._conn, term_id_2, term_id_1)
        seed_lemma(self._conn, term_id_3, term_id_1)

        assert self._lemmatizer.term_count() == 3

    def test_lemma_count_when_lemmatizer_is_empty(self):
        assert self._lemmatizer.lemma_count() == 0

    def test_lemma_count_when_lemmatizer_is_not_empty(self):
        term_id_1 = seed_term(self._conn, 'put')
        term_id_2 = seed_term(self._conn, 'puts')
        term_id_3 = seed_term(self._conn, 'putting')

        seed_lemma(self._conn, term_id_1, term_id_1)
        seed_lemma(self._conn, term_id_2, term_id_1)
        seed_lemma(self._conn, term_id_3, term_id_1)

        assert self._lemmatizer.lemma_count() == 1

    def test_add_term_when_term_is_absent(self):
        term_id_1 = seed_term(self._conn, 'was')
        term_id_2 = seed_term(self._conn, 'be')

        self._lemmatizer.add_term(term_id_1, term_id_2)

        assert self._lemmatizer.term_count()  == 1
        assert self._lemmatizer.lemma_count() == 1

        lemma_id = self._lemmatizer.get_lemma(term_id_1)
        assert lemma_id == term_id_2

    def test_add_term_ignores_duplicate_term_when_term_is_present(self):
        term_id_1 = seed_term(self._conn, 'was')
        term_id_2 = seed_term(self._conn, 'be')
        seed_lemma(self._conn, term_id_1, term_id_2)

        self._lemmatizer.add_term(term_id_1, term_id_2)

        assert self._lemmatizer.term_count()  == 1
        assert self._lemmatizer.lemma_count() == 1

        lemma_id = self._lemmatizer.get_lemma(term_id_1)
        assert lemma_id == term_id_2

    def test_remove_term_when_term_is_present(self):
        term_id_1 = seed_term(self._conn, 'were')
        term_id_2 = seed_term(self._conn, 'where')
        term_id_3 = seed_term(self._conn, 'be')

        seed_lemma(self._conn, term_id_1, term_id_3)
        seed_lemma(self._conn, term_id_2, term_id_3)

        self._lemmatizer.remove_term(term_id_2)

        assert self._lemmatizer.term_count()  == 1
        assert self._lemmatizer.lemma_count() == 1

        lemma_id = self._lemmatizer.get_lemma(term_id_2)
        assert lemma_id == term_id_2
        lemma_id = self._lemmatizer.get_lemma(term_id_1)
        assert lemma_id == term_id_3

    def test_remove_term_when_term_is_absent(self):
        term_id_1 = seed_term(self._conn, 'were')
        term_id_2 = seed_term(self._conn, 'where')
        term_id_3 = seed_term(self._conn, 'be')

        seed_lemma(self._conn, term_id_1, term_id_3)

        has_removed = self._lemmatizer.remove_term(term_id_2)
        assert has_removed == False

        assert self._lemmatizer.term_count()  == 1
        assert self._lemmatizer.lemma_count() == 1

        assert self._lemmatizer.get_lemma(term_id_1) == term_id_3

    def test_get_lemma_when_term_is_present(self):
        term_id_1 = seed_term(self._conn, 'is')
        term_id_2 = seed_term(self._conn, 'are')
        term_id_3 = seed_term(self._conn, 'be')

        seed_lemma(self._conn, term_id_1, term_id_3)
        seed_lemma(self._conn, term_id_2, term_id_3)

        lemma_id = self._lemmatizer.get_lemma(term_id_1)
        assert lemma_id == term_id_3

    def test_get_lemma_when_term_is_absent(self):
        term_id_1 = seed_term(self._conn, 'is')
        term_id_2 = seed_term(self._conn, 'are')
        term_id_3 = seed_term(self._conn, 'be')

        seed_lemma(self._conn, term_id_1, term_id_3)

        lemma_id = self._lemmatizer.get_lemma(term_id_2)
        assert lemma_id == term_id_2

    def test_get_terms_when_lemma_is_present(self):
        term_id_1 = seed_term(self._conn, 'set')
        term_id_2 = seed_term(self._conn, 'sets')
        term_id_3 = seed_term(self._conn, 'setting')

        seed_lemma(self._conn, term_id_1, term_id_3)
        seed_lemma(self._conn, term_id_2, term_id_3)
        seed_lemma(self._conn, term_id_3, term_id_3)

        term_ids = self._lemmatizer.get_terms(term_id_3) 
        assert len(term_ids) == 3

        assert term_id_1 in term_ids
        assert term_id_2 in term_ids
        assert term_id_3 in term_ids

    def test_get_terms_when_lemma_is_absent(self):
        term_id_1 = seed_term(self._conn, 'set')
        term_id_2 = seed_term(self._conn, 'sets')
        term_id_3 = seed_term(self._conn, 'setting')
        term_id_4 = seed_term(self._conn, 'be')

        seed_lemma(self._conn, term_id_1, term_id_3)
        seed_lemma(self._conn, term_id_2, term_id_3)
        seed_lemma(self._conn, term_id_3, term_id_3)

        term_ids = self._lemmatizer.get_terms(term_id_4) 
        assert len(term_ids) == 0

    def test_contains_term_when_term_is_present(self):
        term_id_1 = seed_term(self._conn, 'has')
        term_id_2 = seed_term(self._conn, 'had')
        term_id_3 = seed_term(self._conn, 'have')

        seed_lemma(self._conn, term_id_1, term_id_3)
        seed_lemma(self._conn, term_id_2, term_id_3)

        assert self._lemmatizer.contains_term(term_id_1) == True

    def test_contains_term_when_term_is_absent(self):
        term_id_1 = seed_term(self._conn, 'has')
        term_id_2 = seed_term(self._conn, 'had')
        term_id_3 = seed_term(self._conn, 'have')

        seed_lemma(self._conn, term_id_1, term_id_3)

        assert self._lemmatizer.contains_term(term_id_2) == False

    def test_contains_lemma_when_lemma_is_present(self):
        term_id_1 = seed_term(self._conn, 'has')
        term_id_2 = seed_term(self._conn, 'had')
        term_id_3 = seed_term(self._conn, 'have')

        seed_lemma(self._conn, term_id_1, term_id_3)
        seed_lemma(self._conn, term_id_2, term_id_3)

        assert self._lemmatizer.contains_lemma(term_id_3) == True

    def test_contains_lemma_when_lemma_is_absent(self):
        term_id_1 = seed_term(self._conn, 'has')
        term_id_2 = seed_term(self._conn, 'had')
        term_id_3 = seed_term(self._conn, 'have')
        term_id_4 = seed_term(self._conn, 'be')

        seed_lemma(self._conn, term_id_1, term_id_3)
        seed_lemma(self._conn, term_id_2, term_id_3)

        assert self._lemmatizer.contains_lemma(term_id_4) == False
