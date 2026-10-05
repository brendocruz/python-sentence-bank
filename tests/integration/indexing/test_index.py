from sqlite3 import Connection

from pytest import fixture

from sentencebank.indexing.index import InvertedIndex
from sentencebank.indexing.types import TermPosition, Posting
from tests.support.builders.posting import PostingTestBuilder
from tests.support.seeders import seed_document, seed_term


class TestInvertedIndex:
    _conn:    Connection
    _index:   InvertedIndex
    _builder: PostingTestBuilder

    @fixture(autouse=True)
    def setup(self, db_connection: Connection):
        self._conn = db_connection
        self._index   = InvertedIndex(self._conn)
        self._builder = PostingTestBuilder()

    def test_posting_when_count_is_zero(self):
        assert self._index.posting_count() == 0

    def test_posting_when_count_is_non_zero(self):
        term_id   = seed_term(self._conn, 'cat')
        doc_id_1  = seed_document(self._conn, 'I have a cat.')
        doc_id_2  = seed_document(self._conn, 'The cat is on the chair.')
        doc_id_3  = seed_document(self._conn, 'Where is the cat?')
        posting_1 = self._builder.build(doc_id_1, 3, 9, 12)
        posting_2 = self._builder.build(doc_id_2, 1, 4, 7)
        posting_3 = self._builder.build(doc_id_3, 3, 13, 16)

        self._index.add_posting(term_id, posting_1)
        self._index.add_posting(term_id, posting_2)
        self._index.add_posting(term_id, posting_3)

        assert self._index.posting_count() == 3

    def test_get_postings_when_term_is_present(self):
        term_id   = seed_term(self._conn, 'cat')
        doc_id_1  = seed_document(self._conn, 'I have a cat.')
        doc_id_2  = seed_document(self._conn, 'The cat is on the chair.')
        doc_id_3  = seed_document(self._conn, 'Where is the cat?')
        posting_1 = self._builder.build(doc_id_1, 3, 9, 12)
        posting_2 = self._builder.build(doc_id_2, 1, 4, 7)
        posting_3 = self._builder.build(doc_id_3, 3, 13, 16)

        self._index.add_posting(term_id, posting_1)
        self._index.add_posting(term_id, posting_2)
        self._index.add_posting(term_id, posting_3)

        postings = self._index.get_postings_by_term_id(term_id)
        assert len(postings) == 3

        assert postings[0].doc_id   == doc_id_1
        assert postings[0].position == 3
        assert postings[0].start    == 9
        assert postings[0].end      == 12

        assert postings[1].doc_id   == doc_id_2
        assert postings[1].position == 1
        assert postings[1].start    == 4
        assert postings[1].end      == 7

        assert postings[2].doc_id   == doc_id_3
        assert postings[2].position == 3
        assert postings[2].start    == 13
        assert postings[2].end      == 16

    def test_get_postings_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'cat')
        doc_id  = seed_document(self._conn, 'I have a cat.')
        posting = self._builder.build(doc_id, 3, 9, 12)
        self._index.add_posting(term_id, posting)

        absent_term_id = term_id + 1
        postings = self._index.get_postings_by_term_id(absent_term_id)
        assert len(postings) == 0

    def test_add_posting_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'hello')
        doc_id  = seed_document(self._conn, 'Hello.')
        posting = self._builder.build(doc_id, 4, 8, 13)

        self._index.add_posting(term_id, posting)
        assert self._index.posting_count() == 1

        postings = self._index.get_postings_by_term_id(term_id)
        assert postings[0].doc_id   == doc_id
        assert postings[0].position == 4
        assert postings[0].start    == 8
        assert postings[0].end      == 13

    def test_add_posting_when_term_is_present(self):
        term_id   = seed_term(self._conn, 'cat')
        doc_id_1  = seed_document(self._conn, 'I have a cat.')
        doc_id_2  = seed_document(self._conn, 'The cat is on the chair.')
        posting_1 = self._builder.build(doc_id_1, 3, 9, 12)
        posting_2 = self._builder.build(doc_id_2, 1, 4, 7)

        self._index.add_posting(term_id, posting_1)
        self._index.add_posting(term_id, posting_2)

        assert self._index.posting_count() == 2

        postings = self._index.get_postings_by_term_id(term_id)
        assert postings[0].doc_id   == doc_id_1
        assert postings[0].position == 3
        assert postings[0].start    == 9
        assert postings[0].end      == 12

        postings = self._index.get_postings_by_term_id(term_id)
        assert postings[1].doc_id   == doc_id_2
        assert postings[1].position == 1
        assert postings[1].start    == 4
        assert postings[1].end      == 7

    def test_remove_posting_when_term_is_present(self):
        term_id = seed_term(self._conn, 'book')
        doc_id  = seed_document(self._conn, 'The book is on the shelf.')
        posting = self._builder.build(doc_id, 1, 4, 8)
        self._index.add_posting(term_id, posting)

        was_removed = self._index.remove_posting(term_id, doc_id, 1)
        assert was_removed == True

        postings = self._index.get_postings_by_term_id(term_id)
        assert len(postings) == 0

    def test_remove_posting_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'book')
        doc_id  = seed_document(self._conn, 'The book is on the shelf.')
        posting = Posting(doc_id=doc_id, position=1, start=4, end=8)
        self._index.add_posting(term_id, posting)

        absent_term_id = term_id + 1
        was_removed    = self._index.remove_posting(absent_term_id, doc_id, 1)
        assert was_removed == False

        postings = self._index.get_postings_by_term_id(absent_term_id)
        assert len(postings) == 0

        postings = self._index.get_postings_by_term_id(term_id)
        assert len(postings) == 1

        assert postings[0].doc_id   == doc_id
        assert postings[0].position == 1
        assert postings[0].start    == 4
        assert postings[0].end      == 8

    def test_remove_posting_when_document_is_absent(self):
        term_id = seed_term(self._conn, 'book')
        doc_id  = seed_document(self._conn, 'The book is on the shelf.')
        posting = Posting(doc_id=doc_id, position=1, start=4, end=8)
        self._index.add_posting(term_id, posting)

        absent_doc_id = doc_id + 1
        was_removed   = self._index.remove_posting(term_id, absent_doc_id, 1)
        assert was_removed == False

        postings = self._index.get_postings_by_term_id(term_id)
        assert len(postings) == 1

        assert postings[0].doc_id   == doc_id
        assert postings[0].position == 1
        assert postings[0].start    == 4
        assert postings[0].end      == 8

    def test_remove_posting_when_position_is_absent(self):
        term_id = seed_term(self._conn, 'book')
        doc_id  = seed_document(self._conn, 'The book is on the shelf.')
        posting = Posting(doc_id=doc_id, position=1, start=4, end=8)
        self._index.add_posting(term_id, posting)

        was_removed = self._index.remove_posting(term_id, doc_id, 2)
        assert was_removed == False

        postings = self._index.get_postings_by_term_id(term_id)
        assert len(postings) == 1

        assert postings[0].doc_id   == doc_id
        assert postings[0].position == 1
        assert postings[0].start    == 4
        assert postings[0].end      == 8

    def test_remove_postings_by_document_when_document_is_present(self):
        doc_id    = seed_document(self._conn, 'earth is round')
        term_id_1 = seed_term(self._conn, 'earth')
        term_id_2 = seed_term(self._conn, 'is')
        term_id_3 = seed_term(self._conn, 'round')
        
        posting_1 = self._builder.build(doc_id, 0, 0,  5)
        posting_2 = self._builder.build(doc_id, 1, 6,  8)
        posting_3 = self._builder.build(doc_id, 2, 9, 14)

        self._index.add_posting(term_id_1, posting_1)
        self._index.add_posting(term_id_2, posting_2)
        self._index.add_posting(term_id_3, posting_3)

        was_removed = self._index.remove_postings_by_document(doc_id)
        assert was_removed == True

        postings = self._index.get_postings_by_document_id(doc_id)
        assert len(postings) == 0

    def test_remove_postings_by_document_when_document_is_absent(self):
        doc_id    = seed_document(self._conn, 'earth is round')
        term_id_1 = seed_term(self._conn, 'earth')
        term_id_2 = seed_term(self._conn, 'is')
        term_id_3 = seed_term(self._conn, 'round')
        
        posting_1 = self._builder.build(doc_id, 0, 0,  5)
        posting_2 = self._builder.build(doc_id, 1, 6,  8)
        posting_3 = self._builder.build(doc_id, 2, 9, 14)

        self._index.add_posting(term_id_1, posting_1)
        self._index.add_posting(term_id_2, posting_2)
        self._index.add_posting(term_id_3, posting_3)

        absent_doc_id = doc_id + 1
        was_removed = self._index.remove_postings_by_document(absent_doc_id)
        assert was_removed == False

    def test_contains_posting_when_posting_is_present(self):
        term_id = seed_term(self._conn, 'dog')
        doc_id  = seed_document(self._conn, 'The dog barks.')
        posting = self._builder.build(doc_id, 1, 4, 7)
        self._index.add_posting(term_id, posting)

        assert self._index.contains_posting(term_id, doc_id, 1) == True

    def test_contains_posting_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'dog')
        doc_id  = seed_document(self._conn, 'The dog barks.')
        posting = self._builder.build(doc_id, 1, 4, 7)
        self._index.add_posting(term_id, posting)

        absent_term_id = term_id + 1
        assert self._index.contains_posting(absent_term_id, doc_id, 5) == False

    def test_contains_posting_when_document_is_absent(self):
        term_id = seed_term(self._conn, 'dog')
        doc_id  = seed_document(self._conn, 'The dog barks.')
        posting = self._builder.build(doc_id, 1, 4, 7)
        self._index.add_posting(term_id, posting)

        absent_doc_id = doc_id + 1
        assert self._index.contains_posting(term_id, absent_doc_id, 1) == False

    def test_contains_posting_when_position_is_absent(self):
        term_id = seed_term(self._conn, 'dog')
        doc_id  = seed_document(self._conn, 'The dog barks.')
        posting = self._builder.build(doc_id, 1, 4, 7)
        self._index.add_posting(term_id, posting)

        assert self._index.contains_posting(term_id, doc_id, 2) == False

    def test_contains_term_when_term_is_present(self):
        term_id = seed_term(self._conn, 'dog')
        doc_id  = seed_document(self._conn, 'The dog barks.')
        posting = self._builder.build(doc_id, 1, 4, 7)
        self._index.add_posting(term_id, posting)

        assert self._index.contains_term(term_id) == True

    def test_contains_term_when_term_is_absent(self):
        term_id = seed_term(self._conn, 'dog')
        doc_id  = seed_document(self._conn, 'The dog barks.')
        posting = self._builder.build(doc_id, 1, 4, 7)
        self._index.add_posting(term_id, posting)

        absent_term_id = term_id + 1
        assert self._index.contains_term(absent_term_id) == False

    def test_get_term_counts_by_document_when_document_is_present(self):
        doc_id    = seed_document(self._conn, 'To be or not to be.')
        term_id_1 = seed_term(self._conn, 'to')
        term_id_2 = seed_term(self._conn, 'be')
        term_id_3 = seed_term(self._conn, 'or')
        term_id_4 = seed_term(self._conn, 'not')
        
        posting_1 = self._builder.build(doc_id, 0,  0,  2)
        posting_2 = self._builder.build(doc_id, 1,  3,  5)
        posting_3 = self._builder.build(doc_id, 2,  6,  8)
        posting_4 = self._builder.build(doc_id, 3,  9, 12)
        posting_5 = self._builder.build(doc_id, 4, 13, 15)
        posting_6 = self._builder.build(doc_id, 5, 16, 18)

        self._index.add_posting(term_id_1, posting_1)
        self._index.add_posting(term_id_2, posting_2)
        self._index.add_posting(term_id_3, posting_3)
        self._index.add_posting(term_id_4, posting_4)
        self._index.add_posting(term_id_1, posting_5)
        self._index.add_posting(term_id_2, posting_6)

        counts = self._index.get_term_counts_by_document(doc_id)
        assert len(counts) == 4

        assert counts[0].term_id == term_id_1
        assert counts[0].count   == 2
        assert counts[1].term_id == term_id_2
        assert counts[1].count   == 2
        assert counts[2].term_id == term_id_3
        assert counts[2].count   == 1
        assert counts[3].term_id == term_id_4
        assert counts[3].count   == 1

    def test_get_term_counts_by_document_when_document_is_absent(self):
        doc_id    = seed_document(self._conn, 'To be or not to be.')

        counts = self._index.get_term_counts_by_document(doc_id)
        assert len(counts) == 0

    def test_get_positions_by_term_id(self):
        doc_id_1 = seed_document(self._conn, 'I like you like you like me.')
        doc_id_2 = seed_document(self._conn, 'You do not talk like that.')
        doc_id_3 = seed_document(self._conn, 'I hate pizza.')
        doc_id_4 = seed_document(self._conn, 'What do you like?')

        term_id_1 = seed_term(self._conn, 'like')
        term_id_2 = seed_term(self._conn, 'you')
        term_id_3 = seed_term(self._conn, 'hate')

        posting_01 = self._builder.build(doc_id_1, 1,  2,  6)
        posting_02 = self._builder.build(doc_id_1, 2,  7, 10)
        posting_03 = self._builder.build(doc_id_1, 3, 11, 15)
        posting_04 = self._builder.build(doc_id_1, 4, 16, 19)
        posting_05 = self._builder.build(doc_id_1, 5, 20, 24)
        posting_06 = self._builder.build(doc_id_2, 0,  0,  3)
        posting_07 = self._builder.build(doc_id_2, 3, 16, 20)
        posting_08 = self._builder.build(doc_id_3, 1,  2,  6)
        posting_09 = self._builder.build(doc_id_4, 0,  8, 11)
        posting_10 = self._builder.build(doc_id_4, 3, 12, 16)

        self._index.add_posting(term_id_1, posting_01)
        self._index.add_posting(term_id_2, posting_02)
        self._index.add_posting(term_id_1, posting_03)
        self._index.add_posting(term_id_2, posting_04)
        self._index.add_posting(term_id_1, posting_05)
        self._index.add_posting(term_id_2, posting_06)
        self._index.add_posting(term_id_1, posting_07)
        self._index.add_posting(term_id_3, posting_08)
        self._index.add_posting(term_id_2, posting_09)
        self._index.add_posting(term_id_1, posting_10)

        positions = self._index.get_positions_by_term_id(term_id_1)

        assert positions.keys() == {doc_id_1, doc_id_2, doc_id_4}
        assert positions[doc_id_1] == [TermPosition(term_id_1, 1),
                                       TermPosition(term_id_1, 3),
                                       TermPosition(term_id_1, 5)]
        assert positions[doc_id_2] == [TermPosition(term_id_1, 3)]
        assert positions[doc_id_4] == [TermPosition(term_id_1, 3)]

    def test_get_positions_by_term_ids_when_term_ids_is_not_empty(self):
        doc_id_1 = seed_document(self._conn, 'Water is blue.')
        doc_id_2 = seed_document(self._conn, 'I hate Mondays.')
        doc_id_3 = seed_document(self._conn, 'No pain, no gain.')
        doc_id_4 = seed_document(self._conn, 'My favorite color is green.')

        term_id_1 = seed_term(self._conn, 'water')
        term_id_2 = seed_term(self._conn, 'blue')
        term_id_3 = seed_term(self._conn, 'hate')
        term_id_4 = seed_term(self._conn, 'mondays')
        term_id_5 = seed_term(self._conn, 'pain')
        term_id_6 = seed_term(self._conn, 'gain')
        term_id_7 = seed_term(self._conn, 'color')

        posting_1 = self._builder.build(doc_id_1, 0,  0,  5)
        posting_2 = self._builder.build(doc_id_1, 2,  9, 13)
        posting_3 = self._builder.build(doc_id_2, 1,  2,  6)
        posting_4 = self._builder.build(doc_id_2, 2,  7, 14)
        posting_5 = self._builder.build(doc_id_3, 1,  3,  7)
        posting_6 = self._builder.build(doc_id_3, 3, 12, 16)
        posting_7 = self._builder.build(doc_id_4, 2, 12, 17)

        self._index.add_posting(term_id_1, posting_1)
        self._index.add_posting(term_id_2, posting_2)
        self._index.add_posting(term_id_3, posting_3)
        self._index.add_posting(term_id_4, posting_4)
        self._index.add_posting(term_id_5, posting_5)
        self._index.add_posting(term_id_6, posting_6)
        self._index.add_posting(term_id_7, posting_7)

        term_ids  = [term_id_1, term_id_2, term_id_4, term_id_5]
        positions = self._index.get_positions_by_term_ids(term_ids)

        assert positions.keys() == {doc_id_1, doc_id_2, doc_id_3}
        assert positions[doc_id_1] == [TermPosition(term_id_1, 0),
                                       TermPosition(term_id_2, 2)]
        assert positions[doc_id_2] == [TermPosition(term_id_4, 2)]
        assert positions[doc_id_3] == [TermPosition(term_id_5, 1)]

    def test_get_positions_by_term_ids_when_term_ids_is_empty(self):
        doc_id_1 = seed_document(self._conn, 'Water is blue.')
        doc_id_2 = seed_document(self._conn, 'I hate Mondays.')

        term_id_1 = seed_term(self._conn, 'water')
        term_id_2 = seed_term(self._conn, 'blue')
        term_id_3 = seed_term(self._conn, 'hate')
        term_id_4 = seed_term(self._conn, 'mondays')

        posting_1 = self._builder.build(doc_id_1, 0,  0,  5)
        posting_2 = self._builder.build(doc_id_1, 2,  9, 13)
        posting_3 = self._builder.build(doc_id_2, 1,  2,  6)
        posting_4 = self._builder.build(doc_id_2, 2,  7, 14)

        self._index.add_posting(term_id_1, posting_1)
        self._index.add_posting(term_id_2, posting_2)
        self._index.add_posting(term_id_3, posting_3)
        self._index.add_posting(term_id_4, posting_4)

        term_ids  = []
        positions = self._index.get_positions_by_term_ids(term_ids)
        assert len(positions) == 0

    def test_get_posting_by_document_id(self):
        doc_id_1 = seed_document(self._conn, 'apples are red.')
        doc_id_2 = seed_document(self._conn, 'red is a color.')

        term_id_1 = seed_term(self._conn, 'apples')
        term_id_2 = seed_term(self._conn, 'red')
        term_id_3 = seed_term(self._conn, 'color')

        posting_1 = self._builder.build(doc_id_1, 0,  0,  6)
        posting_2 = self._builder.build(doc_id_1, 2, 11, 14)
        posting_3 = self._builder.build(doc_id_2, 0,  0,  3)
        posting_4 = self._builder.build(doc_id_2, 2,  9, 14)

        self._index.add_posting(term_id_1, posting_1)
        self._index.add_posting(term_id_2, posting_2)
        self._index.add_posting(term_id_2, posting_3)
        self._index.add_posting(term_id_3, posting_4)

        postings = self._index.get_postings_by_document_id(doc_id_1)
        assert len(postings) == 2

        assert postings[0].term_id == term_id_1
        assert postings[0].posting == posting_1
        assert postings[1].term_id == term_id_2
        assert postings[1].posting == posting_2
    
    def test_get_document_ids_by_term_id_when_term_id_is_present(self):
        doc_id_1 = seed_document(self._conn, 'The cat is fast.')
        doc_id_2 = seed_document(self._conn, 'The sky is blue.')
        doc_id_3 = seed_document(self._conn, 'Where is the cat?')

        term_id_1 = seed_term(self._conn, 'cat')
        term_id_2 = seed_term(self._conn, 'sky')

        posting_1 = self._builder.build(doc_id_1, 1,  4,  7)
        posting_2 = self._builder.build(doc_id_2, 1,  4,  7)
        posting_3 = self._builder.build(doc_id_3, 3, 13, 16)

        self._index.add_posting(term_id_1, posting_1)
        self._index.add_posting(term_id_2, posting_2)
        self._index.add_posting(term_id_1, posting_3)

        doc_ids = self._index.get_document_ids_by_term_id(term_id_1)

        assert doc_ids == {doc_id_1, doc_id_3}
    
    def test_get_document_ids_by_term_id_when_term_id_is_absent(self):
        doc_id_1 = seed_document(self._conn, 'The cat is fast.')
        doc_id_2 = seed_document(self._conn, 'The sky is blue.')
        doc_id_3 = seed_document(self._conn, 'Where is the cat?')

        term_id_1 = seed_term(self._conn, 'cat')
        term_id_2 = seed_term(self._conn, 'sky')
        term_id_3 = seed_term(self._conn, 'doc')

        posting_1 = self._builder.build(doc_id_1, 1,  4,  7)
        posting_2 = self._builder.build(doc_id_2, 1,  4,  7)
        posting_3 = self._builder.build(doc_id_3, 3, 13, 16)

        self._index.add_posting(term_id_1, posting_1)
        self._index.add_posting(term_id_2, posting_2)
        self._index.add_posting(term_id_1, posting_3)

        doc_ids = self._index.get_document_ids_by_term_id(term_id_3)

        assert doc_ids == set()

    def test_get_document_ids_by_term_ids_when_term_ids_is_empty(self):
        doc_id_1 = seed_document(self._conn, 'It is raining a lot.')
        doc_id_2 = seed_document(self._conn, 'The sky is blue.')
        doc_id_3 = seed_document(self._conn, 'Where are you from?')

        term_id_1 = seed_term(self._conn, 'raining')
        term_id_2 = seed_term(self._conn, 'sky')
        term_id_3 = seed_term(self._conn, 'where')

        posting_1 = self._builder.build(doc_id_1, 2, 6, 13)
        posting_2 = self._builder.build(doc_id_2, 1, 4,  7)
        posting_3 = self._builder.build(doc_id_3, 0, 0,  5)

        self._index.add_posting(term_id_1, posting_1)
        self._index.add_posting(term_id_2, posting_2)
        self._index.add_posting(term_id_3, posting_3)

        term_ids = []
        doc_ids  = self._index.get_document_ids_by_term_ids(term_ids)

        assert doc_ids == set()
    
    def test_get_document_ids_by_term_ids_when_term_ids_is_not_empty(self):
        doc_id_1 = seed_document(self._conn, 'It is raining a lot.')
        doc_id_2 = seed_document(self._conn, 'The sky is blue.')
        doc_id_3 = seed_document(self._conn, 'Where are you from?')

        term_id_1 = seed_term(self._conn, 'raining')
        term_id_2 = seed_term(self._conn, 'sky')
        term_id_3 = seed_term(self._conn, 'where')

        posting_1 = self._builder.build(doc_id_1, 2, 6, 13)
        posting_2 = self._builder.build(doc_id_2, 1, 4,  7)
        posting_3 = self._builder.build(doc_id_3, 0, 0,  5)

        self._index.add_posting(term_id_1, posting_1)
        self._index.add_posting(term_id_2, posting_2)
        self._index.add_posting(term_id_3, posting_3)

        term_ids = [term_id_1, term_id_2, term_id_3]
        doc_ids  = self._index.get_document_ids_by_term_ids(term_ids)

        assert doc_ids == {doc_id_1, doc_id_2, doc_id_3}

    def test_get_position_by_document(self):
        doc_id_1 = seed_document(self._conn, 'her hair is blue')
        doc_id_2 = seed_document(self._conn, 'Are your eyes blue?')

        term_id_1 = seed_term(self._conn, 'her')
        term_id_2 = seed_term(self._conn, 'hair')
        term_id_3 = seed_term(self._conn, 'is')
        term_id_4 = seed_term(self._conn, 'blue')
        term_id_5 = seed_term(self._conn, 'are')
        term_id_6 = seed_term(self._conn, 'your')
        term_id_7 = seed_term(self._conn, 'eyes')

        posting_1 = self._builder.build(doc_id_1, 0,  0,  3)
        posting_2 = self._builder.build(doc_id_1, 1,  4,  8)
        posting_3 = self._builder.build(doc_id_1, 2,  9, 11)
        posting_4 = self._builder.build(doc_id_1, 3, 12, 16)
        posting_5 = self._builder.build(doc_id_2, 0,  0,  3)
        posting_6 = self._builder.build(doc_id_2, 1,  4,  8)
        posting_7 = self._builder.build(doc_id_2, 2,  9, 13)
        posting_8 = self._builder.build(doc_id_2, 3, 14, 18)

        self._index.add_posting(term_id_1, posting_1)
        self._index.add_posting(term_id_2, posting_2)
        self._index.add_posting(term_id_3, posting_3)
        self._index.add_posting(term_id_4, posting_4)
        self._index.add_posting(term_id_5, posting_5)
        self._index.add_posting(term_id_6, posting_6)
        self._index.add_posting(term_id_7, posting_7)
        self._index.add_posting(term_id_4, posting_8)

        positions = self._index.get_positions_by_document_id(doc_id_1)
        assert len(positions) == 4

        assert positions[0] == TermPosition(term_id_1, 0)
        assert positions[1] == TermPosition(term_id_2, 1)
        assert positions[2] == TermPosition(term_id_3, 2)
        assert positions[3] == TermPosition(term_id_4, 3)
