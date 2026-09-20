from sentencebank.indexing.lemmatizer import Lemmatizer
from sentencebank.db.database import init_db
from sqlite3 import connect, IntegrityError
from pytest import fixture, raises


class TestLemmatizer:
    lemmatizer: Lemmatizer

    TERMS = {'be':       1,
             'was':      2,
             'were':     3,
             'been':     4,
             'is':       5,
             'are':      6,
             'put':     10,
             'puts':    11,
             'putting': 12,
             'set':     20,
             'sets':    21,
             'setting': 22,
             'have':    30,
             'has':     31,
             'had':     32,
             'where':   50,}

    @fixture(autouse=True)
    def setup(self):
        conn = connect(':memory:')

        init_db(conn)
        self.lemmatizer = Lemmatizer(conn)

        lexicon_data = [(term_id, term) for term, term_id in self.TERMS.items()]
        conn.executemany(
                'INSERT INTO lexicon (term_id, term) VALUES (?, ?)',
                lexicon_data)

        yield

        conn.close()

    def test_term_count_zero(self):
        assert self.lemmatizer.term_count() == 0

    def test_term_count_non_zero(self):
        self.lemmatizer.add_term(self.TERMS['put'],     self.TERMS['put'])
        self.lemmatizer.add_term(self.TERMS['puts'],    self.TERMS['put'])
        self.lemmatizer.add_term(self.TERMS['putting'], self.TERMS['put'])

        assert self.lemmatizer.term_count() == 3

    def test_lemma_count_zero(self):
        assert self.lemmatizer.lemma_count() == 0

    def test_lemma_count_non_zero(self):
        self.lemmatizer.add_term(self.TERMS['put'],     self.TERMS['put'])
        self.lemmatizer.add_term(self.TERMS['puts'],    self.TERMS['put'])
        self.lemmatizer.add_term(self.TERMS['putting'], self.TERMS['put'])

        assert self.lemmatizer.lemma_count() == 1

    def test_add_term_absent_term(self):
        self.lemmatizer.add_term(self.TERMS['was'], self.TERMS['be'])

        assert self.lemmatizer.term_count()  == 1
        assert self.lemmatizer.lemma_count() == 1

        lemma_id = self.lemmatizer.lemmatize(self.TERMS['was'])
        assert lemma_id == self.TERMS['be']

        term_ids = self.lemmatizer.get_terms(self.TERMS['be']) 
        assert len(term_ids) == 1

        assert self.TERMS['was'] in term_ids

    def test_add_term_present_term_reassigns_lemma_raises_error(self):
        self.lemmatizer.add_term(self.TERMS['was'], self.TERMS['been'])

        with raises(IntegrityError):
            self.lemmatizer.add_term(self.TERMS['was'], self.TERMS['be'])

    def test_remove_term_present_term(self):
        self.lemmatizer.add_term(self.TERMS['were'],  self.TERMS['be'])
        self.lemmatizer.add_term(self.TERMS['where'], self.TERMS['be'])

        self.lemmatizer.remove_term(self.TERMS['where'])

        assert self.lemmatizer.term_count()  == 1
        assert self.lemmatizer.lemma_count() == 1

        lemma_id = self.lemmatizer.lemmatize(self.TERMS['where'])
        assert lemma_id == self.TERMS['where']
        lemma_id = self.lemmatizer.lemmatize(self.TERMS['were'])
        assert lemma_id == self.TERMS['be']

        term_ids = self.lemmatizer.get_terms(self.TERMS['be'])
        assert len(term_ids) == 1

        assert self.TERMS['were'] in term_ids

    def test_remove_term_absent_term(self):
        self.lemmatizer.add_term(self.TERMS['were'], self.TERMS['be'])

        has_removed = self.lemmatizer.remove_term(self.TERMS['where'])
        assert has_removed == False

        assert self.lemmatizer.term_count()  == 1
        assert self.lemmatizer.lemma_count() == 1

        assert self.lemmatizer.lemmatize(self.TERMS['were']) == self.TERMS['be']

        term_ids = self.lemmatizer.get_terms(self.TERMS['be'])
        assert len(term_ids) == 1

        assert self.TERMS['were'] in term_ids

    def test_lemmatize_present_variation(self):
        self.lemmatizer.add_term(self.TERMS['is'], self.TERMS['be'])

        lemma_id = self.lemmatizer.lemmatize(self.TERMS['is'])
        assert lemma_id == self.TERMS['be']

    def test_lemmatize_absent_term(self):
        self.lemmatizer.add_term(self.TERMS['is'], self.TERMS['be'])

        lemma_id = self.lemmatizer.lemmatize(self.TERMS['are'])
        assert lemma_id == self.TERMS['are']

    def test_get_terms_present_lemma(self):
        self.lemmatizer.add_term(self.TERMS['set'],     self.TERMS['set'])
        self.lemmatizer.add_term(self.TERMS['sets'],    self.TERMS['set'])
        self.lemmatizer.add_term(self.TERMS['setting'], self.TERMS['set'])

        term_ids = self.lemmatizer.get_terms(self.TERMS['set']) 
        assert len(term_ids) == 3

        assert self.TERMS['set']     in term_ids
        assert self.TERMS['sets']    in term_ids
        assert self.TERMS['setting'] in term_ids

    def test_get_term_absent_lemma(self):
        self.lemmatizer.add_term(self.TERMS['set'],     self.TERMS['set'])
        self.lemmatizer.add_term(self.TERMS['sets'],    self.TERMS['set'])
        self.lemmatizer.add_term(self.TERMS['setting'], self.TERMS['set'])

        term_ids = self.lemmatizer.get_terms(self.TERMS['be']) 
        assert len(term_ids) == 0

    def test_contains_term_present_term(self):
        self.lemmatizer.add_term(self.TERMS['has'], self.TERMS['have'])

        assert self.lemmatizer.contains_term(self.TERMS['has']) == True

    def test_contains_term_absent_term(self):
        self.lemmatizer.add_term(self.TERMS['has'], self.TERMS['have'])

        assert self.lemmatizer.contains_term(self.TERMS['had']) == False

    def test_contains_lemma_present_lemma(self):
        self.lemmatizer.add_term(self.TERMS['has'], self.TERMS['have'])

        assert self.lemmatizer.contains_lemma(self.TERMS['have']) == True

    def test_contains_lemma_absent_lemma(self):
        self.lemmatizer.add_term(self.TERMS['has'], self.TERMS['have'])

        assert self.lemmatizer.contains_lemma(self.TERMS['be']) == False
