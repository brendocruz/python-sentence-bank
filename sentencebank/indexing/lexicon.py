from sentencebank.indexing.types import TermID
from sqlite3 import Connection


class Lexicon:
    _conn: Connection

    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def contains(self, term: str) -> bool:
        if not term:
            return False

        cursor = self._conn.execute(
                """
                SELECT 1
                FROM   lexicon
                WHERE  term = ?
                LIMIT  1
                """,
                (term,))
        return cursor.fetchone() is not None

    def get_term(self, term_id: TermID) -> str | None:
        cursor = self._conn.execute(
                """
                SELECT term
                FROM   lexicon
                WHERE  term_id = ?
                """,
                (term_id,))
        row    = cursor.fetchone()

        if row is None:
            return None
        return row[0]

    def get_term_id(self, term: str) -> TermID | None:
        if not term:
            return None

        cursor = self._conn.execute(
                """
                SELECT term_id
                FROM   lexicon
                WHERE  term = ?
                """,
                (term,))
        row    = cursor.fetchone()

        if row is None:
            return None
        return row[0]

    def get_term_ids(self, terms: list[str]) -> list[TermID]:
        if not terms:
            return []

        self._conn.execute(
                """
                CREATE TEMP TABLE IF NOT EXISTS temp_terms (
                    term TEXT PRIMARY KEY
                )
                """)
        self._conn.execute(
                """
                DELETE FROM temp_terms
                """)

        self._conn.executemany(
                """
                INSERT OR IGNORE
                INTO   temp_terms (term)
                VALUES (?)
                """, [(term,) for term in terms])

        cursor = self._conn.execute(
                """
                SELECT l.term_id
                FROM   lexicon AS l
                JOIN   temp_terms as t
                ON     l.term = t.term
                """)
        return [row[0] for row in cursor.fetchall()]

    def get_doc_freq(self, term_id: int) -> int:
        cursor = self._conn.execute(
                """
                SELECT doc_freq
                FROM   lexicon
                WHERE  term_id = ?
                """,
                (term_id,))
        row    = cursor.fetchone()

        if row is None:
            return 0
        return row[0]

    def get_col_freq(self, term_id: int) -> int | None:
        cursor = self._conn.execute(
                """
                SELECT col_freq
                FROM   lexicon
                WHERE  term_id = ?
                """,
                (term_id,))
        row    = cursor.fetchone()

        if row is None:
            return 0
        return row[0]

    def get_all_terms(self) -> list[str]:
        cursor = self._conn.execute('SELECT term FROM lexicon')
        return [row[0] for row in cursor.fetchall()]

    def get_all_protected_terms(self) -> list[str]:
        cursor = self._conn.execute(
                """
                SELECT term
                FROM   lexicon
                WHERE  is_protected = 1
                """)
        return [row[0] for row in cursor.fetchall()]

    def size(self) -> int:
        cursor = self._conn.execute('SELECT COUNT(*) FROM lexicon')
        row    = cursor.fetchone()

        assert row is not None
        return row[0]

    def add_term(self, term: str, is_protected: bool = False) -> TermID:
        if not term:
            message = '`term` must not be an empty string'
            raise ValueError(message)
        
        cursor = self._conn.execute(
                """
                INSERT OR IGNORE
                INTO   lexicon (term, doc_freq, col_freq, is_protected)
                VALUES (?, 0, 0, ?)
                """,
                (term, is_protected))
        assert cursor.lastrowid
        return cursor.lastrowid

    def increment_doc_freq(self, term_id: int, amount: int) -> None:
        self._conn.execute(
                """
                UPDATE lexicon
                SET    doc_freq = doc_freq + ?
                WHERE  term_id = ?
                """,
                (amount, term_id,))
        
    def decrement_doc_freq(self, term_id: int, amount: int) -> None:
        self._conn.execute(
                """
                UPDATE lexicon
                SET    doc_freq = MAX(0, doc_freq - ?)
                WHERE  term_id = ?
                """,
                (amount, term_id,))

    def increment_col_freq(self, term_id: int, amount: int) -> None:
        self._conn.execute(
                """
                UPDATE lexicon
                SET    col_freq = col_freq + ?
                WHERE  term_id = ?
                """,
                (amount, term_id,))

    def decrement_col_freq(self, term_id: int, amount: int) -> None:
        self._conn.execute(
                """
                UPDATE lexicon
                SET    col_freq = MAX(0, col_freq - ?)
                WHERE  term_id = ?
                """,
                (amount, term_id,))

    def is_protected_term(self, term_id: TermID) -> bool:
        cursor = self._conn.execute(
                """
                SELECT is_protected
                FROM   lexicon
                WHERE  term_id = ?
                """,
                (term_id,))
        row    = cursor.fetchone()

        if row is None:
            return False
        return bool(row[0])

    def purge_unused_terms(self) -> list[str]:
        cursor = self._conn.execute(
                """
                DELETE
                FROM   lexicon
                WHERE  doc_freq == 0 AND is_protected = FALSE
                RETURNING term
                """)
        return [row[0] for row in cursor.fetchall()]

