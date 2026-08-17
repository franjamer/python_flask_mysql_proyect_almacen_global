import os
import time
import sqlite3
from typing import Optional

DB_ENGINE = os.getenv('DB_ENGINE', 'mysql').lower()

try:
    import mysql.connector
except Exception:
    mysql = None


class SQLiteCursorWrapper:
    def __init__(self, cur, dict_rows=False):
        self.cur = cur
        self.dict_rows = dict_rows

    def execute(self, query, params=None):
        # SQLite uses ? placeholders; allow using %s in existing code and translate
        if params is None:
            params = ()
        if isinstance(query, str) and '%s' in query:
            query = query.replace('%s', '?')
        return self.cur.execute(query, params)

    def executemany(self, query, seq_of_params):
        if isinstance(query, str) and '%s' in query:
            query = query.replace('%s', '?')
        return self.cur.executemany(query, seq_of_params)

    def fetchall(self):
        rows = self.cur.fetchall()
        if self.dict_rows:
            return [dict(row) for row in rows]
        return rows

    def fetchone(self):
        row = self.cur.fetchone()
        if self.dict_rows and row is not None:
            return dict(row)
        return row

    def close(self):
        try:
            self.cur.close()
        except Exception:
            pass


class SQLiteConnectionWrapper:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def cursor(self, dictionary=False):
        return SQLiteCursorWrapper(self.conn.cursor(), dict_rows=dictionary)

    def commit(self):
        return self.conn.commit()

    def rollback(self):
        return self.conn.rollback()

    def close(self):
        return self.conn.close()


def get_connection(retries: int = 5, retry_delay: int = 2) -> Optional[object]:
    """Return a DB connection object. Supports MySQL (default) and SQLite when DB_ENGINE=sqlite.
    For MySQL, returns a mysql.connector connection. For SQLite, returns a SQLiteConnectionWrapper.
    """
    if DB_ENGINE == 'sqlite':
        # path from env or default to data/sqlite.db inside project
        sqlite_path = os.getenv('SQLITE_PATH', os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db'))
        os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
        try:
            return SQLiteConnectionWrapper(sqlite_path)
        except Exception as e:
            print(f"Error abriendo SQLite: {e}")
            return None

    # default: mysql
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASS', 'root')
    database = os.getenv('DB_NAME', 'almacenrepuestos')

    if mysql is None:
        print('mysql-connector not available')
        return None

    for i in range(retries):
        try:
            conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
            return conn
        except mysql.connector.Error as err:
            print(f"Intento {i+1}/{retries}: Error al conectar con MySQL: {err}")
            if i < retries - 1:
                time.sleep(retry_delay)
            else:
                return None