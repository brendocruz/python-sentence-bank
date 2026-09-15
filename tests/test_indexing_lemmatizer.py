from sentencebank.indexing.lemmatizer import Lemmatizer


class TestLemmatizer:

    def test_count_zero(self):
        lemmatizer = Lemmatizer()

        assert lemmatizer.variation_count() == 0
        assert lemmatizer.lemma_count()     == 0

    def test_count_non_zero(self):
        TERM_ID_PUT     = 20
        TERM_ID_PUTS    = 21
        TERM_ID_PUTTING = 22

        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_PUT,     TERM_ID_PUT)
        lemmatizer.set_variation(TERM_ID_PUTS,    TERM_ID_PUT)
        lemmatizer.set_variation(TERM_ID_PUTTING, TERM_ID_PUT)

        assert lemmatizer.variation_count() == 3
        assert lemmatizer.lemma_count()     == 1

    def test_clear(self):
        TERM_ID_PUT     = 20
        TERM_ID_PUTS    = 21
        TERM_ID_PUTTING = 22

        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_PUT,     TERM_ID_PUT)
        lemmatizer.set_variation(TERM_ID_PUTS,    TERM_ID_PUT)
        lemmatizer.set_variation(TERM_ID_PUTTING, TERM_ID_PUT)

        lemmatizer.clear()
        assert lemmatizer.variation_count() == 0
        assert lemmatizer.lemma_count()     == 0

    def test_remove_variation_present_variation_retains_lemma(self):
        TERM_ID_BE    = 10
        TERM_ID_WERE  = 12
        TERM_ID_WHERE = 90

        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_WERE,  TERM_ID_BE)
        lemmatizer.set_variation(TERM_ID_WHERE, TERM_ID_BE)

        lemmatizer.remove_variation(TERM_ID_WHERE)

        assert lemmatizer.variation_count()       == 1
        assert lemmatizer.lemma_count()           == 1
        assert lemmatizer.lemmatize(TERM_ID_WERE) == TERM_ID_BE

        variations = lemmatizer.get_variations(TERM_ID_BE)
        assert len(variations) == 1
        assert TERM_ID_WERE    in variations

    def test_remove_variation_present_variation_cleans_lemma(self):
        TERM_ID_BE   = 10
        TERM_ID_WERE = 12

        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_WERE,  TERM_ID_BE)

        lemmatizer.remove_variation(TERM_ID_WERE)

        assert lemmatizer.variation_count() == 0
        assert lemmatizer.lemma_count()     == 0

    def test_remove_variation_absent_variation(self):
        TERM_ID_BE   = 10
        TERM_ID_WERE = 12
        TERM_ID_WHERE = 90

        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_WERE,  TERM_ID_BE)

        lemmatizer.remove_variation(TERM_ID_WHERE)

        assert lemmatizer.variation_count()       == 1
        assert lemmatizer.lemma_count()           == 1
        assert lemmatizer.lemmatize(TERM_ID_WERE) == TERM_ID_BE

        variations = lemmatizer.get_variations(TERM_ID_BE)
        assert len(variations) == 1
        assert TERM_ID_WERE    in variations

    def test_set_variation_absent_variation_creates_lemma(self):
        TERM_ID_BE  = 10
        TERM_ID_WAS = 11

        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_WAS, TERM_ID_BE)

        assert lemmatizer.variation_count()          == 1
        assert lemmatizer.lemma_count()              == 1
        assert lemmatizer.lemmatize(TERM_ID_WAS)     == TERM_ID_BE

        variations = lemmatizer.get_variations(TERM_ID_BE) 
        assert len(variations) == 1
        assert TERM_ID_WAS     in variations

    def test_set_variation_present_variation_reassigns_lemma(self):
        TERM_ID_BE   = 10
        TERM_ID_WAS  = 11
        TERM_ID_BEEN = 13

        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_WAS, TERM_ID_BEEN)
        lemmatizer.set_variation(TERM_ID_WAS, TERM_ID_BE)

        assert lemmatizer.variation_count()    == 1
        assert lemmatizer.lemma_count()        == 1
        assert lemmatizer.lemmatize(TERM_ID_WAS)     == TERM_ID_BE
        assert lemmatizer.get_variations(TERM_ID_BE) == [TERM_ID_WAS]

    def test_set_variation_present_lemma_appends_variation(self):
        TERM_ID_BE   = 10
        TERM_ID_WAS  = 11
        TERM_ID_WERE = 12

        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_WAS, TERM_ID_BE)
        lemmatizer.set_variation(TERM_ID_WERE, TERM_ID_BE)

        assert lemmatizer.variation_count()       == 2
        assert lemmatizer.lemma_count()           == 1
        assert lemmatizer.lemmatize(TERM_ID_WAS)  == TERM_ID_BE
        assert lemmatizer.lemmatize(TERM_ID_WERE) == TERM_ID_BE

        variations = lemmatizer.get_variations(TERM_ID_BE) 
        assert len(variations) == 2
        assert TERM_ID_WAS     in variations
        assert TERM_ID_WERE    in variations

    def test_lemmatize_present_variation(self):
        TERM_ID_BE = 10
        TERM_ID_IS = 14

        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_IS, TERM_ID_BE)

        assert lemmatizer.lemmatize(TERM_ID_IS) == TERM_ID_BE

    def test_lemmatize_absent_variation(self):
        TERM_ID_BE  = 10
        TERM_ID_IS  = 14
        TERM_ID_ARE = 15

        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_IS, TERM_ID_BE)

        assert lemmatizer.lemmatize(TERM_ID_ARE) == None

    def test_get_variations_present_lemma(self):
        TERM_ID_SET     = 40
        TERM_ID_SETS    = 41
        TERM_ID_SETTING = 42

        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_SET,     TERM_ID_SET)
        lemmatizer.set_variation(TERM_ID_SETS,    TERM_ID_SET)
        lemmatizer.set_variation(TERM_ID_SETTING, TERM_ID_SET)

        variations = lemmatizer.get_variations(TERM_ID_SET) 
        assert len(variations) == 3
        assert TERM_ID_SET     in variations
        assert TERM_ID_SETS    in variations
        assert TERM_ID_SETTING in variations

    def test_get_variations_absent_lemma(self):
        TERM_ID_BE      = 10
        TERM_ID_SET     = 40
        TERM_ID_SETS    = 41
        TERM_ID_SETTING = 42

        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_SET,     TERM_ID_SET)
        lemmatizer.set_variation(TERM_ID_SETS,    TERM_ID_SET)
        lemmatizer.set_variation(TERM_ID_SETTING, TERM_ID_SET)

        variations = lemmatizer.get_variations(TERM_ID_BE) 
        assert len(variations) == 0

    def test_contains_variation_present_variation(self):
        TERM_ID_HAVE = 30
        TERM_ID_HAS  = 31
        
        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_HAS, TERM_ID_HAVE)

        assert lemmatizer.contains_variation(TERM_ID_HAS) == True

    def test_contains_variation_absent_variation(self):
        TERM_ID_HAVE = 30
        TERM_ID_HAS  = 31
        TERM_ID_HAD  = 32
        
        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_HAS, TERM_ID_HAVE)

        assert lemmatizer.contains_variation(TERM_ID_HAD) == False

    def test_contains_lemma_present_lemma(self):
        TERM_ID_HAVE = 30
        TERM_ID_HAS  = 31
        
        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_HAS, TERM_ID_HAVE)

        assert lemmatizer.contains_lemma(TERM_ID_HAVE) == True

    def test_contains_lemma_absent_lemma(self):
        TERM_ID_BE   = 10
        TERM_ID_HAVE = 30
        TERM_ID_HAS  = 31
        
        lemmatizer = Lemmatizer()
        lemmatizer.set_variation(TERM_ID_HAS, TERM_ID_HAVE)

        assert lemmatizer.contains_lemma(TERM_ID_BE) == False
