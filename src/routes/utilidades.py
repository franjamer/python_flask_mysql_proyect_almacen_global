import database as db

def asegurar_fila_minima_auto(tabla):
    campos, valores = obtener_campos_y_valores_por_defecto(tabla)
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
    count = cursor.fetchone()[0]
    if count == 1:
        campos_str = ','.join(campos)
        placeholders = ','.join(['%s'] * len(valores))
        cursor.execute(f"INSERT INTO {tabla} ({campos_str}) VALUES ({placeholders})", tuple(valores))
        conn.commit()
    cursor.close()
    conn.close()

def obtener_campos_y_valores_por_defecto(nombre_tabla):
    """
    Devuelve dos listas: nombres de columnas (sin el id autoincremental)
    y valores por defecto válidos según el tipo de dato.
    """
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE, COLUMN_KEY
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s
        ORDER BY ORDINAL_POSITION
    """, (nombre_tabla,))
    columnas = []
    valores = []
    for col in cursor.fetchall():
        if col['COLUMN_KEY'] == 'PRI' and col['DATA_TYPE'] in ('int', 'bigint', 'smallint', 'mediumint', 'tinyint'):
            # Saltar el campo id autoincremental
            continue
        columnas.append(col['COLUMN_NAME'])
        tipo = col['DATA_TYPE']
        if tipo in ('int', 'bigint', 'smallint', 'mediumint', 'tinyint'):
            valores.append(0)
        elif tipo in ('float', 'double', 'decimal'):
            valores.append(0.0)
        elif tipo in ('varchar', 'char', 'text', 'longtext', 'mediumtext', 'tinytext'):
            valores.append('')
        elif tipo in ('date', 'datetime', 'timestamp'):
            valores.append(None)
        else:
            valores.append(None)
    cursor.close()
    conn.close()
    return columnas, valores