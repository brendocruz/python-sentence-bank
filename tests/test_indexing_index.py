from sentencebank.indexing.index import InvertedIndex, Posting


class TestInvertedIndex:

    def test_count_zero(self):
        postings = {}
        index    = InvertedIndex(postings)

        assert index.term_count() == 0

    def test_count_non_zero(self):
        postings = {3: [[10, 2, 5, 7]], 5: [[21, 4, 3, 7]], 12: [[5, 1, 12, 15]]}
        index = InvertedIndex(postings)

        assert index.term_count() == 3

    def test_clear(self):
        postings = {3: [[10, 2, 5, 7]], 5: [[21, 4, 3, 7]], 12: [[5, 1, 12, 15]]}
        index    = InvertedIndex(postings)

        index.clear()
        assert index.term_count() == 0

    def test_get_posting_present(self):
        postings = {12: [[10, 2, 5, 7], [13, 5, 10, 13]]}
        index    = InvertedIndex(postings)

        result = index.get_posting(12, 10, 2)
        assert result          is not None
        assert result.doc_id   == 10
        assert result.position == 2
        assert result.start    == 5
        assert result.end      == 7

    def test_get_posting_absent_term(self):
        postings = {5: [[21, 4, 3, 7]]}
        index    = InvertedIndex(postings)

        assert index.get_posting(3, 2, 1) == None

    def test_get_posting_absent_document(self):
        postings = {5: [[21, 4, 3, 7], [34, 2, 5, 9]]}
        index    = InvertedIndex(postings)

        assert index.get_posting(5, 7, 1) == None

    def test_get_posting_absent_position(self):
        postings = {5: [[21, 4, 3, 7], [34, 2, 5, 9]]}
        index    = InvertedIndex(postings)

        assert index.get_posting(5, 21, 1) == None

    def test_get_postings_present(self):
        postings = {5: [[21, 4, 3, 7]], 12: [[10, 2, 5, 7], [13, 5, 10, 13]]}
        index    = InvertedIndex(postings)

        results = index.get_postings(12)
        assert len(results) == 2

        assert results[0].doc_id   == 10
        assert results[0].position == 2
        assert results[0].start    == 5
        assert results[0].end      == 7

        assert results[1].doc_id   == 13
        assert results[1].position == 5
        assert results[1].start    == 10
        assert results[1].end      == 13

    def test_get_postings_absent(self):
        postings = {5: [[21, 4, 3, 7]], 12: [[10, 2, 5, 7], [13, 5, 10, 13]]}
        index    = InvertedIndex(postings)

        results = index.get_postings(7)
        assert len(results) == 0

    def test_remove_posting_present_retains_term(self):
        postings = {12: [[10, 2, 5, 7], [13, 5, 10, 13]]}
        index    = InvertedIndex(postings)

        index.remove_posting(12, 10, 2)
        assert len(postings) == 1

        results = index.get_postings(12)
        assert results[0].doc_id   == 13
        assert results[0].position == 5
        assert results[0].start    == 10
        assert results[0].end      == 13

    def test_remove_posting_present_cleans_term(self):
        postings = {12: [[13, 5, 10, 13]]}
        index    = InvertedIndex(postings)

        index.remove_posting(12, 10, 2)
        assert len(postings) == 0

    def test_remove_posting_absent_term(self):
        postings = {5: [[21, 4, 3, 7]]}
        index    = InvertedIndex(postings)

        index.remove_posting(3, 2, 1)
        assert len(postings) == 1

        results = index.get_postings(5)
        assert results[0].doc_id   == 21
        assert results[0].position == 4
        assert results[0].start    == 3
        assert results[0].end      == 7

    def test_remove_posting_absent_document(self):
        postings = {5: [[21, 4, 3, 7], [34, 2, 5, 9]]}
        index    = InvertedIndex(postings)

        index.remove_posting(5, 7, 1)
        assert len(postings) == 1

        results = index.get_postings(5)
        assert results[0].doc_id   == 21
        assert results[0].position == 4
        assert results[0].start    == 3
        assert results[0].end      == 7

        assert results[1].doc_id   == 34
        assert results[1].position == 2
        assert results[1].start    == 5
        assert results[1].end      == 9

    def test_remove_posting_absent_position(self):
        postings = {5: [[21, 4, 3, 7], [34, 2, 5, 9]]}
        index    = InvertedIndex(postings)

        index.remove_posting(5, 21, 1)
        assert len(postings) == 1

        results = index.get_postings(5)
        assert results[0].doc_id   == 21
        assert results[0].position == 4
        assert results[0].start    == 3
        assert results[0].end      == 7

        assert results[1].doc_id   == 34
        assert results[1].position == 2
        assert results[1].start    == 5
        assert results[1].end      == 9

    def test_add_posting_present_duplicate(self):
        postings = {4: [[24, 1, 0, 5], [31, 4, 10, 15]]}
        index    = InvertedIndex(postings)

        posting = Posting(31, 4, 10, 15)
        index.add_posting(4, posting)
        assert index.term_count() == 1

        results = index.get_postings(4)
        assert results[0].doc_id   == 24
        assert results[0].position == 1
        assert results[0].start    == 0
        assert results[0].end      == 5

        assert results[1].doc_id   == 31
        assert results[1].position == 4
        assert results[1].start    == 10
        assert results[1].end      == 15

    def test_add_posting_absent(self):
        postings = {4: [[24, 1, 0, 5], [31, 4, 10, 15]]}
        index    = InvertedIndex(postings)

        posting = Posting(35, 1, 0, 5)
        index.add_posting(7, posting)
        assert index.term_count() == 2

        results = index.get_postings(7)
        assert results[0].doc_id   == 35
        assert results[0].position == 1
        assert results[0].start    == 0
        assert results[0].end      == 5

        results = index.get_postings(4)
        assert results[0].doc_id   == 24
        assert results[0].position == 1
        assert results[0].start    == 0
        assert results[0].end      == 5

        assert results[1].doc_id   == 31
        assert results[1].position == 4
        assert results[1].start    == 10
        assert results[1].end      == 15

    def test_contains_posting_present(self):
        postings = {12: [[10, 2, 5, 7], [13, 5, 10, 13]]}
        index    = InvertedIndex(postings)

        assert index.contains_posting(12, 10, 2) == True

    def test_contains_posting_absent_term(self):
        postings = {5: [[21, 4, 3, 7]]}
        index    = InvertedIndex(postings)

        assert index.contains_posting(3, 2, 1) == False

    def test_contains_posting_absent_document(self):
        postings = {5: [[21, 4, 3, 7], [34, 2, 5, 9]]}
        index    = InvertedIndex(postings)

        assert index.contains_posting(5, 7, 1) == False

    def test_contains_posting_absent_position(self):
        postings = {5: [[21, 4, 3, 7], [34, 2, 5, 9]]}
        index    = InvertedIndex(postings)

        assert index.contains_posting(5, 21, 1) == False

    def test_contains_term_present(self):
        postings = {5: [[21, 4, 3, 7]]}
        index    = InvertedIndex(postings)

        assert index.contains_term(5) == True

    def test_contains_term_absent(self):
        postings = {5: [[21, 4, 3, 7]]}
        index    = InvertedIndex(postings)

        assert index.contains_term(7) == False
