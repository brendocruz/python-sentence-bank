from sqlite3 import Connection

from pytest import fixture, raises

from sentencebank.indexing.store import DocumentStore


class TestDocumentStore:
    _store: DocumentStore

    @fixture(autouse=True)
    def setup(self, db_connection: Connection):
        self._conn = db_connection
        self._store = DocumentStore(self._conn)

    def test_add_document_when_document_is_not_empty(self):
        document = 'Hello, World!'

        doc_id   = self._store.add_document(document)
        assert self._store.size() == 1

        assert self._store.get_document(doc_id) == document

    def test_add_document_when_document_is_empty(self):
        document = ''

        with raises(ValueError):
            self._store.add_document(document)

    def test_remove_document_when_document_is_present(self):
        document = 'Hello, World!'
        doc_id   = self._store.add_document(document)

        was_removed = self._store.remove_document(doc_id)
        assert was_removed == True

        assert self._store.size()               == 0
        assert self._store.get_document(doc_id) is None

    def test_remove_document_when_document_is_absent(self):
        document = 'Hello, World!'
        doc_id   = self._store.add_document(document)

        absent_doc_id = doc_id + 1
        was_removed   = self._store.remove_document(absent_doc_id)
        assert was_removed == False

        assert self._store.size()                      == 1
        assert self._store.get_document(absent_doc_id) is None
        assert self._store.get_document(doc_id)        == document

    def test_size_when_store_is_not_empty(self):
        self._store.add_document('Hello, World!')
        self._store.add_document('Good morning.')

        assert self._store.size() == 2

    def test_size_when_store_is_empty(self):
        assert self._store.size() == 0
