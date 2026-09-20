from pathlib import Path
from sqlite3 import Connection

SCHEMA_PATH = Path(__file__).parent.joinpath('schema.sql')

def init_db(conn: Connection) -> None:
    schema_sql = SCHEMA_PATH.read_text(encoding='utf-8')
    conn.executescript(schema_sql)
    conn.commit()
