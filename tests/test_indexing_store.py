from sentencebank.indexing.store import DocumentStore
from sentencebank.db.database import init_db
from sqlite3 import connect
from pytest import fixture


class TestDocumentStore:
    store: DocumentStore

    @fixture(autouse=True)
    def setup(self):
        conn = connect(':memory:')

        init_db(conn)
        self.store = DocumentStore(conn)

        yield

        conn.close()

    def test_add_document(self):
        document = 'Hello, World!'

        doc_id = self.store.add_document(document)
        assert self.store.size() == 1

        assert self.store.get_document(doc_id) == document

    def test_remove_document_present_document(self):
        document = 'Hello, World!'
        doc_id   = self.store.add_document(document)

        was_removed = self.store.remove_document(doc_id)
        assert was_removed       == True
        assert self.store.size() == 0

        assert self.store.get_document(doc_id) is None

    def test_remove_document_absent_document(self):
        document = 'Hello, World!'
        doc_id   = self.store.add_document(document)

        absent_doc_id = doc_id + 1
        was_removed   = self.store.remove_document(absent_doc_id)
        assert was_removed       == False
        assert self.store.size() == 1

        assert self.store.get_document(absent_doc_id) is None
        assert self.store.get_document(doc_id)        == document

    def test_size_non_empty(self):
        self.store.add_document('Hello, World!')
        self.store.add_document('Good morning.')

        assert self.store.size() == 2

    def test_size_empty(self):
        assert self.store.size() == 0
