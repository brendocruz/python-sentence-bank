from sqlite3 import connect

from pytest import fixture

from sentencebank.db.database import init_db

@fixture
def db_connection():
        conn = connect(':memory:')
        conn.execute('PRAGMA foreign_keys = ON;')
        init_db(conn)
        yield conn
        conn.close()
