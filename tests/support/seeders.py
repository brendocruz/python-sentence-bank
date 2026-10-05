from sqlite3 import Connection

from sentencebank.indexing.types import TermID, DocID

def seed_document(conn: Connection, document: str) -> DocID:
    cursor = conn.execute(
            """
            INSERT INTO documents (text)
            VALUES    (?)
            RETURNING doc_id
            """,
            (document,))
    row = cursor.fetchone()
    assert row is not None
    return row[0]

def seed_term(conn: Connection, term: str, *,
              is_protected: bool = False,
              doc_freq: int = 0, col_freq: int = 0) -> TermID:
    cursor = conn.execute(
            """
            INSERT INTO lexicon (term, is_protected, doc_freq, col_freq)
            VALUES    (?, ?, ?, ?)
            RETURNING term_id
            """,
            (term, is_protected, doc_freq, col_freq))
    row = cursor.fetchone()
    assert row is not None
    return row[0]

def seed_lemma(conn: Connection, term_id: TermID, lemma_id: TermID) -> None:
    conn.execute(
            """
            INSERT INTO lemmas (term_id, lemma_id)
            VALUES (?, ?)
            """,
            (term_id, lemma_id))
