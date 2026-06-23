import sqlite3

DB_PATH = 'prices.db'

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as c:
        c.executescript('''
            CREATE TABLE IF NOT EXISTS products (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT    NOT NULL,
                url       TEXT    NOT NULL UNIQUE,
                selector  TEXT,
                threshold REAL,
                active    INTEGER DEFAULT 1,
                added_at  TEXT    DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS price_history (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id),
                price      REAL    NOT NULL,
                checked_at TEXT    DEFAULT (datetime('now'))
            );
        ''')
