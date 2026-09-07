from sentencebank.indexing.lexicon import Lexicon


class TestLexicon:

    def test_contains_true(self):
        entries = { 'hello': [1, 1] }
        lexicon = Lexicon(entries)
        assert lexicon.contains('hello') == True

    def test_contains_false(self):
        entries = { 'hello': [1, 1] }
        lexicon = Lexicon(entries)
        assert lexicon.contains('world') == False

    def test_get_doc_freq_absent_term(self):
        entries = { 'language': [6, 7] }
        lexicon = Lexicon(entries)
        assert lexicon.get_doc_freq('language') == 6

    def test_get_doc_freq_present_term(self):
        entries = { 'language': [6, 7] }
        lexicon = Lexicon(entries)
        assert lexicon.get_doc_freq('learning') == 0

    def test_get_col_freq_absent_term(self):
        entries = { 'language': [6, 7] }
        lexicon = Lexicon(entries)
        assert lexicon.get_col_freq('language') == 7

    def test_get_col_freq_present_term(self):
        entries = { 'language': [6, 7] }
        lexicon = Lexicon(entries)
        assert lexicon.get_col_freq('learning') == 0

    def test_get_terms(self):
        entries = { 'cat': [6, 7], 'dog': [1, 1], 'bird': [1, 3] }
        lexicon = Lexicon(entries)

        terms = lexicon.get_terms()
        assert len(terms) == 3
        assert 'cat'  in terms
        assert 'dog'  in terms
        assert 'bird' in terms

    def test_size_empty(self):
        lexicon = Lexicon()
        assert lexicon.size() == 0

    def test_size_non_empty(self):
        entries = { 'hello': [1, 1], 'word': [1, 2] }
        lexicon = Lexicon(entries)
        assert lexicon.size() == 2

    def test_clear(self):
        entries = { 'cat': [6, 7], 'dog': [1, 1], 'bird': [1, 3] }
        lexicon = Lexicon(entries)

        assert lexicon.size() == 3
        lexicon.clear()
        assert lexicon.size() == 0

    def test_set_entry_present_term(self):
        entries = { 'cat': [20, 26] }
        lexicon = Lexicon(entries)

        lexicon.set_entry('cat', 20, 26)
        assert lexicon.contains('cat')     == True
        assert lexicon.get_doc_freq('cat') == 20
        assert lexicon.get_col_freq('cat') == 26

    def test_set_entry_absent_term(self):
        entries = { 'cat': [20, 26] }
        lexicon = Lexicon(entries)

        lexicon.set_entry('dog', 1, 3)
        assert lexicon.contains('dog')     == True
        assert lexicon.get_doc_freq('dog') == 1
        assert lexicon.get_col_freq('dog') == 3

    def test_increment_doc_freq_present_term(self):
        entries = { 'bird': [2, 6] }
        lexicon = Lexicon(entries)

        assert lexicon.get_doc_freq('bird') == 2
        lexicon.increment_doc_freq('bird')
        assert lexicon.get_doc_freq('bird') == 3

    def test_increment_doc_freq_absent_term(self):
        entries = { 'bird': [2, 6] }
        lexicon = Lexicon(entries)

        assert lexicon.get_doc_freq('home') == 0
        lexicon.increment_doc_freq('home')
        assert lexicon.get_doc_freq('home') == 1

    def test_decrement_doc_freq_present_term_and_greater_than_zero(self):
        entries = { 'bird': [2, 6] }
        lexicon = Lexicon(entries)

        assert lexicon.get_doc_freq('bird') == 2
        lexicon.decrement_doc_freq('bird')
        assert lexicon.get_doc_freq('bird') == 1

    def test_decrement_doc_freq_present_term_and_equal_zero(self):
        entries = { 'bird': [0, 0] }
        lexicon = Lexicon(entries)

        assert lexicon.get_doc_freq('bird') == 0
        lexicon.decrement_doc_freq('bird')
        assert lexicon.get_doc_freq('bird') == 0

    def test_decrement_doc_freq_absent_term(self):
        entries = { 'bird': [2, 6] }
        lexicon = Lexicon(entries)

        assert lexicon.get_doc_freq('home') == 0
        lexicon.decrement_doc_freq('home')
        assert lexicon.get_doc_freq('home') == 0

    def test_increment_col_freq_present_term(self):
        entries = { 'horse': [3, 5] }
        lexicon = Lexicon(entries)

        assert lexicon.get_col_freq('horse') == 5
        lexicon.increment_col_freq('horse')
        assert lexicon.get_col_freq('horse') == 6

    def test_increment_col_freq_absent_term(self):
        entries = { 'horse': [3, 5] }
        lexicon = Lexicon(entries)

        assert lexicon.get_col_freq('chair') == 0
        lexicon.increment_col_freq('chair')
        assert lexicon.get_col_freq('chair') == 1

    def test_decrement_col_freq_present_term_and_greater_than_zero(self):
        entries = { 'horse': [3, 5] }
        lexicon = Lexicon(entries)

        assert lexicon.get_col_freq('horse') == 5
        lexicon.decrement_col_freq('horse')
        assert lexicon.get_col_freq('horse') == 4

    def test_decrement_col_freq_present_term_and_equal_zero(self):
        entries = { 'horse': [0, 0] }
        lexicon = Lexicon(entries)

        assert lexicon.get_col_freq('horse') == 0
        lexicon.decrement_col_freq('horse')
        assert lexicon.get_col_freq('horse') == 0

    def test_decrement_col_freq_absent_term(self):
        entries = { 'horse': [3, 5] }
        lexicon = Lexicon(entries)

        assert lexicon.get_col_freq('chair') == 0
        lexicon.decrement_col_freq('chair')
        assert lexicon.get_col_freq('chair') == 0
