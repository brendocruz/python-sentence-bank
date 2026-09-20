from sentencebank.indexing.index import InvertedIndex, Posting
from sentencebank.db.database import init_db
from sqlite3 import connect
from pytest import fixture


class TestInvertedIndex:
    _index: InvertedIndex

    DOCUMENTS = {'pizza_1': ('I eat a pizza today.',            1),
                 'book_1':  ('The book is on the shelf.',       2),
                 'park_1':  ('They have gone to the park.',     3),
                 'cat_1':   ('I have an orange cat.',           4),
                 'cat_2':   ('A cat was sitting on the chair.', 5),
                 'cat_3':   ('Cat got your tongue?',            6),}

    TERMS = {'pizza': 1,
             'book':  2,
             'park':  3,
             'cat':   4,}

    @fixture(autouse=True)
    def setup(self):
        conn = connect(':memory:')
        conn.execute('PRAGMA foreign_keys = ON;')

        init_db(conn)
        self._index = InvertedIndex(conn)

        lexicon_data = [(term_id, term) for term, term_id in self.TERMS.items()]
        conn.executemany(
                'INSERT INTO lexicon (term_id, term) VALUES (?, ?)',
                lexicon_data)

        document_data = [(doc[1], doc[0]) for doc in self.DOCUMENTS.values()]
        conn.executemany(
                'INSERT INTO documents (doc_id, text) VALUES (?, ?)',
                document_data)

        yield

        conn.close()

    def test_posting_count_zero(self):
        assert self._index.posting_count() == 0

    def test_posting_count_non_zero(self):
        term_id = self.TERMS['pizza']
        doc_id  = self.DOCUMENTS['pizza_1'][1]
        posting = Posting(doc_id=doc_id, position=3, start=8, end=13)
        self._index.add_posting(term_id, posting)

        term_id = self.TERMS['book']
        doc_id  = self.DOCUMENTS['book_1'][1]
        posting = Posting(doc_id=doc_id, position=1, start=4, end=8)
        self._index.add_posting(term_id, posting)

        term_id = self.TERMS['park']
        doc_id  = self.DOCUMENTS['park_1'][1]
        posting = Posting(doc_id=doc_id, position=5, start=22, end=26)
        self._index.add_posting(term_id, posting)

        assert self._index.posting_count() == 3

    def test_get_postings_present_term(self):
        term_id  = self.TERMS['cat']
        doc_id_1 = self.DOCUMENTS['cat_1'][1]
        posting  = Posting(doc_id=doc_id_1, position=4, start=17, end=20)
        self._index.add_posting(term_id, posting)

        doc_id_2 = self.DOCUMENTS['cat_2'][1]
        posting  = Posting(doc_id=doc_id_2, position=1, start=2, end=5)
        self._index.add_posting(term_id, posting)

        doc_id_3 = self.DOCUMENTS['cat_3'][1]
        posting  = Posting(doc_id=doc_id_3, position=0, start=0, end=3)
        self._index.add_posting(term_id, posting)

        postings = self._index.get_postings(term_id)
        assert len(postings) == 3

        assert postings[0].doc_id   == doc_id_1
        assert postings[0].position == 4
        assert postings[0].start    == 17
        assert postings[0].end      == 20

        assert postings[1].doc_id   == doc_id_2
        assert postings[1].position == 1
        assert postings[1].start    == 2
        assert postings[1].end      == 5

        assert postings[2].doc_id   == doc_id_3
        assert postings[2].position == 0
        assert postings[2].start    == 0
        assert postings[2].end      == 3

    def test_get_postings_absent_term(self):
        doc_id  = self.DOCUMENTS['pizza_1'][1]
        posting = Posting(doc_id=doc_id, position=3, start=8, end=13)
        self._index.add_posting(self.TERMS['pizza'], posting)

        absent_term_id = self.TERMS['park']
        postings = self._index.get_postings(absent_term_id)
        assert len(postings) == 0

    def test_add_posting_absent_term(self):
        term_id = self.TERMS['pizza']
        doc_id  = self.DOCUMENTS['pizza_1'][1]
        posting = Posting(doc_id=doc_id, position=4, start=8, end=13)

        self._index.add_posting(term_id, posting)
        assert self._index.posting_count() == 1

        postings = self._index.get_postings(term_id)
        assert postings[0].doc_id   == doc_id
        assert postings[0].position == 4
        assert postings[0].start    == 8
        assert postings[0].end      == 13

    def test_add_posting_present_term(self):
        term_id  = self.TERMS['cat']
        doc_id_1 = self.DOCUMENTS['cat_1'][1]
        posting  = Posting(doc_id=doc_id_1, position=4, start=17, end=20)
        self._index.add_posting(term_id, posting)

        doc_id_2 = self.DOCUMENTS['cat_2'][1]
        posting  = Posting(doc_id=doc_id_2, position=1, start=2, end=5)
        self._index.add_posting(term_id, posting)

        assert self._index.posting_count() == 2

        postings = self._index.get_postings(term_id)
        assert postings[0].doc_id   == doc_id_1
        assert postings[0].position == 4
        assert postings[0].start    == 17
        assert postings[0].end      == 20

        postings = self._index.get_postings(term_id)
        assert postings[1].doc_id   == doc_id_2
        assert postings[1].position == 1
        assert postings[1].start    == 2
        assert postings[1].end      == 5

    def test_remove_posting_present_term(self):
        term_id = self.TERMS['book']
        doc_id  = self.DOCUMENTS['book_1'][1]
        posting = Posting(doc_id=doc_id, position=1, start=4, end=8)
        self._index.add_posting(term_id, posting)

        was_removed = self._index.remove_posting(term_id, doc_id, 1)
        assert was_removed == True

        postings = self._index.get_postings(term_id)
        assert len(postings) == 0

    def test_remove_posting_absent_term(self):
        term_id = self.TERMS['book']
        doc_id  = self.DOCUMENTS['book_1'][1]
        posting = Posting(doc_id=doc_id, position=1, start=4, end=8)
        self._index.add_posting(term_id, posting)

        absent_term_id = self.TERMS['pizza']
        was_removed    = self._index.remove_posting(absent_term_id, doc_id, 1)
        assert was_removed == False

        postings = self._index.get_postings(absent_term_id)
        assert len(postings) == 0

        postings = self._index.get_postings(term_id)
        assert len(postings) == 1

        assert postings[0].doc_id   == doc_id
        assert postings[0].position == 1
        assert postings[0].start    == 4
        assert postings[0].end      == 8

    def test_remove_posting_absent_document(self):
        term_id = self.TERMS['book']
        doc_id  = self.DOCUMENTS['book_1'][1]
        posting = Posting(doc_id=doc_id, position=1, start=4, end=8)
        self._index.add_posting(term_id, posting)

        absent_doc_id = doc_id + 1
        was_removed   = self._index.remove_posting(term_id, absent_doc_id, 1)
        assert was_removed == False

        postings = self._index.get_postings(term_id)
        assert len(postings) == 1

        assert postings[0].doc_id   == doc_id
        assert postings[0].position == 1
        assert postings[0].start    == 4
        assert postings[0].end      == 8

    def test_remove_posting_absent_position(self):
        term_id = self.TERMS['book']
        doc_id  = self.DOCUMENTS['book_1'][1]
        posting = Posting(doc_id=doc_id, position=1, start=4, end=8)
        self._index.add_posting(term_id, posting)

        was_removed = self._index.remove_posting(term_id, doc_id, 2)
        assert was_removed == False

        postings = self._index.get_postings(term_id)
        assert len(postings) == 1

        assert postings[0].doc_id   == doc_id
        assert postings[0].position == 1
        assert postings[0].start    == 4
        assert postings[0].end      == 8

    def test_remove_document_postings_present_document(self):
        term_id = self.TERMS['cat']
        doc_id  = self.DOCUMENTS['cat_3'][1]
        posting = Posting(doc_id=doc_id, position=0, start=0,  end=3)
        self._index.add_posting(term_id, posting)
        posting = Posting(doc_id=doc_id, position=1, start=4,  end=7)
        self._index.add_posting(term_id, posting)
        posting = Posting(doc_id=doc_id, position=2, start=8,  end=12)
        self._index.add_posting(term_id, posting)
        posting = Posting(doc_id=doc_id, position=3, start=13, end=19)
        self._index.add_posting(term_id, posting)

        was_removed = self._index.remove_document_postings(doc_id)
        assert was_removed == True

        postings = self._index.get_postings(term_id)
        assert len(postings) == 0

    def test_remove_document_postings_absent_document(self):
        term_id = self.TERMS['cat']
        doc_id  = self.DOCUMENTS['cat_3'][1]
        posting = Posting(doc_id=doc_id, position=3, start=13, end=19)
        self._index.add_posting(term_id, posting)

        absent_doc_id = self.DOCUMENTS['cat_2'][1]
        was_removed = self._index.remove_document_postings(absent_doc_id)
        assert was_removed == False

        postings = self._index.get_postings(term_id)
        assert len(postings) == 1

    def test_contains_posting_present_posting(self):
        term_id = self.TERMS['park']
        doc_id  = self.DOCUMENTS['park_1'][1]
        posting = Posting(doc_id=doc_id, position=5, start=22, end=26)
        self._index.add_posting(term_id, posting)

        assert self._index.contains_posting(self.TERMS['park'], doc_id, 5) == True

    def test_contains_posting_absent_term(self):
        term_id = self.TERMS['park']
        doc_id  = self.DOCUMENTS['park_1'][1]
        posting = Posting(doc_id=doc_id, position=5, start=22, end=26)
        self._index.add_posting(term_id, posting)

        absent_term_id = self.TERMS['pizza']
        assert self._index.contains_posting(absent_term_id, doc_id, 5) == False

    def test_contains_posting_absent_document(self):
        term_id = self.TERMS['park']
        doc_id  = self.DOCUMENTS['park_1'][1]
        posting = Posting(doc_id=doc_id, position=5, start=22, end=26)
        self._index.add_posting(term_id, posting)

        absent_doc_id = doc_id + 1
        assert self._index.contains_posting(term_id, absent_doc_id, 5) == False

    def test_contains_posting_absent_position(self):
        position = 5
        term_id  = self.TERMS['park']
        doc_id   = self.DOCUMENTS['park_1'][1]
        posting  = Posting(doc_id=doc_id, position=position, start=22, end=26)
        self._index.add_posting(term_id, posting)

        absent_position = position + 1
        assert self._index.contains_posting(term_id, doc_id, absent_position) == False

    def test_contains_term_present_term(self):
        term_id = self.TERMS['park']
        doc_id  = self.DOCUMENTS['park_1'][1]
        posting = Posting(doc_id=doc_id, position=5, start=22, end=26)
        self._index.add_posting(term_id, posting)

        assert self._index.contains_term(term_id) == True

    def test_contains_term_absent_term(self):
        term_id = self.TERMS['park']
        doc_id  = self.DOCUMENTS['park_1'][1]
        posting = Posting(doc_id=doc_id, position=5, start=22, end=26)
        self._index.add_posting(term_id, posting)

        absent_term_id = self.TERMS['pizza']
        assert self._index.contains_term(absent_term_id) == False
