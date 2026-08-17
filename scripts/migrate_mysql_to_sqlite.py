"""
Script sencillo para migrar datos desde MySQL hacia SQLite.
Uso: exporta todas las tablas listadas en `TABLAS_PERMITIDAS` (si existe) y crea tablas con columnas TEXT en SQLite.
Advertencia: este script no reproduce tipos exactos, constraints ni FK; sirve para migración de datos
rápida para empaquetado de una app de escritorio.
"""
import os
import sys
import sqlite3
import json
import base64

try:
    import mysql.connector
except Exception as e:
    print('mysql-connector no está instalado. Instálalo para usar este script.')
    raise

# leer configuración desde variables de entorno
MYSQL_HOST = os.getenv('DB_HOST', 'localhost')
MYSQL_USER = os.getenv('DB_USER', 'root')
MYSQL_PASS = os.getenv('DB_PASS', 'root')
MYSQL_DB = os.getenv('DB_NAME', 'almacenrepuestos')

SQLITE_PATH = os.getenv('SQLITE_PATH', os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db'))
os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)

# opcional: lista de tablas a migrar desde utils
TABLAS = None
try:
    from src.utils.data_admin import TABLAS_PERMITIDAS
    TABLAS = TABLAS_PERMITIDAS
except Exception:
    TABLAS = None

if TABLAS is None:
    print('No se encontró TABLAS_PERMITIDAS, se utilizarán todas las tablas de la BD MySQL.')


def fetch_tables_from_mysql(conn):
    cur = conn.cursor(buffered=True)
    try:
        cur.execute("SHOW TABLES")
        rows = cur.fetchall()
        return [row[0] for row in rows]
    finally:
        cur.close()


def main():
    src = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASS, database=MYSQL_DB)

    if TABLAS:
        tables = TABLAS
    else:
        tables = fetch_tables_from_mysql(src)

    dst = sqlite3.connect(SQLITE_PATH)
    dst.row_factory = sqlite3.Row
    dst_cur = dst.cursor()

    for t in tables:
        print(f'Migrando tabla {t}...')
        # use a buffered cursor for metadata and selects to avoid unread-result errors
        meta_cur = src.cursor(buffered=True)
        try:
            try:
                meta_cur.execute(f"SELECT * FROM {t} LIMIT 0")
            except Exception as e:
                print(f'Error accediendo a {t}: {e}')
                continue
            # capture column names from meta_cur before closing
            cols = [d[0] for d in meta_cur.description]
        finally:
            meta_cur.close()
        # crear tabla en sqlite (todas las columnas TEXT)
        col_defs = ','.join([f'"{c}" TEXT' for c in cols])
        dst_cur.execute(f'DROP TABLE IF EXISTS "{t}"')
        dst_cur.execute(f'CREATE TABLE "{t}" ({col_defs})')
        dst.commit()
        # fetch rows using a fresh buffered cursor
        data_cur = src.cursor(buffered=True)
        try:
            data_cur.execute(f"SELECT * FROM {t}")
            rows = data_cur.fetchall()
        finally:
            data_cur.close()
        if not rows:
            print('  sin filas')
            continue
        placeholders = ','.join(['?'] * len(cols))
        insert_sql = f'INSERT INTO "{t}" ({",".join(["\""+c+"\"" for c in cols])}) VALUES ({placeholders})'
        batch = []
        for r in rows:
            converted = []
            for v in r:
                if v is None:
                    converted.append(None)
                elif isinstance(v, (bytes, bytearray)):
                    converted.append(base64.b64encode(v).decode('ascii'))
                else:
                    converted.append(str(v))
            batch.append(tuple(converted))
        try:
            dst_cur.executemany(insert_sql, batch)
            dst.commit()
            print(f'  insertadas {len(batch)} filas')
        except Exception as e:
            print(f'  error insertando filas en {t}: {e}')

    src.close()
    dst_cur.close()
    dst.close()
    print('Migración finalizada. SQLite en:', SQLITE_PATH)


if __name__ == '__main__':
    main()
