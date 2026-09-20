from sentencebank.indexing.types import TermID, DocID
from sqlite3 import Connection
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Posting:
    doc_id: DocID
    position: int
    start: int
    end: int


class InvertedIndex:
    _conn: Connection

    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def posting_count(self) -> int:
        cursor = self._conn.execute(
                """
                SELECT COUNT(*)
                FROM   inverted_index
                """)
        row    = cursor.fetchone()
        return row[0]

    def get_postings(self, term_id: TermID) -> list[Posting]:
        cursor = self._conn.execute(
                """
                SELECT   doc_id, position, start_ofs, end_ofs
                FROM     inverted_index
                WHERE    term_id = ?
                ORDER BY doc_id, position
                """,
                (term_id,))

        postings: list[Posting] = []
        for row in cursor.fetchall():
            posting = Posting(doc_id=row[0],
                              position=row[1],
                              start=row[2],
                              end=row[3])
            postings.append(posting)
        
        return postings

    def add_posting(self, term_id: TermID, posting: Posting) -> None:
        self._conn.execute(
                """
                INSERT
                INTO   inverted_index
                       (term_id, doc_id, position, start_ofs, end_ofs)
                VALUES (?, ?, ?, ?, ?)
                """,
                (term_id, posting.doc_id, posting.position, posting.start, posting.end))

    def remove_posting(self, term_id: TermID, doc_id: DocID, position: int) -> bool:
        cursor = self._conn.execute(
                """
                DELETE
                FROM   inverted_index
                WHERE  term_id  = ?
                AND    doc_id   = ?
                AND    position = ?
                """,
                (term_id, doc_id, position,))
        return cursor.rowcount > 0

    def remove_document_postings(self, doc_id: DocID) -> bool:
        cursor = self._conn.execute(
                """
                DELETE
                FROM   inverted_index
                WHERE  doc_id = ?
                """,
                (doc_id,))
        return cursor.rowcount > 0

    def contains_posting(self, term_id: TermID, doc_id: DocID, position: int) -> bool:
        cursor = self._conn.execute(
                """
                SELECT 1
                FROM   inverted_index
                WHERE  term_id  = ?
                AND    doc_id   = ?
                AND    position = ?
                LIMIT  1
                """,
                (term_id, doc_id, position))
        return cursor.fetchone() is not None

    def contains_term(self, term_id: TermID) -> bool:
        cursor = self._conn.execute(
                """
                SELECT 1
                FROM   inverted_index 
                WHERE  term_id = ?
                LIMIT  1
                """,
                (term_id,))
        return cursor.fetchone() is not None
