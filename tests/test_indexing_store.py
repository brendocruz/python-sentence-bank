from sentencebank.indexing.store import DocumentStore


class TestDocumentStore:

    def test_add_sentence(self):
        store = DocumentStore()

        doc_id = store.add_sentence("Hello, World!")

        assert store.size()               == 1
        assert store.get_sentence(doc_id) == "Hello, World!"

    def test_remove_sentence_present_sentence(self):
        store  = DocumentStore()
        doc_id = store.add_sentence("Hello, World!")

        assert store.remove_sentence(doc_id) == True
        assert store.size()                  == 0
        assert store.get_sentence(doc_id)    is None

    def test_remove_sentence_absent_sentence(self):
        store  = DocumentStore()
        doc_id = store.add_sentence("Hello, World!")

        absent_doc_id = doc_id + 1
        assert store.remove_sentence(absent_doc_id) == False
        assert store.size()                         == 1
        assert store.get_sentence(absent_doc_id)    is None
        assert store.get_sentence(doc_id)           == "Hello, World!"

    def test_size_non_empty(self):
        store  = DocumentStore()
        store.add_sentence("Hello, World!")
        store.add_sentence("Good morning.")

        assert store.size() == 2

    def test_size_empty(self):
        store  = DocumentStore()

        assert store.size() == 0
