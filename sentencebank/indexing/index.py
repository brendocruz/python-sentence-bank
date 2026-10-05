from sqlite3 import Connection

from sentencebank.indexing import types as t


class InvertedIndex:
    _conn: Connection

    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def _populate_temp_term_ids_table(self, term_ids: list[t.TermID]) -> None:
        self._conn.execute(
                """
                CREATE TEMP TABLE IF NOT EXISTS temp_term_ids (
                    term_id INTEGER PRIMARY KEY
                )
                """)
        self._conn.execute(
                """
                DELETE FROM temp_term_ids
                """)

        self._conn.executemany(
                """
                INSERT OR IGNORE
                INTO   temp_term_ids (term_id)
                VALUES (?)
                """,
                [(term_id,) for term_id in term_ids])

    def add_posting(self, term_id: t.TermID, posting: t.Posting) -> None:
        self._conn.execute(
                """
                INSERT
                INTO   inverted_index
                       (term_id, doc_id, position, start_ofs, end_ofs)
                VALUES (?, ?, ?, ?, ?)
                """,
                (term_id, posting.doc_id, posting.position, posting.start, posting.end))

    def get_postings_by_term_id(self, term_id: t.TermID) -> list[t.Posting]:
        cursor = self._conn.execute(
                """
                SELECT   doc_id, position, start_ofs, end_ofs
                FROM     inverted_index
                WHERE    term_id = ?
                ORDER BY doc_id, position
                """,
                (term_id,))

        postings: list[t.Posting] = []
        for row in cursor.fetchall():
            posting = t.Posting(doc_id=row[0],
                                position=row[1],
                                start=row[2],
                                end=row[3])
            postings.append(posting)
        
        return postings

    def get_postings_by_document_id(self, doc_id: t.DocID) -> list[t.TermPosting]:
        cursor = self._conn.execute(
                """
                SELECT   term_id, position, start_ofs, end_ofs
                FROM     inverted_index
                WHERE    doc_id = ?
                ORDER BY position
                """,
                (doc_id,))

        term_postings: list[t.TermPosting] = []
        for row in cursor.fetchall():
            term_id = row[0]
            posting = t.Posting(doc_id=doc_id,
                              position=row[1],
                              start=row[2],
                              end=row[3])
            term_posting = t.TermPosting(term_id, posting)
            term_postings.append(term_posting)
        
        return term_postings

    def get_term_counts_by_document(self, doc_id: t.DocID) -> list[t.TermCount]:
        cursor = self._conn.execute(
                """
                SELECT   term_id, COUNT(*) AS count
                FROM     inverted_index
                WHERE    doc_id = ?
                GROUP BY term_id
                """,
                (doc_id,))

        counts: list[t.TermCount] = []
        for row in cursor.fetchall():
            count = t.TermCount(term_id=row[0], count=row[1])
            counts.append(count)
        return counts

    def get_document_ids_by_term_id(self, term_id: t.TermID) -> set[t.DocID]:
        cursor = self._conn.execute(
                """
                SELECT DISTINCT doc_id
                FROM   inverted_index
                WHERE  term_id = ?
                """,
                (term_id,))
        return set(row[0] for row in cursor.fetchall())

    def get_document_ids_by_term_ids(self, term_ids: list[t.TermID]) -> set[t.DocID]:
        if not term_ids:
            return set()

        self._populate_temp_term_ids_table(term_ids)

        cursor = self._conn.execute(
                """
                SELECT DISTINCT idx.doc_id
                FROM   inverted_index AS idx
                JOIN   temp_term_ids AS tmp
                ON     idx.term_id = tmp.term_id
                """)

        return set(row[0] for row in cursor.fetchall())

    def get_positions_by_document_id(self, doc_id: t.DocID) -> list[t.TermPosition]:
        cursor = self._conn.execute(
                """
                SELECT   term_id, position
                FROM     inverted_index
                WHERE    doc_id = ?
                ORDER BY position
                """,
                (doc_id,))

        position: list[t.TermPosition] = []
        for row in cursor.fetchall():
            count = t.TermPosition(term_id=row[0], position=row[1])
            position.append(count)
        return position

    def get_positions_by_term_id(self, term_id: t.TermID) -> t.TermPositionMap:
        cursor = self._conn.execute(
                """
                SELECT doc_id, term_id, position
                FROM   inverted_index
                WHERE  term_id = ?
                """,
                (term_id,))

        positions: t.TermPositionMap = { }
        for row in cursor.fetchall():
            if row[0] not in positions:
                positions[row[0]] = []
            position = t.TermPosition(row[1], row[2])
            positions[row[0]].append(position)
        return positions

    def get_positions_by_term_ids(self, term_ids: list[t.TermID]) -> t.TermPositionMap:
        if not term_ids:
            return {}

        self._populate_temp_term_ids_table(term_ids)

        cursor = self._conn.execute(
                """
                SELECT idx.doc_id, idx.term_id, idx.position
                FROM   inverted_index AS idx
                JOIN   temp_term_ids AS tmp
                ON     idx.term_id = tmp.term_id
                """)

        positions: t.TermPositionMap = { }
        for row in cursor.fetchall():
            if row[0] not in positions:
                positions[row[0]] = []
            position = t.TermPosition(row[1], row[2])
            positions[row[0]].append(position)
        return positions

    def remove_posting(self, term_id: t.TermID, doc_id: t.DocID, position: int) -> bool:
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

    def remove_postings_by_document(self, doc_id: t.DocID) -> bool:
        cursor = self._conn.execute(
                """
                DELETE
                FROM   inverted_index
                WHERE  doc_id = ?
                """,
                (doc_id,))
        return cursor.rowcount > 0

    def contains_posting(self, term_id: t.TermID, doc_id: t.DocID, position: int) -> bool:
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

    def contains_term(self, term_id: t.TermID) -> bool:
        cursor = self._conn.execute(
                """
                SELECT 1
                FROM   inverted_index 
                WHERE  term_id = ?
                LIMIT  1
                """,
                (term_id,))
        return cursor.fetchone() is not None

    def posting_count(self) -> int:
        cursor = self._conn.execute(
                """
                SELECT COUNT(*)
                FROM   inverted_index
                """)
        row    = cursor.fetchone()
        return row[0]
