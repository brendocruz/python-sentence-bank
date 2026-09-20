from sentencebank.indexing.types import TermID
from sqlite3 import Connection


class Lemmatizer:
    _conn: Connection

    def __init__(self, connection: Connection) -> None:
        self._conn = connection
    
    def term_count(self) -> int:
        cursor = self._conn.execute('SELECT COUNT(DISTINCT term_id) FROM lemmas')
        row    = cursor.fetchone()
        return row[0]
    
    def lemma_count(self) -> int:
        cursor = self._conn.execute('SELECT COUNT(DISTINCT lemma_id) FROM lemmas')
        row    = cursor.fetchone()
        return row[0]
    
    def remove_term(self, term_id: TermID) -> bool:
        cursor = self._conn.execute(
                'DELETE FROM lemmas where term_id = ?',
                (term_id,))
        return cursor.rowcount > 0


    def add_term(self, term_id: TermID, lemma_id: TermID) -> None:
        self._conn.execute(
                'INSERT INTO lemmas (term_id, lemma_id) VALUES (?, ?)',
                (term_id, lemma_id))

    def lemmatize(self, term_id: TermID) -> TermID:
        cursor = self._conn.execute(
                'SELECT lemma_id FROM lemmas WHERE term_id = ?',
                (term_id,))
        row    = cursor.fetchone()

        if row is None:
            return term_id
        return row[0]

    def get_terms(self, lemma_id: TermID) -> list[TermID]:
        cursor = self._conn.execute(
                'SELECT term_id FROM lemmas WHERE lemma_id = ?',
                (lemma_id,))
        return [row[0] for row in cursor.fetchall()]

    def contains_term(self, term_id: TermID) -> bool:
        cursor = self._conn.execute(
                'SELECT 1 FROM lemmas WHERE term_id = ? LIMIT 1',
                (term_id,))
        return cursor.fetchone() is not None

    def contains_lemma(self, lemma_id: TermID) -> bool:
        cursor = self._conn.execute(
                'SELECT 1 FROM lemmas WHERE lemma_id = ? LIMIT 1',
                (lemma_id,))
        return cursor.fetchone() is not None
