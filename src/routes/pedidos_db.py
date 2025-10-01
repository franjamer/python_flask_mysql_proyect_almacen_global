import database as db

def obtener_inventario():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT referencia, nombre FROM inventario_tabla")
    inventario = cursor.fetchall()
    cursor.close()
    conn.close()
    return inventario

def obtener_pedidos(columnas):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, referencia_pedido, fecha_creacion, completo FROM pedidos_global_tabla ORDER BY id DESC LIMIT 50")
    pedidos_raw = cursor.fetchall()
    pedidos = [dict(zip(columnas, pedido)) for pedido in pedidos_raw]
    cursor.close()
    conn.close()
    return pedidos

def obtener_lineas_pedido(pedido_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lineas_pedido_tabla WHERE pedido_id = %s", (pedido_id,))
    lineas = cursor.fetchall()
    cursor.close()
    conn.close()
    return lineas

def obtener_pedido_cabecera(pedido_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT referencia_pedido, fecha_creacion FROM pedidos_global_tabla WHERE id = %s", (pedido_id,))
    pedido = cursor.fetchone()
    cursor.close()
    conn.close()
    return pedido

def insertar_pedido(referencia_pedido, fecha_creacion, lineas, obtener_nombre_articulo):
    conn = db.get_connection()
    cursor = conn.cursor()
    completo = False
    cursor.execute("""
        INSERT INTO pedidos_global_tabla (referencia_pedido, fecha_creacion, completo)
        VALUES (%s, %s, %s)
    """, (referencia_pedido, fecha_creacion, completo))
    pedido_id = cursor.lastrowid

    for linea in lineas:
        referencia, cantidad_pedida, cantidad_recibida, fecha_recibido = linea
        cantidad_pedida = int(cantidad_pedida)
        cantidad_recibida = int(cantidad_recibida) if cantidad_recibida else 0
        completo_linea = cantidad_pedida == cantidad_recibida
        nombre_articulo = obtener_nombre_articulo(cursor, referencia)
        cursor.execute("""
            INSERT INTO lineas_pedido_tabla
            (pedido_id, referencia_articulo, nombre_articulo, cantidad_pedida, cantidad_recibida, fecha_recibido, completo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (pedido_id, referencia, nombre_articulo, cantidad_pedida, cantidad_recibida, fecha_recibido, completo_linea))

    cursor.execute("""
        SELECT COUNT(*) FROM lineas_pedido_tabla WHERE pedido_id = %s AND completo = 0
    """, (pedido_id,))
    incompletas = cursor.fetchone()[0]
    if incompletas == 0:
        cursor.execute(
            "UPDATE pedidos_global_tabla SET completo = 1 WHERE id = %s", (pedido_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return pedido_id

def actualizar_linea_pedido(linea_id, cantidad_pedida, cantidad_recibida, fecha_recibido):
    conn = db.get_connection()
    cursor = conn.cursor()
    if not fecha_recibido:
        cursor.execute(
            "SELECT fecha_recibido FROM lineas_pedido_tabla WHERE id = %s", (linea_id,))
        result = cursor.fetchone()
        fecha_recibido = result[0] if result else None

    completo = cantidad_recibida >= cantidad_pedida

    cursor.execute("""
        UPDATE lineas_pedido_tabla
        SET cantidad_pedida = %s,
            cantidad_recibida = %s,
            fecha_recibido = %s,
            completo = %s
        WHERE id = %s
    """, (cantidad_pedida, cantidad_recibida, fecha_recibido, completo, linea_id))

    cursor.execute(
        "SELECT pedido_id FROM lineas_pedido_tabla WHERE id = %s", (linea_id,))
    pedido_id_db = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM lineas_pedido_tabla WHERE pedido_id = %s AND completo = 0", (pedido_id_db,))
    incompletas = cursor.fetchone()[0]
    cursor.execute("UPDATE pedidos_global_tabla SET completo = %s WHERE id = %s",
                   (incompletas == 0, pedido_id_db))

    conn.commit()
    cursor.close()
    conn.close()
    return pedido_id_db

def eliminar_pedido(pedido_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM lineas_pedido_tabla WHERE pedido_id = %s", (pedido_id,))
    cursor.execute(
        "DELETE FROM pedidos_global_tabla WHERE id = %s", (pedido_id,))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_linea(linea_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT pedido_id FROM lineas_pedido_tabla WHERE id = %s", (linea_id,))
    result = cursor.fetchone()
    if not result:
        cursor.close()
        conn.close()
        return None
    pedido_id_db = result[0]
    cursor.execute(
        "SELECT COUNT(*) FROM lineas_pedido_tabla WHERE pedido_id = %s", (pedido_id_db,))
    num_lineas = cursor.fetchone()[0]
    if num_lineas > 1:
        cursor.execute(
            "DELETE FROM lineas_pedido_tabla WHERE id = %s", (linea_id,))
        conn.commit()
    cursor.close()
    conn.close()
    return pedido_id_db

def modificar_pedido(pedido_id, referencia_pedido, fecha_creacion, lineas, obtener_nombre_articulo):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pedidos_global_tabla
        SET referencia_pedido = %s, fecha_creacion = %s
        WHERE id = %s
    """, (referencia_pedido, fecha_creacion, pedido_id))

    cursor.execute(
        "DELETE FROM lineas_pedido_tabla WHERE pedido_id = %s", (pedido_id,))

    for linea in lineas:
        referencia, cantidad_pedida, cantidad_recibida, fecha_recibido = linea
        cantidad_pedida = int(cantidad_pedida)
        cantidad_recibida = int(cantidad_recibida) if cantidad_recibida else 0
        completo_linea = cantidad_pedida == cantidad_recibida
        nombre_articulo = obtener_nombre_articulo(cursor, referencia)
        cursor.execute("""
            INSERT INTO lineas_pedido_tabla
            (pedido_id, referencia_articulo, nombre_articulo, cantidad_pedida, cantidad_recibida, fecha_recibido, completo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (pedido_id, referencia, nombre_articulo, cantidad_pedida, cantidad_recibida, fecha_recibido, completo_linea))

    cursor.execute(
        "SELECT COUNT(*) FROM lineas_pedido_tabla WHERE pedido_id = %s AND completo = 0", (pedido_id,))
    incompletas = cursor.fetchone()[0]
    cursor.execute(
        "UPDATE pedidos_global_tabla SET completo = %s WHERE id = %s", (incompletas == 0, pedido_id))

    conn.commit()
    cursor.close()
    conn.close()