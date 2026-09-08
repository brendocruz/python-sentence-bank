from sentencebank.indexing.lemmatizer import Lemmatizer


class TestLemmatizer:

    def test_count_zero(self):
        variations = {}
        lemmas     = {}
        lemmatizer = Lemmatizer(variations, lemmas)

        assert lemmatizer.variation_count() == 0
        assert lemmatizer.lemma_count()     == 0

    def test_count_non_zero(self):
        variations = {'put': 'put', 'puts': 'put', 'putting': 'put'}
        lemmas     = {'put': ['put', 'puts', 'putting']}
        lemmatizer = Lemmatizer(variations, lemmas)

        assert lemmatizer.variation_count() == 3
        assert lemmatizer.lemma_count()     == 1

    def test_clear(self):
        variations = {'put': 'put', 'puts': 'put', 'putting': 'put'}
        lemmas     = {'put': ['put', 'puts', 'putting']}
        lemmatizer = Lemmatizer(variations, lemmas)

        lemmatizer.clear()
        assert lemmatizer.variation_count() == 0
        assert lemmatizer.lemma_count()     == 0

    def test_remove_variation_present_retains_lemma(self):
        variations = {'were': 'be', 'where': 'be'}
        lemmas     = {'be': ['were', 'where']}
        lemmatizer = Lemmatizer(variations, lemmas)

        lemmatizer.remove_variation('where')
        assert lemmatizer.variation_count()    == 1
        assert lemmatizer.lemma_count()        == 1
        assert lemmatizer.lemmatize('were')    == 'be'
        assert lemmatizer.get_variations('be') == ['were']

    def test_remove_variation_present_cleans_lemma(self):
        variations = {'were': 'be'}
        lemmas     = {'be': ['were']}
        lemmatizer = Lemmatizer(variations, lemmas)

        lemmatizer.remove_variation('were')
        assert lemmatizer.variation_count()    == 0
        assert lemmatizer.lemma_count()        == 0

    def test_remove_variation_absent(self):
        variations = {'were': 'be'}
        lemmas     = {'be': ['were']}
        lemmatizer = Lemmatizer(variations, lemmas)

        lemmatizer.remove_variation('where')
        assert lemmatizer.variation_count()    == 1
        assert lemmatizer.lemma_count()        == 1
        assert lemmatizer.lemmatize('were')    == 'be'
        assert lemmatizer.get_variations('be') == ['were']

    def test_set_variation_absent(self):
        variations = {}
        lemmas     = {}
        lemmatizer = Lemmatizer(variations, lemmas)

        lemmatizer.set_variation('was', 'be')
        assert lemmatizer.variation_count()    == 1
        assert lemmatizer.lemma_count()        == 1
        assert lemmatizer.lemmatize('was')     == 'be'
        assert lemmatizer.get_variations('be') == ['was']

    def test_set_variation_present_create_lemma(self):
        variations = {'was': 'been'}
        lemmas     = {'been': ['was']}
        lemmatizer = Lemmatizer(variations, lemmas)

        lemmatizer.set_variation('was', 'be')
        assert lemmatizer.variation_count()    == 1
        assert lemmatizer.lemma_count()        == 1
        assert lemmatizer.lemmatize('was')     == 'be'
        assert lemmatizer.get_variations('be') == ['was']

    def test_set_variation_present_append_lemma(self):
        variations = {'was': 'be'}
        lemmas     = {'be': ['was']}
        lemmatizer = Lemmatizer(variations, lemmas)

        lemmatizer.set_variation('were', 'be')
        assert lemmatizer.variation_count()    == 2
        assert lemmatizer.lemma_count()        == 1
        assert lemmatizer.lemmatize('was')     == 'be'
        assert lemmatizer.lemmatize('were')    == 'be'
        assert lemmatizer.get_variations('be') == ['was', 'were']

    def test_lemmatize_present(self):
        variations = {'is': 'be'}
        lemma      = {'be': ['is']}
        lemmatizer = Lemmatizer(variations, lemma)

        assert lemmatizer.lemmatize('is') == 'be'

    def test_lemmatize_absent(self):
        variations = {'is': 'be'}
        lemma      = {'be': ['is']}
        lemmatizer = Lemmatizer(variations, lemma)

        assert lemmatizer.lemmatize('are') == ''

    def test_get_variations_present(self):
        variations = {'set': 'set', 'sets': 'set', 'setting': 'set'}
        lemmas     = {'set': ['set', 'sets', 'setting']}
        lemmatizer = Lemmatizer(variations, lemmas)

        assert lemmatizer.get_variations('set') == ['set', 'sets', 'setting']

    def test_get_variations_absent(self):
        variations = {'set': 'set', 'sets': 'set', 'setting': 'set'}
        lemmas     = {'set': ['set', 'sets', 'setting']}
        lemmatizer = Lemmatizer(variations, lemmas)

        assert lemmatizer.get_variations('be') == []

    def test_contains_variation_present(self):
        variations = {'has': 'have'}
        lemma      = {'have': ['has']}
        lemmatizer = Lemmatizer(variations, lemma)

        assert lemmatizer.contains_variation('has') == True

    def test_contains_variation_absent(self):
        variations = {'has': 'have'}
        lemma      = {'have': ['has']}
        lemmatizer = Lemmatizer(variations, lemma)

        assert lemmatizer.contains_variation('had') == False

    def test_contains_lemma_present(self):
        variations = {'has': 'have'}
        lemma      = {'have': ['has']}
        lemmatizer = Lemmatizer(variations, lemma)

        assert lemmatizer.contains_lemma('have') == True

    def test_contains_lemma_absent(self):
        variations = {'has': 'have'}
        lemma      = {'have': ['has']}
        lemmatizer = Lemmatizer(variations, lemma)

        assert lemmatizer.contains_lemma('be') == False
