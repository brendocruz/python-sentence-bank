from sentencebank.indexing.trie import Trie


class TestTrie:

    def test_insert_empty_string(self):
        trie = Trie()

        assert trie.insert('') == False

    def test_insert_absent_term(self):
        trie = Trie()

        assert trie.insert('get')      == True

        assert trie.contains('g')      == False
        assert trie.contains('ge')     == False
        assert trie.contains('get')    == True

    def test_insert_present_term(self):
        trie = Trie()
        trie.insert('get')

        assert trie.insert('get')      == False

        assert trie.contains('g')      == False
        assert trie.contains('ge')     == False
        assert trie.contains('get')    == True

    def test_insert_shared_prefix_terms_shorter_to_longer(self):
        trie = Trie()

        assert trie.insert('ask')      == True
        assert trie.insert('asks')     == True
        assert trie.insert('asked')    == True
        assert trie.insert('asker')    == True
        assert trie.insert('asking')   == True

        assert trie.contains('a')      == False
        assert trie.contains('as')     == False
        assert trie.contains('ask')    == True
        assert trie.contains('asks')   == True
        assert trie.contains('aske')   == False
        assert trie.contains('asked')  == True
        assert trie.contains('asker')  == True
        assert trie.contains('aski')   == False
        assert trie.contains('askin')  == False
        assert trie.contains('asking') == True

    def test_insert_shared_prefix_terms_longer_to_shorter(self):
        trie = Trie()

        assert trie.insert('asking')   == True
        assert trie.insert('asker')    == True
        assert trie.insert('asked')    == True
        assert trie.insert('asks')     == True
        assert trie.insert('ask')      == True

        assert trie.contains('a')      == False
        assert trie.contains('as')     == False
        assert trie.contains('ask')    == True
        assert trie.contains('asks')   == True
        assert trie.contains('aske')   == False
        assert trie.contains('asked')  == True
        assert trie.contains('asker')  == True
        assert trie.contains('aski')   == False
        assert trie.contains('askin')  == False
        assert trie.contains('asking') == True

    def test_insert_shared_suffix_terms_shorter_to_longer(self):
        trie = Trie()

        assert trie.insert('ever')      == True
        assert trie.insert('asker')     == True
        assert trie.insert('teacher')   == True

        assert trie.contains('e')       == False
        assert trie.contains('ev')      == False
        assert trie.contains('eve')     == False
        assert trie.contains('ever')    == True
        assert trie.contains('a')       == False
        assert trie.contains('as')      == False
        assert trie.contains('ask')     == False
        assert trie.contains('aske')    == False
        assert trie.contains('asker')   == True
        assert trie.contains('t')       == False
        assert trie.contains('te')      == False
        assert trie.contains('tea')     == False
        assert trie.contains('teac')    == False
        assert trie.contains('teach')   == False
        assert trie.contains('teache')  == False
        assert trie.contains('teacher') == True

    def test_insert_shared_suffix_terms_longer_to_shorter(self):
        trie = Trie()

        assert trie.insert('teacher')   == True
        assert trie.insert('asker')     == True
        assert trie.insert('ever')      == True

        assert trie.contains('e')       == False
        assert trie.contains('ev')      == False
        assert trie.contains('eve')     == False
        assert trie.contains('ever')    == True
        assert trie.contains('a')       == False
        assert trie.contains('as')      == False
        assert trie.contains('ask')     == False
        assert trie.contains('aske')    == False
        assert trie.contains('asker')   == True
        assert trie.contains('t')       == False
        assert trie.contains('te')      == False
        assert trie.contains('tea')     == False
        assert trie.contains('teac')    == False
        assert trie.contains('teach')   == False
        assert trie.contains('teache')  == False
        assert trie.contains('teacher') == True

    def test_contains_empty_tree(self):
        trie = Trie()
        trie.insert('')

        assert trie.contains('ran') == False

    def test_contains_empty_string(self):
        trie = Trie()
        trie.insert('ran')

        assert trie.contains('') == False

    def test_contains_present_term(self):
        trie = Trie()
        trie.insert('run')
        trie.insert('runs')
        trie.insert('runner')
        trie.insert('runners')

        assert trie.contains('run')     == True
        assert trie.contains('runs')    == True
        assert trie.contains('runner')  == True
        assert trie.contains('runners') == True

    def test_contains_absent_shorter_term(self):
        trie = Trie()
        trie.insert('meaning')

        assert trie.contains('mean') == False

    def test_contains_absent_longer_term(self):
        trie = Trie()
        trie.insert('mean')

        assert trie.contains('meaning') == False 

    def test_remove_empty_string(self):
        trie = Trie()
        trie.insert('cat')

        assert trie.remove('')      == False

        assert trie.contains('c')   == False
        assert trie.contains('ca')  == False
        assert trie.contains('cat') == True
        
    def test_remove_empty_tree(self):
        trie = Trie()

        assert trie.remove('cat') == False

    def test_remove_last_term(self):
        trie = Trie()
        trie.insert('language')

        assert trie.remove('language')   == True

        assert trie.contains('l')        == False
        assert trie.contains('la')       == False
        assert trie.contains('lan')      == False
        assert trie.contains('lang')     == False
        assert trie.contains('langu')    == False
        assert trie.contains('langua')   == False
        assert trie.contains('languag')  == False
        assert trie.contains('language') == False

    def tset_remove_absent_term(self):
        trie = Trie()
        trie.insert('dog')

        assert trie.remove('cat')   == False

        assert trie.contains('d')   == False
        assert trie.contains('do')  == False
        assert trie.contains('dog') == True
        assert trie.contains('c')   == False
        assert trie.contains('ca')  == False
        assert trie.contains('cat') == True

    def test_remove_shared_prefix_terms_removes_present_longer_one(self):
        trie = Trie()
        trie.insert('let')
        trie.insert('letting')

        assert trie.remove('letting')   == True

        assert trie.contains('l')       == False
        assert trie.contains('le')      == False
        assert trie.contains('let')     == True
        assert trie.contains('lett')    == False
        assert trie.contains('letti')   == False
        assert trie.contains('lettin')  == False
        assert trie.contains('letting') == False

    def test_remove_shared_prefix_terms_removes_present_shorter_one(self):
        trie = Trie()
        trie.insert('let')
        trie.insert('letting')

        assert trie.remove('let')       == True

        assert trie.contains('l')       == False
        assert trie.contains('le')      == False
        assert trie.contains('let')     == False
        assert trie.contains('lett')    == False
        assert trie.contains('letti')   == False
        assert trie.contains('lettin')  == False
        assert trie.contains('letting') == True

    def test_remove_shared_prefix_terms_removes_the_absent_longer_one(self):
        trie = Trie()
        trie.insert('let')

        assert trie.remove('letting')   == False

        assert trie.contains('l')       == False
        assert trie.contains('le')      == False
        assert trie.contains('let')     == True
        assert trie.contains('lett')    == False
        assert trie.contains('letti')   == False
        assert trie.contains('lettin')  == False
        assert trie.contains('letting') == False

    def test_remove_shared_prefix_terms_removes_the_absent_shorter_one(self):
        trie = Trie()
        trie.insert('letting')

        assert trie.remove('let')       == False

        assert trie.contains('l')       == False
        assert trie.contains('le')      == False
        assert trie.contains('let')     == False
        assert trie.contains('lett')    == False
        assert trie.contains('letti')   == False
        assert trie.contains('lettin')  == False
        assert trie.contains('letting') == True

    def test_remove_unshared_suffix_keeps_sibling_branches(self):
        trie = Trie()
        trie.insert('invest')
        trie.insert('investigation')
        trie.insert('investigative')

        assert trie.remove('investigative')   == True

        assert trie.contains('i')             == False
        assert trie.contains('in')            == False
        assert trie.contains('inv')           == False
        assert trie.contains('inve')          == False
        assert trie.contains('inves')         == False
        assert trie.contains('invest')        == True
        assert trie.contains('investi')       == False
        assert trie.contains('investig')      == False
        assert trie.contains('investiga')     == False
        assert trie.contains('investigat')    == False
        assert trie.contains('investigati')   == False
        assert trie.contains('investigatio')  == False
        assert trie.contains('investigation') == True
        assert trie.contains('investigativ')  == False
        assert trie.contains('investigative') == False

    def test_search_empty_tree_returns_empty(self):
        trie = Trie()
        trie.insert('')

        matches = trie.search('like')
        assert matches == []

    def test_search_empty_pattern_returns_empty(self):
        trie = Trie()
        trie.insert('like')

        matches = trie.search('')
        assert matches == []

    def test_search_exact_match_present_term_returns_match(self):
        trie = Trie()
        trie.insert('hello')

        matches = trie.search('hello')
        assert matches == ['hello']

    def test_search_exact_match_absent_term_returns_empty(self):
        trie = Trie()
        trie.insert('write')

        matches = trie.search('right')
        assert matches == []

    def test_search_single_char_wildcard_as_suffix(self):
        trie = Trie()
        trie.insert('brave')

        matches = trie.search('brav?')
        assert matches == ['brave']

    def test_search_single_char_wildcard_as_prefix(self):
        trie = Trie()
        trie.insert('clean')

        matches = trie.search('?lean')
        assert matches == ['clean']

    def test_search_single_char_wildcard_as_infix(self):
        trie = Trie()
        trie.insert('smart')

        matches = trie.search('sm?rt')
        assert matches == ['smart']

    def test_search_single_char_wildcard_as_suffix_matches_multiple_branches(self):
        trie = Trie()
        trie.insert('star')
        trie.insert('stay')

        matches = trie.search('sta?')
        assert matches == ['star', 'stay']

    def test_search_single_char_wildcard_as_prefix_matches_multiple_branches(self):
        trie = Trie()
        trie.insert('done')
        trie.insert('gone')

        matches = trie.search('?one')
        assert matches == ['done', 'gone']

    def test_search_single_char_wildcard_as_infix_matches_multiple_branches(self):
        trie = Trie()
        trie.insert('danger')
        trie.insert('dancer')

        matches = trie.search('dan?er')
        assert matches == ['dancer', 'danger']

    def test_search_single_char_wildcard_adjacent(self):
        trie = Trie()
        trie.insert('pear')
        trie.insert('peer')

        matches = trie.search('p??r')
        assert matches == ['pear', 'peer']

    def test_search_single_char_wildcard_pattern_too_long_returns_empty(self):
        trie = Trie()
        trie.insert('hop')

        matches = trie.search('hop?')
        assert matches == []

    def test_search_multi_char_wildcard_as_suffix_matches_zero(self):
        trie = Trie()
        trie.insert('sit')

        matches = trie.search('sit*')
        assert matches == ['sit']

    def test_search_multi_char_wildcard_as_suffix_matches_one(self):
        trie = Trie()
        trie.insert('site')

        matches = trie.search('sit*')
        assert matches == ['site']

    def test_search_multi_char_wildcard_as_suffix_matches_many(self):
        trie = Trie()
        trie.insert('sitting')

        matches = trie.search('sit*')
        assert matches == ['sitting']

    def test_search_multi_char_wildcard_as_prefix_matches_zero(self):
        trie = Trie()
        trie.insert('mile')

        matches = trie.search('*mile')
        assert matches == ['mile']

    def test_search_multi_char_wildcard_as_prefix_matches_one(self):
        trie = Trie()
        trie.insert('smile')

        matches = trie.search('*mile')
        assert matches == ['smile']

    def test_search_multi_char_wildcard_as_prefix_matches_many(self):
        trie = Trie()
        trie.insert('outsmile')

        matches = trie.search('*mile')
        assert matches == ['outsmile']

    def test_search_multi_char_wildcard_as_infix_matches_zero(self):
        trie = Trie()
        trie.insert('herd')

        matches = trie.search('he*rd')
        assert matches == ['herd']

    def test_search_multi_char_wildcard_as_infix_matches_one(self):
        trie = Trie()
        trie.insert('heard')

        matches = trie.search('he*rd')
        assert matches == ['heard']

    def test_search_multi_char_wildcard_as_infix_matches_many(self):
        trie = Trie()
        trie.insert('landscaping')

        matches = trie.search('land*ing')
        assert matches == ['landscaping']

    def test_search_multi_char_wildcard_as_suffix_matches_multiple_branches(self):
        trie = Trie()
        trie.insert('within')
        trie.insert('without')

        matches = trie.search('with*')
        assert matches == ['within', 'without']

    def test_search_multi_char_wildcard_as_prefix_matches_multiple_branches(self):
        trie = Trie()
        trie.insert('teacher')
        trie.insert('researcher')

        matches = trie.search('*cher')
        assert matches == ['researcher', 'teacher']

    def test_search_multi_char_wildcard_as_infix_matches_multiple_branches(self):
        trie = Trie()
        trie.insert('teaching')
        trie.insert('testing')

        matches = trie.search('te*ing')
        assert matches == ['teaching', 'testing']

    def test_search_multi_char_wildcard_alone_returns_all_terms(self):
        trie = Trie()
        trie.insert('sunflower')
        trie.insert('orchid')
        trie.insert('tulip')

        matches = trie.search('*')
        assert matches == ['orchid', 'sunflower', 'tulip']

    def test_search_multi_char_wildcard_adjacent_prevents_duplicates(self):
        trie = Trie()
        trie.insert('cat')

        matches = trie.search('c**t')
        assert matches == ['cat']

    def test_clear(self):
        trie = Trie()
        trie.insert('dog')
        
        trie.clear()

        assert trie.contains('d')   == False
        assert trie.contains('do')  == False
        assert trie.contains('dog') == False
