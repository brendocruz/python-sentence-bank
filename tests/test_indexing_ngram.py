from sentencebank.indexing.ngram import NgramIndex


class TestNgramIndex:

    def test_size_empty(self):
        index = NgramIndex()
        assert index.size() == 0

    def test_size_non_empty(self):
        entries = { '$en': ['end'], 'end': ['end'], 'nd$': ['end'] }
        index   = NgramIndex(entries, order=3)
        assert index.size() == 3

    def test_clear(self):
        entries = { '$do': ['dog'], 'dog': ['dog'], 'og$': ['dog'] }
        index   = NgramIndex(entries, order=3)

        assert index.size() == 3
        index.clear()
        assert index.size() == 0

    def test_generate_ngrams_empty_string(self):
        index = NgramIndex()

        ngrams = index._generate_ngrams('')
        assert len(ngrams) == 0

    def test_generate_ngrams_order_2(self):
        index = NgramIndex(order=2)

        ngrams = index._generate_ngrams('language')
        assert len(ngrams) == 9

        assert ngrams[0] == '$l'
        assert ngrams[1] == 'la'
        assert ngrams[2] == 'an'
        assert ngrams[3] == 'ng'
        assert ngrams[4] == 'gu'
        assert ngrams[5] == 'ua'
        assert ngrams[6] == 'ag'
        assert ngrams[7] == 'ge'
        assert ngrams[8] == 'e$'

    def test_generate_ngrams_order_3(self):
        index = NgramIndex(order=3)

        ngrams = index._generate_ngrams('language')
        assert len(ngrams) == 8

        assert ngrams[0] == '$la'
        assert ngrams[1] == 'lan'
        assert ngrams[2] == 'ang'
        assert ngrams[3] == 'ngu'
        assert ngrams[4] == 'gua'
        assert ngrams[5] == 'uag'
        assert ngrams[6] == 'age'
        assert ngrams[7] == 'ge$'

    def test_generate_ngrams_order_4(self):
        index = NgramIndex(order=4)

        ngrams = index._generate_ngrams('language')
        assert len(ngrams) == 7

        assert ngrams[0] == '$lan'
        assert ngrams[1] == 'lang'
        assert ngrams[2] == 'angu'
        assert ngrams[3] == 'ngua'
        assert ngrams[4] == 'guag'
        assert ngrams[5] == 'uage'
        assert ngrams[6] == 'age$'

    def test_add_term_absent_ngrams(self):
        index = NgramIndex(order=4)

        index.add_term('python')
        assert index.size() == 5

        assert index.get_terms('$pyt') == ['python']
        assert index.get_terms('pyth') == ['python']
        assert index.get_terms('ytho') == ['python']
        assert index.get_terms('thon') == ['python']
        assert index.get_terms('hon$') == ['python']

    def test_add_term_present_ngrams_and_absent_term(self):
        entries = {'$hea': ['heart'], 'hear': ['heart'],
                   'eart': ['heart'], 'art$': ['heart']}
        index = NgramIndex(entries, order=4)

        index.add_term('hear')
        assert index.size() == 5

        assert index.get_terms('$hea') == ['heart', 'hear']
        assert index.get_terms('hear') == ['heart', 'hear']
        assert index.get_terms('ear$') == ['hear']
        assert index.get_terms('eart') == ['heart']
        assert index.get_terms('art$') == ['heart']

    def test_add_term_present_ngrams_and_present_term(self):
        entries = {'$ho': ['home'], 'hom': ['home'], 'ome': ['home'], 'me$': ['home']}
        index = NgramIndex(entries, order=3)

        index.add_term('home')
        assert index.size() == 4

        assert index.get_terms('$ho') == ['home']
        assert index.get_terms('hom') == ['home']
        assert index.get_terms('ome') == ['home']
        assert index.get_terms('me$') == ['home']

    def test_remove_term_absent_term_and_absent_ngram(self):
        entries = { '$ca': ['cat'], 'cat': ['cat'], 'at$': ['cat'] }
        index = NgramIndex(entries, order=3)

        index.remove_term('ruby')
        assert index.size() == 3

        assert index.get_terms('$ca') == ['cat']
        assert index.get_terms('cat') == ['cat']
        assert index.get_terms('at$') == ['cat']

    def test_remove_term_absent_term_and_present_ngram(self):
        entries = { '$on': ['onion'], 'nio': ['onion'], 'ion': ['onion'], 'on$': ['onion'] }
        index   = NgramIndex(entries, order=3)
        
        index.remove_term('on')
        assert index.size() == 4

        assert index.get_terms('$on') == ['onion']
        assert index.get_terms('nio') == ['onion']
        assert index.get_terms('ion') == ['onion']
        assert index.get_terms('on$') == ['onion']

    def test_remove_term_present_term_and_not_alone(self):
        entries = {'$ca': ['cat', 'catch'], 'cat': ['cat', 'catch'],
                   'at$': ['cat', 'at'], 'atc': ['catch'],
                   'tch': ['catch'], 'ch$': ['catch'], '$at': ['at']}
        index = NgramIndex(entries, order=3)

        index.remove_term('cat')
        assert index.size() == 7

        assert index.get_terms('$ca') == ['catch']
        assert index.get_terms('cat') == ['catch']
        assert index.get_terms('at$') == ['at']
        assert index.get_terms('atc') == ['catch']
        assert index.get_terms('tch') == ['catch']
        assert index.get_terms('ch$') == ['catch']
        assert index.get_terms('$at') == ['at']

    def test_remove_term_present_term_and_alone(self):
        entries = { '$ca': ['cat'], 'cat': ['cat'], 'at$': ['cat'] }
        index = NgramIndex(entries, order=3)

        index.remove_term('cat')
        assert index.size() == 0

    def test_get_terms_present_ngram(self):
        entries = { '$re': ['reduzir', 'reutilizar', 'reciclar'] }
        index   = NgramIndex(entries, order=3)

        terms = index.get_terms('$re')
        assert len(terms) == 3

        assert 'reduzir'    in terms
        assert 'reutilizar' in terms
        assert 'reciclar'   in terms

    def test_get_terms_absent_ngram(self):
        entries = { '$re': ['reduzir', 'reutilizar', 'reciclar'] }
        index   = NgramIndex(entries, order=3)

        terms = index.get_terms('$ra')
        assert len(terms) == 0

    def test_contains_present(self):
        entries = { '$do': ['dog'], 'dog': ['dog'], 'og$': ['dog'] }
        index   = NgramIndex(entries)
        assert index.contains('og$') == True

    def test_contains_absent(self):
        entries = { '$do': ['dog'], 'dog': ['dog'], 'og$': ['dog'] }
        index   = NgramIndex(entries)
        assert index.contains('at$') == False
