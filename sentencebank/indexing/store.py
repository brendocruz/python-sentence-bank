from sentencebank.indexing.types import DocID
from sqlite3 import Connection


class DocumentStore:
    _conn: Connection

    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def add_document(self, text: str) -> DocID:
        cursor = self._conn.execute(
                'INSERT INTO documents (text) VALUES (?)',
                (text,))
        assert cursor.lastrowid
        return cursor.lastrowid

    def remove_document(self, doc_id: DocID) -> bool:
        cursor = self._conn.execute(
                'DELETE FROM documents WHERE doc_id = ?',
                (doc_id,))
        return cursor.rowcount > 0

    def get_document(self, doc_id: DocID) -> str | None:
        cursor = self._conn.execute(
                'SELECT text FROM documents WHERE doc_id = ?',
                (doc_id,))
        row    = cursor.fetchone()

        if row is None:
            return None
        return row[0] 

    def size(self) -> int:
        cursor = self._conn.execute('SELECT COUNT(*) FROM documents')
        row    = cursor.fetchone()

        assert row is not None
        return row[0]
