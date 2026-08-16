import json
import os
from datetime import date, datetime
from decimal import Decimal

# safe whitelist of tables
TABLAS_PERMITIDAS = [
    'perfiles', 'operadores', 'situacion_tabla', 'inventario_tabla',
    'movimientos_tabla', 'pedidos_global_tabla', 'lineas_pedido_tabla', 'proveedor_tabla'
]


def _serialize_row(row):
    # row is expected to be a dict
    serialized = {}
    for k, v in row.items():
        if isinstance(v, (date, datetime)):
            serialized[k] = v.isoformat()
        elif isinstance(v, Decimal):
            # keep as string to preserve precision
            serialized[k] = str(v)
        elif isinstance(v, (bytes, bytearray)):
            try:
                serialized[k] = v.decode('utf-8')
            except Exception:
                serialized[k] = str(v)
        else:
            serialized[k] = v
    return serialized


def export_tables(conn, tables):
    result = {}
    cursor = conn.cursor(dictionary=True)
    try:
        for t in tables:
            if t not in TABLAS_PERMITIDAS:
                result[t] = {'error': 'tabla no permitida'}
                continue
            try:
                cursor.execute(f"SELECT * FROM {t}")
                rows = cursor.fetchall()
                # serialize rows
                result[t] = [_serialize_row(r) for r in rows]
            except Exception as e:
                result[t] = {'error': str(e)}
    finally:
        cursor.close()
    return result


def save_export_to_file(data, folder, prefix='export_registros'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = f"{prefix}_{int(datetime.utcnow().timestamp())}.json"
    path = os.path.join(folder, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename, path


def import_data(conn, data, replace=False):
    cursor = conn.cursor()
    try:
        for t, rows in data.items():
            if t not in TABLAS_PERMITIDAS:
                continue
            if not isinstance(rows, list):
                continue
            if replace:
                cursor.execute(f"DELETE FROM {t}")
            for row in rows:
                if not isinstance(row, dict):
                    continue
                cols = ','.join(row.keys())
                placeholders = ','.join(['%s'] * len(row))
                vals = tuple(row.values())
                try:
                    cursor.execute(f"INSERT INTO {t} ({cols}) VALUES ({placeholders})", vals)
                except Exception:
                    # ignore individual row errors
                    pass
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


def delete_tables_data(conn, tables):
    cursor = conn.cursor()
    try:
        for t in tables:
            if t not in TABLAS_PERMITIDAS:
                continue
            try:
                cursor.execute(f"DELETE FROM {t}")
            except Exception:
                pass
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
