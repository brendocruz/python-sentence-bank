from sentencebank.indexing.index import InvertedIndex, Posting


class TestInvertedIndex:

    def test_count_zero(self):
        index = InvertedIndex()

        assert index.term_count() == 0

    def test_count_non_zero(self):
        index = InvertedIndex()
        index.add_posting(3,  Posting(10, 2, 5, 7))
        index.add_posting(5,  Posting(21, 4, 3, 7))
        index.add_posting(12, Posting(5, 1, 12, 15))

        assert index.term_count() == 3

    def test_clear(self):
        index = InvertedIndex()
        index.add_posting(3,  Posting(10, 2, 5, 7))
        index.add_posting(5,  Posting(21, 4, 3, 7))
        index.add_posting(12, Posting(5, 1, 12, 15))

        index.clear()
        assert index.term_count() == 0

    def test_get_posting_present_term(self):
        index = InvertedIndex()
        index.add_posting(12, Posting(10, 2, 5,  7))
        index.add_posting(12, Posting(13, 5, 10, 13))

        posting = index.get_posting(12, 10, 2)

        assert posting          is not None
        assert posting.doc_id   == 10
        assert posting.position == 2
        assert posting.start    == 5
        assert posting.end      == 7

    def test_get_posting_absent_term(self):
        index = InvertedIndex()
        index.add_posting(5, Posting(21, 4, 3, 7))

        assert index.get_posting(3, 2, 1) == None

    def test_get_posting_absent_document(self):
        index = InvertedIndex()
        index.add_posting(5, Posting(21, 4, 3, 7))
        index.add_posting(5, Posting(34, 2, 5, 9))

        assert index.get_posting(5, 7, 1) == None

    def test_get_posting_absent_position(self):
        index = InvertedIndex()
        index.add_posting(5, Posting(21, 4, 3, 7))
        index.add_posting(5, Posting(34, 2, 5, 9))

        assert index.get_posting(5, 21, 1) == None

    def test_get_postings_present_term(self):
        index = InvertedIndex()
        index.add_posting(5,  Posting(21, 4, 3,  7))
        index.add_posting(12, Posting(10, 2, 5,  7))
        index.add_posting(12, Posting(13, 5, 10, 13))

        postings = index.get_postings(12)
        assert len(postings) == 2

        assert postings[0].doc_id   == 10
        assert postings[0].position == 2
        assert postings[0].start    == 5
        assert postings[0].end      == 7

        assert postings[1].doc_id   == 13
        assert postings[1].position == 5
        assert postings[1].start    == 10
        assert postings[1].end      == 13

    def test_get_postings_absent_term(self):
        index = InvertedIndex()
        index.add_posting(5,  Posting(21, 4, 3,  7))
        index.add_posting(12, Posting(10, 2, 5,  7))
        index.add_posting(12, Posting(13, 5, 10, 13))

        postings = index.get_postings(7)

        assert len(postings) == 0

    def test_remove_posting_present_posting_retains_term(self):
        index = InvertedIndex()
        index.add_posting(12, Posting(10, 2, 5,  7))
        index.add_posting(12, Posting(13, 5, 10, 13))

        index.remove_posting(12, 10, 2)

        postings = index.get_postings(12)
        assert len(postings)        == 1

        assert postings[0].doc_id   == 13
        assert postings[0].position == 5
        assert postings[0].start    == 10
        assert postings[0].end      == 13

    def test_remove_posting_present_posting_cleans_term(self):
        index = InvertedIndex()
        index.add_posting(12, Posting(13, 5, 10, 13))

        index.remove_posting(12, 13, 5)

        postings = index.get_postings(12)
        assert len(postings) == 0

    def test_remove_posting_absent_term(self):
        index = InvertedIndex()
        index.add_posting(5, Posting(21, 4, 3, 7))

        index.remove_posting(3, 2, 1)

        postings = index.get_postings(5)
        assert len(postings)        == 1

        assert postings[0].doc_id   == 21
        assert postings[0].position == 4
        assert postings[0].start    == 3
        assert postings[0].end      == 7

    def test_remove_posting_absent_document(self):
        index = InvertedIndex()
        index.add_posting(5, Posting(21, 4, 3, 7))
        index.add_posting(5, Posting(34, 2, 5, 9))

        index.remove_posting(5, 7, 1)

        postings = index.get_postings(5)
        assert len(postings) == 2

        assert postings[0].doc_id   == 21
        assert postings[0].position == 4
        assert postings[0].start    == 3
        assert postings[0].end      == 7

        assert postings[1].doc_id   == 34
        assert postings[1].position == 2
        assert postings[1].start    == 5
        assert postings[1].end      == 9

    def test_remove_posting_absent_position(self):
        index = InvertedIndex()
        index.add_posting(5, Posting(21, 4, 3, 7))
        index.add_posting(5, Posting(34, 2, 5, 9))

        index.remove_posting(5, 21, 1)

        postings = index.get_postings(5)
        assert len(postings)        == 2

        assert postings[0].doc_id   == 21
        assert postings[0].position == 4
        assert postings[0].start    == 3
        assert postings[0].end      == 7

        assert postings[1].doc_id   == 34
        assert postings[1].position == 2
        assert postings[1].start    == 5
        assert postings[1].end      == 9

    def test_add_posting_present_term(self):
        index = InvertedIndex()
        index.add_posting(4, Posting(24, 1, 0, 5))
        index.add_posting(4, Posting(31, 4, 10, 15))

        posting = Posting(31, 4, 10, 15)
        index.add_posting(4, posting)
        assert index.term_count() == 1

        postings = index.get_postings(4)
        assert len(postings)        == 2

        assert postings[0].doc_id   == 24
        assert postings[0].position == 1
        assert postings[0].start    == 0
        assert postings[0].end      == 5

        assert postings[1].doc_id   == 31
        assert postings[1].position == 4
        assert postings[1].start    == 10
        assert postings[1].end      == 15

    def test_add_posting_absent_term(self):
        index = InvertedIndex()
        index.add_posting(4, Posting(24, 1, 0, 5))
        index.add_posting(4, Posting(31, 4, 10, 15))

        index.add_posting(7, Posting(35, 1, 0, 5))
        assert index.term_count() == 2

        postings = index.get_postings(7)
        assert postings[0].doc_id   == 35
        assert postings[0].position == 1
        assert postings[0].start    == 0
        assert postings[0].end      == 5

        postings = index.get_postings(4)
        assert postings[0].doc_id   == 24
        assert postings[0].position == 1
        assert postings[0].start    == 0
        assert postings[0].end      == 5

        assert postings[1].doc_id   == 31
        assert postings[1].position == 4
        assert postings[1].start    == 10
        assert postings[1].end      == 15

    def test_contains_posting_present_posting(self):
        index = InvertedIndex()
        index.add_posting(12, Posting(10, 2, 5, 7))
        index.add_posting(12, Posting(13, 5, 10, 13))

        assert index.contains_posting(12, 10, 2) == True

    def test_contains_posting_absent_term(self):
        index = InvertedIndex()
        index.add_posting(5, Posting(21, 4, 3, 7))

        assert index.contains_posting(3, 2, 1) == False

    def test_contains_posting_absent_document(self):
        index = InvertedIndex()
        index.add_posting(5, Posting(21, 4, 3, 7))
        index.add_posting(5, Posting(34, 2, 5, 9))

        assert index.contains_posting(5, 7, 1) == False

    def test_contains_posting_absent_position(self):
        index = InvertedIndex()
        index.add_posting(5, Posting(21, 4, 3, 7))
        index.add_posting(5, Posting(34, 2, 5, 9))

        assert index.contains_posting(5, 21, 1) == False

    def test_contains_term_present_term(self):
        index = InvertedIndex()
        index.add_posting(5, Posting(21, 4, 3, 7))

        assert index.contains_term(5) == True

    def test_contains_term_absent_term(self):
        index = InvertedIndex()
        index.add_posting(5, Posting(21, 4, 3, 7))

        assert index.contains_term(7) == False
