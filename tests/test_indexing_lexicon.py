from sentencebank.indexing.lexicon import Lexicon


class TestLexicon:

    def test_contains_true(self):
        lexicon = Lexicon()
        lexicon.set_entry('hello', 1, 1)

        assert lexicon.contains('hello') == True

    def test_contains_false(self):
        lexicon = Lexicon()
        lexicon.set_entry('hello', 1, 1)

        assert lexicon.contains('world') == False

    def test_get_term_present_id(self):
        lexicon = Lexicon()
        term_id = lexicon.set_entry('language', 6, 7)

        assert lexicon.get_term(term_id) == 'language'

    def test_get_term_absent_id(self):
        lexicon = Lexicon()
        term_id = lexicon.set_entry('language', 6, 7)

        absent_term_id = term_id + 1
        assert lexicon.get_term(absent_term_id) is None

    def test_get_term_id_present_term(self):
        lexicon = Lexicon()
        term_id = lexicon.set_entry('language', 6, 7)

        assert lexicon.get_term_id('language') == term_id

    def test_get_term_id_absent_term(self):
        lexicon = Lexicon()
        lexicon.set_entry('language', 6, 7)

        assert lexicon.get_term_id('learning') is None

    def test_get_doc_freq_absent_term(self):
        lexicon = Lexicon()
        lexicon.set_entry('language', 6, 7)

        assert lexicon.get_doc_freq('language') == 6

    def test_get_doc_freq_present_term(self):
        lexicon = Lexicon()
        lexicon.set_entry('language', 6, 7)

        assert lexicon.get_doc_freq('learning') == 0

    def test_get_col_freq_absent_term(self):
        lexicon = Lexicon()
        lexicon.set_entry('language', 6, 7)

        assert lexicon.get_col_freq('language') == 7

    def test_get_col_freq_present_term(self):
        lexicon = Lexicon()
        lexicon.set_entry('language', 6, 7)

        assert lexicon.get_col_freq('learning') == 0

    def test_get_terms(self):
        lexicon = Lexicon()
        lexicon.set_entry('cat',  6, 7)
        lexicon.set_entry('dog',  1, 1)
        lexicon.set_entry('bird', 1, 3)

        terms = lexicon.get_terms()

        assert len(terms) == 3
        assert 'cat'  in terms
        assert 'dog'  in terms
        assert 'bird' in terms

    def test_size_empty(self):
        lexicon = Lexicon()

        assert lexicon.size() == 0

    def test_size_non_empty(self):
        lexicon = Lexicon()
        lexicon.set_entry('hello', 1, 1)
        lexicon.set_entry('word',  1, 2)

        assert lexicon.size() == 2

    def test_clear(self):
        lexicon = Lexicon()
        lexicon.set_entry('cat',  6, 7)
        lexicon.set_entry('dog',  1, 1)
        lexicon.set_entry('bird', 1, 3)

        lexicon.clear()
        
        assert lexicon.size()                 == 0
        assert lexicon.set_entry('cat', 1, 1) == 1

    def test_set_entry_absent_term(self):
        lexicon = Lexicon()

        assert lexicon.set_entry('dog', 1, 3) == 1

        assert lexicon.contains('dog')        == True
        assert lexicon.get_term(1)            == 'dog'
        assert lexicon.get_term_id('dog')     == 1
        assert lexicon.get_doc_freq('dog')    == 1
        assert lexicon.get_col_freq('dog')    == 3

    def test_set_entry_present_term(self):
        lexicon = Lexicon()

        assert lexicon.set_entry('cat', 20, 26) == 1
        assert lexicon.set_entry('cat', 32, 40) == 1

        assert lexicon.contains('cat')     == True
        assert lexicon.get_term(1)         == 'cat'
        assert lexicon.get_doc_freq('cat') == 32
        assert lexicon.get_col_freq('cat') == 40

    def test_increment_doc_freq_present_term(self):
        lexicon = Lexicon()
        lexicon.set_entry('bird', 2, 6)

        lexicon.increment_doc_freq('bird')

        assert lexicon.get_doc_freq('bird') == 3

    def test_increment_doc_freq_absent_term(self):
        lexicon = Lexicon()
        lexicon.set_entry('bird', 2, 6)

        lexicon.increment_doc_freq('home')

        assert lexicon.get_doc_freq('home') == 1

    def test_decrement_doc_freq_present_term_and_greater_than_zero(self):
        lexicon = Lexicon()
        lexicon.set_entry('bird', 2, 6)

        lexicon.decrement_doc_freq('bird')

        assert lexicon.get_doc_freq('bird') == 1

    def test_decrement_doc_freq_present_term_and_equal_zero(self):
        lexicon = Lexicon()
        lexicon.set_entry('bird', 0, 0)

        lexicon.decrement_doc_freq('bird')

        assert lexicon.get_doc_freq('bird') == 0

    def test_decrement_doc_freq_absent_term(self):
        lexicon = Lexicon()
        lexicon.set_entry('bird', 2, 6)

        lexicon.decrement_doc_freq('home')

        assert lexicon.get_doc_freq('home') == 0

    def test_increment_col_freq_present_term(self):
        lexicon = Lexicon()
        lexicon.set_entry('horse', 3, 5)

        lexicon.increment_col_freq('horse')

        assert lexicon.get_col_freq('horse') == 6

    def test_increment_col_freq_absent_term(self):
        lexicon = Lexicon()
        lexicon.set_entry('horse', 3, 5)

        lexicon.increment_col_freq('chair')

        assert lexicon.get_col_freq('chair') == 1

    def test_decrement_col_freq_present_term_and_greater_than_zero(self):
        lexicon = Lexicon()
        lexicon.set_entry('horse', 3, 5)

        lexicon.decrement_col_freq('horse')

        assert lexicon.get_col_freq('horse') == 4

    def test_decrement_col_freq_present_term_and_equal_zero(self):
        lexicon = Lexicon()
        lexicon.set_entry('horse', 0, 0)

        lexicon.decrement_col_freq('horse')

        assert lexicon.get_col_freq('horse') == 0

    def test_decrement_col_freq_absent_term(self):
        lexicon = Lexicon()
        lexicon.set_entry('horse', 3, 5)

        lexicon.decrement_col_freq('chair')

        assert lexicon.get_col_freq('chair') == 0
